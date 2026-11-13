# Toolkit by workflow stage

Compiled 2026-11-14 from a practitioner overview supplied by the repository owner, then checked tool by tool: every link below returned HTTP 200 unless noted, and every DOI resolves to the paper named. Where the overview and the tool's own page disagreed, the page won and the difference is listed at the end. The field moves quickly, so confirm that a tool is still maintained, and what its licence allows for your use, before building on it.

"Public code" means a public repository exists; it says nothing about the licence. Papers are cited by DOI, preprints marked.

## 1. Sequence analysis, numbering, germline, humanness

| Tool | Does | Access and note |
|---|---|---|
| [ANARCI](https://github.com/oxpig/ANARCI) | Numbers antibody and TCR sequences (IMGT, Kabat, Chothia, AHo); the usual first step | Public code, needs HMMER. [doi:10.1093/bioinformatics/btv552](https://doi.org/10.1093/bioinformatics/btv552) |
| [ANARCII](https://github.com/oxpig/ANARCII) | Language-model successor to ANARCI; handles VHH and shark VNAR | `pip install anarcii`. [doi:10.1101/2025.04.16.648720](https://doi.org/10.1101/2025.04.16.648720) (preprint). Details in antibody-sequence-bioinformatics `tools.md` |
| [abnumber](https://github.com/prihoda/AbNumber) | Python wrapper over ANARCI with region and renumbering helpers | Public code |
| [IgBLAST](https://www.ncbi.nlm.nih.gov/igblast/) | Germline V(D)J assignment and somatic mutations from nucleotide or protein | Web and command line. [doi:10.1093/nar/gkt382](https://doi.org/10.1093/nar/gkt382) |
| [IMGT/DomainGapAlign](https://www.imgt.org/3Dstructure-DB/cgi/DomainGapAlign.cgi) | Closest germline for a variable domain, with IMGT-numbered alignment | Web |
| [BioPhi](https://github.com/Merck/BioPhi) ([web app](https://biophi.dichlab.org)), [Sapiens](https://github.com/Merck/Sapiens) | Humanisation, humanness evaluation (OASis score) and antibody design from natural repertoires; Sapiens is its antibody language model | Public code and a web app. [doi:10.1080/19420862.2021.2020203](https://doi.org/10.1080/19420862.2021.2020203) |

## 2. Structure prediction

| Tool | Does | Access and note |
|---|---|---|
| [ImmuneBuilder](https://github.com/oxpig/ImmuneBuilder) | ABodyBuilder2 (antibody), NanoBodyBuilder2 (nanobody) and TCRBuilder2 (TCR) Fv structures | Public code. [doi:10.1038/s42003-023-04927-7](https://doi.org/10.1038/s42003-023-04927-7) |
| [IgFold](https://github.com/Graylab/IgFold) | Fast antibody structure prediction from sequence | Public code. [doi:10.1038/s41467-023-38063-x](https://doi.org/10.1038/s41467-023-38063-x) |
| [AlphaFold 3](https://github.com/google-deepmind/alphafold3), [AlphaFold Server](https://alphafoldserver.com) | Complexes of proteins and other molecules, antibody–antigen included | Code on GitHub; the server is a web interface. Check the model-parameter terms. [doi:10.1038/s41586-024-07487-w](https://doi.org/10.1038/s41586-024-07487-w) |
| [Boltz](https://github.com/jwohlwend/boltz) | Open co-folding (Boltz-1, Boltz-2); Boltz-2 adds a binding-affinity head trained on protein–small-molecule data, not antibody–antigen | Public code. [doi:10.1101/2025.06.14.659707](https://doi.org/10.1101/2025.06.14.659707) (Boltz-2, preprint) |
| [Chai-1](https://github.com/chaidiscovery/chai-lab) | Co-folding of biomolecular complexes | Public code. [doi:10.1101/2024.10.10.615955](https://doi.org/10.1101/2024.10.10.615955) (preprint) |
| [ColabFold](https://github.com/sokrypton/ColabFold) | AlphaFold 2 and AlphaFold-Multimer with fast alignments; the easy way to run them | Public code and notebooks. [doi:10.1038/s41592-022-01488-1](https://doi.org/10.1038/s41592-022-01488-1) |

**Limit.** Fv prediction is good and fast; the antibody–antigen complex, and CDR3 in particular, is the weak point. Co-folding confidence is not affinity. See antibody-binder-design `references/models-and-metrics.md`.

## 3. Docking and interface analysis

| Tool | Does | Access and note |
|---|---|---|
| [HADDOCK](https://www.bonvinlab.org/software/haddock3/) ([web server](https://wenmr.science.uu.nl/haddock2.4/)) | Information-driven docking; takes epitope and paratope restraints | Software and web server. [doi:10.1016/j.str.2019.10.011](https://doi.org/10.1016/j.str.2019.10.011) (antibody–antigen) |
| [ClusPro](https://cluspro.bu.edu) | Rigid-body docking; an Antibody Mode (Advanced Options) uses an asymmetric potential and can mask non-CDR regions. [AbEMap](https://abemap.cluspro.org) predicts epitopes | Web server, reported free for non-commercial use; the `cluspro.org` address timed out on 2026-11-14, use `cluspro.bu.edu` |
| [ZDOCK](https://zdock.umassmed.edu) | FFT-based rigid-body docking | Web. [doi:10.1093/bioinformatics/btu097](https://doi.org/10.1093/bioinformatics/btu097) |
| [SAbPred](https://opig.stats.ox.ac.uk/webapps/sabdab-sabpred/sabpred) | OPIG suite of structure-based antibody prediction servers | Web. [doi:10.1093/nar/gkw361](https://doi.org/10.1093/nar/gkw361) |
| [ParaPred](https://github.com/eliberis/parapred) | Paratope prediction from sequence and structure | Public code. [doi:10.1093/bioinformatics/bty305](https://doi.org/10.1093/bioinformatics/bty305) |
| [PISA](https://www.ebi.ac.uk/pdbe/pisa/) | Interfaces, surfaces and assemblies from a structure: contact areas, bonds, predicted stability | Web (EBI). [doi:10.1016/j.jmb.2007.05.022](https://doi.org/10.1016/j.jmb.2007.05.022) |
| `interface_contacts.py` | Contacting residues, hotspot coverage and CDR contribution of a model | In antibody-sequence-bioinformatics |

**PLIP is not on this list on purpose.** [PLIP](https://plip-tool.biotec.tu-dresden.de/plip-web/plip/index) is a protein–*ligand* interaction profiler (2021: extended to DNA and RNA; [doi:10.1093/nar/gkab294](https://doi.org/10.1093/nar/gkab294)). Use it for small-molecule or peptide ligands. For an antibody–antigen interface use PISA or `interface_contacts.py`.

**Limit.** Treat a docking or co-folded pose as a hypothesis. Check it against anything known: epitope mapping, an alanine scan, published mutants. Restraints improve docking only when they are correct.

## 4. Mutation scoring: affinity maturation and stability

| Tool | Family | Does | Access and note |
|---|---|---|---|
| [Rosetta](https://rosettacommons.org) Flex ddG | Physics | Ensemble-based estimate of the change in binding energy on mutation | Licensed software, check terms. [doi:10.1021/acs.jpcb.7b11367](https://doi.org/10.1021/acs.jpcb.7b11367) |
| [FoldX](https://foldxsuite.crg.eu) | Physics | Fast empirical ΔΔG for stability and binding | Licensed, check terms. [doi:10.1093/nar/gki387](https://doi.org/10.1093/nar/gki387) |
| [ProteinMPNN](https://github.com/dauparas/ProteinMPNN) | Inverse folding | Sequences for a backbone; scores variants on a fixed structure | Public code. [doi:10.1126/science.add2187](https://doi.org/10.1126/science.add2187) |
| [ESM-IF1 and ESM-2](https://github.com/facebookresearch/esm) | Inverse folding; language model | Structure-conditioned and sequence-only scoring of variants | Public code. ESM-IF1: [doi:10.1101/2022.04.10.487779](https://doi.org/10.1101/2022.04.10.487779) (preprint) |
| [AbLang-2](https://github.com/oxpig/AbLang2) | Antibody language model | Likelihoods and embeddings; built to reduce germline bias | Public code. [doi:10.1101/2024.02.02.578678](https://doi.org/10.1101/2024.02.02.578678) (preprint) |
| [AntiBERTy](https://github.com/jeffreyruffolo/AntiBERTy) | Antibody language model | Embeddings and mutation scoring | Public code. [arXiv:2112.07782](https://arxiv.org/abs/2112.07782) |
| [IgLM](https://github.com/Graylab/IgLM) | Antibody language model | Generates and infills antibody sequence, including CDRs | Public code. [doi:10.1016/j.cels.2023.10.001](https://doi.org/10.1016/j.cels.2023.10.001) |
| [Graphinity](https://github.com/oxpig/Graphinity) | Learned ΔΔG | Equivariant graph network for antibody–antigen ΔΔG | Public code. [doi:10.1038/s43588-025-00823-8](https://doi.org/10.1038/s43588-025-00823-8) |

**What the evidence supports.** General protein language models can propose affinity-improving mutations from a sequence alone: [Hie et al., *Nat. Biotechnol.* 2023](https://doi.org/10.1038/s41587-023-01763-2) tested a small number of variants per antibody and reported improvements. A preprint benchmark, [AbBiBench](https://arxiv.org/abs/2506.04235) (over 184,000 measurements for 14 antibodies against 9 antigens, 15 models), found structure-conditioned inverse folding models best at tracking affinity. The Graphinity authors report that on current experimental data a learned ΔΔG model does not generalise robustly and that orders of magnitude more data are likely needed. Use language-model and inverse-folding scores as a cheap first filter, physics as a second opinion, and neither as a measurement.

## 5. Generative and de novo design

| Tool | Does | Access and note |
|---|---|---|
| [RFdiffusion](https://github.com/RosettaCommons/RFdiffusion), [RFantibody](https://github.com/RosettaCommons/RFantibody) | RFantibody fine-tunes RFdiffusion to design antibody and nanobody binders | Public code. RFdiffusion [doi:10.1038/s41586-023-06415-8](https://doi.org/10.1038/s41586-023-06415-8); RFantibody [doi:10.1101/2024.03.14.585103](https://doi.org/10.1101/2024.03.14.585103) (preprint) |
| [Germinal](https://github.com/SantiagoMille/germinal) | Epitope-targeted nanobody and scFv design | Public code. [doi:10.1038/s41587-026-03187-0](https://doi.org/10.1038/s41587-026-03187-0) |
| [BindCraft](https://github.com/martinpacesa/BindCraft) | Binder design from a target structure; not antibody-specific | Public code. [doi:10.1038/s41586-025-09429-6](https://doi.org/10.1038/s41586-025-09429-6) |
| [IgDesign](https://github.com/AbSciBio/igdesign) | CDR design by inverse folding, with wet-lab validation reported | Public code. [doi:10.1101/2023.12.08.570889](https://doi.org/10.1101/2023.12.08.570889) (preprint) |
| [dyMEAN](https://github.com/THUNLP-MT/dyMEAN) | End-to-end full-atom antibody design | Public code. [ICML 2023](https://proceedings.mlr.press/v202/kong23a.html), [arXiv:2302.00203](https://arxiv.org/abs/2302.00203) |
| AbDiffuser | Full-atom diffusion model for antibodies | Paper only: [NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/hash/801ec05b0aae9fcd2ef35c168bd538e0-Abstract.html); no official code repository could be confirmed |
| Chai-2 | Reported zero-shot antibody design ([doi:10.1101/2025.07.05.663018](https://doi.org/10.1101/2025.07.05.663018), preprint) | Availability not verified; ask the developer ([Chai Discovery](https://www.chaidiscovery.com)). Treat reported hit rates as the authors' claims |

This area changes monthly. For designing a binder from scratch, with the workflow, calibration and selection steps, use antibody-binder-design; this table only places the tools.

## 6. Developability and liabilities

| Tool | Does | Access and note |
|---|---|---|
| [TAP](https://opig.stats.ox.ac.uk/webapps/sabdab-sabpred/sabpred/tap) | Compares an antibody's developability properties with those of clinical-stage therapeutics | Web (OPIG). [doi:10.1073/pnas.1810576116](https://doi.org/10.1073/pnas.1810576116) |
| [TNP](https://tnp.opig.stats.ox.ac.uk/) | The same idea for nanobodies | Web and [code](https://github.com/oxpig/TNP). [doi:10.1101/2025.08.11.669635](https://doi.org/10.1101/2025.08.11.669635) (preprint) |
| SAP (spatial aggregation propensity) | Structure-based map of aggregation-prone surface patches | Method: [doi:10.1073/pnas.0904191106](https://doi.org/10.1073/pnas.0904191106). Needs a structure or model; implementations vary |
| [DeepSP](https://github.com/Lailabcode/DeepSP) | Predicts SAP- and spatial-charge-type properties from sequence as a surrogate for molecular dynamics | Public code. [CSBJ 2024](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11140563/) |
| [Aggrescan3D](https://biocomp.chem.uw.edu.pl/A3D2/) | Aggregation propensity of a structure | Web. [doi:10.1093/nar/gkv359](https://doi.org/10.1093/nar/gkv359) |
| [CamSol](https://www-cohsoftware.ch.cam.ac.uk/index.php/camsolintrinsic) | Intrinsic solubility and solubility-improving mutations | Web. [doi:10.1016/j.jmb.2014.09.026](https://doi.org/10.1016/j.jmb.2014.09.026) |
| Solubis | Suggests mutations that reduce aggregation | Server (`solubis.switchlab.org`) returned HTTP 502 on 2026-11-14; paper [doi:10.1093/protein/gzw019](https://doi.org/10.1093/protein/gzw019) |
| Motif scans | Deamidation (`NG`), isomerisation (`DG`), Met and Trp oxidation, N-glycosylation (`N-X-S/T`) | `vhh_qc.py` and antibody-sequence-bioinformatics `liabilities.md` |

## 7. Immunogenicity risk

| Tool | Does | Access and note |
|---|---|---|
| [NetMHCIIpan](https://services.healthtech.dtu.dk/services/NetMHCIIpan-4.3/) | Predicts peptide binding to MHC class II, the T-cell epitopes in a sequence | Web (DTU). [doi:10.1093/nar/gkaa379](https://doi.org/10.1093/nar/gkaa379) (NetMHCpan-4.1 and NetMHCIIpan-4.0) |
| [IEDB MHC-II tools](https://tools.iedb.org/mhcii/) | MHC class II binding predictions from the Immune Epitope Database | Web |
| EpiMatrix and the ISPRI platform ([EpiVax](https://epivax.com)) | Commercial T-cell epitope mapping and in-silico deimmunisation | Vendor; the site refuses automated fetches (HTTP 403), and terms and pricing were not verified |
| BioPhi (OASis) | Humanness against natural repertoires | See section 1 |

**Limit.** Epitope predictions correlate only weakly with clinical anti-drug antibody responses and a high humanness score does not guarantee low immunogenicity (antibody-sequence-bioinformatics `liabilities.md`). Use them to rank risk, not to clear a molecule.

## 8. Databases and benchmarks

The sequence and structure databases (SAbDab and SAbDab-nano, OAS, PLAbDab, Thera-SAbDab) and the measured-data sets (SKEMPI 2.0, AB-Bind, AbDb, CoV-AbDab, AbBiBench, Proteinbase) are listed once, with links, in antibody-literature-search `references/resources.md`.

## What was checked, changed or left out

- **PLIP:** the overview listed it for interface analysis; its papers describe a protein–ligand profiler (2021: DNA and RNA). Moved to a note.
- **ISPRI:** exists as an EpiVax platform; its expanded name varies between sources and no official product page was fetchable, so it is named without expansion.
- **AbDiffuser:** the paper exists; no official code repository could be confirmed.
- **Chai-2:** a preprint exists; availability was not verified.
- **AbBiBench:** real, but a preprint; it is in `resources.md` flagged as such.
- **DeepSP:** named by its paper's own title.
- **ClusPro:** the current host is `cluspro.bu.edu`.
- **Solubis:** the server was down when checked; the paper resolves.
- The overview's "fast and accurate" and similar descriptions of individual tools are the tools' own claims and were not independently tested here.
