# Fact file: power and battery

Status: **mostly unresearched.** Only code facts so far.

- The TX firmware sets +8 dBm output power (the highest setting it names; costly for a battery) and can enter `NRF_POWER->SYSTEMOFF` (the chip's deepest sleep) when an input reads low (`upstream/gcwireless/src/tx.cpp` @ 576878d).
- To research with citations: nRF52840 radio current at +8 dBm, a battery that fits a stock GameCube shell, a charging circuit, the PhobGCC supply voltage.
