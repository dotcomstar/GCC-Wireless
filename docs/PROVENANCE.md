# Provenance of upstream code

All pinned as git submodules under `upstream/`. All are GPL-3.0 (LICENSE files are inside each submodule).

| Path | URL | Commit | Role |
|---|---|---|---|
| upstream/gcwireless | https://github.com/heatherspacek/gcwireless | 576878d (2026-02-26) | nRF52 TX/RX firmware (PlatformIO) |
| upstream/gcwireless_bridge | https://github.com/heatherspacek/gcwireless_bridge | 5c31147 | RP2040 SPI-slave to joybus |
| upstream/Wireless-PhobGCC-nRF24 | https://github.com/heatherspacek/Wireless-PhobGCC-nRF24 | c25004e (2024-03-24) | older nRF24 version, reference only |
| upstream/PhobGCC-SW | https://github.com/PhobGCC/PhobGCC-SW | b4f175e (2025-11-15) | controller firmware |
| upstream/PhobGCC-doc | https://github.com/PhobGCC/PhobGCC-doc | 23e9192 (2026-08-14) | Phob build/user documentation |
| upstream/PhobGCCv2-HW | https://github.com/PhobGCC/PhobGCCv2-HW | ff645aa (2023-04-17) | Phob 2.0 KiCad hardware, CERN-OHL-S v2 |

Notes: `gcwireless/.gitmodules` still lists pico-rectangle and PhobGCC-SW although its commit bd570f2 removed them; we add PhobGCC-SW ourselves. `build-support/boards/nicenano.json` is our own stand-in board file (derived from PlatformIO's Adafruit Feather nRF52840 definition).

