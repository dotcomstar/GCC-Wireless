# FAQ

Only questions the user actually asked. Each answer links a fact file. (Target: 10; currently 3.)

**Should `plans/WORKER_NOTES.md` be committed instead of gitignored?**
No. `plans/` holds agent workflow files, not project knowledge. Project status lives in [STATUS.md](STATUS.md), which is tracked.

**Why does the upstream code not build?**
`platformio.ini` names a `nicenano` board that PlatformIO does not ship, and the code uses `PIN_0xx` names no checked board package defines. See [BUILD_LOG.md](BUILD_LOG.md) and [facts/nrf52-radio.md](facts/nrf52-radio.md).

**Where is J6 on the Phob, and how many free pins does the Phob have? Which RP2040 is that?**
J6 is the "GPIO Breakout" row of 6 pads near the middle of the board, with a picture in [facts/phobgcc.md](facts/phobgcc.md). Only GPIO12-15 are free (plus 3.3V and GND); every other pin of the Phob's *own* on-board RP2040 is in use. The radio board and the bridge's RP2040 are separate chips.
