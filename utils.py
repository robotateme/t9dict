import numpy as np

WORDS_PATH = '/usr/share/dict/words'
TEST_PATH = 'storage/test'



class WordsHelper:
    """Помощник для извлечения строк из файла слов в Unix-системах"""

    @staticmethod
    def read_words_in_chunks():
        """Ленивая загрузка, генератор."""
        fp = open(WORDS_PATH, 'r')
        line = fp.readline()
        while line:
            yield line.strip()
            line = fp.readline()
        fp.close()

    @staticmethod
    def levenshtein(seq1, seq2):
        size_x = len(seq1) + 1
        size_y = len(seq2) + 1
        matrix = np.zeros((size_x, size_y))
        for x in range(size_x):
            matrix[x, 0] = x
        for y in range(size_y):
            matrix[0, y] = y

        for x in range(1, size_x):
            for y in range(1, size_y):
                if seq1[x - 1] == seq2[y - 1]:
                    matrix[x, y] = min(
                        matrix[x - 1, y] + 1,
                        matrix[x - 1, y - 1],
                        matrix[x, y - 1] + 1
                    )
                else:
                    matrix[x, y] = min(
                        matrix[x - 1, y] + 1,
                        matrix[x - 1, y - 1] + 1,
                        matrix[x, y - 1] + 1
                    )
        # print(matrix)
        return matrix[size_x - 1, size_y - 1]


class T9Helper:
    """Помощник для обработчика t9"""
    mapping = {1: ["'"], 2: ["a", "A", "b", "B", "c", "C"],
               3: ["d", "D", "e", "E", "f", "F"],
               4: ["g", "G", "h", "H", "i", "I"],
               5: ["j", "J", "k", "K", "l", "L"],
               6: ["m", "M", "n", "N", "o", "O"],
               7: ["p", "P", "q", "Q", "r", "R", "s", "S"],
               8: ["t", "T", "u", "U", "v", "V"],
               9: ["w", "W", "x", "X", "y", "Y", "z", "Z"]}

    @classmethod
    def word2t9(cls, raw_input: str, full=False):
        """Преобразует первое слово в T9"""
        code = list()
        input_letters = list(raw_input.split(' ')[0])
        input_letters = input_letters if full else input_letters[0:4]
        for in_letter in input_letters:
            for key, letters in cls.mapping.items():
                if in_letter in letters:
                    code.append(str(key))
        return ''.join(code)

    @classmethod
    def word2t9_by_cursor(cls, raw_input: str, full=False):
        """Преобразует слово по позиции курсора в предложении"""
        return cls.word2t9(raw_input.split(' ')[-1], full)
