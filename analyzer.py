# -------------------------------------------------------
# Diseño de Lenguajes de Programación
# Lexical Analyzer
# Francisco Rosal - 18676
# -------------------------------------------------------

# Lexical Analyzer for ArchivoPrueba1 Compiler

import sys
from afd import AFD
from log import Log

ANY_BUT_QUOTES = '«««««««««««««««l¦d»¦s»¦o»¦ »¦(»¦)»¦/»¦*»¦=»¦.»¦|»¦[»¦]»¦{»¦}»'

entry_file_name = sys.argv[1]

# CHARACTERS
CHARACTERS = {
    'A': '0123456789',
    ' ': ' ',
    'S': '-',
    'T': '+',
    'U': '*',
    'V': '/',
    'W': '(',
    'X': ')',
    'b': 'Instruccion',
    'c': ';',
    'd': 'Expresion',
    'e': 'Termino',
    'f': 'Factor',
    'g': 'Number',
    'h': 'numero',
}

# KEYWORDS
KEYWORDS = {
    'NEWLINE': '\\n',
}

# TOKENS RE
TOKENS_RE = {
    'menos': 'S',
    'mas': 'T',
    'por': 'U',
    'div': 'V',
    '(': 'W',
    ')': 'X',
    'numero': 'A«A»±',
    'space': ' ',
}

# Whitespace definition
IGNORE = {
    'char_numbers': [9, 20],
    'strings': [],
}

# PRODUCTIONS
PRODUCTIONS = {
    'EstadoInicial0': '«bc»±',
    'Instruccion0': 'd',
    'Expresion0': 'e«Se»±',
    'Expresion1': 'e«Te»±',
    'Termino0': 'f«Vf»±',
    'Termino1': 'f«Uf»±',
    'Factor0': 'WdX',
    'Factor1': 'SWdX',
    'Factor2': 'g',
    'Factor3': 'Sg',
    'Number0': 'h',
}


TOKENS = []

# -------------------------------------------------------

class Token():
    def __init__(self, value, line, column):
        self.value = value
        self.line = line + 1
        self.column = column + 1
        self.type = Token.get_type_of(value)

    def __str__(self):
        return f'Token({self.value}, {self.type}, {self.line}, {self.column})'

    @classmethod
    def get_type_of(cls, word):
        if word in KEYWORDS.values():
            return 'KEYWORD'
        elif word in [chr(number) for number in IGNORE['char_numbers']] or word in IGNORE['strings']:
            return 'IGNORE'
        else:
            for token_type, re in TOKENS_RE.items():
                if AFD(re.replace('a', ANY_BUT_QUOTES)).accepts(word, CHARACTERS):
                    return token_type
        return 'ERROR'

# -------------------------------------------------------

def eval_line(entry_file_lines, line, line_index):
    analyzed_lines = 1
    line_position = 0
    current_line_recognized_tokens = []
    while line_position < len(line):
        current_token = None
        next_token = None
        avance = 0
        continuar = True
        while continuar:
            if current_token and next_token:
                if current_token.type != 'ERROR' and next_token.type == 'ERROR':
                    avance -= 1
                    continuar = False
                    break

            if line_position + avance > len(line):
                continuar = False
                break

            if line_position + avance <= len(line):
                current_token = Token(line[line_position:line_position + avance], line_index, line_position)

            avance += 1

            if line_position + avance <= len(line):
                next_token = Token(line[line_position:line_position + avance], line_index, line_position)

            # Log.WARNING(current_token)

        line_position = line_position + avance


        if current_token and current_token.type != 'ERROR':
            # Log.INFO(current_token)
            TOKENS.append(current_token)
            current_line_recognized_tokens.append(current_token)
        else:
            Log.FAIL(current_token)

            if line_position == len(line) + 1 and len(current_line_recognized_tokens) != 0:
                TOKENS.append(current_token)

            # Si se llega al final de la linea y no se reconoce ningun token,
            # se agrega la siguiente linea y se vuelve a intentar.
            if line_position == len(line) + 1 and len(current_line_recognized_tokens) == 0:
                if line_index < len(entry_file_lines) - 1:
                    new_line = line + ' ' + entry_file_lines[line_index + 1].replace('\n', '\\n')
                    line_index += 1
                    Log.INFO('Trying: ', new_line)
                    analyzed_lines += eval_line(entry_file_lines, new_line, line_index)

    return analyzed_lines

# -------------------------------------------------------

def run():
    try:
        entry_file = open(entry_file_name, 'r')
    except Exception as e:
        print('Error: ', e)
        exit()

    entry_file_lines = entry_file.readlines()
    entry_file.close()

    # -------------------------------------------------------
    # GET TOKENS
    # -------------------------------------------------------
    line_index = 0
    while line_index < len(entry_file_lines):
        line = entry_file_lines[line_index].replace('\n', '\\n')
        analyzed_lines = eval_line(entry_file_lines, line, line_index)
        line_index += analyzed_lines

    Log.OKGREEN('\n\nTokens found:')
    for token in TOKENS:
        if token.type == 'ERROR':
            Log.WARNING(token)
        else:
            Log.INFO(token)

    # -------------------------------------------------------
    # GET TOKENS
    # -------------------------------------------------------
    lexical_errors = False
    Log.OKBLUE('\n\nLexical errors:')
    for token in TOKENS:
        if token.type == 'ERROR':
            Log.WARNING(f'Lexical error on line {token.line} column {token.column}: {token.value}')
            lexical_errors = True

    if lexical_errors:
        Log.FAIL('\nLexical errors found on compiler definition file')

    # -------------------------------------------------------
    # WRITE TOKEN FLOW FILE
    # -------------------------------------------------------
    try:
        tokens_flow_file = open('output/tokens-flow', 'w+')

        for token in TOKENS:
            if token.type == 'IGNORE':
                continue
            if token.type == 'KEYWORD':
                if token.value == '\\n':
                    continue
                    # tokens_flow_file.write('\n')
                else:
                    tokens_flow_file.write(f'{token.value}')
            elif token.type == 'space':
                # tokens_flow_file.write(f'{token.value}')
                continue
            else:
                tokens_flow_file.write(f'{token.type}')
            tokens_flow_file.write(' ')

        Log.OKGREEN('\nTokens flow file generated successfully.')
    except:
        Log.FAIL('\nThere was an error opening and writing on the file.')
        exit()
    finally:
        tokens_flow_file.close()

    Log.N('\nTokens flow file finished.')


try:
    run()
except Exception as e:
    Log.FAIL('There is an error: ', e)

instruction_word = ''
for token in TOKENS:
    if token.type == 'IGNORE':
        continue
    if token.type == 'KEYWORD':
        if token.value == '\\n':
            continue
        else:
            instruction_word += token.value
    elif token.type == 'space':
        continue
    else:
        instruction_word += token.value


print(instruction_word)
re = PRODUCTIONS['EstadoInicial0']
re_replace_index = 0

# while True:
#     print(re)

#     if AFD(re.replace('a', ANY_BUT_QUOTES)).accepts(instruction_word, CHARACTERS):
#         break

#     print("AVER", re[re_replace_index])
#     replace_re = CHARACTERS.get(re[re_replace_index])

#     if PRODUCTIONS.get(replace_re):
#         replace_re = PRODUCTIONS[replace_re]

#     if replace_re:
#         re = re.replace(re[re_replace_index], replace_re)

#     re_replace_index += 1

#     if re_replace_index >= len(re):
#         break
