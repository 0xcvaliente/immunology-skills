# Reading an antibody paper

## Extraction template

Pull these fields from every paper that will support a claim. A missing field is itself a finding — report it as missing.

- **Target** — antigen, species, isoform or domain, and whether the construct was full-length, an ectodomain or a peptide.
- **Antibody** — clone or construct name, source (hybridoma, display, donor-derived), format and subclass, and whether the sequence is disclosed.
- **Binding** — affinity with the method and the geometry: which partner was immobilised, monovalent or bivalent analyte, buffer and temperature. A KD without its method is not comparable to another KD.
- **Epitope** — how it was mapped, and at what resolution: competition, mutagenesis, peptide scan, structure.
- **Function** — the assay, the readout, and whether the effect is blockade, agonism, killing or delivery.
- **Model system** — cell line, primary cells, animal model, or human; passage and source matter for cell lines.
- **Controls** — isotype control, irrelevant-target antibody, antigen-negative cells, genetic knockout, dose-response. Their absence caps how far the result travels.
- **Effect size and n** — the number itself, the replicate structure (biological versus technical), and the statistic.
- **Limitations the authors state** — usually the fastest route to the weak point.

## Evidence hierarchy

Strongest to weakest, and worth labelling explicitly in any summary:

1. Randomised controlled trial in humans, published with its registry record.
2. Single-arm or early-phase human data, published.
3. Peer-reviewed in vivo animal work with genetic and pharmacological controls.
4. Peer-reviewed in vitro work.
5. Preprint, awaiting review.
6. Conference abstract or poster — little method detail, frequently never published in full.
7. Company press release or investor deck — selected endpoints, no method.

Recency does not override this order. A 2026 press release is weaker evidence than a 2019 published trial.

## Red flags

- **Reagent not identified** — no clone, catalogue number or RRID, so the key reagent is unidentifiable and the work is not repeatable. Common in older immunohistochemistry and immunoblot literature.
- **No knockout or knockdown control** where specificity carries the claim.
- **A single antibody** supporting a localisation or expression claim; independent antibodies against different epitopes are what make it credible.
- **Blots cropped to single bands**, hiding the rest of the lane and any off-target reactivity.
- **Affinity compared across methods** or across different immobilisation geometries.
- **Avidity read as affinity** — a bivalent measurement quoted as monovalent KD.
- **Species mismatch** — reactivity shown in mouse, claim made for human.
- **Overexpression systems only**, where endogenous-level specificity was never tested.
- **Conclusions in the abstract** that the figures do not reach.

## Writing the summary

- Lead with what the evidence supports, not with what the authors hoped.
- Attach the identifier to each claim, so a reader can go check it.
- Separate "this was measured" from "the authors propose".
- Give conflicting findings room rather than picking the convenient one; where studies disagree, say what differs in their methods.
- Name the gaps. In antibody literature the recurring ones are specificity controls, species translation, and whether anything was tested at endogenous expression levels.
