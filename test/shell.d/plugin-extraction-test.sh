#!/bin/bash
set -euo pipefail
source "$(dirname "$0")/base-test.sh"
run_node_test <<'JS'
const fs = require('fs')
const vm = require('vm')
const service = fs.readFileSync(path.join(root, 'Service.qml'), 'utf8')
const expression = service.match(/readonly property string helperPath: (.+)/)[1]
const location = '/tmp/RSS reader #1/fetch_news.py'
const helper = vm.runInNewContext(expression, {
  Qt: {resolvedUrl: name => new URL('file://' + encodeURI('/tmp/RSS reader ')+ '%231/' + name)}
})
assertEqual(helper, location, 'helper resolves beside installed plugin, including spaces and escaped characters')

const palette = fs.readFileSync(path.join(root, 'ReaderPalette.qml'), 'utf8')
const load = palette.match(/function load\(raw\) \{([\s\S]*?)\n  \}/)[1]
const context = {values: {green: '#000000'}}
vm.createContext(context)
vm.runInContext('function load(raw) {' + load + '}', context)
context.load('green = "#123456"\ncolor4 = "#abcdef"')
assertEqual(context.values.green, '#123456', 'reader palette accepts semantic theme colours')
assertEqual(context.values.color4, '#abcdef', 'reader palette preserves ANSI fallback colours')
context.load('blue = "#654321"')
assert(context.values.green === undefined, 'theme changes clear colours absent from the next theme')
context.load('green = "not a colour"')
assertEqual(Object.keys(context.values).length, 0, 'invalid palette values use shell colour fallbacks')

for (const name of ['Panel.qml', 'BarWidget.qml', 'FeedManager.qml']) {
  const source = fs.readFileSync(path.join(root, name), 'utf8')
  assert(!source.includes('"omarchy.news"'), name + ' targets the independent plugin ID')
}
JS
