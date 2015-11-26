from figure import Figure
import commands
import os
import re

def confirmAndMakeDir(path):
    dirname, basename = os.path.split(path)
    if not os.path.exists(dirname):
        commands.getoutput("mkdir -p %s" % dirname)

def main():
    pngfile_list = commands.getoutput('find images -name "*.png"').split('\n')

    for pngfile in pngfile_list:
        jsonfile = re.sub('^images', 'jsons', pngfile)
        testfile = re.sub('^images', 'tests', pngfile)
        try:
            confirmAndMakeDir(jsonfile)
            confirmAndMakeDir(testfile)

            figure = Figure(pngfile)
            figure.saveJSON(jsonfile)
            figure.saveTestPNG(testfile)
        except:
            print 'failed:', pngfile

main()


