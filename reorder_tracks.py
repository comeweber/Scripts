# coding=utf-8
"""
Script that merges a multi-CD album into a one CD album (a concatenation of all the CDs)
	* Sets a common album name
	* Automatically updates the track indices 

Handles command line arguments (cf. usage). If an argument is not submitted,
the user will have to give it interactively

Usage:
	python reorder_tracks.py [-p </path/to/root/folder>] [-a <new_album_name>]

Author : Côme Weber
"""


from mutagen.easyid3 import EasyID3
import sys, os, glob, re
from shutil import copy,move

HELPCMD = "reorder_tracks.py [-p </path/to/root/folder>] [-a <new_album_name>]"

def main(args):

	album=root=None

	try:
        opts, args = getopt.getopt(args, "hp:a:", ["--path","--album_name","--help"])
    except getopt.GetoptError as err:
        print HELPCMD
        sys.exit(-1)

    for opt, arg in opts:
        if opt in ("-a","--album_name"):
           album=arg
        elif opt in ("-p",'--path'):
        	root=arg 
        elif opt in ('-h','--help'):
        	print HELPCMD
           
         
    if root is None:
		#Ask the user, the path of the root folder
		print "Path to folder containing \"CD1,...\" folders:",
		root = raw_input().strip()

	if album is None: 
		# and the album name
		print "Album name ('' to keep the current name):",
		album = raw_input().strip()

	#Check path correctness
	if not os.path.exists(root) or os.path.isfile(root):
		print >> sys.stderr, "Given folder does not exist or is a file... Stopping"
		sys.exit(-1)


	#Reformat path (ensure '/' at the end)	
	root = os.path.join(root,'')

	#Count the total number of tracks
	total_tracks = len(glob.glob(root+"CD*/*.mp3"))
	len_tot_tracks = str(len(str(total_tracks)))

	tracks_treated = 0


	regex = re.compile("^\d*\s.*$") # used to determine wheter or not a file starts with track number

	for cd_folder in sorted(glob.glob(root+'*')):
		if os.path.basename(cd_folder)[0:2]=="CD":

			print "Treating", os.path.basename(cd_folder)
			cd_tracks=0
			for mp3_file in sorted(glob.glob(cd_folder+"/*.mp3")):


				#copy file to the root_folder
				copy(mp3_file,root+'tmp_'+os.path.basename(mp3_file))

				#open newly copied file
				audio = EasyID3(root+'tmp_'+os.path.basename(mp3_file))

				# retrieve the track number (if indicated)
				if 'tracknumber' in audio.keys():
					current_track = int(str(audio["tracknumber"]).split('/')[0][3:])
				# or infer it
				else:
					print >> sys.stderr, "Warning: track",os.path.basename(cd_folder)+"/"+os.path.basename(mp3_file),\
					"had no track number tag. The inferred (inner) track number is", cd_tracks+1
					current_track = cd_tracks+1

				audio["tracknumber"]=str(current_track+tracks_treated)+"/"+str(total_tracks)

				if album is not "":
					audio['album'] = album

				audio.save()


				# change file name
				new_file_name = os.path.basename(mp3_file)
				if regex.match(new_file_name):
					new_file_name = ' '.join(new_file_name.split()[1:])
				new_file_name = (("%0"+len_tot_tracks+"i") % (current_track+tracks_treated)) + ' ' + new_file_name

				#move file
				move(root+'tmp_'+os.path.basename(mp3_file),root+new_file_name)

				#increment inner cd counter
				cd_tracks+=1

			#update total number of tracks	
			tracks_treated+=cd_tracks

	print "Job Done !"

	

if __name__=="__main__":
	main(sys.argv[:1])