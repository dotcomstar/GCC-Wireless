# Fact file: the nRF52 radio as used in `gcwireless`

Source: `upstream/gcwireless` @ 576878d (`src/tx.cpp`, `src/rx.cpp`, `platformio.ini`). Everything under "Verified from code" was read from those files on 2026-10-09. Items marked **Unverified** are not yet checked against Nordic's datasheet.

Terms: **nRF52** = Nordic Semiconductor's family of 2.4 GHz radio microcontrollers. **TX** = transmitter (in the controller). **RX** = receiver (plugged into console/PC). **HAL** = hardware abstraction layer (Nordic's C wrapper over the chip's registers). **S0 / LENGTH** = fields in the radio packet header.

## Verified from code
- Firmware drives the chip's radio peripheral directly through `nrf_radio.h` (no Bluetooth). Docs linked in the source: https://docs.nordicsemi.com/bundle/sdk_nrf5_v17.1.0/page/group_nrf_radio_hal.html
- Mode: `NRF_RADIO_MODE_NRF_2MBIT` (Nordic proprietary mode, 2 Mbit/s). Same in TX and RX.
- Frequency: `nrf_radio_frequency_set(NRF_RADIO, 2401)`. **Verified 2026-10-10:** the argument is MHz. `nrf_radio_frequency_set` is documented "Frequency in MHz" and asserts 2360..2500 (`framework-arduinoadafruitnrf52/cores/nRF5/nordic/nrfx/hal/nrf_radio.h`, line ~566). Values below 2400 set the register's MAP bit to "Low" (2360-2460 MHz map). 2401 MHz is register value 1 on the default map (2400-2500 MHz). Note it sits right next to the bottom of the 2.4 GHz band (Wi-Fi channel 1 is centered at 2412 MHz), so interference is likely; see Open questions.
- TX power: `NRF_RADIO_TXPOWER_POS8DBM` (+8 dBm, TX only).
- Packet configuration (identical both sides): 8-bit preamble; LENGTH field 8 bits; S0 field 1 byte; no S1; max payload 8 bytes; static length 0 (length comes from the LENGTH field); base address 4 bytes; little-endian; no whitening.
- Address: base0 `0x12345678`, prefix0 `0x12345678`; TX uses logical address 0; RX listens on logical address 0 only (`rxaddresses = 0b00000001`).
- RAM buffer is 10 bytes, 4-byte aligned. With a 1-byte S0, buffer[0] is S0, buffer[1] is LENGTH, payload starts at buffer[2].
- CRC (error check): the code never configures it. In Nordic's header, `CRCCNF.LEN = 0` means "CRC length is zero and CRC calculation is disabled" (`nrf52840_bitfields.h`). The reset value is not in that header. A Nordic engineer reading the registers of a radio with no CRC setup saw "CRCCNF is '0'" (https://devzone.nordicsemi.com/f/nordic-q-a/80695/nrf52840-radio-receiving-with-crc/334337), so **probably no CRC by default, but the Product Specification reset value was not read** (the docs site truncates in the fetch tool). Safe plan: set the CRC explicitly on both sides, e.g. `nrf_radio_crc_configure(RADIO_CRCCNF_LEN_Two, NRF_RADIO_CRC_ADDR_INCLUDE, poly)` plus the initial value. Without a CRC a corrupted packet would be accepted as stick data.

## What the transmitter actually sends today (read carefully)
- `setup_transmitter()` fills the buffer with constants: S0 = `0x01`, LENGTH = `0x04`, then `DD CC BB AA 27 27 27 27`. This is a placeholder, not controller data. Because LENGTH is 4, only `DD CC BB AA` would go on air.
- A comment gives the intended layout: AX, AY, CX, CY, LA, RA (stick/trigger values 0-255, one byte each) plus a buttons bitfield "ABXYZSLR DDDD____".
- `loop_transmitter()` only blinks the LED and powers off when a button reads low (`SYSTEMOFF`). It never triggers a radio START. `sense_light_and_send()` does, but nothing calls it, and the "shortcuts" that would auto-send are commented out.
- Conclusion: **the upstream TX/RX pair is an early prototype; no working controller link exists in the code yet.**

## Receiver today
- Sets up the radio and starts listening, then overwrites its buffer with `0x1B` ("lets spoof some received bytes"). `loop_receiver()` never reads radio events (that block is commented out).
- Sets SPI-master pins (SCK `PIN_020`, MOSI `PIN_022`, MISO `PIN_024`) on `NRF_SPIM3` and starts a 10-byte transfer each loop. `rx.cpp` lines 72-82 only set pins and the TX buffer. **Verified by reading the file:** it never writes `ENABLE`, never sets the SPI frequency, and never sets an RX buffer. In the nrfx header, the ENABLE value that turns SPIM on is 7 (`SPIM_ENABLE_ENABLE_Enabled`), so the transfer cannot run until that is written. Expect it to do nothing today.

## Why not nRF24
Upstream author Heather Spacek: "nrf24 series is not recommended for new designs so I started again from scratch with nrf52's" (quoted in the project brief).

## Resolved 2026-10-10
- `PIN_0xx` naming: `PIN_<port><pin>` = P<port>.<pin> (TinyGo nice!nano table). With a generated header (`build-support/gcwireless/pins.h`) both TX and RX compile. See BUILD_LOG.
- Reset values (Nordic Product Specification v1.1): FREQUENCY = 2 (2402 MHz), CRCCNF = 0 (CRC disabled). So **with no CRC set up, as upstream does, both ends run with no error check at all.**

## Open questions
- The real nice!nano v2 pin-to-GPIO map has only been taken from TinyGo's table, not the official schematic.
- Channel choice: 2401 MHz is outside Wi-Fi's strongest region only if channel 1 is not in use nearby (Wi-Fi 2.4 GHz channel 1 is centered at 2412 MHz, ~22 MHz wide). Whether 2401 MHz is legal/usable depends on the band-edge rules (2400 MHz is the lower ISM edge); **not researched**. A 2 Mbit signal is ~2 MHz wide, so it sits right at the edge.
