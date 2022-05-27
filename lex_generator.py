# -------------------------------------------------------
# Diseño de Lenguajes de Programación
# Lexical Analyzer Generator
# Francisco Rosal - 18676
# -------------------------------------------------------

import os
from log import Log
from compiler_def import CompilerDef

class LexGenerator:
    def __init__(self):
        self.compiler_def = None
        self.FILE_LINES = []
        self.extract_compiler_def()
        self.lex_analyzer_construction()
        self.run_lex_analyzer()

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
            entry_file = open('input/compiler-def', 'r')
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
            os.system('cp lex-analyzer.template.py lex-analyzer.py')

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

            productions_to_replace = ''
            productions_to_replace += 'PRODUCTIONS = {\n'
            for key, value in self.compiler_def.PRODUCTIONS.items():
                productions_to_replace += f"    '{key}': '{value}',\n"
            productions_to_replace += '}'

            with open('lex-analyzer.py', 'r') as file:
                data = file.read().replace('{{COMPILER_NAME}}', self.compiler_def.COMPILER_NAME)
                data = data.replace('{{CHARACTERS}}', characters_to_replace)
                data = data.replace('{{KEYWORDS}}', keywords_to_replace)
                data = data.replace('{{TOKENS_RE}}', tokens_re_to_replace)
                data = data.replace('{{PRODUCTIONS}}', productions_to_replace)

            with open('lex-analyzer.py', 'w') as file:
                file.write(data)

            Log.OKGREEN('\nLexical analyzer file generated successfully.\n')
        except:
            Log.FAIL('\nThere was an error opening and writing on the file.\n')
            exit()

    def run_lex_analyzer(self):
        try:
            Log.N('\n\n\n\n\n# -------------------------------------------------------')
            Log.N('\nRunning lexical analyzer...')
            os.system('python3 lex-analyzer.py')
        except:
            Log.FAIL('\nThere was an error running the lexical analyzer.')
            exit()
