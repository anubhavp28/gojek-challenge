"""
--------------------
GoJEK Code Challenge 
--------------------

Problem : https://gist.github.com/ciju/40afaa21a4b9be998955e84570a057c0

Function `generate` returns string conforming to the given regex pattern.
Supported features include :

. Match any character except newline
[ Start character class definition
] End character class definition
? 0 or 1 quantifier
* 0 or more quantifiers
+ 1 or more quantifier
{ Start min/max quantifier
} End min/max quantifier
^ Negate the class, but only if the first character
- Indicates character range
| Start of alternative branch
( Start subpattern
) End subpattern

Build using Python 3.7.3

Sample Output 
--------------

>> python3 gojek.py
Here are some samples - 
Pattern =  [-+]?[0-9]{1,16}[.][0-9]{1,6}
String =  +51.6688
Pattern =  (1[0-2]|0[1-9])(:[0-5][0-9]){2} (A|P)M
String =  10:35:35 PM
Pattern =  [1-9][0-9]*|0
String =  722277407537141726978
Pattern =  ([a-zA-Z0-9_.]+)@([a-zA-Z0-9_.]+)[.]([a-zA-Z]{2,5})
String =  8@Zfern_QCszPc0E4dknb.bNobc

Contact Details
---------------

Anubhav Patel (anubhavp28@gmail.com)
Resume : https://anubhavp28.github.io/Resume/resume.pdf

"""

from random import randint


class _CharacterSet:
    """
    Internal class representing a Character Class or Character Set
    (see https://www.regular-expressions.info/charclass.html)
    in a regular expression.
    """

    def __init__(self, patternStr):
        self.pattern = patternStr

    def _negate_choices(self, choices):
        """Return negation of the character set."""
        all_choices = {ascii_value for ascii_value in range(32, 126)}
        for ch in choices:
            all_choices.remove(ch)
        return all_choices

    def generate(self):
        """Generate a string conforming to the character set."""
        # return any visible character if character set is universal
        if self.pattern == '.':
            return chr(randint(32, 126))

        if self.pattern[0] == '(':
            return self.pattern[1:-1]

        # ignore if character set is a singleton
        if self.pattern[0] != '[':
            return self.pattern

        # remove surrounding square brackets
        self.pattern = self.pattern[1:-1]
        negate_choices = False

        # remember to negate the set in the end
        if self.pattern[0] == '^':
            negate_choices = True

        choices = set()
        idx = 0
        while idx < len(self.pattern):
            ch = self.pattern[idx]
            next_ch = None if idx + 1 >= len(self.pattern) else self.pattern[idx + 1]

            # Distinguish between character ranges (ex. a-z) and single characters (ex. y)
            if ch.isalnum() and next_ch == '-':
                start = ch
                end = self.pattern[idx + 2]
                idx = idx + 2

                for ascii_value in range(ord(start), ord(end) + 1):
                    choices.add(ascii_value)
            else:
                choices.add(ord(ch))
            idx = idx + 1

        if negate_choices:
            choices = self._negate_choices(choices)

        # randomly select any character in the set to return
        idx_choice = randint(0, len(choices) - 1)
        choices = list(choices)
        return chr(choices[idx_choice])


class _Quantifier:
    """
    Internal class representing a Quantifier
    (see https://javascript.info/regexp-quantifiers)
    in a regular expression.
    """

    def __init__(self, patternStr):
        if patternStr[0] == '{':
            patternStr = patternStr[1:-1]
        self.pattern = patternStr

    def generate(self):
        """Generate a number conforming to the quantifier."""

        if self.pattern == '?':
            return randint(0, 1)

        if self.pattern == '*':
            return randint(0, 20)

        if self.pattern == '+':
            return randint(1, 20)

        if ',' not in self.pattern:
            return int(self.pattern)

        start, end = self.pattern.split(',')
        start, end = int(start), int(end)
        return randint(start, end)


class _SimplePattern:
    """Internal class representing a regex pattern without any subpatterns."""

    def __init__(self, patternStr):
        self.pattern = patternStr

    def generate(self):
        """Generate a string conforming to the pattern."""

        # randomy select any branch
        if '|' in self.pattern:
            choices = self.pattern.split('|')
            num_of_choices = len(choices)
            self.pattern = choices[randint(0, num_of_choices - 1)]

        # a regex pattern can be decomposed in a sequence of "<character-set><quantifier>" units.
        # process each unit individually
        character_stack = []
        idx = 0
        while idx < len(self.pattern):
            ch = self.pattern[idx]

            # extract sequence describing a character class
            if ch in ('[', '('):
                idx = idx + 1
                char_set = ch
                while self.pattern[idx] not in (']', ')'):
                    char_set = char_set + self.pattern[idx]
                    idx = idx + 1
                char_set = char_set + self.pattern[idx]
            else:
                char_set = ch

            # extract the next character to search for possible quantifier
            idx = idx + 1
            next_ch = None if idx >= len(self.pattern) else self.pattern[idx]

            times = 1

            # check if this is start of a quantifier
            if next_ch in ('{', '?', '+', '*'):
                quantifier = next_ch

                # extract sequence representing a quantifier
                if next_ch == '{':
                    idx = idx + 1
                    quantifier = ""

                    while self.pattern[idx] != '}':
                        quantifier = quantifier + self.pattern[idx]
                        idx = idx + 1

                times = _Quantifier(quantifier).generate()
                idx = idx + 1

            for _ in range(0, times):
                character_stack.append(_CharacterSet(char_set).generate())

        return "".join(character_stack)


class _CompoundPattern:
    """Internal class representing a regex pattern with nested subpatterns."""

    def __init__(self, patternStr):
        self.pattern = patternStr

    def generate(self):
        """Generate a string conforming to the pattern."""

        if '(' not in self.pattern:
            return _SimplePattern(self.pattern).generate()

        # process all subpatterns in bottom-up fashion
        character_stack = []
        for ch in self.pattern:
            if ch != ')':
                character_stack.append(ch)
                continue

            subpattern = ""
            while character_stack[-1] != '(':
                subpattern += character_stack[-1]
                character_stack.pop()
            subpattern = subpattern[::-1]

            subpattern = _SimplePattern(subpattern).generate()
            character_stack.extend(subpattern)
            character_stack.append(')')

        return _SimplePattern("".join(character_stack)).generate()


def generate(regex_pattern):
    """Generate a string conforming to the regex pattern."""
    if regex_pattern[0] == '/':
        regex_pattern = regex_pattern[1:-1]
    return _CompoundPattern(regex_pattern).generate()


if __name__ == '__main__':
    print("Here are some samples - ")
    pattern = "[-+]?[0-9]{1,16}[.][0-9]{1,6}"
    print("Pattern = ", pattern)
    print("String = ", generate(pattern))
    pattern = "(1[0-2]|0[1-9])(:[0-5][0-9]){2} (A|P)M"
    print("Pattern = ", pattern)
    print("String = ", generate(pattern))
    pattern = "[1-9][0-9]*|[1-9][0-9]*|0"
    print("Pattern = ", pattern)
    print("String = ", generate(pattern))
    pattern = "([a-zA-Z0-9_.]+)@([a-zA-Z0-9_.]+)[.]([a-zA-Z]{2,5})"
    print("Pattern = ", pattern)
    print("String = ", generate(pattern))
