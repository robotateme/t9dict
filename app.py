import sys
from argparse import ArgumentParser
from utils import T9Helper, WordsHelper
from db import DBWordsManager
from collections import OrderedDict

parser = ArgumentParser(description='Test task application')

parser.add_argument("-i", "--init", dest="init", help="Command to start initialization of app", action='store_true')

parser.add_argument("-w", "--word", dest="word", type=str,
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

if isinstance(args.word, str):
    result_rows = dbwm.search(args.word, T9Helper.word2t9(args.word, full=True)).fetchall()
    result_words = []

    for row in result_rows:
        distance = WordsHelper.levenshtein(args.word, row['word'])
        word_data = dict(word=row['word'], distance=distance)
        result_words.append(word_data)

        result_words = sorted(result_words, key=lambda k: k['distance'])
    for w in result_words:
        print(w['word'])



