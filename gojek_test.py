import unittest
from gojek import _CharacterSet, _Quantifier, _SimplePattern, _CompoundPattern, generate
import re


class TestGenerateFunction(unittest.TestCase):
    def test_characterSet(self):
        for _ in range(500):
            self.assertIn(_CharacterSet(r'[a-z]').generate(), {chr(code) for code in range(ord('a'), ord('z') + 1)})
            self.assertIn(_CharacterSet(r'[a-b]').generate(), {chr(code) for code in range(ord('a'), ord('b') + 1)})
            self.assertIn(_CharacterSet(r'[a-bc]').generate(), {chr(code) for code in range(ord('a'), ord('c') + 1)})
            self.assertIn(_CharacterSet(r'[ca-b]').generate(), {chr(code) for code in range(ord('a'), ord('c') + 1)})
            self.assertIn(_CharacterSet(r'[cab]').generate(), {chr(code) for code in range(ord('a'), ord('c') + 1)})
            self.assertIn(_CharacterSet(r'[bca]').generate(), {chr(code) for code in range(ord('a'), ord('c') + 1)})
            self.assertNotIn(_CharacterSet(r'[^a-z]').generate(), {chr(code) for code in range(ord('a'), ord('z') + 1)})
            self.assertIn(_CharacterSet(r'[0-9]').generate(), {chr(code) for code in range(ord('0'), ord('9') + 1)})
            self.assertIn(_CharacterSet(r'[8-9]').generate(), {chr(code) for code in range(ord('8'), ord('9') + 1)})
            self.assertIn(_CharacterSet(r'[8-97]').generate(), {chr(code) for code in range(ord('7'), ord('9') + 1)})
            self.assertIn(_CharacterSet(r'[78-9]').generate(), {chr(code) for code in range(ord('7'), ord('9') + 1)})
            self.assertIn(_CharacterSet(r'[879]').generate(), {chr(code) for code in range(ord('7'), ord('9') + 1)})
            self.assertIn(_CharacterSet(r'[987]').generate(), {chr(code) for code in range(ord('7'), ord('9') + 1)})
            self.assertNotIn(_CharacterSet(r'[^0-9]').generate(), {chr(code) for code in range(ord('0'), ord('9') + 1)})
            self.assertIn(_CharacterSet(r'[0-9ca-b]').generate(), set('0123456789cab'))
            self.assertNotIn(_CharacterSet(r'[^0-9ca-b]').generate(), set('0123456789cab'))

    def test_Quantifier(self):
        for _ in range(500):
            self.assertTrue(_Quantifier(r'*').generate() >= 0)
            self.assertTrue(_Quantifier(r'+').generate() >= 1)
            self.assertTrue(_Quantifier(r'?').generate() in (0, 1))
            self.assertTrue(_Quantifier(r'{5}').generate() == 5)
            self.assertTrue(_Quantifier(r'{5, 15}').generate() in {v for v in range(5, 16)})

    def test_generate(self):
        def matches_regex(pattern, given_string):
            pattern = re.compile(pattern)
            return pattern.match(given_string)

        for _ in range(500):
            pattern = "(1[0-2]|0[1-9])(:[0-5][0-9]){2} (A|P)M"
            self.assertTrue(matches_regex(pattern, generate(pattern)))
            pattern = "Python is fun"
            self.assertTrue(matches_regex(pattern, generate(pattern)))
            pattern = "(a|b|c)xz"
            self.assertTrue(matches_regex(pattern, generate(pattern)))
            pattern = "[tT]rue|[yY]es"
            self.assertTrue(matches_regex(pattern, generate(pattern)))
            pattern = "[^a-yA-Y]?"
            self.assertTrue(matches_regex(pattern, generate(pattern)))
            pattern = "[-+]?[0-9]{1,16}[.][0-9]{1,6}"
            self.assertTrue(matches_regex(pattern, generate(pattern)))
            pattern = "[A-Z0-9._%+-]+@[A-Z0-9.-]+[.][A-Z]{2,10}"
            self.assertTrue(matches_regex(pattern, generate(pattern)))
            pattern = "([a-zA-Z0-9_.]+)@([a-zA-Z0-9_.]+)[.]([a-zA-Z]{2,5})"
            self.assertTrue(matches_regex(pattern, generate(pattern)))
            pattern = "[0-9]+"
            self.assertTrue(matches_regex(pattern, generate(pattern)))
            pattern = "[1-9][0-9]*|0"
            self.assertTrue(matches_regex(pattern, generate(pattern)))


if __name__ == '__main__':
    unittest.main()
