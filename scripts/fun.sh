#!/usr/bin/bash

while read -r HTML_FILE; do

    case $HTML_FILE in
       Only*)

         # HTML_FILE=$(echo $HTML_FILE | cut -d ' ' -f3)
         # if [[ $HTML_FILE == *"old_build"* ]]; then
         #    echo "Old Build We Should Delete!"
         #    # echo $HTML_FILE | cut -d ' ' -f3
         # fi

         if [[ $HTML_FILE == *"/build"* ]]; then
            cp $(echo $HTML_FILE | awk '{print $3 $4}' | sed 's/:/\//') ./tmp/new_build/beginworld_finance/
         fi
       ;;
       *differ)
         cp $(echo $HTML_FILE | cut -d ' ' -f2) ./tmp/new_build/beginworld_finance/
       ;;
    esac
done <<< "$(diff -qr ./build ./tmp/old_build/)"
# I use this syntax to read in whole lines from diff and loop over theme

aws s3 sync ./tmp/new_build/beginworld_finance/ s3://beginworld.exchange-f27cf15
