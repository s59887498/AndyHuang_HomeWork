import logging
import time

from .Elements import *
from Method.base import *


class Module:

    # 圖片文字比對&Pytest功能區
    # ====================================================================================================
    def Screenshot_ele_multiple(self, eleName, name, times):
        times_image = 1
        ele, dealError = GetElement(eleName)
        while True:
            scroll_amount_times = int(ele.size['height']) * times_image
            Screenshot_ele(eleName, name + "-Part-" + str(times_image))
            if times_image >= times:
                break
            else:
                JavaScript("window.scrollTo(0,-document.body.scrollHeight)")
                Swipe_Down(eleName, scroll_amount_times)
                time.sleep(1)
                times_image += 1

    def Pytest_status(self, status):
        if status == 'fail':
            pytest.fail("Test failed because condition is not met")
        elif status == 'skip':
            pytest.skip("Test skiped because condition is not met")
        elif status == 'expected':
            raise Exception('Test expected because condition is not met')
        else:
            pass

    def ImageChops_difference_not_have_report(self, filename, filename_02):
        screenshot_img = Image.open(os.path.join(imageDict(), filename + GetTimeStr() + '.png'))
        screenshot_img_V2 = Image.open(os.path.join(imgDict(), filename_02 + '.png'))

        # 計算兩張圖片的哈希值
        hash1 = imagehash.average_hash(screenshot_img)
        hash2 = imagehash.average_hash(screenshot_img_V2)

        print(hash1)
        print(hash2)
        if hash1 == hash2:
            difference = "same"
            Allure_Text(filename + ' is ' + difference)
        else:
            difference = "error"
            Allure_Text(filename + ' is ' + difference)
            pytest.assume(False, "此測項文字比對有錯誤，請查看")

        return difference

    def ImageChops_difference(self, eleName, filename, filename_02):
        image = Screenshot_scroll_combination(eleName, filename)
        Allure(image)
        path_source = os.path.join(imageDict(), filename + GetTimeStr() + '.png')
        path_template = os.path.join(imgDict(), filename_02 + '.png')

        source_image = cv2.imread(path_source)
        template_image = cv2.imread(path_template)

        # 計算阈值
        result = cv2.matchTemplate(source_image, template_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        threshold = 0.999  # 设置阈值
        if max_val > threshold:
            difference = "same"
            Allure_Text(filename + ' is ' + difference)
        else:
            source_gray = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)
            target_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)
            difference = cv2.absdiff(source_gray, target_gray)
            _, thresholded = cv2.threshold(difference, 30, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(source_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            Error_filename = os.path.join(imageDict(), 'error_img.png')
            Error_name = str(filename + '圖片比對上有差異請查看截圖')
            Right_name = str(filename + '正確的圖片如圖')
            cv2.imwrite(Error_filename, source_image)
            allure.attach.file(Error_filename, attachment_type=allure.attachment_type.PNG, name=Error_name)
            allure.attach.file(path_template, attachment_type=allure.attachment_type.PNG, name=Right_name)
            difference = "error"
            pytest.assume(False, "此測項文字比對有錯誤，請查看")
        return difference

    def Text_Comparison(self, ele01, data_value):
        Text = WaitGetText(ele01)
        Text_V1 = data[data_value]
        differ = difflib.Differ()
        diff = differ.compare(Text.splitlines(), Text_V1.splitlines())

        if Text == Text_V1:
            difference = "same"
        else:
            difference = "error"
            Allure_Text_Body(data_value + ' is ' + difference + ' !!!!!!!!!!!!!!!!!!!!!!!!!!',
                             "[Web] is :\n" + Text + "\n[Data] is :\n" + Text_V1 + "\n差異在:\n" + '\n'.join(diff))
            pytest.assume(False, "此測項文字比對有錯誤，請查看")

        return difference

    # 比對文字用區
    # ====================================================================================================

    def compare_and_attach(self, text1, text2):
        # 将两个文本转换为列表形式，每行作为一个元素
        text1_lines = text1.splitlines(keepends=True)
        text2_lines = text2.splitlines(keepends=True)

        # 使用 difflib 模块比较两个文本的差异
        differ = difflib.Differ()
        diff = list(differ.compare(text1_lines, text2_lines))

        # 如果没有差异，则返回 None
        if not any(line.startswith(('+', '-', '?')) for line in diff):
            return None

        # 将差异的部分打印出来
        diff_text = ''.join(diff)
        return diff_text

    def Text_Difference(self, text1, text2):  # 確認文字是否有相符
        # 將字典轉換為字符串
        Text1_real_str = str(text1)  # 網頁上
        Text2_str = str(text2)  # 文件上

        diff_text = self.compare_and_attach(Text1_real_str, Text2_str)
        if diff_text:
            # 如果有差异，将差异部分添加到 allure 报告中
            print('比对失敗！詳情看內容。')
            allure.attach(body=diff_text,
                          name='比对失敗，顯示差異结果',
                          attachment_type=allure.attachment_type.TEXT)
            allure.attach(body='网页上: \n' + Text1_real_str + '\n文件上: \n' + Text2_str,
                          name='比對失敗！詳情看內容！',
                          attachment_type=allure.attachment_type.TEXT)
            pytest.assume(False, "此測項文字比對有錯誤，請查看")
        else:
            # 如果没有差异，直接在控制台打印比对成功的信息
            print('比对完成！没有发现差异。')
            allure.attach(body='网页上: \n' + Text1_real_str + '\n文件上: \n' + Text2_str,
                          name='比對成功！詳情可看內容！',
                          attachment_type=allure.attachment_type.TEXT)

    def Text_in_Difference(self, text1, text2):  # 確認文字是否有"包含"在裡面
        # 將字典轉換為字符串
        Text1_real_str = str(text1)
        Text2_str = str(text2)

        if Text2_str not in Text1_real_str:
            # 如果有差异，将差异部分添加到 allure 报告中
            print('比对包含失敗！詳情看內容。')
            allure.attach(body='网页上: \n' + Text1_real_str + '\n文件上: \n' + Text2_str,
                          name='比對包含失敗！詳情看內容！',
                          attachment_type=allure.attachment_type.TEXT)
            pytest.assume(False, "此測項文字比對有錯誤，請查看")
        else:
            # 如果没有差异，直接在控制台打印比对成功的信息
            print('比对包含完成！没有发现差异。')
            allure.attach(body='网页上: \n' + Text1_real_str + '\n文件上: \n' + Text2_str,
                          name='比對包含成功！詳情可看內容！',
                          attachment_type=allure.attachment_type.TEXT)

    def Text_not_in_Difference(self, text1, text2):  # 確認文字是否沒有"包含"在裡面
        # 將字典轉換為字符串
        Text1_real_str = str(text1)
        Text2_str = str(text2)

        if Text2_str in Text1_real_str:
            # 如果有差异，将差异部分添加到 allure 报告中
            print('比对不包含失敗！詳情看內容。')
            allure.attach(body='网页上: \n' + Text1_real_str + '\n文件上: \n' + Text2_str,
                          name='比對不包含失敗！詳情看內容！',
                          attachment_type=allure.attachment_type.TEXT)
            pytest.assume(False, "此測項文字比對不該包含，請查看")
        else:
            # 如果没有差异，直接在控制台打印比对成功的信息
            print('比对不包含完成！没有发现差异。')
            allure.attach(body='网页上: \n' + Text1_real_str + '\n文件上: \n' + Text2_str,
                          name='比對不包含成功！詳情可看內容！',
                          attachment_type=allure.attachment_type.TEXT)

    # 前台功能模組區
    # ====================================================================================================

    def dogcatstar_check_login(self, username):
        # ---確認有無登入---
        Enter_Url(env('Url') + "/my-account/")
        # ------取網頁上的值------
        web_text = WaitGetText(['Profile', 'My_Username_Text'])
        # ---取Yaml的值---
        logging.info("網頁顯示用戶名稱是:" + web_text)
        user_account = username

        # ---比對文字---
        Text_Difference(web_text, user_account)
        time.sleep(3)
        Screenshot('登入後畫面截圖')  # 截圖有沒有登入成功

    def dogcatstar_add_cart_check(self, product_name):
        # ---前往商品頁---
        Enter_Url(env('Url') + "/product/hairball_relief_lickable/")
        time.sleep(5)
        # ------click color_2------
        WaitClickEle(['Product', 'hairball_relief_lickable_color_1'])
        time.sleep(3)

        # ------add cart------
        WaitClickEle(['Product', 'Add_cart_button'])
        time.sleep(2)
        Screenshot('加入成功後的截圖')  # 截圖有沒有加入成功
        Enter_Url(env('Url') + "/cart/")

        # ------取網頁上的值------
        web_text = WaitGetText(['Cart', 'Product1_Name'])
        # ---取Yaml的值---
        logging.info("商品顯示名稱是:" + web_text)
        user_account = product_name

        # ---比對文字---
        Text_Difference(web_text, user_account)
        time.sleep(3)
        Screenshot('加入後購物車的截圖')  # 截圖有沒有加入成功

        # ---如果加入購物車，幫忙刪除舊的---
        WaitClickEle(['Cart', 'Delete_Card_product1'])


# Module()
# ====================================================================================================
mod = Module()
Screenshot_ele_multiple = mod.Screenshot_ele_multiple
Pytest_status = mod.Pytest_status
Text_Difference = mod.Text_Difference
Text_in_Difference = mod.Text_in_Difference
ImageChops_difference = mod.ImageChops_difference
Text_Comparison = mod.Text_Comparison
dogcatstar_check_login = mod.dogcatstar_check_login
ImageChops_difference_not_have_report = mod.ImageChops_difference_not_have_report
Text_not_in_Difference = mod.Text_not_in_Difference
dogcatstar_add_cart_check = mod.dogcatstar_add_cart_check