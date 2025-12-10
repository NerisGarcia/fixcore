FROM condaforge/mambaforge:latest
LABEL io.github.snakemake.containerized="true"
LABEL io.github.snakemake.conda_env_hash="575ad2a65dd9c46edc778463477d596b521b59adfd34eeb7c00e45a68f8d523d"

# Step 1: Retrieve conda environments

# Conda environment:
#   source: workflow/envs/biopython.yaml
#   prefix: /conda-envs/e7f4bca48ccdc07a76d6302a609abfa3
#   channels:
#     - conda-forge
#     - bioconda
#   dependencies:
#     - python==3.10
#     - biopython==1.81
#     - pandas==2.0.3
#     - pip==23.2.1
RUN mkdir -p /conda-envs/e7f4bca48ccdc07a76d6302a609abfa3
COPY workflow/envs/biopython.yaml /conda-envs/e7f4bca48ccdc07a76d6302a609abfa3/environment.yaml

# Conda environment:
#   source: workflow/envs/common.yaml
#   prefix: /conda-envs/fd5fce429040c63b36c77f89965dc587
#   channels:
#     - bioconda
#     - conda-forge
#   dependencies:
#     - parallel
RUN mkdir -p /conda-envs/fd5fce429040c63b36c77f89965dc587
COPY workflow/envs/common.yaml /conda-envs/fd5fce429040c63b36c77f89965dc587/environment.yaml

# Conda environment:
#   source: workflow/envs/fasta.yaml
#   prefix: /conda-envs/7dc3548994c8f48f588b30e37a5c78cb
#   channels:
#     - auto
#     - bioconda
#   dependencies:
#     - seqkit==2.8.2
#     - snp-sites==2.5.1
RUN mkdir -p /conda-envs/7dc3548994c8f48f588b30e37a5c78cb
COPY workflow/envs/fasta.yaml /conda-envs/7dc3548994c8f48f588b30e37a5c78cb/environment.yaml

# Conda environment:
#   source: workflow/envs/mafft.yaml
#   prefix: /conda-envs/37ba28b62af34bce7001caa179d13112
#   channels:
#     - conda-forge
#     - bioconda
#   dependencies:
#    - mafft=7.526
RUN mkdir -p /conda-envs/37ba28b62af34bce7001caa179d13112
COPY workflow/envs/mafft.yaml /conda-envs/37ba28b62af34bce7001caa179d13112/environment.yaml

# Conda environment:
#   source: workflow/envs/panacota.yaml
#   prefix: /conda-envs/3780f2e188d3ebf1a5876817a2db7b10
#   channels:
#     - bioconda
#     - conda-forge
#   dependencies:
#     - panacota=1.3.1
#     - python=3.6
#     - python-dateutil=2.8.2
#     - python-utils=2.5.6
RUN mkdir -p /conda-envs/3780f2e188d3ebf1a5876817a2db7b10
COPY workflow/envs/panacota.yaml /conda-envs/3780f2e188d3ebf1a5876817a2db7b10/environment.yaml

# Conda environment:
#   source: workflow/envs/panaroo.yaml
#   prefix: /conda-envs/0fe716b8841b5aa370f1619ee05cf8c1
#   channels:
#     - bioconda
#     - conda-forge
#     - anaconda
#   dependencies:
#     - python=3.9
#     - panaroo=1.5.1
#     - mkl=2023.2.0
RUN mkdir -p /conda-envs/0fe716b8841b5aa370f1619ee05cf8c1
COPY workflow/envs/panaroo.yaml /conda-envs/0fe716b8841b5aa370f1619ee05cf8c1/environment.yaml

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

# Conda environment:
#   source: workflow/envs/prokka.yaml
#   prefix: /conda-envs/10abe7edd267172db16445de628c84f0
#   channels:
#     - bioconda
#     - conda-forge
#   dependencies:
#     - prokka=1.14.6
RUN mkdir -p /conda-envs/10abe7edd267172db16445de628c84f0
COPY workflow/envs/prokka.yaml /conda-envs/10abe7edd267172db16445de628c84f0/environment.yaml

