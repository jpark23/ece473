#!/usr/bin/python

import sys

if len(sys.argv) != 3: sys.exit("needs a file to transcribe and a location to transcribe it to")

transcription = ""
with open(sys.argv[1], 'r') as f:
    for count, line in enumerate(f, start=1):
        if count % 2 == 0:
            transcription += line
output = open(sys.argv[2], 'w')
output.write(transcription.replace("\n", " "))
output.close()
f.close()