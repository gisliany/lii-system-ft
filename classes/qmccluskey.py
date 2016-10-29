class QuineMcCluskey:

    def __init__(self, expression):
        self.__expression = expression

    def __group_by_ones__(self):
        groups = {}
        terms_number = len(self.__expression)
        term_len = len(self.__expression[0])

        for i in range(terms_number):
            ones_number = 0
            for j in range(term_len):
                if self.__expression[i][j] == '1':
                    ones_number = ones_number + 1

            if not groups.has_key(str(ones_number)):
                groups[str(ones_number)] = []
            groups[str(ones_number)].append(self.__expression[i])

        return groups


    def resolve(self):
        print self.__group_by_ones__()

# main
