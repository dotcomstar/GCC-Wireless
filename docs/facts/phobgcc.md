# Fact file: PhobGCC

**PhobGCC** = open-source replacement board and firmware for a GameCube controller. Org: https://github.com/PhobGCC (firmware `PhobGCC-SW`, docs `PhobGCC-doc`, hardware `PhobGCCv2-HW`). Pinned firmware here: `upstream/PhobGCC-SW` @ b4f175e (2025-11-15).

Verified 2026-10-09 from `upstream/Wireless-PhobGCC-nRF24/Wireless_Transmitter/include/Phob2_0.h` (the PhobGCC 2.0 pin map):
- RP2040 GPIO: A 17, B 16, X 18, Y 19, Z 20, L 22, R 21, Start 5; D-pad Left 8, Up 9, Down 10, Right 11; rumble 25; brake 29; joybus data 28; status LED 15; spare 12, 13, 14.
- Stick sensing uses external ADCs (analog-to-digital converters) on SPI: clock 6, MOSI 7, MISO 4; chip-selects 24 (A stick) and 23 (C stick). Analog triggers on ADC pins 26 and 27.
- Pins 0-3 form a small resistor-ladder DAC (digital-to-analog converter).

Not yet researched (do before building): how the board fits a stock shell, which spare pins a radio could use, the board's power supply. Source to read: PhobGCC-doc. **Unverified until read.**
