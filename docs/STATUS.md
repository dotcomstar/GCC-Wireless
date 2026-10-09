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
