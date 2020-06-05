#!/usr/bin/bash

NEW_BUILD_FOLDER="./tmp/new_build"
NEW_BEGINWORLD="$NEW_BUILD_FOLDER/beginworld_finance"

rm -rf $NEW_BUILD_FOLDER

# Is -p POSIX compliant?
mkdir -p $NEW_BEGINWORLD

while read -r HTML_FILE; do

    case $HTML_FILE in
       Only*)

         # HTML_FILE=$(echo $HTML_FILE | cut -d ' ' -f3)
         # if [[ $HTML_FILE == *"old_build"* ]]; then
         #    echo "Old Build We Should Delete!"
         #    # echo $HTML_FILE | cut -d ' ' -f3
         # fi

         if [[ $HTML_FILE == *"/build"* ]]; then
            cp $(echo $HTML_FILE | awk '{print $3 $4}' | sed 's/:/\//') $NEW_BEGINWORLD
         fi
       ;;
       *differ)
         cp $(echo $HTML_FILE | cut -d ' ' -f2) $NEW_BEGINWORLD
       ;;
    esac
done <<< "$(diff -qr ./build ./tmp/old_build/)"
# I use this syntax to read in whole lines from diff and loop over theme

aws s3 sync "$NEW_BEGINWORLD/" s3://beginworld.exchange-f27cf15
