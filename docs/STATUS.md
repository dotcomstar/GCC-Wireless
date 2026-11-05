# Status (2026-10-09)

| Area | State |
|---|---|
| Repo, upstream pinned | Done |
| Fact files | First drafts from reading code; power and PhobGCC fit need research |
| nRF52 TX/RX build | **Blocked**: board `nicenano` and `PIN_0xx` names missing (see BUILD_LOG) |
| RP2040 bridge build | **Compiles** (`bash build-support/build-bridge.sh` -> .uf2; not run on hardware) |
| Hardware | None owned; user is not ready to build on a board yet |
| Console test / PC receiver | Not started; PC/USB receiver does not exist upstream |

## Key finding
Upstream `gcwireless` is an early prototype: the transmitter never sends in its main loop, its payload is placeholder bytes, and the receiver fakes its data. Upstream `gcwireless_bridge` copies only one byte (main stick X). A working link must be written, not just built. Details: [facts/nrf52-radio.md](facts/nrf52-radio.md).

## Next / missing (checklist)
- [~] Phob facts mostly done (see facts/phobgcc.md): power path and spare header J6 verified from netlist. Programming guide, PhobVision and maker guides read 2026-10-10. Remaining: AMS1117 datasheet, v2.0.5 vs schematic check, shell-fit measurement
- [x] Radio power/battery numbers from Nordic spec -> `facts/power.md` (shell fit, RP2040 current, charging still open)
- [x] Joybus bit timing cross-checked against two references -> `facts/joybus.md`
- [x] nRF52 radio unknowns verified (frequency = MHz, CRC off at reset, SPIM3 never enabled) -> `facts/nrf52-radio.md`
- [~] TX/RX build: done with a generated pin header. Still to do: verify the real nice!nano v2 pin map against the official schematic
- [x] RP2040 bridge build works via `build-support/build-bridge.sh`
- [ ] Decide the PC/USB receiver approach (not in upstream)
- [x] KiCad 10 workspace with Phob, TX, RX and reference sheets: `hardware/`, guide in [HARDWARE.md](HARDWARE.md) (ERC: 0 errors on new sheets; 6 inherited from upstream Phob)
- [ ] Write `PHOB_CHANGES.md` (only if Phob is modified) and wiring tables
- [x] BOM: Gosre Deluxe kit ($39.99) ordered by the user 2026-11-05; donor supplies stickboxes/pots
- [ ] Grow the FAQ to 10 real questions
