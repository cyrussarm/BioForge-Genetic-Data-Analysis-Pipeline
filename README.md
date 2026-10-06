# BioForge

BioForge is a Python-based bioinformatics project developed as a team project
during the Python Mini Camp at Quera College.

The project reads DNA sequences from a FASTA file, analyzes their possible
reading frames, detects Open Reading Frames (ORFs), translates them into
proteins, and provides filtering options for the detected results.

The project also keeps incomplete ORFs instead of discarding them and records
the main execution steps and errors using a logging system.

---

## Features

BioForge provides the following features:

- Reading DNA sequences from FASTA files
- Validating DNA sequences
- Handling FASTA format errors
- Generating the Complement strand
- Generating the Reverse Complement strand
- Finding all 6 Reading Frames
- Detecting Open Reading Frames (ORFs)
- Detecting both complete and incomplete ORFs
- Keeping incomplete ORFs in the results
- Translating codons into amino acid sequences
- Calculating protein molecular weight
- Detecting motifs in protein sequences
- Filtering results based on:
  - Protein length
  - Molecular weight
  - Motifs
- Assigning unique IDs to detected ORFs
- Logging important steps, warnings, and errors
- Saving the final results in a report file
- Using custom exceptions for error handling
- Providing a command-line interface for running the program

---

## Project Workflow

The general workflow of BioForge is:

```text
FASTA Input
     |
     v
FASTA Validation
     |
     v
DNA Sequence Validation
     |
     v
Complement & Reverse Complement
     |
     v
6 Reading Frames
     |
     v
ORF Detection
     |
     +------------------+
     |                  |
     v                  v
Complete ORFs     Incomplete ORFs
     |                  |
     +--------+---------+
              |
              v
      Codon Translation
              |
              v
      Protein Generation
              |
              v
          Filtering
        /      |       \
       /       |        \
 Length   Molecular     Motif
          Weight
              |
              v
          Annotation
              |
              v
           Report

Main Components
fileLoaders/

Responsible for loading input and biological data files.

inputLoader.py reads and validates FASTA input.
dataLoader.py loads codon and amino acid weight data.
models/

Contains the main biological objects used by the project.

Sequence represents a DNA sequence and provides sequence-related
operations.
ORF represents a detected Open Reading Frame.
Protein represents a translated protein and stores its molecular weight
and detected motifs.
Annotate assigns unique IDs to detected ORFs.
BioForgeExceptions.py contains custom exceptions.
utils/

Contains the main processing operations.

ORF_detector.py detects ORFs.
translator.py translates codons into amino acids.
filtering.py provides different filtering classes.
writeReport.py generates the final report.
logger.py

Provides logging functionality for recording program execution, warnings,
and errors.

main.py

Provides the command-line interface and coordinates the complete processing
pipeline.

Technologies

The project was developed using:

Python 3.13
Object-Oriented Programming (OOP)
Regular Expressions (Regex)
Python Logging
argparse
pathlib
Git
GitHub
Python Standard Library

The project does not require external Python packages for its main
functionality.

Requirements
Python 3.13 or compatible Python 3.x version
A FASTA input file
The required data files:
data/codon_table.txt
data/amino_weights.txt
Running the Project

BioForge is executed from the command line using main.py.

Run the command from the project root directory.

Basic Usage
python main.py --input <input_fasta> --out <output_directory> --min-length <minimum_protein_length>

The output directory is created automatically if it does not already exist.

| Argument       | Required | Description                                          |
| -------------- | -------- | ---------------------------------------------------- |
| `--input`      | Yes      | Path to the input FASTA file                         |
| `--out`        | Yes      | Path to the output directory                         |
| `--min-length` | Yes      | Minimum protein length                               |
| `--min-weight` | No       | Minimum molecular weight                             |
| `--max-weight` | No       | Maximum molecular weight                             |
| `--motif`      | No       | Motif to search for; can be specified multiple times |

Filtering

BioForge supports three types of filtering.

Protein Length

The minimum protein length is required when running the program.

Example:
python main.py --input input/input.fasta --out output --min-length 50

Only proteins satisfying the specified minimum length are kept after
filtering.

Molecular Weight

A minimum molecular weight can be specified:
python main.py --input input/input.fasta --out output --min-length 50 --min-weight 5000

A maximum molecular weight can also be specified:
python main.py --input input/input.fasta --out output --min-length 50 --max-weight 20000

Motif

A motif can be provided using the --motif option:
python main.py --input input/input.fasta --out output --min-length 50 --motif GHG

Input Format

The input file must be in FASTA format.

Example:
>sequence_1 Example sequence
ATGAAACCCGGGTAG

>sequence_2 Another sequence
ATGAAACCCGGG

Design Decisions

The following design decisions were made during the development of BioForge.

1. Representing Biological Concepts with Separate Classes
Decision

Biological concepts such as DNA sequences, ORFs, and proteins were represented
using separate classes:

Sequence
ORF
Protein
Reason

Each object has its own properties and responsibilities.

For example, the Sequence class handles sequence-related operations such as
validation, complement generation, reverse complement generation, and GC
content calculation.

The ORF class stores information specific to an ORF, while the Protein
class handles protein-related information such as amino acid sequence,
molecular weight, and motifs.

This separation makes the code easier to understand and maintain.

2. Separating ORF Detection from Sequence and ORF Objects Decision

The ORF detection process was implemented separately in:

utils/ORF_detector.py

instead of putting the complete ORF detection algorithm inside the Sequence
or ORF classes.

Reason

The Sequence and ORF classes are mainly responsible for representing
biological data, while the detection process is an algorithm that operates on
that data.

Separating the detection algorithm keeps the model classes simpler and makes
the detection logic easier to modify or test independently.

3. Using Separate Filter Classes
Decision

Different filtering conditions were implemented as separate classes:

LengthFilter
WeightFilter
MotifFilter

and applied through a common filtering process.

Reason

Protein length, molecular weight, and motif are different filtering criteria.
Keeping them as separate classes makes it possible to combine different
filters without putting all filtering conditions into one large function.

For example, the user can use only length filtering or combine length,
molecular weight, and motif filtering.

This design also makes adding another filter in the future easier.

4. Using Custom Exceptions and Logging
Decision

BioForge uses custom exceptions derived from BioForgeError, including:

FastaFormatError
InvalidSequenceError
DataFileError
FilteringError

The project also uses a logging system to record execution information,
warnings, and errors.

Reason

Different problems can occur during processing, such as invalid DNA
sequences, incorrect FASTA input, or missing data files.

Custom exceptions make these errors easier to distinguish and handle.

Logging was also chosen instead of relying only on print() statements because
the execution history can be stored in a log file and reviewed after the
program finishes.

5. Using a Command-Line Interface
Decision

The program uses Python's argparse module to receive input and filtering
parameters from the command line.

Reason

A command-line interface allows the same program to be executed with different
input files and filtering conditions without changing the source code.

Error Handling

BioForge uses custom exception handling to manage errors during execution.

Examples include:

Missing or invalid input files
Empty input files
Invalid DNA sequences
FASTA format problems
Invalid or missing data files
Filtering-related errors

Errors related to individual records can be handled without necessarily
stopping the processing of all other records.

Unexpected errors are also logged and propagated so that they are not silently
ignored.

Team Members

This project was developed as a team project during the Python Mini Camp at
Quera College.

سیروس
عارفه
رضا
مبینا
کمیل

Project Goal

The main goal of BioForge is to apply Python programming concepts such as
Object-Oriented Programming, file handling, regular expressions, exception
handling, logging, and modular software design to a practical bioinformatics
problem.

