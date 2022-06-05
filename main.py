# -------------------------------------------------------
# Diseño de Lenguajes de Programación
# Analyzer Generator Main
# Francisco Rosal - 18676
# -------------------------------------------------------

from afd import AFD
from log import Log
import PySimpleGUI as sg
from lex_generator import AnalyzerGenerator

ANY_BUT_QUOTES = '«««««««««««««««««l¦d»¦s»¦o»¦ »¦(»¦)»¦/»¦*»¦=»¦.»¦|»¦[»¦]»¦{»¦}»¦<»¦>»'

def analyzer_generator(compiler_def_file_name, entry_file_name):
    AnalyzerGenerator(compiler_def_file_name, entry_file_name)

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


try:
    tokens_flow_file = open('output/tokens-flow', 'w+')
    tokens_flow_file.write('')
    tokens_flow_file.close()
except:
    Log.FAIL('\nThere was an error opening and writing on the file.')
    exit()

sg.theme('Dark')

layout_font = 'Helvetica 15'

layout = [
    [sg.Text('Select the compiler definition file', font=layout_font), sg.FileBrowse(key='-Compiled-Def-', font=layout_font)],
    [sg.Text('Select the file to analyze', font=layout_font), sg.FileBrowse(key='-Entry-File-', font=layout_font)],
    [sg.Button('OK', font=layout_font), sg.Button('Exit', font=layout_font)],
    [sg.Multiline(size=(200, 8), font='Helvetica 20', key='-Input-', disabled=True)],
    [sg.Multiline(size=(200, 8), font='Helvetica 20', key='-Output-', disabled=True)],
    # [sg.Output(size=(200,15), font=layout_font)],
]

# Create the Window
window = sg.Window('Analizador Lexico y Sintactico', layout, size=(1500,800))

compiler_def_file_name = None
entry_file_name = None

# Event Loop to process 'events' and get the 'values' of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    # print('You entered ', values)

    if values['-Compiled-Def-'] and values['-Entry-File-']:
        compiler_def_file_name = values['-Compiled-Def-']
        entry_file_name = values['-Entry-File-']
        break

# analyzer_generator()
try:
    if not compiler_def_file_name or not entry_file_name:
        compiler_def_file_name = 'compiler_def'
        entry_file_name = 'entry.w'

    try:
        entry_file = open(entry_file_name, 'r')
        entry_file_lines = entry_file.readlines()
        entry_file.close()
        [window['-Input-'].print(line) for line in entry_file_lines]
    except Exception as e:
        print('Error: ', e)
        exit()

    analyzer_generator(compiler_def_file_name, entry_file_name)

    # Event Loop to process 'events' and get the 'values' of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        # print('You entered ', values)

        try:
            tokens_flow_file = open('output/tokens-flow', 'r')
        except Exception as e:
            print('Error: ', e)
            exit()

        tokens_extracted = tokens_flow_file.readlines()
        tokens_flow_file.close()
        [window['-Output-'].print(token) for token in tokens_extracted]

        for i in range(0, 10):
            print('')

        print('Press exit or close the window to exit')

except Exception as e:
    Log.FAIL('\nUnable to generate lexical analyzer. Error: ', e)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    
    print('Press exit or close the window to exit')


window.close()
