#!/bin/bash
style=$1
if [[ $style == "log" ]];then
    python ./modules/crawler.py all
elif [[ $style == "db" ]];then
    python ./modules/crawlerV3.py all
fi
