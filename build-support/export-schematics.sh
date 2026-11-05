#!/usr/bin/env bash
# Regenerates docs/img/schematics.pdf (all sheets) and docs/img/sch/*.svg (one per sheet)
# from hardware/GCC-Wireless.kicad_sch, and the ERC report docs/img/sch/erc.json.
# Needs KiCad 10 (override the path with KICAD_CLI). Run from anywhere in Git Bash.
set -euo pipefail
KC="${KICAD_CLI:-C:/Program Files/KiCad/10.0/bin/kicad-cli.exe}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCH="$ROOT/hardware/GCC-Wireless.kicad_sch"
OUT="$ROOT/docs/img"
mkdir -p "$OUT/sch"
rm -f "$OUT"/sch/*.svg
"$KC" sch export pdf -o "$OUT/schematics.pdf" "$SCH"
"$KC" sch export svg -o "$OUT/sch" "$SCH"
# ERC is allowed to find upstream's errors in the Phob sheet; it must still run.
# KiCad names each file "GCC-Wireless-<sheet name>.svg"; make the names URL-friendly.
for f in "$OUT"/sch/GCC-Wireless*.svg; do
  b="$(basename "$f" .svg)"; n="$(echo "${b#GCC-Wireless}" | sed 's/^-//; s/[ ()!]/_/g')"
  [ -z "$n" ] && n=root
  mv "$f" "$OUT/sch/$n.svg"
done
"$KC" sch erc --severity-all --format json -o "$OUT/sch/erc.json" "$SCH" || true
ls -la "$OUT/schematics.pdf" "$OUT"/sch
