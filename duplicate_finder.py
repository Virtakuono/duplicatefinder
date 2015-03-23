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
sizes = []

times = [time.time()]

print('Listing files in %s ...'%(rootdir,))
for root, dirs, files in os.walk(rootdir, topdown=False):
    for name in files:
        paths.append(os.path.join(root,name))
        sizes.append(os.path.getsize(os.path.join(root,name)))


times.append(time.time())
print('Listing done in %d seconds'%(times[-1]-times[-2]))

hashes = {}

print('%d files found in total , computing sha256 digests to find duplicates...'%(len(paths)))

wastedSpace = 0

for ind in range(0,len(paths)):
    path = paths[ind]
    print('inspecting file %d/%d ...'%(ind,len(paths)))
    try:
        hash = hashfile(open(path, 'rb'))
        fileSize = os.path.getsize(path)
    except IOError:
        print('   could not compute digest for %s'%(path,))
    try:
        print('   %s is a duplicate of\n      %s'%(path,hashes[hash]))
        wastedSpace += fileSize
        if fileSize > 1024:
            if fileSize > 1024**2:
                print('     size of duplicate: %d MB'%(fileSize/1024/1024))
            else:
                print('     size of duplicate: %d kB'%(fileSize/1024))
        else:
            print('     size of duplicate: %d bytes'%(fileSize))

    except KeyError:
        hashes[hash] = path

times.append(time.time())
print('Digest comparison done in %d seconds'%(times[-1]-times[-2]))
print('Overall runtime %d seconds'%(times[-1]-times[0]))
if wastedSpace>1024:
    if wastedSpace>1024**2:
        print('Overall %d MB wasted on duplicates'%(wastedSpace/1024/1024))
    else:
        print('Overall %d kB wasted on duplicates'%(wastedSpace/1024))
else:
    print('Overall %d bytes on duplicates'%(wastedSpace))

print('Quitting.\nHave a nice day!')


