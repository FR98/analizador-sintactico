# -------------------------------------------------------
# Diseño de Lenguajes de Programación
# Lexical Analyzer Generator
# Francisco Rosal - 18676
# -------------------------------------------------------

import os
import json
from log import Log
from compiler_def import CompilerDef

class AnalyzerGenerator:
    def __init__(self, compiler_def_file, entry_file):
        self.compiler_def = None
        self.FILE_LINES = []
        self.compiler_def_file = compiler_def_file
        self.entry_file = entry_file
        self.extract_compiler_def()
        self.lex_analyzer_construction()
        self.run_lex_analyzer()
        self.parser_construction()

    def add_header(self):
        self.FILE_LINES.append('# -------------------------------------------------------')
        self.FILE_LINES.append('# Diseño de Lenguajes de Programación')
        self.FILE_LINES.append('# Lexical Analyzer')
        self.FILE_LINES.append('# Francisco Rosal - 18676')
        self.FILE_LINES.append('# -------------------------------------------------------')

    def add_enter(self):
        self.FILE_LINES.append('')

    def add_line(self, line):
        self.FILE_LINES.append(line)

    def extract_compiler_def(self):
        # -------------------------------------------------------
        # Extracting content from compiler definition file
        # -------------------------------------------------------
        Log.N('\nExtracting content from compiler definition file...')

        try:
            entry_file = open(self.compiler_def_file, 'r')
        except IOError:
            Log.FAIL('\nFile not found or path is incorrect')
            exit()

        entry_file_lines = entry_file.readlines()
        entry_file.close()

        self.compiler_def = CompilerDef(entry_file_lines)

        Log.OKGREEN('\nContent extracted successfully!\n')

    def lex_analyzer_construction(self):
        # -------------------------------------------------------
        # Writing the lexical analyzer file
        # -------------------------------------------------------
        try:
            os.system('cp analyzer.template.py analyzer.py')

            characters_to_replace = ''
            characters_to_replace += 'CHARACTERS = {\n'
            for key, value in self.compiler_def.CHARACTERS.items():
                characters_to_replace += f"    '{key}': '{value}',\n"
            characters_to_replace += '}'

            keywords_to_replace = ''
            keywords_to_replace += 'KEYWORDS = {\n'
            for key, value in self.compiler_def.KEYWORDS.items():
                keywords_to_replace += f"    '{key}': '{value}',\n"
            keywords_to_replace += '}'

            tokens_re_to_replace = ''
            tokens_re_to_replace += 'TOKENS_RE = {\n'
            for key, value in self.compiler_def.TOKENS_RE.items():
                tokens_re_to_replace += f"    '{key}': '{value}',\n"
            tokens_re_to_replace += '}'

            ignore_to_replace = ''
            ignore_to_replace += 'IGNORE = {\n'
            ignore_to_replace += f"    'char_numbers': {self.compiler_def.WHITE_SPACE_DECL['char_numbers']},\n"
            ignore_to_replace += f"    'strings': {self.compiler_def.WHITE_SPACE_DECL['strings']},\n"
            ignore_to_replace += '}'

            productions_to_replace = ''
            productions_to_replace += 'PRODUCTIONS = {\n'
            for key, value in self.compiler_def.PRODUCTIONS.items():
                productions_to_replace += f"    '{key}': '{value}',\n"
            productions_to_replace += '}'

            with open('analyzer.py', 'r') as file:
                data = file.read().replace('{{COMPILER_NAME}}', self.compiler_def.COMPILER_NAME)
                data = data.replace('{{CHARACTERS}}', characters_to_replace)
                data = data.replace('{{KEYWORDS}}', keywords_to_replace)
                data = data.replace('{{TOKENS_RE}}', tokens_re_to_replace)
                data = data.replace('{{IGNORE}}', ignore_to_replace)
                data = data.replace('{{PRODUCTIONS}}', productions_to_replace)

            with open('analyzer.py', 'w') as file:
                file.write(data)

            Log.OKGREEN('\nLexical analyzer file generated successfully.\n')
        except:
            Log.FAIL('\nThere was an error opening and writing on the file.\n')
            exit()

    def run_lex_analyzer(self):
        try:
            Log.N('\n\n\n\n\n# -------------------------------------------------------')
            Log.N('\nRunning lexical analyzer...')
            os.system(f'python3 analyzer.py {self.entry_file}')
        except:
            Log.FAIL('\nThere was an error running the lexical analyzer.')
            exit()

    def parser_construction(self):
        parser_file_lines = []
        production_tokens = self.compiler_def.get_production_tokens()

        starting_production = True
        tabs = 0
        on_if = False
        current_def = None
        for token in production_tokens:
            Log.FAIL(f'{token.type} \t\t {token.value}')

            if starting_production:
                next_token = production_tokens[production_tokens.index(token) + 1]
                tabs = 1
                current_def = token.value
                if next_token.type == 'attrs':
                    ref = next_token.value.replace('<.', '').replace('.>', '').replace('ref', '').strip()
                    tabs_str = '\t' * tabs
                    parser_file_lines.append(f'{tabs_str}def {token.value}(self, {ref}):\n')
                else:
                    tabs_str = '\t' * tabs
                    parser_file_lines.append(f'{tabs_str}def {token.value}(self):\n')
                tabs = 2
            
            if token.type == 'iteration':
                if current_def == 'EstadoInicial':
                    while_condition = "self.current_token['type'] in ['numero', 'menos', '(']"
                else:
                    strings_in_iteration = []
                    for t in production_tokens[production_tokens.index(token) + 1:]:
                        if t.type == 'string':
                            strings_in_iteration.append(t.value.replace('"', ''))
                        elif t.value == '}':
                            break

                    while_condition = f"self.current_token['value'] in {strings_in_iteration}"

                if token.value == '{':
                    tabs_str = '\t' * tabs
                    parser_file_lines.append(f'{tabs_str}while {while_condition}:\n')
                    tabs += 1
                elif token.value == '}':
                    tabs -= 1

            if token.type == 'semantic_action':
                action = token.value.replace('(.', '').replace('.)', '').strip()
                if 'return' in action and on_if:
                    tabs -= 1
                    parser_file_lines.append('\n')
                tabs_str = '\t' * tabs
                parser_file_lines.append(f'{tabs_str}{action}\n')

            if token.type == 'ident' and not starting_production:
                next_token = production_tokens[production_tokens.index(token) + 1]
                if next_token.type == 'attrs':
                    ref = next_token.value.replace('<.', '').replace('.>', '').replace('ref', '').strip()
                    tabs_str = '\t' * tabs
                    parser_file_lines.append(f'{tabs_str}{ref} = self.{token.value}({ref})\n')
                else:
                    tabs_str = '\t' * tabs
                    parser_file_lines.append(f'{tabs_str}self.{token.value}()\n')

            if token.type == 'token':
                tabs_str = '\t' * tabs
                parser_file_lines.append(f'{tabs_str}{token.value} = float(self.current_token["value"])\n')
                parser_file_lines.append(f'{tabs_str}self.update_current_token()\n')

            if token.type == 'string':
                if token.value != '")"':
                    if on_if:
                        tabs -= 1

                    on_if = True
                    parser_file_lines.append('\n')
                    tabs_str = '\t' * tabs
                    parser_file_lines.append(f'{tabs_str}if self.current_token["value"] == {token.value}:\n')
                    tabs += 1
                tabs_str = '\t' * tabs
                parser_file_lines.append(f'{tabs_str}self.update_current_token()\n')

            if token.type == 'final':
                tabs = 0
                on_if = False
                parser_file_lines.append('\n')
                Log.INFO('Fin de produccion.\n')
                starting_production = True
            else:
                starting_production = False

        self.write_parser_file(parser_file_lines)

    def write_parser_file(self, parser_file_lines):
        header = [
            '# -------------------------------------------------------\n',
            '# Diseño de Lenguajes de Programación\n',
            '# Parser file generated by the compiler.\n',
            '# Francisco Rosal - 18676\n',
            '# -------------------------------------------------------\n',
            '\n',
        ]

        parser_class_header = [
            'class Parser():\n',
            '\tdef __init__(self, tokens):\n',
            '\t\tself.tokens = tokens\n',
            '\t\tself.current_token_index = 0\n',
            '\t\tself.current_token = self.tokens[self.current_token_index]\n',
            '\t\tself.EstadoInicial()\n',
            '\n',
            '\tdef update_current_token(self):\n',
            '\t\tif self.current_token_index < len(self.tokens) - 1:\n',
            '\t\t\tself.current_token_index += 1\n',
            '\t\t\tself.current_token = self.tokens[self.current_token_index]\n',
            '\n',
        ]

        try:

            with open('instruction.json', 'r') as file:
                instruction_json = json.load(file)

            class_init = [
                f'Parser({instruction_json})\n',
            ]

            with open('parser.py', 'w') as file:
                file.writelines(header)
                file.writelines(parser_class_header)
                file.writelines(parser_file_lines)
                file.writelines(class_init)
        except:
            Log.FAIL('\nThere was an error opening and writing on the file.')
            exit()
