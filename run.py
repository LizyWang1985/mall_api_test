import unittest
from lib.HTMLTestReporterCN import HTMLTestRunner
from config.config import *
from lib.send_email import send_email
from mall_api_test.test.suite.test_suites import *
import pickle
import sys

def discover(): #根据测试目录查看到所有的测试用例组装到测试套件
    return unittest.defaultTestLoader.discover(test_case_path)

def run(suite):
    logging.info("=====================================测试开始========================================")

    with open(report_file,'wb') as f: #二进制写格式打开要生成的报告文件
        result = HTMLTestRunner(stream=f, title="Api Test", description="测试描述", tester="念念").run(suite)

    if result.failures:# 保存失败用例序列化文件
        save_failures(result,last_fails_file)

    if send_email_after_run:# 是否发送邮件
        send_email(report_file)

    logging.info("=====================================测试结束=======S=================================")

def save_failures(result,file):# file为序列化保存的文件名，配置在config/config.py中
    suite=unittest.TestSuite()
    for case_result in result.failures:# 组装TestSuite
        suite.addTests(case_result[0])# case_result是个元祖，第一个元素是用例对象，后面是失败原因等等

    with open(file,'wb') as f: # 序列化到指定文件
        pickle.dump(suite,f) #序列化到指定文件

def rerun_fails():# 失败用例重跑方法
    sys.path.append(test_case_path) # 需要将用例路径添加到包搜索路径中，不然反序列化TestSuite会找不到用例
    with open(last_files_file,'rb') as f:
        suite=pickle.loads(f) # 反序列化得到TestSuite
    run(suite)



def run_all(): #运行所有的用例
    run(discover())

def run_suite(suite_name): # 运行`test/suite/test_suites.py`文件中自定义的TestSuite
    suite=get_suite(suite_name)
    if suite:
        run(suite)
    else:
        print("TestSuite不存在")


#只列出所有用例（并不执行）
def collect():# 由于使用discover() 组装的TestSuite是按文件夹目录多级嵌套的，我们把所有用例取出，放到一个无嵌套的TestSuite中，方便之后操作
    suite = unittest.TestSuite()

    def _collect(tests):# 递归，如果下级元素还是TestSuite则继续往下找
        if isinstance(tests,unittest.TestSuite):
            if tests.countTestCases()!=0:
                for i in tests:
                    _collect(i)
        else:
            suite.addTests(tests)# 如果下级元素是TestCase，则添加到TestSuite中

    _collect(discover())
    return suite

def collect_only():# 仅列出所用用例
    t0=time.time()
    i=0
    for case in collect():
        i+=1
        print("{}.{}".format(str(i),case.id()))
    print("--------------------------------------------")
    print("Collect {} tests is {:.3f}s".format((str(i),time.time()-t0)))



'''按testlist用例列表运行,test文件夹下新建testlist.txt，内容如下
test_user_login_normal
test_user_reg_normal
# test_user_reg_exist   # 注释后不执行

run.py中添加
'''
def makesuite_by_testlist(testlist_file):
    with open(testlist_file) as f:
        testlist=f.readlines()

    testlist=[i.strip() for  i in testlist if not i.startswith("#")]   # 去掉每行结尾的"/n"和 #号开头的行

    suite=unittest.TestSuite()
    all_cases=collect() #所有用例
    for case in all_cases:
        if case._testMethodName in testlist:
            suite.addTests(case)
        return  suite


def main():
    if options.collect_only:    # 如果指定了--collect-only参数
        collect_only()
    elif options.rerun_fails:    # 如果指定了--rerun-fails参数
        rerun_fails()
    elif options.testlist:    # 如果指定了--testlist参数
        run(makesuite_by_testlist(testlist_file))
    elif options.testsuite:  # 如果指定了--testsuite=***
        run_suite(options.testsuite)
    elif options.tag:  # 如果指定了--tag=***
        run(makesuite_by_tag(options.tag))
    else:   # 否则，运行所有用例
        run_all()

if __name__ == '__main__':
    main()   # 调用main()


