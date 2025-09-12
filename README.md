# CSV2Substack

Small Python CLI that converts a CSV file into LaTeX `array` markup suitable for embedding tables in Substack posts.

Usage

- `python main.py` prompts for the CSV filename.
- `python main.py --tk` opens a GUI file picker (Tkinter).
- `python main.py <filename>` uses the provided path.
- Options:
  - `--header` bold the header row
  - `--first-column` bold the first column
  - `--grid` add cell grid lines
  - `--italic` italicize non-bold cells
  - `--align left|center|right` column alignment (or `l|c|r`)
  - `-o, --output <file>` write output to a file instead of stdout

Examples

- `python main.py data.csv --header --grid --align left -o table.tex`
- `python main.py --tk --first-column --italic`

Notes

- Output is printed to stdout by default; redirect or use `-o` to save to a file.
- Special LaTeX characters in cells are escaped automatically.

Development

- Create a virtualenv: `python3 -m venv .venv && source .venv/bin/activate`
- Run help: `python main.py --help`
- Tests (if you have pytest installed): `pytest -q`


