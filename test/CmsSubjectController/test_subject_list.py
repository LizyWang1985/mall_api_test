import unittest
import requests
import json
import logging
import sys
sys.path.append("../..")  # 提升2级到项目根目录下
from mall_api_test.test.case.basecase import *
from mall_api_test.config.config import *
from mall_api_test.lib.read_excel import *
from mall_api_test.lib.db import *

'''
CmsSubjectController商品专题管理
/subject/list
根据专题名称分页获取专题
curl -X GET "http://139.199.12.254/manager/subject/list?pageNum=1&pageSize=5" -H "accept: */*"

Parameters:
keyword   string
(query)	
pageNum
integer($int32)
(query)	

pageSize
integer($int32)
(query)
'''
class TestSubjectList(BaseCase):

    @classmethod
    def setUpClass(cls):
        BaseCase.write_token(cls)
        cls.data_list = excel_to_list(os.path.join(data_path,'mall_api_test.xlsx'),'TestSubjectList')#读取excel,TestSubjectLis工作薄的所有数据生成列表字典

    @classmethod
    def tearDownClass(cls):
        pass

    def Subject_List(self,case_name):
        case_data = get_test_data(self.data_list,case_name)
        if not case_data:
            logging.error('数据不存在')

        url =case_data.get('url')
        # keyword = case_data.get('keyword')
        # pageNum = case_data.get('pageNum')
        # pageSize = case_data.get('pageSize')
        # print(type(pageSize))
        #sql语句
        if not case_data.get('keyword') and not case_data.get('pageNum') and not case_data.get('pageSize') or  isinstance(case_data.get('pageNum'),str) or isinstance(case_data.get('pageSize'),str) :
            sql = 'SELECT title FROM cms_subject WHERE title '
            sql_total= 'SELECT count(title) FROM cms_subject WHERE title '
            print(sql)
        elif not case_data.get('keyword') and not case_data.get('pageNum') and isinstance(int(case_data.get('pageSize')),int) :
            pageSize = int(case_data.get('pageSize'))
            sql = 'SELECT title FROM cms_subject WHERE title  limit {};'.format(pageSize)
            sql_total = 'SELECT count(title) FROM cms_subject  WHERE title  limit {};'.format(pageSize)
            print(sql)
        elif not case_data.get('keyword') and isinstance(int(case_data.get('pageNum')),int) and isinstance(int(case_data.get('pageSize')),int):
            pageNum = int(case_data.get('pageNum'))
            pageSize = int(case_data.get('pageSize'))
            limita = (pageNum - 1) * pageSize  # sql语句中不运算所以提出来运算完毕再使用
            sql = 'SELECT title FROM cms_subject WHERE title limit {},{};'.format(limita, pageSize)
            sql_total = 'SELECT count(title) FROM cms_subject WHERE title limit {},{};'.format(limita, pageSize)
            print(sql)
        else:
            keyword = case_data.get('keyword')
            pageNum = int(case_data.get('pageNum'))
            pageSize = int(case_data.get('pageSize'))
            limita = (int(pageNum) - 1) * int(pageSize)  # sql语句中不运算所以提出来运算完毕再使用
            sql = 'SELECT title FROM cms_subject WHERE title LIKE "%{}%"  limit {},{};'.format(keyword, limita,pageSize)
            sql_total = 'SELECT count(title) FROM cms_subject WHERE title LIKE "%{}%"  limit {},{};'.format(keyword, limita,pageSize)
            print(sql)


        data = case_data.get('data')
        # data ='{"keyword":'+keyword+',"pageNum":'+pageNum+',"pageSize":'+pageSize+'}'
        data = json.loads(data)
        print(data)
        expect_code = case_data.get('expect_code')
        #self.Makelog("开始发送请求")
        try:

            response = requests.get(url=url,headers={"Authorization":BaseCase.read_token(self)},params=data)
        except Exception as e:
            print(e)
            pass

        result = json.loads(response.text)
        # self.assertEqual(result['message'],'操作成功')
        # self.assertEqual(result['data'][0]['id'],1)
        self.assertEqual(response.status_code,expect_code)#检查httpcode
        if  response.status_code!=400 and case_data.get('keyword') and not (isinstance(case_data.get('pageNum'),str) and isinstance(case_data.get('pageSize'),str)):
            conn = DB()
            # subject = conn.check_Subject_List(keyword,pageNum,pageSize)
            subject = conn.query(sql)
            print(subject)  # 结果为一个元组
            if len(subject) !=0:
                expect_title = subject[0][0]
                print(expect_title)
                self.assertIn(result['data']['list'][0]['title'], expect_title)  # 检查keyword是否查出
            #expect_total_subject = conn.check_Subject_List_total(keyword, pageNum, pageSize)
            expect_total_subject = conn.query(sql_total)
            print(expect_total_subject)
            self.assertEqual(result['data']['total'], expect_total_subject[0][0])  # 检查是否为数据库中查出的记录数相同

    def test_Subject_List_normal_keywordIsExists(self):
        self.Subject_List(case_name='test_Subject_List_normal_keywordIsExists')

    def test_Subject_List_normal_keywordIsNotExists(self):
        self.Subject_List(case_name='test_Subject_List_normal_keywordIsNotExists')

    def test_Subject_List_normal_ParameterIsNull(self):
        self.Subject_List(case_name='test_Subject_List_normal_ParameterIsNull')

    def test_Subject_List_normal_keywordIsNull(self):
        self.Subject_List(case_name='test_Subject_List_normal_keywordIsNull')

    def test_Subject_List_normal_PageNumIsNull(self):
        self.Subject_List(case_name='test_Subject_List_normal_PageNumIsNull')

    def test_Subject_List_normal_PageSizeIsNull(self):
        self.Subject_List(case_name='test_Subject_List_normal_PageSizeIsNull')

    def test_Subject_List_normal_keywordIsBlank(self):
        self.Subject_List(case_name='test_Subject_List_normal_keywordIsBlank')

    def test_Subject_List_normal_keywordIsLongCharacter(self):
        self.Subject_List(case_name='test_Subject_List_normal_keywordIsLongCharacter')

    def test_Subject_List_Wrong_PageNumIsString(self):
        self.Subject_List(case_name='test_Subject_List_Wrong_PageNumIsString')

    def test_Subject_List_Wrong_PageSizeIsString(self):
        self.Subject_List(case_name='test_Subject_List_Wrong_PageSizeIsString')

    def test_Subject_List_Wrong_PageSizePageNumAllIsString(self):
        self.Subject_List(case_name='test_Subject_List_Wrong_PageSizePageNumAllIsString')


if __name__ == '__main__':
    unittest.main(verbosity=2)