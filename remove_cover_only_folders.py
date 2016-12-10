import getopt
import glob
import os
import re
import sys


HELPCMD = '''\
remove_cover_only_folders.py -f <root_dir_path>
'''

def is_empty_like_folder(folder):

    path = os.path.join(folder,'')
    file_list = my_glob(path+'*')

    for f_ in file_list:
        f = os.path.basename(f_)
        if f not in ('@eaDir','.DS_Store','folder.jpg','cover.jpg'):
            return False
    return True

def remove_empty_folders(folder):
    path = os.path.join(folder,'')
    folders = sorted([val for val in my_glob(path+'*') if not os.path.isfile(val) and not ignore_folder(val)])

    for fold in folders:
        remove_empty_folders(fold)

    if is_empty_like_folder(path):
        remove_folder(path)


def ignore_folder(folder):
    filename = os.path.basename(folder)
    if filename[0]== '.':
        return True
    elif filename.startswith('@eaDir'):
        return True

    return False

def remove_folder(path):
    path = os.path.join(path,'')
    if not path.count('/')>=4:
        print "COWARDLY REFUSED TO REMOVE",path
        return
    os.system("rm -rf "+path)
    print "Removed 'empty like' folder:",path

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

def main(argv):

    root_dir = None

    try:
        opts, args = getopt.getopt(argv, "f:", [])
    except getopt.GetoptError as err:
        print HELPCMD
        sys.exit(-1)

    for opt, arg in opts:
        if opt=="-f":
            root_dir = arg

    if not all([root_dir]):
        print "Error : mandatory argument missing..."
        print HELPCMD
        sys.exit(-1)

    # validating command line arguments
    root_dir = os.path.join(root_dir, '')
    if not os.path.exists(root_dir):
        print "Error: the given directory does not exist :", root_dir
        sys.exit(-1)

    remove_empty_folders(root_dir)

if __name__ == '__main__':
    main(sys.argv[1:])