# Numbering and regions

## The schemes

| Scheme | Basis | Notes |
|---|---|---|
| **IMGT** | Structural alignment, fixed positions 1–128 per domain with gaps | The default for repertoire work. Gaps are inserted at conserved structural positions, so position numbers are comparable across sequences of different lengths. |
| **Kabat** | Sequence variability, historical | Still dominant in the therapeutic and patent literature. Uses insertion codes (`H35A`, `H52A`, `L27A`) where sequences are longer than the reference. |
| **Chothia** | Structural loops | Like Kabat but with CDR-H1 and CDR-H2 shifted to match the structural loops. |
| **Martin** (extended Chothia) | Structural, corrected framework alignment | Common in structure-based work. |
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

**Kabat, Chothia, Martin** (heavy chain, in their own numbering):

| Region | Kabat | Chothia | Martin |
|---|---|---|---|
| CDR-H1 | 31–35B | 26–32 | 26–35 |
| CDR-H2 | 50–65 | 52–56 | 50–58 |
| CDR-H3 | 95–102 | 95–102 | 95–102 |

**Light chain** is 24–34, 50–56, 89–97 in Kabat, Chothia and Martin alike.

Consequences worth internalising:

- IMGT CDR-H1 and CDR-H2 are longer than the Chothia equivalents; a "CDR1 length" statistic is not portable between schemes.
- CDR-H3 shares the same endpoints across Kabat, Chothia and Martin, which is why CDR-H3 length is the one region length people compare loosely — but IMGT CDR3 includes the conserved flanking positions 105 and 117, so IMGT CDR3 lengths run two residues longer than junction-minus-anchors definitions.
- The **junction** in AIRR terms spans the conserved Cys to the conserved Trp/Phe inclusive, so `junction_aa` is CDR3 plus two residues. Mixing `junction_aa` and `cdr3_aa` in one analysis is a common and silent bug.
- **North** CDR definitions (from clustered loop conformations) are wider again; if a paper's CDR lengths look unfamiliar, check whether it used North.

## Insertion codes and gaps

- Kabat-family schemes extend positions with letters (`100A`, `100B`, …) for longer loops. Sort order is numeric-then-letter, which plain string sorting gets wrong.
- IMGT inserts gaps rather than letters, so an IMGT-numbered sequence has fixed positions and may contain gap characters. Stripping gaps destroys the alignment — keep the gapped form for position lookups and a separate ungapped sequence for identity calculations.
- A numbered sequence is a mapping from positions to residues, not a string. Represent it as a dict or an ordered list of `(position, insertion_code, residue)` and the index bugs disappear.

## Converting between schemes

Re-number the raw sequence under the target scheme with ANARCI or abnumber. There is no index-to-index lookup table that survives insertions, and arithmetic conversions found in old scripts are wrong for long CDR-H3s — which is to say, wrong exactly where it matters.
