# coding=utf-8
"""
Script that is used to synchronize subtitles on a video, given
the entry and exit points time references of both the video
and the subtitles. It outputs two factors that are especially 
made to be used with Jubler (custom reencoding function).

Usage:
python compute_subtitle_offset.py

Author : Côme Weber
"""

print "Timecode must be of the following shape : HH:MM:SS.MMM"
print "First audio timecode : ",
a1 = raw_input("")
print "Last audio timecode : ",
a2 = raw_input("")
print "First subtitle timecode : ",
s1 = raw_input("")
print "Last subtitle timecode : ",
s2 = raw_input("")

def convert_to_sec(tc):
	split = [float(i) for i in tc.strip().split(':')]
	while len(split)<3:
		split=[0]+split
	sec = 0.
	for factor, time in zip([3600,60,1],split):
		sec += factor*time
	return sec

a1 = convert_to_sec(a1)
a2 = convert_to_sec(a2)
s1 = convert_to_sec(s1)
s2 = convert_to_sec(s2)

speed_factor = (a2-a1)/(s2-s1)

print "The speed factor is " + '%.15f' % speed_factor

print "Prior to that, you should offset the sub by ", a1-s1

print "The central time is ", a1
