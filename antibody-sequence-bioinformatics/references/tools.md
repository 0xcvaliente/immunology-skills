# Tools

Check what is already installed and what the project pins before adding anything; versions here move, so confirm the current interface from the tool's own `--help` or documentation rather than trusting a remembered flag.

## Tool to job

| Job | Tool |
|---|---|
| Number a variable domain, extract CDRs, detect chain type | ANARCI, or **abnumber** for a friendlier Python API |
| Germline V(D)J assignment from nucleotide reads | IgBLAST (NCBI), or IMGT/V-QUEST for small interactive sets |
| Raw sequencing reads to annotated repertoire | MiXCR (licence terms apply to commercial use), or pRESTO + IgBLAST + Change-O from Immcantation |
| Clonal grouping, lineage, mutation analysis | Change-O, SHazaM, Dowser (Immcantation, R) |
| Single-cell BCR with transcriptome | scirpy (Python), Dandelion (Python), immunarch or scRepertoire (R) |
| Repertoire statistics and diversity | immunarch (R), alakazam (R) |
| Read and write AIRR files with schema validation | the `airr` Python or R package |
| General sequence parsing and translation | Biopython, biotite |
| Structure prediction | ABodyBuilder3 / ImmuneBuilder (OPIG), or an AlphaFold-family model |
| Developability flags from sequence or structure | TAP (Therapeutic Antibody Profiler, OPIG) plus the motif checks in `liabilities.md` |
| Background repertoire context | OAS (Observed Antibody Space) |

OPIG periodically replaces its tools with successors (ANARCI has newer siblings); start from `https://opig.stats.ox.ac.uk/webapps` and use the current one rather than pinning to a name from memory.

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
