class No:
    # A classe que vai representar cada nó de nossa árvore
    def __init__(self, tipo, operador, id=None, filho_esq=None, filho_dir=None ):
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
class arvore:
    # Essa classe controi a árvore sintática, que é muito importante para a conversão para AFD
    # Ela recebe a expressão regular como entrada
    def __init__(self, exRe):
        self.raiz = self.criar_arvore(exRe)
        self.folha = dict()
        self.id_contador = 1


        #self.followpos = [set() for i in range(self.id_contador)]
        #self.postorder_nullable_firstpos_lastpos_followpos(self.raiz)
    def criar_arvore(self, exRe):
        if (exRe != []):
            token = exRe[0]
            if token == ".":
                
            elif token == "+":
                
            elif token == "*":
                
            else: #letra
                del exRe[0]
                return No("letra", token,id  = self.contador_id()), exRe
        else:
            return None
    def contador_id(self):
        id = self.id_contador
        self.id_contador += 1
        return id
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

if __name__ == "__main__":
    main()