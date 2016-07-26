#!/usr/bin/env python
#
import os
import os.path
import site

def showtree(root):
    l = len(root)
    for dirname,subdirs,filenames in os.walk(root):
        print dirname[l:]
        #print '\n\t%s'.join(subdirs)

def showdirs(root,chosen):
    for fname in os.listdir(root):
        dirname = os.path.join(root,fname)
        if not os.path.isdir(dirname):
            continue
        print fname
        for subdir in os.listdir( dirname):
            print '\t%s/%s' % (fname,subdir)

if __name__ == '__main__':
    firstSite = site.getsitepackages()[0]
    firstSite = '/usr/local/lib/python2.7/site-packages/pip-6.0.8-py2.7.egg/pip'
    showdirs(firstSite,['pip','setup','site'])
