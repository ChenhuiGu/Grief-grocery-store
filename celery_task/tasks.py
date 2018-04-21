#创建应用，对象内部封装要异步执行的任务

from celery import Celery
from django.core.mail import send_mail
from Mystore import settings
#客户端的名称，指定redis数据库
app = Celery('myCelery',broker='redis://127.0.0.1:6379/1')

@app.task
def send_active_email(username,email,token):
    '''发送邮件'''
    subject = '用户激活'
    message = ''
    sender = settings.EMAIL_FROM
    receivers = [email]
    html_message = ('<h2>尊敬的 %s, 欢迎来到的我的小商店</h2>' 
                   '<p>请点击此链接激活您的帐号: ' 
                   '<a href="http://127.0.0.1:8000/users/active/%s">' 
                   'http://127.0.0.1:8000/users/active/%s</a>'
                    )% (username, token, token)
    send_mail(subject, message, sender, receivers, html_message=html_message)