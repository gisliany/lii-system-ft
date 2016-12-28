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
        self.__result = {}

    def __isEventRepeated(self, event):
        number = 0
        for row_condition in self.__condition:
            for load in row_condition['inputs']:
                for list_i in self.__expressions[load]:
                    for row in list_i:
                        for col in row:
                            number += col.count(event)
                            if number > 1:
                                return 'repeat'
        return 'basic'

    def __getDistributionFunctionSharpe(self):
        if self.__distribution == 'Steady-State Component Unavailability':
            return 'ss_unavail'
        elif self.__distribution == 'Instantaneous Component Unavailability':
            return 'inst_unavail'
        elif self.__distribution == 'Failure Rate':
            return 'exp'
        elif self.__distribution == 'Probability of Failure':
            return 'prob'
        elif self.__distribution == 'Weibull Failure Distribution':
            return 'weibull'
        elif self.__distribution == 'Erlang Distribution':
            return 'Erlang'
        elif self.__distribution == 'Hypoexponential Distribution':
            return 'hypoexp'
        elif self.__distribution == 'Hyperexponential Distribution':
            return 'hyperexp'
        elif self.__distribution == 'Mixture Distribution':
            return 'mixture'
        elif self.__distribution == 'Defective Distribution':
            return 'defective'
        elif self.__distribution == 'Oneshot Distribution':
            return 'oneshot'
        elif self.__distribution == 'Binomial Distribution':
            return 'binomial'

    def __getMetricFunctionSharpe(self, metric, parameters):
        function = ''

        if metric == 'Steady-State Unavailability' or metric == 'Probability of Occurence of the Top Event ':
            function = 'expr sysprob(ft_sg)'
        elif metric == 'Steady-State Availability':
            function = 'expr 1-sysprob(ft_sg)'
        elif metric == 'Downtime':
            function = 'expr 60*8760*sysprob(ft_sg)'
        elif metric == 'Cost of Downtime':
            functions = 'expr ' + parameters[0] + '*60*8760*sysprob(ft_sg)'
        elif metric == 'Unavailability' or metric == 'Unreliability':
            if len(parameters) > 1:
                function = 'loop t,' + str(parameters[0]) + ',' + str(parameters[1]) + ',' + str(parameters[2])
                function += '\nexpr tvalue(t;ft_sg)\nend'
            else:
                function = 'expr tvalue(' + str(parameters[0]) + ';ft_sg)'
        elif metric == 'Availability' or metric == 'Reliability':
            if len(parameters) > 1:
                function = 'loop t,' + str(parameters[0]) + ',' + str(parameters[1]) + ',' + str(parameters[2])
                function += '\nexpr 1-tvalue(t;ft_sg)\nend'
            else:
                function = 'expr 1-tvalue(' + str(parameters[0]) + ';ft_sg)'
        elif metric == 'MTTF':
            function = 'expr mean(ft_sg)'
        elif metric == 'Variance':
            function = 'expr variance(ft_sg)'
        elif metric.find('Birnbaum Importance') != -1:
            if len(parameters) > 2:
                function = 'loop t,' + str(parameters[0]) + ',' + str(parameters[1]) + ',' + str(parameters[2])
                function += '\nexpr bimpt(t;ft_sg,' + parameters[3] + ')\nend'
            else:
                function = 'expr bimpt(' + str(parameters[0]) + ';ft_sg,' + parameters[1] + ')'
        elif metric.find('Criticality Importance') != -1:
            if len(parameters) > 2:
                function = 'loop t,' + str(parameters[0]) + ',' + str(parameters[1]) + ',' + str(parameters[2])
                function += '\nexpr cimpt(t;ft_sg,' + parameters[3] + ')\nend'
            else:
                function = 'expr cimpt(' + str(parameters[0]) + ';ft_sg, ' + parameters[1] + ')'
        elif metric.find('Structural Importance') != -1:
            if len(parameters) > 2:
                function = 'loop t,' + str(parameters[0]) + ',' + str(parameters[1]) + ',' + str(parameters[2])
                function += '\nexpr simpt(t;ft_sg,' + parameters[3] + ')\nend'
            else:
                function = 'expr simpt(' + str(parameters[0]) + ';ft_sg, ' + parameters[1] + ')'

        return function

    def __listToString(self, listUsed):
        string = ''
        for item in listUsed:
            string += item + ' '

        return string[:-1]

    def getCommand(self):
        return self.__command

    def prepareCommand(self):

        # Iterating over the rates list and declaring the basic/repeat events
        for node in self.__rates:
            self.__command += self.__isEventRepeated(node['id']) + ' ' + node['id'] + ' ' + self.__getDistributionFunctionSharpe() + '('
            for r in node['rate']:
                self.__command += str(r) + ', '
            self.__command = self.__command[:-2] + ')\n'

        # Iterating over the expression dictionary to define the subtrees
        for load, expression in self.__expressions.iteritems():
            or_items = []
            self.__command += '\n'
            for row_index, row in enumerate(expression):
                and_items = []
                for col_index, col in enumerate(row):
                    if len(col) > 1:
                        gate_name = 'or_' + load + '_' + str(row_index) + '_' + str(col_index)
                        self.__command += 'or ' + gate_name + ' ' + self.__listToString(col) + '\n'
                        and_items.append(gate_name)
                    else:
                        and_items.append(col[0])

                if len(and_items) > 1:
                    gate_name = 'and_' + load + '_' + str(row_index)
                    self.__command += 'and ' + gate_name + ' ' + self.__listToString(and_items) + '\n'
                    or_items.append(gate_name)
                else:
                    or_items.append(and_items[0])

            if len(or_items) > 1:
                self.__command += 'or or_' + load + ' ' + self.__listToString(or_items) + '\n'
                self.__subtrees[load] = 'or_' + load
            else:
                self.__subtrees[load] = or_items[0]

        # Iterating over the failure condition
        for key, condition in enumerate(self.__condition):
            self.__command += '\n'
            self.__command += condition['gate'] + ' ' + condition['name'] + ' '
            if condition['k'] > 0:
                self.__command += str(condition['k']) + ', ' + str(condition['n']) + ','
            for load in condition['inputs']:
                self.__command += ' ' + self.__subtrees[load]

        self.__command += '\n\n' + 'end'

        # Iterating over the evaluation metrics to get results
        for metric in sorted(self.__metrics):
            self.__command += '\n' + self.__getMetricFunctionSharpe(metric, self.__metrics[metric]) + '\n'
        self.__command += '\n' + 'end'

    def initSharpe(self):
        print self.__command
        exe = subprocess.Popen(["start", "/B", "C:\Sharpe-Gui\sharpe\sharpe"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        result = exe.communicate(input=self.__command)[0]

        result = result[707:-3].split('\n')
        self.__result = {}
        list_results = []
        for r in result:
            if r != '\r' and r.find('--------') == -1:
                list_results.append(r.strip())

        self.__result = {}
        i = 0
        for metric in sorted(self.__metrics):
            parameters = self.__metrics[metric]
            sharpe_code = self.__getMetricFunctionSharpe(metric, parameters)

            self.__result[metric] = []
            if len(parameters) > 2:
                i += 1
                sharpe_code = sharpe_code.split('\n')[1]
                for x in range((parameters[1]/parameters[2] + 1)):
                    string = (list_results[i].replace(sharpe_code[5:] + ':', '')).strip()
                    self.__result[metric].append(float(string))
                    if x != (parameters[1]/parameters[2] + 1):
                        i += 2
            else:
                string = (list_results[i].replace(sharpe_code[5:] + ':', '')).strip()
                self.__result[metric].append(float(string))
                i += 1

        print self.__result
