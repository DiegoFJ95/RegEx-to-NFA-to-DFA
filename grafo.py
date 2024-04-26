# Conversor de RegEx a NFA y a DFA.
# Elaborado por Diego Isaac Fuentes Juvera A01705506.
# El día 15 de marzo del 2024 para la materia de Implementación de métodos computacionales.

# ================================ Grafo ===============================

#Clase Directed_Graph, grafo, o autómata. Guarda un diccionario que contiene todos los estados y transiciones del autómata.
class Directed_Graph:

    def __init__(self):     # Inicializa la clase con un diccionario vacío que guardará cada nodo del grafo, sus conexiones, y sus transiciones para cada conexión.
        self.graph_dict = {}

    def add_vertex(self, vertex):   # Añade un nodo al grafo si este no existe todavía.
        if vertex in self.graph_dict:
            return "Vertex already in graph"
        else:
            self.graph_dict[vertex] = []

    def add_edge(self, edge):   # Añade una conexión al grafo.
        v1 = edge.get_v1()  # Nodo origen.
        v2 = edge.get_v2()  # Nodo destino.
        trans = edge.get_trans()    # Transición.

        if v1 not in self.graph_dict:   # Comprueba que los nodos que se quieran conectar existan en el grafo.
            raise ValueError(f"Vertex {v1.get_name()} not in graph")
        if v2 not in self.graph_dict:
            raise ValueError(f"Vertex {v2.get_name()} not in graph")
        
        self.graph_dict[v1].append([v2, trans])     # Añade la conexión al diccionario del grafo. (Añade el grafo v2 como una conexión del diccionario de conexiones del grafo v1).

    def is_vertex_in(self, vertex):     # Devuelve verdadero si el nodo existe en el grafo.
        return vertex in self.graph_dict 

    def get_vertex(self, vertex_name):  # Devuelve el nodo correspondiente a partir de una string (Ej. Buscar el nodo llamado "1" o "B").
        for v in self.graph_dict:
            if vertex_name == v.get_name():
                return v
        print(f"Vertex {vertex_name} does not exist")   # Si no lo encuentra devuelve este mensaje.

    def get_neighbours(self, vertex):   # Devuelve la lista de conexiones de un nodo.
        return self.graph_dict[vertex]
    
    def __str__(self):  # Función que se ejecuta al mandar a imprimir un objeto de la clase Directed_Graph: print(Graph).
        all_edges = ""  # Va añadiendo todos los nodos del grafo junto a sus conexiones a una string "all_edges" y la devuelve.
        accepting_states = []
        for v1 in self.graph_dict:     
            all_edges += v1.get_name() + " => ["
            first = True
            for v2 in self.graph_dict[v1]:
                if first:
                    first = False
                    all_edges += "(" + v2[0].get_name() + ", '" + v2[1].get_character() + "')"
                else:
                    all_edges += ", (" + v2[0].get_name() + ", '" + v2[1].get_character() + "')"
            all_edges += "]"
            if v1.get_end():
                accepting_states.append(v1.get_name())
            if v1.get_begin():
                all_edges += " Start"
            

            all_edges += "\n"
        all_edges += "Accepting states: ["
        first = True
        for state in accepting_states:
            if first:
                all_edges += "'" + state + "'"
            else:
                all_edges += ",'" + state + "'"
        all_edges += "]"
        return all_edges
    
    def merge_graph(self, graph):   # Función para combinar 2 grafos. Copia los nodos y conexiones del segundo grafo en el primero.
        for v in graph.graph_dict:  # Primero añade todos los nodos al diccionario.
            self.add_vertex(v)        
        for v in graph.graph_dict:  # Luego añade todas las conexiones a los nodos añadidos.
            for v2 in graph.graph_dict[v]:
                self.add_edge(Edge(v, v2[0], v2[1]))

# Clase Edge, arista, o transición.
class Edge:
    
    def __init__(self, v1, v2, trans):  # Una conexión está compuesta de 1 nodo origen, 1 nodo destino, y una transición.
        self.v1 = v1
        self.v2 = v2
        self.trans = trans

    def get_v1(self):
        return self.v1
    
    def get_v2(self):
        return self.v2
    
    def get_trans(self):
        return self.trans
    
    def __str__(self):  # Función que se ejecuta al mandar a imprimir un objeto de la clase Edge: print(eje1).
        return self.v1.get_name() + "--" + self.trans.get_character() + "->" + self.v2.get_name()
    
