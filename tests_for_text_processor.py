import unittest
from textprocessor import *


test_text1 = "HeLLo, WOrlD, Here THE STOP text!!!"


class TestTextProcessor(unittest.TestCase):
    def test_clean_text_removes_non_alphabetic_characters(self):
        # Проверка удаления небуквенных символов и приведения текста к нижнему регистру
        processor = TextProcessor(test_text1)
        processor.clean_text()
        self.assertEqual(processor.cleaned_text, "hello world here the stop text")

    def test_clean_text_converts_to_lowercase(self):
        # Проверка приведения текста к нижнему регистру
        processor = TextProcessor(test_text1)
        processor.clean_text()
        self.assertEqual(processor.cleaned_text, "hello world here the stop text")

    def test_clean_text_handles_empty_string(self):
        # Проверка работы метода на пустой строке
        processor = TextProcessor("")
        processor.clean_text()
        self.assertEqual(processor.cleaned_text, "")

    def test_remove_stop_words_removes_specified_words(self):
        # Проверка удаления стоп-слов
        processor = TextProcessor(test_text1)
        stop_words = ['the', 'stop']
        processor.remove_stop_words(stop_words)
        self.assertEqual(processor.cleaned_text, "hello world here text")

    def test_remove_stop_words_calls_clean_text_if_needed(self):
        # Проверка, что текст корректно очищается, если clean_text не был вызван заранее
        processor = TextProcessor(test_text1)
        stop_words = ['hello']
        processor.remove_stop_words(stop_words)
        self.assertEqual(processor.cleaned_text, "world here the stop text")

    def test_remove_stop_words_works_without_any_stop_words(self):
        # Проверка работы метода при отсутствии стоп-слов
        processor = TextProcessor(test_text1)
        stop_words = []
        processor.remove_stop_words(stop_words)
        self.assertEqual(processor.cleaned_text, "hello world here the stop text")

    # Запуск тестов


if __name__ == '__main__':
    unittest.main()