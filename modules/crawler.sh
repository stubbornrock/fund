#!/bin/bash
style=$1
if [[ $style == "log" ]];then
    python ./modules/crawler.py all
elif [[ $style == "db" ]];then
    python ./modules/crawler2.py all
fi
