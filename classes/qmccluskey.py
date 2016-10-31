class QuineMcCluskey:

    def __init__(self, expression):
        self.__expression = expression

    def __group_by_ones(self):
        groups = {}
        terms_number = len(self.__expression)
        term_len = len(self.__expression[0])

        for i in range(terms_number):
            ones_number = 0
            for j in range(term_len):
                if self.__expression[i][j] == '1':
                    ones_number += 1

            if not groups.has_key(str(ones_number)):
                groups[str(ones_number)] = []
            groups[str(ones_number)].append(self.__expression[i])

        return groups

    def get_expression(self): # mudar para property
        return self.__expression


    def resolve(self):
        groups = self.__group_by_ones()
        term_len = len(self.__expression[0])
        exp = []
        execute_again = False

        print "GROUPS \n"
        print groups

        for i in range(term_len):
            if groups.has_key(str(i)) and groups.has_key(str(i + 1)):
                for k in range(len(groups[str(i)])):
                    for m in range(len(groups[str(i + 1)])):

                        diff_bit_index = 0
                        diff_bit_number = 0
                        for n in range(term_len):

                            if groups[str(i)][k][n] != groups[str(i + 1)][m][n]:
                                diff_bit_index = n
                                diff_bit_number += 1

                        if diff_bit_number == 1:
                            execute_again = True
                            term = groups[str(i)][k][:diff_bit_index] + '-' + groups[str(i)][k][diff_bit_index + 1:]
                            #print groups[str(i)][k] + " and " + groups[str(i + 1)][m] + "\n"
                            exp.append(term)

        if execute_again:
            if len(exp) > 0:
                self.__expression = list(set(exp))
            self.resolve()
        else:
            #print self.__expression
            return self.__expression
