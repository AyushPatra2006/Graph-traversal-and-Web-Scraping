'''
Important!
Enter your full name (as it appears on Canvas) and NetID.  
If you are working in a group (maximum of 4 members), include the full names and NetIDs of all your partners.  
If you're working alone, enter `None` for the partner fields.
'''

'''
Project: MP4
Student 1: Ayush Patra, apatra8
Student 2: <Name>, <NETID>
Student 3: <Name>, <NETID>
Student 4: <Name>, <NETID>
'''
from collections import deque

class GraphSearcher:
    def __init__(self):
        self.visited = set()
        self.order = []

    def visit_and_get_children(self, node):
        """ 
        Leave this method as is! It will be over-written the child classes
        Each child class should perform the following:
            Record the node value in self.order AND return its children
            parameter: node
            return: children of the given node
        """
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        # 1. clear out visited set and order list
        self.visited.clear()
        self.order.clear()
        # 2. start recursive search by calling dfs_visit
        self.dfs_visit(node)
    def dfs_visit(self, node):
        # 1. if this node has already been visited, just `return` (no value necessary)
        if node in self.visited:
            return
        # 2. mark node as visited by adding it to the set
        self.visited.add(node)
        # 3. call self.visit_and_get_children(node) to get the children
        children = self.visit_and_get_children(node)
        # 4. in a loop, call dfs_visit on each of the children
        for child in children:
            self.dfs_visit(child)
    def bfs_search(self,node):
        self.visited.clear()
        self.order.clear()
        self.bfs_visit(node) 
    def bfs_visit(self, node):
        queue = deque([node])
        self.visited.add(node)

        while queue:
            current = queue.popleft()
            children = self.visit_and_get_children(current)
            for child in children:
                if child not in self.visited:
                    self.visited.add(child)
                    queue.append(child)
            
class MatrixSearcher(GraphSearcher):
    def __init__(self, df):
        super().__init__() # call constructor method of parent class
        self.df = df

    def visit_and_get_children(self, node):
        # TODO: Record the node value in self.order
        self.order.append(node)
        children = []
        for child, has_edge in self.df.loc[node].items():
            if has_edge == 1:
                children.append(child)
        # TODO: use `self.df` to determine what children the node has and append them
        return children
class FileSearcher(GraphSearcher):
    def __init__(self):
        super().__init__()
    def visit_and_get_children(self, node):
        with open(f"file_nodes/{node}", 'r') as f:
            lines = f.read().splitlines()
            value = lines[0]
            children_line = lines[1] if len(lines) > 1 else ""
            children = [child.strip() for child in children_line.split(",") if child.strip()]

        self.order.append(value)
        return children
    def concat_order(self):
        return ''.join(self.order)