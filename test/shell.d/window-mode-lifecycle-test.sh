#!/bin/bash
set -euo pipefail
source "$(dirname "$0")/base-test.sh"
run_node_test <<'JS'
const fs = require('fs')
const vm = require('vm')
const panel = fs.readFileSync(path.join(root, 'Panel.qml'), 'utf8')
const manager = fs.readFileSync(path.join(root, 'FeedManager.qml'), 'utf8')
function body(source, name) {
  const match = source.match(new RegExp('  function ' + name + '\\([^)]*\\) \\{([\\s\\S]*?)\\n  \\}'))
  if (!match) throw new Error('Missing function ' + name)
  return match[1]
}
let starts = 0, stops = 0, popupsClosed = 0
const state = {
  opened: false, windowModePending: false, windowModeError: 'previous failure',
  windowModeTimer: {restart() { starts++ }, stop() { stops++ }},
  markReadTimer: {stop() {}},
  windowModeProcess: {running: true}, window: {visible: true},
  feedManager: {dismissPopup() { popupsClosed++ }}
}
vm.createContext(state)
vm.runInContext('function request() {' + body(panel, 'requestWindowMode') + '}\nfunction close() {' + body(panel, 'close') + '}', state)
state.request()
assertEqual(starts, 0, 'hidden reader does not schedule window operations')
state.opened = true
state.request()
assert(state.windowModePending && state.windowModeError === '', 'mode changes queue application and clear old errors')
assertEqual(starts, 1, 'open reader schedules window-mode application')
state.close()
assert(!state.opened && !state.windowModePending && !state.windowModeProcess.running && !state.window.visible,
       'closing cancels pending and running placement work and hides the reader')
assertEqual(stops, 1, 'closing stops the placement timer')
assertEqual(popupsClosed, 1, 'closing also dismisses the window-mode dropdown')

let saved = null
const configuration = {news: {settings: {enabledFeeds:['hacker-news'], customFeeds:'https://example.com/rss', feedCollections:'[]'}},
  shell: {updateEntryInline(id, settings) { saved = {id, settings} }}}
vm.createContext(configuration)
vm.runInContext('function persistSettings(values) {' + body(manager, 'persistSettings') + '}', configuration)
configuration.persistSettings({windowMode:'Centred floating'})
assertEqual(saved.id, 'io.github.tcballard.rss-feed', 'window-mode preference is persisted under this plugin')
assertEqual(saved.settings.windowMode, 'Centred floating', 'floating preference reaches persistent shell settings')
assertEqual(saved.settings.customFeeds, 'https://example.com/rss', 'window-mode change preserves subscriptions')
assertEqual(saved.settings.feedCollections, '[]', 'window-mode change preserves collections')
configuration.persistSettings({windowMode:'Tiled'})
assertEqual(saved.settings.windowMode, 'Tiled', 'returning to tiled replaces the saved preference')
JS
