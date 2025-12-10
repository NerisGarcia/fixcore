# FixCore

[![Snakemake](https://img.shields.io/badge/Snakemake-≥8.20-brightgreen.svg?style=flat)](https://snakemake.readthedocs.io)
![Test workflow](https://github.com/NerisGarcia/fixcore/actions/workflows/test.yaml/badge.svg)
 [![License (AGPL version 3)](https://img.shields.io/badge/license-GNU%20AGPL%20version%203-green.svg)](COPYING)

FixCore is a Snakemake workflow for producing high-quality core-genome alignments and phylogenies from pangenome analyses. It can either derive core genes from assemblies using PanACoTA, Roary, or Panaroo, or start from precomputed core-family FASTA files. Each core gene is aligned, trimmed, and curated to remove poorly aligned regions. Curated gene alignments are then concatenated to build a robust species-level alignment and a maximum-likelihood tree.

The pipeline includes the fixcore algorithm for curating core gene alignments. This algorithm is based on the gene and amino acid alignment and its phylogeny to detect and remove sequences with errors.

---


## Prerequisites
- Snakemake ≥ 8.20.5
- Conda (Miniconda or Mambaforge) recommended for environment management.
- Linux/macOS. Tested on Linux.
  
If Snakemake 8.20.5 is not available on your system, install it following the [official guide](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html).

With conda:

```
conda create -n snakemake -c conda-forge -c bioconda snakemake=8.20.5
conda activate snakemake
```
## Installation
You can download the repository as a zip or clone it:

```
git clone https://github.com/NerisGarcia/fixcore.git
cd FixCore
```


## Quick start
1. Edit the target configuration `config/target.yaml` to set input data.
   - Option A (precomputed core families): point to a directory containing multi-FASTA files for each gene family with the `.fasta` extension.
   - Option B (assemblies): point to a directory with genome assemblies (`.fasta`) and set `core_tool` to `panacota`, `roary`, or `panaroo` in `config/config.yaml`. The workflow will run the selected pangenome tool to derive core genes before curation.
2. Adjust parameters in `config/config.yaml` as needed.
3. Run the workflow:

```
snakemake --use-conda -c 8
```

We recommend at least 8 threads, but any positive integer is valid.

Alternatively, you can use the provided Docker container to run the workflow. First, make sure you have [apptainer](https://apptainer.org/) or [Singularity](https://sylabs.io/singularity/) installed. Then, you can run the workflow using the following command:

```
snakemake --sdm apptainer -c 8  
```

## Configuration
Workflow parameters can be changed in the configuration files:
- `config/config.yaml`: global settings, including `core_tool` selection and parameters for pangenome, alignment, trimming, and phylogeny.
- `config/target.yaml`: input paths for genomes or core-family FASTA files and output directories.


## Workflow overview
- Input: assemblies or core-family FASTA files.
- Core-genome extraction (optional): PanACoTA, Roary, or Panaroo.
- Multiple sequence alignment (MAFFT) per core gene.
- Trimming and curation using provided scripts.
- Concatenation of curated gene alignments.
- Maximum likelihood phylogeny from the concatenated alignment.

## Outputs
- Concatenated curated alignment of core genes.
- Maximum-likelihood phylogeny for the concatenated alignment.
- Intermediate files (per-gene alignments, trimmed and curated versions) to support downstream analyses.

## Troubleshooting
- Ensure `--use-conda` is used so all environments defined under `workflow/envs/` are created automatically.
- If a rule fails, re-run with increased verbosity:
  - `snakemake -c 8 --use-conda -p --printshellcmds`
- Check that file extensions (`.fasta`) and directory paths in `config/target.yaml` are correct.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a Pull Request.

## Citation
If you use FixCore in your research, please cite this repository. A formal citation will be added upon publication.

## License
FixCore is licensed under the **GNU AGPL v3**. See the [LICENSE](LICENSE) file for details.

## Contact
For issues or questions, open an [issue](https://github.com/NerisGarcia/fixcore/issues) on GitHub.


## Contributors

[![Contributors figure](https://contrib.rocks/image?repo=NerisGarcia/fixcore)](https://github.com/NerisGarcia/fixcore/graphs/contributors)
