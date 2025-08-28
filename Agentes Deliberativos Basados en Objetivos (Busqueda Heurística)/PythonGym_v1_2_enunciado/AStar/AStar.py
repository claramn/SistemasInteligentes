
#Algoritmo A* genérico que resuelve cualquier problema descrito usando la plantilla de la
#la calse Problem que tenga como nodos hijos de la clase Node
class AStar:

    def __init__(self, problem):
        self.open = [] # lista de abiertos o frontera de exploración
        self.precessed = set() # set, conjunto de cerrados (más eficiente que una lista)
        self.problem = problem #problema a resolver
    """
    def GetPlan(self):
        findGoal = False
        #TODO implementar el algoritmo A*
        #cosas a tener en cuenta:
        #Si el número de sucesores es 0 es que el algoritmo no ha encontrado una solución, devolvemos el path vacio []
        #Hay que invertir el path para darlo en el orden correcto al devolverlo (path[::-1])
        #GetSucesorInOpen(sucesor) nos devolverá None si no lo encuentra, si lo encuentra
        #es que ese sucesor ya está en la frontera de exploración, DEBEMOS MIRAR SI EL NUEVO COSTE ES MENOR QUE EL QUE TENIA ALMACENADO
        #SI esto es asi, hay que cambiarle el padre y setearle el nuevo coste.
        self.open.clear()
        self.precessed.clear()

        self.open.append(self.problem.getInitial())
        path = []
        #mientras no encontremos la meta y haya elementos en open....
        #TODO implementar el bucle de búsqueda del algoritmo A*
        while len(self.open) > 0 and not findGoal:
            nodo = min(self.open, key=lambda x: x.F()) #sacamos el nodo con menor coste F
            self.open.remove(nodo) #lo sacamos de la lista de abiertos
            if nodo == self.problem.getGoal():
                path = self.ReconstructPath(nodo)
                findGoal = True
                break
            self.precessed.add(nodo)
            sucesores = self.problem.GetSucessors(nodo)
            for sucesor in sucesores:
                if any((node == sucesor) for node in self.precessed):
                     continue
                
                # Calculamos el nuevo coste G
                new_g = nodo.G() + self.problem.GetGCost(sucesor)
                
                # Comprobamos si está en la lista abierta
                node_in_open = self.GetSucesorInOpen(sucesor)
                
                if node_in_open is None:
                    # No está en abierta, lo configuramos y añadimos
                    self._ConfigureNode(sucesor, nodo, new_g)
                    self.open.append(sucesor)
                elif new_g < node_in_open.G():
                    # Está en abierta pero con peor coste, lo actualizamos
                    self._ConfigureNode(node_in_open, nodo, new_g)
    
        return path
    """
    def GetPlan(self):
        self.open.clear
        self.precessed.clear()
        initial = self.problem.Initial()
        initial.SetH(self.problem.Heuristic(initial))
        self.open.append(initial)

        while self.open:
            self.open.sort(key=lambda n: n.F())
            actual = self.open.pop(0) #sacamos el nodo con menor coste F
            if actual == self.problem.getGoal(): #si es la meta, devolvemos el path
                return self.ReconstructPath(actual)
            self.precessed.add(actual)

            for sucesor in self.problem.GetSucessors(actual):
                if sucesor in self.precessed:
                    continue
                open_s = self.GetSucesorInOpen(sucesor) #miramos si el sucesor ya está en abierta
                new_g = actual.G() + self.problem.GetGCost(sucesor) #calculamos el nuevo coste G
                if open_s:
                    if new_g < open_s.G():
                        self._ConfigureNode(open_s, actual, new_g)
                else:
                    self._ConfigureNode(sucesor, actual, new_g)
                    self.open.append(sucesor) #añadimos el sucesor a la lista de abiertos
        return [] #si no hemos encontrado la meta, devolvemos el path vacio
    

    #nos permite configurar un nodo (node) con el padre y la nueva G
    def _ConfigureNode(self, node, parent, newG):
        node.SetParent(parent)
        node.SetG(newG)
        #TODO Setearle la heuristica que está implementada en el problema. (si ya la tenía será la misma pero por si reutilizais este método para otras cosas)
        node.SetH(self.problem.Heuristic(node))

    #nos dice si un sucesor está en abierta. Si esta es que ya ha sido expandido y tendrá un coste, comprobar que le nuevo camino no es más eficiente
    #En caso de serlos, _ConfigureNode para setearle el nuevo padre y el nuevo G, asi como su heurística
    def GetSucesorInOpen(self,sucesor):
        i = 0
        found = None
        while found == None and i < len(self.open):
            node = self.open[i]
            i += 1
            if node == sucesor:
                found = node
        return found


    #reconstruye el path desde la meta encontrada.
    def ReconstructPath(self, goal):
        path = []
        #TODO: devuelve el path invertido desde la meta hasta que el padre sea None.
        nodoActual = goal
        while nodoActual != None:
            path.append(nodoActual)
            nodoActual = nodoActual.GetParent()
        #path = path[::-1] #invertimos el path para devolverlo en el orden correcto
        path = path[::-1]
        return path