# Clase Vertex, vertice, nodo, o estado.
class Vertex:
    def __init__(self, name):   # Un nodo tiene nombre y puede tener 3 estados posibles: Ser el inicio del grafo, ser el final del grafo, o no ser ninguno de los 2.
        self.name = name
        self.begin = False
        self.end = False

    def get_name(self):
        return self.name
    
    def get_begin(self):
        return self.begin
    
    def set_begin(self, state):
        self.begin = state

    def get_end(self):
        return self.end

    def set_end(self, state):
        self.end = state

    def __str__(self):
        return self.name
    
# Clase Transition, transición, o costo.
class Transition:   # El objeto transición solo guarda el caracter de transición para objetos de la clase Edge.
    def __init__(self, character):
        self.character = character

    def get_character(self):
        return self.character
    
    def __str__(self):
        return self.character


# ================================ Construcción de autómatas ===============================
     

# Función para construir un automata a partir de una sola transición: a
def build_simple_automata(trans):
    g = Directed_Graph()
    global node_counter     # Contador global para saber cuantos nodos se han creado hasta el momento.

    temp_c1 = str(node_counter)     # Pasamos el número del contador a string para poder nombrar nodos con él.
    g.add_vertex(Vertex(temp_c1))   # Añadimos un nodo llamado temp_c1 (contador 1 temporal) al grafo g.
    g.get_vertex(temp_c1).set_begin(True)   # Definimos que este nuevo nodo será el inicio del grafo.
    node_counter += 1    # Añadimos uno al contador global de nodos.

    temp_c2 = str(node_counter)     # Hacemos lo mismo para este otro nodo.
    g.add_vertex(Vertex(temp_c2))
    g.get_vertex(temp_c2).set_end(True)     # Lo definimos como el final del grafo.
    node_counter += 1

    g.add_edge(Edge(g.get_vertex(temp_c1), g.get_vertex(temp_c2),Transition(trans)))    # Añadimos una conexión al grafo compuesta de los nodos inicial y final definidos previamente y de la transición que especifiquemos para el autómata.
    return g    # Regresamos el grafo de este autómata.

# Construir un automata a partir de automatas encadenados: ab.
def build_sequence_automata(g1, g2):

    g1.merge_graph(g2)  # Combinamos los 2 grafos.
    for v1 in g2.graph_dict:
            if v1.get_begin() == True:  # Revisamos el segundo grafo para encontrar su nodo de inicio.
                for v2 in g1.graph_dict:
                    if v2.get_end() == True:    # Revisamos el primer grafo para encontrar su nodo de fin
                        g1.add_edge(Edge(v2, v1, Transition("#")))  # Conectamos el nodo de fin del primer grafo con el nodo de incio del segundo.
                        v2.set_end(False)   # Establecemos que los nodos de inicio y fin que acabamos de conectar ya no lo son, pues han sido conectados.
                        v1.set_begin(False)
                        break   # Rompemos el ciclo para que no busque mas nodos de inicio y de fin.
                break
    

    return g1   # Devolvemos el primer grafo, en el que sucedieron los cambios.

# Función para construir un automata a partir de automadas agrupados por un or: s|p.
def build_or_automata(g1, g2):
    g1.merge_graph(g2)  # Combinamos los 2 grafos que son parte de la expresión or.
    global node_counter     # Llamamos a la variable global de contador de nodos.

    temp_c1 = str(node_counter)     # Creamos un nodo nuevo en base al contador.
    g1.add_vertex(Vertex(temp_c1))
    node_counter += 1

    for v in g1.graph_dict: 
        if v.get_begin() == True:   # Encontramos todos los nodos con la propiedad begin.
            g1.add_edge(Edge(g1.get_vertex(temp_c1), v, Transition("#")))   # Conectamos esos nodos al nuevo nodo que acababamos de crear.
            v.set_begin(False)  # Le quitamos la propiedad begin a los nodos que acabamos de conectar.
    
    g1.get_vertex(temp_c1).set_begin(True)  # Establecemos el nuevo nodo, ya conectado, como el inicio del grafo.

    temp_c2 = str(node_counter)     # Repetimos lo mismo pero ahora con el final del grafo, creamos un nuevo nodo.
    g1.add_vertex(Vertex(temp_c2))
    node_counter += 1

    for v in g1.graph_dict:
        if v.get_end() == True:     # Encontramos los nodos con la propiedad end.
            g1.add_edge(Edge(v, g1.get_vertex(temp_c2), Transition("#")))   # Conectamos esos nodos al nuevo nodo.
            v.set_end(False)    # Les quitamos la propiedad end.
    
    g1.get_vertex(temp_c2).set_end(True)    # Establecemos el nuevo nodo como el final del grafo.

    return g1   # Devolvemos el primer grafo, en el que sucedieron los cambios.

