#!/bin/bash

#  ishijie.sh
#  catch video stream from lovev site.
#  merg ts pieces into one video file.
#  Created by Xiang Xiao on 31/03/2014.
#
#  first parameter indicate the first frame url.
#  second parameter indicate the output video file name.

url=$1
fileName=$2
index=0
touch ${index}.ts
echo "start" >${index}.ts
while [ -s ${index}.ts ]
do
index=$(($index+1))
curl -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30" ${url/@0-0/@0-$(($index-1))} > ${index}.ts
#echo ${url/@0-0/@0-$(($index-1))}
#echo $index
echo "have download the ${index} files"
done
command1="cat 0.ts"
for((i=1;i<index;i++))
do
command1=${command1}" "${i}".ts"
done
command1=${command1}" > video.ts"
echo $command1
eval $command1
command2="ffmpeg -i video.ts -qscale 4 -strict -2 "${fileName}".mp4"
echo $command2
eval $command2
rm *.ts


