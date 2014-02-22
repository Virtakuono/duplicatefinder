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
hashedpaths = []

import os
for root, dirs, files in os.walk(rootdir, topdown=False):
    for name in files:
        paths.append(os.path.join(root,name))

hashes = []
errfiles = []
duplicatehashes = []


print('Computing sha256 digest for %d files'%(len(paths)))



for ind in range(0,len(paths)):
    path = paths[ind]
    try:
        hashes.append(hashfile(open(path, 'rb')) )
        hashedpaths.append(path)
        print('sha256 digest for file %d/%d %s:\n\t%s'%(ind,len(paths),path,hashes[-1]))
    except IOError:
        print('could not compute digest for %s'%(path,))
        errfiles.append(path)

print('Digests done. Finding duplicates.')

for ind in range(0,len(hashes)):
    hash = hashes[ind]
    path = hashedpaths[ind]
    duplicateCount = hashes.count(hash)-1
    if duplicateCount and (hash not in duplicatehashes):
        duplicatehashes.append(hash)
        print('file %d/%d:  %s has %d duplicate(s):'%(ind,len(hashes),path,duplicateCount))
        for ind2 in range(ind+1,len(hashes)):
            if hashes[ind2] == hash:
                print('\t%s'%(hashedpaths[ind2],))

print('The following files could not be inspected for whatever reason')
for errfile in errfiles:
    print('\t%s'%(errfile,))

print('Have a nice day.')


