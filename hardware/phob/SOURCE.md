# Source of the files in this folder

Unmodified copies from https://github.com/PhobGCC/PhobGCCv2-HW at commit **ff645aa** (2023-04-17), which is the upstream tag **v2.0.5** (`git ls-remote --tags origin`, 2026-11-05: v2.0.5 = ff645aa = HEAD). The submodule `upstream/PhobGCCv2-HW` in this repo is pinned to the same commit.

| Here | Upstream path |
|---|---|
| `PhobGCC_2_0_0_proto_1.kicad_sch` | `PCB/KiCAD/PhobGCC_2_0_0_proto_1.kicad_sch` |
| `PhobGCC_2_0_0_proto_1.kicad_pcb` | `PCB/KiCAD/PhobGCC_2_0_0_proto_1.kicad_pcb` |
| `PhobGCC_2_0_0_proto_1.kicad_pro` | `PCB/KiCAD/PhobGCC_2_0_0_proto_1.kicad_pro` |
| `PhobGCC_2_0_0_footprints.pretty/` | `PCB/KiCAD/PhobGCC_2_0_0_footprints.pretty/` |

The file names say "2_0_0_proto_1" for historical reasons; the board silkscreen reads "PhobGCC 2.0.5" and the commit message at ff645aa is "revert pads to 2.0.2, rev to 2.0.5".

**Licence: CERN-OHL-S v2** (CERN Open Hardware Licence Version 2 - Strongly Reciprocal), upstream file `LICENSE`. Changes to these files must be published under the same licence.

**Why copies and not a path into `upstream/`:** KiCad rewrites a schematic in its own newer format when it saves the project, and this file is KiCad 6 format (`version 20211123`). A relative path into the submodule would let KiCad edit the pinned upstream files. Copies keep `upstream/` untouched. Check that the copies are still byte-identical:
```
for f in kicad_sch kicad_pcb kicad_pro; do cmp hardware/phob/PhobGCC_2_0_0_proto_1.$f upstream/PhobGCCv2-HW/PCB/KiCAD/PhobGCC_2_0_0_proto_1.$f; done
```
Do not edit these files; open the PCB with `PhobGCC_2_0_0_proto_1.kicad_pro` in this folder if you want to look at the board layout.
