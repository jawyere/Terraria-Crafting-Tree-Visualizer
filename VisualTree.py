from Tree import Tree
import pygame
from Node import Node
import math



"""
A visualTree has a Tree and uses it to display the tree on a window

Like Tree, needs to add node and traverse tree
I also want it to zoom in to specific parts of the tree

addRootNode
addNode
zoom
Traverse (multiple) (may use zoom)
createScreen


lots of nice visual effects/ smooth looking
"""


class VisualTree:

    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800

    
    

    def __init__(self, tree, layer_len = 100, xSep = 60, name = "Tree Visualizer"):

        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 800
        self.clock = pygame.time.Clock()
        self.running = True
        self.myTree = tree
        self.curNode = 0
        self.traversalNode = 0
        self.nodesToDraw = set()
        self.offset = 0.0
        self.heldKeys = set()
      
        
        self.nextX = 0
        self.xSep = xSep
        self.layerLen = layer_len

     
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
        self.screen.fill((255, 255, 255))
        pygame.display.set_caption(name)


    def addRootNode(self, root):
        self.myTree.addRootNode(root)
    
    def addNode(self, parentNode, newNode):
        self.myTree.addNode(parentNode,newNode)
    

    def spaceXpos(self):

        self.nextX = 0  
        self.assign(self.myTree.root, 0)


    def assign(self, node, depth):
        node.y = depth * self.layerLen  

        children = self.myTree.adjList.get(node, [])
        if not children:
            #get next x value
            node.x = self.nextX
            self.nextX += 1 * self.xSep
        else:
            # Recursively position all children
            for child in children:
                self.assign(child, depth + 1)

            # Center this node based on its children
            minX = children[0].x
            maxX = children[-1].x
            node.x = (minX + maxX) / 2

    def update(self):
        self.screen.fill((255, 255, 255))
        self.draw()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYUP:
                 self.heldKeys.remove(event.key)

            if event.type == pygame.KEYDOWN:
                self.heldKeys.add(event.key)

                if event.key == pygame.K_1:
                    self.addNextNode()

                if event.key == pygame.K_2:
                    self.addAllNodes()  

                if event.key == pygame.K_0:
                    self.clearNodes() 

        if pygame.K_4 in self.heldKeys:
            self.center(self.myTree.root)

        self.traverseBTD() 
      
        self.checkZoom()
        self.updateMovement()


        pygame.display.flip()


    def updateMovement(self):

        changeTime = self.clock.get_time()/1000
        sensitivity = 300
        self.offset = sensitivity * changeTime
       

        if pygame.K_LEFT in self.heldKeys:
            for node in self.myTree.adjList.keys():
                node.x += self.offset
            

        if pygame.K_RIGHT in self.heldKeys:
            for node in self.myTree.adjList.keys():
                node.x -= self.offset


        if pygame.K_UP in self.heldKeys:
            for node in self.myTree.adjList.keys():
                node.y += self.offset

        if pygame.K_DOWN in self.heldKeys:
            for node in self.myTree.adjList.keys():
                node.y -= self.offset    

    def addNextNode(self):
        centerX = self.SCREEN_WIDTH
        centerY = self.SCREEN_HEIGHT

        queue = self.myTree.traverseBTD()

        
        if self.curNode < len(queue):
            #circle = ((0,0,0), (queue[self.curNode][1].x*self.xSep + centerX//2, queue[self.curNode][1].y + centerY//2 - 300), 10, 0)
            self.nodesToDraw.add(queue[self.curNode][1])
           
            self.curNode += 1

    def addAllNodes(self):
        

        queue = self.myTree.traverseBTD()
        
        for i in range(len(queue)):
            #circle = ((0,0,0), (queue[i][1].x*self.xSep + centerX//2, queue[i][1].y + centerY//2 - 300), 10, 0)
            self.nodesToDraw.add(queue[i][1])
           
    def checkZoom(self):
        centerX = self.SCREEN_WIDTH//2
        centerY = self.SCREEN_HEIGHT//2

        sensitivity = .01
        zoomFactor = 1

        if pygame.K_6 in self.heldKeys:
            zoomFactor = 1 + sensitivity

        elif pygame.K_7 in self.heldKeys:
            zoomFactor = 1 - sensitivity




        for node in self.myTree.adjList.keys():

            xFromCenter = float(node.x - centerX)
            yFromCenter = float(node.y - centerY)
            
            node.x = centerX + xFromCenter * zoomFactor
            node.y = centerY + yFromCenter * zoomFactor

    #centers given node on screen at speed based on distance to it
    #returns true if in center
    def center(self, node, speed = .02):
        x = node.x
        y = node.y

        centerX = self.SCREEN_WIDTH//2
        centerY = self.SCREEN_HEIGHT//2

        moveX = x - centerX
        moveY = y - centerY

        boost = 0

    
        outOfXCenter = moveX > 2 or moveX < -2
        outOfYCenter = moveY > 2 or moveY < -2
        print(outOfXCenter, outOfYCenter)
        
        if(outOfXCenter):
            #move all nodes in correct dir
            for node in self.myTree.adjList.keys():
                node.x -= (moveX) * speed 

        if(outOfYCenter):
            #move all nodes in correct dir
            for node in self.myTree.adjList.keys():
                node.y -= (moveY)* speed 

        if(not outOfXCenter and not outOfYCenter):
            return True
        else:
            return False

    def clearNodes(self):
        self.screen.fill((255, 255, 255))
        self.curNode = 0
        self.nodesToDraw = set()

    
    def traverseBTD(self, lines = False, revealNodes = False, modifiedBFS = True):
        #SHOULD CHECK LEN NODES TO DRAW = keys
        
        if pygame.K_3 in self.heldKeys:
            queue = self.myTree.traverseBTD()
            if(self.traversalNode >= len(queue)):
                self.traversalNode = 0

            #calculate node path to next node
            nextNode = None
            self.center(queue[self.traversalNode][1])

            if(self.center(queue[self.traversalNode][1]) == True):
                self.traversalNode+= 1

            




    def draw(self):
        color = (0,0,0)
        centerOffset = 6
        for node in self.nodesToDraw:
            color = ((self.myTree.families[node] * 112 + 77) %255,(self.myTree.families[node] * 190-100) %255,(self.myTree.families[node] * 34) %255 )
            x = int(node.x)
            y = int(node.y)

            text_surface = self.my_font.render(node.data, False, (0, 0, 0))
            pygame.draw.circle(self.screen, color, (x,y), 20, 5)
            self.screen.blit(text_surface, (x-centerOffset,y-centerOffset))
            
    def run(self):
        while(self.running):

            self.update()
            self.clock.tick(60)

if __name__ == "__main__":
    pygame.font.init() 
    a = Node("a")
    b = Node("b")
    c = Node("c")
    d = Node("d")
    e = Node("e")
    f = Node("f")
    g = Node("g")
    h = Node("h")
    i = Node("i")
    j = Node("j")
    k = Node("k")
    l = Node("l")
    myTree2 = Tree()


    myTree2.addRootNode(a)


    myTree2.addNode(a,b)
    myTree2.addNode(a,c)

    myTree2.addNode(b,d)
    myTree2.addNode(b,e)

    myTree2.addNode(c,f)
    myTree2.addNode(c,h)
    myTree2.addNode(c,i)
    myTree2.addNode(c,j)
    myTree2.addNode(c,k)
    myTree2.addNode(k,l)


    myVT = VisualTree(myTree2)
    myVT.spaceXpos()

    myVT.run()

