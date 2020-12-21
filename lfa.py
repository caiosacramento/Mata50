import sys
class Estado:
    # Construtor da classe Estado
    # Args:
    #  Alfabeto da expressão regular
    #  Lista de folhas
    #  Id da folha

    def __init__(self, alfabeto, id_lista, id, id_terminal):
        self.id_set = set(id_lista)
        self.id = id
        self.transicoes = dict()
        self.final = (id_terminal) in self.id_set
        for a in alfabeto:
            self.transicoes[a] = {} 
class AFD:
    def __init__(self, alfabeto, arvore):
        self.estados = []
        self.alfabeto = alfabeto
        self.id_contador = 1
        self.final = arvore.id_contador-1
        self.computa_estados(arvore)
    def computa_estados(self, arvore):
        D1 = Estado(self.alfabeto, arvore.raiz.primeiraPos, self.proximo_id(), self.final)
        self.estados.append(D1)
        queue = [D1]
        while len(queue) > 0:  # Encontra as transicoes pros estados
            st = queue.pop(0)
            new_states = self.Dtran(st, arvore)
            for s in new_states:
                state = Estado(self.alfabeto, s, self.proximo_id(), self.final)
                self.estados.append(state)
                queue.append(state)
        return
    def Dtran(self, estado, arvore):
        # Essa função calcula todas as transições de um estado
        # Recebe o estado e a árvore sintática
        # Retorna uma lista de estados

        new_states = []
        for i in estado.id_set:
            if i == self.final:
                continue
            label = arvore.folhas[i]
            if estado.transicoes[label] == {}:
                estado.transicoes[label] = arvore.proximaPos[i]
            else:
                estado.transicoes[label] = estado.transicoes[label].union(arvore.proximaPos[i])
        for a in self.alfabeto:
            if estado.transicoes[a] != {}:
                new = True
                for s in self.estados:
                    if s.id_set == estado.transicoes[a] or estado.transicoes[a] in new_states:
                        new = False
                if new:
                    new_states.append(estado.transicoes[a])
        return new_states
    def computa_palavra(self, palavra):

        self.post_processing()

        estado_atual= 0
        while palavra != "":
            if len(palavra) > 1:
                estado_atual = self.estados[estado_atual].transicoes[palavra[0]]-1
            else:
                estado_atual = self.estados[estado_atual].transicoes[palavra]-1    
            palavra = palavra[1:]
        if self.estados[estado_atual].final == True:
            print("SIM")
            return
        print("NAO")
        return    
    def proximo_id(self):
        id = self.id_contador
        self.id_contador += 1
        return id
    def post_processing(self):
        # Facilita a vizualização do automato
        has_none_state = False
        for state in self.estados:
            for a in self.alfabeto:
                if state.transicoes[a] == {}:
                    has_none_state = True
                    state.transicoes[a] = self.id_contador
                SET = state.transicoes[a]
                for state2 in self.estados:
                    if state2.id_set == SET:
                        state.transicoes[a] = state2.id
        if has_none_state:
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