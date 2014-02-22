#!/usr/bin/python

# A script to find duplicate files
# in a directory
# juho.happola@iki.fi

# I bet there are a gazillion implementations of this already
# floating around, most of which more elegant and fast than mine.


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

import os
for root, dirs, files in os.walk(rootdir, topdown=False):
    for name in files:
        paths.append(os.path.join(root,name))

hashes = []

errfiles = []

for path in paths:
    try:
        hashes += [hashfile(open(path, 'rb')) ]
        print('sha256 digest for %s:\n\t%s'%(path,hashes[-1]))
    except IOError:
        print('could not compute digest for %s'%(path,))
        paths.remove(path)
        errfiles.append(path)

for ind in range(0,len(hashes)):
    hash = hashes[ind]
    path = paths[ind]
    duplicateCount = hashes.count(hash)-1
    if not duplicateCount:
        print('file %s has %d duplicates:'%(path,duplicateCount))
        for ind2 in range(ind+1,len(hashes)):
            if hashes[ind2] == hash:
                print('\t%s'%(paths[ind2],))

print('The following files could not be inspected for whatever reason')
for errfile in errfiles:
    print('\t%s'%(errfile,))

print('Have a nice day.')


