# adapted from: https://stackoverflow.com/questions/14182879/regex-to-match-latex-equations

# original regex code with comments
# (?:        # start non-capture group for all possible match starts
#   # group 1, match dollar signs only 
#   # single or double dollar sign enforced by look-arounds
#   ((?<!\$)\${1,2}(?!\$))
# )
# # if group 1 was start
# (?(1)
#   # non greedy match everything in between
#   # group 1 matches do not support recursion
#   (.*?)
#   # match ending double or single dollar signs
#   (?<!\$)\1(?!\$)  
# )

import re
import sys
import os

def latex_convert(file_path):
    # open existing README file
    with open(file_path) as infile:
        content = infile.read()
        
        # replace all latex equations with the latex.codecogs implementation
        # for markdown using regex.
        # example: $|s\rangle$ ---> <img src="https://latex.codecogs.com/svg.latex?|s\rangle">,
        # where some of the parts of the link were left out for readability
        content_new = re.sub('(?:((?<!\$)\${1,2}(?!\$)))(?(1)(.*?)(?<!\$)\\1(?!\$))',
            '<img align=center src=\"https://latex.codecogs.com/svg.latex?\\\\small\\\\pagecolor{white}\\2\">',
            content)
        
        # replace all *N* or *a* or *x* with the latex.codecogs implementation
        # for markdown using regex.
        # example: *N* ---> <img src="https://latex.codecogs.com/svg.latex?N">
        content_new = re.sub('\*([a-zA-Z]){1,10}\*',
            '<img align=center src=\"https://latex.codecogs.com/svg.latex?\\\\small\\\\pagecolor{white}\\1\">',
            content_new)

    # seperate filename from extension
    file_name = os.path.basename(file_path).split('.') 
    
    file_folder = os.path.dirname(file_path)

    # write out file in a renamed copy
    if len(file_folder) != 0:
        file_path_new = file_folder + '/' + file_name[0] + "_LATEX." + file_name[1]
    else:
        file_path_new = file_name[0] + "_LATEX." + file_name[1]
    with open(file_path_new, "w+") as outfile:
        outfile.write(content_new)

if __name__ == "__main__":
    file_path = sys.argv[1]
    latex_convert(file_path)
