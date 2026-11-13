# Tools

Check what is already installed and what the project pins before adding anything; versions here move, so confirm the current interface from the tool's own `--help` or documentation rather than trusting a remembered flag.

## Tool to job

| Job | Tool |
|---|---|
| Number a variable domain, extract CDRs, detect chain type | **ANARCII** (language-model numbering; antibodies, VHH, TCR, shark VNAR), ANARCI, or **abnumber** for a friendlier Python API over ANARCI |
| First-pass QC of a VH/VHH sequence with nothing installed | `scripts/vhh_qc.py` (regions, hallmarks, cysteines, liabilities, charge) |
| Map CDRs to a structure's residue numbers; build a loop-redesign contig | `scripts/cdr_contig.py` |
| Where does a predicted complex touch the target | `scripts/interface_contacts.py` |
| Germline V(D)J assignment from nucleotide reads | IgBLAST (NCBI), or IMGT/V-QUEST for small interactive sets |
| Raw sequencing reads to annotated repertoire | MiXCR (licence terms apply to commercial use), pRESTO + IgBLAST + Change-O from Immcantation, or the nf-core **airrflow** Nextflow pipeline when a reproducible, containerised run matters |
| Clonal grouping, lineage, mutation analysis | Change-O, SHazaM, Dowser (Immcantation, R) |
| Single-cell BCR with transcriptome | scirpy (Python), Dandelion (Python), immunarch or scRepertoire (R) |
| Repertoire statistics and diversity | immunarch (R), alakazam (R) |
| Read and write AIRR files with schema validation | the `airr` Python or R package |
| General sequence parsing and translation | Biopython, biotite |
| Structure prediction of the binder alone | NanoBodyBuilder2 and ABodyBuilder3 / ImmuneBuilder (OPIG), or an AlphaFold-family model; complexes need a co-folding model (see antibody-binder-design) |
| Developability flags from sequence or structure | TAP (Therapeutic Antibody Profiler) for conventional antibodies, **TNP** (Therapeutic Nanobody Profiler) for VHHs, both OPIG, plus the motif checks in `liabilities.md` |
| Background repertoire context | OAS (Observed Antibody Space) |

OPIG periodically replaces its tools with successors (ANARCI has newer siblings); start from `https://opig.stats.ox.ac.uk/webapps` and use the current one rather than pinning to a name from memory.

## ANARCII

The successor to ANARCI from the same group: a transformer language model that predicts IMGT (or another scheme's) numbering for antibodies, TCRs and shark VNAR, with no HMMER dependency. `pip install anarcii` (installs PyTorch, so allow several minutes and a few hundred MB; the first import took about 9 s on a laptop CPU). Web tool: `https://opig.stats.ox.ac.uk/webapps/sabdab-sabpred/sabpred/anarcii/`. Paper: Greenshields-Watson et al., bioRxiv 2025, [doi:10.1101/2025.04.16.648720](https://doi.org/10.1101/2025.04.16.648720).

```python
from anarcii import Anarcii

model = Anarcii(seq_type="antibody", cpu=True)     # 'antibody' | 'tcr' | 'shark' | 'unknown'; a VHH is numbered as 'antibody'
result = model.number([seq1, seq2])                 # a list of sequences, a FASTA path or a PDB path
entry = next(iter(result.values()))                 # dict keyed per input, in input order
entry["chain_type"], entry["score"], entry["scheme"]    # 'H', a float score, 'imgt'
entry["numbering"]                                  # [((position, insertion_code), residue), ...]; '-' marks a gap
entry["query_start"], entry["query_end"], entry["error"]
```

`mode="accuracy"` (default) or `"speed"` picks the model; `to_legacy()` returns ANARCI-style output. Check `error` on every entry: a sequence that is not an antigen receptor variable domain fails rather than being forced. A shark VNAR pushed through the antibody model number scored about 18–19 against about 28–30 for confident heavy-chain domains in one panel (see `vhh.md`), so look at `score` and `chain_type`, not only at whether numbering came back. Build region strings from positions `a <= position <= b`, counting insertion positions (`111A`) under their integer position.

## ANARCI

HMM-based alignment to pre-numbered germline profiles; requires HMMER. Install via conda (`bioconda`) or pip from source.

```bash
ANARCI -i heavy.fasta --scheme imgt --restrict ig --csv -o numbered
ANARCI -i seqs.fasta --scheme chothia --assign_germline
```

It returns the numbering, the detected chain type and species, and germline assignment when asked. A sequence it cannot align is usually not an immunoglobulin variable domain, a truncated fragment, or in the wrong frame — inspect rather than discard silently.

## abnumber

A thin Python layer over ANARCI, and the shortest path to correct region handling:

```python
from abnumber import Chain

chain = Chain(vh_aa_sequence, scheme='imgt')
chain.cdr1_seq, chain.cdr2_seq, chain.cdr3_seq
chain.chain_type          # 'H', 'K' or 'L'
chain.positions           # position objects, insertion codes intact
chain.renumber('kabat')   # re-number, never re-index
```

Prefer `chain.positions` over slicing the raw string; the position objects carry insertion codes and gaps correctly.

## IgBLAST

Germline assignment and alignment from nucleotide sequences, with AIRR-format output:

```bash
igblastn \
  -germline_db_V imgt_human_ig_v -germline_db_D imgt_human_ig_d -germline_db_J imgt_human_ig_j \
  -organism human -ig_seqtype Ig -auxiliary_data optional_file/human_gl.aux \
  -outfmt 19 \
  -query reads.fasta -out out.tsv
```

`-outfmt 19` emits AIRR Rearrangement TSV, which is why IgBLAST is the usual front end for a pipeline. The germline databases must be built from a reference set (IMGT or OGRDB) with `makeblastdb`; record which reference set and version was used, because assignments change between sets and are not comparable across them.

## Writing pipeline code

- Read and write AIRR TSV through the `airr` package when validation matters, or pandas with `sep='\t'`, `dtype=str` for the identifier columns and explicit `na_values`, so `v_call` strings are never coerced.
- Stream large repertoire files; a single sample can run to millions of rows, and loading several into memory at once is the usual cause of a stalled analysis.
- Keep raw, annotated and filtered data as separate artefacts, each with the command that produced it recorded. Repertoire conclusions depend heavily on filtering, so the filter must be inspectable.
- Set a fixed random seed for any subsampling, and report the depth; diversity metrics are depth-dependent, so comparisons require equal depth or explicit rarefaction.
- Translate with an explicit frame and check for stop codons rather than assuming `productive`.
