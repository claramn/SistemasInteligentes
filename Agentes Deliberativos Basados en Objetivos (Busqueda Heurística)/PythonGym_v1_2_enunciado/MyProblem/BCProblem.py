#import sys
#sys.path.insert(1, '../AStar')
from AStar.Problem import Problem
from MyProblem.BCNode import BCNode
from States.AgentConsts import AgentConsts
import sys
import numpy as np

#Clase que implementa el problema especifico que queremos resolver y que hereda de la calse
#Problema genérico.
class BCProblem(Problem):
    

    def __init__(self, initial, goal, xSize, ySize):
        super().__init__(initial, goal)
        self.map = np.zeros((xSize,ySize),dtype=int)
        self.xSize = xSize
        self.ySize = ySize
    
    #inicializa un mapa con el mapa proveniente del entorno Vector => Matriz
    def InitMap(self,m):
        for i in range(len(m)):
            x,y = BCProblem.Vector2MatrixCoord(i,self.xSize,self.ySize)
            self.map[x][y] = m[i]

    #Muestra el mapa por consola
    def ShowMap(self):
        for j in range(self.ySize):
            s = ""
            for i in range(self.xSize):
                s += ("[" + str(i) + "," + str(j) + "," + str(self.map[i][j]) +"]")
            print(s)

    #Calcula la heuristica del nodo en base al problema planteado (Se necesita reimplementar)
    def Heuristic(self, node):
        #TODO: heurística del nodo
        if self.goal is None: 
            return 0    
        dx = abs(node.x - self.goal.x)
        dy = abs(node.y - self.goal.y)
        return dx + dy #distancia Manhattan
        

    #Genera la lista de sucesores del nodo (Se necesita reimplementar)
    def GetSucessors(self, node):
        successors = []
        #TODO: sucesores de un nodo dado
        directions = [(0,1,AgentConsts.NEIGHBORHOOD_UP),
                      (0,-1,AgentConsts.NEIGHBORHOOD_DOWN),
                      (1,0,AgentConsts.NEIGHBORHOOD_RIGHT),
                      (-1,0,AgentConsts.NEIGHBORHOOD_LEFT)]
        for dx, dy, direction in directions:
            x = node.x + dx
            y = node.y + dy
            if x >= 0 and x < self.xSize and y >= 0 and y < self.ySize:
                if BCProblem.CanMove(self.map[x][y]):   #creamos nuevo nodo con la accion q toque
                    """
                    nuevoNodo= BCNode(node,BCProblem.GetCost(self.map[x][y]),self.map[x][y],x,y)
                    nuevoNodo.action = direction
                    nuevoNodo.SetH(self.Heuristic(nuevoNodo))
                    successors.append(nuevoNodo)
                    """
                    self.CreateNode(successors,node,x,y)
        return successors
    
    #métodos estáticos
    #nos dice si podemos movernos hacia una casilla, se debe poner el valor de la casilla como
    #parámetro
    @staticmethod
    def CanMove(value):
        return value != AgentConsts.UNBREAKABLE and value != AgentConsts.SEMI_UNBREKABLE #and value != AgentConsts.SEMI_BREKABLE
        
    #convierte coordenadas mapa en formato vector a matriz
    @staticmethod
    def Vector2MatrixCoord(pos,xSize,ySize):
        x = pos % xSize
        y = pos // ySize #division entera
        return x,y

    #convierte coordenadas mapa en formato matriz a vector
    @staticmethod
    def Matrix2VectorCoord(x,y,xSize):
        return y * xSize + x
    
    #convierte coordenadas del mapa en coordenadas del entorno (World) (nótese que la Y está invertida)
    @staticmethod
    def MapToWorldCoord(x,y,ySize):
        xW = x * 2
        yW = (ySize - y - 1) * 2
        return xW, yW

    #convierte coordenadas del entorno (World) en coordenadas mapa (nótese que la Y está invertida)
    @staticmethod
    def WorldToMapCoord(xW,yW,ySize):
        x = xW // 2
        y = yW // 2
        y = ySize - y - 1
        return x, y
    
    #versión real del método anterior, que nos ayuda a buscar los centros de las celdas.
    #aqui nos dirá los decimales, es decir como de cerca estamos de la esquina superior derecha
    #un valor de 1.9,1.9 nos dice que estamos en la casilla 1,1 muy cerca de la 2,2
    #en realidad, lo que buscamos es el punto medio de la casilla, es decir la 1.5, 1.5 en el caso
    #de la casilla 1,1
    @staticmethod
    def WorldToMapCoordFloat(xW,yW,ySize):
        x = xW / 2
        invY = (ySize*2) - yW
        invY = invY / 2
        return x, invY

    #se utiliza para calcular el coste de cada elemento del mapa 
    @staticmethod
    def GetCost(value):
        #TODO: debes darle un coste a cada tipo de casilla del mapa.
        cost_map = {
            AgentConsts.NOTHING: 1,
            AgentConsts.BRICK: 5,
            AgentConsts.SEMI_BREKABLE: 3,
            AgentConsts.COMMAND_CENTER: 1,
            AgentConsts.PLAYER: 10,
            AgentConsts.SHELL: 100,
            AgentConsts.OTHER: 8,
            AgentConsts.LIFE: 1
        }
        return cost_map.get(value, sys.maxsize)  # Devuelve 1 si el valor no está en el mapa de costes
    
    #crea un nodo y lo añade a successors (lista) con el padre indicado y la posición x,y en coordenadas mapa 
    def CreateNode(self,successors,parent,x,y):
        value=self.map[x][y]
        g=BCProblem.GetCost(value)
        rightNode = BCNode(parent,g,value,x,y)
        rightNode.SetH(self.Heuristic(rightNode))
        successors.append(rightNode)

    #Calcula el coste de ir del nodo from al nodo to (Se necesita reimplementar)
    def GetGCost(self, nodeTo):
        return BCProblem.GetCost(nodeTo.value)

    def distancia(self, pos1, pos2):
        """
        Calcula la distancia de Manhattan entre dos posiciones en el mapa.
        :param pos1: Tupla (x1, y1) representando la primera posición.
        :param pos2: Tupla (x2, y2) representando la segunda posición.
        :return: Distancia de Manhattan entre las dos posiciones.
        """
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x1 - x2) + abs(y1 - y2)
    
    def getInitial(self):
        return self.initial
    
    def setInitial(self,initial):
        self.initial = initial

    def getGoal(self):
        return self.goal
    
    def SetGoal(self, goal):
        return super().SetGoal(goal)
    
    