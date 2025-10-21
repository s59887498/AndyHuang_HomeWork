#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys, re, pytest, configparser, json, logging, hashlib

sys.path.append("./")
from Core.APIQuery import *
# from Method.CommonMethod import *
from Method.RequestMethod import *
import Library.GlobalAdapter as GlobalAdapter


# Load資料用的()
# ====================================================================================================
class ConfigLoader: #

    def __init__(self, base_path="./Config/"):
        '''啟動時自動導入'''
        self.base_path = base_path
        sys.setrecursionlimit(3000)

    def load_config(self, file_name):
        '''Config資料夾裡面的json檔轉成程式可用資料'''
        file_path = f"{self.base_path}{file_name}.json"
        with open(file_path, encoding='utf-8') as config_file:
            return json.load(config_file)

    def load_stage_config(self, config_file_name):
        '''Loading Config資料夾裡面的json檔名'''
        return self.load_config(config_file_name)

    def load_commonSetting(self, env):
        '''讀取CommonSetting.ini"的Url'''
        CommonSetting = configparser.ConfigParser()
        path = f"{self.base_path}CommonSetting.ini"
        CommonSetting.read(path)
        if env == "Fusion":
            GlobalAdapter.CommonVar.FusionUrl = CommonSetting[(env)][GlobalAdapter.FramkWorkVar.Enviornment]
            return GlobalAdapter.CommonVar.FusionUrl
        elif env == "BackstageFusion":
            GlobalAdapter.CommonVar.BackstageFusionUrl = CommonSetting[(env)][GlobalAdapter.FramkWorkVar.Enviornment]
            return GlobalAdapter.CommonVar.BackstageFusionUrl
        else:
            pass


# ConfigLoader()
# ====================================================================================================
con = ConfigLoader()
load_config = con.load_config
load_stage_config = con.load_stage_config
load_commonSetting = con.load_commonSetting
