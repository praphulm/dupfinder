# File comparison code

import hashlib
import shelve
import glob
import argparse
from pathlib import Path
import os
import shutil

# Function to compute the hash value of a file
def file_hash (file_path):
    hasher = hashlib.sha1()
    with open(file_path, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
        str = hasher.hexdigest()
    afile.close
    return str

def main():
    # parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i","--input", required = True, help = "path to source location of images")
    ap.add_argument("-s", "--shelve", required = True, help = "output shelve database")
    ap.add_argument("-e", "--extension", required = True, help = "extension of files to find duplicates")
    ap.add_argument("-m", "--move", required = False, help = "path to move duplicate files to")

    args = vars(ap.parse_args())
    print (args)
    
    # loop over the files in the directory including sub-directories
    p = Path(args["input"])

    if os.path.isdir(p.__str__()):
        files = list(p.rglob(args["extension"]))
        # open the shelve database
        db = shelve.open(args["shelve"], writeback = True, flag='n')
        for filePath in files:
            h = file_hash (filePath)
            # extract the filename from the path and update the database
            # using the hash as the key and the filename append to the
            # list of values   
            db[h] = db.get(h, []) + [filePath]
        
        # close the shelf database
        db.close()
    else:
        print ("Invalid source path:", p.__str__())
        return

    # Search for duplicate file
    m = args["move"]

    if m.__sizeof__() > 0:
     # open the shelve database
        db = shelve.open(args["shelve"])
    
        for entry in db:
            pw = db.get(entry)
            sz = len(pw)
            # print (pw[0],end='\t')
            item = 1
            while item < sz:
                print (pw[item]," *")
                shutil.move(str(pw[item]),str(m))
                item = item + 1
                print()
   
        # close the shelve database
        db.close()


if __name__ == "__main__":
    main()   