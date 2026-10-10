# Fact file: GameCube controller protocol ("joybus") as implemented in the bridge

Source: `upstream/gcwireless_bridge` @ 5c31147 (`src/joybus.cpp`, `pio/joybus.pio`, `include/gcReport.hpp`, `src/main.cpp`), adapted from pico-rectangle (https://github.com/JulienBernard3383279/pico-rectangle). Read 2026-10-09.

**Joybus** = Nintendo's one-wire serial protocol between a console and a controller. The console is the master: it sends a command, the controller answers. One data pin carries both directions.

## Commands handled (first byte received)
| Byte | Meaning (per code comments) | Reply |
|---|---|---|
| `0x00` | Probe ("what are you?") | `09 00 03` (3 bytes) |
| `0x41` | Origin (neutral position; `0x41`, not `0x81`) | 10 bytes: `00 80 128 128 128 128 0 0 0 0` |
| `0x40` | Poll (send your buttons); 2 more bytes follow (mode, rumble) | 8-byte `GCReport` |
| other | ignored; wait 400 us, resume listening | none |

The rumble byte is read but discarded (the pin write is commented out).

## The 8-byte report (`GCReport`, `gcReport.hpp`)
- Byte 0: A, B, X, Y, Start (bits 0-4), 3 pad bits.
- Byte 1: D-pad left, right, down, up; Z; R; L; then a fixed 1 bit.
- Bytes 2-7: main stick X, Y; C-stick X, Y; analog L; analog R (each 0-255, 128 = centered).

## Wire timing (from `joybus.pio`)
- RP2040 system clock must be 125 MHz; PIO clock divider 5 gives 25 MHz (40 ns per cycle).
- Output bit: low 25 cycles, two 25-cycle slots at the data value, then high 20 cycles (plus a few 1-cycle instructions). By my arithmetic that is about 4 us per bit.

### Cross-check against references (2026-10-10)
- Bit timing, per the page at https://www.int03.co.uk/crema/hardware/gamecube/gc-control.html (a hobby reverse-engineering write-up): each bit is about 4 us. A **0** is 3 us low then 1 us high. A **1** is 1 us low then 3 us high. A single high stop bit ends each message. The n64brew wiki (https://n64brew.dev/wiki/Joybus_Protocol) agrees that data bits and the controller stop bit are 4 us (console stop bit 3 us) but gives the low/high split only in an image.
- Check of the bridge's PIO: low 25 cycles x 40 ns = 1 us, then two 25-cycle slots at the data value = 2 us, then ~0.8 us high. So a 0 is ~3 us low + ~1 us high, a 1 is 1 us low + ~3 us high. **This matches the references.** Input sampling 62 cycles x 40 ns = 2.48 us after the falling edge lands inside the high part of a 1 (starts at 1 us) and the low part of a 0 (lasts to 3 us). Also consistent.
- Command 0x40 is 3 bytes: `40 03 0R`, where the last bit of the third byte is the rumble motor on/off bit (int03 page; the page lists the third byte as `02`; a search-result summary of another source lists it as `00` + rumble bit - the low bit is what matters). The reply is 8 bytes (64 bits) + stop bit.
- Reply byte layout per int03: byte 0 = 3 unused bits then Start, Y, X, B, A; byte 1 = always-1 bit then L, R, Z, D-up, D-down, D-right, D-left; bytes 2-7 = stick X/Y, C-stick X/Y, left analog, right analog. int03 lists bits first-sent (most significant) first. Read that way, A is bit 0 and Start bit 4 of byte 0; Left is bit 0 ... L bit 6, fixed 1 at bit 7 of byte 1. **This matches the bridge's `gcReport.hpp` order (checked 2026-10-10).**
- Timing between command and reply: int03 saw ~15 us in one experiment and none in another. A full poll is ~348 us (88 bits). Polls come roughly every 6 ms on an official controller (that figure is from one experiment on one controller; the PhobVision guide talks in 1-frame = ~17 ms steps, which is the game's sampling, not the poll rate).
- n64brew command table (marked "requires verification" by its authors): 0x00/0xFF info -> 3 bytes; 0x40 short poll -> 8 bytes; 0x43 long poll -> 10 bytes; 0x41 read origin and 0x42 calibrate sizes unknown there.

- Input: wait for a falling edge, wait 62 cycles, sample the pin.
- Data pin: GP27 (`_pinTX = 27` in `main.cpp`). Stock PhobGCC uses GP28.

## Bridge behavior today
- The bridge copies only byte 0 of the SPI data into `Ax` (main stick X). The full copy code is commented out, so buttons and the other axes stay at 0.

## Citations still to add
- Done above: int03 and n64brew pages cited. Still not read: Nintendo-era primary docs do not exist publicly. The stacksmashing video linked from `joybus.cpp` (https://www.youtube.com/watch?v=yYnQYF_Xa8g) has not been watched or verified.
