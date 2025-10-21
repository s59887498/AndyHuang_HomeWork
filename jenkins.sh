#!/bin/bash
work_directory=$(pwd)
cd ./$BUILD_TARGET
rm -rf ./target  || true #先清空專案資料夾原本的report，不要讓舊資料影響到
pip install --user -r ./requirements.txt
python3 -m pytest ./$MultiCase -s -q --alluredir=./target/allure-results