#!/usr/bin/env bash
# Builds upstream/gcwireless_bridge (RP2040 firmware) on Windows/Git Bash with no host C compiler.
# Needs: CMake, Ninja, Arm GNU Toolchain 14.x (set ARM_TC), gh CLI (downloads prebuilt pioasm/picotool).
# Work files go to $WORK (default ~/.cache/gcc-wireless), not into the repo.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd -W 2>/dev/null || pwd)"
WORK="${WORK:-$HOME/.cache/gcc-wireless}"
ARM_TC="${ARM_TC:-C:/Program Files (x86)/Arm GNU Toolchain arm-none-eabi/14.2 Rel1}"
SDK_VER=2.1.1; TOOLS_TAG=v2.1.1-3
mkdir -p "$WORK/tools"; cd "$WORK"
[ -d pico-sdk ] || git clone -q --depth 1 --branch "$SDK_VER" https://github.com/raspberrypi/pico-sdk.git pico-sdk
if [ ! -d tools/pioasm ]; then
  (cd tools && gh release download "$TOOLS_TAG" -R raspberrypi/pico-sdk-tools \
     -p "pico-sdk-tools-$SDK_VER-x64-win.zip" -p "picotool-$SDK_VER-x64-win.zip" --clobber && unzip -oq "*.zip")
fi
W="$(pwd -W)"
export PICO_SDK_PATH="$W/pico-sdk"
export PATH="/c/Program Files/CMake/bin:$PATH"
B="${BUILD_DIR:-$W/bb}"   # keep this path short (CMake's 250-char object-path limit)
cmake -G Ninja -S "$REPO/upstream/gcwireless_bridge" -B "$B" \
  -Dpioasm_DIR="$W/tools/pioasm" -Dpicotool_DIR="$W/tools/picotool" \
  -DPICO_BOARD=pico -DPICO_TOOLCHAIN_PATH="$ARM_TC" >/dev/null
cmake --build "$B"
ls -la "$B"/gcwireless_bridge.uf2
