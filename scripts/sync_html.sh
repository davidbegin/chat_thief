#!/usr/bin/bash

NEW_BUILD_FOLDER="./tmp/new_build"
NEW_BEGINWORLD="$NEW_BUILD_FOLDER/beginworld_finance"

rm -rf $NEW_BUILD_FOLDER

# Is -p POSIX compliant?
mkdir -p $NEW_BEGINWORLD
mkdir -p $NEW_BEGINWORLD/styles
mkdir -p $NEW_BEGINWORLD/js
mkdir -p $NEW_BEGINWORLD/commands

while read -r HTML_FILE; do

    case $HTML_FILE in
       Only*)

         # HTML_FILE=$(echo $HTML_FILE | cut -d ' ' -f3)
         if [[ $HTML_FILE == *"old_build"* ]]; then
            DEST_PATH=$(echo $HTML_FILE | sed 's/\// /g' | rev | awk '{print $1 "/" $2}' | rev | sed 's/://')
            # echo "DELETING: ${DEST_PATH}"
            aws s3 rm "s3://beginworld.exchange-f27cf15/${DEST_PATH}"
         fi

         if [[ $HTML_FILE == *"/build"* ]]; then
           FILE_PATH=$(echo $HTML_FILE | awk '{print $3 $4}' | sed 's/:/\//')
           DEST_PATH=$(echo $HTML_FILE | sed 's/\// /g' | rev | awk '{print $1 "/" $2}' | rev | sed 's/://' | sed 's/beginworld_finance\///')

           # echo "NEW FILE: ${DEST_PATH}"
           cp $FILE_PATH "${NEW_BEGINWORLD}/${DEST_PATH}"
         fi
       ;;
       *differ)
         DEST_PATH=$(echo $HTML_FILE | sed 's/\// /g' | rev | awk '{print $2 "/" $3}' | rev | sed 's/://' | sed 's/beginworld_finance\///')
         # echo "FILE DIFF: ${DEST_PATH}"
         cp $(echo $HTML_FILE | cut -d ' ' -f2) "${NEW_BEGINWORLD}/${DEST_PATH}"
       ;;
    esac
done <<< "$(diff -qr ./build ./tmp/old_build/)"
# I use this syntax to read in whole lines from diff and loop over theme

# Maybe CSS --delete is only for styles??
aws s3 sync "$NEW_BEGINWORLD/" s3://beginworld.exchange-f27cf15
