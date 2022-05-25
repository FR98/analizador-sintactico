# -------------------------------------------------------
# Diseño de Lenguajes de Programación
# Log
# Francisco Rosal - 18676
# -------------------------------------------------------

class Log:
    _BLUE = '\033[94m'
    _CYAN = '\033[96m'
    _GREEN = '\033[92m'
    _YELLOW = '\033[93m'
    _RED = '\033[91m'
    _BOLD = '\033[1m'
    _UNDERLINE = '\033[4m'
    _END = '\033[0m'

    def OKBLUE(*attr):
        print(Log._BLUE, *attr, Log._END)

    def OKGREEN(*attr):
        print(Log._GREEN, *attr, Log._END)

    def INFO(*attr):
        print(Log._CYAN, *attr, Log._END)

    def WARNING(*attr):
        print(Log._YELLOW, *attr, Log._END)

    def FAIL(*attr):
        print(Log._RED, *attr, Log._END)

    def N(*attr):
        print(*attr)

    def BOLD(*attr):
        print(Log._BOLD, *attr, Log._END)

    def UNDERLINE(*attr):
        print(Log._UNDERLINE, *attr, Log._END)
