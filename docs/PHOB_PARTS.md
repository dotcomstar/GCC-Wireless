# PhobGCC v2.0.5 Parts and Specs

Source: `upstream/PhobGCC-doc/For_Makers/Phob2_Ordering_Guide.md` and `Build_Guide_2.0.md`, read 2026-11-04. Vendor prices from the Gosre Etsy shop (Berlin, MD; https://www.etsy.com/shop/Gosre) screenshot and listing text the user pasted on 2026-11-04. Kit tiers and prices: the user's screenshot and pasted listing description of 2026-11-05 (Etsy returns HTTP 403 to agent fetches, so nothing was fetched).

Decision so far: Gosre **Deluxe** tier, Blue, $39.99 (user's choice, 2026-11-05). Includes the Premium Rumble Bracket with pre-installed coreless motor. Bare kit over the $104.99 drop-in because this is a learning project.

## Gosre kit tiers (listing "GCC Phob 2.0.5 Motherboard Kits", read 2026-11-05)

Listing page text: "In 20+ carts", "$21.99+", ships from Maryland, "Arrives soon! Get it by Nov 7-10 if you order today" (quoted as of 2026-11-04). Kit Color: Blue. Kit listing URL not captured. Tiers are cumulative.

| Tier | Price | Contents |
|---|---|---|
| Essential | $21.99 | Phob v2.0.5 motherboard; trigger paddle set (with four color-matching pre-cut, pre-stripped jumper wires); grey C-stick ribbon cable |
| Basic | $29.99 | Essential, plus: upgraded color-matching C-stick harness (6-pin JST PH, Japan Solderless Terminal connector family, with straight and right-angle terminals); 4x DH1H1 magnet mounts + magnets; 1x Tactile-Z switch (100 gf, grams-force) |
| Deluxe | $39.99 | Basic, plus: Premium Rumble Bracket (color matching) with pre-installed adjustable-strength coreless motor, mounted to the motherboard with 2 screws and a driver (included). Bracket listing: https://www.etsy.com/listing/1758136726/ |

Seller notes (pasted): kits are not all-inclusive; you still need trigger potentiometers, stickboxes, and cables. Firmware is not flashed; flash it over micro-USB. Ships in cardboard boxes, not bubble mailers.

## Phob-specific parts (exact parts, "no non-identical substitutions")

| Part | Spec | In Gosre Deluxe kit? |
|---|---|---|
| Board | PhobGCC v2.0.5, C-stick daughterboard included (ordering guide) | Yes |
| Trigger paddles + jumper wires | Four color-matching pre-cut, pre-stripped jumper wires | Yes |
| C-stick ribbon | Grey ribbon cable | Yes |
| Tactile-Z switch | 100 gf | Yes |
| Rumble bracket + motor | Premium bracket, pre-installed coreless motor, 2 screws + driver | Yes (Deluxe) |
| Magnets x4 | DH1H1: 1/10" x 1/10" (2.5 x 2.5 mm) N52 neodymium cylinder (KJ Magnetics). D12 or N30H alternatives need a different mount offset and PhobVision tuning | Yes (DH1H1) |
| Magnet mounts x4 | Underslung DH1H1 mounts, 3D-printed. PhobGCC v1.x mounts do not work. Superglue (cyanoacrylate) to the stickbox pegs; magnets must sit horizontal | Yes |
| C-stick wiring | 6 conductors; the OEM 5-wire ribbon is unusable. 26 AWG stranded or a 6-pin ribbon / JST-PH harness | Yes (6-pin JST PH harness, straight + right-angle) |
| Superglue | Cyanoacrylate, used sparingly | No, buy |
| Stickboxes, trigger pots, cable, shell parts | See stock-parts table | Not in kit |

## Stock GameCube controller (GCC) parts still needed

| Part | Spec | Source |
|---|---|---|
| Stickboxes x2 | T3 (also found in Wii Classic / Classic Pro) | donor (reuse); buy only if the test in the Donor section fails. Fallback: Gosre T3 Stickbox $12.99 each |
| Trigger potentiometers x2 | Any GCC trigger pot | donor (reuse); buy only if the test in the Donor section fails. Fallback: Gosre Noble pair $5.99 |
| Trigger paddles x2 | With pre-cut, pre-stripped jumper wires | Kit |
| Z switch | Tactile, 100 gf | Kit |
| Cable with GCC plug | Donor cable. Only needed for a wired fallback; the project controller is wireless | Donor |
| Rumble bracket | Required as structure | Kit (Deluxe) |
| Shell, buttons, stick caps, rubber pads, screws | Donor | Donor |

## Not needed for Phob 2

Heartbeat modules / shunt resistors, Teensy or Pico, OEM C-stick ribbon, separate Hall sensors (on-board), Hall-effect stickboxes.

## Tools the build guide calls mandatory

- Temperature-controlled soldering iron, chisel tip >= 1.6 mm. Sn63Pb37 solder at 315-340 C (600-650 F) or SAC305 at 340-370 C (650-700 F). No dial-on-handle irons.
- Flux-core solder, no-clean rosin flux paste
- Tri-Wing driver; JIS #0 and #1 drivers (Phillips strips the screws)
- Flush cutters, solder sucker, isopropyl alcohol
- Micro-USB cable for flashing firmware (kit ships unflashed)

## Rumble (bracket included in Deluxe; wireless rumble forwarding still unverified)

Gosre Premium Rumble Bracket ($14.99 alone, included in the Deluxe tier): 3D-printed, 0.4 oz vs 1.4 oz OEM, pre-installed coreless motor with trim-pot strength adjust; Phob 2.0+ also adjusts strength in settings. This is the "cellphone rumble" style the Phob guide lists as an alternative. Open question: whether upstream gcwireless / gcwireless_bridge forwards rumble commands at all (not verified).

## Donor controller: Smash 4 bundle OEM GCC

OEM = original equipment manufacturer (a stock Nintendo-made controller). The donor came bundled with the Smash 4 release.

- Stamp (T1/T2/T3): **unknown, not verified.** Step: open the shell, read the T-stamp inside, record it here. Stamp guide: https://gccontrollerlibrary.com/guides/gamecube-controller-stamps-guide/ (linked from the ordering guide, not fetched).
- Plan (user's choice): reuse donor stickboxes and donor trigger pots; buy neither.

**Do I need T3 stickboxes or trigger pots?** No, if the donor's are usable.
- Stickboxes come from the donor. `Phob2_Ordering_Guide.md` lists stickbox sources as T3 GCCs, Wii Classic/Classic Pro, or loose on Etsy, and says "we have no stick potentiometers": Phob reads sticks with on-board Hall sensors and magnets on the stickbox. So stick-pot wear does not matter; check mechanical wear (centering, slop, gates). The `Build_Guide_2.0.md` harvest list says stickboxes "(preferably T3)", so other stamps are usable but T3 is preferred.
- Trigger pots come from the donor (ordering guide: any GCC works). They are still read as analog values, so worn ones show up as noisy or short-range triggers. You suspect yours are worn, so test before buying.

**Test donor trigger pots before buying.** After assembly, open the PhobScope Input Viewer in PhobVision and read the "Hardware Inputs" analog L/R numbers (`upstream/PhobGCC-doc/For_Users/Phobvision_Guide_Latest.md`, section "Input Viewer"; needs a PhobVision device per that guide). Pass: each trigger sweeps smoothly from rest to full press with no jumps. Fail: buy a pot pair (Gosre Noble pair $5.99 or Kadano's Etsy listing) and log it in BUILD_LOG.md.

## Gosre order (ORDERED by the user on 2026-11-05)

The user bought the Gosre Deluxe kit, Blue, $39.99 on 2026-11-05. Order number and arrival date not recorded.

| Item | Price |
|---|---|
| Deluxe kit, Blue | $39.99 |
| Subtotal (before shipping and tax) | $39.99 |

No stickboxes or trigger pots are in the order, by the user's choice (donor parts).

## Open items

- Read the donor stamp (open the shell).
- Capture the kit listing URL.
- Confirm whether Gosre T3 stickboxes are bare (only relevant if the donor stickboxes are rejected).
