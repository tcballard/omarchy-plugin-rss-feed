# Keyboard and mouse controls

## Global shortcut

**Super + Alt + N** opens or closes RSS Feed. It is named **RSS Feed** in Omarchy's keybinding list (**Super + K**).

After installing the plugin, run this once in your desktop terminal:

```bash
python3 ~/.config/omarchy/plugins/io.github.tcballard.rss-feed/scripts/keybindings.py
```

This adds a guarded include to `~/.config/hypr/bindings.lua`, backs up the exact previous file, reloads Hyprland and checks that the shortcut is active. Repeating it does not duplicate the binding. If another app uses the chord, it stops before editing your configuration. An existing shortcut for our original reader can be replaced.

The included Lua file ships with the plugin and follows its updates. The include checks that the file exists, so removing the plugin does not leave a broken `dofile`. Plugin installation itself does not execute setup hooks or alter your personal shortcuts.

## Choose a different shortcut

If Super + Alt + N is already in use, add a binding of your choice to `~/.config/hypr/bindings.lua` using this form, then run `hyprctl reload`:

```lua
o.bind("YOUR CHORD", "RSS Feed", "omarchy-shell shell toggle io.github.tcballard.rss-feed")
```

Replace `YOUR CHORD` with an unused chord supported by your Hyprland configuration. Don't run the default shortcut setup as well unless you want both shortcuts.

## Inside RSS Feed

Press **F** to open the feed manager. **Window mode** at the top offers **Tiled** (the default) and **Centred floating**. The preference is saved with your feeds and collections. Floating centres the reader on its own monitor, using a 1040 × 720 window reduced to fit the usable screen down to the reader's existing 720 × 480 minimum. It does not pin the window across workspaces or alter other applications. Escape dismisses an open mode dropdown before leaving the manager.

You can also select the same **Window mode** in the bar widget's settings. No Hyprland configuration edit or additional shortcut setup is needed. If you added the earlier manual `o.window({ title = "^RSS Feed$" }, ...)` rule, you can remove that rule; the built-in option now applies the chosen mode whenever RSS Feed opens.

| Key | Action |
| --- | --- |
| F | Manage feeds and collections |
| R | Refresh |
| O | Open the selected article on its original website |
| Up / Down or K / J | Select a headline, or scroll when reading |
| Right / L / Enter | Read the selected article |
| Left / H | Return focus to headlines |
| [ / ] | Previous / next source or collection |
| Page Up / Page Down / Space | Scroll the article |
| Home / End | Top / bottom of the article while reading |
| Escape | Return from feed management, or close the reader |

While editing a feed or collection, ordinary keys go to the controls instead of triggering reader shortcuts. Escape returns to the reader.

Click the bar icon to toggle RSS Feed; right-click it to refresh. The reader keeps its existing mouse controls, independent scrolling, article links and window buttons.

## Remove the shortcut

Before removing the plugin:

```bash
python3 ~/.config/omarchy/plugins/io.github.tcballard.rss-feed/scripts/keybindings.py --remove
omarchy plugin remove io.github.tcballard.rss-feed
```

Removal deletes only the marked include and retains other user bindings. If you already removed the plugin, delete the `BEGIN RSS Feed shortcut` through `END RSS Feed shortcut` block from `~/.config/hypr/bindings.lua`, then run `hyprctl reload`. The guarded block is otherwise inert after removal.
