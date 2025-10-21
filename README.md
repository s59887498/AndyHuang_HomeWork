# Fusion
## Directory Structure

---
### UI架構
```
|____data                           //The data for testing is stored
|____img                            //Store images for comparison.
|____tests                          //Test scripts folder by product
    |____   Web                     //Environment 001
    |____   xxx                     //Environment 002
            |____ Base.py           //Managing its setup and teardown for tests
            |____ Elements.py       //Store functions for clicking and other related features
            |____ Module.py         //Store repetitive actions such as login and logout.
            |____ test_xxx.py       //Test script
```
---
### API架構
```
|____Config                     //Feature configuration and pre-condition
|____Core                       //Core API method folder
|____Library                    //Public library folder
|____Method                     //Logic and data processing method
```
---
### 共用項目架構
```
|____Readme.md                      //help
|____pytest.ini                     //Pytest setting configuration
|____requirements                   //Pip install library
```

---

## Python Version
`Python = 3.9.6`

---

## Install Library before test
`pip3 install -r requirements.txt`

---

## Run Test Command Line
`python3 -m pytest`

---

## TestReport To Html (It is on https://test.pypi.org/)
`pip install -i https://test.pypi.org/simple/ TestReportBaifu`

or

`pip3 install -i https://test.pypi.org/simple/ TestReportBaifu`

---
## Allure Report 
`--alluredir=./result`


## TestReport To Html (allure Report)
`allure generate ./result --clean`

