import json

from node import Nodo

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def insertar(self, padre, nuevo_nodo, posicion):
        if posicion == 'izquierda':
            if padre.izquierdo is None:
                padre.izquierdo = nuevo_nodo
            else:
                print(f"El nodo con ID={padre.id} ya tiene un hijo izquierdo.")
        elif posicion == 'derecha':
            if padre.derecho is None:
                padre.derecho = nuevo_nodo
            else:
                print(f"El nodo con ID={padre.id} ya tiene un hijo derecho.")
        else:
            print("Posición inválida. Usa 'izquierda' o 'derecha'.")

    def insertar_secuencias(self, padre, nuevo_nodo):
        self.insertar(padre, nuevo_nodo, 'izquierda')

    def insertar_condicional(self, padre, nuevo_nodo, si_no):
        if si_no == "si":
            self.insertar(padre, nuevo_nodo, "izquierda")
        elif si_no == "no":
            self.insertar(padre, nuevo_nodo, "derecha")
        else:
            print("Valor inválido para si_no. Usa 'si' o 'no'.")

    def buscar(self, id):
        return self._buscar(self.raiz, id)

    def _buscar(self, actual, id):
        if actual is None:
            return None
        if id == actual.id:
            return actual
        elif id < actual.id:
            return self._buscar(actual.izquierdo, id)
        else:
            return self._buscar(actual.derecho, id)

    def _nodo_a_diccionario(self, nodo):
        if nodo is None:
            return None
        return {
            "id": nodo.id,
            "data": nodo.data,
            "izquierdo": self._nodo_a_diccionario(nodo.izquierdo),
            "derecho": self._nodo_a_diccionario(nodo.derecho)
        }

    def exportar_a_json(self, nombre_archivo):
        estructura = self._nodo_a_diccionario(self.raiz)
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(estructura, f, indent=4, ensure_ascii=False)
        print(f"Árbol exportado a '{nombre_archivo}'.")

arbol = ArbolBinario()
raiz = Nodo(1, "Raíz")
arbol.raiz = raiz

nodo_a = Nodo(2, "Secuencial A")
arbol.insertar_secuencias(raiz, nodo_a)

nodo_b = Nodo(3, "Secuencial B")
arbol.insertar_secuencias(nodo_a, nodo_b)

nodo_c = Nodo(4, "Condicional SI")
arbol.insertar_condicional(nodo_b, nodo_c, "si")

nodo_d = Nodo(5, "Secuencial dentro de condicional")
arbol.insertar_secuencias(nodo_c, nodo_d)

nodo_e = Nodo(6, "Secuencial posterior")
arbol.insertar_secuencias(nodo_d, nodo_e)

nodo_f = Nodo(7, "Condicional NO")
arbol.insertar_condicional(nodo_e, nodo_f, "no")

arbol.exportar_a_json("arbol_binario.json")
