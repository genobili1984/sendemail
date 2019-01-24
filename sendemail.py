# !/usr/bin/env python
# -*- coding:utf-8 -*-
 
import smtplib
import sys
import os
import mimetypes
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr,formataddr
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
 

COMMASPACE = ', '
# 163邮箱服务器地址
smtp_server='smtp.163.com'
# 发件人邮箱地址, 登录密码evergrande123
from_addr='evergrande_ios@163.com'
# 发件人邮箱密码(使用申请的客户端授权码代替)
passwd='evergrande123'
# 收件人邮箱地址
#to_addr=["445044628@qq.com", "evergrande_ios@163.com"]
to_addr=["evergrande_ios@163.com"]
 
 
def send_email(url):
    # 构建邮件内容(参数:邮件内容; 类型-plain,html; 编码)
    content = "<p>打包成功！</p> \n <p><a href=\"http://fir.im/egscios\"> 扫码安装</a></p> \n  <p><a href=\"{0}\">ftp安装</a></p> \n <p>FTP用户名：daemon 密码：xampp</p>".format( url )
    #msg=MIMEText( '邮件内容', 'plain', 'utf-8' )
    msg=MIMEText( content, 'html', 'utf-8')
    # 设置邮件主题
    #msg['Subject']='融合版打包成功'
    #msg['To'] = COMMASPACE.join( to_addr )
    #msg['From'] = "evergrande_ios@163.com"

    outer = MIMEMultipart()
    # 设置邮件主题
    outer['Subject']='融合版打包成功'
    outer['To'] = COMMASPACE.join( to_addr )
    outer['From'] = "evergrande_ios@163.com"
    outer.attach( msg )

    #构造附件，发送某个目录下的文件
    directory = './attach'
    for filename in os.listdir( directory ) : 
        path = os.path.join( directory, filename )
        if not os.path.isfile( path ):
            continue
        #guess the content base on the file's extension. 
        ctype, encoding = mimetypes.guess_type( path )
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        if maintype == 'text':
            fp = open( path )
            msg = MIMEText( fp.read(), _subtype=subtype )
            fp.close()
        elif maintype == 'image':
            fp = open( path, 'rb' )
            msg = MIMEImage( fp.read(), _subtype=subtype )
            fp.close()
        elif maintype == 'audio':
            fp = open(path, 'rb')
            msg = MIMEAudio( fp.read(), _subtype=subtype )
            fp.close()
        else:
            fp = open( path, 'rb')
            msg = MIMEBase( maintype, subtype )
            msg.set_payload( fp.read() )
            fp.close()
            #Encode the payload using Base64
            encoders.encode_base64( msg )
        msg.add_header( 'Content-Disposition', 'attachment', filename=filename )
        outer.attach( msg )
    composed = outer.as_string()

    # 获取SMTP对象
    server=smtplib.SMTP(host=smtp_server,port=25)
    # 登录163邮箱服务器
    server.login(user=from_addr,password=passwd)
    # 发送邮件
    #server.sendmail(from_addr, to_addr, msg.as_string() )
    server.sendmail(from_addr, to_addr, composed )
    
    # 退出邮箱服务器
    server.quit()
    print "send end!"
 
 
if __name__ == '__main__':
    params = len(sys.argv)
    print "params count = {0}".format( params )
    if params <= 1:
        print "command param error!"
        sys.exit(1)
    ftp_url = sys.argv[1]
    if len(ftp_url) == 0: 
        print "url is not valid"
        sys.exit(1)
    print "ftp = {0}".format( ftp_url )
    send_email( ftp_url )

