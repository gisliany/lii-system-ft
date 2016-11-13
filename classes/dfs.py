class DFS:
    '''
    DFS class
        This class implements Depth-First Search to search all paths between two specific nodes.

    Attributes:
        __source: a string representing the source id
        __target: a string representing the target id
        __topology: a dictionary whoses indexes are node ids and the values are lists of adjacents nodes (id)
        __visited: a list with the ids of the visited nodes
        __paths: a list with all paths between the source and the target
    '''

    def __init__(self, source, target, topology):
        ''' This constructor initializes the class attributes. '''
        self.__source = source
        self.__target = target
        self.__topology = topology

        self.__visited = [source]
        self.__paths = []

    def getPaths(self):
        ''' getPaths public method returns a list with all paths found. '''
        return self.__paths

    def execute(self):
        ''' execute public method executes the DFS and fills the __paths attribute. '''
        nodes = self.__topology[self.__visited[-1]] # getting adjacents nodes of the last node visited

        for node in nodes:
            if node in self.__visited:
                continue
            elif node == self.__target:
                self.__paths.append(self.__visited[:])
            else:
                self.__visited.append(node)
                self.execute()
                self.__visited.pop()
