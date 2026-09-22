pragma Singleton
import QtQuick
import Quickshell.Io
import qs.Commons

QtObject {
  id: root
  property var values: ({})
  readonly property color green: values.green || values.color2 || Color.accent
  readonly property color yellow: values.yellow || values.color3 || Color.urgent
  readonly property color cyan: values.cyan || values.color6 || Color.foreground
  readonly property color blue: values.blue || values.color4 || Color.accent
  readonly property color magenta: values.magenta || values.color5 || Color.accent

  function load(raw) {
    var next = ({})
    var lines = String(raw || "").split("\n")
    for (var i = 0; i < lines.length; i++) {
      var match = lines[i].match(/^\s*([A-Za-z0-9_-]+)\s*=\s*["']?(#[0-9A-Fa-f]{6})/)
      if (match) next[match[1]] = match[2]
    }
    values = next
  }

  property FileView paletteFile: FileView {
    path: Color.currentThemePath + "/colors.toml"
    watchChanges: true
    printErrors: false
    onLoaded: root.load(text())
    onFileChanged: reload()
    onLoadFailed: root.values = ({})
  }

  // Theme switches replace a symlink; the shell's theme notification also
  // reloads the path, even when the old file itself did not change.
  property Connections themeChanges: Connections {
    target: Color
    function onThemeShellValuesChanged() { root.paletteReload.restart() }
  }
  property Timer paletteReload: Timer {
    interval: 50
    onTriggered: root.paletteFile.reload()
  }
}
