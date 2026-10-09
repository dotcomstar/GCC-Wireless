# Build log

Newest entries at the bottom. Times are US Eastern.

## 2026-10-09 — Session 1: repo and toolchain

**Goal:** get the upstream code onto this machine and compile it.

1. `git init -b main`. A git repo records every change so we can go back and see what we did.
2. Added upstream projects as *submodules* (a submodule is a pointer to another repo at one exact commit) under `upstream/`:
   - `gcwireless` @ 576878d — nRF52 transmitter/receiver (nRF52 = Nordic's newer radio chip family).
   - `gcwireless_bridge` @ 5c31147 — Raspberry Pi Pico (RP2040 chip) that talks to the console.
   - `Wireless-PhobGCC-nRF24` @ c25004e — older nRF24 version, reference only.
   - `PhobGCC-SW` @ b4f175e (2025-11-15) — the controller firmware.
   Why pin commits: upstream can change; our notes must describe the code we actually read.
3. **Finding:** `gcwireless/.gitmodules` lists pico-rectangle and PhobGCC-SW, but the repo has no submodule entries (commit bd570f2 "remove submodules"). The stale file is harmless; we add PhobGCC-SW ourselves.
4. Installed tools: `uv tool install platformio` (PlatformIO = build system for microcontrollers), and with winget: Kitware.CMake, Ninja-build.Ninja, Arm.GnuArmEmbeddedToolchain (compiler for ARM chips). CMake+Ninja are for the Pico bridge.
5. **Failure:** `pio run` in gcwireless -> `UnknownBoard: Unknown board ID 'nicenano'`.
   Cause: platform nordicnrf52 11.0.0 ships no `nicenano` board file. Upstream's author presumably had one locally (unverified).
   Workaround: `build-support/boards/nicenano.json`, copied from the Adafruit Feather nRF52840 definition, used via `PLATFORMIO_BOARDS_DIR`. **It is a stand-in:** it proves the code compiles, but pin numbers may not match a real nice!nano. Verify before wiring.

## 2026-10-09 — Session 1 (cont.): second failure, nRF52 build still blocked

6. Ran `pio run` with the stand-in board. Both envs fail: `'PIN_017' was not declared` (also PIN_020/022/024/031 in `src/tx.cpp`, `src/rx.cpp`).
   Cause: `PIN_0xx` names are not defined by the Adafruit nRF52 core (checked variants list: feather, itsybitsy, metro, pca10056, etc.; none define them). They must come from a nice!nano-specific variant that upstream's author had locally. I could not find it (one web search, GitHub variants listing).
   Status: **TX and RX firmware do not yet build.** Next options: (a) find the nice!nano variant (ask Heather via a GitHub issue on gcwireless), (b) translate PIN_0xx to the P0.xx/P1.xx GPIO numbers via the nRF52840 pin map and add a small header. Option (b) needs the stand-in board's pin map checked; not done.
   Not yet attempted: bridge (`gcwireless_bridge`) build.

## 2026-10-09 — Session 2: docs focus
User is not ready to build on a board; focus moved to repo setup and research docs. Read all of `gcwireless` src and `gcwireless_bridge` src; wrote `docs/facts/*`, README, STATUS, PROVENANCE, DECISIONS, FAQ. Main finding: upstream is a prototype (TX never sends in loop, RX spoofs data, bridge copies one byte). See STATUS.

## 2026-10-09 — Session 2 (cont.): PhobGCC docs
Added PhobGCC-doc and PhobGCCv2-HW as submodules. Learned: Phob 2 has its own on-board RP2040 (no Pico needed), parts come from a donor GCC, schematic shows 3.3 V regulators and spare GPIO12-15 labels. Rail/pad details still unverified. See facts/phobgcc.md.

## 2026-10-09 — Session 2 (cont.): KiCad netlist
User installed KiCad 10. Ran `"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe" sch export netlist --format kicadsexpr` on the Phob 2.0.0-proto-1 schematic and parsed it with a short Python script. Found header J6 (+3V3, GPIO12-15, GND) and the power path (cable +5V -> AMS1117-3.3 -> +3V3). A first parsing attempt matched nothing because KiCad 10 writes one token per line; fixed the regex. Details in facts/phobgcc.md.
