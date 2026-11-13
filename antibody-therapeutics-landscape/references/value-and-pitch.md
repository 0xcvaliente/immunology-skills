# Value, user fit and path to value

How to say who a computational antibody-design result is for and what would make it worth something. Written for the two product criteria of a design hackathon ("user fit" and "path to value"), and equally useful for a job interview at a biotech or an AI-for-drug-discovery company. Items marked **(guide)** come from the AI × Antibodies participant guide, retrieved 2026-11-13; the rest is general reasoning to be checked against the case.

## The two questions

- **User fit:** what is this design (or this method) for, and who needs it?
- **Path to value:** what is a credible route from what exists today to real use, for the molecule or for the method?

Both want specifics. "Pharma" is not a user. "The scientist running lead optimization on a program about to enter safety studies" is **(guide)**.

## Who buys, and what they buy

Buyers are pharma discovery groups, biotech platform companies and contract research organisations. They do not buy models. They buy decisions they can defend internally: which 20 molecules to make next, which programme to stop, which problem to fix before a safety study **(guide)**.

## Where the value sits

Sequences are cheap. Value is in avoided waste: fewer wet-lab rounds, and fewer late failures **(guide)**. A table to adapt, with no figures because costs and durations vary by company and target:

| Stage | What a design tool can do there | Why being right is worth something |
|---|---|---|
| Target and epitope selection | Epitope and liability assessment before committing | A wrong target or site wastes the whole programme; rarely addressed |
| Hit discovery | Generate and rank candidates | A crowded space, so differentiation is hard |
| Lead optimisation | Predict which mutations help without breaking anything | The long, expensive grind |
| Developability screening | Flag aggregation, immunogenicity and liabilities early | Late failures are the costly ones |
| Manufacturing and formulation | Expression and formulation prediction | Under-served |

One wet-lab round (expressing and testing a panel of variants) takes weeks, so a tool that removes a round sells time, not software **(guide, reasoning)**. Put your own numbers in, with their source.

## What makes and kills a sale

- **Kills it:** a tool that cannot say how confident it is, needs a PhD to run, does not fit the existing workflow, or was validated only on retrospective public data **(guide)**.
- **Makes it:** prospective validation, even tiny. Ten designs made and measured beat a thousand scored on a computer **(guide)**.

## What is defensible

Structure prediction and binder generation are now widely available as largely open tools, so "we can predict structures" is something a competitor can run in an afternoon. What is not a commodity: the data, the judgment layer (which designs and why), the validation record, and the workflow a scientist actually uses **(guide)**. Say which of these you have, and which you would build next.

## Five questions to answer in a pitch

1. Who specifically is the user?
2. What does the problem cost them today, in money or months?
3. Why does your approach beat what they do now, which may be a spreadsheet and an experienced colleague's intuition?
4. What would you have to prove next, and what would proving it cost?
5. What is defensible in a year: data, workflows and validation records, rather than model architecture **(guide)**.

## From a clinical problem to an editable property

Almost every property clinicians see in an antibody drug traces to something an engineer can edit **(guide)**:

| What clinicians see | Why | What engineers change |
|---|---|---|
| Infusion reactions, or a drug that stops working over months | The body makes antibodies against the drug (immunogenicity) | Make the sequence look more human |
| Dosing every few weeks | IgG is recycled, so a standard one lasts about three weeks | Engineer the Fc for longer half-life |
| A bare nanobody works for hours, not weeks | At 15 kDa the kidneys filter it | Attach an Fc or an albumin binder, or use the short action on purpose |
| An infusion chair instead of a pen | Concentrated protein clumps or turns viscous | Improve solubility |
| Side effects in healthy tissue | The target is also on healthy cells | Tune affinity, or pick another epitope |
| Different patients respond differently | Targets and receptors vary between people | Choose epitope and format with that variation in mind |
| Cold chain and short shelf life | A fragile molecule | Make it sturdier |

**Tighter binding is not automatically better.** In solid tumours a very tight binder can stay at the first target it meets at a vessel wall and never reach the tissue behind it; for T-cell engagers, too tight can trigger dangerous cytokine release. Affinity is a design decision, not a maximum **(guide)**.

## Nanobodies in a pitch

For: reach hidden or recessed targets, tolerate harsh conditions, cheap microbial production, modular formats that join several binders in one molecule. Against: fast kidney clearance, so half-life extension is usually part of the product **(guide)**. Format choice is a pharmacokinetics decision before it is a binding one.

## Sizing claims

Market-size estimates vary widely between analyst reports, and the participant guide itself says to verify any figure before quoting it. Quote a number only with its source and date, say which segment it covers (all antibodies, not nanobodies), and prefer a bottom-up estimate you can defend (users times decisions times what a decision is worth) to a headline total. Where to look for sourced figures: the Antibody Society's tables and its yearly "Antibodies to watch" review, company annual reports for specific products, and the regulators' databases for approvals. All of these are volatile; see the main skill's rule.
