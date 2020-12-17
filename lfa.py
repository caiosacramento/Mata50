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
        self.folha = dict()
        self.id_contador = 1
        self.raiz, doideira= self.criar_arvore(exRe)
        print(doideira)
        print("Nv 0")
        print(self.raiz)
        print("Nv 1")
        print(self.raiz.filho_esq)
        print(self.raiz.filho_dir)
        print("Nv 2")
        print(self.raiz.filho_esq.filho_esq)
        print(self.raiz.filho_esq.filho_dir)
        print("Nv 3")
        print(self.raiz.filho_esq.filho_esq.filho_esq)
        print(self.raiz.filho_esq.filho_esq.filho_dir)
        print("Nv 4")
        print(self.raiz.filho_esq.filho_esq.filho_dir.filho_esq)
        print(self.raiz.filho_esq.filho_esq.filho_dir.filho_dir)
        
        self.followpos = [set() for i in range(self.id_contador)]
        self.nullable_firstpos_lastpos_followpos(self.raiz)
    def criar_arvore(self, exRe):
        print(exRe)
        if (exRe != []):
            token = exRe[0]
            if token == ".":
                del exRe[0]
                filho_esq, n_exRe = self.criar_arvore(exRe)
                filho_dir, nn_exRe = self.criar_arvore(n_exRe)
                id  = self.contador_id()
                return No("conc", token, id, filho_esq, filho_dir), nn_exRe
            elif token == "+":
                del exRe[0]
                filho_esq, n_exRe = self.criar_arvore(exRe)
                filho_dir, nn_exRe = self.criar_arvore(n_exRe)
                id = self.contador_id()
                return No("ou", token, id, filho_esq, filho_dir), nn_exRe
            elif token == "*":
                del exRe[0]
                filho_esq, n_exRe = self.criar_arvore(exRe)
                id  = self.contador_id()
                return No("fecho", token, id, filho_esq), n_exRe
            else: #letra
                del exRe[0]
                return No("letra", token, id  = self.contador_id()), exRe
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
            self.compute_follows(no)  # Follows is only computed for star and cat nodes
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
            self.compute_follows(no)  # Follows is only computed for star and cat nodes
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
    print(ALFABETO, ExRe)
    arv = Arvore(ExRe)

if __name__ == "__main__":
    main()