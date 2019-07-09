import sys
import sqlite3
from time import sleep
from argparse import ArgumentParser
from utils import WordsHelper, T9Helper
from db import DBWordsManager
from configparser import ConfigParser

cfg_parser = ConfigParser()
cfg_parser.readfp(open('storage/config.ini'))
cfg_parser.get('DEFAULT', 'MinLettersSens')

parser = ArgumentParser(description='Test task application')

parser.add_argument("-i", "--init", dest="init", help="Command to start initialization of app", action='store_true')

parser.add_argument("-w", "--word", dest="word", type=int,
                    help="Start searching words", metavar="WORD")
dbwm = DBWordsManager()
args = parser.parse_args()
if args.init is True:
    print('Are you sure you want to continue initialization (Y/n)')
    ans = input()
    if ans == 'Y':
        dbwm.learn()
    else:
        sys.exit('Exit init')


# sleep(0.1)
res = dbwm.search('worl', T9Helper.word2t9('worl', full=True)).fetchall()
print(res)

