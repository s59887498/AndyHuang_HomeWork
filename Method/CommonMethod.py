#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging, names, datetime, random, os
from id_validator import validator

from Method.base import *
import xml.etree.ElementTree as ET
import pandas as pd
import openpyxl
import pyotp
from PIL import Image
from pyzbar.pyzbar import decode
import re

from Method.base import load_stage_config

# Set Global Data
load_commonSetting(env="Fusion")
load_commonSetting(env="BackstageFusion")
# Load Data
UserVariable = load_stage_config(config_file_name="User")
BackstageUserVariable = load_stage_config(config_file_name="BackstageUser")


def ReplaceJsonTemp(SampleData, ElementChange):  # 置換json內容
    '''
        SampleData : From /config/*json
        ElementChange : Input you want to replace(json format)
    '''
    ResultJson = {**SampleData, **ElementChange}
    return ResultJson


def FilterElementWhenDictInList(InputList, ElementName):  # 提取response相同元素的列表
    '''
        For exanple :
        InputList = [{"sample":sampletest,"sample1":test},{"sample":sampletest1,"sample2":test},{"sample3":sampletest2,"":test}]
        FilterElementWhenDictInList(InputList,"Sample")
        it will return
        [sampletest,sampletest1,sampletest2]
    '''
    ResultList = list(filter(lambda item: item, map(lambda item: item.get(ElementName), InputList)))
    return ResultList


def RandomPhoneNumber():  # 隨機產生電話號碼
    NumTemp = str(int(datetime.datetime.now().timestamp()))[-9:]
    PhoneNumber = "13%s" % NumTemp
    return PhoneNumber


def RandomRealName():  # 隨機產生名字
    RealNameTmp = names.get_last_name()
    RealName = "Autotest" + RealNameTmp
    return RealName


def RandomIDValiator():  # 隨機產生中國地區身分證
    RandomID = validator.fake_id()
    return RandomID


def RandomBirthDay():  # 隨機產生日期
    RandomBirth = str(datetime.date.today())
    return RandomBirth


def CompareTwoList(ListOne, ListTwo, Key=None):  # 兩個列表比對返回bool
    if Key == None:
        return sorted(ListOne) == sorted(ListTwo)
    else:
        return sorted(ListOne, key=lambda x: x[Key]) == sorted(ListTwo, key=lambda x: x[Key])


def RandomFloatStr(RangeStart, RangeEnd, DecimalPoint):
    Result = round(random.uniform(RangeStart, RangeEnd), DecimalPoint)
    return str(Result)


def RamdomIntStr(RangeStart, RangeEnd):
    Result = random.randint(RangeStart, RangeEnd)
    return str(Result)


# 一些時間存放在這()
# ====================================================================================================
def StartTimeToYear(
        Day=0):  # Day can be set -n ~ n sample:today is 2023/09/09, 2023/09/09 00:00:00, Day = 0>> 2023/09/09
    datetime_combine = datetime.datetime.now() + datetime.timedelta(Day)
    datetime_combine_min = datetime.datetime.combine(datetime_combine, datetime.time.min)  # 取當天日期
    return datetime_combine_min.strftime("%Y")


def StartTimeToDay(
        Day=0):  # Day can be set -n ~ n sample:today is 2023/09/09, 2023/09/09 00:00:00, Day = 0>> 2023/09/09
    datetime_combine = datetime.datetime.now() + datetime.timedelta(Day)
    datetime_combine_min = datetime.datetime.combine(datetime_combine, datetime.time.min)  # 取當天日期
    return datetime_combine_min.strftime("%Y/%m/%d")


def EndTimeToDay(
        Day=1):  # Day can be set -n ~ n sample: today is 2023/09/09, Day = 0 >> 2023/09/09 00:00:00, Day = 1 >> 2023/09/10
    datetime_combine = datetime.datetime.now() + datetime.timedelta(Day)
    datetime_combine_max = datetime.datetime.combine(datetime_combine, datetime.time.max)  # 取當天日期+1 day
    return datetime_combine_max.strftime("%Y/%m/%d")


def StartTimeToMin(
        Day=0):  # Day can be set -n ~ n sample:today is 2023/09/09, Day = 0 >> 2023/09/09 00:00:00 , Day = -1 >> 2023/09/08 11:11:11
    # 輸入時的開始時間格式
    datetime_combine = datetime.datetime.now() + datetime.timedelta(Day)
    datetime_combine_min = datetime.datetime.combine(datetime_combine, datetime.time.min)  # 取當天時分最小值
    return datetime_combine_min.strftime("%Y/%m/%d %H:%M")


