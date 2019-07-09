import sqlite3
from utils import WordsHelper, T9Helper

DB_PATH = 'storage/database'
SCHEMA_PATH = 'storage/schema.sql'


class Database:
    """
        Класс описывающий соединение с базой данных
    """
    table_name = 't9_words'
    _db_connection = None
    _db_cursor = None

    def __init__(self, ):
        self._db_connection = sqlite3.connect(DB_PATH)
        self._db_cursor = self._db_connection.cursor()

    def query(self, query, params):
        """
            Метод реализующий выполнение запросов принимает стандарные параметры для метода sqlite3.execute()
        """
        return self._db_cursor.execute(query, params)

    def __del__(self):
        self._db_connection.close()


class DBSchemaManager(Database):
    """
        Класс менеджер для работы со схемой, исключительно.
        Загрузки схемы и данных
    """

    def restore(self):
        """
        Производит загрузку схемы из дампа.
        """
        with open(SCHEMA_PATH) as fp:
            self._db_cursor.executescript(fp.read())


class DBWordsManager(Database):
    """
        Класс для работы с таблицей слов Sqlite
    """
    table_name = 'words'

    def learn(self):
        i = 0
        for piece in WordsHelper.read_words_in_chunks():
            i += 1
            print("learned {}/{} ...".format(i, 99171))
            self.insert({'word': piece, 'code': T9Helper.word2t9(piece, full=True)})

    def insert(self, data):
        columns = ','.join(data.keys())
        placeholders = ','.join('?' * len(data.keys()))
        sql = 'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'.format(
            table_name=self.table_name, columns=columns, placeholders=placeholders)
        self.query(sql, (data['word'], data['code']))
        self._db_connection.commit()

    def search(self, word_part, code):
        self._db_cursor.row_factory = sqlite3.Row
        sql = 'SELECT word,code FROM words WHERE code >= ? AND word LIKE ? LIMIT {limit}'.format(
            limit=len(word_part) * 3
        )
        return self.query(sql, (code, '{}%'.format(word_part),))
