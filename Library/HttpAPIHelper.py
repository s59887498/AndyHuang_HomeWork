#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
 HttpApiHelper.py: The def of this file called by other function.
'''
import time
import requests
import logging

##For Send HTTP packets to API interface
class APIController():
    def SendAPIPacket(http_method, url, headers=None, data=None,sleep=0,url_param=None,files=None):
        ''' SendAPIPacket : Send API Packet
                Input argu :
                    http_method - get, delete, post, put
                    url - url for http request
                    payload - payload for http request
                    headers - headers for http request
                Return code :
                    http response - session / status / text
                    0 - fail
        '''
        logging.info("Enter APIController SendAPIPacket")
        http_method = str(http_method).lower()
        response = ""
        logging.info("Send to api url: %s" % (url))

        ##HTTP Get
        if http_method == "get":
            time.sleep(sleep)
            ##Send get request directly
            logging.info("Send get request directly")
            response = requests.request("GET",url, headers=headers, data=data, params=url_param,files=files)
        ##HTTP Delete
        elif http_method == "delete":
            time.sleep(sleep)
            ##Send delete request directly
            logging.info("Send delete request directly")
            response = requests.request("DELETE",url, headers=headers)
            
        #HTTP POST
        elif http_method == "post":
            time.sleep(sleep)
            ##Send Post request directly
            logging.info("Send Post request directly")
            response = requests.request("POST",url, headers=headers, data=data, params=url_param, files=files)

        #HTTP PUT
        elif http_method == "put":
            time.sleep(sleep)
            ##Send Put request directly
            logging.info("Send Put request directly")
            response = requests.request("PUT",url, headers=headers, data=data)
        else:
            logging.error("!!!!Please check your http_method!!!!")

        #Record API Spent time
        logging.info("Response Time = %s" %response.elapsed.total_seconds())
        logging.info("End APIController SendAPIPacket")
        return response