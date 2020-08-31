import unittest
import requests
import json
import sys
import logging
sys.path.append("../..")   # 统一将包的搜索路径提升到项目根目录下

from mall_api_test.lib.read_excel import *
from mall_api_test.lib.case_log import log_case_info
from mall_api_test.config.config import *
class BaseCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # if cls.__name__！="BaseCase":
        # cls.data_list=excel_to_list(data_file,cls.__name__)
        pass


    def write_token(self):
        '''将Token信息写入到token.md文件中'''
        data = {"username":"admin","password":"admin123"}
        response = requests.post(url=url+'/admin/login',json=data,headers={"Content-Type":"application/json;charset=UTF-8"})
        self.Makelog('日志跟踪：将token写入到Token.md文件中')
        with open('../../data/token.md','w') as f:
            Authorization = response.json()['data']['tokenHead']+response.json()['data']['token']
            f.write(Authorization)

    def read_token(self):
        '''读取Token信息'''
        # with open('os.path.join(data_path,"token.md")','r') as f:
        with open('../../data/token.md','r') as f:
            return f.read()

    def get_case_data(self,case_name):
        return get_test_data(self.data_list,case_name)

    def send_requests(self,case_data):
        case_name = case_data.get('case_name')
        url = case_data.get('url')
        data=case_data.get("data")
        headers = case_data.get('headers')
        expect_res = case_data.get('expect_res')
        method = case_data.get('method')
        data_type=case_data.get('data_type')

        if method.upper()=='GET':  #GET类型请求
            res=requests.get(url=url,params=json.loads(data))
        elif data_type.upper()=='FORM': #POST Form表单提交  lower()/upper(): 将字符串转换为全小写/大写
            res=requests.post(url=url,data=json.loads(data),headers=json.loads(headers))
            log_case_info(case_name,url,data,expect_res,res.text)
            self.assertEqual(res.text,expect_res)
        else:
            res=requests.post(url=url,json=json.loads(data),headers=json.loads(headers))  # JSON格式请求
            log_case_info(case_name,url,data,
                          json.dumps(json.loads(expect_res),sort_keys=True),
                          json.dumps(res.json(),ensure_ascii=False,sort_keys=True))
            self.assertDictEqual(res.json(),json.loads(expect_res))


