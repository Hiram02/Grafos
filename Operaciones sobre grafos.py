from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx.drawing.nx_agraph import graphviz_layout
import pylab


#--------------------------------------------
#    MATRIZ DE ADYACENCIA PARA TWITTER
#--------------------------------------------

def borrar_espacios(linea):
    return linea.replace(" ", "")

def matriz_tw(lados):
    #crea una lista vacia para cada nueva clave
    mat_ad = defaultdict(list)
    for linea in lados:
        linea = borrar_espacios(linea)
        #elimina \n
        linea = linea.strip()
        #separa la linea en cada ',' y hace una lista con los elementos de la linea
        nodos = linea.split(',')
        #añade conexiones para cada nodo
        mat_ad[nodos[0]].append(nodos[1])
    return mat_ad


#--------------------------------------------
#    MATRIZ DE ADYACENCIA PARA Road-Net
#--------------------------------------------

def matriz(lados):
    #crea una lista vacia para cada nueva clave
    mat_ad = defaultdict(list)
    for linea in lados:
        #elimina \n
        linea = linea.strip()
        #separa la linea en cada ',' y hace una lista con los elementos de la linea
        nodos = linea.split(' ')
        #añade conexiones para cada nodo
        mat_ad[nodos[0]].append(nodos[1])
        mat_ad[nodos[1]].append(nodos[0])
    return mat_ad


#--------------------------------------------
#                  BFS
#--------------------------------------------

def bfs(diccionario, inicial, capas):
    capas = int(capas)
    visitados = [inicial]
    #contador de capas
    i = 0
    #lista de listas, en cada posicion hay una lista con los nodos en la capa i
    l = []
    l.append([inicial])
    #lista donde se guardan los lados que se crean en cada capa
    arbol = []
    while len(l[i]) >= 1:
    	#detente cuando llegues al numero de capas solicitado
        if i >= capas:
            break
        else:
        	#se crea una nueva capa, inicialmente vacia
            laux = []
            l.append(laux)
            for nodo in l[i]:
            	#nodos adyacentes a cada nodo en la capa actual (i)
                adyacentes = diccionario[nodo]
                #se revisan los nodos adyacentes
                for adyacente in adyacentes:
                	
                    #if adyacente not in visitados:
                	#si el nodo aun no ha sido visitado, se añade a la lista de visitados
                #    visitados.append(adyacente)
                    #se crea un lado solo si el nodo adyacente no ha sido visitado
                    arbol.append((nodo, adyacente))
                    #se añade el nodo a la lista que corresponde a su capa
                    l[i + 1].append(adyacente)
            
            i = i + 1
    bfs_tree = nx.Graph()
    bfs_tree.add_edges_from(arbol)
    nx.draw(bfs_tree, with_labels=True)
    return bfs_tree


#
#--------------------------------------------
#                  DFS
#--------------------------------------------

#copia sin referencia
def copy_camino(camino):
    nuevo_camino = []
    for nodo in camino:
        nuevo_camino.append(nodo)
    return nuevo_camino


def dfs(matriz, inicio, saltos, contador = int(0), camino=[], camino_largo=[]):
    saltos = int(saltos)
    #se va actualizando la lista de nodos en el camino
    camino = camino + [inicio]
    #condicion de paro 1
    if len(camino_largo) - 1 == saltos:
        return camino_largo
    #condicion de paro 2
    elif contador > 900:
        return camino_largo
    else:
        if len(camino) > len(camino_largo):
            camino_largo = copy_camino(camino)
        for nodo in matriz[inicio]:
            if nodo not in camino:
                contador = contador + 1
                camino_largo = dfs(matriz, nodo, saltos, contador, camino, camino_largo)
        return camino_largo


