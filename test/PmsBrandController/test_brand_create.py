import unittest
import requests
import logging
from mall_api_test.test.case.basecase import *
from mall_api_test.lib.db import *
from mall_api_test.config.config import *
'''
响应：
{
  "code": 200,
  "message": "操作成功",
  "data": 1
}'''

#post数据准备
BRAND_DATA = {
  "bigPic": "https://gss0.baidu.com/7LsWdDW5_xN3otqbppnN2DJv/forum/pic/item/ac4bd11373f08202d0d7ea6d5cfbfbedab641b1e.jpg",
  "brandStory": "VIVO手机的品牌故事",
  "factoryStatus": 1,
  "firstLetter": "V",
  "logo": "https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=1180996836,1580132188&fm=26&gp=0.jpg",
  "name": "VIVO",
  "showStatus": 1,
  "sort": 0
}

class Test_BrandCreate(BaseCase):
    conn = DB()
    @classmethod
    def setUpClass(cls):
        pass
    @classmethod
    def tearDownClass(cls):
        pass


    def clear_brand(self,query_sql,delete_sql):
        if Test_BrandCreate.conn.query(query_sql) is not None:
            Test_BrandCreate.conn.exec(delete_sql)



    def test_brand_create(self):
        name = BRAND_DATA["name"]
        query_sql = 'SELECT * FROM pms_brand WHERE name="{}";'.format(name)
        delete_sql = 'DELETE  FROM pms_brand WHERE name="{}";'.format(name)
        # 删除数据库同名品牌数据
        self.clear_brand(query_sql,delete_sql)

        #添加品牌
        try:
            response = requests.post(url=url+'/brand/create',headers={"Authorization":BaseCase.read_token(self)},json=BRAND_DATA)
        except Exception as e:
            logging.error(e)
            pass

        log_case_info('test_brand_create',url+'/brand/create',BRAND_DATA,{"code":200,"message":"操作成功","data":1},response.text)
        #断言是否新增成功，检查数据库是否新增数据
        print(response.text)
        result = json.loads(response.text)
        print(result)
        self.assertEqual(response.status_code,200)#检查返回码是否200
        DB_Result=Test_BrandCreate.conn.query(query_sql)
        print(DB_Result)
        self.assertEqual(name,DB_Result[0][1])#检查数据库是否存在name的记录



if __name__ == '__main__':
    unittest.main(verbosity=2)


