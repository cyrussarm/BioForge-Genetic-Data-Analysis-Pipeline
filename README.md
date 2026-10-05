# BioForge

**A Comprehensive Genetic Data Analysis Pipeline**

BioForge is a command-line pipeline for analyzing DNA sequences from FASTA files. It detects Open Reading Frames (ORFs) across all six reading frames, translates them into proteins, filters the results based on user-defined criteria, annotates them with unique IDs, and produces a structured report.

This project was developed as the mini-project for the **Quera Python Alpha Bootcamp – 13th Series**.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Command-Line Arguments](#command-line-arguments)
- [Input Format](#input-format)
- [Output Files](#output-files)
- [Pipeline Overview](#pipeline-overview)
- [Design Decisions (OOP)](#design-decisions-oop)
- [Edge Cases and Behaviors](#edge-cases-and-behaviors)
- [Error Handling](#error-handling)
- [Logging](#logging)
- [Examples](#examples)

---

## Features

- **FASTA parsing** with validation and duplicate-ID detection
- **DNA sequence validation** (only `A`, `C`, `G`, `T` allowed)
- **Sequence operations**: complement, reverse complement, DNA → RNA, GC content
- **ORF detection** in all 6 reading frames (3 forward + 3 reverse)
- **Complete and incomplete ORF** reporting (`is_complete` flag)
- **Translation** of codons to amino acids using an external codon table
- **Molecular weight calculation** using monoisotopic residue masses
- **Motif detection** inside translated proteins with position tracking
- **Three independent filters**: `LengthFilter`, `WeightFilter`, `MotifFilter`
- **Automatic annotation** with IDs of the form `BFG_001`, `BFG_002`, …
- **Structured reporting** to `output/report.txt`
- **Full logging** to `output/bioforge.log` (append mode)
- **Custom exception hierarchy** for precise error handling

---

## Project Structure
BioForge/
├── data/
│ ├── codon_table.txt # CODON AMINO_ACID table
│ └── amino_weights.txt # ONE_LETTER_CODE RESIDUE_MASS table
├── input/
│ └── input.fasta # Example / test input
├── fileLoaders/
│ ├── dataLoader.py # Loads codon table & amino weights
│ └── inputLoader.py # FASTA parser + validation
├── models/
│ ├── sequence.py # Sequence class
│ ├── ORF.py # ORF class
│ ├── protein.py # Protein class
│ ├── annotation.py # Annotate class (ID generation)
│ └── BioForgeExceptions.py # Custom exceptions
├── utils/
│ ├── ORF_detector.py # ORF detection across 6 frames
│ ├── translator.py # Codon → amino acid translation
│ ├── filtering.py # Filter classes + apply_filters
│ └── writeReport.py # Report writer
├── output/
│ ├── report.txt # Generated report (created at runtime)
│ └── bioforge.log # Log file (append mode)
├── logger.py # Logging setup
├── main.py # CLI entry point
└── README.md


---

## Requirements

- **Python 3.10+**
- No external dependencies — uses only the Python standard library:
  - `argparse`, `os`, `re`, `abc`, `logging`, `pathlib`

---

## Installation

```bash
git clone <repository-url>
cd BioForge

Usage
```bash
python main.py --input <FASTA_FILE> --out <OUTPUT_DIR> --min-length <N> [OPTIONS]

Required arguments:

Argument	Description
--input	Path to the input FASTA file
--out	Path to the output directory
--min-length	Minimum protein length (in amino acids)
Optional arguments:

Argument	Description
--min-weight	Minimum molecular weight (Da)
--max-weight	Maximum molecular weight (Da)
--motif	Motif to require in proteins (can be repeated)
Command-Line Arguments
--input (required)
Path to the FASTA file to analyze.

--out (required)
Directory where report.txt and bioforge.log will be written. Created automatically if it does not exist.

--min-length (required)
Minimum protein length in amino acids. Applied via LengthFilter.

--min-weight (optional)
Minimum molecular weight in Daltons. When given, a WeightFilter is added to the pipeline.

--max-weight (optional)
Maximum molecular weight in Daltons. Can be combined with --min-weight.

--motif (optional, repeatable)
An amino-acid motif to search for in translated proteins. Can be passed multiple times:

bash
--motif MK --motif TAG
Each motif creates a separate MotifFilter instance.

Input Format
BioForge accepts standard FASTA files with one or more records:

text
>seq001 organism=E_coli sample=A
ATGCTTTTCATAG

>seq002 organism=Human sample=B
CCCATGGGGTAA
Rules:

Each record starts with a header line beginning with >.

The first token after > is the sequence ID.

Everything after the ID on the header line is the description.

Sequence lines contain only A, C, G, T (case-insensitive).

Blank lines and lines starting with # are ignored.

A header without a following sequence raises FastaFormatError.

A sequence before the first header raises FastaFormatError.

An empty input file raises FastaFormatError.

Output Files
output/report.txt
A human-readable report grouped by input sequence. For each sequence:

ID, description, sequence, complement, reverse complement, GC content

Number of ORFs (total / complete / incomplete)

For each ORF:

is_complete status

Codons

Auto-generated ID (BFG_XXX)

Strand (forward / reverse)

Frame (0 / 1 / 2)

Start position (1-based, relative to the original DNA strand)

Protein sequence, molecular weight, length

Detected motifs with their positions

output/bioforge.log
A log file written in append mode. Contains:

Application start / stop events

Data file loading status

FASTA record loading summary

ORF detection counts per sequence

Filter activation messages

Warnings (duplicate IDs, division-by-zero in GC content)

Errors with full traceback for unexpected exceptions

Format:

Pipeline Overview

FASTA Input
    ↓
Parsing (inputLoader)
    ↓
Validation (Sequence.validate)
    ↓
ORF Detection (6 frames)
    ↓
Translation (translator)
    ↓
Motif Detection (Protein.motif_detector)
    ↓
Filtering (LengthFilter → WeightFilter → MotifFilter)
    ↓
Annotation (BFG_XXX IDs)
    ↓
Reporting (write_report)
    ↓
Logging (bioforge.log)
Design Decisions (OOP)
This project uses Object-Oriented Programming where it adds clarity. Below are the key design decisions.

Classes
Class	Responsibility
Sequence	Encapsulates a DNA sequence and its behaviors: validation, complement, reverse complement, DNA → RNA, GC content
ORF	Holds ORF data: codons, strand, frame, start position, completeness, associated protein
Protein	Holds the amino acid sequence, molecular weight, and detected motifs
Filter (ABC)	Abstract interface for all filters
LengthFilter, WeightFilter, MotifFilter	Concrete filter implementations
Annotate	Generates unique IDs (BFG_001, BFG_002, …)
BioForgeError + subclasses	Unified exception hierarchy
Functions
Function	Why a function and not a class
data_loader	Stateless — reads two files and returns two dicts
input_loader	Stateless — parses a file and returns a list of records
ORF_detection	Pure algorithm with no persistent state
translator	Pure transformation from codons to amino acids
write_report	Stateless I/O
apply_filters	Chains filters without needing any state
Inheritance
Exception hierarchy: BioForgeError → FastaFormatError, InvalidSequenceError, DataFileError, FilteringError

Filter hierarchy: Filter (ABC) → LengthFilter, WeightFilter, MotifFilter

Polymorphism
All concrete filters implement Filter.apply(orfs). The apply_filters function calls filter_.apply(result) without knowing the concrete filter type. Adding a new filter only requires subclassing Filter — no changes to apply_filters.

Composition
Sequence has a list of ORF objects (seq.orfs)

ORF has a Protein object (orf.protein)

Protein has a list of motifs (protein.motifs)

Design Decisions (Rationale)
Filters implement a common ABC. This lets apply_filters treat all filters uniformly and makes adding new filter types trivial (Open/Closed Principle).

Incomplete ORFs are kept, not dropped. The project specification requires reporting both complete and incomplete ORFs, with an is_complete flag. Dropping them would lose information.

Reverse-strand start_pos is converted to forward-strand coordinates. The report must express positions relative to the original DNA strand, regardless of the strand on which the ORF was found.

Codon table and amino weights are loaded from external files. The specification explicitly forbids hardcoding this data; it must be read from data/.

Only --min-length is required by the CLI. The specification lists exactly three required arguments. --min-weight, --max-weight, and --motif are added as optional extensions that activate additional filters only when provided.

WeightFilter and MotifFilter are activated conditionally. If no weight or motif is given, the corresponding filter is not constructed. This keeps the pipeline lean and matches the "optional filter" design.

exc_info=True is used when logging unexpected exceptions. Full tracebacks are essential for debugging bugs that slip past the domain-specific BioForgeError handlers.

ORF detection runs in 6 frames separately. Both strands and all three frames per strand must be scanned — this is the standard bioinformatics approach and is required by the specification.

