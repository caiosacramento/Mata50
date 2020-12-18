class Estado:
    # Construtor da classe estado
    # Args:
    #  Alfabeto da expressão regular
    #  Lista de folhas
    #  Id da folha

    def __init__(self, alfabeto, id_lista, id, id_terminal):
        self.id_set = set(id_lista)
        self.id = id
        self.transicoes = dict()
        print("id_terminal",id_terminal-1)
        print(self.id_set)
        #print()
        self.final = (id_terminal) in self.id_set
        for a in alfabeto:
            self.transicoes[a] = {} 
class AFD:
    def __init__(self, alfabeto, arvore):
        self.estados = []
        self.alfabeto = alfabeto
        self.id_contador = 1
        #self.final = arvore.id_contador -1
        self.final = len(arvore.folhas) +1
        self.computa_estados(arvore)
    def computa_estados(self, arvore):
        D1 = Estado(self.alfabeto, arvore.raiz.lastpos, self.proximo_id(), self.final)
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
                estado.transicoes[label] = arvore.followpos[i]
            else:
                estado.transicoes[label] = estado.transicoes[label].union(arvore.followpos[i])
        for a in self.alfabeto:
            if estado.transicoes[a] != {}:
                new = True
                for s in self.estados:
                    if s.id_set == estado.transicoes[a] or estado.transicoes[a] in new_states:
                        new = False
                if new:
                    new_states.append(estado.transicoes[a])
        return new_states
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
    def __str__(self):
        self.post_processing()
        s = ''
        for state in self.estados:
            if state.id == 1:
                s = s+'->\t'
            else:
                s = s+'\t'
            s= s+str(state.id)+' \t'
            for a in self.alfabeto:
                s=s+str(a)+' : '+str(state.transicoes[a])+' \t'
            if state.final:
                s=s+"Final State"
            s+='\n'
        return s

    def __repr__(self):
        return self.__str__()
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
        # Analisar
        self.nullable = False  # Verdadeiro se conseguimos chegar na palavra vazia por esse nó
        self.firstpos = set()  # firstpos of node (refer to documentation.md for detail).
        self.lastpos = set()  # followpos of node (refer to documentation.md for detail).

    def __repr__(self):
        '''In console string'''
        childrenCount = int(self.filho_dir != None) + int(self.filho_esq != None)
        s = "<" + "'{0}'".format(self.tipo) + ' Node with label ' + "'{0}'".format(self.operador) + ' and ' + str(
            childrenCount) + [' child', ' children'][childrenCount != 1] + "id é: "+ "'{0}'".format(self.id) + '>'
        return s
class Arvore:
    # Essa classe controi a árvore sintática, que é muito importante para a conversão para AFD
    # Ela recebe a expressão regular como entrada
    def __init__(self, exRe):
        self.folhas = dict()
        self.id_contador = 1
        self.raiz, lixo= self.criar_arvore(exRe)
        lixo = ""
        #print("Nv 0")
        #print(self.raiz)
        #print("Nv 1")
        #print(self.raiz.filho_esq)
        #print(self.raiz.filho_dir)
        #print("Nv 2")
        #print(self.raiz.filho_esq.filho_esq)
        #print(self.raiz.filho_esq.filho_dir)
        #print("Nv 3")
        #print(self.raiz.filho_esq.filho_esq.filho_esq)
        #print(self.raiz.filho_esq.filho_esq.filho_dir)
        #print("Nv 4")
        #print(self.raiz.filho_esq.filho_esq.filho_dir.filho_esq)
        #print(self.raiz.filho_esq.filho_esq.filho_dir.filho_dir)
        
        self.followpos = [set() for i in range(self.id_contador)]
        self.nullable_firstpos_lastpos_followpos(self.raiz)
        print(self.folhas)
    def criar_arvore(self, exRe):
        if (exRe != []):
            token = exRe[0]
            if token == ".":
                del exRe[0]
                filho_esq, n_exRe = self.criar_arvore(exRe)
                filho_dir, nn_exRe = self.criar_arvore(n_exRe)
                #id  = self.contador_id()
                return No("conc", token, None, filho_esq, filho_dir), nn_exRe
            elif token == "+":
                del exRe[0]
                filho_esq, n_exRe = self.criar_arvore(exRe)
                filho_dir, nn_exRe = self.criar_arvore(n_exRe)
                #id = self.contador_id()
                return No("ou", token, None, filho_esq, filho_dir), nn_exRe
            elif token == "*":
                del exRe[0]
                filho_esq, n_exRe = self.criar_arvore(exRe)
                #id  = self.contador_id()
                return No("fecho", token, None, filho_esq), n_exRe
            else: #letra
                del exRe[0]
                id  = self.contador_id()
                self.folhas[id] = token
                return No("letra", token, id), exRe
        else:
            return None
    def contador_id(self):
        id = self.id_contador
        self.id_contador += 1
        return id
    def nullable_firstpos_lastpos_followpos(self, no):
        if no== None:
            return
        # esq
        self.nullable_firstpos_lastpos_followpos(no.filho_esq)
        # dir
        self.nullable_firstpos_lastpos_followpos(no.filho_dir)
        #raiz
        if no.tipo == "letra":
            if no.operador == "@":  # empty char
                no.nullable = True
            else:
                no.firstpos.add(no.id)
                no.lastpos.add(no.id)
        elif no.tipo == "ou":
            no.nullable = no.filho_esq.nullable or no.filho_dir.nullable
            no.firstpos = no.filho_esq.firstpos.union(no.filho_dir.firstpos)
            no.lastpos = no.filho_esq.lastpos.union(no.filho_dir.lastpos)
        elif no.tipo == "fecho":
            no.nullable = True
            no.firstpos = no.filho_esq.firstpos
            no.lastpos = no.filho_esq.lastpos
            self.compute_follows(no) 
        elif no.tipo == "conc":
            no.nullable = no.filho_esq.nullable and no.filho_dir.nullable
            if no.filho_esq.nullable:
                no.firstpos = no.filho_esq.firstpos.union(no.filho_dir.firstpos)
            else:
                no.firstpos = no.filho_esq.firstpos
            if no.filho_dir.nullable:
                no.lastpos = no.filho_esq.lastpos.union(no.filho_dir.lastpos)
            else:
                no.lastpos = no.filho_dir.lastpos
            self.compute_follows(no)
        return
    def compute_follows(self, no):
        if no.tipo == "conc":
            for i in no.filho_esq.lastpos:
                self.followpos[i] = self.followpos[i].union(no.filho_dir.firstpos)
        elif no.tipo == "fecho":
            for i in no.filho_esq.lastpos:
                self.followpos[i] = self.followpos[i].union(no.filho_esq.firstpos)
def op(caractere):
    ## Diz se o char é uma letra ou um operador
    if caractere == "." or caractere =="*" or caractere =="+":
        return False
    else:
        return True
def ler_input():
    ## Recebe a entrada na forma descrita pela especificação
    ## Retorna duas listas, uma contendo o alfabeto e outra contendo a Expressão Regular
    entrada = input()
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
def main():
    # Passo 1, processa o input
    ALFABETO, ExRe = ler_input()
    arv = Arvore(ExRe)
    d = AFD(ALFABETO, arv)
    print(d)

if __name__ == "__main__":
    main()