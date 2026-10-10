# Fact file: PC / USB receiver options

Status (2026-10-10): research only. **No PC receiver exists upstream**; `gcwireless` RX only drives an SPI link to the console bridge. Everything under "Candidate approaches" is analysis, not tested.

## What the hardware can do (verified)
- The nRF52840 has a USB 2.0 full-speed (12 Mbit/s) device controller, with 64-byte buffers per bulk/interrupt endpoint, 8 IN + 8 OUT endpoints, 1 IN + 1 OUT isochronous (Nordic Product Specification v1.1, USBD chapter; same PDF as in `power.md`). The nice!nano exposes a USB-C port wired to it (nicekeyboards page cited in `power.md`). So the receiver board can present itself to a PC with no extra chip.

## How Dolphin (the GameCube/Wii emulator Slippi builds on) talks to the official GameCube adapter
Source: Dolphin `Source/Core/InputCommon/GCAdapter.cpp` at master, commit e6f3ae17627e4344da95b13424af5baf4c892b08 (committed 2026-10-08), read 2026-10-10 from https://raw.githubusercontent.com/dolphin-emu/dolphin/master/Source/Core/InputCommon/GCAdapter.cpp.
- The adapter is matched by USB vendor ID `0x057e` (Nintendo) and product ID `0x0337` (WUP-028 adapter). Also confirmed by Dolphin forum posts.
- Init: a control transfer (`bmRequestType 0x21, bRequest 11, wValue 1`) that "makes Nyko-brand (and perhaps other) adapters work" but errors harmlessly on Mayflash; then Dolphin writes one byte `0x13` to the OUT endpoint to start the adapter.
- Input report: 37 bytes. Byte 0 = `0x21` (`LIBUSB_DT_HID`, checked by the code). Then four ports x 9 bytes starting at `data[1 + 9*port]`.
- Each 9-byte port record: byte 0 = status (bit 4 set -> wired controller, bit 5 set -> wireless/WaveBird, neither -> nothing plugged in); byte 1 = buttons: bit0 A, bit1 B, bit2 X, bit3 Y, bit4 D-left, bit5 D-right, bit6 D-down, bit7 D-up; byte 2 = bit0 Start, bit1 Z, bit2 R, bit3 L; bytes 3-8 = main stick X, main stick Y, C-stick X, C-stick Y, L analog, R analog.
- Rumble (vibration motor): host writes a 5-byte packet `0x11, r0, r1, r2, r3` (one byte per port; Dolphin skips it for wireless controllers).
- Windows needs the adapter bound to the WinUSB driver (use the Zadig tool, "Replace Driver"), per https://wiki.dolphin-emu.org/index.php?title=How_to_use_the_Official_GameCube_Controller_Adapter_for_Wii_U_in_Dolphin . Third-party adapters must be in "Wii U" mode. Dolphin's native support "will offer better latency" than vJoy-style virtual drivers (same page). A device could avoid the Zadig step by advertising a WinUSB-compatible ID in its USB descriptors - **not checked**.

## Candidate approaches (analysis; not tested)
| Option | Works with | Cost / risk |
|---|---|---|
| A. Receiver pretends to be the Nintendo adapter (VID 057e, PID 0337, the 37-byte report above) | Dolphin / Slippi natively; probably other tools that know the adapter | Cleanest for Melee. Need to confirm Windows driver handling and that Dolphin does not check anything beyond VID/PID/endpoints. Using Nintendo's VID is a licensing grey area for anything distributed. |
| B. Generic USB HID gamepad | Anything that reads a HID gamepad (Steam Input, browsers); Dolphin only through its HID mapping | Easiest; needs button mapping by the user; no rumble convention. |
| C. Xbox/XInput-style | Most PC games | Needs Microsoft's XInput USB class details; **not researched**. |

## Open questions
- Latency of USB polling: full-speed HID interrupt endpoints poll at 1 ms at best; whether Dolphin reads the adapter at 125 Hz or faster is not checked (the code measures `s_adapter_poll_rate`).
- Whether a WinUSB descriptor from a TinyUSB device removes the Zadig step.
- TinyUSB (Adafruit's USB library on the Adafruit nRF52 core) example support for custom bulk/interrupt devices - not read.
- Real-world prior art for adapter emulation: web search found projects for the reverse direction (USBRetro, OpenGCC) but none emulating the 0x0337 adapter; treat as "none found", not "none exist".
