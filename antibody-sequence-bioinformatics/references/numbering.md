# Numbering and regions

## The schemes

| Scheme | Basis | Notes |
|---|---|---|
| **IMGT** | Structural alignment, fixed positions 1–128 per domain with gaps | The default for repertoire work. Gaps are inserted at conserved structural positions, so position numbers are comparable across sequences of different lengths. |
| **Kabat** | Sequence variability, historical | Still dominant in the therapeutic and patent literature. Uses insertion codes (`H35A`, `H52A`, `L27A`) where sequences are longer than the reference. |
| **Chothia** | Structural loops | Like Kabat but with CDR-H1 and CDR-H2 shifted to match the structural loops. |
| **Martin** (AbM, extended Chothia) | Structural, corrected framework alignment | Common in structure-based work; extends CDR-H1 to 26–35 and trims CDR-H2. |
| **Contact** | Structural contacts between antibody and antigen | The widest of the common CDR definitions; used where the question is which residues touch antigen. |
| **AHo** | Structural, 149 positions | Designed for structural alignment across all immunoglobulin domains. |
| **EU** | Fc and constant region | What Fc engineering mutations are quoted in (`N297`, `L234A/L235A`, `M428L/N434S`). Separate from the variable-domain schemes — do not mix them in one coordinate statement. |

## CDR boundaries

Boundaries as commonly implemented. Verify against the output of the tool actually in use rather than hand-counting, because implementations differ at the edges and a one-residue disagreement changes a CDR3 length distribution.

**IMGT** (same positions for heavy and light):

| Region | Positions |
|---|---|
| FR1 | 1–26 |
| CDR1 | 27–38 |
| FR2 | 39–55 |
| CDR2 | 56–65 |
| FR3 | 66–104 |
| CDR3 | 105–117 |
| FR4 | 118–128 |

**Kabat, Chothia, Martin/AbM, Contact** (heavy chain, in each scheme's own numbering):

| Region | Kabat | Chothia | Martin / AbM | Contact |
|---|---|---|---|---|
| CDR-H1 | 31–35B | 26–32 | 26–35 | 30–35 |
| CDR-H2 | 50–65 | 52–56 | 50–58 | 47–58 |
| CDR-H3 | 95–102 | 95–102 | 95–102 | 93–101 |

**Light chain** is 24–34, 50–56, 89–97 in Kabat, Chothia and Martin alike; Contact is wider again at 30–36, 46–55, 89–96. Boundary tables here follow the definitions implemented by ANARCI and abYsis (Lefranc et al., *Dev. Comp. Immunol.* 2003; Zhu et al., *Protein Eng. Des. Sel.* 2025); a paper may use a different interpretation of the same scheme name, so verify against the tool's own output.

Consequences worth internalising:

- IMGT CDR-H1 and CDR-H2 are longer than the Chothia equivalents; a "CDR1 length" statistic is not portable between schemes.
- CDR-H3 shares the same endpoints across Kabat, Chothia and Martin, which is why CDR-H3 length is the one region length people compare loosely.
- The **IMGT CDR3-IMGT** of a rearranged domain is positions 105–117 and *excludes* the conserved 2nd-Cys at 104 and the J-Trp/Phe at 118. The **AIRR junction** spans 104 to 118 inclusive, so `junction_aa` is exactly two residues longer than the IMGT CDR3 it contains (13 CDR3 positions → 15 junction positions is the reference case). Mixing `junction_aa` and `cdr3_aa` in one length distribution or clonotype key is a common and silent bug.
- **North** CDR definitions (from clustered loop conformations) are wider again; if a paper's CDR lengths look unfamiliar, check whether it used North.
- A **VHH** is numbered as a heavy-chain variable domain, with the same IMGT ranges. Its CDR3 is often long, so the IMGT CDR3 carries insertion positions (`111A`, `112A`, ...) beyond the nominal 13 slots.

## Insertion codes and gaps

- Kabat-family schemes extend positions with letters (`100A`, `100B`, …) for longer loops. Sort order is numeric-then-letter, which plain string sorting gets wrong.
- IMGT inserts gaps rather than letters, so an IMGT-numbered sequence has fixed positions and may contain gap characters. Stripping gaps destroys the alignment — keep the gapped form for position lookups and a separate ungapped sequence for identity calculations.
- A numbered sequence is a mapping from positions to residues, not a string. Represent it as a dict or an ordered list of `(position, insertion_code, residue)` and the index bugs disappear.

## IMGT positions are not residue numbers in a structure file

A PDB or mmCIF file numbers residues in its own way (here, author numbering): usually 1, 2, 3 ... along the chain, with gaps where residues are unresolved and sometimes insertion codes. IMGT numbering has fixed slots with gaps and insertion positions. The two agree on nothing except by accident, and a contig, a hotspot list or a mutation (`N55A`) must be written in the file's numbering.

Worked example, PDB 1ZVY chain A (a dromedary VHH bound to hen lysozyme), IMGT regions placed by `scripts/cdr_contig.py` and checked against ANARCII:

| Region | IMGT positions | Residues | Residue numbers in the file |
|---|---|---|---|
| CDR1 | 27-38 | `GSTDSIEY` | A26-A33 |
| CDR2 | 56-65 | `LYTHTGNT` | A51-A58 |
| CDR3 | 105-117 (plus insertion positions) | `GATRKYVPVRFALDQSSYDY` (20 residues) | A97-A116 |
| FR4 | 118-128 | `WGQGTQVTV` (resolved part) | A117-A125 |

Two details that cost time if missed: residue A1 is excluded from the contig because its backbone N is absent in the file, and residues 126-136 (the end of FR4 and a tag) are unresolved, which is why a FR4 range stops at A125. The command that produced the table and a contig that regenerates CDR3 at its native length:

```bash
python3 scripts/cdr_contig.py 1ZVY.cif --chain A --target-chain B
# contig (guide style):  B1-129, /0, A2-96, 20, A117-125
```

## Converting between schemes

Re-number the raw sequence under the target scheme with ANARCI or abnumber. There is no index-to-index lookup table that survives insertions, and arithmetic conversions found in old scripts are wrong for long CDR-H3s — which is to say, wrong exactly where it matters.
