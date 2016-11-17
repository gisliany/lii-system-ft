import subprocess

class Converter:

    def __init__(self, expressions, distribution, rates, evaluation_metrics, failure_condition):
        self.__expressions = expressions
        self.__distribution = distribution
        self.__rates = rates
        self.__metrics = evaluation_metrics
        self.__condition = failure_condition

        self.__subtrees = {}
        self.__command = 'format 8\nfactor on\n\nftree ft_sg\n\n'

    def __isEventRepeated(self):
        #avaliar condicao de falha e expressao booleana
        pass

    def __getDistributionFunctionSharpe(self):
        if self.__distribution == "Steady-State Component Unavailability":
            return 'ss_unavail'
        elif self.__distribution == "Instantaneous Component Unavailability":
            return 'inst_unavail'
        elif self.__distribution == "Failure Rate":
            return 'exp'

    def __listToString(self, listUsed):
        string = ''
        for item in listUsed:
            string += item + ' '

        return string[:-1]

    def prepareCommand(self):

        # Iterating over the rates list and declaring the basic/repeat events
        for node in self.__rates:
            #substituir repeat por metodo que verifica se evento eh basico ou repetido
            self.__command += 'repeat ' + node['id'] + ' ' + self.__getDistributionFunctionSharpe() + '('
            for r in node['rate']:
                self.__command += str(r) + ', '
            self.__command = self.__command[:-2] + ')\n'

        # Iterating over the expression dictionary to define the subtrees
        for charge, expression in self.__expressions.iteritems():
            or_items = []
            self.__command += '\n'
            for row_index, row in enumerate(expression):
                and_items = []
                for col_index, col in enumerate(row):
                    if len(col) > 1:
                        gate_name = 'or_' + charge + '_' + str(row_index) + '_' + str(col_index)
                        self.__command += 'or ' + gate_name + ' ' + self.__listToString(col) + '\n'
                        and_items.append(gate_name)
                    else:
                        and_items.append(col[0])

                if len(and_items) > 1:
                    gate_name = 'and_' + charge + '_' + str(row_index)
                    self.__command += 'and ' + gate_name + ' ' + self.__listToString(and_items) + '\n'
                    or_items.append(gate_name)
                else:
                    or_items.append(and_items[0])

            if len(or_items) > 1:
                self.__command += 'or or_' + charge + ' ' + self.__listToString(or_items) + '\n'
                self.__subtrees[charge] = 'or_' + charge
            else:
                self.__subtrees[charge] = or_items[0]

        # Iterating over the failure condition

        return self.__command


    def initSharpe(self):
        exe = subprocess.Popen(["start", "/B", "C:\Sharpe-Gui\sharpe\sharpe"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        result = exe.communicate(input=self.__command)[0]
        print result[707:-40]
