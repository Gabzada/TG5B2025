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
        # Verifica se os vértices existem
        if v not in self.verticeId or w not in self.verticeId:
            print("Erro: Um ou ambos os vértices não existem no grafo")
            return

        v_idx = self.verticeId[v]
        w_idx = self.verticeId[w]

        if self.adj[v_idx][w_idx] == 0:
            self.adj[v_idx][w_idx] = value
            self.m += 1
            if self.tipo < 4:
                self.adj[w_idx][v_idx] = value
        else:
            print("Já existe uma aresta com essa origem e destino!")

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
                    # Verifica se há um rótulo diferente do número do vértice
                    vertice_id = i + 1
                    rotulo = self.rotulos.get(str(vertice_id), str(vertice_id))
                    if rotulo == str(vertice_id):
                        f.write(f"{vertice_id}\n")  # Apenas o número se não houver rótulo diferente
                    else:
                        f.write(f"{vertice_id} {rotulo}\n")
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
            print("Vértice já existe!")
        else:
            self.indiceVertices[self.n] = vertice
            self.verticeId[vertice] = self.n
            self.rotulos[str(vertice)] = str(vertice)  # Adiciona rótulo padrão
            # Expande a matriz de adjacência
            for row in self.adj:
                row.append(0)
            self.adj.append([0] * (self.n + 1))
            self.n += 1
            print("Vértice criado com sucesso!")

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


    def _obter_caminho(self, predecessores, origem, destino):
        caminho = []
        while destino != -1 and destino != origem and predecessores[destino] != -1:
            caminho.insert(0, destino)
            destino = predecessores[destino]
        if destino == origem:
            caminho.insert(0, origem)
        return caminho
    
    def dijkstra(self, origem):
        if origem not in self.verticeId:
            print("Erro: Vértice de origem não existe no grafo")
            return

        origem_idx = self.verticeId[origem]
        distancias = [float('inf')] * self.n
        predecessores = [-1] * self.n
        visitados = [False] * self.n

        distancias[origem_idx] = 0

        for _ in range(self.n):
            # Encontra o vértice não visitado com menor distância
            u = -1
            min_dist = float('inf')
            for v in range(self.n):
                if not visitados[v] and distancias[v] < min_dist:
                    min_dist = distancias[v]
                    u = v

            if u == -1:
                break

            visitados[u] = True

            # Atualiza as distâncias dos vizinhos
            for v in range(self.n):
                if self.adj[u][v] != 0 and not visitados[v]:
                    nova_distancia = distancias[u] + self.adj[u][v]
                    if nova_distancia < distancias[v]:
                        distancias[v] = nova_distancia
                        predecessores[v] = u

        # Exibe os resultados
        print("\nResultados do Algoritmo de Dijkstra:")
        print(f"Vértice de origem: {origem}")
        print("{:<10} {:<10} {:<15} {:<15}".format("Vértice", "Rótulo", "Distância", "Caminho"))
        for v in range(self.n):
            vertice_id = self.indiceVertices.get(v, v+1)
            rotulo = self.rotulos.get(str(vertice_id), str(vertice_id))
            caminho = self._obter_caminho(predecessores, origem_idx, v)
            caminho_str = " -> ".join(str(self.indiceVertices.get(i, i+1)) for i in caminho)
            print("{:<10} {:<10} {:<15} {:<15}".format(
                vertice_id, rotulo[0] if isinstance(rotulo, tuple) else rotulo, 
                distancias[v], caminho_str))

    def coloracao_sequencial(self):
        # Inicialização
        classes = []  # Lista de classes de cores (cada classe é um conjunto de vértices)
        k = 0         # Índice da classe de cor atual (começa em 0 para indexação em Python)

        # Para todos os n vértices do grafo
        for i in range(self.n):
            vertice_adicionado = False
            # Tenta adicionar o vértice à primeira classe possível
            while not vertice_adicionado:
                if k >= len(classes):
                    # Cria uma nova classe se necessário
                    classes.append(set())

                # Verifica se algum vértice da classe atual é vizinho do vértice i
                vizinhos = set()
                for w in range(self.n):
                    if self.adj[i][w] != 0 or (self.tipo < 4 and self.adj[w][i] != 0):
                        vizinhos.add(w)

                # Verifica interseção entre vizinhos e a classe atual
                if classes[k].isdisjoint(vizinhos):
                    classes[k].add(i)
                    vertice_adicionado = True
                else:
                    k += 1  # Tenta a próxima classe

            # Volta para a primeira classe para o próximo vértice
            k = 0

        # Prepara o resultado para exibição
        resultado = [-1] * self.n
        for cor, classe in enumerate(classes):
            for vertice in classe:
                resultado[vertice] = cor

        # Exibe os resultados
        print("\nColoração do Grafo (Algoritmo Sequencial):")
        print(f"Número de cores utilizadas: {len(classes)}")
        print("{:<10} {:<10} {:<10}".format("Vértice", "Rótulo", "Cor"))

        for v in range(self.n):
            vertice_id = self.indiceVertices.get(v, v+1)
            rotulo = self.rotulos.get(str(vertice_id), str(vertice_id))
            print("{:<10} {:<10} {:<10}".format(
                vertice_id, 
                rotulo[0] if isinstance(rotulo, tuple) else rotulo, 
                resultado[v] + 1))  # +1 para cores começarem em 1

        # Mostra as classes de cores
        print("\nClasses de cores:")
        for i, classe in enumerate(classes, 1):
            vertices = []
            for v in classe:
                vertice_id = self.indiceVertices.get(v, v+1)
                rotulo = self.rotulos.get(str(vertice_id), str(vertice_id))
                vertices.append(f"{vertice_id} ({rotulo[0] if isinstance(rotulo, tuple) else rotulo})")
            print(f"Classe {i}: {', '.join(vertices)}")

    def grau_vertices(self):
        print("\nGrau dos vértices:")
        print("{:<10} {:<10} {:<10} {:<15}".format("Vértice", "Rótulo", "Grau", "Tipo"))

        for v in range(self.n):
            vertice_id = self.indiceVertices.get(v, v+1)
            rotulo = self.rotulos.get(str(vertice_id), str(vertice_id))
            grau = 0

            # Calcula o grau do vértice
            for w in range(self.n):
                if self.adj[v][w] != 0:
                    grau += 1

            # Determina o tipo do vértice
            if self.tipo < 4:  # Grafo não direcionado
                tipo = "Normal"
            else:# Grafo direcionado
                grau_entrada = 0
                for u in range(self.n):
                    if self.adj[u][v] != 0:
                        grau_entrada += 1

                if grau == 0 and grau_entrada == 0:
                    tipo = "Isolado"
                elif grau == 0:
                    tipo = "Sumidouro"
                elif grau_entrada == 0:
                    tipo = "Fonte"
                else:
                    tipo = "Normal"

            print("{:<10} {:<10} {:<10} {:<15}".format(
                vertice_id, rotulo[0] if isinstance(rotulo, tuple) else rotulo, 
                grau, tipo))

    def euleriano(self):
        if self.tipo < 4:  # Grafo não direcionado
            # Verifica se o grafo é conexo
            visitados = [False] * self.n
            self._dfs_nao_direcionado(0, visitados)
            if not all(visitados):
                print("O grafo não é euleriano: não é conexo")
                return

            # Conta vértices com grau ímpar
            impares = 0
            for v in range(self.n):
                grau = 0
                for w in range(self.n):
                    if self.adj[v][w] != 0:
                        grau += 1
                if grau % 2 != 0:
                    impares += 1

            if impares == 0:
                print("O grafo é euleriano: possui ciclo euleriano")
            elif impares == 2:
                print("O grafo é semi-euleriano: possui caminho euleriano mas não ciclo")
            else:
                print(f"O grafo não é euleriano: possui {impares} vértices com grau ímpar")
        else:  # Grafo direcionado
            # Verifica se o grafo é fortemente conexo
            componentes = self.encontrar_componentes_fortemente_conexas()
            if len(componentes) != 1:
                print("O grafo não é euleriano: não é fortemente conexo")
                return

            # Verifica graus de entrada e saída
            euleriano = True
            for v in range(self.n):
                grau_saida = 0
                grau_entrada = 0
                for w in range(self.n):
                    if self.adj[v][w] != 0:
                        grau_saida += 1
                    if self.adj[w][v] != 0:
                        grau_entrada += 1

                if grau_saida != grau_entrada:
                    euleriano = False
                    break

            if euleriano:
                print("O grafo é euleriano: possui ciclo euleriano direcionado")
            else:
                print("O grafo não é euleriano: graus de entrada e saída não são iguais para todos os vértices")

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
    print("10. Executar Algoritmo de Dijkstra")
    print("11. Realizar Coloração do Grafo")
    print("12. Mostrar Grau dos Vértices")
    print("13. Verificar se o Grafo é Euleriano")
    print("0. Encerrar a aplicação")

    while True:
        choice = input("Digite sua escolha: ")
        if choice == "1":
            grafo.lerArquivo()
            print("\nDados do arquivo grafo.txt lidos com sucesso!")
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
        elif choice == "10":
            origem = int(input("Digite o vértice de origem para o algoritmo de Dijkstra: "))
            grafo.dijkstra(origem)
        elif choice == "11":
            grafo.coloracao_sequencial()
        elif choice == "12":
            grafo.grau_vertices()
        elif choice == "13":
            grafo.euleriano()
        elif choice == "0":
            print("Aplicação encerrada")
            break
        else:
            print("Escolha inválida.")

main()