#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Jordi Sevilla Fortuny
# Script to launch the snakemake workflow FIXCORE

import os
import sys
from argparse import ArgumentParser
from sys import argv
from shutil import which
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich_argparse import RichHelpFormatter


console = Console()

# Version
__version__ = "1.0.0"


# Parse command line arguments
def parse_args():
    parser = ArgumentParser(
        description="Run the FIXCORE snakemake workflow.",
        formatter_class=RichHelpFormatter,
    )
    parser.add_argument(
        "-c",
        "--cores",
        type=int,
        default=4,
        help="Number of cores to use for the workflow",
    )
    parser.add_argument(
        "-g",
        "--genes_dir",
        type=str,
        required=False,
        help="Directory containing the gene alignments to process",
        default=None,
    )

    parser.add_argument(
        "-a",
        "--assemblies_dir",
        type=str,
        required=False,
        help="Directory containing the assemblies to process. Only if no genes_dir is provided.",
        default=None,
    )

    parser.add_argument(
        "-p",
        "--prefix",
        type=str,
        default="fixcore_job",
        help="Prefix for the output files",
    )

    parser.add_argument(
        "-o",
        "--outdir",
        type=str,
        default="bdpp_output",
        help="Output directory for the results",
    )

    parser.add_argument(
        "-t",
        "--pangenome-tool",
        type=str,
        required=False,
        help="Pangenome analysis tool to use. Only if no assemblies_dir is provided.",
        default="none",
        choices=["none", "roary", "panaroo", "panacota"],
    )

    parser.add_argument(
        "-th",
        "--threshold",
        type=float,
        required=False,
        help="Threshold percentage for core gene definition. Only if pangenome-tool is not 'none'.",
        default=0.9,
    )

    parser.add_argument(
        "-d",
        "--use-apptainer",
        required=False,
        help="Whether to use Apptainer containers for the workflow.",
        default=False,
        action="store_true",
    )

    return parser.parse_args()


def check_arguments(args):
    if args.genes_dir is None and args.assemblies_dir is None:
        console.print(
            "[bold red]Error ❌: You must provide either a genes directory or an assemblies directory.[/bold red]"
        )
        sys.exit(1)
    if args.genes_dir is not None and args.assemblies_dir is not None:
        console.print(
            "[bold red]Error ❌: You cannot provide both a genes directory and an assemblies directory.[/bold red]"
        )
        sys.exit(1)
    if args.assemblies_dir is not None and args.pangenome_tool == "none":
        console.print(
            "[bold red]Error ❌ : You must specify a pangenome tool when providing assemblies.[/bold red]"
        )
        sys.exit(1)
    if args.pangenome_tool != "none" and (args.threshold < 0 or args.threshold > 1):
        console.print(
            "[bold red]Error ❌: Threshold must be between 0 and 1.[/bold red]"
        )
        sys.exit(1)

    return args.assemblies_dir is not None


def check_tools(apptainer=False):
    # Check that snakemake is instaled and with the correct version
    if which("snakemake") is None:
        console.print(
            "[bold red]Error ❌: Snakemake is not installed or not found in PATH.[/bold red]"
        )
        sys.exit(1)
    else:
        console.print(
            "[bold green]Snakemake found ✔[/bold green]"
        )
    import snakemake

    if snakemake.__version__ != "8.20.5":
        console.print(
            f"[bold red]Error ❌: Snakemake version 8.20.5 is required, but version {snakemake.__version__} is installed.[/bold red]"
        )
        sys.exit(1)
    else:
        console.print(
            "[bold green]Snakemake version is correct ✔[/bold green]"
        )


    # Check that apptainer/singularity is installed if needed
    if apptainer:
        if which("apptainer") is None or which("singularity") is None:
            console.print(
                "[bold red]Error ❌: Apptainer/Singularity is not installed or not found in PATH.[/bold red]"
            )
            sys.exit(1)
        return "--sdm apptainer"
    else:
        # Check mamba or conda is installed
        if which("mamba") is None and which("conda") is None:
            console.print(
                "[bold red]Error ❌: Mamba or Conda is not installed or not found in PATH.[/bold red]"
            )
            sys.exit(1)
        elif which("mamba") is not None:
            console.print(
                "[bold green]Mamba found ✔[/bold green]"
            )
            return "--use-conda"
        elif which("conda") is not None:
            console.print(
                "[bold yellow]Warning ⚠: Mamba not found, using Conda instead.[/bold yellow]"
            )
            return "--use-conda --conda-frontend conda"


