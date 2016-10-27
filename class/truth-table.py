class TruthTable:
    def __init__(self, inputs, outputs):
        self.__input_variables = inputs
        self.__output_variables = outputs

        inputs_number = len(self.__input_variables)
        self.__inputs = []
        for i in range(2**inputs_number):
            binary = (inputs_number - len(bin(i)[2:]))*'0' + bin(i)[2:]
            self.__inputs.append(binary)


    #def __analyze__(self, priorities):

#main

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

priority = [
    {'id': 'C1', 'priority': 0},
    {'id': 'C2', 'priority': 1},
    {'id': 'C3', 'priority': 2},
    {'id': 'C4', 'priority': 3},
    {'id': 'C5', 'priority': 4}
]

x = TruthTable(potencias['supply'], potencias['charge'])
