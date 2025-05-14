import Nodo

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

    def insertar_secuencias(self, id, data,padre):
        nodo = Nodo(id, data)
        self.insertar(padre, nodo, "izquierda")



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
