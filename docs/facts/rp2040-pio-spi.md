# Fact file: RP2040 PIO and SPI as used in the bridge

Source: `upstream/gcwireless_bridge` @ 5c31147. Read 2026-10-09.

**RP2040** = Raspberry Pi's microcontroller (two Arm cores). **PIO** = Programmable I/O: small state machines that toggle pins with exact timing, independent of the CPU. **SPI** = Serial Peripheral Interface: a 4-wire link (clock SCK, data in, data out, chip-select CSn).

- PIO runs the joybus program (`pio/joybus.pio`). The comment in `joybus.cpp` says why: software bit-banging made the controller disconnect for a frame now and then; PIO fixed it.
- Core 0 runs `enterMode()` (the joybus loop). Core 1 (`second_core()`) runs SPI: `spi_init(spi_default, 1 MHz)` then `spi_set_slave(true)`. The RP2040 is the SPI **slave**; the nRF52 receiver (`NRF_SPIM3`, a master peripheral) is the master.
- SPI pins are the Pico SDK defaults `PICO_DEFAULT_SPI_{RX,SCK,TX,CSN}_PIN`. **Unverified:** their GPIO numbers; they depend on the `PICO_BOARD` the build selects.
- Transfer size is 10 bytes (`BUF_LEN`). Core 1 loops: sleep 10 us (comment: "superstition"), blocking-read 10 bytes, copy `in_buf[0]` into `_btn.Ax`.
- The build uses CMake with `PICO_SDK_PATH` (unset on this machine as of 2026-10-09).
