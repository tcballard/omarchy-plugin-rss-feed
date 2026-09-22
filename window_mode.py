#!/usr/bin/python3
"""Apply RSS Feed's window mode to its own mapped Hyprland window."""

import argparse
import json
import os
import re
import subprocess
import sys
import time


def hyprctl(*arguments):
    result = subprocess.run(["hyprctl", *arguments], capture_output=True, text=True, timeout=2)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Hyprland command failed")
    return result.stdout


def reader_client(clients, pid):
    matches = [client for client in clients
               if client.get("pid") == pid and client.get("title") == "RSS Feed"
               and client.get("mapped", True) and not client.get("hidden", False)]
    if len(matches) > 1:
        raise ValueError("More than one RSS Feed window belongs to this shell")
    if not matches:
        return None
    address = matches[0].get("address", "")
    if not re.fullmatch(r"0x[0-9a-fA-F]+", address):
        raise ValueError("Invalid RSS Feed window address")
    return matches[0]


def floating_size(client, monitors):
    monitor = next((item for item in monitors if item.get("id") == client.get("monitor")), None)
    if monitor is None:
        raise ValueError("RSS Feed's monitor is unavailable")
    scale = float(monitor.get("scale", 1))
    if scale <= 0:
        raise ValueError("Invalid monitor scale")
    width, height = float(monitor["width"]), float(monitor["height"])
    if int(monitor.get("transform", 0)) % 2:
        width, height = height, width
    left, top, right, bottom = monitor.get("reserved", [0, 0, 0, 0])
    return (min(1040, max(720, int(width / scale - left - right - 32))),
            min(720, max(480, int(height / scale - top - bottom - 32))))


def commands(client, mode, monitors):
    # Address validation is repeated at the command boundary. Never dispatch
    # against the active window: focus may have moved since the reader opened.
    address = client.get("address", "")
    if not re.fullmatch(r"0x[0-9a-fA-F]+", address):
        raise ValueError("Invalid RSS Feed window address")
    target = f'window = "address:{address}"'
    if mode == "Tiled":
        return [f'hl.dsp.window.float({{ {target}, action = "unset" }})']
    if mode != "Centred floating":
        raise ValueError("Unknown window mode")
    width, height = floating_size(client, monitors)
    return [f'hl.dsp.window.float({{ {target}, action = "set" }})',
            f'hl.dsp.window.resize({{ {target}, x = {width}, y = {height} }})',
            f'hl.dsp.window.center({{ {target} }})']


def apply(mode, pid, attempts=12):
    for attempt in range(attempts):
        client = reader_client(json.loads(hyprctl("-j", "clients")), pid)
        if client:
            monitors = json.loads(hyprctl("-j", "monitors")) if mode == "Centred floating" else []
            for command in commands(client, mode, monitors):
                result = hyprctl("dispatch", command).strip()
                if result != "ok":
                    raise RuntimeError(result or "Hyprland did not acknowledge the window command")
            return
        if attempt + 1 < attempts:
            time.sleep(0.08)
    raise RuntimeError("RSS Feed window did not map in time")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["Tiled", "Centred floating"])
    args = parser.parse_args()
    try:
        # Quickshell's Process launches this helper directly, making its PID
        # the parent PID. Other applications with the same title are excluded.
        apply(args.mode, os.getppid())
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.SubprocessError) as error:
        print(f"Could not apply RSS Feed window mode: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
