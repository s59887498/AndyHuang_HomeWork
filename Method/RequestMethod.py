#!/usr/bin/python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import json

def FromHeaderGetCookie(Resp):#NB後台提取cookies
    Cookie = json.loads(json.dumps(dict(Resp.headers)))["Set-Cookie"]
    return Cookie

def FromHeaderGetToken(Resp):#NB後台提取token
    Token = json.loads(json.dumps(dict(Resp.headers)))["Auth-Token"]
    return Token



