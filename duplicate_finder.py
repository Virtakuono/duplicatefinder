#!/usr/bin/python

# A script to find duplicate files
# in a directory
# juho.happola@iki.fi

# I bet there are a gazillion implementations of this already
# floating around, most of which more elegant and fast than mine.

# Thanks for the remarks on bad programming style to Liam Mencel.

import os,sys,hashlib,time


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
    print('(or, more often in practice, duplicate_finder.py [rootdir] > [logfile])')
    print('(or, in shorter form, duplicate_finder.py [rootdir] | grep -v \"inspecting file\" > [logfile])')
    print('Defaulting rootdir to ./')
    rootdir =  './'

paths = []

times = [time.time()]

print('Listing files in %s ...'%(rootdir,))
for root, dirs, files in os.walk(rootdir, topdown=False):
    for name in files:
        paths.append(os.path.join(root,name))

times.append(time.time())
print('Listing done in %d seconds'%(times[-1]-times[-2]))

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

times.append(time.time())
print('Digest comparison done in %d seconds'%(times[-1]-times[-2]))
print('Overall runtime %d seconds'%(times[-1]-times[0]))
print('Quitting.\nHave a nice day!')