def EndTimeToMin(
        Day=7):  # Day can be set -n ~ n sample:today is 2023/09/09, Day = 0 >> 2023/09/09 23:59:59, Day = 1 >> 2023/09/10 23:59:59
    # 輸入時的結束時間格式
    datetime_combine = datetime.datetime.now() + datetime.timedelta(Day)
    datetime_combine_max = datetime.datetime.combine(datetime_combine, datetime.time.max)  # 取當天時分最大值
    return datetime_combine_max.strftime("%Y/%m/%d %H:%M")


def StartTimeToSec(
        Day=0):  # Day can be set -n ~ n sample:today is 2023/09/09, Day = 0 >> 2023/09/09 00:00:00 , Day = -1 >> 2023/09/08 11:11:11
    # 標題的時間格式
    datetime_combine = datetime.datetime.now() + datetime.timedelta(Day)
    datetime_combine_min = datetime.datetime.combine(datetime_combine, datetime.time.min)  # 取當天時分秒最小值
    return datetime_combine_min.strftime("%Y/%m/%d %H:%M:%S")


def EndTimeToSec(
        Day=0):  # Day can be set -n ~ n sample:today is 2023/09/09, Day = 0 >> 2023/09/09 23:59:59, Day = 1 >> 2023/09/10 23:59:59
    datetime_combine = datetime.datetime.now() + datetime.timedelta(Day)
    datetime_combine_max = datetime.datetime.combine(datetime_combine, datetime.time.max)  # 取當天時分秒最大值
    return datetime_combine_max.strftime("%Y/%m/%d %H:%M:%S")


def NowTime(Day=0):
    # titleTime
    datetime_combine = datetime.datetime.now() + datetime.timedelta(Day)
    return datetime_combine.strftime("%Y/%m/%d %H:%M:%S")


def NowTime_Hr_Min_Sec(Day=0):  # 現在時分秒
    datetime_combine = datetime.datetime.now() + datetime.timedelta(Day)
    return datetime_combine.strftime("%H:%M:%S")


def PublistTime(Day=0):  # 公告的時間格式
    datetime_combine = datetime.datetime.now() + datetime.timedelta(Day)
    return datetime_combine.strftime("%Y-%m-%dT%H:%M")


def PublishTime_on_fore(Day=0):  # 後台前端顯示公告的時間格式
    datetime_combine = datetime.datetime.now() + datetime.timedelta(Day)
    return datetime_combine.strftime("%Y-%m-%d %H:%M:00")


def StartTime_on_fore(Day=0):
    datetime_combine = datetime.datetime.now() + datetime.timedelta(Day)
    datetime_combine_min = datetime.datetime.combine(datetime_combine, datetime.time.min)  # 取當天時分秒最小值
    return datetime_combine_min.strftime("%Y-%m-%d %H:%M:00")  # 後台前端顯示的開始時間格式


def EndTime_on_fore(Day=7):
    # 今天起 七天後的現在時間
    datetime_combine = datetime.datetime.now() + datetime.timedelta(Day)
    datetime_combine_max = datetime.datetime.combine(datetime_combine, datetime.time.max)  # 取當天時分秒最大值
    return datetime_combine_max.strftime("%Y-%m-%d %H:%M:00")  # 後台前端顯示的開結束時間格式


# Module() 重複的執行功能可以放在這
# ====================================================================================================

def Download_Excel_File(response, filename):  # 下載excel
    directory = './download/'
    file_name = filename + '.xlsx'
    # 使用 os.path.join() 组合目录和文件名
    path = os.path.join(directory, file_name)
    if response.status_code == 200:
        with open(path, 'wb') as file:
            file.write(response.content)
        logging.info(f"excel 下载成功，保存到 {path}")
    else:
        logging.info("excel 下载失败")


def Excel_compare_download_to_title_1_column(filename, text):  # 比對excel的title
    directory = './download/'
    df = pd.read_excel(directory + filename + ".xlsx")
    column_titles = df.columns.tolist()
    print(column_titles)
    assert column_titles[0] == text  # 比對是不是同一個字，確保有下載成功
    logging.info("Excel 比對成功")


def Excel_Get_Value_and_Comparison(filename, position, text):  # 比對excel的指定儲存格的內容
    directory = './download/'
    workbook = openpyxl.load_workbook(directory + filename + ".xlsx")
    sheet = workbook['Worksheet']
    print(sheet[position].value)
    assert text in str(sheet[position].value)  # 比對是不是同一個字，確保有下載成功
    logging.info("Excel 比對內容成功")


# Fusion前台功能模組區
# ====================================================================================================
def fusion_signin():
    """fusion前台登入"""

    # Login fusion
    LoginResponse = FusionAPI.fusion_signin(UserVariable["fusion_signin"])
    assert LoginResponse["errorcode"] == 200


# 後台功能模組區
# ====================================================================================================
def fusion_backstage_signin():
    """fusion後台登入"""

    # Login fusion
    LoginResponse = BackstageFusion.fusion_backstage_signin(BackstageUserVariable["fusion_backstage_signin"])
    assert LoginResponse["errorcode"] == 200
