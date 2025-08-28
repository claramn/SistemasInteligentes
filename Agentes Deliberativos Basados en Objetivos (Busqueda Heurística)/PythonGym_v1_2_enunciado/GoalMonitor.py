import random
from States.AgentConsts import AgentConsts

class GoalMonitor:

    GOAL_COMMAND_CENTRER = 0
    GOAL_LIFE = 1
    GOAL_PLAYER = 2
    def __init__(self, problem, goals):
        self.goals = goals
        self.problem = problem
        self.lastTime = -1
        self.recalculate = False
        self.goalTypeActual = None
        self.tiempoReplanificar = 1 #cada 1 segundo

    def ForceToRecalculate(self):
        self.recalculate = True

    #determina si necesitamos replanificar
    def NeedReplaning(self, perception, map, agent):
        
        currentTime = perception[AgentConsts.TIME]
        salud = perception[AgentConsts.HEALTH]
        if self.recalculate:
            self.recalculate = False
            self.lastTime = currentTime
            return True
        #TODO definir la estrategia de cuando queremos recalcular
        #puede ser , por ejemplo cada cierto tiempo o cuanod tenemos poca vida.
        if currentTime - self.lastTime > self.tiempoReplanificar:
            self.lastTime = currentTime
            return True
        #TODO quizas falta poner una condicion q sea que si el objetivo actual ya no es valido deberiamos recalcular
        return False
    
    #selecciona la meta mas adecuada al estado actual
    def SelectGoal(self, perception, map, agent):
        #TODO definir la estrategia del cambio de meta
        salud = perception[AgentConsts.HEALTH]
        posJugador = (perception[AgentConsts.PLAYER_X], perception[AgentConsts.PLAYER_Y])
        comcntrPos = (perception[AgentConsts.COMMAND_CENTER_X], perception[AgentConsts.COMMAND_CENTER_Y])
        vidaPos = (perception[AgentConsts.LIFE_X], perception[AgentConsts.LIFE_Y])
        agentePos = (perception[AgentConsts.AGENT_X], perception[AgentConsts.AGENT_Y])

        #si la vida es menor de 3, vamos a por la vida
        if salud < 3 and vidaPos != (-1,-1) and self.problem.distancia(vidaPos, agentePos) < self.problem.distancia(comcntrPos, agentePos):
            #si la vida está cerca y tenemos poca vida, vamos a por la vida
            self.goalTypeActual = self.GOAL_LIFE
            return self.goals[self.GOAL_LIFE]
        #si el jugador está cerca, vamos a por el jugador
        if posJugador != (-1,-1) and self.problem.distancia(posJugador, agentePos) < self.problem.distancia(comcntrPos, agentePos) - 5:
            self.goalTypeActual = self.GOAL_PLAYER
            return self.goals[self.GOAL_PLAYER]
        #si el jugador está lejos, vamos a por la base
        self.goalTypeActual = self.GOAL_COMMAND_CENTRER
        return self.goals[self.GOAL_COMMAND_CENTRER]
    
    def UpdateGoals(self,goal, goalId):
        self.goals[goalId] = goal
