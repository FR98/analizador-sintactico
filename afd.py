# -------------------------------------------------------
# Diseño de Lenguajes de Programación
# Automatas Finitos Deterministas
# Francisco Rosal - 18676
# -------------------------------------------------------

import graphviz
import re as regex
from retree import RETree


class Estado:
    def __init__(self, val, anul, prima_pos, ult_pos, next_pos):
        self.val = val
        self.anul = anul
        self.prima_pos = prima_pos
        self.ult_pos = ult_pos
        self.next_pos = next_pos


class AFD:
    def __init__(self, re, draw=False, print_tree=False):
        self.data = {}
        self.tree = None
        self.alfabeto = []
        self.transiciones = {}
        self.print_tree = print_tree
        self.construct_tree(re)
        self.init_estados()
        self.get_transiciones()

        if draw:
            self.draw()

    def construct_tree(self, re):
        re = '«' + re + '»#'
        retree = RETree(re)
        self.tree = retree.get_tree()
        if self.print_tree:
            print(self.tree)

    def init_estados(self):
        cont = 1

        # Se inicializa el diccionario de estados
        for i in self.tree.postorder:
            self.data[str(cont)] = Estado(chr(i.value), None, None, None, [])
            i.value = cont
            cont += 1

        # Extraigo letras de la expresion
        for hoja in self.tree.leaves:
            if regex.match(r'[a-zA-Z"\'/*=.|()[\]{} ]', self.data[str(hoja.value)].val) and self.data[str(hoja.value)].val not in self.alfabeto:
                self.alfabeto.append(self.data[str(hoja.value)].val)

        self.alfabeto.sort()

        for node in self.tree.postorder:
            self.anul(node)
            self.prima_y_ult(node)
            self.next_pos(node)

    def accepts(self, word, characters):
        return self.simulacion(word, characters)

    def simulacion(self, word, characters):
        for char in word:
            belongs_to = False
            for key in self.alfabeto:
                if characters.get(key):
                    if char in characters[key]:
                        belongs_to = True
                        break
                else:
                    return False
            if not belongs_to:
                return False

        current_state = 'S0'

        for char in word:
            llave = ''
            alfabeto_key = None

            for key in self.alfabeto:
                if char in characters[key]:
                    alfabeto_key = key

            for key, value in self.transiciones.items():
                if value['name'] == current_state and value[alfabeto_key] is not None:
                    llave = key
                elif value['name'] == current_state and value[alfabeto_key] is None:
                    return False

            current_state = self.transiciones[llave][alfabeto_key]

        for key, value in self.transiciones.items():
            if value['name'] == current_state:
                states = key
                for specialChar in ['[', ']', ' ']:
                    states = states.replace(specialChar, '')
                states = states.split(',')

                return True if str(self.tree.right.value) in states else False

    def get_transiciones(self):
        # Se genera la tabla de transiciones
        cont = 0

        # El primer valor de la tabla son las primeras posiciones de la raiz del arbol
        self.transiciones[str(self.data[str(self.tree.value)].prima_pos)] = {
            'name': 'S' + str(cont),
        }

        for letra in self.alfabeto:
            self.transiciones[str(self.data[str(self.tree.value)].prima_pos)][letra] = None

        cont += 1
        continuar = True
        while (continuar):
            initial_size = len(self.transiciones)
            keys = list(self.transiciones.keys())

            for key in keys:
                for letra in self.alfabeto:
                    if self.transiciones[key][letra] is None:
                        new_state = []
                        state = key

                        for specialChar in ['[', ']', ' ']:
                            state = state.replace(specialChar, '')
                        state = state.split(',')

                        for i in state:
                            if self.data[str(i)].val == letra: new_state.append(self.data[str(i)].next_pos)

                        new_state = [item for sublist in new_state for item in sublist]
                        new_state = list(set(new_state))
                        new_state.sort()

                        if len(new_state) > 0:
                            if str(new_state) not in self.transiciones:
                                self.transiciones[str(new_state)] = {
                                    'name': 'S' + str(cont)
                                }

                                for letter in self.alfabeto:
                                    self.transiciones[str(new_state)][letter] = None

                                cont += 1
                                self.transiciones[key][letra] = self.transiciones[str(new_state)]['name']
                            else:
                                self.transiciones[key][letra] = self.transiciones[str(new_state)]['name']

            final_size = len(self.transiciones)

            if initial_size == final_size:
                continuar = not all(self.transiciones.values())

    def anul(self, node):
        # Es anul si te puede devolver Epsilon (~)
        if self.data[str(node.value)].val == '¦' and node.left and node.right:
            self.data[str(node.value)].anul = self.data[str(node.left.value)].anul or self.data[str(node.right.value)].anul
        elif self.data[str(node.value)].val == '.' and node.left and node.right:
            self.data[str(node.value)].anul = self.data[str(node.left.value)].anul and self.data[str(node.right.value)].anul
        elif self.data[str(node.value)].val in ['±', '?', '~']:
            self.data[str(node.value)].anul = True
        else:
            self.data[str(node.value)].anul = False

    def prima_y_ult(self, node):
        if self.data[str(node.value)].val in ['¦', '?'] and node.left and node.right:
            # Se obtienen todas las primeras posiciones de ambos hijos
            self.data[str(node.value)].prima_pos = [item for sublist in [self.data[str(node.left.value)].prima_pos, self.data[str(node.right.value)].prima_pos] for item in sublist]
            self.data[str(node.value)].ult_pos = [item for sublist in [self.data[str(node.left.value)].ult_pos, self.data[str(node.right.value)].ult_pos] for item in sublist]
        elif self.data[str(node.value)].val == '.' and node.left and node.right:
            if self.data[str(node.left.value)].anul:
                # Si el hijo izquierdo es anul, se obtiene la primera posición de sus hijos
                self.data[str(node.value)].prima_pos = [item for sublist in [self.data[str(node.left.value)].prima_pos, self.data[str(node.right.value)].prima_pos] for item in sublist]
            else:
                # Si el hijo izquierdo no es anul, se obtiene la primera posición del hijo izquierdo
                self.data[str(node.value)].prima_pos = [item for sublist in [self.data[str(node.left.value)].prima_pos] for item in sublist]

            if self.data[str(node.right.value)].anul:
                self.data[str(node.value)].ult_pos = [item for sublist in [self.data[str(node.left.value)].ult_pos, self.data[str(node.right.value)].ult_pos] for item in sublist]
            else:
                self.data[str(node.value)].ult_pos = [item for sublist in [self.data[str(node.right.value)].ult_pos] for item in sublist]
        elif self.data[str(node.value)].val in ['±', '+']:
            # Se obtiene la primera posición de su hijo
            self.data[str(node.value)].prima_pos = [item for sublist in [self.data[str(node.left.value)].prima_pos] for item in sublist]
            self.data[str(node.value)].ult_pos = [item for sublist in [self.data[str(node.left.value)].ult_pos] for item in sublist]
        elif self.data[str(node.value)].val == '~':
            self.data[str(node.value)].prima_pos = []
            self.data[str(node.value)].ult_pos = []
        else:
            self.data[str(node.value)].prima_pos = [node.value]
            self.data[str(node.value)].ult_pos = [node.value]

    def next_pos(self, node):
        # Para cada una de las ultimas posiciones se agregan las ultimas posiciones de sus hijos de la derecha
        if self.data[str(node.value)].val == '.' and node.left and node.right:
            for ult_pos in self.data[str(node.left.value)].ult_pos:
                for prim_pos in self.data[str(node.right.value)].prima_pos:
                    if prim_pos not in self.data[str(node.left.value)].next_pos:
                        self.data[str(ult_pos)].next_pos.append(prim_pos)

        # Para cada ultima posicion de su hijo se agregan las ultimas posiciones de sus hijos de la derecha
        elif self.data[str(node.value)].val == '±':
            for ult_pos in self.data[str(node.left.value)].ult_pos:
                for prim_pos in self.data[str(node.left.value)].prima_pos:
                    if prim_pos not in self.data[str(node.left.value)].next_pos:
                        self.data[str(ult_pos)].next_pos.append(prim_pos)

    def draw(self):
        canvas = graphviz.Digraph(comment='AFD')
        canvas.attr(rankdir='LR')

        for key in self.transiciones.keys():
            states = key
            for specialChar in ['[', ']', ' ']:
                states = states.replace(specialChar, '')
            states = states.split(',')

            if str(self.tree.right.value) in states:
                canvas.node(self.transiciones[key]['name'], self.transiciones[key]['name'], shape='doublecircle')
            else:
                canvas.node(self.transiciones[key]['name'], self.transiciones[key]['name'])

        for key, value in self.transiciones.items():
            for c in self.alfabeto:
                if value['name'] is not None and value[c] is not None:
                    canvas.edge(value['name'], value[c], c)

        canvas.view()
