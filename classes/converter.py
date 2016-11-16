import subprocess

class Converter:

    def __init__(self, expressions, distribution, rates, evaluation_metrics, failure_condition):
        self.__expressions = expressions
        self.__distribution = distribution
        self.__rates = rates
        self.__metrics = evaluation_metrics
        self.__condition = failure_condition
        self.__command = 'format 8\nfactor on\nftree ft_sg\n'

    def prepareCommand():


    def initSharpe(self):
        exe = subprocess.Popen(["start", "/B", "C:\Sharpe-Gui\sharpe\sharpe"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        result = exe.communicate(input=self.__command)[0]
        print result[707:-40]
