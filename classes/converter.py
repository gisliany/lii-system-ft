import subprocess

class Converter:

    def __init__(self, expressions, distribution, rates, evaluation_metrics, failure_condition):
        self.__expressions = expressions
        self.__distribution = distribution
        self.__rates = rates
        self.__metrics = evaluation_metrics
        self.__condition = failure_condition
        self.__command = 'format 8\nfactor on\nftree ft_sg\n'

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

    def prepareCommand(self):

        # Iterating over the rates list and declaring the basic/repeat events
        for node in self.__rates:
            #substituir repeat por metodo que verifica se evento eh basico ou repetido
            self.__command += 'repeat ' + node['id'] + ' ' + self.__getDistributionFunctionSharpe() + '('
            for r in node['rate']:
                self.__command += str(r) + ', '
            self.__command = self.__command[:-2] + ')\n'
        return self.__command

        # Iterating over the expression dictionary to define the fault tree struct



    def initSharpe(self):
        exe = subprocess.Popen(["start", "/B", "C:\Sharpe-Gui\sharpe\sharpe"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        result = exe.communicate(input=self.__command)[0]
        print result[707:-40]
