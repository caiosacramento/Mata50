import sys
class Estado:
    # Construtor da classe Estado
    # Args:
    #  Alfabeto da expressão regular
    #  Lista das primeiras pos(Algumas nós da árvore se juntam para representa um nó no autômato, a primeira pos determina quais nós se juntam)
    #  Id do estadp
    #  Id_final como o id da última folha

    def __init__(self, alfabeto, id_lista, id, id_final):
        self.id_set = set(id_lista)
        self.id = id
        self.transicoes = dict()
        self.final = (id_final) in self.id_set # Verdadeiro se é um estado final
        for a in alfabeto: # Inicializa o dict de transições
            self.transicoes[a] = {} 
class AFD:  # Classe do AFD, recebe o alfabeto e a árvore sintática para gerar um AFD
    def __init__(self, alfabeto, arvore):
        self.estados = []   # Contém a lista de Estados
        self.alfabeto = alfabeto    # O Alfabeto
        self.id_contador = 1    
        self.final = arvore.id_contador-1   # Tem essa subtração pois lembre que em nossa árvore temos um nó vazio
        self.computa_estados(arvore)    # Chamamos então a função de criar o autõmato
    def computa_estados(self, arvore):
        primeiro_estado = Estado(self.alfabeto, arvore.raiz.primeiraPos, self.proximo_id(), self.final) # Cria o primeiro esado
        self.estados.append(primeiro_estado)
        pilha_de_estados = [primeiro_estado]
        while len(pilha_de_estados) > 0:  # Encontra as transicoes pros estados. É aqui que novos estados vão ser criados e serão atribuitas suas transições
            estado = pilha_de_estados.pop(0)
            novos_estados = self.computa_transicoes(estado, arvore)
            for est in novos_estados:   # Com a lista de estados para criar, criamos eles e os adicionamos na pilha. Em algum momento, não terão estados
                estado_criado = Estado(self.alfabeto, est, self.proximo_id(), self.final) # novos e então acaba o loop.
                self.estados.append(estado_criado)
                pilha_de_estados.append(estado_criado)
        return
    def computa_transicoes(self, estado, arvore):
        # Essa função calcula todas as transições de um estado
        # Recebe o estado e a árvore sintática
        # Retorna uma lista de estados

        novos_estados = []  # Lista para os estados que serão criados
        for est in estado.id_set:
            if est == self.final:   #   Checa se est é igual ao id final
                continue
            operador = arvore.folhas[est]   # Busca o operador da folha(folhas são sempre letras)
            if estado.transicoes[operador] == {}:
                estado.transicoes[operador] = arvore.proximaPos[est]
            else:
                estado.transicoes[operador] = estado.transicoes[operador].union(arvore.proximaPos[est])
        for letra in self.alfabeto:
            if estado.transicoes[letra] != {}:
                flag = True
                for est in self.estados:
                    if est.id_set == estado.transicoes[letra] or estado.transicoes[letra] in novos_estados:
                        flag = False
                if flag:
                    novos_estados.append(estado.transicoes[letra])
        return novos_estados    # Retorna os novos estaods
    def computa_palavra(self, palavra): # Sunção que recebe as palavras para ver se são aceitas pelo autômato

        self.maquia_automato() # Função para deixar o autômato mais agradável e fácil de entender e trabalhar

        estado_atual= 0     # Marca o estado inicial
        while palavra != "":    # Enquanto a palavra não for vazia, processa. Basicamente faz a transição e guarda o estado onde está agora
            if len(palavra) > 1:
                estado_atual = self.estados[estado_atual].transicoes[palavra[0]]-1
            else:
                estado_atual = self.estados[estado_atual].transicoes[palavra]-1    
            palavra = palavra[1:]
        if self.estados[estado_atual].final == True: # Checa se no final do processamento da palavra chegou em um estado final.
            print("SIM")
            return
        print("NAO")
        return    
    def proximo_id(self):
        id = self.id_contador
        self.id_contador += 1
        return id
    def maquia_automato(self):
        # Apenas facilita a vizualização do automato
        flag = False
        for state in self.estados:
            for letra in self.alfabeto:
                if state.transicoes[letra] == {}:
                    flag = True
                    state.transicoes[letra] = self.id_contador
                SET = state.transicoes[letra]
                for state2 in self.estados:
                    if state2.id_set == SET:
                        state.transicoes[letra] = state2.id
        if flag:
            self.estados.append(Estado(self.alfabeto, [], self.id_contador, self.final))
            for a in self.alfabeto:
                self.estados[-1].transicoes[a] = self.estados[-1].id
