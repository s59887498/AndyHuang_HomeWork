import allure
import inspect


def pytest_runtest_call(item):
    # 獲取當前測試函數
    test_func = item.function
    # 提取 docstring
    docstring = inspect.getdoc(test_func)
    if docstring:
        allure.dynamic.description(docstring)
