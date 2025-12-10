#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Jordi Sevilla Fortuny
# Script to launch the snakemake workflow BDPP

import os
import sys
from argparse import ArgumentParser
from sys import argv
from shutil import which

# Version
__version__ = "1.0.0"

# Parse command line arguments
def parse_args():
    parser = ArgumentParser(description="Run the BDPP snakemake workflow.")
    parser.add_argument(
        "-c", "--cores", type=int, default=4, help="Number of cores to use for the workflow"
    )
    parser.add_argument(
        "-g", "--genes_dir",
        type=str,
        required=False,
        help="Directory containing the gene alignments to process",
        default=None
    )

    parser.add_argument(
        "-a", "--assemblies_dir",
        type=str,
        required=False,
        help="Directory containing the assemblies to process. Only if no genes_dir is provided.",
        default=None
    )

    parser.add_argument(
        "-p", "--prefix",
        type=str,
        default="fixcore_job",
        help="Prefix for the output files"
    )

    parser.add_argument(
        "-o", "--outdir",
        type=str,
        default="bdpp_output", 
        help="Output directory for the results"
    )

    parser.add_argument(
        "-t", "--pangenome-tool",
        type=str,
        required=False,
        help="Pangenome analysis tool to use. Only if no assemblies_dir is provided.",
        default="none",
        choices=["none", "roary", "panaroo", "panacota"]
    )

    parser.add_argument(
        "-th", "--threshold",
        type=float,
        required=False,
        help="Threshold percentage for core gene definition. Only if pangenome-tool is not 'none'.",
        default=0.9
    )

    parser.add_argument(
        "-d", "--use-apptainer",
        required=False,
        help="Whether to use Apptainer containers for the workflow.",
        default=False,
        action="store_true" 
    )


    return parser.parse_args()

def check_arguments(args):
    if args.genes_dir is None and args.assemblies_dir is None:
        print("Error: You must provide either a genes directory or an assemblies directory.")
        sys.exit(1)
    if args.genes_dir is not None and args.assemblies_dir is not None:
        print("Error: You cannot provide both a genes directory and an assemblies directory.")
        sys.exit(1)
    if args.assemblies_dir is not None and args.pangenome_tool == "none":
        print("Error: You must specify a pangenome tool when providing assemblies.")
        sys.exit(1)
    if args.pangenome_tool != "none" and (args.threshold < 0 or args.threshold > 1):
        print("Error: Threshold must be between 0 and 1.")
        sys.exit(1)
    
    return args.assemblies_dir is not None

def check_tools(apptainer=False):
    # Check that snakemake is instaled and with the correct version
    if which("snakemake") is None:
        print("Error: Snakemake is not installed or not found in PATH.")
        sys.exit(1)
    import snakemake

    if snakemake.__version__ != "8.20.5":
        print(f"Error: Snakemake version 8.20.5 is required, but version {snakemake.__version__} is installed.")
        sys.exit(1)
   
    # Check that apptainer/singularity is installed if needed
    if apptainer:
        if which("apptainer") is None or which("singularity") is None:
            print("Error: Apptainer/Singularity is not installed or not found in PATH.")
            sys.exit(1)
        
def check_files(path, extension=".fasta"):
    if not os.path.isdir(path):
        print(f"Error: Directory '{path}' does not exist.")
        sys.exit(1)
    files = [f for f in os.listdir(path) if f.endswith(extension)]
    if len(files) == 0:
        print(f"Error: No files with extension '{extension}' found in directory '{path}'.")
        sys.exit(1)

def main():
    args = parse_args()

    print(" _____ _       ____               \n|  ___(_)_  __/ ___|___  _ __ ___ \n| |_  | \\ \\/ / |   / _ \\| '__/ _ \\\n|  _| | |>  <| |__| (_) | | |  __/\n|_|   |_/_/\\_\\\\____\\___/|_|  \\___|\n                                  \n")
    print(f"Pipeline to fix pangenome based alignments (version {__version__})\n")

    print("checking input arguments...\n")
    assemblies = check_arguments(args)

    print("checking required tools...\n")
    check_tools(apptainer=args.use_apptainer)

    # Check that there are files in the provided directories
    if assemblies:
        check_files(args.assemblies_dir, extension=".fasta")
    else:
        check_files(args.genes_dir, extension=".fasta")
    

    # Ges script directory to run snakemake from there
    script_dir = os.path.dirname(os.path.abspath(argv[0]))

    # Construct the snakemake command
    # Software managment flag
    software_flag = "--sdm apptainer" if args.use_apptainer else "--use-conda --conda-frontend conda"

    if assemblies:
        cmd = f"cd {script_dir} && " + " ".join([
            "snakemake",
            "--cores", str(args.cores),
            "--config",
            f"GENOMES_DIR={os.path.abspath(args.assemblies_dir)}",
            f"OUTDIR={os.path.abspath(args.outdir)}",
            f"PREFIX={args.prefix}",
            "CORE='{TOOL : %s, THRESHOLD: %s}'" % (args.pangenome_tool, args.threshold),
            software_flag,
            " -q rules"
        ])
    else:
        cmd = f"cd {script_dir} && " + " ".join([
            "snakemake",
            "--cores", str(args.cores),
            "--config",
            f"GENES_DIR={os.path.abspath(args.genes_dir)}",
            f"OUTDIR={os.path.abspath(args.outdir)}",
            f"PREFIX={args.prefix}",
            software_flag,
            " -q rules"
        ])
        

    # Execute the command
    
    print(f"Launching workflow with the following command:\n{cmd}\n")
    os.system(cmd)


if __name__ == "__main__":
    main()
    sys.exit(0)
