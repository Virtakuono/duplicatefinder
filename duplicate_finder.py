#!/usr/bin/python

# A script to find duplicate files
# in a directory
# juho.happola@iki.fi

# I bet there are a gazillion implementations of this already
# floating around, most of which more elegant and fast than mine.

# Thanks for the remarks on bad programming style to Liam Mencel.

import os,sys,hashlib


def hashfile(afile, blocksize=65536):
    hasher = hashlib.sha256()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()

try:
    rootdir = sys.argv[1]
except IndexError:
    print('Usage: duplicate_finder.py <rootdir>')
    print('Defaulting rootdir to ./')
    rootdir =  './'

paths = []

print('Scanning files in %s ...'%(rootdir,))
for root, dirs, files in os.walk(rootdir, topdown=False):
    for name in files:
        paths.append(os.path.join(root,name))

hashes = {}

print('%d files found in total , computing sha256 digests to find duplicates...'%(len(paths)))

for ind in range(0,len(paths)):
    path = paths[ind]
    print('inspecting file %d/%d ...'%(ind,len(paths)))
    try:
        hash = hashfile(open(path, 'rb')) 
    except IOError:
        print('   could not compute digest for %s'%(path,))
    try:
        print('   %s is a duplicate of\n      %s'%(path,hashes[hash]))
    except KeyError:
        hashes[hash] = path

print('Quitting.\nHave a nice day!')


