import argparse
import io
import csv
from pathlib import Path

import main


def test_escape_latex_chars_all():
    text = r"\ { } $ & % # ^ _ ~"
    escaped = main.escape_latex_chars(text)
    # Check a few representative escapes
    assert "\\textbackslash{}" in escaped  # backslash
    assert "\\{" in escaped and "\\}" in escaped
    assert "\\$" in escaped and "\\&" in escaped and "\\%" in escaped and "\\#" in escaped
    assert "\\textasciicircum{}" in escaped and "\\_" in escaped and "\\textasciitilde{}" in escaped


def test_args_to_preferences_align_mapping():
    args = argparse.Namespace(
        header=False,
        first_column=True,
        grid=False,
        italic=True,
        align="left",
    )
    prefs = main.args_to_preferences(args)
    assert prefs["align"] == "l"
    assert prefs["first_column"] is True
    assert prefs["italic"] is True


def test_generate_latex_table_with_header_and_grid(tmp_path: Path):
    # Prepare a small CSV file
    csv_path = tmp_path / "sample.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["A", "B"])  # header
        w.writerow(["x", "y"])  # data row

    prefs = {
        "header": True,
        "first_column": True,
        "grid": True,
        "italic": False,
        "align": "c",
    }

    tex = main.generate_latex_table(str(csv_path), prefs)

    # Array spec should include grid and 2 centered columns
    assert "\\begin{array}{|c|c|}" in tex
    # Header should be bold
    assert "\\textbf{A}" in tex and "\\textbf{B}" in tex
    # First column of data row should be bold
    assert "\\textbf{x}" in tex
    # Grid line markers present
    assert "\\hline" in tex

