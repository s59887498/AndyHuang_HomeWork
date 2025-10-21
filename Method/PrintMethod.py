#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime


from pprint import pprint

import json
def PrettyPrint(resp,Debug_mode="Close"):#只能用在Requests Response(不能使用json format)
    #如果debug mode是等於Open,將會顯示全部API的資訊「Payload、Header等」
    print ("{:=^40s}".format("START"))
    if Debug_mode == "Open":
        try:
            print("[當前時間]")
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            time_data = {
                "post_time": formatted_time
            }
            time_json_data = json.dumps(time_data)
            pprint(time_json_data)

            pprint(resp.request.method+' '+resp.request.url)
            print ("[Payload]")
            pprint(resp.request.body)
            print ("[Header]")
            pprint(resp.headers)
            print("[Response]")
            pprint(resp.json())
        except:
            pprint("Content is not valid JSON.")
            pprint(resp)  # 如果不是 JSON，則輸出原始內容
    else:
        try:
            pprint(resp.request.method + ' ' + resp.request.url)
            print("[Response]")
            pprint(resp.json())
        except:
            pprint("Content is not valid JSON.")
            pprint(resp)  # 如果不是 JSON，則輸出原始內容


    print("{:=^40s}".format("END"))