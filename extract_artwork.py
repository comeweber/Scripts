# coding=utf-8
'''
Script that looks for album recursively to extract the cover image from mp3s
and places it inside the album directory as a folder.jpg file.
This is done for compatibility issues with some music library softwares like DSAudio.

Usage:

extract_artwork.py -f <pathname> [-r] [-F]

-f <pathname> : folder that should be inspected
-r : activate recursion (off by default)
-F : force 'folder.jpg' overwrite

Author : Côme Weber
'''

import getopt
import glob
import os
import re
import mutagen as mut
import sys

HELPCMD = '''\
extract_artwork.py -f <pathname> [-r] [-F]
-f <pathname> : folder that should be inspected
-r : activate recursion (off by default)
-F : force 'folder.jpg' overwrite
'''

FORCE = False

def main(argv):

    #Variable initialization
    root_dir=None
    do_recursion = False

    global FORCE

    try:
        opts, args = getopt.getopt(argv, "rf:F", [])
    except getopt.GetoptError as err:
        print HELPCMD
        sys.exit(-1)

    for opt, arg in opts:
        if opt=="-f":
            root_dir = arg
        if opt == '-r':
            do_recursion = True
        if opt == "-F":
            FORCE = True


    if not all([root_dir]):
        print 'Mandatory argument missing...'
        print HELPCMD
        exit(-1)

    #validating command line arguments
    root_dir =os.path.join(root_dir,'')
    if not os.path.exists(root_dir):
        print "Error: the given directory does not exist :",root_dir
        sys.exit(-1)

    print "Starting Extraction..."
    extract_image_in_folder(root_dir,do_recursion)
    print "Extraction finished"

def my_glob(path):
    """
    escapes square brackets [] in filenames not to be handled as special glob chars
    """
    # replace the left square bracket with [[]
    glob_pattern = re.sub(r'\[', '[[]', path)
    # replace the right square bracket with []] but be careful not to replace
    # the right square brackets in the left square bracket's 'escape' sequence.
    glob_pattern = re.sub(r'(?<!\[)\]', '[]]', glob_pattern)
    return glob.glob(glob_pattern)

def extract_image_in_folder(path,do_recursion=False,img_name='folder.jpg'):

    path = os.path.join(path,"")
    if FORCE or not os.path.exists(path+img_name):
        mp3_files = sorted(my_glob(path+"*.mp3"))
        if len(mp3_files) > 0:
            extract_image_from_mp3(mp3_files[0],path)
        elif do_recursion is False:
            print "Error: no MP3 found in ", path

    if do_recursion:
        folders = sorted([val for val in my_glob(path+'*') if not os.path.isfile(val) and not ignore_folder(val)])
        for folder in folders:
            extract_image_in_folder(folder,do_recursion)

def ignore_folder(folder):
    filename = os.path.basename(folder)
    if filename[0]== '.':
        return True
    elif filename.startswith('@eaDir'):
        return True

    return False


def extract_image_from_mp3(mp3_path,dest_folder,img_name='folder.jpg'):

    mp3_file = mut.File(mp3_path)
    artwork = None
    try:
        for tagname in mp3_file.tags.keys():
            if tagname.startswith("APIC:"):
                artwork = mp3_file.tags[tagname].data
                dest_folder = os.path.join(dest_folder,"")
                with open(dest_folder + img_name, 'wb') as img:
                    img.write(artwork)
                break
        if artwork is None:
            print "No image found in file:",mp3_path
        else:
            print "Image extracted from", os.path.dirname(mp3_path)

    except:
        print "An error occured with file during cover image extraction:",mp3_path


if __name__ == '__main__':
    main(sys.argv[1:])
