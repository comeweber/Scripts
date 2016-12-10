# Scripts

This repositery stores various scripts of general use, mainly dealing the gestion of multimedia files.

##Compute Subtitle Offset

`compute_subtitle_offset.py` is a script used to compute quickly the reencoding factors that should be used to synchronize subtitles wrt a video file. The factors computed are especially made for an usage with Jubler.


##Extract Artworks

`extract_artwork.py` is a script used to extract the embedded cover image in mp3 files into a `folder.jpg` file. This is made to run recursively in a music library, leading to the extraction of a cover file per album. This is useful for some softwares that don't always recongnize embedded covers (like DSAudio for instance). 

It is based on the [Mutagen](https://github.com/quodlibet/mutagen) python module.

##Remove MKV Tracks

`remove_mkv_tracks.py` is a script used to easily remove the unwanted tracks in a series of `mkv` video files. 

It is based on the `mkvmerge` and `mkvinfo` binaries that can be found on [MKVToolNix's website](https://mkvtoolnix.download).

##Multi CD Merge

`reorder_tracks.py` is a script used to merge a multi-CD album into a one CD album (a concatenation of all the CDs), with the following actions:

* Set a common album name
* Update automatically the tracks indices 