def dibuja_grafo_dfs(camino_largo):
    edges = []
    i = 0
    for nodo in range(len(camino_largo)):
        if i + 1 < len(camino_largo):
            origen = camino_largo[i]
            destino = camino_largo[i + 1]
            edges.append((origen,destino))
            i = i + 1
    dfs_graph = nx.Graph()
    dfs_graph.add_edges_from(edges)
    return dfs_graph, edges

def colorear_grafo_dfs(grafo, raiz):
    color_map = []
    for node in grafo:
        if node == raiz:
            color_map.append('red')
        else:
            color_map.append('blue')
    pos = nx.spring_layout(grafo, k=0.6 * 1 / np.sqrt(len(grafo.nodes())), iterations=11)
    plt.figure(3, figsize=(12, 6))
    nx.draw(grafo, node_color = color_map, node_size=220, pos=pos, width=2, edge_color="skyblue", alpha=0.6, with_labels= True)
    return grafo


#--------------------------------------------
#             Independent Set
#--------------------------------------------

def independet_set(matriz_adyacencia, inicial, tamanio):
    inicial = str(inicial)
    tamanio = int(tamanio)
    set = [inicial]
    nodos_in_set = 1
    for nodo, adyacentes in matriz_adyacencia.items():
        if nodos_in_set >= tamanio:
            break
        else:
            aux = []
            aux.append(nodo)
            aux = aux + adyacentes
            if any(i in set for i in aux):
                continue
            else:
                set.append(nodo)
                nodos_in_set = nodos_in_set + 1
    # se crea un grafo que contiene al independent set
    g = grafo(matriz_adyacencia, set, 1, [])
    #set = independent set
    return g ,set


# i es el numero de veces que se repite la funcion
def grafo(matriz, nodos, i, lados):
    nuevos_nodos = []
    for nodo in nodos:
        for adyacente in matriz[nodo]:
            lados.append((nodo, adyacente))
            nuevos_nodos.append(adyacente)
    i = i + 1
    if i == 2:
        gra = nx.Graph()
        gra.add_edges_from(lados)
        return gra
    else:
        return grafo(matriz, nuevos_nodos, i, lados)


def color(grafo, nodos_independientes, inicial):
    color_map = []
    for node in grafo:
        if node in nodos_independientes:
            if node == inicial:
                color_map.append('red')
            else:
                color_map.append('green')
        else:
            color_map.append('blue')

    pos = nx.spring_layout(grafo, k=0.6 * 1 / np.sqrt(len(grafo.nodes())), iterations=11)
    plt.figure(3, figsize=(12, 6))
    nx.draw(grafo, node_color = color_map, node_size=220, pos=pos, width=2, edge_color="seagreen", alpha=0.6, with_labels= True)
    return grafo


#--------------------------------------
# Crear grafo en forma de árbol, tomada de:
# https://stackoverflow.com/questions/29586520/can-one-get-hierarchical-graphs-from-networkx-with-python-3/29597209#29597209
#--------------------------------------

def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')
    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))
    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        if len(children)!=0:
            dx = width/len(children)
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap,
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


#--------------------------------------
#     Coloreado de grafos BFS
#--------------------------------------

def colorear_grafo(grafo, raiz):
    color_map = []
    for node in grafo:
        if node == raiz:
            color_map.append('red')
        else:
            color_map.append('blue')
#    pos = nx.spring_layout(grafo, k=0.6 * 1 / np.sqrt(len(grafo.nodes())), iterations=8)
    pos = hierarchy_pos(grafo,raiz)
    plt.figure(3, figsize=(12, 6))
    nx.draw(grafo, pos=pos, node_color = color_map, node_size=450, width=2, edge_color="seagreen", alpha=0.6, with_labels= True)
    return grafo





#--------------------------------------------
#               MAIN
#--------------------------------------------

print('+------------------------------------------------------+')
print('|              OPERACIONES SOBRE GRAFOS                |')
print('|                                                      |')
print('|             Los grafos disponibles son:              |')
print('|                                                      |')
print('|    Pulsa 1 para trabajar con el grafo "Twitter"      |')
print('|    Pulsa 2 para trabajar con el grafo "Road-Net"     |')
print('+------------------------------------------------------+')
print()
print()

