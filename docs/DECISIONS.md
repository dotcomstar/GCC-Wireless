# Decisions

## D1: Radio family is Nordic nRF52, not nRF24 (2026-10-09)
Upstream author Heather Spacek says nRF24 is not recommended for new designs and rewrote on nRF52 (`gcwireless`). We follow. nRF24 repo kept for reference only.

## D2: Controller is PhobGCC in a stock GameCube shell (2026-10-09)
Open-source hardware and firmware, and it fits a stock shell (user's statement; fit not yet verified, see facts/phobgcc.md). Phob changes only when needed, each listed in `docs/PHOB_CHANGES.md` (none yet). The user wants to defer deep Phob modification.

## D3: Documentation first (2026-10-09)
User is not ready to build on a board. Focus is repo setup and verified research docs.

## D4: Repo license GPL-3.0
Derived from GPL-3.0 code.

## BOM
Gosre Deluxe kit ordered by the user 2026-11-05 (details below). Nothing else is ordered without the user's approval.

### Phob PCB vendor: Gosre (2026-10-14 lead; Deluxe kit ordered 2026-11-05)
- Gosre, Etsy shop https://www.etsy.com/shop/Gosre. User says the seller is local (DC/MD/VA). Etsy returns HTTP 403 to agent fetches. From the user's screenshot and pasted description (2026-11-05), "GCC Phob 2.0.5 Motherboard Kits" tiers are Essential $21.99, Basic $29.99, Deluxe $39.99. **Chosen: Deluxe, Blue, $39.99** (includes the Premium Rumble Bracket with pre-installed coreless motor). The donor Smash 4 bundle GCC supplies stickboxes and trigger pots; pots are tested first. Details: PHOB_PARTS.md. **Ordered by the user on 2026-11-05** (Deluxe, Blue, $39.99); order number and arrival date not recorded.
- dol-003.info (https://dol-003.info/) is a GameCube-controller info site with a modder directory; it lists Gosre as a featured modder. Map: https://dol-003.info/modders?map=1; tag filters include "phobs". Profile pages (location, services) not yet read.
- Open questions for the listing: PCB version (must match docs read so far, Phob 2.0.5), bare board vs populated, donor-controller parts needed, price, shipping.