# Conda environment:
#   source: workflow/envs/renv.yaml
#   prefix: /conda-envs/82dbff34e236ee8c16c4551365b88c8f
#   channels:
#     - conda-forge
#     - bioconda
#   dependencies:
#     - r-base=4.4.1
#     - r-tidyverse==2.0.0
#     - r-ape==5.8
#     - r-phangorn==2.12.1
#     - r-phylobase==0.8.12
#     - r-logger==0.3.0
RUN mkdir -p /conda-envs/82dbff34e236ee8c16c4551365b88c8f
COPY workflow/envs/renv.yaml /conda-envs/82dbff34e236ee8c16c4551365b88c8f/environment.yaml

# Conda environment:
#   source: workflow/envs/roary.yaml
#   prefix: /conda-envs/06530e6e687f659bdaa8f80230fdcfb7
#   channels:
#     - bioconda
#     - conda-forge
#     - r
#   dependencies:
#     - roary=3.13.0
RUN mkdir -p /conda-envs/06530e6e687f659bdaa8f80230fdcfb7
COPY workflow/envs/roary.yaml /conda-envs/06530e6e687f659bdaa8f80230fdcfb7/environment.yaml

# Conda environment:
#   source: workflow/envs/trimal.yaml
#   prefix: /conda-envs/d4a41624447e8ba622e6b2a5b79583ac
#   channels:
#     - conda-forge
#     - bioconda
#   dependencies:
#     - trimal=1.5.0
RUN mkdir -p /conda-envs/d4a41624447e8ba622e6b2a5b79583ac
COPY workflow/envs/trimal.yaml /conda-envs/d4a41624447e8ba622e6b2a5b79583ac/environment.yaml

# Step 2: Generate conda environments

RUN mamba env create --prefix /conda-envs/e7f4bca48ccdc07a76d6302a609abfa3 --file /conda-envs/e7f4bca48ccdc07a76d6302a609abfa3/environment.yaml && \
    mamba env create --prefix /conda-envs/fd5fce429040c63b36c77f89965dc587 --file /conda-envs/fd5fce429040c63b36c77f89965dc587/environment.yaml && \
    mamba env create --prefix /conda-envs/7dc3548994c8f48f588b30e37a5c78cb --file /conda-envs/7dc3548994c8f48f588b30e37a5c78cb/environment.yaml && \
    mamba env create --prefix /conda-envs/37ba28b62af34bce7001caa179d13112 --file /conda-envs/37ba28b62af34bce7001caa179d13112/environment.yaml && \
    mamba env create --prefix /conda-envs/3780f2e188d3ebf1a5876817a2db7b10 --file /conda-envs/3780f2e188d3ebf1a5876817a2db7b10/environment.yaml && \
    mamba env create --prefix /conda-envs/0fe716b8841b5aa370f1619ee05cf8c1 --file /conda-envs/0fe716b8841b5aa370f1619ee05cf8c1/environment.yaml && \
    mamba env create --prefix /conda-envs/587f409f4cc07e23a3fc4e1c8fb64b48 --file /conda-envs/587f409f4cc07e23a3fc4e1c8fb64b48/environment.yaml && \
    mamba env create --prefix /conda-envs/10abe7edd267172db16445de628c84f0 --file /conda-envs/10abe7edd267172db16445de628c84f0/environment.yaml && \
    mamba env create --prefix /conda-envs/82dbff34e236ee8c16c4551365b88c8f --file /conda-envs/82dbff34e236ee8c16c4551365b88c8f/environment.yaml && \
    mamba env create --prefix /conda-envs/06530e6e687f659bdaa8f80230fdcfb7 --file /conda-envs/06530e6e687f659bdaa8f80230fdcfb7/environment.yaml && \
    mamba env create --prefix /conda-envs/d4a41624447e8ba622e6b2a5b79583ac --file /conda-envs/d4a41624447e8ba622e6b2a5b79583ac/environment.yaml && \
    mamba clean --all -y