class No:
    # A classe que vai representar cada nó de nossa árvore
    def __init__(self, tipo, operador, id=None, filho_esq=None, filho_dir=None):
        # Construtor da Classe Nó

        # Argumentos:
        #   tipo: pode representar "letra", "ou", "concatenação", "fecho". Sendo isso o tipo do nó na árvore
        #   operadot: Símbolo do nó(".","*","+")
        #   id: Inteiro id do nó
        #   filho_xxx: Nó representando o filho da esquerda ou direita
        
        self.id = id
        self.operador = operador
        self.tipo = tipo
        self.filho_esq = filho_esq
        self.filho_dir = filho_dir
       
        self.nulo = False  # Verdadeiro se conseguimos chegar na palavra vazia por esse nó
        
        # Abaixo são meta dados da árvore que nos ajudaram a fazer a relação entre a árvore e os autômatos 
        self.primeiraPos = set()  
        self.ultimaPos = set()  

class Arvore:
    # Essa classe controi a árvore sintática, que é muito importante para a conversão para AFD
    # Ela recebe a expressão regular como entrada
    def __init__(self, exRe):
        self.folhas = dict()    # Cria um atributo para armezar mais fácilmente as folhas
        self.id_contador = 1    # Contador de nós que são letras
        raiz_aux, lixo= self.criar_arvore(exRe) # Função de criar a árvore. A expressão regular que ela retorna deve ser vazia, ou teve algum erro
        if(lixo != []): # Não deveria acontecer
            print("Erro") 
        no_aux = No('letra', '#', id=self.contador_id())    # A nossa árvore sempre vai ter o primeiro nó como uma concatenação, o filho a esquerda
        self.raiz = No("conc", ".", None, raiz_aux, no_aux) # é a árvore normal, e o filho a direita é um nó do tipo letra com o operador "#"

        self.proximaPos = [set() for i in range(self.id_contador)] 
        self.nulo_primeiraPos_ultimaPos_proximaPos(self.raiz) # Após a árvore estar pronta, chamamos essa função para anotar os meta dados dela
    def criar_arvore(self, exRe): #Função recursiva de criar a árvore
        if (exRe != []): # Enquanto a expressão regular não for vazia, continuamos
            token = exRe[0]
            if token == ".":    # Se for uma concatenação, fazemos recursivamente o filho da esqueda e depois o da direita e deletamos o primeiro 
                del exRe[0]     # elemento da Expressão Regular, pois acabamos de analisar ele
                filho_esq, n_exRe = self.criar_arvore(exRe)
                filho_dir, nn_exRe = self.criar_arvore(n_exRe)
                return No("conc", token, None, filho_esq, filho_dir), nn_exRe
            elif token == "+":  # Mesma lógica da concatenação
                del exRe[0]
                filho_esq, n_exRe = self.criar_arvore(exRe)
                filho_dir, nn_exRe = self.criar_arvore(n_exRe)
                return No("ou", token, None, filho_esq, filho_dir), nn_exRe
            elif token == "*":  # No fecho, chamamos a função apenas para o filho da esquerda
                del exRe[0]
                filho_esq, n_exRe = self.criar_arvore(exRe)
                return No("fecho", token, None, filho_esq), n_exRe
            else: #letra    # Caso base. Aqui não chamamos a função criar_arvore() novamente
                del exRe[0]
                if(len(token) == 1): # Se a string que estamos analisando tiver apenas uma letra, criamos um nó e acabam as chamadas recursivas por enquanto
                    id  = self.contador_id()
                    self.folhas[id] = token
                    return No("letra", token, id), exRe
                else:   # Se a string que estamos analisando tiver duas ou mais letras, como "aa", "bba", "aaabc", por exemplo, transformaremos ela
                    return self.string_multipla(token), exRe # numa sequencia concatenada, transformando "aa" em "a.a", "bba" em "b.b.a" e assim em diante
        else:
            return None
    def string_multipla(self, palavra): # Função para o caso da string ter mais que uma letra. Isto é, se o elemente da lista é "aa", então temos que
        if(len(palavra) == 1):          # transforma em a concatenado com a. Esta linha é o caso base.
            id = self.contador_id()
            self.folhas[id] = palavra
            return No("letra", palavra, id)
        else:                           # Se a palavra em questão ainda for maior que uma letra apenas, criamos um nó de concatenação, com o filho a 
            id = self.contador_id()     # esquerda como letra atual(ex, se a palavra for "aaa", a letra atual é apenas "a"), e mandamos o resto("aa") para
            self.folhas[id] = palavra[0]# a recursão como o filho direito do nó
            filho_esq = No("letra", palavra[0], id)
            filho_dir = self.string_multipla(palavra[1:])
            return No("conc", ".", None, filho_esq, filho_dir)
    def contador_id(self):              # Apenas para ser um contador
        id = self.id_contador
        self.id_contador += 1
        return id
    def nulo_primeiraPos_ultimaPos_proximaPos(self, no):
        if not no:
            return
        # Segue recursivamente a esquerda
        self.nulo_primeiraPos_ultimaPos_proximaPos(no.filho_esq)
        # Segue recursivamente a direita
        self.nulo_primeiraPos_ultimaPos_proximaPos(no.filho_dir)
        #raiz
        if no.tipo == "letra":  # Se é uma folha, primeira e ultima posição serão o id desses nós
            if no.operador == "@":  # palavra vazia
                no.nulo = True
            else:
                no.primeiraPos.add(no.id)
                no.ultimaPos.add(no.id)
        elif no.tipo == "ou":   # Se é concatenação, será nulo se algum dos filhos for nulo, a primeira e a ultima posição será a união da primeira 
            no.nulo = no.filho_esq.nulo or no.filho_dir.nulo # e da ultima pos dos filhos
            no.primeiraPos = no.filho_esq.primeiraPos.union(no.filho_dir.primeiraPos)
            no.ultimaPos = no.filho_esq.ultimaPos.union(no.filho_dir.ultimaPos)
        elif no.tipo == "fecho": # Pode ser nulo, e como só tem filho a esquerda, primeira e ultima pos será igual ao dele
            no.nulo = True
            no.primeiraPos = no.filho_esq.primeiraPos
            no.ultimaPos = no.filho_esq.ultimaPos
            self.computa_proximaPos(no) # Chamamos a função de computar prox posição
        elif no.tipo == "conc": # Se é concatenação, o nó nulo tem que ter os dois filhos podendo ser nulos
            no.nulo = no.filho_esq.nulo and no.filho_dir.nulo
            if no.filho_esq.nulo: # Se o filho esq é nulo, a primeira pos é a união da primeira pos dos dois filhos
                no.primeiraPos = no.filho_esq.primeiraPos.union(no.filho_dir.primeiraPos)
            else: # Senão, é apenas a do filho esq 
                no.primeiraPos = no.filho_esq.primeiraPos
            if no.filho_dir.nulo: # Similar ao caso acima, mas para o filho direito e para a ultima pos
                no.ultimaPos = no.filho_esq.ultimaPos.union(no.filho_dir.ultimaPos)
            else:
                no.ultimaPos = no.filho_dir.ultimaPos
            self.computa_proximaPos(no) 
        return
    def computa_proximaPos(self, no): # Apenas no fecho e na concatenação chamamos essa função. Ela apenas computa o atributo de proxPos do nó
        if no.tipo == "conc":
            for i in no.filho_esq.ultimaPos:
                self.proximaPos[i] = self.proximaPos[i].union(no.filho_dir.primeiraPos)
        elif no.tipo == "fecho":
            for i in no.filho_esq.ultimaPos:
                self.proximaPos[i] = self.proximaPos[i].union(no.filho_esq.primeiraPos)