# Función para consturir un automata a partir de otro autómata que se pueda repetir 1 o más veces: s+.
def build_oneOrmore_automata(g):
    global node_counter

    temp_c1 = str(node_counter)     # Creamos un nuevo nodo.
    g.add_vertex(Vertex(temp_c1))
    node_counter += 1

    temp_c2 = str(node_counter)     # Creamos otro nuevo nodo.
    g.add_vertex(Vertex(temp_c2))
    node_counter += 1

    for v1 in g.graph_dict: 
        if v1.get_end() == True:
            for v2 in g.graph_dict:
                if v2.get_begin() == True:
                    g.add_edge(Edge(v1, v2, Transition("#")))   # Conectamos el último nodo del autómata al primero para que pueda haber iteraciones.
            
    for v in g.graph_dict:
        if v.get_begin() == True:
            g.add_edge(Edge(g.get_vertex(temp_c1), v, Transition("#")))     # Conectamos el primer nodo que creamos al inicio del automata.
            v.set_begin(False)  # Quitamos la propiedad begin al nodo del autómata que acabamos de conectar.

    g.get_vertex(temp_c1).set_begin(True)   # Definimos que el primer nodo que creamso yq ue acabamos de conectar es el nuevo incio del autómata.
    
    for v in g.graph_dict:
        if v.get_end() == True:
            g.add_edge(Edge(v, g.get_vertex(temp_c2), Transition("#")))     # Hacemos lo mismo pero para el segundo nodo que creamos, convirtiendolo en el final del autómata.
            v.set_end(False)

    g.get_vertex(temp_c2).set_end(True)

    return g    # Devolvemos el automata modificado.
    

# Función para construir un autómata a partir de otro automata que se pueda repetir 0 o más veces: s*.
def build_recursion_automata(g):    # Esta función es similar a la del or, pero solo requiere un grafo y además primero cree todos los nuevos nodos y luego los conecte.
    global node_counter

    temp_c1 = str(node_counter)     # Creamos un nuevo nodo.
    g.add_vertex(Vertex(temp_c1))
    node_counter += 1

    temp_c2 = str(node_counter)     # Creamos otro nuevo nodo.
    g.add_vertex(Vertex(temp_c2))
    node_counter += 1

    g.add_edge(Edge(g.get_vertex(temp_c1), g.get_vertex(temp_c2), Transition("#")))     # Conectamos el primer nodo con el último.

    for v1 in g.graph_dict: 
        if v1.get_end() == True:
            for v2 in g.graph_dict:
                if v2.get_begin() == True:
                    g.add_edge(Edge(v1, v2, Transition("#")))   # Conectamos el último nodo del autómata al primero para que pueda haber iteraciones.
            
    for v in g.graph_dict:
        if v.get_begin() == True:
            g.add_edge(Edge(g.get_vertex(temp_c1), v, Transition("#")))     # Conectamos el primer nodo que creamos al inicio del automata.
            v.set_begin(False)  # Quitamos la propiedad begin al nodo del autómata que acabamos de conectar.

    g.get_vertex(temp_c1).set_begin(True)   # Definimos que el primer nodo que creamso yq ue acabamos de conectar es el nuevo incio del autómata.
    
    for v in g.graph_dict:
        if v.get_end() == True:
            g.add_edge(Edge(v, g.get_vertex(temp_c2), Transition("#")))     # Hacemos lo mismo pero para el segundo nodo que creamos, convirtiendolo en el final del autómata.
            v.set_end(False)

    g.get_vertex(temp_c2).set_end(True)

    return g    # Devolvemos el automata modificado.

