# FAQ

Only questions the user actually asked. Each answer links a fact file. (Target: 10; currently 2.)

**Should `plans/WORKER_NOTES.md` be committed instead of gitignored?**
No. `plans/` holds agent workflow files, not project knowledge. Project status lives in [STATUS.md](STATUS.md), which is tracked.

**Why does the upstream code not build?**
`platformio.ini` names a `nicenano` board that PlatformIO does not ship, and the code uses `PIN_0xx` names no checked board package defines. See [BUILD_LOG.md](BUILD_LOG.md) and [facts/nrf52-radio.md](facts/nrf52-radio.md).