def check_files(path, extension=".fasta"):
    if not os.path.isdir(path):
        console.print(
            f"[bold red]Error ❌: Directory '{path}' does not exist.[/bold red]"
        )
        sys.exit(1)
    files = [f for f in os.listdir(path) if f.endswith(extension)]
    if len(files) == 0:
        console.print(
            f"[bold red]Error ❌: No files with extension '{extension}' found in directory '{path}'.[/bold red]"
        )
        sys.exit(1)


def main():
    args = parse_args()

    console.print(
        Panel.fit(
            " _____ _       ____               \n|  ___(_)_  __/ ___|___  _ __ ___ \n| |_  | \\ \\/ / |   / _ \\| '__/ _ \\\n|  _| | |>  <| |__| (_) | | |  __/\n|_|   |_/_/\\_\\\\____\\___/|_|  \\___|\n                                  \n",
            style="bold purple",
        )
    )
    console.print(f"[bold green]FixCore Runner v{__version__}[/bold green]\n")

    # Check arguments
    assemblies = check_arguments(args)

    # Check required tools
    software_flag = check_tools(apptainer=args.use_apptainer)
    console.print("[bold green]The required tools are installed ✔[/bold green]\n")

    # Check that there are files in the provided directories
    if assemblies:
        check_files(args.assemblies_dir, extension=".fasta")
    else:
        check_files(args.genes_dir, extension=".fasta")
    console.print("[bold green]Input files found ✔[/bold green]\n")

    # Ges script directory to run snakemake from there
    script_dir = os.path.dirname(os.path.abspath(argv[0]))

    # Construct the snakemake command
    # Software managment flag
     
    if assemblies:
        cmd = f"cd {script_dir} && " + " ".join(
            [
                "snakemake",
                "--cores",
                str(args.cores),
                "--config",
                "\\\n",
                f"GENOMES_DIR={os.path.abspath(args.assemblies_dir)}",
                "\\\n",
                f"OUTDIR={os.path.abspath(args.outdir)}",
                "\\\n",
                f"PREFIX={args.prefix}",
                "\\\n",
                "CORE='{TOOL : %s, THRESHOLD: %s}'"
                % (args.pangenome_tool, args.threshold),
                "\\\n",
                software_flag,
                " -q rules",
            ]
        )
    else:
        cmd = f"cd {script_dir} && " + " ".join(
            [
                "snakemake",
                "--cores",
                str(args.cores),
                "--config",
                "\\\n",
                f"GENES_DIR={os.path.abspath(args.genes_dir)}",
                "\\\n",
                f"OUTDIR={os.path.abspath(args.outdir)}",
                "\\\n",
                f"PREFIX={args.prefix}",
                "\\\n",
                software_flag,
                " -q rules",
            ]
        )

    # Execute the command

    console.print(f"Launching workflow with the following command:\n{cmd}\n")
    # run the command and catch the return code
    return_code = os.system(cmd)
    if return_code != 0:
        console.print(
            f"[bold red]Error ❌: Workflow failed with return code {return_code}.[/bold red]"
        )
        sys.exit(1)
    else:
        console.print("\n[bold green]Workflow completed ✔[/bold green]")


if __name__ == "__main__":
    main()
    sys.exit(0)