node_counter = 0    # Variable global de contador de cuantos nodos llevamos.
    
def get_prio(ch):   # Devuelve la prioridad de los operadores, siendo 1 la mas baja.
    if ch == "+":
        return 2
    elif ch == "*":
        return 2
    elif ch == "·":
        return 3
    elif ch == "|":
        return 4
    elif ch == "(":
        return 5

def do_operation(operator):     # Ejecuta transformaciones de los automatas dependiendo del operador con el que se llame. Administra los utomatas del stack para que se operen en orden correcto.
    global stack_operandos

    if operator == "|":
        a1 = stack_operandos.pop()
        a2 = stack_operandos.pop()
        stack_operandos.append(build_or_automata(a2, a1))
        return "| exitoso"
    
    elif operator == "*":
        a1 = stack_operandos.pop()
        stack_operandos.append(build_recursion_automata(a1))
        return "* exitoso"
    
    elif operator == "+":
        a1 = stack_operandos.pop()
        stack_operandos.append(build_oneOrmore_automata(a1))
        return "+ exitoso"

    elif operator == "·":
        a1 = stack_operandos.pop()
        a2 = stack_operandos.pop()
        stack_operandos.append(build_sequence_automata(a2, a1))
        return "· exitoso"


# ================================ Regex to NFA ================================


alfabetostr = input("Alphabet: ")   # Inputs del alfabeto y de la expresión.
expres = input("RegEx: ")

print("\n----RESULTS----\nINPUT:")
print(expres)

alfabeto = []
expresion = []

operadores = ["+","*","·","|","(",]     # Lista de operadores.
for letra in alfabetostr:
    alfabeto.append(letra)  # Convierte el string del alfabeto en un arreglo.

for letrar in expres:
    expresion.append(letrar)

posiciones = []
for i in range(0,len(expresion)):   # Ciclo para obtener las posiciones en las que dentro de la expresión debería ir un operador · de concatenación.

    if i != 0 and (expresion[i] in alfabeto or expresion[i] == "(") and (expresion[i-1] in alfabeto or expresion[i-1] == ")" or expresion[i-1] == "*" or expresion[i-1] == "+"):
        posiciones.append(i)

for i in range(0, len(posiciones)):     # Ciclo para insertar el operador · dentro de las posiciones obtenidas, teniendo en cuenta el desfase ocurrido por las inserciones.
    expresion.insert((posiciones[i]+i), "·") 


stack_operandos = []    # Stack donde se guardan los operandos o autómatas.
stack_operadores = []   # Stack donde se guardan los operadores.

for i in range(0,len(expresion)):   # Repite el ciclo hasta terminar de analizar toda la expresión.

    if expresion[i] in alfabeto:    # Si el caracter que estamos analizando se encuentra dentro del alfabeto.
        stack_operandos.append(build_simple_automata(expresion[i]))     # Agrega el automata de la letra que analizamos al stack de operandos.

    elif expresion[i] == "(":
            stack_operadores.append(expresion[i])
                  
    elif expresion[i] in operadores:    # Si el caracter que estamos analizando es un operador.

        
        if not stack_operadores:    # Si el stack de operadores esta vacío, añadimos el operador al stack.
            stack_operadores.append(expresion[i])

        elif get_prio(expresion[i]) < get_prio(stack_operadores[-1]):       # Si el operador que estamos analizando tiene más prioridad que el operador que está hasta arriba del stack de operadores.
            stack_operadores.append(expresion[i])                           # solo lo añadimos al stack.

        elif get_prio(expresion[i]) >= get_prio(stack_operadores[-1]):      # Si el operador que analizamos tiene menos prioridad,   
            op = stack_operadores.pop()                                     # sacamos el operador de hasta arriba del stack,
            do_operation(op)                                                # hacemos su operación correspondiente,
            stack_operadores.append(expresion[i])                           # e introducimos el operador que analizamos arriba del stack. 

    elif expresion[i] == ")":   # Si el caracter es un ")"
        while stack_operadores[-1] != "(":  # Mientras el ultimo elemento del stack de operadores no sea un "("
            op = stack_operadores.pop()     # Sacamos el ultimo operador del stack y hacemos la operación correspondiente.
            do_operation(op)   

        if stack_operadores[-1] == "(":     # Si el ultimo elemento si es un "(" entonces lo eliminamos.
            stack_operadores.pop()

