# coding=utf-8
"""
Script that is used to remove/keep specific tracks of a series
of mkv video files. This is especially useful when all the mkvs
have similar structures, and that for instance one only wants to
keep the main video track, the english audio and the french subs.

This script uses the two binaries mkvmerge and mkvinfo that can
be downloaded from MKVToolNix website. 

Usage:
remove_mkv_tracks.py --interactive [--mkvmergepath </path/to/mkvmerge>]

Author : Côme Weber
"""

import getopt
import glob
import os
import sys
import subprocess

HELPCMD = "remove_mkv_tracks.py --interactive [--mkvmergepath </path/to/mkvmerge>]"

MKVMERGE = "/Applications/MKVToolNix-9.2.0.app/Contents/MacOS/mkvmerge" # default mkvmerge/mkvinfo path

def main(argv):

    mkv_merge_path = "mkvmerge"
    prefix="new_"
    interactive_mode = False

    try:
        opts, args = getopt.getopt(argv, "i", ["--interactive"])
    except getopt.GetoptError as err:
        print HELPCMD
        sys.exit(-1)

    for opt, arg in opts:
        if opt in ("-i","--interactive"):
            interactive_mode = True
            break

    if interactive_mode:
        print "path to mkvmerge bin (default is '"+MKVMERGE+"'): ",
        var = raw_input().strip()
        mkv_merge_path = var if var != "" else MKVMERGE

        print "path to directory containing MKVs: ",
        mkv_folder = os.path.join(raw_input().strip(),'')

        ref_tracks = ref_tracks_objects = ref_like_files = ref_diff_files = None
        mkv_file_counter = 0

        has_diff = False
        handle_diff_files = False

        for mkv_file in map(os.path.basename,sorted(glob.glob(mkv_folder+"*.mkv"))):

            mkv_file_counter+=1

            #compute track scheme
            infos = [Track(t) for t in subprocess.check_output(mkv_merge_path[:-5]+ "info "+ mkv_folder+mkv_file,shell=True).split('| + A track')[1:]]
            tracks = '\n'.join([str(t) for t in infos])

            #store reference scheme
            if ref_tracks is None:
                ref_tracks = tracks
                ref_like_files = [mkv_file]
                ref_tracks_objects = infos
                print "Ref_file:", mkv_file
                print ref_tracks

            #compare schemes
            elif ref_tracks != tracks:
                print >> sys.stderr, "Differences observed between ref file and",mkv_file
                print >> sys.stderr, tracks
                has_diff = True
                if ref_diff_files is None:
                    ref_diff_files = [mkv_file]
                else:
                    ref_diff_files.append(mkv_file)

            else:
                ref_like_files.append(mkv_file)

        if has_diff:
            print "Differences were found.\nDo you want to take these files into account (default",("True)" if handle_diff_files else "False)"),  "?:"
            answer = raw_input().strip()
            if answer.lower() in ["yes","y","1","true",'t']:
                handle_diff_files = True
            elif answer.lower() in ["no",'n','0','false','f']:
                handle_diff_files = False

        print "video tracks to keep (everything kept by default): ",
        video_tracks = raw_input().strip()

        print "audio tracks to keep (everything kept by default): ",
        audio_tracks = raw_input().strip()

        print "subtitle tracks to keep: ",
        sub_tracks = raw_input().strip()

        print "Prefix to append to new mkvs (default is '"+prefix+"'): ",
        var = raw_input().strip()
        prefix = var if var != "" else prefix

        '"-o "fixed_$file" -a !3 --compression -1:none "$file""'

        for i, mkv_file in enumerate(ref_like_files + ref_diff_files if has_diff and handle_diff_files else ref_like_files,start=1):

            cmd = mkv_merge_path + ' -o "'+mkv_folder+prefix+mkv_file+'"'
            cmd += ' -a '+ find_tracks_ids(audio_tracks,ref_tracks_objects,"audio")
            cmd += ' -d '+ find_tracks_ids(video_tracks,ref_tracks_objects,"video")
            cmd += ' -s '+ find_tracks_ids(sub_tracks,ref_tracks_objects,"subtitles")
            cmd += ' --compression -1:none'
            cmd += ' '+mkv_folder+mkv_file
            print "File",str(i)+'/'+str(mkv_file_counter - len(ref_diff_files) if has_diff and not handle_diff_files else mkv_file_counter)+ ":", cmd
            subprocess.check_output(cmd,shell=True)

        print "Done."

def find_tracks_ids(selection, ref_tracks, type):
    #todo handle ! prefix

    selected_tracks = set()
    if selection == '-1':
        return '-1'
    elif selection == "":
        for track in ref_tracks:
            if track.type == type:
                selected_tracks.add(track.track_id)
    for select in selection.split(','):
        for track in ref_tracks:
            if track.type == type and select in (str(track.track_id), track.lang):
                selected_tracks.add(track.track_id)

    return ','.join(map(str,list(selected_tracks))) if len(selected_tracks)>0 else '-1'




class Track:
    def __init__(self,description):
        self.track_id = int(description.split('track ID for mkvmerge & mkvextract:')[1].split(')')[0].strip())
        self.type = description.split('Track type:')[1].split()[0].strip()
        if "Language:" in description:
            self.lang = description.split('Language:')[1].split()[0].strip()
        else:
            self.lang = "und"

    def __str__(self):
        return 'Track ID '+str(self.track_id)+ ": "+self.type+" ["+self.lang+']'


if __name__ == '__main__':
    main(sys.argv[1:])
