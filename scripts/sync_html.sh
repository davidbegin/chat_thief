#!/usr/bin/sh

rm -rf ./tmp/new_build
mkdir -p ./tmp/new_build/beginworld_finance

for html_file in $(diff -qr ./build ./tmp/old_build/ | cut -d ' ' -f2)
do
   echo $html_file
   cp $html_file ./tmp/new_build/beginworld_finance/
done

aws s3 sync ./tmp/new_build/beginworld_finance/ s3://beginworld.exchange-f27cf15
