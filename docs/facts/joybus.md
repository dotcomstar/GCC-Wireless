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
- Output bit: low 25 cycles, two 25-cycle slots at the data value, then high 20 cycles (plus a few 1-cycle instructions). By my arithmetic that is about 4 us per bit. **Unverified** against a protocol reference.
- Input: wait for a falling edge, wait 62 cycles, sample the pin.
- Data pin: GP27 (`_pinTX = 27` in `main.cpp`). Stock PhobGCC uses GP28.

## Bridge behavior today
- The bridge copies only byte 0 of the SPI data into `Ax` (main stick X). The full copy code is commented out, so buttons and the other axes stay at 0.

## Citations still to add
- A protocol reference. The stacksmashing video linked from `joybus.cpp` (https://www.youtube.com/watch?v=yYnQYF_Xa8g) has not been watched or verified.
