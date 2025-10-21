# -*- coding: UTF-8 -*-
import logging
import os
import time

from Core.APIQuery import *
from Method.CommonMethod import *
from Method.RequestMethod import *
from Method.base import *

case = os.path.basename(__file__)

# Set Global Data
load_commonSetting(env="Fusion")
load_commonSetting(env="BackstageFusion")

# Load Data
userCenterVariable = load_stage_config(config_file_name="userCenter")


# 整個.py測試前執行程式碼，執行 Login
def setup_module():
    logging.info("整個.py測試前做事情")
    fusion_signin()
    fusion_backstage_signin()


# 整個.py測試後執行程式碼，執行 Logout
def teardown_module():
    logging.info("整個.py測試前後做事情")


# Test case放在這
# ====================================================================================================
@pytest.mark.bet
def test_get_withdrawrecords():
    """fusion前端-取得提現紀錄"""
    logging.info("Step 1 : onlineRecharge in fusion")
    WithdrawRecordsResponse = FusionAPI.withdrawrecords(userCenterVariable["withdrawrecords"])

    assert WithdrawRecordsResponse["errorcode"] == 200
    assert WithdrawRecordsResponse["message"] == "操作成功"


if __name__ == '__main__':
    pytest.main(['-s', __file__])
