from gac_config import config
from gac_logger import logger
from imbox import Imbox
import datetime
import re

def read_mailcode():

    #读取配置文件
    host = config.get('email', 'host')
    port = config.get('email', 'port')
    password = config.get('email', 'password')
    email = config.get('account', 'email')
    logger.info('正在获取[%s]的邮件验证码', email)

    #连接邮箱
    conn = Imbox(host, email, password, True, port)
    messages = conn.messages(unread=True, sent_from='support@glados.network', sent_to=email, date__on=datetime.date.today(), subject='GLaDOS Authentication')

    #筛选邮件
    for uid, message in messages:
        message_dict = eval(str(message))
        date = message_dict['date']
        subject = message_dict['subject']
        sent_from = message_dict['sent_from'][0]['email']
        sent_to = message_dict['sent_to'][0]['email']
        logger.debug('邮件简要信息：subject:%s, sent_from:%s, sent_to:%s, date:%s', subject, sent_from, sent_to, date)

        email_datetime = datetime.datetime.strptime(date, '%a, %d %b %Y %H:%M:%S +0000 (UTC)') + datetime.timedelta(hours=8)
        min_datetime = datetime.datetime.now() - datetime.timedelta(minutes=3)
        max_datetime = datetime.datetime.now() + datetime.timedelta(minutes=3)

        condition1 = sent_from == 'support@glados.network' and sent_to == email and subject == 'GLaDOS Authentication'
        condition2 = email_datetime >= min_datetime and email_datetime <= max_datetime
        if  condition1 and condition2:
            body = message_dict['body']['plain'][0]
            logger.debug('找到符合条件的邮件，邮件ID:%s，邮件内容：%s', uid, body)
            mailcode = re.search(r'[0-9]\d*', body, flags=0).group(0)
            logger.info('邮件验证码为：%s', mailcode)
            conn.mark_seen(uid)
            conn.logout()
            return mailcode
    conn.logout()