def op(caractere):
    # Diz se o char é uma letra ou um operador
    if caractere == "." or caractere =="*" or caractere =="+":
        return False
    else:
        return True
def ler_input(entrada):
    # Recebe a entrada na forma descrita pela especificação
    # Retorna duas listas, uma contendo o alfabeto e outra contendo a Expressão Regular
    alfabeto = []
    exRe = []
    
    tam = len(entrada)
    i = 0
    temp = ""

    while (i < tam):
        if (entrada[i] != " "):
            if op(entrada[i]):
                alfabeto.append(entrada[i])
            if(i+1 == tam):
                if (temp == ""):
                    exRe.append(entrada[i])
                else:
                    exRe.append(temp+entrada[i])
                    temp = ""
            elif (entrada[i+1] == " "):
                if (temp == ""):
                    exRe.append(entrada[i])
                else:
                    exRe.append(temp+entrada[i])
                    temp = ""
            else:
                temp = temp + entrada[i]
        i= i+1

    aux = set(alfabeto)
    alfabeto = list(aux)

    return alfabeto, exRe
def main(argv, expres, palavra):
    if argv ==  "-e":
        # Passo 1: Processa o input das duas Expressões Regulares
        ALFABETO1, ExRe1 = ler_input(expres)
        ALFABETO2, ExRe2 = ler_input(palavra)
        # Passo 2: Cria as árvores sintáticas das Expressões Regulares
        arv1 = Arvore(ExRe1)
        arv2 = Arvore(ExRe2)
        # Passo 3: Usa a Árvore Sintática para criar um AFD
        d1 = AFD(ALFABETO1, arv1)
        d2 = AFD(ALFABETO2, arv2)
        # Passo 4: Checa se os AFDs são equivalentes ...
        return
    elif argv == "-p":
        # Passo 1: Processa o input da Expressão Regular e da Palavra
        ALFABETO, ExRe = ler_input(expres) #Retorna o alfabeto e a expressão regular
        # Passo 2: Cria a árvore sintática
        arv = Arvore(ExRe)
        # Passo 3: Usa a arvore sintática para criar um AFD
        d = AFD(ALFABETO, arv)
        # Passo 4: Percorre o AFD para checar se a palavra pertence a Expressão Regular.
        d.computa_palavra(palavra)
    else:
        print("Argumento Inválido")

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3])