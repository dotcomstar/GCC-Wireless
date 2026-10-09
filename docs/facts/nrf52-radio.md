# Fact file: the nRF52 radio as used in `gcwireless`

Source: `upstream/gcwireless` @ 576878d (`src/tx.cpp`, `src/rx.cpp`, `platformio.ini`). Everything under "Verified from code" was read from those files on 2026-10-09. Items marked **Unverified** are not yet checked against Nordic's datasheet.

Terms: **nRF52** = Nordic Semiconductor's family of 2.4 GHz radio microcontrollers. **TX** = transmitter (in the controller). **RX** = receiver (plugged into console/PC). **HAL** = hardware abstraction layer (Nordic's C wrapper over the chip's registers). **S0 / LENGTH** = fields in the radio packet header.

## Verified from code
- Firmware drives the chip's radio peripheral directly through `nrf_radio.h` (no Bluetooth). Docs linked in the source: https://docs.nordicsemi.com/bundle/sdk_nrf5_v17.1.0/page/group_nrf_radio_hal.html
- Mode: `NRF_RADIO_MODE_NRF_2MBIT` (Nordic proprietary mode, 2 Mbit/s). Same in TX and RX.
- Frequency: `nrf_radio_frequency_set(NRF_RADIO, 2401)`. **Unverified:** that the argument means MHz (2401 MHz); check the HAL source.
- TX power: `NRF_RADIO_TXPOWER_POS8DBM` (+8 dBm, TX only).
- Packet configuration (identical both sides): 8-bit preamble; LENGTH field 8 bits; S0 field 1 byte; no S1; max payload 8 bytes; static length 0 (length comes from the LENGTH field); base address 4 bytes; little-endian; no whitening.
- Address: base0 `0x12345678`, prefix0 `0x12345678`; TX uses logical address 0; RX listens on logical address 0 only (`rxaddresses = 0b00000001`).
- RAM buffer is 10 bytes, 4-byte aligned. With a 1-byte S0, buffer[0] is S0, buffer[1] is LENGTH, payload starts at buffer[2].
- CRC (error check): the code never configures it. **Unverified:** what the chip does by default; read the datasheet before relying on it.

## What the transmitter actually sends today (read carefully)
- `setup_transmitter()` fills the buffer with constants: S0 = `0x01`, LENGTH = `0x04`, then `DD CC BB AA 27 27 27 27`. This is a placeholder, not controller data. Because LENGTH is 4, only `DD CC BB AA` would go on air.
- A comment gives the intended layout: AX, AY, CX, CY, LA, RA (stick/trigger values 0-255, one byte each) plus a buttons bitfield "ABXYZSLR DDDD____".
- `loop_transmitter()` only blinks the LED and powers off when a button reads low (`SYSTEMOFF`). It never triggers a radio START. `sense_light_and_send()` does, but nothing calls it, and the "shortcuts" that would auto-send are commented out.
- Conclusion: **the upstream TX/RX pair is an early prototype; no working controller link exists in the code yet.**

## Receiver today
- Sets up the radio and starts listening, then overwrites its buffer with `0x1B` ("lets spoof some received bytes"). `loop_receiver()` never reads radio events (that block is commented out).
- Sets SPI-master pins (SCK `PIN_020`, MOSI `PIN_022`, MISO `PIN_024`) on `NRF_SPIM3` and starts a 10-byte transfer each loop. I found no call that enables SPIM3. **Unverified** whether it runs at all.

## Why not nRF24
Upstream author Heather Spacek: "nrf24 series is not recommended for new designs so I started again from scratch with nrf52's" (quoted in the project brief).

## Open questions
- Board: `platformio.ini` says `board = nicenano`; PlatformIO ships no such board, and the `PIN_0xx` names are undefined in the Adafruit core. See `docs/BUILD_LOG.md`.
