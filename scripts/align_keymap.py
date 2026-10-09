#!/usr/bin/env python3
"""Re-align the layer bindings of a ZMK keymap for a Corne-shaped board.

    python3 scripts/align_keymap.py [KEYMAP ...]    (default: config/*.keymap)

Every layer becomes three rows of columns plus a row of six thumb keys under
the inner columns. Column widths are shared by all layers, so the layers line
up with each other. Layers may have 36 keys (5 columns per half) or 42 keys
(6 columns per half). Nothing outside the layers' `bindings` is changed.
"""
import re
import sys
from pathlib import Path

INDENT = "  "  # in front of every row
HAND_GAP = 0  # extra spaces between the left and right halves
THUMBS = 6

BINDINGS = re.compile(r"((?<![\w-])bindings\s*=\s*<)(.*?)(\s*>;)", re.S)


def keymap_span(text):
    """Offsets of the braces enclosing the `zmk,keymap` node."""
    start = text.rindex("{", 0, text.index('compatible = "zmk,keymap"'))
    depth = 0
    for end in range(start, len(text)):
        depth += {"{": 1, "}": -1}.get(text[end], 0)
        if depth == 0:
            return start, end
    raise ValueError("unbalanced braces in the keymap node")


def split_bindings(block):
    """'&kp A &lt 1 B' -> ['&kp A', '&lt 1 B']"""
    if "//" in block or "/*" in block:
        raise ValueError("comments inside `bindings` are not supported")
    keys = []
    for word in block.split():
        if word.startswith("&"):
            keys.append(word)
        elif keys:
            keys[-1] += " " + word
        else:
            raise ValueError(f"expected a binding starting with '&', got '{word}'")
    return keys


def row_columns(count):
    """The column of every key, row by row, for a layer of `count` keys."""
    columns, rest = divmod(count - THUMBS, 3)
    if rest or columns not in (10, 12):
        raise ValueError(f"a layer has {count} bindings, expected 36 or 42")
    first = (columns - THUMBS) // 2
    return [range(columns)] * 3 + [range(first, first + THUMBS)]


def align(text):
    start, end = keymap_span(text)
    layers = [split_bindings(m[2]) for m in BINDINGS.finditer(text, start, end)]
    if len({len(keys) for keys in layers}) != 1:
        raise ValueError(f"layers differ in size: {[len(keys) for keys in layers]}")
    rows = row_columns(len(layers[0]))
    columns = [column for row in rows for column in row]

    widths = [0] * len(rows[0])
    for keys in layers:
        for column, key in zip(columns, keys):
            widths[column] = max(widths[column], len(key))

    def render(match):
        keys = iter(split_bindings(match[2]))
        lines = []
        for row in rows:
            cells = [""] * len(widths)
            for column in row:
                cells[column] = next(keys)
            cells = [cell.ljust(width) for cell, width in zip(cells, widths)]
            half = len(cells) // 2
            hands = " ".join(cells[:half]), " ".join(cells[half:])
            lines.append((INDENT + (" " * (1 + HAND_GAP)).join(hands)).rstrip())
        return match[1] + "\n" + "\n".join(lines) + match[3]

    return text[:start] + BINDINGS.sub(render, text[start:end]) + text[end:]


def main():
    root = Path(__file__).resolve().parent.parent
    paths = [Path(arg) for arg in sys.argv[1:]] or sorted(root.glob("config/*.keymap"))
    for path in paths:
        old = path.read_text()
        try:
            new = align(old)
        except ValueError as error:
            sys.exit(f"{path}: {error}")
        if new != old:
            path.write_text(new)
        print(f"{path}: {'re-aligned' if new != old else 'already aligned'}")


if __name__ == "__main__":
    main()