while stack_operadores:             # Al finalizar de analizar la expresión, si el stack de operadores no esta vacío
    op = stack_operadores.pop()     # Sacamos los operadores uno por uno
    do_operation(op)                # Y ejecutamos sus operaciones correspondientes.

NFA = stack_operandos[-1]   # Guarda el automata que está hasta arriba del stack en la variable NFA.
print("\nNFA:")
print(NFA)


# ================================ NFA to DFA ================================ 


def cerradura(automata, v, trans):  # Función que devuelve el move (lista de estados) a partir de un estado y de una transición.
    closure = []    #Establecemos la lista donde se va guardar el resultado
    neigh = automata.get_neighbours(v)  # Obtenemos la lista de conexiones de nuestro estado.
    for i in range(0, len(neigh)):  # Recorremos cada conexión del estado
        if str(neigh[i][1]) == trans:   # Si encontramos una conexión cuya transición coincida con la transición que definimos para el move
            vert = automata.get_vertex(str(neigh[i][0]))    # Recuperamos el estado
            if vert not in closure:     # Si el estado no ha sido registrado previamente en el resultado
                closure.append(vert)    # Añadimos el estado al resultado
            closure.extend(cerradura(automata, vert, trans))    # Volvemos a llamar la función pero ahora para 
    closure.sort(key = lambda x: x.name)
    return closure

def move(automata, vlist, trans):   # Función que devuelve el move a partir de una lista de estado y una transición.
    closure = []
    for vertex in vlist:    # Mismo funcionamiento que cerradura() pero se aplica a una lista de estados.
        neigh = automata.get_neighbours(vertex)
        for i in range(0, len(neigh)):
            if str(neigh[i][1]) == trans:
                vert = automata.get_vertex(str(neigh[i][0]))
                if vert not in closure:
                    closure.append(vert)
                closure.extend(cerradura(automata, vert, trans))
    closure.sort(key = lambda x: x.name)
    return closure

def cerraduraItmem(automata, vlist, trans):     # Función que devuelve la cerradura a partir de una lista de estados. Solo se usa bajo la transición epsilon (#)
    closure = []     # Mismo funcionamiento que move() pero agrega los estadoss de entrada al resultado.
    for vertms in vlist:
        if vertms not in closure:
            closure.append(vertms)

    for vertex in vlist:
        neigh = automata.get_neighbours(vertex)

        for i in range(0, len(neigh)):
            if str(neigh[i][1]) == trans:
                vert = automata.get_vertex(str(neigh[i][0]))
                if vert not in closure:
                    closure.append(vert)
                closure.extend(cerradura(automata, vert, trans))
    closure.sort(key = lambda x: x.name)
    return closure

vlist = []
estados = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"] # Lista de nombres que pueden tener los estados del DFA
dict_estados = {}   # Diccionario donde se guardarán los datos de los estados del DFA

DFA = Directed_Graph()

