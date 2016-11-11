from qmccluskey import QuineMcCluskey
from dfs import DFS

class TruthTable:

    def __init__(self, inputs, outputs):
        self.__input_variables = inputs
        self.__output_variables = outputs
        self.__inputs = []
        self.__outputs = []

        inputs_number = len(self.__input_variables)

        for i in range(2**inputs_number):
            binary = (inputs_number - len(bin(i)[2:]))*'0' + bin(i)[2:] #binary number of the input
            self.__inputs.append(binary)

    def analyze(self):
        inputs_number = len(self.__input_variables)
        outputs_number = len(self.__output_variables)

        for row in range(2**inputs_number):
            # The first internal loop calculates the total power provided by the supplies
            total_power_supplied = 0
            for col in range(inputs_number):
                total_power_supplied += (int(self.__inputs[row][col])*(-1) + 1)*self.__input_variables[col]['power']

            # The second internal loop calculates the outputs of the truth table. It verifies if the total
            # power supplied is enough to all charges.
            power_consumed = 0
            self.__outputs.append('')
            for col in range(outputs_number):
                power_consumed += self.__output_variables[col]['power']

                if (total_power_supplied - power_consumed < 0):
                    self.__outputs[row] += '1'
                else:
                    self.__outputs[row] += '0'

    def getOutputExpressions(self):
        expressions = []

        for col in range(len(self.__output_variables)):
            exp = []
            for row in range(2**len(self.__input_variables)):
                if self.__outputs[row][col] == '1':
                    exp.append(self.__inputs[row])

            expressions.append(exp)

        return expressions

#-----------------------------------------------------------------------------
#main

# the charges'll be sorted by their priorities
potencias = {
    'supply': [
        {'id': 'F1', 'power': 35000},
        {'id': 'F2', 'power': 25000},
        {'id': 'F3', 'power': 4000},
        {'id': 'F4', 'power': 3000},
        {'id': 'F5', 'power': 5500}
    ],
    'charge': [
        {'id': 'C1', 'power': 19200},
        {'id': 'C2', 'power': 19200},
        {'id': 'C3', 'power': 8800},
        {'id': 'C4', 'power': 5700},
        {'id': 'C5', 'power': 2700}
    ]
}

topology = {
    'S': ['T1'],
    'T1': ['S', 'L'],
    'T2': ['L', 'J1'],
    'L': ['T1', 'T2'],
    'J1': ['T2', 'J2', 'C4'],
    'J2': ['J1', 'J3', 'F5', 'C1'],
    'J3': ['J2', 'J4', 'F1', 'F3', 'C2'],
    'J4': ['J3', 'J5', 'C5',],
    'J5': ['J4', 'F2', 'F4', 'C3'],
    'F1': ['J3'],
    'F2': ['J5'],
    'F3': ['J3'],
    'F4': ['J5'],
    'F5': ['J2'],
    'C1': ['J2'],
    'C2': ['J3'],
    'C3': ['J5'],
    'C4': ['J1'],
    'C5': ['J4']
}

x = TruthTable(potencias['supply'], potencias['charge'])
x.analyze()
print x.getOutputExpressions()[1]

y = QuineMcCluskey(x.getOutputExpressions()[1])
y.resolve()
print y.get_prime_implicants()

z = DFS('F2', 'C5', topology)
z.execute()
print z.getPaths()
