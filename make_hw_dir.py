import os
import sys

NAME=""

def main(homework_num):
    dirname = "homework" + homework_num
    texFile = 'hw' + homework_num + '.tex'
    if makeDirectory(dirname):
        os.chdir(dirname)
        writeBuild()
        writeEdit(homework_num)
        writeTex(texFile)
        setupMercurial(texFile)

    else:
        print("could not build directory")

    return

def makeDirectory(dirname):
    try:
        os.chdir(dirname)
        return False# if it successfully opens the directory, do not make it!!!
    except:
        #since we can't open the directory, we assume it doesn't exist -- okay?
        os.mkdir(dirname)
        return True

def writeBuild():
    build = open('build', 'w')
    build.writelines("""#! /usr/bin/python
import os, sys

if __name__ == '__main__':
    if (len(sys.argv)) == 2:
        f = sys.argv[1]
        fminus = f.split('.tex')[0]
        fdvi = fminus + '.dvi'
        fps = fminus + '.ps'

        os.system('latex %s' % f)
        os.system('dvips -o %s %s' % (fps, fdvi))
""")
    build.close()
    os.system('chmod 777 build')

def writeEdit(homework_num):
    hw = "hw" + homework_num
    edit = open('edit', 'w')
    edit.writelines("""#! /usr/bin/python
import os, sys
import subprocess
import time

if __name__ == '__main__':
    while "stop" not in os.listdir(os.getcwd()):
        os.system('vim {0}.tex')
        os.system('hg commit -m "%s"' % str(time.time()))
        os.system('./build {1}.tex')
        subprocess.Popen(["evince", "{2}.ps"])
    os.system('rm stop')""".format(hw, hw, hw))
    edit.close()
    os.system('chmod 777 edit')

def writeTex(name):
    f = open(name, 'w')
    f.writelines("""\documentclass{article}
\usepackage{amssymb}
\usepackage[margin=1.2in]{geometry}
\\author %s
\\begin{document}
\\newcommand{\\tab}{\hspace*{2em}}
\\noindent %s\\
Insert Date
Insert Title

\section{}
\section{}
\section{}

\end{document}""" % (NAME, NAME))
    f.close()


def setupMercurial(filename):
    os.system("hg init")
    os.system("hg add %s" % filename)


if __name__ == "__main__":

    if len(sys.argv) == 2:
        filename = sys.argv[1]
        main(filename)
    else:
        print("Please supply a homework number")
        