def get_cerraduras(NFA):
    global dict_estados
    global estados
    global alfabeto
    global DFA

    for v in NFA.graph_dict: 
        if v.get_begin() == True:
            vlist.append(v)     # Identifica al estado inicial del NFA para empezar el proceso desde ahí. 
    cont2 = 0   # Contadores que sirven solo para nombrar estados.
    cont = 0
    dict_estados[estados[cont]] = [cerraduraItmem(NFA, vlist, "#"), "#", 0, "", estados[cont2]] # Crea un estado a partir de la cerradura epsilon del estado inicial del NFA
    # El estado lleva de nombre estados[cont], osea A. 
    # LLeva como datos:
    #   [La cerradura epsilon del estado (Lista de estados)
    #   , la transición con la que se llegó a esa lista (Caracter)
    #   , el estado del que partió para llegar a esa lista (Caracter)
    #   , el move al que se le tuvo que haber aplicado la cerradura epsilon para llegar a este estado (lista de estados)]
    #   , el nombre del estado como se mostrará al volverlo parte del grafo.

    DFA.add_vertex(Vertex(dict_estados[estados[cont]][4])) # Añadimos el estado inicial al DFA
    cont2 += 1  # Sumamos uno a los contadores ya que el primer identificador interno y externo fueron usados: "A"
    cont += 1
    continuar = True 

    while continuar:    # El ciclo continua hasta que ya no existan nuevos estados por descubrir para el DFA.
        continuar = False   # Si en esta iteración no ocurre ningún cambio, el ciclo termina.
        dict_estados_temp = dict(dict_estados)  # Hacemos una copia de los contenidos del diccionario de estados con el objetivo de poder modificar el diccionario a la vez que iteramos en él.
        
        for estado in dict_estados_temp:    # Iteramos en los estados dentro de la copia del diccionario para generar los moves.
            for i in range(0, len(alfabeto)):   # Iteramos en cada caracter del alfabeto
                
                temp = move(NFA, dict_estados[estado][0], alfabeto[i])  # Hacemos el move del estado correspondiente bajo la letra del alfabeto en la que estemos iterando. Lo guardamos en una variable temporal.

                state_already_exists = False    # Definimos una variable para comprobar si el move ya existe
                for key in dict_estados:
                    if(dict_estados[key][0] == temp):   # Si el move ya se encuentra dentro del diccionario de estados, asi lo declaramos y rompemos el ciclo
                        state_already_exists = True
                        break

                if state_already_exists == False:   # Si el move no existe aún
                    dict_estados[estados[cont]] = [temp, alfabeto[i], estado, " "]  # Agregamos el move al diccionario de estados, guardandolo como un estado provisional. 
                    continuar = True    # Al haber ocurrido un cambio en el diccionario durante esta iteración declaramos que el ciclo debe continuar.
                    cont += 1
        
        dict_estados_temp = dict(dict_estados)  # Actualizamos la copia del diccionario
        
        for estado in dict_estados_temp: 
                if dict_estados[estado][1] in alfabeto:     # Buscamos los moves en el diccionario de estados (los moves corresponden a todos los estados que tienen como transición asociada una letra del alfabeto)
                    temp = cerraduraItmem(NFA, dict_estados[estado][0], "#") # Creamos una cerradura epsilon para el move en el que estemos iterando

                    state_already_exists = False
                    for key in dict_estados:    # Comprobamos si la cerradura epsilon ya existe
                        if(dict_estados[key][0] == temp): #
                            state_already_exists = True
                            break

                    if state_already_exists == False:   # Si no existe, agragamos la cerradura al diccionario y creamos un estado correspondiente en el DFA.
                        dict_estados[estados[cont]] = [temp, "#", estado, dict_estados[estado][0], estados[cont2]] 
                        DFA.add_vertex(Vertex(dict_estados[estados[cont]][4]))
                        cont2 += 1
                        continuar = True
                        cont += 1

    for estado in dict_estados:     # Al finalizar el ciclo, iteramos en todos los estados (Tanto moves como cerraduras epsilon) del diccionario de estaods
        if dict_estados[estado][1] == "#":  # Revisamos que ese estado haya surgido de una cerradura epsilon
            for i in range(0, len(alfabeto)):   # Iteramos para cada letra del alfabeto
                temp = move(NFA, dict_estados[estado][0], alfabeto[i])  # Creamos un move correspondiente a ese estado con esa letra
                for key in dict_estados:    # Revisamos el diccionario de estados para encontrar una coincidencia, osease comprobamos el estado al que lleva el move que creamos anteriormente.
                    if dict_estados[key][1] == "#":
                        if dict_estados[key][3] == temp: 
                            DFA.add_edge(Edge(DFA.get_vertex(dict_estados[estado][4]), DFA.get_vertex(dict_estados[key][4]), Transition(alfabeto[i])))  # Al encontrar la coincidencia, creamos una transición entre el estado que creo el move y el estado que recibe ese move.
    
    for estado in dict_estados:     
        if dict_estados[estado][1] == "#":  # Buscamos los estados del DFA (los que surgen de una cerradura épsilon)
            for vertex in dict_estados[estado][0]:  # Revisamos si entre los estados del NFA que componen a ese estado del DFA está el estado inicial y el estado final.
                if vertex.get_begin() == True:
                    v = DFA.get_vertex(dict_estados[estado][4])
                    v.set_begin(True)   # Si es así, asignamos los estados del DFA según corresponde.
                if vertex.get_end() == True:
                    v = DFA.get_vertex(dict_estados[estado][4])
                    v.set_end(True) 

get_cerraduras(NFA)

print("\nDFA:")
print(DFA)