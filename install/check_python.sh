#!/usr/bin/env bash

V1=3
V2=4

echo need python version is : $V1.$V2

U_V1=`python -V 2>&1|awk '{print $2}'|awk -F '.' '{print $1}'`
U_V2=`python -V 2>&1|awk '{print $2}'|awk -F '.' '{print $2}'`

echo your python version is : $U_V1.$U_V2

if [ $U_V1 -lt $V1 ];then
    echo 'The current Python version is below 3.4 and can not install SilverBlog'
    exit 1
if [ $U_V2 -lt $V2 ];then
    echo 'The current Python version is below 3.4 and can not install SilverBlog'
    exit 1