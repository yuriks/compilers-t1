class Parse:
    table = None
    
    def __init__(self, table):
        self.table = table

    def __init__(self):
        #self.table = {("#S","@$a") : ["@$a","@$+","@$b"]}
        self.table = {("#S","@$a") : ["@$a","@$+","L"], ("L","@$a") : ["@$a","@$+","@$b"]}

    def print_situation(self, mstack, minput):
        print("Stack:", mstack , "Input:", minput)

    def validateSrc(self, inputTokens):
        stack = ["@@EOF"]
        stack.append(self.chooseTheDestiny(self.table))
        inputTokens.append("@@EOF")
        
        self.print_situation(stack, inputTokens)
        for char in inputTokens:
            try:
                #Procura por uma regra na table
                s = self.table[(stack[len(stack) -1], char)]
                while len(s) > 0:
                    #não sei se vai ter regra de erro na tabela
                    #qualquer coisa apagar até o else lá
                    if s[0] == "@@ERROR":
                        print('Error:', s[1])
                        return
                    else:
                        stack.pop()
                        t = []
                        t.extend(s)
                        t.reverse()
                        for i in t:
                            stack.append(i)
                        self.print_situation(stack, inputTokens)
                    s = self.table[(stack[len(stack) -1], char)]
            except ValueError:
                pass
            except KeyError:
                pass
            
            #retira o topo da pilha e verifica com o input
            c = stack.pop()
            if c == char:
                inputTokens = inputTokens[1::]
            else:
                raise ParseException(char,c)
                return
            self.print_situation(stack, inputTokens)
        #Acabou o input, verifica se a pilha está vazia
        if (len(stack) == 0) & (len(inputTokens) == 0):
            print("Input Accept")
        else:
            print("Incorrect Input")
               
    def chooseTheDestiny(self, table):
        for x in table:
            pass
        return "#S"

    def validate(self, inputText):
        inputTokens = []
        for i in inputText:
            inputTokens.append("@$"+i)                   
        self.validateSrc(inputTokens)
   
    def setTable(self, table):
        self.table = table

class ParseException(Exception):
    def __init__(self, got, expected):
        self.got = got
        self.expected = expected

    def __str__(self):
        return "Unexpected %s. Was expecting %s." % (self.got, self.expected)


