# GCC-Wireless

Wireless GameCube controller project. Learner-driven; the documentation is the primary product.

- Radio: Nordic nRF52 family (nRF24 ruled out — "not recommended for new designs", per upstream author Heather Spacek).
- Upstream (all GPL-3.0, by heatherspacek): `gcwireless` (nRF52 TX/RX, PlatformIO, board `nicenano`), `gcwireless_bridge` (RP2040 SPI-slave → joybus to console), `Wireless-PhobGCC-nRF24` (older nRF24 version, reference only). No USB/PC receiver upstream.
- Controller platform: PhobGCC (https://github.com/PhobGCC — PhobGCC-SW, PhobGCC-doc, PhobGCCv2-HW) in a stock GameCube controller shell. Phob modifications allowed only when needed; user wants to defer deep Phob changes until more comfortable with hardware.
- Machine: Windows 11, Git Bash (no WSL). PlatformIO and Pico toolchain not installed as of 2026-10-09.
- All docs are Markdown in-repo. Define every acronym once; write verified facts, not recollections.
