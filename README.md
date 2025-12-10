# FixCore

[![Snakemake](https://img.shields.io/badge/Snakemake-≥8.20-brightgreen.svg?style=flat)](https://snakemake.readthedocs.io)
![Test workflow](https://github.com/NerisGarcia/fixcore/actions/workflows/test.yaml/badge.svg)
[![License (AGPL version 3)](https://img.shields.io/badge/license-GNU%20AGPL%20version%203-green.svg)](COPYING)

FixCore is a Snakemake workflow for producing high-quality core-genome alignments and phylogenies from pangenome analyses. It can either derive core genes from assemblies using PanACoTA, Roary, or Panaroo, or start from precomputed core-family FASTA files. Each core gene is aligned, trimmed, and curated to remove poorly aligned regions. Curated gene alignments are then concatenated to build a robust species-level alignment and a maximum-likelihood tree.

The pipeline includes the FixCore algorithm for curating core gene alignments. This algorithm uses the nucleotide and amino-acid alignments together with per-gene phylogenies to detect and remove problematic sequences.

------------------------------------------------------------------------

## Workflow overview

-   Input: assemblies or core-family FASTA files.
-   Optional core-genome extraction: PanACoTA, Roary, or Panaroo. Family thresholds are configurable in `config/config.yaml`. Defaults: PanACoTA 80% identity, Roary 95%, Panaroo 70%.
-   Multiple sequence alignment (MAFFT) per core gene.
-   Trimming (TrimAl) and curation using the FixCore algorithm.
-   Concatenation of curated gene alignments.
-   Maximum-likelihood phylogeny from the concatenated alignment with IQ-TREE 2 (GTR+G, 1000 bootstraps).

## Prerequisites

-   Linux/macOS (tested on Linux).
-   Conda (Miniconda or Mambaforge) recommended for environment management.
-   Snakemake ≥ 8.20.5. If unavailable, install following the [official guide](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html).

    ```bash
    conda create -n snakemake -c conda-forge -c bioconda snakemake=8.20.5
    conda activate snakemake
    ```

## Installation

Clone the repository or download a zip release:

```         
git clone https://github.com/NerisGarcia/fixcore.git
cd fixcore
```

## Quick start

1.  Edit `config/target.yaml` to set input data.
    -   Option A (precomputed core families): directory containing multi-FASTA files per gene family (`.fasta`).
    -   Option B (assemblies): directory with genome assemblies (`.fasta`), and set `core_tool` to `panacota`, `roary`, or `panaroo` in `config/config.yaml`.
2.  Adjust parameters in `config/config.yaml` as needed.
3.  Run the workflow:

    ```bash
    snakemake --use-conda -c 8
    ```

    We recommend at least 8 threads, but any positive integer is valid.

## Configuration and parameter selection

Alternatively, you can use the provided Docker container to run the workflow. First, make sure you have [apptainer](https://apptainer.org/) or [Singularity](https://sylabs.io/singularity/) installed. Then, you can run the workflow using the following command:

```
snakemake --sdm apptainer -c 8  
```

## Configuration
Workflow parameters can be changed in the configuration files:

-   `config/config.yaml`: global settings, including `core_tool` selection and parameters for pangenome, alignment, trimming, curation, and phylogeny.
-   `config/target.yaml`: input paths for genomes or core-family FASTA files and output directories.

See inline comments in these files for parameter descriptions.

## Outputs

-   Concatenated curated alignment of core genes.
-   Maximum-likelihood phylogeny for the concatenated alignment.
-   Intermediate files (per-gene alignments, trimmed and curated versions) to support downstream analyses.

## Troubleshooting

-   Ensure `--use-conda` is used so all environments defined under `workflow/envs/` are created automatically.
-   If a rule fails, re-run with increased verbosity:
    -   `snakemake -c 8 --use-conda -p --printshellcmds`
-   Verify file extensions (`.fasta`) and directory paths in `config/target.yaml`.

## Contributing

Contributions are welcome! To contribute:

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature-name`).
3.  Commit your changes (`git commit -m 'Add new feature'`).
4.  Push to the branch (`git push origin feature-name`).
5.  Open a Pull Request.

## Citation

If you use FixCore in your research, please cite this repository. A formal citation will be added upon publication.

## License

FixCore is licensed under the **GNU AGPL v3**. See the [LICENSE](LICENSE) file for details.

## Contact
For issues or questions, open an [issue](https://github.com/NerisGarcia/fixcore/issues) on GitHub.


## Contributors

[![Contributors figure](https://contrib.rocks/image?repo=NerisGarcia/fixcore)](https://github.com/NerisGarcia/fixcore/graphs/contributors)
