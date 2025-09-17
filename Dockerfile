FROM --platform=linux/amd64 condaforge/mambaforge:latest
LABEL io.github.snakemake.containerized="true"
LABEL io.github.snakemake.conda_env_hash="52e47d8dcac8db88e7816b6cc0c68266344f29a3481780c69288f72b19bc7ddc"

# Step 1: Retrieve conda environments

# Conda environment:
#   source: workflow/envs/common.yaml
#   prefix: /conda-envs/3f7305c3b93f0f7b90ba4db67f9c5ad2
#   channels:
#     - bioconda
#     - conda-forge
#   dependencies:
#     - prokka=1.14.6
#     - parallel
RUN mkdir -p /conda-envs/3f7305c3b93f0f7b90ba4db67f9c5ad2
COPY workflow/envs/common.yaml /conda-envs/3f7305c3b93f0f7b90ba4db67f9c5ad2/environment.yaml

# Conda environment:
#   source: workflow/envs/panaroo.yaml
#   prefix: /conda-envs/ef6754e3ecb2223efa1a0aefb73628e9
#   channels:
#     - bioconda
#     - conda-forge
#     - anaconda
#   dependencies:
#     - python=3.9
#     - panaroo=1.5.1
#     - mkl=2023.2.0
RUN mkdir -p /conda-envs/ef6754e3ecb2223efa1a0aefb73628e9
COPY workflow/envs/panaroo.yaml /conda-envs/ef6754e3ecb2223efa1a0aefb73628e9/environment.yaml

# Conda environment:
#   source: workflow/envs/phylo.yaml
#   prefix: /conda-envs/587f409f4cc07e23a3fc4e1c8fb64b48
#   channels:
#     - conda-forge
#     - bioconda
#   dependencies:
#     - python>=3.5
#     - pip==24.2
#     - amas==1.0
#     - iqtree==2.3.6
#     - snp-sites==2.5.1
#     - snp-dists==0.8.2
RUN mkdir -p /conda-envs/587f409f4cc07e23a3fc4e1c8fb64b48
COPY workflow/envs/phylo.yaml /conda-envs/587f409f4cc07e23a3fc4e1c8fb64b48/environment.yaml

# Step 2: Generate conda environments

RUN mamba env create --prefix /conda-envs/3f7305c3b93f0f7b90ba4db67f9c5ad2 --file /conda-envs/3f7305c3b93f0f7b90ba4db67f9c5ad2/environment.yaml && \
    mamba env create --prefix /conda-envs/ef6754e3ecb2223efa1a0aefb73628e9 --file /conda-envs/ef6754e3ecb2223efa1a0aefb73628e9/environment.yaml && \
    mamba env create --prefix /conda-envs/587f409f4cc07e23a3fc4e1c8fb64b48 --file /conda-envs/587f409f4cc07e23a3fc4e1c8fb64b48/environment.yaml && \
    mamba clean --all -y
