from tkinter import Tk
from tkinter.filedialog import askopenfilename
import csv

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
    return file_path

filename = get_file_path()

do_header = input('Bold header? (y/n): ')
do_first = input('Bold first column? (y/n): ')
do_grid = input('Cell Grid (y/n): ')
do_italic = input('Italicize non-bold cells? (y/n): ')
do_align = input('Align left, center (default), right (l/c/r): ')


tex = ''
with open(filename, 'r') as file:
    reader = csv.reader(file)
    for rnum, row in enumerate(reader):
        if rnum == 0:
            tex += "\\begin{array}{"
            for i in range(len(row)):
                if do_grid == 'y':
                    tex += '|'
                if do_align == 'l':
                    tex += 'l'
                elif do_align == 'r':
                    tex += 'r'
                else:
                    tex += 'c'
            if do_grid == 'y':
                tex += '|'
            tex += '}\n'
            if do_grid == 'y':
                tex += '\\hline'
            tex += '\n'

        if rnum == 0 and do_header == 'y':
            for col in row:
                tex += f'\\textbf{{{col}}} & '
        else:
            for i,col in enumerate(row):
                if i == 0 and do_first == 'y':
                    tex += f'\\textbf{{{col}}} & '
                else:
                    if do_italic == 'y':
                        col = f'\\textit{{{col}}}'
                    else:
                        col = f'\\mbox{{{col}}}'
                    tex += f'{col} & '
        tex = tex[:-2] + '\\\\ \n'
        if do_grid == 'y':
            tex += '\\hline\n'

tex += '\\end{array}\n'
print()
print(tex)
