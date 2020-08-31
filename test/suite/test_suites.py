import unittest
import sys
sys.path.append("../..")
from mall_api_test.test.CmsPrefrenceAreaController import TestPrefrenceArea_listAll
from mall_api_test.test.CmsSubjectController import TestSubjectList
from mall_api_test.test.PmsBrandController import Test_BrandCreate


smoke_suite = unittest.TestSuite() # 自定义的TestSuite
smoke_suite.addTests([TestPrefrenceArea_listAll('test_PrefrenceArea_listAll'),TestSubjectList('test_Subject_List_normal_keywordIsExists'),Test_BrandCreate('test_brand_create')])

def get_suite(suite_name): # 获取TestSuite方法
    return globals().get(suite_name)