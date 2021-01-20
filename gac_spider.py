import requests
import os
import pickle

from gac_config import config
from gac_logger import logger


class Spider:

    def __init__(self):
        self._session = requests.session();
        self._header = {
            'User-Agent' : 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'Accept': 'application/json',
            'Referer': 'https: // glados.rocks / login'
        }
        self.__load_config()
        self._cookie_dir = './cookies/'
        self._cookie_filename = '{0}.cookie'.format(self._config['email'])

    def __load_config(self):
        self._config = {}
        self._config['host'] = config.get('account', 'host')
        self._config['email'] = config.get('account', 'email')

    def __save_cookie(self):
        directory = os.path.dirname(self._cookie_dir)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(self._cookie_dir + self._cookie_filename, 'wb') as f:
            pickle.dump(self._session.cookies, f)
        logger.info('cookie保存成功')

    def __load_cookie(self):
        if not os.path.exists(self._cookie_dir + self._cookie_filename):
            raise FileNotFoundError('Not Found Cookie')
        with open(self._cookie_dir + self._cookie_filename, 'rb') as f:
            self._session.cookies.update(pickle.load(f))
        logger.info('cookie加载成功')

    def __del_cookie(self):
        if os.path.exists(self._cookie_dir + self._cookie_filename):
            os.remove(self._cookie_dir + self._cookie_filename)
        logger.info('cookie删除成功')

    def __send_auth_code(self):
        email = self._config['email']
        host = self._config['host']
        logger.info('向邮箱[%s]发送验证码', email)
        url = 'https://{0}/api/authorization'.format(host)
        payload = {
            'address' : email,
            'site' : 'glados.network'
        }
        logger.debug('验证码获取请求参数：%s', payload)
        response = self._session.post(url, data=payload).json()
        logger.debug('验证码获取响应响应：%s', response)
        if response['code'] == 0:
            logger.info('验证码发送成功')
            code = input('请输入[{0}]邮箱收到的验证码：'.format(email))
            logger.info('输入的验证码为：%s', code)
            return code
        else:
            logger.warn('验证码发送失败')
            return None

    def login(self):
        '''
        登录
        :return: str
        '''

        mailcode = self.__send_auth_code()
        if mailcode is None:
            logger.warn("验证码为None")
            return False

        email = self._config['email']
        host = self._config['host']
        logger.info('正在登录[%s]账号', email)
        url = 'https://{0}/api/login'.format(host)
        payload = {
            'email' : email,
            'mailcode' : mailcode,
            'method' : 'email',
            'site' : 'glados.network'
        }
        logger.debug('登录请求参数：%s', payload)
        response = self._session.post(url, data=payload).json()
        logger.debug('登录响应参数：%s', response)
        if response['code'] == 0:
            logger.info('登录成功，返回消息：%s', response['message'])
            self.__save_cookie()
            return True
        else:
            logger.info('登录失败，返回消息：%s', response['message'])
            return False

    def checkin(self):
        '''
        签到
        :return:
        '''

        email = self._config['email']
        host = self._config['host']
        logger.info('正在进行[%s]账号的签到', email)
        url = 'https://{0}/api/user/checkin'.format(host)
        payload = { 'token' : 'glados_network' }
        logger.debug('签到请求参数：%s', payload)
        try:
            self.__load_cookie()
        except FileNotFoundError as e:
            logger.info(e)
            self.login()
        response = self._session.post(url, data=payload).json()
        logger.debug('签到响应参数：%s', response)
        code = response['code']
        message = response['message']
        if code == 0:
            logger.info('签到成功，返回消息：%s', message)
        elif code == 1:
            logger.info('已经签到过了，返回消息：%s', message)
        elif code == -2:
            logger.info('登录已失效，返回消息：%s', message)
            self.login()
            self.checkin()
        else:
            logger.info('其他，返回消息：%s', message)

    def logout(self):
        '''
        退出账号
        :return:
        '''

        email = self._config['email']
        host = self._config['host']
        try:
            self.__load_cookie();
        except FileNotFoundError as e:
            logger.info('[%s]不存在cookie，无需退出', email)
            return
        logger.info('正在进行[%s]账号的退出', email)
        url = 'https://{0}/api/logout'.format(host)
        response = self._session.post(url, allow_redirects=False)
        if response.status_code == 302:
            logger.info('退出账号成功')
            self.__del_cookie()
        else:
            logger.info('退出账号失败')

spider = Spider()