class QuineMcCluskey:
    '''
    QuineMcCluskey class
        This class is used for minimization of boolean expressions.

    Attributes:
        __expression: a list with the binary terms of the expression
        __prime_implicants: a list with all essential prime implicants
    '''

    def __init__(self, expression):
        ''' This constructor initializes the class attributes. '''
        self.__expression = expression
        self.__prime_implicants = []

    def __groupByOnes(self):
        ''' __groupByOnes private method groups the miniterms of the expression by the number of ones.
            This method returns a dictionary whose indexes are the number of ones.
        '''
        groups = {}
        sorted_groups = {}
        terms_number = len(self.__expression)
        term_len = len(self.__expression[0])

        for i in range(terms_number):
            ones_number = 0
            for j in range(term_len):
                if self.__expression[i][j] == '1':
                    ones_number += 1

            if not groups.has_key(ones_number):
                groups[ones_number] = []
            groups[ones_number].append(self.__expression[i])

        for key in sorted(groups):
            sorted_groups[key] = groups[key]

        return sorted_groups

    def __initMarks(self, groups):
        ''' __initMarks private method associates to each miniterm a flag. Firstly all the flags are False. If the flag is used its
            value becomes True. Otherwise, it is held like False. This means that the term with False flag associated is a essential
            prime implicant.
        '''
        marks = {}
        for key, value in groups.iteritems():
            marks[key] = len(value)*[False]

        return marks

    def getPrimeImplicants(self):
        ''' getPrimeImplicants public method returns the essential prime implicants. '''
        return self.__prime_implicants

    def resolve(self):
        ''' resolve public method applies the Quine-McCluskey method and it finds the essential prime implicants. '''
        groups = self.__groupByOnes()
        marks = self.__initMarks(groups)
        term_len = len(self.__expression[0])
        miniterms = []
        execute_again = False

        for key_ones, terms_list in groups.iteritems():
            if groups.has_key(key_ones + 1):
                for k in range(len(terms_list)):
                    for m in range(len(groups[key_ones + 1])):
                        diff_bit_index = 0
                        diff_bit_number = 0
                        for n in range(term_len):
                            if terms_list[k][n] != groups[key_ones + 1][m][n]:
                                diff_bit_index = n
                                diff_bit_number += 1

                        if diff_bit_number == 1:
                            execute_again = True
                            term = terms_list[k][:diff_bit_index] + '-' + terms_list[k][diff_bit_index + 1:]
                            marks[key_ones][k] = True
                            marks[key_ones + 1][m] = True
                            miniterms.append(term)

        for key, mark_list in marks.iteritems():
            for index, mark in enumerate(mark_list):
                if not mark:
                    self.__prime_implicants.append(groups[key][index])


        if execute_again:
            if len(miniterms) > 0:
                self.__expression = list(set(miniterms))
            self.resolve()
        else:
            self.__prime_implicants = list(set(self.__expression + self.__prime_implicants))
