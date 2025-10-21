import sys
import Library.GlobalAdapter as GlobalAdapter
import json
import requests

from pprint import pprint
from Method.PrintMethod import PrettyPrint
from Library.HttpAPIHelper import *

sys.path.append("./")


class FusionAPI:
    # ----------fusion前台---------------

    def fusion_signin(DataVariable):  # fusion前台登入
        path = "/api/v2/User/signIn"
        payload = json.dumps(DataVariable)
        header = {
            "Content-Type": "application/json",
        }
        response = APIController.SendAPIPacket("POST", url=GlobalAdapter.CommonVar.FusionUrl + path, headers=header,
                                               data=payload,sleep=2)
        PrettyPrint(response)
        GlobalAdapter.AuthVar.FusionAuth = response.headers["Auth-Token"]
        GlobalAdapter.AuthVar.FusionIdentity = response.headers["Auth-Identity"]
        return response.json()

    def withdrawrecords(DataVariable):  # 取得fusion提現紀錄
        path = "/api/Account/withdrawRecords"
        payload = json.dumps(DataVariable)
        header = {
            "Content-Type": "application/json",
            "Auth-Token": GlobalAdapter.AuthVar.FusionAuth,
            "Auth-Identity": GlobalAdapter.AuthVar.FusionIdentity
        }
        response = APIController.SendAPIPacket("POST", url=GlobalAdapter.CommonVar.FusionUrl + path, headers=header,
                                               data=payload)
        PrettyPrint(response)
        return response.json()


class BackstageFusion:
    # ----------fusion後台---------------

    def fusion_backstage_signin(DataVariable):  # fusion後台登入
        path = "/admin/Member/memberLogin"
        payload = json.dumps(DataVariable)
        header = {
            "Content-Type": "application/json",
        }
        response = APIController.SendAPIPacket("POST", url=GlobalAdapter.CommonVar.BackstageFusionUrl + path,
                                               headers=header, data=payload)
        PrettyPrint(response)
        GlobalAdapter.AuthVar.BackstageFusionAuth = response.headers["Auth-Token"]
        return response.json()

