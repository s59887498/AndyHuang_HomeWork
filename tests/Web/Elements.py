import os, logging, yaml, time, allure , cv2 ,numpy as np ,difflib
import pytest, sys, random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as AC
from PIL import Image
import imagehash
from io import BytesIO

class Elements:

    def __init__(self):
        '''啟動時自動導入'''
        self.LoadData()

    def InIDiver(self, driver):
        '''透過外部參數導入 driver'''
        self.driver = driver

    def LoadData(self):
        '''读取指定目录下的 backend.yaml 和 Frontend.yaml，并合并数据'''

        # 创建一个空字典用于存储所有数据
        all_data = {}

        paths = [
            os.path.abspath(os.path.join(os.getcwd(), 'data', 'Web', 'backend.yaml')),
            os.path.abspath(os.path.join(os.getcwd(), 'data', 'Web', 'Frontend.yaml'))
        ]

        for path in paths:
            try:
                with open(path, encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    # 合并数据到all_data字典中
                    all_data.update(data)
            except FileNotFoundError:
                continue  # 如果文件不存在，继续下一个文件的搜索
            except yaml.YAMLError as e:
                logging.error(e)
                break  # 如果在读取过程中出现了错误，就退出循环

        if not all_data:
            logging.error("未找到 backend.yaml 或 Frontend.yaml")
            raise FileNotFoundError("未找到 backend.yaml 或 Frontend.yaml")

        # 将合并后的数据赋值给 self.elementsData
        self.elementsData = all_data

    def data_yaml(self):
        '''讀取指定目錄下的 data.yaml'''
        yaml_path = os.path.abspath(os.path.join(os.getcwd(), "data", "Web", "data.yaml"))
        with open(yaml_path, encoding="utf-8") as f:
            try:
                data = yaml.safe_load(f)
            except yaml.YAMLError as e:
                logging.error(e)
        return yaml_path, data

    def loading_yaml(self, filename):
        '''讀取指定目錄下的yaml'''
        yaml_path = os.path.abspath(os.path.join(os.getcwd(), "data", "Language", filename))
        with open(yaml_path, encoding="utf-8") as f:
            try:
                value = yaml.safe_load(f)
            except yaml.YAMLError as e:
                logging.error(e)
        return value

    def dump_yaml(self, filename, ele, data):
        '''寫入指定目錄下的yaml（指定某個值調整)'''
        yaml_path = os.path.abspath(os.path.join(os.getcwd(), "data", "Web", filename))
        ele_name_str1 = ele[0]
        ele_name_str2 = ele[1]
        ele_name_str3 = ele[2]

        try:
            with open(yaml_path, 'r', encoding="utf-8") as f:
                yaml_data = yaml.safe_load(f)

            # 检查是否成功加载了数据
            if not yaml_data:
                raise ValueError("Failed to load YAML data")

            # 修改数据
            yaml_data[ele_name_str1][ele_name_str2][ele_name_str3] = data

            print(yaml_data)
            with open(yaml_path, 'w', encoding="utf-8") as f:
                # 写入数据到 YAML 文件
                yaml.dump(yaml_data, f)
                self.elementsData[ele_name_str1][ele_name_str2][ele_name_str3] = data

        except FileNotFoundError:
            logging.error(f"File {filename} not found")
        except yaml.YAMLError as e:
            logging.error(f"Error in YAML processing: {e}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

    def env(self, url):
        '''讀取指定目錄下的 env.yaml'''
        config_path = os.path.abspath(os.path.join(os.getcwd(), "data", "env.yaml"))
        with open(config_path, encoding="utf-8") as f:
            try:
                env = yaml.safe_load(f)[url]
            except yaml.YAMLError as e:
                logging.error(e)
        return env
    
    def imageDict(self):
        imageDict = os.path.abspath(os.path.join(os.getcwd(), "image"))
        if not os.path.isdir(imageDict):
            os.mkdir(imageDict)
        return imageDict

    def imgDict(self): #要拿來圖片比對的路徑
        imgDict = os.path.abspath(os.path.join(os.getcwd(), "img"))
        if not os.path.isdir(imgDict):
            os.mkdir(imgDict)
        return imgDict
# selenium element trigger 
# ====================================================================================================
    def ClickEle(self, eleName, img=True):
        '''click'''
        ele, dealError, ele_info = self.GetElement(*eleName)  # 取得元素
        sleepTime = ele_info['time']  # 取得sleep time

        if ele is None: # GetEleExceptionEle = None 時觸發
            if dealError == True:
                self.dealError('ClickEle', eleName, img)
            else:
                # 出現此錯誤訊息代表 GetEleExceptionEle 找不到此一物件，或是 type or value 設定錯誤
                logging.error(f'{eleName}，is None')
                return None
        else:
            try:
                ele.click()
                time.sleep(int(sleepTime))
                logging.info(f'{eleName} - ClickEle Success')
            except Exception as e:
                self.exc('ClickEle', eleName, e, img)

    def WaitClickEle(self, eleName, img=True):
        '''隱式等待 + click'''
        ele, dealError,  = self.GetEleExceptionEle(*eleName)

        if ele is None: # GetEleExceptionEle = None 時觸發
            if dealError == True:
                self.dealError('WaitClickEle', eleName, img)
            else:
                # 出現此錯誤訊息代表 GetEleExceptionEle 找不到此一物件，或是 type or value 設定錯誤
                logging.error(f'{eleName}，is None')
                return None
        else:
            try:
                # click Success 時觸發
                ele.click()
                time.sleep(1)
                logging.info(f'{eleName} - WaitClickEle Success')
            except Exception as e:
                Screenshot('有找到物件但無法點擊，請查看')
                self.exc('WaitClickEle', eleName, e, img)


    def GetText(self, eleName, img=True):
        '''GetText'''
        ele, dealError = self.GetEleExceptionEle(*eleName)
        if ele is None: # GetEleExceptionEle = None 時觸發
            if dealError == True:
                self.dealError('GetText', eleName, img)
            else:
                # 出現此錯誤訊息代表 GetEleExceptionEle 找不到此一物件，或是 type or value 設定錯誤
                logging.error(f'{eleName}，is None')
                return None
        else:
            try:
                return ele.text
            except Exception as e:
                self.exc('GetText', eleName, e, img)
            
    def WaitGetText(self, eleName, img=True):
        '''隱式等待 + GetText'''
        ele, dealError = self.GetEleExceptionEle(*eleName)
        if ele is None: # GetEleExceptionEle = None 時觸發
            if dealError == True:
                self.dealError('WaitGetText', eleName, img)
            else:
                # 出現此錯誤訊息代表 GetEleExceptionEle 找不到此一物件，或是 type or value 設定錯誤
                logging.error(f'{eleName}，is None')
                return None
        else: # 有抓到 value
            try: # 嘗試回傳 value
                logging.info(f'eleName = {eleName} ,text = {str(ele.text)} - WaitGetText Success')
                return str(ele.text.rstrip())
            except Exception as e:
                self.exc('WaitGetText', eleName, e, img)

    def WaitGetAttribute(self, eleName, value='placeholder', img=True):
        '''隱式等待 + get_attribute'''
        ele, dealError = self.GetEleExceptionEle(*eleName)
        if ele is None: # GetEleExceptionEle = None 時觸發
            if dealError == True:
                self.dealError('WaitGetAttribute', eleName, img)
            else:
                # 出現此錯誤訊息代表 GetEleExceptionEle 找不到此一物件，或是 type or value 設定錯誤
                logging.error(f'{eleName}，is None')
                return None
        else: # 有抓到 value
            try: # 嘗試回傳 value
                placeholder_value = ele.get_attribute(value)
                logging.info(f'eleName = {eleName} ,text = {str(placeholder_value)} - WaitGetText Value')
                return str(placeholder_value)
            except Exception as e:
                self.exc('WaitGetAttribute', eleName, e, img)

    def WaitGetAllText(self, eleName, img=True):
        '''隱式等待 + GetAllText(這個元素撈出來的全部文字)'''
        eles, dealError = self.GetElesExceptionEles(*eleName)
        if eles is None: # GetEleExceptionEle = None 時觸發
            if dealError == True:
                self.dealError('WaitGetAllText', eleName, img)
            else:
                # 出現此錯誤訊息代表 GetEleExceptionEle 找不到此一物件，或是 type or value 設定錯誤
                logging.error(f'{eleName}，is None')
                return None
        else:
            try:
                # 創建一個空字典來存放元素的文字內容，以及它們的索引
                element_texts_dict = {}
                print("元素數量:", len(eles))
                # 遍歷每個元素，並將具有 'text' 屬性的元素的文字內容與索引添加到字典中
                for index, element in enumerate(eles):
                    if hasattr(element, 'text'):
                        text = element.text
                        # 如果文字是空值，則將鍵名更改為 "空值"
                        if text == "":
                            text = None
                        element_texts_dict[index] = text

                logging.info('撈出的文字是：' + str(element_texts_dict))
                return element_texts_dict, len(eles)
            except Exception as e:
                self.exc('GetText', eleName, e, img)

    def SendKey_Ele(self, eleName, data, img=True):
        '''send_keys'''
        ele, dealError = self.GetEleExceptionEle(*eleName)  # 取得元素

        if ele is None: # GetEleExceptionEle = None 時觸發
            if dealError == True:
                self.dealError('SendKey_Ele', eleName, img)
            else:
                # 出現此錯誤訊息代表 GetEleExceptionEle 找不到此一物件，或是 type or value 設定錯誤
                logging.error(f'{eleName}，is None')
                return None 
        else:
            try:
                ele.clear()
                ele.send_keys(data)
                time.sleep(1)
            except Exception as e:
                self.exc('SendKey_Ele', eleName, e, img)

    def WaitSendEle(self, eleName, keyList=[], img=True):
        '''隱式等待 + send_keys(一個一個字送出)'''
        ele, dealError = self.GetEleExceptionEle(*eleName)
        if ele is None: # GetEleExceptionEle = None 時觸發
            if dealError == True:  
                self.dealError('WaitSendEle', eleName, img)
            else:
                # 出現此錯誤訊息代表 GetEleExceptionEle 找不到此一物件，或是 type or value 設定錯誤
                logging.error(f'{eleName}，is None')
                return None
        else:
            try:
                # send_keys Success 時觸發
                ele.clear()
                for keyStr in keyList:
                    ele.send_keys(keyStr)
                    logging.info(f'eleName = {eleName}，keyStr = {str(keyStr)} + WaitSendEle Success')
            except Exception as e:
                self.exc('WaitSendEle', eleName, e, img)

    def WaitSelectEle(self, eleName, by, obj, img=True):
        '''控制網頁的 Select 標籤'''
        ele, dealError = self.GetEleExceptionEle(*eleName)  # 取得元素
        sleepTime = 5  # 取得sleep time

        if ele is None: # GetEleExceptionEle = None 時觸發
            if dealError == True:
                self.dealError('SelectEle', eleName, img)
            else:
                # 出現此錯誤訊息代表 GetEleExceptionEle 找不到此一物件，或是 type or value 設定錯誤
                logging.error(f'{eleName}，is None')
                return None
        else:
            try:
                if by == "index":
                    Select(ele).select_by_index(obj)
                    time.sleep(int(sleepTime))
                elif by == "value":
                    Select(ele).select_by_value(obj)
                    time.sleep(int(sleepTime))
                elif by == "text":
                    Select(ele).select_by_visible_text(obj)
                    time.sleep(int(sleepTime))
            except Exception as e:
                self.exc('SelectEle', eleName, e, img)

    def Clear_Ele(self, eleName, img=True):
        '''清除該物件的內容'''
        ele, dealError, ele_info = self.GetElement(*eleName)  # 取得元素
        sleepTime = ele_info['time']  # 取得sleep time

        if ele is None: # GetEleExceptionEle = None 時觸發
            if dealError == True:
                self.dealError('Clear_Ele', eleName, img)
            else:
                # 出現此錯誤訊息代表 GetEleExceptionEle 找不到此一物件，或是 type or value 設定錯誤
                logging.error(f'{eleName}，is None')
                return None
        else:
            try:
                ele.clear()
                logging.info(f'{eleName} - Clear_Ele Success')
                time.sleep(sleepTime)
            except Exception as e:
                self.exc('Clear_Ele', eleName, e, img)
            
    def Clear_Ele_By_Keys(self, eleName, keyList=[Keys.CONTROL+'a'+Keys.DELETE], img=True):
        '''隱式等待 + keyList=[Keys.CONTROL+'a'+Keys.DELETE]'''
        ele, dealError = self.GetEleExceptionEle(*eleName)
        if ele is None: # GetEleExceptionEle = None 時觸發
            if dealError == True:  
                self.dealError('Clear_Ele_By_Keys', eleName, img)
            else:
                # 出現此錯誤訊息代表 GetEleExceptionEle 找不到此一物件，或是 type or value 設定錯誤
                logging.error(f'{eleName}，is None')
                return None
        else:
            try:
                # send_keys Success 時觸發
                ele.clear()
                for keyStr in keyList:
                    ele.send_keys(keyStr)
                    time.sleep(1)
                    logging.info(f"eleName = '+ {eleName} +'，keyStr = '+ {str(keyStr)} + ' - Clear_Ele_By_Keys Success")
            except Exception as e:
                self.exc('Clear_Ele_By_Keys', eleName, e, img)
            
    def exc(self, module, eleName, e, img):
        '''該 Module 沒有正常執行！'''
        if img == True:
            self.screenshot_local(f'{module} - {eleName} - except')
        logging.error(f'{module} - {eleName} - {e}，except！')
        raise Exception(f'{module} - {eleName}，except！')
    
    def dealError(self, module, eleName, img):
        '''dealError == True'''
        if img == True:
            self.screenshot_local(f'{module} - {eleName} - dealError')
        logging.error(f'{module} - {eleName}，dealError！')
        raise Exception(f'{module} - {eleName}，dealError！')

    def actions_click(self, eleName):
        ele, dealError = self.GetEleExceptionEle(*eleName)
        actions = AC(self.driver)
        actions.click(ele)
        actions.perform()
        time.sleep(1)
        logging.info(f'{eleName} - actions_click Success')

    def actions_move(self, eleName):
        ele, dealError = self.GetEleExceptionEle(*eleName)
        actions = AC(self.driver)
        actions.move_to_element(ele)
        actions.perform()
        time.sleep(1)
        logging.info(f'{eleName} - actions_move Success')

    def actions_move_click(self, eleName):
        ele, dealError = self.GetEleExceptionEle(*eleName)
        actions = AC(self.driver)
        actions.move_to_element(ele).click()
        actions.perform()
        time.sleep(1)
        logging.info(f'{eleName} - actions_move_click Success')

    def actions_by_offset_click(self, x, y, left_click=True):
        actions = AC(self.driver)

        if left_click:
            actions.move_by_offset(x, y).click().perform()
        else:
            actions.move_by_offset(x, y).context_click().perform()

        actions.move_by_offset(-x, -y).perform()  # 將滑鼠位置恢復到移動前
        logging.info(f'{x},{y} - actions_by_offset_click Success')
    
# selenium element read 
# ====================================================================================================
    def GetElesExceptionEles(self, *ele_name, sleep_time=5):
        '''隱式等待 + 讀取多個物件設定(elements)'''
        try:
            try:
                ele_info = self.elementsData
                for arg in ele_name:
                    ele_info = ele_info[arg]
            except (KeyError, TypeError, IndexError):
                # 如果在elementsData中找不到對應的值，或者試圖對非字典類型的對象進行索引，則拋出異常
                raise KeyError("Element '{}' not found in elementsData".format(ele_name))

            ele_type = ele_info['type']
            ele_value = ele_info['value']
            deal_error = ele_info.get('dealError', False)
        except KeyError:
            logging.error(f"{ele_name} Incorrect setting!")
            raise Exception(f"{ele_name} Incorrect setting!")

        try:
            locator_dict = {"id":By.ID, "xpath":By.XPATH, "link":By.LINK_TEXT, "partial":By.PARTIAL_LINK_TEXT, "name":By.NAME, "tag":By.TAG_NAME, "class":By.CLASS_NAME, "css":By.CSS_SELECTOR}
            elements = WDW(self.driver, sleep_time).until(EC.presence_of_all_elements_located((locator_dict[ele_type], ele_value)))
            return elements, deal_error
        except Exception as e:
            logging.error(f"{ele_name} - {str(e)}")
            return None, deal_error

    def GetEleExceptionEle(self, *ele_name, sleep_time=10):
        '''隱式等待 + 讀取物件設定(element)'''
        try:
            try:
                ele_info = self.elementsData
                for arg in ele_name:
                    ele_info = ele_info[arg]
            except (KeyError, TypeError, IndexError):
                # 如果在elementsData中找不到對應的值，或者試圖對非字典類型的對象進行索引，則拋出異常
                raise KeyError("Element '{}' not found in elementsData".format(ele_name))

            ele_type = ele_info['type']
            ele_value = ele_info['value']
            deal_error = ele_info.get('dealError', False)
        except KeyError:
            logging.error(f"{ele_name} Incorrect setting!")
            raise Exception(f"{ele_name} Incorrect setting!")

        try:
            locator_dict = {"id":By.ID, "xpath":By.XPATH, "link":By.LINK_TEXT, "partial":By.PARTIAL_LINK_TEXT, "name":By.NAME, "tag":By.TAG_NAME, "class":By.CLASS_NAME, "css":By.CSS_SELECTOR}
            element = WDW(self.driver, sleep_time).until(EC.presence_of_element_located((locator_dict[ele_type], ele_value)))
            return element, deal_error
        except Exception as e:
            logging.error(f"{ele_name} - {str(e)}")
            return None, deal_error

    def GetElement(self, *ele_name):
        '''讀取物件設定(element)'''
        try:
            try:
                ele_info = self.elementsData
                for arg in ele_name:
                    ele_info = ele_info[arg]
            except (KeyError, TypeError, IndexError):
                # 如果在elementsData中找不到對應的值，或者試圖對非字典類型的對象進行索引，則拋出異常
                raise KeyError("Element '{}' not found in elementsData".format(ele_name))

            ele_type = ele_info['type']
            ele_value = ele_info['value']
            deal_error = ele_info.get('dealError', False)
        except KeyError:
            logging.error(f"{ele_name} Incorrect setting!")
            raise Exception(f"{ele_name} Incorrect setting!")

        try:
            locator_dict = {"id":By.ID, "xpath":By.XPATH, "link":By.LINK_TEXT, "partial":By.PARTIAL_LINK_TEXT, "name":By.NAME, "tag":By.TAG_NAME, "class":By.CLASS_NAME, "css":By.CSS_SELECTOR}
            element = self.driver.find_element(locator_dict[ele_type], ele_value)
            return element, deal_error, ele_info
        except Exception as e:
            logging.error(f"{ele_name} - {str(e)}")
            return None, deal_error
              
# function element
# ====================================================================================================
    def JavaScript(self,js):
        '''透過 driver，讓 browser 執行 JS 指令'''
        self.driver.execute_script(js)
        logging.info('script = '+ '\n'+js + '\n- execute_script Success')

    def JS_Click(self, css):
        self.driver.execute_script("document.querySelector('{}').click()".format(css))
        logging.info('JS_Click = '+ css + ' - JS_Click Success')
    
    def JS_Value(self, css, value):
        self.driver.execute_script("document.querySelector('{}').value = '{}'".format(css, value))
        logging.info('JS_Value = '+ css + ' - JS_Value Success')

    def SwitchWindow(self, index, sleepTime=2):
        '''所有視窗 ID + 當前視窗 ID + 切換視窗'''
        try:
            handles = self.driver.window_handles
            logging.info('window_handles = ' + str(handles)+'\n')
            logging.info('current_window_handle = ' + str(self.driver.current_window_handle))
            logging.info('title = ' + str(self.driver.title))
            logging.info('current_url = ' + str(self.driver.current_url)+'\n')
            self.driver.switch_to.window(str(handles[index]))
            logging.info('switch_to.window = ' + str(self.driver.current_window_handle))
            logging.info('title = ' + str(self.driver.title))
            logging.info('current_url = ' + str(self.driver.current_url))
            time.sleep(sleepTime)
        
        except Exception as e:
            logging.error(str(e))

    def SwitchWindow_Url(self, correct_url, sleepTime=2):
        '''
        SwitchWindow 改良版本
        用於比對多個視窗的網址，是否為想要切換的視窗?
        如果是的話終止迴圈，不是的話繼續切換視窗直到找到符合的網址~
        '''
        try:
            handles = self.driver.window_handles
            logging.info('handles = '+str(handles)+'，len = '+str(len(handles))+'\n')
            for handle in handles:
                self.driver.switch_to.window(handle)
                index = list(handles).index(handle)
                time.sleep(sleepTime)
                if self.driver.current_url == correct_url:
                    logging.info('符合')
                    logging.info('handle = '+str(handle)+'，index = '+str(index))
                    logging.info('title = '+str(self.driver.title))
                    logging.info('current_url = '+str(self.driver.current_url)+'\n')
                    break
                else:
                    logging.info('不符合')
                    logging.info('handle = '+str(handle)+'，index = '+str(index))
                    logging.info('title = '+str(self.driver.title))
                    logging.info('current_url = '+str(self.driver.current_url)+'\n')
                if handle == handles[-1]: logging.warning('所有網址皆不符合！')
        
        except Exception as e:
            logging.error(str(e))

    def CloseWindow(self):
        '''關閉當前視窗'''
        self.driver.close()

    def MaximizeWindow(self):
        '''視窗最大化'''
        self.driver.maximize_window()

    def BackWin(self):
        '''上一頁'''
        self.driver.back()

    def ForwardWin(self):
        '''下一頁'''
        self.driver.forward()

    def screenshot_local(self, filename): # 半形: os.path.join會出錯
        '''截圖到 local'''
        filenameTime = os.path.join(self.imageDict(), filename + '.png')
        self.driver.get_screenshot_as_file(filenameTime)

    def screenshot_ele(self, filename, elename):
        '''截圖特定元素'''
        filenameTime = os.path.join(self.imageDict(), filename + '.png')
        screenshot_div = elename.screenshot_as_png
        img = Image.open(BytesIO(screenshot_div))
        img.save(filenameTime)


    def SwitchToFrame(self, num):
        '''切換框架至下一層(用於透過框架進行定位)'''
        self.driver.switch_to.frame(num)
        logging.info(f'SwitchToFrame = {num} - SwitchToFrame Success')

    def SwitchToParent(self):
        '''切換框架至上一層(用於透過框架進行定位)'''
        self.driver.switch_to.parent_frame()
        logging.info('SwitchToParent Success')

    def SwitchToDefault(self):
        '''切換到預設框架(主框架)'''
        self.driver.switch_to.default_content()
        logging.info('SwitchToDefault Success')

    def Allure(self, filename):
        '''Allure 上傳圖片'''
        filenameTime = os.path.join(self.imageDict(), filename +'.png')
        allure.attach.file(filenameTime, attachment_type=allure.attachment_type.PNG, name=filename)

    def Allure_Text(self, Text):
        '''Allure 上傳圖片'''
        allure.attach(body = '', name = Text, attachment_type=allure.attachment_type.TEXT)

    def Allure_Text_Body(self, Text, Body):
        '''Allure 上傳圖片'''
        allure.attach(body = Body, name = Text, attachment_type=allure.attachment_type.TEXT)

    def GET_CurUrl(self):
        '''回傳當前網址'''
        url = self.driver.current_url
        logging.info(f'current_url = {url}')
        return url

    def GET_Title(self):
        '''回傳當前 Title'''
        title = self.driver.title
        logging.info('title = ' + title)
        return title

    def GetTimeStr(self):
        '''取得當前日期'''
        time.sleep(1)
        now = time.strftime(r"_%Y-%m-%d")
        return now
    
    def Enter_Url(self, value):
        '''切換到指定網址'''
        try:
            self.driver.get(value)
            logging.info(value + ' - Enter_Url Success')
            time.sleep(4)
        except Exception as e:
            logging.error(value + ' - ' + str(e))

    def Refresh(self):
        '''重新整理頁面'''
        self.driver.refresh()
        logging.info('Refresh Success')

    def Screenshot(self, name):
        '''screenshot + Allure'''
        image = name + self.GetTimeStr()
        self.screenshot_local(image)
        self.Allure(image)
        logging.info(image + ' - Screenshot Success')

    def Screenshot_ele(self, eleName, name):
        '''screenshot元素 + Allure'''
        ele, dealError = self.GetEleExceptionEle(*eleName)
        image = name + self.GetTimeStr()
        self.screenshot_ele(image,ele)
        self.Allure(image)
        logging.info(image + ' - Screenshot Success')

    def is_displayed(self, eleName):
        '''判斷元素是否顯示'''
        try:
            ele, dealError = self.GetEleExceptionEle(*eleName)
            display = ele.is_displayed()
            logging.info(f'{eleName} - is_displayed ? {str(display)}')
            return display
        except Exception as e:
            logging.error(f'{eleName} - {str(e)}')
            return "No Display"
    
    def is_enabled(self, eleName):
        '''判斷元素是否可用'''
        try:
            ele, dealError = self.GetEleExceptionEle(*eleName)
            enabled = ele.is_enabled()
            logging.info(f'{eleName} - is_enabled ? {str(enabled)}')
            return enabled
        except Exception as e:
            logging.error(f'{eleName} - {str(e)}')
            return "No Enabled"

    def is_selected(self, eleName):
        '''判斷元素是否被選取'''
        try:
            ele, dealError = self.GetEleExceptionEle(*eleName)
            selected = ele.is_selected()
            logging.info(f'{eleName} - is_selected ? {str(selected)}')
            return selected
        except Exception as e:
            logging.error(f'{eleName} - {str(e)}')
            return "No Selected"


    def GoToWindow(self, url):
        '''開啟當前視窗'''
        try:
            self.driver.get(url)
            logging.info(f'{url}，GoToWindow Success')
        except Exception as e:
            logging.error(str(e))

    def Swipe_Down(self, eleName,scrollamount):
        '''網頁滑動'''
        ele, dealError = self.GetEleExceptionEle(*eleName)  # 找到彈出式視窗中的固定 <div> 元素 > ele
        scroll_amount = scrollamount  # 設定滾動的像素數量
        self.driver.execute_script(f"arguments[0].scrollTop = {scroll_amount};", ele)
        logging.info('script Swipe_Down Success')

    def Screenshot_scroll_combination(self, eleName, filename, class_list):
        '''截圖整個滑動'''
        total_high = 0
        for class_name in class_list:
            element, dealError = self.GetEleExceptionEle(*class_name)  # 獲取元素
            if element:
                total_high += element.size['height']  # 加入元素高度
            else:
                print(f"Failed to load element: {class_name}, Error: {dealError}")
        total_high += 15  # 加上額外的偏移量
        logging.info(f"高度是：{total_high}")

        ele, dealError = self.GetEleExceptionEle(*eleName)  # 取得元素
        image = filename + self.GetTimeStr()
        filenameTime = os.path.join(self.imageDict(), image + '.png')
        scroll_amount = int(ele.size['height'])
        # 初始化 frequency 變數

        # 創建一個空的圖像對象，用於保存合併後的截圖
        combined_image = Image.new('RGB', (ele.size['width'], total_high))
        frequency = 1
        while True:
            # 截取 <div> 元素的畫面
            screenshot_data = ele.screenshot_as_png
            screenshot_img = Image.open(BytesIO(screenshot_data))
            lastheight = total_high - scroll_amount * frequency

            combined_image.paste(screenshot_img, (0, scroll_amount * (frequency - 1)))

            # 模擬滑動操作
            JavaScript("window.scrollTo(0,-document.body.scrollHeight)")
            Swipe_Down(eleName, scroll_amount * frequency)
            time.sleep(1)

            # 更新 frequency 變數
            frequency += 1
            print(f"lastheight:" + str(lastheight))
            print(f"scroll_amount:" + str(scroll_amount))
            print(f"frequency:" + str(frequency))
            # 檢查是否到達底部
            if lastheight <= scroll_amount:
                break
        # 儲存合併後的圖片
        screenshot_data = ele.screenshot_as_png
        screenshot_img = Image.open(BytesIO(screenshot_data))
        cropped_screenshot = screenshot_img.crop((0, screenshot_img.height - lastheight, screenshot_img.width, screenshot_img.height))
        combined_image.paste(cropped_screenshot, (0, total_high - lastheight))
        combined_image.save(filenameTime)
        logging.info(filenameTime + ' - Screenshot Success')
        return image


# Elements()
# ====================================================================================================
ele = Elements()
yaml_path, data = ele.data_yaml()
InIDiver = ele.InIDiver
loading_yaml = ele.loading_yaml
dump_yaml = ele.dump_yaml
env = ele.env
imageDict = ele.imageDict
imgDict = ele.imgDict
WaitClickEle = ele.WaitClickEle
ClickEle = ele.ClickEle
SendKey_Ele = ele.SendKey_Ele
GetText = ele.GetText
WaitGetAllText = ele.WaitGetAllText
eleScreenshot = ele.screenshot_local
SwitchToFrame = ele.SwitchToFrame
SwitchToParent = ele.SwitchToParent
SwitchToDefault = ele.SwitchToDefault
GET_CurUrl = ele.GET_CurUrl
WaitSendEle = ele.WaitSendEle
SwitchWindow = ele.SwitchWindow
CloseWindow = ele.CloseWindow
GoToWindow = ele.GoToWindow
WaitGetText = ele.WaitGetText
BackWin = ele.BackWin
WaitSelectEle = ele.WaitSelectEle
Allure = ele.Allure
Allure_Text = ele.Allure_Text
Allure_Text_Body = ele.Allure_Text_Body
GetElement = ele.GetElement
MaximizeWindow = ele.MaximizeWindow
GET_Title = ele.GET_Title
Enter_Url = ele.Enter_Url
JavaScript = ele.JavaScript
Refresh= ele.Refresh
GetTimeStr = ele.GetTimeStr
JS_Click = ele.JS_Click
JS_Value = ele.JS_Value
Clear_Ele = ele.Clear_Ele
actions_click = ele.actions_click
actions_move = ele.actions_move
actions_move_click = ele.actions_move_click
actions_by_offset_click = ele.actions_by_offset_click
Screenshot = ele.Screenshot
Screenshot_ele = ele.Screenshot_ele
Swipe_Down = ele.Swipe_Down
Screenshot_scroll_combination = ele.Screenshot_scroll_combination
elementsData = ele.elementsData
WaitGetAttribute = ele.WaitGetAttribute
is_displayed = ele.is_displayed
