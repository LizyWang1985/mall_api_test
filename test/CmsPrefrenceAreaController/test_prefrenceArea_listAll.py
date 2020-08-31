import unittest
import requests
import json
import sys
sys.path.append("../..")  # 提升2级到项目根目录下
from mall_api_test.test.case.basecase import *
from mall_api_test.config.config import *

'''
CmsPrefrenceAreaController商品优选管理
/prefrenceArea/listAll
获取所有商品优选
'''
class TestPrefrenceArea_listAll(BaseCase):
    @classmethod
    def setUpClass(cls):
        BaseCase.write_token(cls)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_PrefrenceArea_listAll(self):
        response = requests.get(url=url+'/prefrenceArea/listAll',headers={"Authorization":BaseCase.read_token(self)})
        result = json.loads(response.text)
        print(result)
        self.assertEqual(result['message'],'操作成功')
        self.assertEqual(result['data'][0]['id'],1)
        self.assertEqual(response.status_code,200)

if __name__ == '__main__':
    unittest.main(verbosity=2)