"""
A tree is an undirected graph with no cycles
A graph has a set of nodes and a set of edges which are pairs of nodes

To prevent cycles:
    only add edges to graph. cannot add edge (property of tree # edges = # nodes - 1)

Need to traverse tree in desired way

Possible Remove node function

Added families dict to map nodes to a distinct number based on their parent (sibling nodes have same number)
"""

class Tree:

    def __init__(self):
        #map of parent node to set of child nodes
        
        self.adjList = dict()
        self.families = dict()
        self.root = None
    
    #add newNode to parentNode
    def addNode(self, parentNode, newNode):

        if(self.contains(newNode)):
            raise Exception("Graph contains the \"new node\"")
        
        self.adjList[parentNode].append(newNode)
        self.families[newNode] = parentNode
        print(newNode, parentNode)
        self.adjList[newNode] = []


    #add first Root node to graph (used to add first node but also can add parent to existing graph)
    def addRootNode(self, newNode):
        if self.root != None:
            self.adjList[newNode] = [self.root]
            self.families[self.root] = newNode
            
        else:
            self.adjList[newNode] = []
          
            
        self.root = newNode
        self.families[self.root] = self.root
        
        


    
    #create breadth first traversal from top down (BFS from parent node)
    def traverseBTD(self):
        queue = []

        queue.append((self.root, self.root))

        #need to add children of root to queue
        #but also children of them until no more children

        i = 0
        

        while(i < len(queue)):

            #works as expected. This needs to add pairs to the queue so visualTree can use it to make the edges
            for node in self.adjList[queue[i][1]]:
                queue.append((queue[i][1], node))
                
            i += 1

        return queue
    
    

    def getPath(self, node1, node2):
        #get path from both nodes to root. Furthest common node in sequence is the deepest common node (possible because no cycles)
        node1Path = [node1]
        node2Path = [node2]

        #path to root fron node1
        #get parent of node1 and add to path and repeat for them until root
        while(node1Path[-1] != self.root):
            #print(node1Path[-1])
            node1Path.append(self.families[node1Path[-1]])
        
        while(node2Path[-1] != self.root):
            #print(node2Path[-1])
           # print(self.families[node2])

            node2Path.append(self.families[node2Path[-1]])

        i = 0
        while(len(node1Path) > 1 and len(node2Path) > 1 and inode2Path[-1-i] == node1Path[-1-i]):
            i += 1

        commonNode = node1Path[-1-i]

        #path from node1 to node2 should be list node1Path until (inclusive) they have common node and then list (reversed) for node2Path until they have common node (exclusive)
        path = node1Path[:i+1] + node2Path[:i][::-1]

        return path

    #should not allow node in tree to be "newNode" will lead to things I have not fully thought about
    #use contains method (if want to be safe when adding node) to not allow for unknown behavior
    def contains(self, checkNode):
        for node in self.adjList.keys():
            if node == checkNode:
                return True
        return False


if __name__ == "__main__":

    myTree = Tree()

    myTree.addRootNode("a")

    myTree.addNode("a", "b1")

    myTree.addNode("b1", "b")

    myTree.addNode("a", "b2")
    myTree.addNode("a", "b3")
    
    """

    a
    |
    b1    b2     b3
    |
    b
    

    traverseBTD:   

    a
    b
    """

    print(myTree.getPath("a", "b2"))



  #ADDDDDDDDDDDDDD FUNC TO GET CHILD NODES_------------------------------------------------------------