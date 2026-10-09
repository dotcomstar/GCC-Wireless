# Fact file: PhobGCC

**PhobGCC** = open-source replacement board and firmware for a GameCube controller. Org: https://github.com/PhobGCC (firmware `PhobGCC-SW`, docs `PhobGCC-doc`, hardware `PhobGCCv2-HW`). Pinned firmware here: `upstream/PhobGCC-SW` @ b4f175e (2025-11-15).

Verified 2026-10-09 from `upstream/Wireless-PhobGCC-nRF24/Wireless_Transmitter/include/Phob2_0.h` (the PhobGCC 2.0 pin map):
- RP2040 GPIO: A 17, B 16, X 18, Y 19, Z 20, L 22, R 21, Start 5; D-pad Left 8, Up 9, Down 10, Right 11; rumble 25; brake 29; joybus data 28; status LED 15; spare 12, 13, 14.
- Stick sensing uses external ADCs (analog-to-digital converters) on SPI: clock 6, MOSI 7, MISO 4; chip-selects 24 (A stick) and 23 (C stick). Analog triggers on ADC pins 26 and 27.
- Pins 0-3 form a small resistor-ladder DAC (digital-to-analog converter).

See the section below for what was read from PhobGCC-doc and the hardware repo.

## Added 2026-10-09: from PhobGCC-doc and PhobGCCv2-HW
Sources: `upstream/PhobGCC-doc` @ 23e9192 (2026-08-14), `upstream/PhobGCCv2-HW` @ ff645aa (2023-04-17; board licensed CERN-OHL-S v2, "strongly reciprocal": changes to the board must be published and `CHANGES.txt` updated, per its README).

- **What it is:** a replacement motherboard for a GameCube controller (GCC). It reads stick position with magnets and Hall-effect sensors instead of wearing potentiometers (PhobGCC-doc `README.md`).
- **The Phob 2 board has its own RP2040 microcontroller**, flash chip (W25Q128JVS) and stick ADCs (MCP3202). The ordering guide says: "Teensy or Raspberry Pi Pico: the PhobGCC 2 has no need of any external microcontroller board." (`For_Makers/Phob2_Ordering_Guide.md`). So the bridge's RP2040 is a *second*, separate one.
- **Donor controller:** a build reuses parts from a donor stock GCC: 2 stickboxes, 2 trigger potentiometers, cable, rumble bracket, Z switch, optional rumble motor and trigger paddles, plus the shell (`For_Makers/Build_Guide_2.0.md`). The shell and cable are therefore reused, and the Phob board takes the place of the original motherboard. Fit in the shell: the guide warns the Z switch must sit square "or the board may not fit in the controller shell properly" and some solder pads interfere with a rib on the front shell; a USB jack/PhobVision jack are described as tight with the OEM rumble motor.
- **Board parts** (counted in `PhobGCC_2_0_0_proto_1.kicad_sch`): RP2040, 2x AMS1117-3.3 (3.3 V regulators), nets named `+5V`, `VBUS`, `+3V3`, `GCC_3.3V`, `GCC_DATA`, 2x USB-B-micro symbols, USBLC6-2P6 (USB protection), fuses, 4x DRV5055A3 Hall sensors.
- **Spare GPIO:** the schematic has net labels `GPIO12`, `GPIO13`, `GPIO14`, `GPIO15` (matches the spare pins 12/13/14 and LED 15 in `Phob2_0.h`). **Unverified:** whether they reach a solder pad or header that is physically reachable on the finished board; open the KiCad file or inspect a real board.
- **Power:** `GCC_3.3V` and `+5V`/`VBUS` nets exist. **Unverified:** that the board is powered from the console cable (expected, since `GCC_DATA`/`GCC_3.3V` are named for the cable, but not traced); which rail feeds the AMS1117 regulators and how much current is spare. Read the schematic in KiCad before deciding how to power a radio.
- **Firmware flashing:** see `For_Users/Phob2_Programming_Guide.md` (not read yet).

## Still unverified / to read
- Phob2_Programming_Guide (how firmware is loaded; matters for adding radio code).
- Whether a battery can power the Phob 2 board directly (regulator input range).
- Space inside a stock shell for a nice!nano-size board and battery.
