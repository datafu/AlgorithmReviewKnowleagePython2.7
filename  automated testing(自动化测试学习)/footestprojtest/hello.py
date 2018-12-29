# -*- coding: utf-8 -*-
'''示例测试用例
'''
#2018/12/27 QTAF自动生成

# from footestprojlib.testcase import FootestprojTestCase
from testbase.testcase import TestCase
from calcu import string_combine


class HelloTest(TestCase):
    '''示例测试用例
    '''
    owner = "foo"
    status = TestCase.EnumStatus.Ready
    priority = TestCase.EnumPriority.Normal
    timeout = 1

    #测试环境的构造和初始化
    def pre_test(self):
        pass


    def run_test(self):
        # ---------------------------

        # ---------------------------
        self.start_step("测试字符串拼接")
        # ---------------------------
        result = string_combine("xxX", "yy")
        self.assert_("检查string_combine调用结果", result == "xxXyy")



    #保证清理环境 相当于finish
    def post_test(self):
        pass


if __name__ == '__main__':
    HelloTest().debug_run()

