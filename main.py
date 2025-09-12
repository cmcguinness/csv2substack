from tkinter import Tk
from tkinter.filedialog import askopenfilename
import argparse
import csv
import sys
import os

# Prompt the user to select a file and return its path.
def get_file_path():
    root = Tk()
    root.withdraw()  # Hide the Tkinter root window
    root.title("CSV To Make Into Substack Compatible Tex Table")  # Set the title of the file dialog window
    file_path = askopenfilename(
        title="CSV To Make Into Substack Compatible Tex Table",
        filetypes=[("CSV Files", "*.csv"),
                   ("All Files", "*.*")]
    )
    root.destroy()  # Destroy the hidden root window after use
    
    if not file_path:  # User cancelled the dialog
        print("File selection cancelled.")
        sys.exit(0)
    
    return file_path


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Convert CSV files to LaTeX arrays for Substack posts',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py data.csv                    # Interactive mode
  python main.py --tk                        # GUI file selection
  python main.py data.csv --header --grid   # Bold header with grid
  python main.py data.csv -o output.tex     # Save to file
  python main.py data.csv --align left      # Left-aligned columns
        '''
    )
    
    parser.add_argument('filename', nargs='?', 
                        help='CSV file to process (use --tk for GUI selection)')
    
    parser.add_argument('--tk', action='store_true',
                        help='Use GUI file dialog to select file')
    
    parser.add_argument('--header', action='store_true',
                        help='Make header row bold')
    
    parser.add_argument('--first-column', action='store_true',
                        help='Make first column bold')
    
    parser.add_argument('--grid', action='store_true',
                        help='Add cell grid lines')
    
    parser.add_argument('--italic', action='store_true',
                        help='Italicize non-bold cells')
    
    parser.add_argument('--align', choices=['left', 'center', 'right', 'l', 'c', 'r'],
                        default='center',
                        help='Column alignment (default: center)')
    
    parser.add_argument('-o', '--output',
                        help='Output file (default: stdout)')
    
    return parser.parse_args()


def get_user_preferences():
    """Get user preferences for LaTeX formatting options."""
    preferences = {}
    
    do_header = input('Bold header? (y/n): ').lower().strip()
    preferences['header'] = do_header in ['y', 'yes']

    do_first = input('Bold first column? (y/n): ').lower().strip()
    preferences['first_column'] = do_first in ['y', 'yes']

    do_grid = input('Cell Grid (y/n): ').lower().strip()
    preferences['grid'] = do_grid in ['y', 'yes']

    do_italic = input('Italicize non-bold cells? (y/n): ').lower().strip()
    preferences['italic'] = do_italic in ['y', 'yes']

    do_align = input('Align left, center (default), right (l/c/r): ').lower().strip()
    if do_align in ['l', 'left']:
        preferences['align'] = 'l'
    elif do_align in ['r', 'right']:
        preferences['align'] = 'r'
    else:
        preferences['align'] = 'c'
    
    return preferences


def args_to_preferences(args):
    """Convert command-line arguments to preferences dictionary."""
    preferences = {}
    preferences['header'] = args.header
    preferences['first_column'] = args.first_column
    preferences['grid'] = args.grid
    preferences['italic'] = args.italic
    
    # Convert alignment to single character
    if args.align in ['left', 'l']:
        preferences['align'] = 'l'
    elif args.align in ['right', 'r']:
        preferences['align'] = 'r'
    else:
        preferences['align'] = 'c'
    
    return preferences


def escape_latex_chars(text):
    """Escape special LaTeX characters in text."""
    if not isinstance(text, str):
        text = str(text)
    
    # Order matters - backslash must be first to avoid double-escaping
    text = text.strip()
    text = text.replace('\\', '\\textbackslash{}')
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    text = text.replace('$', '\\$')
    text = text.replace('&', '\\&')
    text = text.replace('%', '\\%')
    text = text.replace('#', '\\#')
    text = text.replace('^', '\\textasciicircum{}')
    text = text.replace('_', '\\_')
    text = text.replace('~', '\\textasciitilde{}')
    
    return text


def generate_latex_table(filename, preferences):
    """Generate LaTeX table from CSV file with given preferences."""
    tex = ''
    
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for rnum, row in enumerate(reader):
                if rnum == 0:
                    # Build array column specification
                    tex += "\\begin{array}{"
                    for i in range(len(row)):
                        if preferences['grid']:
                            tex += '|'
                        tex += preferences['align']
                    if preferences['grid']:
                        tex += '|'
                    tex += '}\n'
                    if preferences['grid']:
                        tex += '\\hline'
                    tex += '\n'

                # Process row content
                if rnum == 0 and preferences['header']:
                    for col in row:
                        col = escape_latex_chars(col)
                        tex += f'\\textbf{{{col}}} & '
                else:
                    for i, col in enumerate(row):
                        col = escape_latex_chars(col)
                        if i == 0 and preferences['first_column']:
                            tex += f'\\textbf{{{col}}} & '
                        else:
                            if preferences['italic']:
                                col = f'\\textit{{{col}}}'
                            else:
                                col = f'\\mbox{{{col}}}'
                            tex += f'{col} & '
                
                tex = tex[:-2] + '\\\\ \n'
                if preferences['grid']:
                    tex += '\\hline\n'

        tex += '\\end{array}\n'
        return tex

    except FileNotFoundError:
        print(f"Error: Could not open file '{filename}'.")
        sys.exit(1)
    except csv.Error as e:
        print(f"Error parsing CSV file: {e}")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Error: File '{filename}' contains invalid characters. Please ensure it's a valid text file.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


def write_output(latex_output, output_file=None):
    """Write LaTeX output to file or stdout."""
    if output_file:
        try:
            with open(output_file, 'w') as f:
                f.write(latex_output)
            print(f"Output written to {output_file}")
        except IOError as e:
            print(f"Error writing to file '{output_file}': {e}")
            sys.exit(1)
    else:
        print()
        print(latex_output)


def get_filename():
    """Get filename from command line argument, GUI dialog, or user input."""
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if filename == '--tk':
            filename = get_file_path()
    else:
        filename = input('Name of CSV file: ')
    
    # Clean up quotes (from copy pathname commands)
    if filename.startswith("'") and filename.endswith("'"):
        filename = filename[1:-1]
    elif filename.startswith('"') and filename.endswith('"'):
        filename = filename[1:-1]
    
    return filename


def validate_file(filename):
    """Validate that the file exists and is readable."""
    if not filename or not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    
    if not os.path.isfile(filename):
        print(f"Error: '{filename}' is not a file.")
        sys.exit(1)


def main():
    """Main program function."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Get filename
    if args.tk:
        filename = get_file_path()
    elif args.filename:
        filename = args.filename
        # Clean up quotes (from copy pathname commands)
        if filename.startswith("'") and filename.endswith("'"):
            filename = filename[1:-1]
        elif filename.startswith('"') and filename.endswith('"'):
            filename = filename[1:-1]
    else:
        filename = input('Name of CSV file: ')
        # Clean up quotes from interactive input too
        if filename.startswith("'") and filename.endswith("'"):
            filename = filename[1:-1]
        elif filename.startswith('"') and filename.endswith('"'):
            filename = filename[1:-1]
    
    # Validate file
    validate_file(filename)
    
    # Get preferences - either from command line or interactive
    if any([args.header, args.first_column, args.grid, args.italic, args.align != 'center']):
        # Use command-line preferences
        preferences = args_to_preferences(args)
    else:
        # Fall back to interactive mode if no preferences specified
        preferences = get_user_preferences()
    
    # Generate LaTeX output
    latex_output = generate_latex_table(filename, preferences)
    
    # Write output
    write_output(latex_output, args.output)


if __name__ == '__main__':
    main()
