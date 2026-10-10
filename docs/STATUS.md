# Status (2026-10-09)

| Area | State |
|---|---|
| Repo, upstream pinned | Done |
| Fact files | First drafts from reading code; power and PhobGCC fit need research |
| nRF52 TX/RX build | **Blocked**: board `nicenano` and `PIN_0xx` names missing (see BUILD_LOG) |
| RP2040 bridge build | Not tried (needs Pico SDK; `PICO_SDK_PATH` unset) |
| Hardware | None owned; user is not ready to build on a board yet |
| Console test / PC receiver | Not started; PC/USB receiver does not exist upstream |

## Key finding
Upstream `gcwireless` is an early prototype: the transmitter never sends in its main loop, its payload is placeholder bytes, and the receiver fakes its data. Upstream `gcwireless_bridge` copies only one byte (main stick X). A working link must be written, not just built. Details: [facts/nrf52-radio.md](facts/nrf52-radio.md).

## Next / missing (checklist)
- [~] Phob facts mostly done (see facts/phobgcc.md): power path and spare header J6 verified from netlist. Programming guide, PhobVision and maker guides read 2026-10-10. Remaining: AMS1117 datasheet, v2.0.5 vs schematic check, shell-fit measurement
- [ ] Research power/battery with citations -> `facts/power.md`
- [ ] Verify joybus bit timing against a protocol reference -> `facts/joybus.md`
- [ ] Verify nRF52 radio unknowns (frequency unit, default CRC, SPIM3 enable) against Nordic docs -> `facts/nrf52-radio.md`
- [ ] Find the real nice!nano board/pin map (or ask Heather in a GitHub issue); then get TX/RX to build
- [ ] Try the RP2040 bridge build (install Pico SDK, set `PICO_SDK_PATH`)
- [ ] Decide the PC/USB receiver approach (not in upstream)
- [ ] Write `PHOB_CHANGES.md` (only if Phob is modified), wiring tables, and a BOM with prices (user approval before ordering)
- [ ] Grow the FAQ to 10 real questions
