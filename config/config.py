import logging
import os
import time


from optparse import OptionParser

today=time.strftime('%Y%m%d',time.localtime())
now=time.strftime('%Y%m%d_%H%M%S',time.localtime())


# url
url = 'http://139.199.12.254/manager'

# 项目路径
prj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # 当前文件的上一级的上一级目录（增加一级），__file__指当前文件

data_path= os.path.join(prj_path, 'data')   # 数据目录
test_path = os.path.join(prj_path, 'test')  # 用例目录

#log_file = os.path.join(prj_path, 'log','log.txt')  # 更改路径到log目录下 也可以每天生成新的日志文件
#report_file = os.path.join(prj_path,'report', 'report.html')  # 更改路径到report目录下 也可以每次生成新的报告
log_file=os.path.join(prj_path,'log','log_{}.txt'.format(today))  # 更改路径到log目录下,按天生成log，每次执行生成新的报告
report_file=os.path.join(prj_path,'report','report_{}.test'.format(now))#按天生成report

# log日志配置

logging.basicConfig(level=logging.DEBUG,  # log level
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',  # log格式
                    datefmt='%Y-%m-%d %H:%M:%S',  # 日期格式
                    filename=log_file,  # 日志输出文件
                    filemode='a')  # 追加模式

# if __name__ == '__main__':
#     logging.info('hello')

'''
Log Level==========================:

CRITICAL: 用于输出严重错误信息
ERROR: 用于输出错误信息
WARNING: 用于输出警示信息
INFO: 用于输出一些提升信息
DEBUG: 用于输出一些调试信息
优先级 CRITICAL > ERROR > WARNING > INFO > DEBUG
指定level = logging.DEBUG所有等级大于等于DEBUG的信息都会输出
若指定level = logging.ERROR WARNING,INFO,DEBUG小于设置级别的信息不会输出

日志格式============:

%(levelno)s: 打印日志级别的数值
%(levelname)s: 打印日志级别名称
%(pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
%(filename)s: 打印当前执行程序名
%(funcName)s: 打印日志的当前函数
%(lineno)d: 打印日志的当前行号
%(asctime)s: 打印日志的时间
%(thread)d: 打印线程ID
%(threadName)s: 打印线程名称
%(process)d: 打印进程ID
%(message)s: 打印日志信息

'''
#数据库配置
host='139.199.12.254'
port=3306
user='root'
passwd='root'
db='mall'

# 邮件配置

send_email_after_run=False
smtp_server = 'smtp.163.com'
smtp_user = '***@163.com'
smtp_password = '***'

sender = smtp_user  # 发件人
receiver1 = '***@qq.com'  # 收件人
receiver2 = '***@qq.com'  # 收件人
subject = '接口测试报告'  # 邮件主题


# 命令行选项
parser = OptionParser()

parser.add_option('--collect-only', action='store_true', dest='collect_only', help='仅列出所有用例')
parser.add_option('--rerun-fails', action='store_true', dest='rerun_fails', help='运行上次失败的用例')
parser.add_option('--testlist', action='store_true', dest='testlist', help='运行test/testlist.txt列表指定用例')

parser.add_option('--testsuite', action='store', dest='testsuite', help='运行指定的TestSuite')
parser.add_option('--tag', action='store', dest='tag', help='运行指定tag的用例')

(options, args) = parser.parse_args()  # 应用选项（使生效）