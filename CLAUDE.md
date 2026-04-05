# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A single-file interactive CLI tool (`csv_column_filter.py`) that filters CSV columns and rows. No dependencies beyond the Python standard library.

## Running

```bash
python csv_column_filter.py
```

The script is fully interactive — it prompts for input file path, columns to keep (by index or name), and an optional row filter.

## Architecture

Everything lives in `csv_column_filter.py`:

- `filter_csv(input_file, columns_to_keep, row_filter=None)` — core logic. Reads CSV with ISO-8859-1 encoding, writes `filtered_<filename>` in the same directory. `row_filter` is a tuple `(column_name, value, include_bool)`.
- `format_size(bytes_val)` — utility to format byte counts for display.
- `main()` — interactive prompts, calls `filter_csv`, prints a summary.

Output files are always written to the same directory as the input, prefixed with `filtered_`.