opcion_grafo = input("¿Con cuál grafo quieres trabajar?")

if opcion_grafo == '1':
    print('+------------------------------------------------------+')
    print('|                  Grafo: TWITTER                      |')
    print('|                                                      |')
    print('|              OPERACIONES SOBRE GRAFOS                |')
    print('|                                                      |')
    print('|            Las opciones disponibles son:             |')
    print('|                                                      |')
    print('|         Pulsa 1 para construir un árbol BFS          |')
    print('|         Pulsa 2 para construir un camino DFS         |')
    print('|       Pulsa 3 para construir un Independent Set      |')
    print('+------------------------------------------------------+')
    print()
    print()

    opcion = input("¿Qué es lo que quieres hacer?")

    if opcion == '1':

        #------------------------------------------
        #                  BFS
        #------------------------------------------
        print('+------------------------------------------------------+')
        print('|                  Grafo: TWITTER                      |')
        print('|         Operación: Construir un árbol BFS            |')
        print('|                                                      |')
        print('|                   INSTRUCCIONES                      |')
        print('|                                                      |')
        print('|                Escoje el nodo raíz                   |')
        print('|          El rango de nodos es 1 - 580,768            |')
        print('|                                                      |')
        print('|        Escoje la cantidad de capas del árbol         |')
        print('|                                                      |')
        print('|                    NOMENCLATURA                      |')
        print('|                                                      |')
        print('|         Nodos azules = nodos del árbol BFS           |')
        print('|             Nodo rojo  = Raiz del árbol              |')
        print('+------------------------------------------------------+')
        print()
        print()

        with open("edges.edges", 'r') as lados:
            # Se crea la matriz de adyacencia
            matriz_adyacencia = matriz_tw(lados)

            inicial = input("¿Cuál es el nodo raíz?")
            tamanio = input("¿Cuál es la cantidad de capas?")
            cond_inicial = int(inicial)
            if cond_inicial > 0 and cond_inicial <= 1087562:
                arbol_bfs = bfs(matriz_adyacencia, inicial, tamanio)
