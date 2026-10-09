# Corne-ish Zen V2 ZMK config

My 5-column Corne keymap
([corne-wireless-5-col-view-zmk-config](https://github.com/itsjoaos/corne-wireless-5-col-view-zmk-config))
on a Corne-ish Zen V2. The keymap selects the Zen's 5-column layout, so the
outer column on each half is unmapped and key positions (for combos) are the
same as on the Corne.

## Changing the keymap

1. Edit [`config/corneish_zen.keymap`](config/corneish_zen.keymap).
2. Run `python3 scripts/align_keymap.py` to line the layers back up.
3. Commit and push. GitHub Actions builds the firmware.

The script only rewrites the whitespace inside each layer's `bindings`: three
rows of columns, thumb keys under the inner columns, column widths shared by
all layers. It needs Python 3 and nothing else. Set `HAND_GAP` at the top of
the script to put extra space between the two halves.

## Flashing

1. Open the latest run under **Actions** and download the `firmware` artifact.
   It unzips to `corneish_zen_v2_left-zmk.uf2` and
   `corneish_zen_v2_right-zmk.uf2`.
2. Plug the left half in over USB and double-press its reset button. It shows
   up as a USB drive.
3. Copy the left `.uf2` file onto the drive. The half restarts by itself and
   the drive disappears.
4. Do the same for the right half with the right file.

After a keymap-only change, only the left half needs flashing. After a change
to `config/corneish_zen.conf` or to the ZMK version, flash both.

## ZMK version

Pinned to ZMK v0.3 in both [`config/west.yml`](config/west.yml) and
[`.github/workflows/build.yml`](.github/workflows/build.yml); the two must
match. On ZMK `main` the boards are named `corneish_zen_left//zmk` and
`corneish_zen_right//zmk` instead, so [`build.yaml`](build.yaml) has to change
with them.
