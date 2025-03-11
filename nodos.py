class NodoAST:
    # Clase base para todos los nodos del AST
    pass

class NodoFuncion(NodoAST):
    # Nodo que representa una funcion
    def __init__(self, nombre, parametros, cuerpo):
        self.nombre = nombre
        self.parametros = parametros
        self.cuerpo = cuerpo

class NodoParametro(NodoAST):
    # Nodo que representa un parametro de funcion
    def __init__(self, tipo, nombre):
        self.tipo = tipo
        self.nombre = nombre

class NodoAsignacion(NodoAST):
    # Nodo que representa una asignacion de variables
    def __init__(self, nombre, expresion):
        self.nombre = nombre 
        self.expresion = expresion
        
class NodoOperacion(NodoAST):
    # Nodo que representa una operacion aritmetica
    def __init__(self, izquierda, operador, derecha):
        self.izquierda = izquierda
        self.operador = operador
        self.derecha = derecha

class NodoRetorno(NodoAST):
    # Nodo que representa la sentencia return
    def __init__(self, expresion):
        self.expresion = expresion

class NodoIdentificador(NodoAST):
    # Nodo que representa a un identificador
    def __init__(self, nombre):
        self.nombre = nombre;

class NodoNumero(NodoAST):
    # Nodo que representa un numero
    def __init__(self, valor):
        self.valor = valor
        
class NodoLlamadaFuncion(NodoAST):
    # Nodo que representa una llamada a funcion
    def __init__(self, nombre, argumentos):
        self.nombre = nombre
        self.argumentos = argumentos
        
class NodoPrograma(NodoAST):
    """
    Nodo que representa un programa completo.
    Contiene una lista de funciones.
    """
    def __init__(self, funciones):
        self.funciones = funciones