import sys
from PyPDF2 import PdfFileReader



def scan_pdf(filename):
    reader = PdfFileReader(filename)
    # PyPDF2.utils.PdfReadError: File has not been decrypted
    if reader.isEncrypted:
        reader.decrypt('')
    page = reader.getNumPages()
    return page

def ab_number(n):
    result = chr(ord('a') - 1 + (n%26 if n%26 else 26))
    while(n//26):
        n = n//26
        result = chr(ord('a') - 1 + (n % 26 if n % 26 else 26)) + result
    return result


def write_tex(filename,page):
    head = ['% !TEX program = xelatex\n',
    '\\documentclass[11pt,a4paper]{article}\n',
    '\\usepackage{geometry}\n',
    '\\usepackage{fontspec}\n',
    '\\usepackage{underscore}\n',
    '\\usepackage{hyperref}\n',
    '\\usepackage{mathtools}\n',
    '\\usepackage{pdfpages}\n',
    ' \n',
    '\\setmainfont{Cambria}\n',
    '\\geometry{letterpaper,scale=0.95}\n',
    '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% \n']
    tex_name = 'note_'+filename[0:-3]+'tex'
    tex = open(tex_name, 'w')
    tex.writelines(head)
    tex.flush()
    for i in range(page):
        index = str(i+1)
        index_aa = str(ab_number(i+1))
        textbox = ['\\newcommand{\\Cues'+index_aa+'}{ \n',
        '\tTake down cues for page'+index+'\n',
        '} \n',
        '\\newcommand{\\Summary'+index_aa+'}{ \n',
        '\tTake down summary for page '+index+' \n',
        '} \n',
        '%%%%%%%%%%%%% \n']
        tex.writelines(textbox)
        tex.flush
    tex.write('\\begin{document} \n')
    for i in range(page):
        index = str(i+1)
        index_aa = str(ab_number(i+1))
        minipage = ['\t\\newpage \n',
        '\t\\begin{minipage}[t][500pt]{0.2\\linewidth} \n',
        '\t\t \\paragraph{Cues:} \n',
        '\t\t \\Cues'+index_aa+'\n',
        '\t\\end{minipage} \n',
        '\t\\hfill \n',
        '\t\\begin{minipage}[t][500pt]{0.65\\linewidth} \n',
        '\t\t\\includepdf[pages={'+index+'},width=0.8\\linewidth]{'+filename+'} \n',
        '\t\\end{minipage} \n',
        '\t\\vfill \n',
        '\t\\rule{0.95\\linewidth}{0.05em} \n',
        '\n',
        '\t\\begin{minipage}[t][150pt]{\\linewidth}\n',
        '\t\t\\paragraph{Summary:} \n',
        '\t\\Summary'+index_aa+' \n',
        '\t\\end{minipage} \n']
        tex.writelines(minipage)
        tex.flush
    tex.write('\\end{document}')
    tex.close()
    print(tex_name+' has been generated')


if __name__ == "__main__":
    filename = sys.argv[1]
    page = scan_pdf(filename)
    write_tex(filename, page)