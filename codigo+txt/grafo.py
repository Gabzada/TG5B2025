import numpy as np

# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 13:59:10 2023
@author: icalc
"""

class Grafo:
    TAM_MAX_DEFAULT = 1000 # qtde de vértices máxima default
    # construtor da classe grafo
    def __init__(self, n=TAM_MAX_DEFAULT):
        self.tipo = 0
        self.n = n # número de vértices
        self.m = 0 # número de arestas
        self.rotulos = {}
        self.indiceVertices = {} #id: numero
        self.verticeId = {} #numero: id
        # matriz de adjacência
        self.adj = [[0 for i in range(n)] for j in range(n)]

	# Insere uma aresta no Grafo tal que
	# v é adjacente a w
    def insereA(self, v, w, value: int = 1):
        if self.adj[v][w] == 0:
            self.adj[v][w] = value
            self.m+=1 # atualiza qtd arestas
            if self.tipo < 4:
                if self.adj[v][w] == 0:
                    self.adj[v][w] = value
                    self.adj[w][v] = value
                    self.m-=1  
            else:
                if self.adj[v][w] == 0:
                    self.adj[v][w] = value
                    self.m-=1
        else:
            print("ja existe uma aresta com essa origem e destino!")
    
    # remove uma aresta v->w do Grafo	
    def removeA(self, v, w):
        # testa se temos a aresta
        if self.tipo < 4:
            if self.adj[v][w] != 0:
                self.adj[v][w] = 0
                self.adj[w][v] = 0
                self.m-=1  
        else:
            if self.adj[v][w] != 0:
                self.adj[v][w] = 0
                self.m-=1
    
	# Apresenta o Grafo contendo
	# número de vértices, arestas
	# e a matriz de adjacência obtida	
    def show(self):
        print(f"\n n: {self.n:2d} ", end="")
        print(f"m: {self.m:2d}\n")
        for i in range(self.n):
            for w in range(self.n):
                    print(f"Adj[{i:2d},{w:2d}] = ", self.adj[i][w], " ", end="") 
            print("\n")
        print("\nfim da impressao do grafo." )


	# Apresenta o Grafo contendo
	# número de vértices, arestas
	# e a matriz de adjacência obtida 
    # Apresentando apenas os valores 0 ou 1	
    def showMin(self):
        print(f"\n n: {self.n:2d} ", end="")
        print(f"m: {self.m:2d}\n")
        for i in range(self.n):
            for w in range(self.n):
                    print(self.adj[i][w], " ", end="") 
            print("\n")
        print("\nfim da impressao do grafo." )


    def lerArquivo(self):
        f = open('grafo.txt', 'r', encoding="utf-8")
        arquivoCompleto = f.readlines()
        self.tipo = int(arquivoCompleto[0].strip())
        self.n = int(arquivoCompleto[1].strip())
        self.m = int(arquivoCompleto[2+self.n].strip())
        print(self.tipo, self.n, self.m)

        for i in range(2, 2+self.n):
            partes = arquivoCompleto[i].strip().split()
            self.indiceVertices[i-2] = int(partes[0])
            self.verticeId[int(partes[0])] = i-2
            if len(partes) == 2:
                self.rotulos[partes[0]] = partes[1]
            else:
                self.rotulos[partes[0]] = partes[0]
        
        self.adj = [[0] * self.n for _ in range(self.n)]
        
        for i in range(3+self.n, self.n+self.m+3):
            partes = arquivoCompleto[i].strip().split()
            x, y = int(partes[0])-1, int(partes[1])-1
            if self.tipo < 4:
                if len(partes) == 3:
                    self.adj[x][y] = int(partes[2])
                    self.adj[y][x] = int(partes[2])
                else:
                    self.adj[x][y] = 1
                    self.adj[y][x] = 1
            else:
                if len(partes) == 3:
                    self.adj[x][y] = int(partes[2])
                else:
                    self.adj[x][y] = 1

    def removerV(self, vertice):
        matrixTemp = [[0 for i in range(self.n - 1)] for j in range(self.n - 1)]
        for i in range(self.n):
            for j in range(self.n):
                if i > vertice and j > vertice:
                    matrixTemp[i-1][j-1] = self.adj[i][j]
                if i > vertice and j <= vertice:
                    matrixTemp[i-1][j] = self.adj[i][j]       
                elif j > vertice and i <= vertice:
                    matrixTemp[i][j-1] = self.adj[i][j]
                elif j <= vertice and i <= vertice:
                    matrixTemp[i][j] = self.adj[i][j]
        self.adj = matrixTemp
        self.n -= 1
        
    def inserirV(self, vertice):
        if vertice in self.verticeId.keys():
            print("Vertice ja existe!")       
        else:
            self.indiceVertices[self.n] = vertice
            self.verticeId[vertice] = self.n
            self.n += 1
            grafoTemp = [[0 for i in range(self.n)] for j in range(self.n)]
            for i in range(self.n - 1):
                for j in range(self.n - 1):
                    grafoTemp[i][j] = self.adj[i][j]
            
            self.adj = grafoTemp
            print("vertice criado!")


def mostrarArquivo():
    f = open('grafo.txt', 'r', encoding="utf-8")
    arquivoCompleto = f.readlines()
    for i in range(len(arquivoCompleto)):
        print(arquivoCompleto[i], end="")
    print("")
    


def main():

    grafo = Grafo()

    print("\nTodos os caminhos levam a Moscow")
    print("\n--- MENU DE OPÇÕES ---")
    print("1. Ler dados do arquivo grafo.txt")
    print("2. Gravar dados no arquivo grafo.txt")
    print("3. Inserir vértice")
    print("4. Inserir aresta")
    print("5. Remover vértice")
    print("6. Remover aresta")
    print("7. Mostrar conteúdo do arquivo")
    print("8. Mostrar grafo")
    print("9. Apresentar a conexidade do grafo e o reduzido")
    print("0. Encerrar a aplicação")

    while True:
        choice = input("Digite sua escolha: ")
        if choice == "1":
            grafo.lerArquivo()
        elif choice == "2":
            grafo.salvarArquivo()       #falta fazer esse cara aqui
        elif choice == "3":
            numero = int(input("Digite o numero do vertice = "))
            grafo.inserirV(numero)
        elif choice == "4":
            if grafo.tipo == 0:
                t = int(input("Digite o tipo de grafo = "))
                grafo.tipo = t
            elif grafo.tipo in [2, 3, 6, 7]:
                x = int(input("Digite a origem da aresta a ser inserida = "))
                y = int(input("Digite o destino da aresta a ser inserida = "))
                z = int(input("Digite o peso da aresta a ser inserida = "))
                grafo.insereA(x, y, z)
            else:
                x = int(input("Digite a origem da aresta a ser inserida = "))
                y = int(input("Digite o destino da aresta a ser inserida = "))
                grafo.insereA(x, y)
        elif choice == "5":
            print(grafo.verticeId)
            x = int(input("Digite o vertice a ser removido = "))
            x = grafo.verticeId[x]
            grafo.removerV(x)
        elif choice == "6":
            x = int(input("Digite a origem da aresta a ser removida = "))
            x = grafo.indiceVertices[x]
            y = int(input("Digite o destino da aresta a ser removida = "))
            x = grafo.indiceVertices[y]
            grafo.removeA(x, y)
        elif choice == "7":
            mostrarArquivo()
        elif choice == "8":
            grafo.show()
        elif choice == "9":
            grafo.conex()             #falta fazer esse cara aqui 
        elif choice == "0":
            print("Aplicação encerrada")
            break
        else:
            print("Escolha invalida.")

main()