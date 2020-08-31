import smtplib #用于建立smtp连接
from email.mime.text import MIMEText #邮件需要专用的MIME格式
from email.mime.multipart import MIMEMultipart  # 混合MIME格式，支持上传附件
from email.header import Header  # 用于使用中文邮件主题
from config.config import *

def send_email(report_file):
    #1.编写邮件内容（Email邮件需要专门的MIME格式）
    #msg=MIMEText("This is a test mail","plain","utf-8")  # plain指普通文本格式邮件内容
    with open(report_file, encoding='utf-8') as f: # 打开html报告
        email_body=f.read() # 读取报告内容

    msg = MIMEMultipart()  # 混合MIME格式
    msg.attach(MIMEText(email_body, 'html', 'utf-8'))  # 添加html格式邮件正文（会丢失css格式）

    #2.组装Email头（发件人,收件人，主题）
    msg['From']='wangniannianhappy@163.com'#发件人
    msg['To']='176032837@qq.com' #收件人
    msg['Subject']=Header(subject, 'utf-8')  # 中文邮件主题，指定utf-8编码

    # 3. 构造附件1，传送当前目录下的 test.txt 文件
    att1 = MIMEText(open(report_file, 'rb').read(), 'base64', 'utf-8')  # 二进制格式打开
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="report.html"'  # filename为邮件中附件显示的名字
    msg.attach(att1)

    #4.连接smtp服务器并发送邮件
    try:
        smtp=smtplib.SMTP_SSL(smtp_server)  # smtp服务器地址 使用SSL模式
        smtp.login(smtp_user,smtp_password)#发件人用户名和密码
        smtp.sendmail(sender,receiver1,msg.as_string()) #填写发件人和接收人邮件地址
        smtp.sendmail(sender,receiver2,msg.as_string()) # 发送给另一个邮箱
        logging.info("邮件发送完成！")
    except Exception as e:
        logging.error(str(e))
    finally:
        smtp.quit()