#                arbol_bfs_coloreado = colorear_grafo_dfs(arbol_bfs, inicial)
                #arbol_bfs_coloreado = colorear_grafo_dfs(arbol_bfs, inicial)
                plt.show()
            else:
                print("No seleccionaste un nodo valido")

    elif opcion == '2':

        #------------------------------------------
        #                  DFS
        #------------------------------------------
        print('+------------------------------------------------------+')
        print('|                  Grafo: TWITTER                      |')
        print('|         Operación: Construir un camino DFS           |')
        print('|                                                      |')
        print('|                   INSTRUCCIONES                      |')
        print('|                                                      |')
        print('|                Escoje el nodo raíz                   |')
        print('|          El rango de nodos es 1 - 580,768            |')
        print('|                                                      |')
        print('|            Escoje la longitud del camino             |')
        print('|                                                      |')
        print('|                    NOMENCLATURA                      |')
        print('|                                                      |')
        print('|         Nodos azules = nodos del camino DFS          |')
        print('|             Nodo rojo  = Raiz del camino             |')
        print('+------------------------------------------------------+')
        print()
        print()

        with open("edges.edges", 'r') as lados:
            # Se crea la matriz de adyacencia
            matriz_adyacencia = matriz_tw(lados)

            inicial = input("¿Cuál es el nodo raíz?")
            tamanio = input("¿Cuál es la longitud del camino?")
            cond_inicial = int(inicial)
            if cond_inicial > 0 and cond_inicial <= 1087562:
                #nodos en camino dfs
                arbol_dfs = dfs(matriz_adyacencia, inicial, tamanio, contador=int(0), camino=[], camino_largo=[])
                grafo_dfs = dibuja_grafo_dfs(arbol_dfs)[0]
                grafo_dfs_coloreado = colorear_grafo_dfs(grafo_dfs, inicial)
                plt.show()
            else:
                print("No seleccionaste un nodo valido")
    elif opcion == '3':

        #---------------------------------------
        #     Independent Set
        #---------------------------------------
        print('+------------------------------------------------------+')
        print('|                   GRAFO TWITTER                      |')
        print('|      Operación: Construir un Independent set         |')
        print('|                                                      |')
        print('|                   INSTRUCCIONES                      |')
        print('|                                                      |')
        print('|Escoje un nodo que debe aparecer en el independent set|')
        print('|          El rango de nodos es 1 - 580,768            |')
        print('|                                                      |')
        print('|         Escoje el tamaño del independent set         |')
        print('|                                                      |')
        print('|                    NOMENCLATURA                      |')
        print('|                                                      |')
        print('|     Nodos verdes = Elementos del independent set     |')
        print('|       Nodo rojo  = Nodo definido por el usuario      |')
        print('|                                                      |')
        print('+------------------------------------------------------+')
        print()
        print()

        with open("edges.edges", 'r') as lados:
            # Se crea la matriz de adyacencia
            matriz_adyacencia = matriz_tw(lados)

            inicial = input("¿Cuál es el nodo que debe estar en el independent set?")
            tamanio = input("¿Cuál es la tamaño del independent set?")

            cond_inicial = int(inicial)
            if cond_inicial > 0 and cond_inicial <= 1087562:

                #independent set
                nodos_independientes = independet_set(matriz_adyacencia, inicial, tamanio)[1]
                #grafo que contiene al independent set
                grafi = independet_set(matriz_adyacencia, inicial, tamanio)[0]
                #colorear el grafo, indentificando in. set & nodo requerido
                gra = color(grafi, nodos_independientes, inicial)
#                print("Los nodos que componen al independent set son: ", nodos_independientes)
                plt.show()
            else:
                print("No seleccionaste un nodo valido")
    else:
        print("No has seleccionado una opción valida")

elif opcion_grafo == '2':



    print('+------------------------------------------------------+')
    print('|                  Grafo: ROAD-NET                     |')
    print('|                                                      |')
    print('|              OPERACIONES SOBRE GRAFOS                |')
    print('|                                                      |')
    print('|            Las opciones disponibles son:             |')
    print('|                                                      |')
    print('|         Pulsa 1 para construir un árbol BFS          |')
    print('|         Pulsa 2 para construir un camino DFS         |')
    print('|       Pulsa 3 para construir un Independent Set      |')
    print('+------------------------------------------------------+')
    print()
    print()

    opcion = input("¿Qué es lo que quieres hacer?")

    if opcion == '1':

        #------------------------------------------
        #                  BFS
        #------------------------------------------
        print('+------------------------------------------------------+')
        print('|                  Grafo: ROAD-NET                     |')
        print('|         Operación: Construir un árbol BFS            |')
        print('|                                                      |')
        print('|                   INSTRUCCIONES                      |')
        print('|                                                      |')
        print('|                Escoje el nodo raíz                   |')
        print('|         El rango de nodos es 1 - 1,087,562           |')
        print('|                                                      |')
        print('|        Escoje la cantidad de capas del árbol         |')
        print('|                                                      |')
        print('|                    NOMENCLATURA                      |')
        print('|                                                      |')
        print('|         Nodos azules = nodos del árbol BFS           |')
        print('|             Nodo rojo  = Raiz del árbol              |')
        print('+------------------------------------------------------+')
        print()
        print()

        with open("millones.mtx", 'r') as lados:
            # Se crea la matriz de adyacencia
            matriz_adyacencia = matriz(lados)

            inicial = input("¿Cuál es el nodo raíz?")
            tamanio = input("¿Cuál es la cantidad de capas?")
            cond_inicial = int(inicial)
            if cond_inicial > 0 and cond_inicial <= 1087562:
                arbol_bfs = bfs(matriz_adyacencia, inicial, tamanio)
