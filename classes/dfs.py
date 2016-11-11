class DFS:

    def __init__(self, source, target, topology):
        self.__source = source
        self.__target = target
        self.__topology = topology

        self.__visited = [source]
        self.__paths = []

    def getPaths(self):
        return self.__paths

    def execute(self):
        nodes = self.__topology[self.__visited[-1]] #getting adjacents nodes of the last node visited

        for node in nodes:
            if node in self.__visited:
                continue
            elif node == self.__target:
                self.__paths.append(self.__visited[:])
            else:
                self.__visited.append(node)
                self.execute()
                self.__visited.pop()
