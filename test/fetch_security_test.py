#!/usr/bin/env python3
"""Adversarial fixtures for the feed-to-reader trust boundary; no network."""
import importlib.util
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('reader', ROOT / 'fetch_news.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


def address(ip):
    return (socket.AF_INET, socket.SOCK_STREAM, 6, '', (ip, 443))


class FeedSecurityTests(unittest.TestCase):
    def test_socket_connects_to_validated_address_without_resolving_again(self):
        sock = Mock()
        with patch.object(r.socket, 'getaddrinfo', side_effect=[[address('8.8.8.8')], [address('127.0.0.1')]]) as dns, patch.object(r.socket, 'socket', return_value=sock):
            self.assertIs(r.public_connection(('feed.example', 443)), sock)
            dns.assert_called_once()
            sock.connect.assert_called_once_with(('8.8.8.8', 443))

    def test_mixed_public_and_private_dns_never_opens_a_socket(self):
        for ip in ('127.0.0.1', '10.0.0.1', '169.254.169.254', '0.0.0.0'):
            with self.subTest(ip=ip), patch.object(r.socket, 'getaddrinfo', return_value=[address('8.8.8.8'), address(ip)]), patch.object(r.socket, 'socket') as create:
                with self.assertRaises(ValueError):
                    r.public_connection(('feed.example', 443))
                create.assert_not_called()

    def test_tls_keeps_original_hostname_and_certificate_checks(self):
        conn = r.PublicHTTPSConnection('feed.example', context=r.SSL_CONTEXT)
        sock = Mock()
        with patch.object(r.socket, 'getaddrinfo', return_value=[address('8.8.8.8')]), patch.object(r.socket, 'socket', return_value=sock), patch.object(r.SSL_CONTEXT, 'wrap_socket', return_value=sock) as wrap:
            conn.connect()
            wrap.assert_called_once_with(sock, server_hostname='feed.example')
        self.assertTrue(r.SSL_CONTEXT.check_hostname)
        self.assertEqual(r.SSL_CONTEXT.verify_mode, r.ssl.CERT_REQUIRED)

    def test_failed_connection_closes_socket_and_tries_next_public_address(self):
        failed, good = Mock(), Mock()
        failed.connect.side_effect = OSError('unreachable')
        with patch.object(r.socket, 'getaddrinfo', return_value=[address('8.8.8.8'), address('1.1.1.1')]), patch.object(r.socket, 'socket', side_effect=[failed, good]):
            self.assertIs(r.public_connection(('feed.example', 443)), good)
            failed.close.assert_called_once()

    def test_malformed_urls_are_rejected_without_aborting_other_items(self):
        for value in ('https://[broken', 'https://example.com:bad/', 'file:///tmp/item', 'javascript:alert(1)'):
            self.assertEqual(r.external_url(value), '')
            self.assertEqual(r.canonical_feed_url(value), '')
        feed = b'<rss><channel><item><title>Bad</title><link>https://[broken</link></item><item><title>Good</title><link>https://omarchy.org/news/good</link></item></channel></rss>'
        self.assertEqual([x['title'] for x in r.parse_feed(feed)], ['Good'])
        self.assertNotIn('<a ', r.article_markup('<a href="https://[broken">text</a>'))

    def test_xml_entities_depth_and_bytes_are_bounded(self):
        payloads = [b'<!DOCTYPE rss [<!ENTITY a "expanded">]><rss><channel><title>&a;</title></channel></rss>', ('<a>' * 129 + '</a>' * 129).encode(), b'x' * (r.MAX_RESPONSE_BYTES + 1)]
        for payload in payloads:
            with self.subTest(size=len(payload)), self.assertRaises(ValueError):
                r.feed_root(payload)

    def test_markup_drops_active_content_and_bounds_link_expansion(self):
        markup = r.article_markup('<script>bad</script><img src="https://tracker.example/a"><a href="file:///tmp/x">file</a><a href="https://example.com">good</a>')
        self.assertNotIn('script', markup)
        self.assertNotIn('img', markup)
        self.assertNotIn('file:', markup)
        self.assertIn('href="https://example.com"', markup)
        self.assertLessEqual(len(r.article_markup('<a href="/">x</a>' * 4000, base_url='https://' + 'a' * 1900 + '.example/post')), r.MAX_MARKUP_CHARS)

    def test_cache_is_bounded_and_resanitized(self):
        source = r.SOURCE_CATALOG['omarchy']
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'feed.json'
            path.write_text(json.dumps({'items': [None, {'url': 'file:///tmp/secret', 'title': 'No'}, {'url': 'https://omarchy.org/news/one', 'title': 'Good', 'contentHtml': '<img src="file:///tmp/image"><a href="javascript:evil">bad</a><p>Safe</p>', 'author': {'unexpected': 'object'}, 'unexpected': 'discard me'}]}))
            with patch.object(r, 'cache_path', return_value=path):
                result = r.cached_result(source, 'offline')
                self.assertEqual(len(result['items']), 1)
                item = result['items'][0]
                self.assertEqual(item['author'], '')
                self.assertNotIn('unexpected', item)
                self.assertNotIn('file:', item['contentHtml'])
                self.assertNotIn('javascript:', item['contentHtml'])
                self.assertTrue(item['id'].startswith('omarchy:'))
                path.write_bytes(b' ' * (r.MAX_CACHE_BYTES + 1))
                self.assertIsNone(r.cached_result(source, ''))

    def test_broken_http_response_falls_back_to_cache(self):
        with patch.object(r, 'fetch', side_effect=r.http.client.IncompleteRead(b'partial')), patch.object(r, 'cached_result', return_value={'items': []}):
            items, state, error = r.load_source(r.SOURCE_CATALOG['omarchy'], '2026-09-22T00:00:00+00:00')
            self.assertTrue(state['stale'])
            self.assertIn('IncompleteRead', error)

    def test_deadline_terminates_blocked_worker_threads(self):
        code = "import fetch_news as r; from concurrent.futures import ThreadPoolExecutor; import time; r.install_deadline(1); pool=ThreadPoolExecutor(1); pool.submit(time.sleep, 60); pool.shutdown(wait=True)"
        result = subprocess.run([sys.executable, '-c', code], cwd=ROOT, capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 124)
        self.assertIn('time limit', result.stderr)


if __name__ == '__main__':
    unittest.main()
