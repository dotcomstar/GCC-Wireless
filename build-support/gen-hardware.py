"""Generates the new KiCad files under hardware/ (library, sheets, root, project).

Run from the repo root:  uv run python -I build-support/gen-hardware.py
The generated files are committed; this script is kept so the drawings can be
changed in code and regenerated. It writes text in KiCad 9/10 s-expression format.
Licence: GPL-3.0 (same as the repo).
"""
import uuid
from pathlib import Path

HW = Path("hardware")
NS = uuid.UUID("6f1c2d10-0000-4000-8000-000000000001")
LIB = "GCC-Wireless"
PROJECT = "GCC-Wireless"
ROOT_UUID = str(uuid.uuid5(NS, "root"))
G = 2.54
PITCH = 5.08  # row spacing of our symbols (wider than the usual 2.54 so labels do not collide)


def uid(*parts):
    return str(uuid.uuid5(NS, "/".join(map(str, parts))))


def q(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


FONT = "(font (size 1.27 1.27))"

# ---------------------------------------------------------------- symbols
# A symbol is a dict: name, ref, datasheet, descr, rows (n, odd), left/right
# lists of (row, number, pin_name), width (body width in mm), body_title.
NANO_LEFT = ["GND", "P0.06", "P0.08", "GND", "GND", "P0.17", "P0.20", "P0.22",
             "P0.24", "P1.00", "P0.11", "P1.04", "P1.06"]
NANO_RIGHT = ["BATTERY+", "BATTERY+", "GND", "RESET", "3.3V", "P0.31", "P0.29",
              "P0.02", "P1.15", "P1.13", "P1.11", "P0.10", "P0.09"]
NANO_URL = "https://nicekeyboards.com/docs/nice-nano/pinout-schematic"
SYMS = {
    "NiceNano_v2": dict(
        ref="U", datasheet=NANO_URL, width=20.32, rows=13,
        descr="nice!nano v2 (nRF52840 board). Pin names copied from the official v2 pinout image; "
              "pin numbers are ours: left column 1-13 top to bottom, right column 14-26 bottom to top.",
        left=[(k, str(k + 1), n) for k, n in enumerate(NANO_LEFT)],
        right=[(k, str(26 - k), n) for k, n in enumerate(NANO_RIGHT)],
        footprint=""),
    "GameCube_Plug": dict(
        ref="J", datasheet="https://www.int03.co.uk/crema/hardware/gamecube/gc-control.html",
        width=15.24, rows=7,
        descr="GameCube controller connector. Numbering is the int03 page's own (socket view).",
        left=[], right=[(0, "1", "+5V"), (1, "2", "DATA"), (2, "3", "GND"), (3, "4", "GND"),
                        (4, "5", "NC"), (5, "6", "3.43V"), (6, "7", "SHIELD")],
        footprint=""),
    "Battery_Conn": dict(
        ref="J", datasheet=NANO_URL, width=10.16, rows=3,
        descr="Single-cell LiPo battery connection (2 pins). Connector type is TBD.",
        left=[(0, "1", "BAT+"), (2, "2", "BAT-")], right=[], footprint=""),
    "Phob_J6": dict(
        ref="J", datasheet="https://github.com/PhobGCC/PhobGCCv2-HW/tree/v2.0.5/PCB/KiCAD",
        width=12.7, rows=7,
        descr="Mirror of PhobGCC 2.0.5 header J6 (6-pin, 2.00 mm). The real J6 is on the Phob sheet.",
        left=[], right=[(0, "1", "+3V3"), (1, "2", "GPIO12"), (2, "3", "GPIO13"),
                        (3, "4", "GPIO14"), (4, "5", "GPIO15"), (5, "6", "GND")],
        footprint="Connector_PinSocket_2.00mm:PinSocket_1x06_P2.00mm_Vertical"),
}
PICO_URL = "https://github.com/heatherspacek/gcwireless_bridge"
SYMS["RP2040_Pico_Bridge"] = dict(
    ref="U", datasheet=PICO_URL, width=35.56, rows=13,
    descr="Raspberry Pi Pico (the board gcwireless_bridge builds for) - only the pins the bridge code uses. "
          "Pin numbers are the GPIO numbers, not physical pin numbers (those were not checked).",
    left=[(4, "GP27", "GP27 (joybus DATA)"), (9, "GND", "GND")],
    right=[(3, "GNDR", "GND"), (6, "GP18", "GP18 SPI0 SCK"), (7, "GP16", "GP16 SPI0 RX"),
           (8, "GP19", "GP19 SPI0 TX"), (9, "GP17", "GP17 SPI0 CSn")],
    footprint="")
# pico: right GND shares the net with left GND (two physical GND pads)
SYMS["RP2040_Pico_Bridge"]["right"][0] = (3, "GND2", "GND")
SYMS["RP2040_Pico_Bridge"]["left"][1] = (9, "GND1", "GND")


def pin_xy(sym, side, row):
    """Pin connection point relative to symbol origin, schematic coordinates (y down)."""
    s = SYMS[sym]
    ymid = (s["rows"] - 1) / 2
    y = (row - ymid) * PITCH
    x = (s["width"] / 2 + G) * (-1 if side == "L" else 1)
    return x, y


def sym_text(name, prefix=""):
    s = SYMS[name]
    full = prefix + name
    w, n = s["width"], s["rows"]
    top = (n - 1) / 2 * PITCH + PITCH / 2
    out = []
    out.append(f'(symbol {q(full)} (pin_names (offset 1.016)) (exclude_from_sim no) (in_bom yes) (on_board yes)')
    out.append(f'  (property "Reference" {q(s["ref"])} (at 0 {top + 1.27:.3f} 0) (effects {FONT}))')
    out.append(f'  (property "Value" {q(name)} (at 0 {-top - 1.27:.3f} 0) (effects {FONT}))')
    out.append(f'  (property "Footprint" {q(s["footprint"])} (at 0 0 0) (effects {FONT} (hide yes)))')
    out.append(f'  (property "Datasheet" {q(s["datasheet"])} (at 0 0 0) (effects {FONT} (hide yes)))')
    out.append(f'  (property "Description" {q(s["descr"])} (at 0 0 0) (effects {FONT} (hide yes)))')
    out.append(f'  (symbol {q(name + "_0_1")} (rectangle (start {-w/2:.3f} {top:.3f}) (end {w/2:.3f} {-top:.3f})'
               f' (stroke (width 0.254) (type default)) (fill (type background))))')
    out.append(f'  (symbol {q(name + "_1_1")}')
    ymid = (n - 1) / 2
    for side, pins, x, ang in (("L", s["left"], -w / 2 - G, 0), ("R", s["right"], w / 2 + G, 180)):
        for row, num, pname in pins:
            y = -(row - ymid) * PITCH  # symbol coords: y up
            out.append(f'    (pin passive line (at {x:.3f} {y:.3f} {ang}) (length {G})'
                       f' (name {q(pname)} (effects {FONT})) (number {q(num)} (effects {FONT})))')
    out.append('  )')
    out.append('  (embedded_fonts no))')
    return "\n".join(out)


def write_lib():
    parts = ['(kicad_symbol_lib (version 20241209) (generator "gen-hardware.py") (generator_version "10.0")']
    for name in SYMS:
        parts.append(sym_text(name))
    parts.append(")")
    (HW / "lib" / f"{LIB}.kicad_sym").write_text("\n".join(parts) + "\n", encoding="utf-8", newline="\n")
    (HW / "sym-lib-table").write_text(
        '(sym_lib_table\n  (version 7)\n'
        f'  (lib (name "{LIB}")(type "KiCad")(uri "${{KIPRJMOD}}/lib/{LIB}.kicad_sym")(options "")'
        '(descr "Symbols made for this project (GPL-3.0)"))\n)\n', encoding="utf-8", newline="\n")
    fp = ('(fp_lib_table\n  (version 7)\n'
          '  (lib (name "PhobGCC_2_0_0_footprints")(type "KiCad")'
          '(uri "${KIPRJMOD}/phob/PhobGCC_2_0_0_footprints.pretty")(options "")'
          '(descr "Footprints from PhobGCCv2-HW ff645aa (CERN-OHL-S v2)"))\n)\n')
    (HW / "fp-lib-table").write_text(fp, encoding="utf-8", newline="\n")


# ---------------------------------------------------------------- sheets
class Sheet:
    def __init__(self, file, title, sheet_uuid, page, comment="", paper="A4"):
        self.file, self.title, self.sheet_uuid, self.page = file, title, sheet_uuid, page
        self.comment, self.paper = comment, paper
        self.items, self.used, self.pos = [], set(), {}

    # --- placement
    def place(self, sym, ref, value, x, y, *, align=None, ref_dx=0, fp=None):
        """align=(side,row,y): put the symbol so that pin (side,row) sits at schematic y."""
        if align:
            side, row, ay = align
            y = ay - pin_xy(sym, side, row)[1]
        self.pos[ref] = (sym, x, y)
        self.used.add(sym)
        s = SYMS[sym]
        top = (s["rows"] - 1) / 2 * PITCH + PITCH / 2
        pins = "".join(f'(pin {q(num)} (uuid {q(uid(self.file, ref, num))}))'
                       for _, num, _ in s["left"] + s["right"])
        self.items.append(
            f'(symbol (lib_id {q(LIB + ":" + sym)}) (at {x:.3f} {y:.3f} 0) (unit 1) (exclude_from_sim no)'
            f' (in_bom yes) (on_board yes) (dnp no) (uuid {q(uid(self.file, ref))})\n'
            f'  (property "Reference" {q(ref)} (at {x + ref_dx:.3f} {y - top - 1.27:.3f} 0) (effects {FONT}))\n'
            f'  (property "Value" {q(value)} (at {x + ref_dx:.3f} {y + top + 1.27:.3f} 0) (effects {FONT}))\n'
            f'  (property "Footprint" {q(fp if fp is not None else s["footprint"])} (at {x:.3f} {y:.3f} 0) (effects {FONT} (hide yes)))\n'
            f'  (property "Datasheet" {q(s["datasheet"])} (at {x:.3f} {y:.3f} 0) (effects {FONT} (hide yes)))\n'
            f'  {pins}\n'
            f'  (instances (project {q(PROJECT)} (path {q("/" + ROOT_UUID + "/" + self.sheet_uuid)}'
            f' (reference {q(ref)}) (unit 1)))))')

    def pin(self, ref, side, row):
        sym, x, y = self.pos[ref]
        dx, dy = pin_xy(sym, side, row)
        return x + dx, y + dy

    # --- drawing primitives
    def wire(self, a, b):
        self.items.append(f'(wire (pts (xy {a[0]:.3f} {a[1]:.3f}) (xy {b[0]:.3f} {b[1]:.3f}))'
                          f' (stroke (width 0) (type default)) (uuid {q(uid(self.file, "w", len(self.items)))}))')

    def label(self, text, at, side="R", glob=False, shape="passive"):
        ang, just = (0, "left") if side == "R" else (180, "right")
        if glob:
            self.items.append(
                f'(global_label {q(text)} (shape {shape}) (at {at[0]:.3f} {at[1]:.3f} {ang}) (fields_autoplaced yes)'
                f' (effects {FONT} (justify {just})) (uuid {q(uid(self.file, "g", len(self.items)))})'
                f' (property "Intersheetrefs" "${{INTERSHEET_REFS}}" (at 0 0 0) (effects {FONT} (hide yes))))')
        else:
            self.items.append(
                f'(label {q(text)} (at {at[0]:.3f} {at[1]:.3f} {ang}) (effects {FONT} (justify {just} bottom))'
                f' (uuid {q(uid(self.file, "l", len(self.items)))}))')

    def stub(self, ref, side, row, text, length=7.62, glob=False):
        p = self.pin(ref, side, row)
        e = (p[0] + (length if side == "R" else -length), p[1])
        self.wire(p, e)
        self.label(text, e, side, glob)

    def link(self, ref_a, side_a, row_a, ref_b, side_b, row_b, text):
        a, b = self.pin(ref_a, side_a, row_a), self.pin(ref_b, side_b, row_b)
        assert abs(a[1] - b[1]) < 1e-6, (ref_a, ref_b, a, b)
        self.wire(a, b)
        self.label(text, ((a[0] + b[0]) / 2 - 4, a[1]), "R")

    def nc(self, ref, side, row):
        p = self.pin(ref, side, row)
        self.items.append(f'(no_connect (at {p[0]:.3f} {p[1]:.3f}) (uuid {q(uid(self.file, "nc", len(self.items)))}))')

    def nc_rest(self, ref, used):
        sym, _, _ = self.pos[ref]
        s = SYMS[sym]
        for side, pins in (("L", s["left"]), ("R", s["right"])):
            for row, num, _n in pins:
                if (side, row) not in used:
                    self.nc(ref, side, row)

    def text(self, s, x, y, size=1.27):
        self.items.append(f'(text {q(s)} (exclude_from_sim no) (at {x:.3f} {y:.3f} 0)'
                          f' (effects (font (size {size} {size})) (justify left top)) (uuid {q(uid(self.file, "t", len(self.items)))}))')

    def rect(self, a, b, width=0.3, fill=False):
        f = "background" if fill else "none"
        self.items.append(f'(rectangle (start {a[0]:.3f} {a[1]:.3f}) (end {b[0]:.3f} {b[1]:.3f})'
                          f' (stroke (width {width}) (type default)) (fill (type {f})) (uuid {q(uid(self.file, "r", len(self.items)))}))')

    def circle(self, c, r=0.8, fill=True):
        f = "outline" if fill else "none"
        self.items.append(f'(circle (center {c[0]:.3f} {c[1]:.3f}) (radius {r}) (stroke (width 0.15) (type default))'
                          f' (fill (type {f})) (uuid {q(uid(self.file, "c", len(self.items)))}))')

    def label_text(self, s, x, y, just="left", size=1.5, bold=False):
        b = " bold" if bold else ""
        j = "" if just == "center" else f" (justify {just})"
        self.items.append(f'(text {q(s)} (exclude_from_sim no) (at {x:.3f} {y:.3f} 0)'
                          f' (effects (font (size {size} {size}){b}){j}) (uuid {q(uid(self.file, "t", len(self.items)))}))')

    def render(self):
        libs = "\n".join(sym_text(n, LIB + ":") for n in sorted(self.used))
        return (f'(kicad_sch (version 20250114) (generator "gen-hardware.py") (generator_version "10.0")\n'
                f'(uuid {q(uid(self.file, "sheet"))})\n(paper "{self.paper}")\n'
                f'(title_block (title {q(self.title)}) (date "2026-11-05") (company "GCC-Wireless (GPL-3.0)")'
                f' (comment 1 {q(self.comment)}))\n'
                f'(lib_symbols\n{libs}\n)\n' + "\n".join(self.items) + '\n(embedded_fonts no)\n)\n')


D_L = ["", "D1", "D0", "", "", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9"]
D_R = ["", "", "", "", "", "D21", "D20", "D19", "D18", "D15", "D14", "D16", "D10"]


def nano_sheet(s):
    """Front and reverse view of the nice!nano v2 with the labels on the pins, like the official image."""
    row, top, w = 5.08, 62.0, 22.86

    def board(cx, title, back):
        x0, x1 = cx - w / 2, cx + w / 2
        s.rect((x0, top - 8), (x1, top + 12 * row + 8), 0.5)
        s.rect((cx - 4.5, top - 8), (cx + 4.5, top - 2), 0.3)  # USB-C shell
        s.label_text("USB-C", cx, top - 5, "center", 1.0)
        s.label_text(title, cx, top - 13, "center", 2.0, True)
        for r in range(13):
            y = top + r * row
            s.circle((x0 + 1.5, y))
            s.circle((x1 - 1.5, y))
            ln, rn = (NANO_RIGHT[r], NANO_LEFT[r]) if back else (NANO_LEFT[r], NANO_RIGHT[r])
            s.label_text(ln, x0 - 2, y, "right", 1.5, True)
            s.label_text(rn, x1 + 2, y, "left", 1.5, True)
            if not back:
                if D_L[r]:
                    s.label_text(D_L[r], x0 - 15, y, "right", 1.5)
                if D_R[r]:
                    s.label_text(D_R[r], x1 + 15, y, "left", 1.5)
    board(60, "FRONT (USB-C at top)", False)
    board(190, "REVERSE (left-right mirrored)", True)
    # reverse-only pads, as on the official image (positions approximate)
    cx = 190
    s.rect((cx - 1.5, top + 2.5 * row - 1), (cx + 1.5, top + 2.5 * row + 1), 0.2, True)
    s.label_text("BOOST pads (bridge for 500 mA charge)", cx + 24, top + 2.5 * row, "left", 1.3)
    for i, name in enumerate(["SWC", "SWD", "P1.01", "P1.02", "P1.07"]):
        y = top + (8.5 + i * 0.75) * row
        s.rect((cx + 3, y - 0.8), (cx + 6, y + 0.8), 0.2, True)
        s.label_text(name, cx + 24, y, "left", 1.3)
    # legend / notes under the boards
    ny = top + 12 * row + 20
    s.text("Source: https://nicekeyboards.com/docs/nice-nano/pinout-schematic (pinout-v2.png, fetched 2026-11-05).\n"
           "Pin names and D numbers are copied from that image (Dn = Arduino label). Pin numbers 1-26 are ours.\n"
           "BATTERY+ appears twice on the front, as on the image. When P0.13 is set low, power to 3.3V is cut off.\n"
           "Back pads (SWC, SWD, P1.01, P1.02, P1.07, BOOST) are named as on the image; their positions here are approximate.\n"
           "BOOST: bridging the back jumper raises the charge rate from 100 mA to 500 mA (only for batteries > 500 mAh).",
           20, ny, 1.27)


def build_sheets():
    sheets = []

    # ---- reference: nice!nano pinout
    s = Sheet("ref_nicenano.kicad_sch", "Ref nice!nano v2 pinout", uid("s", "nano"), 3,
              "Reference only - no wiring. Redrawn from the official v2 pinout image.")
    nano_sheet(s)
    sheets.append(s)

    # ---- reference: GameCube port
    s = Sheet("ref_gc_port.kicad_sch", "Ref GameCube port pinout", uid("s", "gcport"), 4,
              "Reference only - no wiring.")
    s.place("GameCube_Plug", "J302", "GameCube plug", 50, 45)
    s.nc_rest("J302", set())
    s.text("Source: https://www.int03.co.uk/crema/hardware/gamecube/gc-control.html (read 2026-11-05).\n"
           "Pin numbers are that page's own, viewed looking into the console socket (so a plug is the mirror).\n"
           "1 yellow: 5 V supply (used by the rumble motor)\n"
           "2 red: DATA, bidirectional, pull-up to 3.43 V\n"
           "3 green: ground      4 white: ground (Skillz adapter ties 3 and 4 together)\n"
           "5: not connected by the official controller\n"
           "6 blue: 3.43 V logic supply (page measured 3.43 V on a PAL console; calls 3.3 V a likely fine choice)\n"
           "7 black: cable shield / ground\n"
           "The page's own caveat: pinout is deduced from multimeter and oscilloscope work, no guarantee.\n"
           "Cross-check: Phob J1 (cable pads) in the Phob sheet = 1 GCC_3.3V, 2 +5V, 3 GCC_DATA, 4-6 GND\n"
           "(docs/facts/phobgcc.md, netlist of PhobGCCv2-HW ff645aa). Same four signals, different numbering.\n"
           "Bridge data pin: GP27 (upstream/gcwireless_bridge @ 5c31147, src/main.cpp line 10).", 20, 80)
    sheets.append(s)

    # ---- reference: bridge pins
    s = Sheet("ref_rp2040_bridge.kicad_sch", "Ref RP2040 bridge pins", uid("s", "bridge"), 5,
              "Reference only - no wiring.")
    s.place("RP2040_Pico_Bridge", "U303", "Raspberry Pi Pico (bridge)", 60, 45)
    s.nc_rest("U303", set())
    s.text("Source: upstream/gcwireless_bridge @ 5c31147 (https://github.com/heatherspacek/gcwireless_bridge).\n"
           "Board: CMakeLists.txt sets no board, so the Pico SDK default (pico) applies; build-support/build-bridge.sh\n"
           "passes -DPICO_BOARD=pico. The SDK header boards/pico.h (SDK 2.1.1) defines the default SPI pins.\n\n"
           "GPIO  use                         source line\n"
           "GP27  joybus DATA to console      src/main.cpp:10  _pinTX = 27 ; enterMode(_pinTX, ...)\n"
           "GP16  SPI0 RX (data in)           src/main.cpp:87  PICO_DEFAULT_SPI_RX_PIN  (pico.h: 16)\n"
           "GP18  SPI0 SCK (clock in)         src/main.cpp:88  PICO_DEFAULT_SPI_SCK_PIN (pico.h: 18)\n"
           "GP19  SPI0 TX (data out)          src/main.cpp:89  PICO_DEFAULT_SPI_TX_PIN  (pico.h: 19)\n"
           "GP17  SPI0 CSn (chip select)      src/main.cpp:90  PICO_DEFAULT_SPI_CSN_PIN (pico.h: 17)\n"
           "GP25  onboard LED, set high       src/joybus.cpp:100 gpio_put(25, 1)\n"
           "SPI runs as slave (src/main.cpp:86 spi_set_slave), 1 MHz setting, 10-byte reads (BUF_LEN = 10).\n"
           "Pin numbers on the symbol are GPIO numbers; physical pin numbers were not checked.", 20, 90)
    sheets.append(s)

    # ---- TX add-on
    s = Sheet("tx_addon.kicad_sch", "Controller add-on TX", uid("s", "tx"), 6,
              "Drawing only. TBD items are decisions the upstream code does not make.")
    nano_x, nano_y = 170, 95
    s.place("NiceNano_v2", "U101", "nice!nano v2 (TX)", nano_x, nano_y)
    s.place("Phob_J6", "J102", "Phob J6 (mirror)", 55, 0, align=("R", 0, s.pin("U101", "R", 4)[1]),
            fp="Connector_PinSocket_2.00mm:PinSocket_1x06_P2.00mm_Vertical")
    # ^ J6 pin 1 (+3V3) is level with the nice!nano 3.3V pin only for tidiness
    s.place("Battery_Conn", "J103", "LiPo battery", 255, 0, align=("L", 0, s.pin("U101", "R", 0)[1]))
    # power nets (global names; GND and +3V3 are also global in the Phob sheet)
    s.stub("J102", "R", 0, "+3V3", 22.86, glob=True)
    # KiCad 10 splits the Phob 3.3 V rail into "+3.3V" and "+3V3" when the old file is a sub-sheet
    # (a standalone netlist of the same file has one net). This second label joins them again.
    p0 = s.pin("J102", "R", 0)
    s.label("+3.3V", (p0[0] + 5.08, p0[1]), "R", glob=True)
    s.stub("J102", "R", 5, "GND", 10.16, glob=True)
    s.stub("U101", "R", 4, "+3V3", 10.16, glob=True)
    for row in (2,):
        s.stub("U101", "R", row, "GND", 10.16, glob=True)
    s.stub("U101", "L", 0, "GND", 10.16, glob=True)
    s.stub("U101", "L", 3, "GND", 10.16, glob=True)
    s.stub("U101", "L", 4, "GND", 10.16, glob=True)
    # battery
    s.wire(s.pin("J103", "L", 0), s.pin("U101", "R", 0))
    s.label("BAT+", ((s.pin("J103", "L", 0)[0] + s.pin("U101", "R", 0)[0]) / 2 - 4, s.pin("U101", "R", 0)[1]))
    s.wire(s.pin("U101", "R", 1), (s.pin("U101", "R", 1)[0] + 7.62, s.pin("U101", "R", 1)[1]))
    s.label("BAT+", (s.pin("U101", "R", 1)[0] + 7.62, s.pin("U101", "R", 1)[1]))
    s.stub("J103", "L", 2, "GND", 7.62, glob=True)
    # Phob GPIO labels, left unconnected on the nice!nano side (TBD)
    for i, row in enumerate((1, 2, 3, 4)):
        s.stub("J102", "R", row, f"GPIO{12 + i}", 10.16)
    # code-derived pins
    s.stub("U101", "L", 5, "LIGHT_IN", 10.16)
    s.stub("U101", "R", 5, "POWEROFF_IN", 10.16)
    used = {("L", 0), ("L", 3), ("L", 4), ("L", 5), ("R", 0), ("R", 1), ("R", 2), ("R", 4), ("R", 5)}
    s.nc_rest("U101", used)
    s.text("TBD (not invented): which nice!nano pins receive Phob GPIO12-GPIO15 and whether the link is SPI or UART.\n"
           "Upstream gcwireless TX code (src/tx.cpp @ 576878d) has no Phob link at all: it only reads P0.17 (light\n"
           "sensor test, INPUT_PULLUP, tx.cpp lines 7 and 96) and P0.31 (power-down input, tx.cpp lines 5 and 88).\n"
           "Those two are labelled LIGHT_IN and POWEROFF_IN here; they are firmware test pins, not final wiring.\n"
           "TBD: power direction on J6 pin 1. The Phob 3.3 V rail is normally fed by +5V -> AMS1117 -> D1\n"
           "(docs/facts/phobgcc.md); feeding +3V3 from the nice!nano 3.3V pin is unverified (docs/facts/power.md).\n"
           "TBD: battery connector type (nice!nano has BATTERY+ pads; pinout page above).\n"
           "BAT+ goes to both BATTERY+ pins, as the official image shows two.", 15, 15)
    sheets.append(s)

    # ---- RX receiver
    s = Sheet("rx_receiver.kicad_sch", "Console receiver RX", uid("s", "rx"), 7,
              "Drawing only. TBD items are decisions the upstream code does not make.")
    s.place("NiceNano_v2", "U201", "nice!nano v2 (RX)", 215, 95)
    y_spi = s.pin("U201", "L", 6)[1]
    s.place("RP2040_Pico_Bridge", "U202", "Raspberry Pi Pico (bridge)", 130, 0, align=("R", 6, y_spi))
    s.place("GameCube_Plug", "J201", "GameCube plug", 40, 0, align=("R", 1, s.pin("U202", "L", 4)[1]))
    # SPI between nano (master) and Pico (slave)
    s.link("U201", "L", 6, "U202", "R", 6, "SPI_SCK")      # P0.20 -> GP18
    s.link("U201", "L", 7, "U202", "R", 7, "SPI_MOSI")     # P0.22 -> GP16 (Pico RX)
    s.link("U201", "L", 8, "U202", "R", 8, "SPI_MISO")     # P0.24 <- GP19 (Pico TX)
    s.stub("U202", "R", 9, "SPI_CSN_TBD", 10.16)          # GP17, nRF side not decided in code
    s.link("U201", "L", 3, "U202", "R", 3, "GND")          # GND to GND
    # globals for the rest of GND on nano
    s.stub("U201", "L", 0, "GND", 10.16, glob=True)
    s.stub("U201", "L", 4, "GND", 10.16, glob=True)
    s.stub("U201", "R", 2, "GND", 10.16, glob=True)
    # console side
    s.link("J201", "R", 1, "U202", "L", 4, "JOYBUS_DATA")  # DATA <-> GP27
    s.stub("U202", "L", 9, "GND", 10.16, glob=True)
    s.stub("J201", "R", 2, "GND", 10.16, glob=True)
    s.stub("J201", "R", 3, "GND", 10.16, glob=True)
    s.stub("J201", "R", 6, "GND", 10.16, glob=True)
    s.stub("J201", "R", 0, "GC_5V_TBD", 10.16)
    s.stub("J201", "R", 5, "GC_3V3_TBD", 10.16)
    s.nc("J201", "R", 4)
    used_nano = {("L", 0), ("L", 3), ("L", 4), ("L", 6), ("L", 7), ("L", 8), ("R", 2)}
    s.nc_rest("U201", used_nano)
    s.text("SPI (Serial Peripheral Interface) nets, from the code:\n"
           "  nRF52 side: upstream/gcwireless src/rx.cpp @ 576878d lines 72-76: nrf_spim_pins_set(NRF_SPIM3,\n"
           "    PIN_020 /*SCK*/, PIN_022 /*MOSI*/, PIN_024 /*MISO*/). With build-support/gcwireless/pins.h (ours),\n"
           "    PIN_020 = P0.20, PIN_022 = P0.22, PIN_024 = P0.24 (D3, D4, D5 on the official image).\n"
           "  RP2040 side: upstream/gcwireless_bridge @ 5c31147 src/main.cpp lines 85-90 (slave on the SDK default\n"
           "    SPI0 pins: SCK GP18, RX GP16, TX GP19, CSn GP17; values from pico.h in Pico SDK 2.1.1).\n"
           "  So SCK P0.20 -> GP18, MOSI P0.22 -> GP16 (the Pico's RX), MISO P0.24 <- GP19 (the Pico's TX).\n"
           "  Direction wording (MOSI/MISO) is our reading of which side is master; the code does not say it outright.\n"
           "Joybus DATA: bridge GP27 (src/main.cpp:10) to GameCube plug pin 2 (int03 numbering).\n"
           "TBD: chip select. rx.cpp lines 66-71 has the nRF CSN setup (PIN_002) commented out, so no nRF pin is chosen;\n"
           "  GP17 (CSn) is drawn dangling as SPI_CSN_TBD.\n"
           "TBD: how the receiver is powered (GC +5V and 3.43V are labelled only); the code is silent.\n"
           "Note the bridge currently copies only byte 0 of the SPI data (main.cpp line 104), and reads 10 bytes.", 15, 15)
    sheets.append(s)
    return sheets


def write_root(sheets):
    items = []
    entries = [("PhobGCC 2.0.5", "phob/PhobGCC_2_0_0_proto_1.kicad_sch", uid("s", "phob"), 2)]
    for s in sheets:
        entries.append((s.title, s.file, s.sheet_uuid, s.page))
    entries.sort(key=lambda e: e[3])
    for i, (name, file, su, page) in enumerate(entries):
        x, y = 20 + (i % 2) * 130, 50 + (i // 2) * 40
        items.append(
            f'(sheet (at {x} {y}) (size 100 14) (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)'
            f' (fields_autoplaced yes) (stroke (width 0.1524) (type solid)) (fill (color 0 0 0 0.0))'
            f' (uuid {q(su)})\n'
            f'  (property "Sheetname" {q(name)} (at {x} {y - 0.7} 0) (effects {FONT} (justify left bottom)))\n'
            f'  (property "Sheetfile" {q(file)} (at {x} {y + 14.7} 0) (effects {FONT} (justify left top)))\n'
            f'  (instances (project {q(PROJECT)} (path "/{ROOT_UUID}" (page "{page}")))))')
    items.append('(text "GCC-Wireless KiCad workspace. Open a sheet: double-click it (or select it, Ctrl+Tab).\\n'
                 'PhobGCC 2.0.5 is an unmodified copy of upstream (see phob/SOURCE.md). The other sheets are ours.\\n'
                 'Guide: docs/HARDWARE.md" (exclude_from_sim no) (at 20 20 0) (effects (font (size 1.27 1.27)) (justify left top))'
                 f' (uuid {q(uid("root", "text"))}))')
    (HW / "GCC-Wireless.kicad_sch").write_text(
        f'(kicad_sch (version 20250114) (generator "gen-hardware.py") (generator_version "10.0")\n'
        f'(uuid {q(ROOT_UUID)})\n(paper "A4")\n'
        f'(title_block (title "GCC-Wireless: schematics for the wireless PhobGCC") (date "2026-11-05")'
        f' (company "GCC-Wireless (GPL-3.0); Phob sheet CERN-OHL-S v2"))\n'
        f'(lib_symbols)\n' + "\n".join(items) + '\n'
        f'(sheet_instances (path "/" (page "1")))\n(embedded_fonts no)\n)\n',
        encoding="utf-8", newline="\n")


def main():
    write_lib()
    sheets = build_sheets()
    for s in sheets:
        (HW / s.file).write_text(s.render(), encoding="utf-8", newline="\n")
    write_root(sheets)
    pro = HW / "GCC-Wireless.kicad_pro"
    if not pro.exists():
        pro.write_text('{\n  "meta": {"filename": "GCC-Wireless.kicad_pro", "version": 3},\n'
                       '  "schematic": {"drawing": {"default_text_size": 50.0}}\n}\n', encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
