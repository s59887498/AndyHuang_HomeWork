# -*- coding: UTF-8 -*-
import logging
import os

from .Base import *
from Core.APIQuery import *
from Method.CommonMethod import *
from Method.RequestMethod import *
from Method.base import *

case = os.path.basename(__file__)


class Test(Base):
    file = "CN.yaml"  # 在类级别定义 file 变量
    # ---前台登入的帳號密碼從這邊設定---
    Frontend_Username = data['username_automation']

    @allure.title(case)
    # 整個.py測試前執行程式碼，執行 Login
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, newDriver):
        logging.info("setup_class: 整個.py測試前執行程式碼")

    @staticmethod
    def teardown_method():
        logging.info("teardown_method: 每个用例结束后执行")

    def test_login_and_add_cart(self, newDriver):
        """
        確認NB登入頁文字是否正確，拿來當範例參考用
        """

        allure.attach.file(yaml_path, 'data', allure.attachment_type.YAML)
        logging.info('starting ' + case)

        # ---確認登入---
        dogcatstar_check_login(self.Frontend_Username)

        # ---商品加入購物車---
        dogcatstar_add_cart_check("汪喵星球 排毛保健純肉泥｜保健肉泥")

        # ---程式跑完截圖---
        Screenshot("Case結束後畫面驗證截圖：")

        logging.info('end ' + case)


    if __name__ == '__main__':
        pytest.main(['-s', __file__])
