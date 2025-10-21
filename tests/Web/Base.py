import pytest
import platform
from selenium import webdriver
from pyvirtualdisplay import Display  # 上傳到linux時須設定虛擬螢幕
# ChromeService
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
# EdgeService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options as EdgeOptions
# FirefoxService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from .Module import *


class Base:

    @pytest.fixture(scope="module", autouse=True)
    def newDriver(self):
        system = platform.system()
        if system == "Linux":
            display = Display(visible=0, size=(2560, 1080))  # 上傳到linux時須設定虛擬螢幕 - 設定虛擬螢幕尺寸
            display.start()  # 上傳到linux時須設定虛擬螢幕 - 開啟虛擬螢幕

        op = ChromeOptions()
        # op = EdgeOptions()
        # op = FirefoxOptions()
        prefs = {"download.default_directory": os.path.abspath(r'.\tests\Web\files')}  # 指定到某一個下載路徑
        op.add_experimental_option("prefs", prefs)  # 加入額外設定參數
        user_dir = os.path.expanduser("~/selenium-profiles/dogcatstar")
        op.add_argument(f"--user-data-dir={user_dir}")
        # 若該資料夾下沒有其他 profile，預設就是 "Default"
        op.add_argument("--profile-directory=Default")

        # op.set_preference('browser.download.dir', os.path.abspath(r'.\tests\Web\files')) # 指定到某一個下載路徑 Firefox
        # op.add_argument("--incognito")  # 設定成以無痕視窗開啟瀏覽器 Chrome
        # op.add_argument("--inprivate")  # 設定成以無痕視窗開啟瀏覽器 Edge
        # op.add_argument("--private")  # 設定成以無痕視窗開啟瀏覽器 Firefox
        # op.add_argument("--headless")  # 不開啟實體瀏覽器在背景執行
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=op)

        # driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=op)
        # driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=op)

        # driver.set_window_size(430, 950)   # 設定瀏覽器尺寸
        driver.maximize_window()# 設定瀏覽器尺寸最大化
        driver.switch_to.window(driver.current_window_handle)  # 切換到當前視窗
        InIDiver(driver)
        GoToWindow(env('Url'))
        yield driver  # Case 結束後執行以下命令
        driver.quit()  # 關閉 driver
        # display.stop() #上傳到linux時須設定虛擬螢幕 - 關閉虛擬螢幕
        return driver  # 因為有多個 Case 要跑，所以要 return driver，否則跑下一個 Case 就會找不到 driver
