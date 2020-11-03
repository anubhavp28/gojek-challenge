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