#                arbol_bfs_coloreado = colorear_grafo_dfs(arbol_bfs, inicial)
                #arbol_bfs_coloreado = colorear_grafo_dfs(arbol_bfs, inicial)
                plt.show()
            else:
                print("No seleccionaste un nodo valido")

    elif opcion == '2':

        #------------------------------------------
        #                  DFS
        #------------------------------------------
        print('+------------------------------------------------------+')
        print('|                  Grafo: ROAD-NET                     |')
        print('|         Operación: Construir un camino DFS           |')
        print('|                                                      |')
        print('|                   INSTRUCCIONES                      |')
        print('|                                                      |')
        print('|                Escoje el nodo raíz                   |')
        print('|         El rango de nodos es 1 - 1,087,562           |')
        print('|                                                      |')
        print('|            Escoje la longitud del camino             |')
        print('|                                                      |')
        print('|                    NOMENCLATURA                      |')
        print('|                                                      |')
        print('|         Nodos azules = nodos del camino DFS          |')
        print('|             Nodo rojo  = Raiz del camino             |')
        print('+------------------------------------------------------+')
        print()
        print()

        with open("millones.mtx", 'r') as lados:
            # Se crea la matriz de adyacencia
            matriz_adyacencia = matriz(lados)

            inicial = input("¿Cuál es el nodo raíz?")
            tamanio = input("¿Cuál es la longitud del camino?")
            cond_inicial = int(inicial)
            if cond_inicial > 0 and cond_inicial <= 1087562:
                #nodos en camino dfs
                arbol_dfs = dfs(matriz_adyacencia, inicial, tamanio, contador=int(0), camino=[], camino_largo=[])
                grafo_dfs = dibuja_grafo_dfs(arbol_dfs)[0]
                grafo_dfs_coloreado = colorear_grafo_dfs(grafo_dfs, inicial)
                plt.show()
            else:
                print("No seleccionaste un nodo valido")
    elif opcion == '3':

        #---------------------------------------
        #     Independent Set
        #---------------------------------------
        print('+------------------------------------------------------+')
        print('|                   GRAFO ROAD-NET                     |')
        print('|      Operación: Construir un Independent set         |')
        print('|                                                      |')
        print('|                   INSTRUCCIONES                      |')
        print('|                                                      |')
        print('|Escoje un nodo que debe aparecer en el independent set|')
        print('|         El rango de nodos es 1 - 1,087,562           |')
        print('|                                                      |')
        print('|         Escoje el tamaño del independent set         |')
        print('|                                                      |')
        print('|                    NOMENCLATURA                      |')
        print('|                                                      |')
        print('|     Nodos verdes = Elementos del independent set     |')
        print('|       Nodo rojo  = Nodo definido por el usuario      |')
        print('|                                                      |')
        print('+------------------------------------------------------+')
        print()
        print()

        with open("millones.mtx", 'r') as lados:
            # Se crea la matriz de adyacencia
            matriz_adyacencia = matriz(lados)

            inicial = input("¿Cuál es el nodo que debe estar en el independent set?")
            tamanio = input("¿Cuál es la tamaño del independent set?")

            cond_inicial = int(inicial)
            if cond_inicial > 0 and cond_inicial <= 1087562:

                #independent set
                nodos_independientes = independet_set(matriz_adyacencia, inicial, tamanio)[1]
                #grafo que contiene al independent set
                grafi = independet_set(matriz_adyacencia, inicial, tamanio)[0]
                #colorear el grafo, indentificando in. set & nodo requerido
                gra = color(grafi, nodos_independientes, inicial)
#                print("Los nodos que componen al independent set son: ", nodos_independientes)
                plt.show()
            else:
                print("No seleccionaste un nodo valido")
    else:
        print("No has seleccionado una opción valida")
else:
    print("No has seleccionado una opción valida")