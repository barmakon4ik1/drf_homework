import json
import unittest
import os
from utils import *


class TestFileOperations(unittest.TestCase):
    def setUp(self):
        # Подготовка тестового файла и данных перед каждым тестом.
        self.filename = "test_file.json"
        self.test_data = test_data = {
            "pk": 4,
            "author": "Test Author",
            "publisher_date": "2024-06-23",
            "publisher": 6,
            "price": 9.99,
            "discount_price": 3.56,
            "is_bestseller": True,
            "is_banned": False,
            "genres": [1, 2]
        }

    def tearDown(self):
        # Удаление тестового файла после каждого теста, если он существует.
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_write_and_read_file(self):
        # Проверка записи и чтения корректных данных
        write_to_file(self.filename, self.test_data)
        read_data = read_from_file(self.filename)

        # Проверяем, что прочитанные данные совпадают с исходными
        self.assertEqual(read_data, self.test_data)

        # Проверяем типы данных полей
        self.assertIsInstance(read_data['pk'], int)
        self.assertIsInstance(read_data['author'], str)
        self.assertIsInstance(read_data['publisher_date'], str)
        self.assertIsInstance(read_data['publisher'], int)
        self.assertIsInstance(read_data['price'], float)
        self.assertIsInstance(read_data['discount_price'], float)
        self.assertIsInstance(read_data['is_bestseller'], bool)
        self.assertIsInstance(read_data['is_banned'], bool)
        self.assertIsInstance(read_data['genres'], list)

    def test_write_and_read_empty_file(self):
        # Проверка записи и чтения пустого словаря
        empty_data = {}
        write_to_file(self.filename, empty_data)
        read_data = read_from_file(self.filename)
        self.assertEqual(read_data, self.test_data)

    def test_read_nonexistent_file(self):
        # Проверка чтения из несуществующего файла
        with self.assertRaises(FileNotFoundError):
            read_from_file('nonexistent_file.json')

    def test_write_bad_data_into_file(self):
        # Проверка записи некорректных данных
        # (например, данных, которые не могут быть сериализованы в JSON)
        bad_data = {'set_data': {1, 2, 3}}  # Наборы не могут быть сериализованы в JSON

        with self.assertRaises(TypeError):
            write_to_file(self.filename, bad_data)


if __name__ == '__main__':
    unittest.main()
