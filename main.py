from gac_spider import spider
import sys

if __name__ == '__main__':
    mode = None
    if len(sys.argv) == 2:
        mode = sys.argv[1]
    if mode == 'login':
        spider.login()
    elif mode == 'logout':
        spider.logout()
    else:
        spider.checkin()