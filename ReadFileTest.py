import unittest

from ReadFile import ReadFile


class ReadFileTestCase(unittest.TestCase):
    def setUp(self):
        self.read_file = ReadFile()

    def test_read_file(self):
        docs = self.read_file.read_docs("./test_data/FB396011/FB396011")
        self.assertEqual(265, len(docs))
        self.assertIsNotNone(docs[2].id)
        self.assertIsNotNone(docs[2].text)

    def test_read_files_from_path(self):
        docs = self.read_file.read_files("./test_data/")
        self.assertEqual(347 + 176, len(docs))

    def test_doc_with_no_text(self):
        docs = self.read_file.read_docs("./test_data/FB396070/FB396070")
        print(len(docs))
        self.assertEqual(176, len(docs))


if __name__ == '__main__':
    unittest.main()
