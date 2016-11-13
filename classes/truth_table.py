class TruthTable:
    '''
    TruthTable class
        This class is used to evaluate the output expressions of the charges. It's important that the charges are sorted by
        their priorities.

    Attributes:
        __input_variables: a list with all the supplies of the Smart Grid (id and power informations)
        __output_variables: a list with all the charges of the Smart Grid (id and power informations)
        __inputs: a list with all possible binary inputs
        __outputs: a list with all binary outputs
    '''

    def __init__(self, inputs, outputs):
        ''' This constructor initializes the class attributes. It fills the inputs according to number of supplies (input variables) '''
        self.__input_variables = inputs
        self.__output_variables = outputs
        self.__inputs = []
        self.__outputs = []

        inputs_number = len(self.__input_variables)

        for i in range(2**inputs_number):
            binary = (inputs_number - len(bin(i)[2:]))*'0' + bin(i)[2:] # Binary number of the input
            self.__inputs.append(binary)

    def analyze(self):
        ''' analyze public method resolves the truth table and it fills the 'outputs' attribute '''
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
        ''' getOutputExpressions public method returns all the output expressions of the charges '''
        expressions = []

        for col in range(len(self.__output_variables)):
            exp = []
            for row in range(2**len(self.__input_variables)):
                if self.__outputs[row][col] == '1':
                    exp.append(self.__inputs[row])

            expressions.append(exp)

        return expressions
