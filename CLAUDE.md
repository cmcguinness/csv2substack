# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simple Python utility that converts CSV files into LaTeX arrays suitable for embedding in Substack posts. The project consists of a single main script (`main.py`) that handles file input, user preferences, and LaTeX output generation.

## Running the Application

The script can be executed in three different ways:

- `python main.py` - Interactive mode, prompts for CSV filename
- `python main.py --tk` - GUI mode, opens file dialog for file selection  
- `python main.py filename.csv` - Direct mode, uses specified filename

Output is written to stdout, so use shell redirection to save to a file.

## Code Architecture

The application is structured as a single-file script with:

- File input handling (command line args, GUI dialog, or interactive prompt)
- Quote cleanup for filenames
- Interactive configuration prompts for formatting options
- CSV parsing with LaTeX character escaping
- LaTeX array generation with configurable styling options

## Key Components

- **File Selection**: Supports multiple input methods including tkinter file dialog
- **Character Escaping**: Handles LaTeX special characters ($, %, _) in CSV content
- **Formatting Options**: Bold headers, bold first column, cell grids, italics, and alignment
- **LaTeX Generation**: Creates properly formatted LaTeX arrays for Substack compatibility

## Dependencies

The script uses only Python standard library modules:
- `tkinter` - For GUI file selection dialog
- `csv` - For CSV file parsing
- `sys` - For command line argument handling

No external dependencies or package management files are present.