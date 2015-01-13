#!flask/bin/python
import unittest

from search import searchWord

class TestCase(unittest.TestCase):

	def test_search(self):
		keywords = "zoo"
		result = searchWord(keywords)
		expectedListLenth = 20
		assert len(result) == expectedListLenth


if __name__ == '__main__':
	unittest.main()