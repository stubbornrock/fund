#!/bin/bash

#define echo color
function echo_info(){
    echo -e "\033[32m >> $1 \033[0m"
}
function echo_error(){
    echo -e "\033[31m >> $1 \033[0m"
}
function echo_warn(){
    echo -e "\033[33m >> $1 \033[0m"
}
##
function rebuild_db(){
    echo_info "Clear database fund ..."
    mysql -uroot -e "drop database if exists fund;"
    mysql -uroot -e "create database if not exists fund DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
    echo_info "Auth database fund ..."
    mysql -uroot -e "grant all privileges on fund.* to 'root'@'localhost' identified by '123456' with grant option; "
    echo_info "Creating table fund ..."
    python ./modules/mysql.py
    echo_info "View table schema ..."
    mysql -uroot -e "use fund;desc fund;"
}

function pull_fund(){
    echo_info "Pull all fund info ...."
    python ./modules/pull.py
    echo_info "Table Record nums ..."
    mysql -uroot -e "use fund;select count(*) from fund;"
}

function crawler(){
    mkdir -p /var/log/crawler/
    echo_info "Crawler all fund info ..."
    read -p " >> Are you ready to start process using :(log|db):" c
    if [[ $c == "log" ]];then
        sh ./modules/crawler.sh log &
    elif [[ $c == "db" ]];then
        sh ./modules/crawler.sh db &
    fi
}

function crawler_stop(){
    num=`ps -ef | grep crawler | wc -l`
    if [[ $num -gt 1 ]];then
        echo_info "Crawler Process has started.. stop it !!"
        pid=0
        alls=`ps -ef | grep crawler | awk '{print $2"-"$8}'`
        for p in $alls;do
            arr=(${p//-/ })
            if [[ ${arr[1]} == "python" ]];then
                pid=${arr[0]}
            fi
        done
        read -p " >> Are you ready to stop the process :(Y|N):" c
        if [[ $c == "Y" ]];then
            kill -9 $pid >/dev/null 2>&1
            crawler_stop
            echo $pid
        fi
    else
        echo_info "Crawler Process not running!!"
    fi
}

function patch(){
    #num=`python ./modules/patch.py`
    read -p " >> Are you ready to check process using :(log|db):" c
    if [[ $c == "log" ]];then
        num=`grep -nr "FAIL" /var/log/crawler/*.* |wc -l`
        echo_info "There are $num http url errors..."
        #grep -nr "FAIL" /var/log/crawler/*.*
        echo_info  "Try to reCrawler the urls!!"
        if [[ $num -gt 0 ]];then
            python ./modules/crawler.py patch
        fi
    elif [[ $c == "db" ]];then
        num=`mysql -uroot -e "use fund;select count(*) from fund where updated=False;" |sed -n '2p'`
        echo_info "There are $num http url errors..."
        echo_info  "Try to reCrawler the urls!!"
        if [[ $num -gt 0 ]];then
            python ./modules/crawler2.py patch
        fi
    fi
}

function logs(){
    num=`ps -ef | grep crawler | wc -l`
    if [[ $num -gt 1 ]];then
        echo_info "Crawler Process is running!!"
    else
        echo_info "Crawler Process not running!!"
    fi
    read -p " >> Are you ready to check process using :(log|db):" c
    if [[ $c == "log" ]];then
        count=0
        for file in `ls -l /var/log/crawler | awk '{print $9}'`;do
            lines=`cat /var/log/crawler/$file | wc -l`
            count=`expr $count + $lines`
        done
        echo_info "Crawler total Num: $count"
        num=`grep -nr "FAIL" /var/log/crawler/*.* |wc -l`
        echo_info "Crawler error Num: $num"
    elif [[ $c == "db" ]];then
        total=`mysql -uroot -e "use fund;select count(*) from fund;" | sed -n '2p'`
        count=`mysql -uroot -e "use fund;select count(*) from fund where updated=True;" |sed -n '2p'`
        echo_info "Crawler total Num: $total"
        echo_info "Crawler Num: $count"
    fi
}

function analyse(){
    python ./modules/analyse.py
}

function menu(){
    echo_warn "################### Choose your Menu ##############"
    echo_warn "###                                            ####"
    echo_warn "###      r  --> rebuild your enviroment        ####"
    echo_warn "###      s  --> sync all fund code             ####"
    echo_warn "###      c  --> crawler all code info          ####"
    echo_warn "###      cs --> crawler process stop           ####"
    echo_warn "###      p  --> path crawler error code        ####"
    echo_warn "###      h  --> how many fund has crawler      ####"
    echo_warn "###      a  --> analyse the result             ####"
    echo_warn "###      q  --> exit the menu                  ####"
    echo_warn "###                                            ####"
    echo_warn "################### Choose your Menu ##############"
}
function start()
{
    while :
    do
        menu
        read -p " >> Please choose the function to install function:" c
        case $c in
        'r')
            echo_info "Now start to rebuild database ..."
            rebuild_db
            ;;
        's')
            echo_info "Now start to sync all fund code ..."
            pull_fund
            ;;
        'c')
            echo_info "Now start to crawler all fund infos ..."
            crawler
            ;;
        'cs')
            echo_info "Now stop to crawler all fund infos ..."
            crawler_stop
            ;;
        'p')   
            echo_info "Now start to patch all error fund codes ..."
            patch
            ;;
        'h')
            echo_info "Now start to find crawlerd fund num ..."
            logs
            ;;
        'a')
            echo_info "Now start to analyse the result ..."
            analyse
            ;;
        'q')
            exit
        esac
    done
}
start
