# -------------------------------------------------------
# Diseño de Lenguajes de Programación
# Lexical Analyzer Generator Main
# Francisco Rosal - 18676
# -------------------------------------------------------

from afd import AFD
from log import Log
from lex_generator import LexGenerator

ANY_BUT_QUOTES = '«««««««««««««««««l¦d»¦s»¦o»¦ »¦(»¦)»¦/»¦*»¦=»¦.»¦|»¦[»¦]»¦{»¦}»¦<»¦>»'

def lexical_generator():
    LexGenerator()

def afd_test():
    """
    https://elcodigoascii.com.ar
    34 - "
    35 - #
    39 - '
    42 - *
    43 - +
    46 - .
    63 - ?
    124 - |
    126 - ~
    174 - «
    175 - »
    221 - ¦
    241 - ±
    ¶¤§¨ª¬¯°²³´µ·¸¹º×
    """

    re_tests = [{
        'name': 'space',
        're': ' ',
        'tests' : [{
            'w': ' ',
            'result': True
        }]
    }, {
        'name': 'assign',
        're': '=',
        'tests' : [{
            'w': '=',
            'result': True
        }]
    }, {
        'name': 'final',
        're': '.',
        'tests' : [{
            'w': '.',
            'result': True
        }]
    }, {
        'name': 'or',
        're': '|',
        'tests' : [{
            'w': '|',
            'result': True
        }]
    }, {
        'name': 'group',
        're': '(¦)',
        'tests' : [{
            'w': '(',
            'result': True
        }, {
            'w': ')',
            'result': True
        }]
    }, {
        'name': 'option',
        're': '[¦]',
        'tests' : [{
            'w': '[',
            'result': True
        }, {
            'w': ']',
            'result': True
        }]
    }, {
        'name': 'iteration',
        're': '{¦}',
        'tests' : [{
            'w': '{',
            'result': True
        }, {
            'w': '}',
            'result': True
        }]
    }, {
        'name': 'operator',
        're': 'o',
        'tests' : [{
            'w': '+',
            'result': True
        }, {
            'w': '-',
            'result': True
        }, {
            'w': '+-',
            'result': False
        }]
    }, {
        'name': 'ident',
        're': 'l«l¦d»±',
        'tests' : [{
            'w': 'var1',
            'result': True
        }, {
            'w': '1var1',
            'result': False
        }, {
            'w': 'var1iable2',
            'result': True
        }]
    }, {
        'name': 'number',
        're': 'd«d»±',
        'tests' : [{
            'w': '123',
            'result': True
        }, {
            'w': '123w',
            'result': False
        }, {
            'w': '123.123',
            'result': False
        }]
    }, {
        'name': 'string',
        're': '"«a¦\'»±"',
        'tests' : [{
            'w': '"string1@"',
            'result': True
        }, {
            'w': '"hola mundo"',
            'result': True
        }, {
            'w': '"hola  mundo\')$*"',
            'result': True
        }, {
            'w': '"string1@',
            'result': False
        }, {
            'w': 'string1@""',
            'result': False
        }]
    }, {
        'name': 'char',
        're': '«\'«a¦"»±»\'',
        'tests' : [{
            'w': '\'2\'',
            'result': True
        }, {
            'w': '\'a\'',
            'result': True
        }, {
            'w': '\'@\'',
            'result': True
        }, {
            'w': '\'*\'',
            'result': True
        }, {
            'w': '\'"\'',
            'result': True
        }, {
            'w': '\'string1@',
            'result': False
        }, {
            'w': 'string1@\'\'',
            'result': False
        }]
    }, {
        'name': 'comment',
        're': '//««««l¦d»¦s»¦o»¦ »±',
        'tests' : [{
            'w': '//string1@',
            'result': True
        }, {
            'w': '//hola mundo 1 @',
            'result': True
        }, {
            'w': '/string1@',
            'result': False
        }, {
            'w': 'str//ing1»@',
            'result': False
        }]
    }, {
        'name': 'comment_block',
        're': '«/*««a¦"»¦\'»±*»/',
        'tests' : [{
            'w': '/*string1@*/',
            'result': True
        }, {
            'w': '/*string 1 \' " @ */',
            'result': True
        }, {
            'w': '/*string1@',
            'result': False
        }, {
            'w': 'str/**/ing1»@',
            'result': False
        }]
    }, {
        'name': 'semantic_action',
        're': '«(.««a¦"»¦\'»±.»)',
        'tests' : [{
            'w': '(.string1@.)',
            'result': True
        }, {
            'w': '(.string1 @.)',
            'result': True
        }, {
            'w': '(. string1 " \' @ .)',
            'result': True
        }, {
            'w': '.string1@.',
            'result': False
        }, {
            'w': '(.string1@',
            'result': False
        }, {
            'w': 'string1@.)',
            'result': False
        }]
    }, {
        'name': 'attrs',
        're': '«<.««a¦"»¦\'»±.»>',
        'tests' : [{
            'w': '<.string1@.>',
            'result': True
        }, {
            'w': '<.string1 @.>',
            'result': True
        }, {
            'w': '<. string1 " \' @ .>',
            'result': True
        }, {
            'w': '.string1@.',
            'result': False
        }, {
            'w': '<.string1@',
            'result': False
        }, {
            'w': 'string1@.>',
            'result': False
        }]
    }]

    characters = {
        ' ': ' ',
        '"': '"',
        '\'': '\'',
        '/': '/',
        '*': '*',
        '=': '=',
        '.': '.',
        '|': '|',
        '<': '<',
        '>': '>',
        '(': '(',
        ')': ')',
        '[': '[',
        ']': ']',
        '{': '{',
        '}': '}',
        'o': '+-',
        's': '@~!#$%^&_;:,?',
        'l': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'd': '0123456789',
    }

    Log.INFO('Tokens RE')
    for re_test in re_tests[::-1]:
        Log.N(f"'{re_test['name']}': '{re_test['re']}',")

    error_found = False
    for re_test in re_tests:
        Log.INFO('\n\nTesting RE: ' + re_test['name'])
        afd = AFD(
            re_test['re'].replace('a', ANY_BUT_QUOTES),
            draw = False,
            print_tree = True
        )

        for test in re_test['tests']:
            result = afd.accepts(test['w'], characters)

            if result == test['result']:
                Log.OKGREEN(re_test['re'], ' <- ', test['w'], ': ', test['result'])
            else:
                error_found = True
                Log.FAIL(re_test['re'], ' <- ', test['w'], ': ', test['result'])

    if error_found:
        Log.FAIL('\n\nTest failed')
    else:
        Log.OKGREEN('\n\nTest passed')

afd_test()

# lexical_generator()
try:
    lexical_generator()
except Exception as e:
    Log.FAIL('\nUnable to generate lexical analyzer. Error: ', e)
