class DFS:

    def __init__(self, source, target, topology):
        self.__source = source
        self.__target = target
        self.__topology = topology

        self.__visited = [source]
        self.__paths = []

    def execute(self):
        nodes = self.__topology[visited[-1]] #getting adjacents nodes of the last node visited

        for node in nodes:
            if node in visited:
                continue

            if node == self.__target:
                visited.append(node)
                self.__paths.append(visited)
                visited.pop()
                break
