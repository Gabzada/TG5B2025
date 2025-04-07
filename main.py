class Grafo:
    TAM_MAX_DEFAULT = 1000

    def __init__(self, n=TAM_MAX_DEFAULT):
        self.tipo = 0
        self.n = n
        self.m = 0
        self.rotulos = {}
        self.indiceVertices = {}
        self.verticeId = {}
        self.adj = [[0 for i in range(n)] for j in range(n)]

    def insereA(self, v, w, value: int = 1):
        if self.adj[v][w] == 0:
            self.adj[v][w] = value
            self.m += 1
            if self.tipo < 4:
                self.adj[w][v] = value
            else:
                pass
        else:
            print("ja existe uma aresta com essa origem e destino!")

    def removeA(self, v, w):
        if self.tipo < 4:
            if self.adj[v][w] != 0:
                self.adj[v][w] = 0
                self.adj[w][v] = 0
                self.m -= 1
        else:
            if self.adj[v][w] != 0:
                self.adj[v][w] = 0
                self.m -= 1

    def show(self):
        print(f"\n n: {self.n:2d} m: {self.m:2d}\n")
        for i in range(self.n):
            for w in range(self.n):
                print(f"Adj[{i:2d},{w:2d}] = {self.adj[i][w]} ", end="")
            print("\n")
        print("\nfim da impressao do grafo.")

    def showMin(self):
        print(f"\n n: {self.n:2d} m: {self.m:2d}\n")
        for i in range(self.n):
            for w in range(self.n):
                print(self.adj[i][w], " ", end="")
            print("\n")
        print("\nfim da impressao do grafo.")

    def lerArquivo(self):
        f = open('grafo.txt', 'r', encoding="utf-8")
        arquivoCompleto = f.readlines()
        self.tipo = int(arquivoCompleto[0].strip())
        self.n = int(arquivoCompleto[1].strip())
        self.m = int(arquivoCompleto[2 + self.n].strip())

        for i in range(2, 2 + self.n):
            partes = arquivoCompleto[i].strip().split()
            self.indiceVertices[i - 2] = int(partes[0])
            self.verticeId[int(partes[0])] = i - 2
            self.rotulos[partes[0]] = partes[1] if len(partes) == 2 else partes[0]

        self.adj = [[0] * self.n for _ in range(self.n)]

        for i in range(3 + self.n, self.n + self.m + 3):
            partes = arquivoCompleto[i].strip().split()
            x, y = int(partes[0]) - 1, int(partes[1]) - 1
            peso = int(partes[2]) if len(partes) == 3 else 1
            self.adj[x][y] = peso
            if self.tipo < 4:
                self.adj[y][x] = peso

    def salvarArquivo(self):
        try:
            with open('grafo.txt', 'w', encoding="utf-8") as f:
                f.write(f"{self.tipo}\n")
                f.write(f"{self.n}\n")
                for i in range(self.n):
                    rotulo = self.rotulos.get(i, str(i + 1))
                    f.write(f"{i + 1} {rotulo}\n")
                f.write(f"{self.m}\n")
                for i in range(self.n):
                    for j in range(self.n):
                        if self.adj[i][j] != 0 and (self.tipo >= 4 or i <= j):
                            f.write(f"{i + 1} {j + 1} {self.adj[i][j]}\n")
            print("Grafo salvo com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar arquivo: {e}")

    def removerV(self, vertice):
        matrixTemp = [[0 for _ in range(self.n - 1)] for _ in range(self.n - 1)]
        for i in range(self.n):
            for j in range(self.n):
                if i > vertice and j > vertice:
                    matrixTemp[i - 1][j - 1] = self.adj[i][j]
                elif i > vertice:
                    matrixTemp[i - 1][j] = self.adj[i][j]
                elif j > vertice:
                    matrixTemp[i][j - 1] = self.adj[i][j]
                else:
                    matrixTemp[i][j] = self.adj[i][j]
        self.adj = matrixTemp
        self.n -= 1

    def inserirV(self, vertice):
        if vertice in self.verticeId:
            print("Vertice ja existe!")
        else:
            self.indiceVertices[self.n] = vertice
            self.verticeId[vertice] = self.n
            self.n += 1
            grafoTemp = [[0 for _ in range(self.n)] for _ in range(self.n)]
            for i in range(self.n - 1):
                for j in range(self.n - 1):
                    grafoTemp[i][j] = self.adj[i][j]
            self.adj = grafoTemp
            print("vertice criado!")

    def conex(self):
        if self.n == 0:
            print("Grafo vazio!")
            return

        if self.tipo < 4:
            visitados = [False] * self.n
            self._dfs_nao_direcionado(0, visitados)
            print("Grafo conexo" if all(visitados) else "Grafo desconexo")
        else:
            componentes = self.encontrar_componentes_fortemente_conexas()
            if len(componentes) == 1:
                print("Grafo fortemente conexo (C3)")
            elif self._eh_fracamente_conexo():
                if self._eh_unilateralmente_conexo_otimizado(componentes):
                    print("Grafo unilateralmente conexo (C2)")
                else:
                    print("Grafo fracamente conexo (C1)")
            else:
                print("Grafo desconexo (C0)")

            print("\nComponentes fortemente conexas:")
            for i, comp in enumerate(componentes, 1):
                vertices = [self.rotulos.get(str(v + 1), str(v + 1)) for v in comp]
                print(f"Componente {i}: {', '.join(vertices)}")

            self.mostrar_grafo_reduzido(componentes)

    def _dfs_nao_direcionado(self, v, visitados):
        visitados[v] = True
        for w in range(self.n):
            if self.adj[v][w] != 0 and not visitados[w]:
                self._dfs_nao_direcionado(w, visitados)

    def encontrar_componentes_fortemente_conexas(self):
        visitados = [False] * self.n
        ordem = []
        for v in range(self.n):
            if not visitados[v]:
                self._dfs_ordem(v, visitados, ordem)
        grafo_invertido = self._inverter_grafo()
        visitados = [False] * self.n
        componentes = []
        for v in reversed(ordem):
            if not visitados[v]:
                componente = []
                self._dfs_componente(v, visitados, componente, grafo_invertido)
                componentes.append(componente)
        return componentes

    def _dfs_ordem(self, v, visitados, ordem):
        visitados[v] = True
        for w in range(self.n):
            if self.adj[v][w] != 0 and not visitados[w]:
                self._dfs_ordem(w, visitados, ordem)
        ordem.append(v)

    def _inverter_grafo(self):
        invertido = [[0] * self.n for _ in range(self.n)]
        for v in range(self.n):
            for w in range(self.n):
                if self.adj[v][w] != 0:
                    invertido[w][v] = self.adj[v][w]
        return invertido

    def _dfs_componente(self, v, visitados, componente, grafo):
        visitados[v] = True
        componente.append(v)
        for w in range(self.n):
            if grafo[v][w] != 0 and not visitados[w]:
                self._dfs_componente(w, visitados, componente, grafo)

    def _eh_unilateralmente_conexo_otimizado(self, componentes):
        num_componentes = len(componentes)
        alcanca = [set() for _ in range(num_componentes)]
        componente_de = [0] * self.n
        for i, comp in enumerate(componentes):
            for v in comp:
                componente_de[v] = i
        for i in range(num_componentes):
            for v in componentes[i]:
                for w in range(self.n):
                    if self.adj[v][w] != 0:
                        j = componente_de[w]
                        if i != j:
                            alcanca[i].add(j)
        for i in range(num_componentes):
            for j in range(i + 1, num_componentes):
                if j not in alcanca[i] and i not in alcanca[j]:
                    return False
        return True

    def _eh_fracamente_conexo(self):
        visitados = [False] * self.n
        self._dfs_fracamente_conexo(0, visitados)
        return all(visitados)

    def _dfs_fracamente_conexo(self, v, visitados):
        visitados[v] = True
        for w in range(self.n):
            if (self.adj[v][w] != 0 or self.adj[w][v] != 0) and not visitados[w]:
                self._dfs_fracamente_conexo(w, visitados)

    def mostrar_grafo_reduzido(self, componentes):
        num_componentes = len(componentes)
        grafo_reduzido = [[0] * num_componentes for _ in range(num_componentes)]
        componente_de = [0] * self.n
        for i, componente in enumerate(componentes):
            for v in componente:
                componente_de[v] = i
        for v in range(self.n):
            for w in range(self.n):
                if self.adj[v][w] != 0 and componente_de[v] != componente_de[w]:
                    grafo_reduzido[componente_de[v]][componente_de[w]] = 1
        print("\nMatriz de adjacência do grafo reduzido:")
        for i in range(num_componentes):
            for j in range(num_componentes):
                print(grafo_reduzido[i][j], end=" ")
            print()


def mostrarArquivo():
    f = open('grafo.txt', 'r', encoding="utf-8")
    print("".join(f.readlines()))


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
            grafo.salvarArquivo()
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
            y = int(input("Digite o destino da aresta a ser removida = "))
            x = grafo.verticeId[x]
            y = grafo.verticeId[y]
            grafo.removeA(x, y)
        elif choice == "7":
            mostrarArquivo()
        elif choice == "8":
            grafo.show()
        elif choice == "9":
            grafo.conex()
        elif choice == "0":
            print("Aplicação encerrada")
            break
        else:
            print("Escolha invalida.")

main()