import unittest

from ReadFile import ReadFile


class ReadFileTestCase(unittest.TestCase):
    def setUp(self):
        self.read_file = ReadFile()

    def test_read_FB_file(self):
        docs = self.read_file.read_docs_from_FB_file("./test_data/FB396011/FB396011")
        self.assertEqual(265, len(docs))
        self.assertEqual("FBIS3-2550", docs[3].id)
        text = '''At the first session of the third Siping City 
People's Congress, Li Shixue was elected chairman of the city 
people's congress standing committee, and Zang Shengye was 
elected mayor of Siping city. 
  At the first session of the third Liaoyuan City People's 
Congress, Zhao Yongji was elected chairman of the city people's 
congress standing committee, and An Li was elected mayor of the 
city.'''
        self.assertEqual(text, docs[3].text)

    def test_read_FT_file(self):
        docs = self.read_file.read_docs_from_FT_file("./test_data/FT942_40/FT942_40")
        self.assertEqual(289, len(docs))
        self.assertEqual("FT942-13574", docs[3].id)
        text = "Nearly 40 teenage rugby players were hurt when the bus taking them from" + "\n" + \
               "Stirling to a tournament at the border town of Hawick was in collision with" + "\n" + \
               "a tanker at Middleton Moor, near Edinburgh."
        self.assertEqual(text, docs[3].text)

    def test_read_LA_file(self):
        docs = self.read_file.read_docs_from_LA_file("./test_data/LA010790/LA010790")
        self.assertEqual(226, len(docs))
        self.assertEqual("LA010790-0008", docs[7].id)
        text = '''"What Are We Doing to Our Children?," KTLA's program on the foster care and 
juvenile justice system, presented an honest, realistic and disturbing 
portrayal of what happens when parents fail and children are left at the mercy 
of an overwhelmed and ineffective governmental agency. What is more alarming is 
that, with the increase in drug use, domestic violence, infant abandonments, 
etc., we are seeing more and more children swept into a whirlpool of 
instability and danger. 

Gary Traxler, North Hollywood 
'''
        self.assertEqual(text, docs[7].text)


    def test_doc_with_missing_text_tag(self):
        docs = self.read_file.read_docs_from_FB_file("./test_data/FB396070/FB396070")
        print(len(docs))
        self.assertEqual(176, len(docs))



if __name__ == '__main__':
    unittest.main()
