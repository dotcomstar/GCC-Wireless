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
Not started. Nothing is ordered without the user's approval.

### Candidate: Phob PCB vendor (2026-10-14, user's lead; not approved, not ordered)
- Gosre, Etsy shop https://www.etsy.com/shop/Gosre. User says the seller is local (DC/MD/VA). Not verified by me: Etsy returned HTTP 403 to my fetch, so product, price, bare-vs-assembled and shipping are **unknown**. User must read the listing.
- dol-003.info (https://dol-003.info/) is a GameCube-controller info site with a modder directory; it lists Gosre as a featured modder. Map: https://dol-003.info/modders?map=1; tag filters include "phobs". Profile pages (location, services) not yet read.
- Open questions for the listing: PCB version (must match docs read so far, Phob 2.0.5), bare board vs populated, donor-controller parts needed, price, shipping.
