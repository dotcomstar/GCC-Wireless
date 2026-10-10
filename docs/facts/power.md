# Fact file: power and battery

Status (2026-10-10): radio and nice!nano numbers are **verified from primary sources** (below). Battery fit inside a shell, the Phob's own current draw, and charging choices are still open.

Terms: **mA** = milliamp, **uA** = microamp (1/1000 mA). **DC/DC** = the nRF52's built-in switching converter (more efficient than its **LDO**, linear regulator). **TIFS** = turnaround time between packets.

## nRF52840 radio current (Nordic Product Specification v1.1, section 6.20.15, text extracted from the PDF at https://cdn.sparkfun.com/assets/d/2/6/2/6/nRF52840_PS_v1.1.pdf, read 2026-10-10)
Transmit-only run current, 3 V supply:

| Output power | DC/DC | LDO |
|---|---|---|
| +8 dBm (what upstream uses) | 14.8 mA | 32.7 mA |
| +4 dBm | 9.6 mA | 21.4 mA |
| 0 dBm | 4.8 mA | 10.6 mA |
| -4 dBm | 3.1 mA | 8.1 mA |
| -20 dBm | 2.7 mA | 5.6 mA |

Receive-only run current, 3 V: 2 Mbit/s = 5.2 mA with DC/DC, 11.1 mA with LDO. (1 Mbit/s: 4.6 / 9.9 mA.)

- **Whether DC/DC is on matters more than the dBm setting.** Upstream `gcwireless` never enables the DC/DC (grep of `upstream/gcwireless/src` and `platformio.ini` for dcdc/regulators/modecnf found nothing; the Adafruit core was only spot-checked, so the default is unconfirmed), so assume the LDO column: +8 dBm costs 32.7 mA while 0 dBm costs 10.6 mA.
- Sleep: System ON with RAM retained, waiting for an event = 2.35 uA; System OFF, no RAM retained = 0.40 uA (section 5.2.1.1).
- Sensitivity (how weak a signal the receiver can still decode): -89 dBm at 2 Mbit/s in Nordic's proprietary mode, -93 dBm at 1 Mbit/s. A 3 dB penalty applies if receive addresses 1-7 are used instead of address 0.
- Timing: TX or RX ramp-up is 140 us by default or 40 us with the fast ramp-up setting (`RADIO.MODECNF0.RU`). The 2 Mbit disable delay is 4 us (TX) / 0 us (RX).
- Reset values: FREQUENCY = 2 (2402 MHz); CRCCNF = 0 (CRC off).

## How long is one packet? (derived)
At 2 Mbit/s one byte takes 4 us. Upstream's frame is 1 preamble + 5 address (4 base + 1 prefix) + S0 + LENGTH + up to 8 payload bytes = 16 bytes, plus 2 if a 2-byte CRC is added = 18 bytes = **72 us on air**. Adding a ramp-up of 40-140 us, the radio is on about 0.11-0.21 ms per packet. This is arithmetic from the spec figures, not a measurement.

## Rough average radio current (derived; ignores the CPU and the board)
Using LDO +8 dBm = 32.7 mA over ~0.21 ms per packet (default ramp-up):
- 1 packet per 1 ms: ~6.9 mA average
- 1 packet per 4 ms: ~1.7 mA
- 1 packet per 8 ms: ~0.9 mA
The CPU and anything else awake add to this. Real figures need a bench measurement.

## nice!nano (official page https://nicekeyboards.com/docs/nice-nano/ fetched 2026-10-10)
- nRF52840, 21 GPIO, Pro Micro pinout, 3.2 mm thick. Board length/width are not on that page.
- Takes a **3.7 V lithium-polymer (LiPo) battery** on top pads (+/-). Recommended cell: 301230 (100 mAh, ~3 mm thick).
- Charges at about 100 mA by default (page says actual ~85 mA), good for cells of 100-500 mAh; a solder jumper ("boost") raises that to ~500 mA for cells over 500 mAh. Under 100 mAh is not recommended; over 2000 mAh can damage the cell or the board. Ideal charge rate is 0.25-0.5C (C = battery capacity per hour).
- The page names no power switch (a software MOSFET switches the LEDs' supply). Each LED can draw ~1 mA even when "off". Check battery connections before powering: pins can puncture the cell.
- Battery voltage is readable through P0.04 (AIN2); P0.13 high cuts the 3.3 V output (VCC) to external parts (per https://docs.splitkb.com/product-guides/nice-nano/schematics-and-pinout, a second source; not checked against the schematic).
- Not on the page: regulator type and current limit on VCC. Open question.

## How the Phob is powered (see `phobgcc.md`)
Phob input is +5 V from the console cable (J1 pin 2), through an AMS1117-3.3 (3-10 mA of its own quiescent current, dropout 1.25-1.4 V at 1 A depending on maker) and a Schottky diode (D1) to the 3.3 V rail. A 3.7 V cell cannot feed that 5 V input. The ways in are: (a) feed the 3.3 V rail through J6 pin 1 (3V3) and be sure the diode D1 blocks backflow into the AMS1117; or (b) a boost converter to 5 V. Neither has been checked on hardware. The RP2040 current draw has not been looked up.

## RP2040 current (RP2040 datasheet, section 5.7, https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf, read 2026-10-10)
Table 637 (typical / worst-case average, mA). The RP2040 makes its 1.1 V core (DVDD) from 3.3 V with an on-chip linear regulator, so core current is drawn from the 3.3 V supply one-for-one.
- BOOTSEL mode, USB idle: DVDD 9.0 / 14.3; IOVDD (pin supply) 1.2 / 4.3. About 10 mA typical total.
- Sleep: DVDD 0.39 / 4.5. Dormant: DVDD 0.18 / 4.2.
- Popcorn video demo at 48 MHz (heavy IO): DVDD 10.9 / 16.6; IOVDD 24.8 / 35.5.
- Peripherals add per MHz of system clock (Table 635), e.g. PIO 12.3 uA/MHz per block, IO + pads 23.6, UART 3.5; at 125 MHz a PIO block adds roughly 1.5 mA (arithmetic).
- Not in the datasheet text I extracted: the Phob's own firmware current. Table 637 text columns were garbled by extraction, so IOVDD/USB cells above were read by layout; recheck against the PDF before relying on them.
- Consequence (derived): the Phob alone is probably on the order of 10-20 mA at 3.3 V before the radio board; adding a TX at ~7 mA average gives ~20-30 mA, so a 100 mAh cell would last only a few hours. Needs a bench measurement.

## Still to research
- Phob firmware real current (measure; datasheet gives only generic cases).
- LiPo charging and protection: the nice!nano charger as the only charger vs a separate board.
- Does a battery fit inside a stock GameCube shell with a Phob (no dimensions in any doc yet).
- Whether the nRF52 DC/DC needs an inductor on the nice!nano (see Nordic reference design); if not fitted, DC/DC cannot be enabled.
- Safety: LiPo in a handheld device; protection circuit and venting.
