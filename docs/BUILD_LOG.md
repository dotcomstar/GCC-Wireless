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
