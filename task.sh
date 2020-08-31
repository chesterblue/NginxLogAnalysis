#!/bin/bash
date=$(date "+%Y%m%d")
file="/var/log/nginx/access.log-${date}.gz"
gunzip -c $file > ./access.log
python main.py