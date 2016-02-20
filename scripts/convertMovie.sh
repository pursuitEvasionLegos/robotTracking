#!/bin/bash

input=$1
ext=${input#*.}

output=${input%.*}.mp4

if [ "$ext" == "avi" ]; then
    ffmpeg -i "$input" -acodec libfaac -b:a 128k -vcodec mpeg4 -b:v 1200k -flags +aic+mv4 "$output"
else
    echo "Input is not an avi file."
    exit 1
fi
