from Agent import Agent, findSpouse, socialize, tryMarry
import random
import matplotlib.pyplot as plt

AGENTS = 50
DAYS = 250
INTERACTIONS = 3

class World:
    _agents = []
    _days = 0
    _currentDay = 1
    _interactions = 0
    _people = []
    _dayList = []
    _populationList = []
    _birthList = []
    _deathList = []
    _marriedList = []

    def __init__(self, agents, days, interactions):
        self.initAgents(agents)
        self._days = days
        self._interactions = interactions

    def run(self):
        l = False
        plt.plot()
        plt.xlabel('Days')
        plt.ylabel('Agents')
        plt.title("Population")

        for d in range(0, self._days):
            plt.plot(self._dayList, self._populationList,
                     label='Population', color='blue')
            plt.plot(self._dayList, self._birthList,
                     label='Births', color='green')
            plt.plot(self._dayList, self._deathList,
                     label='Deaths', color='red')
            plt.plot(self._dayList, self._marriedList,
                     label=f'Weddings', color='pink')
            if not l:
                plt.legend()
                l = True

            plt.pause(0.05)

            print("Day:", self._currentDay)
            self.doInteractions()
            self.doWeddings()
            self.repopulate()
            self.nextDay()

            if len(self._agents) == 0:
                break
        plt.show()

    def initAgents(self, agents):
        self._agents = [None] * agents
        for i in range(0, len(self._agents)):
            a = Agent(i, self._currentDay)
            self._agents[i] = a

    def doInteractions(self):
        if len(self._agents) > 1:
            for agent in self._agents:
                agentID = agent.getID()
                for i in range(0, self._interactions):
                    randAgent = None
                    while True:
                        randAgent = self._agents[random.randrange(
                            0, len(self._agents))]
                        randID = randAgent.getID()
                        if randID != agentID:
                            break
                    socialize(agent, randAgent)

    def doWeddings(self):
        weddings = 0
        for agent in self._agents:
            if agent.getAge() > 16:
                agentID = agent.getID()
                if not agent.isMarried():
                    other = None
                    for other in self._agents:
                        otherID = other.getID()
                        if otherID != agentID:
                            if not other.isMarried():
                                success = tryMarry(agent, other)
                                if success:
                                    weddings += 1

        self._marriedList.append(weddings)

    def repopulate(self):
        deceased = []
        births = 0
        for agent in self._agents:
            if agent.getAge() >= agent.getDeathAge():
                self._agents.remove(agent)
                deceased.append(agent.getID())
            else:
                if agent.isMarried():
                    spouse = findSpouse(agent, self._agents)
                    if spouse is not None:
                        if not agent.isMale():
                            if agent.getAge() <= 40 + random.randint(-5, 5):
                                chance = 1
                                if not agent.isParent():
                                    chance = 0.545

                                elif len(agent.getChildren()) == 1:
                                    chance = 0.321

                                elif len(agent.getChildren()) == 2:
                                    chance = 0.133
                                
                                else:
                                    chance = 0.09

                                
                                if (random.random() < chance):
                                    for i in range(0, 1):
                                        c = Agent(len(self._agents), self._currentDay)
                                        births += 1
                                        self._agents.append(c)
                                        agent.setChild(c.getName())
                                        spouse.setChild(c.getName())


                            

        self._deathList.append(len(deceased))
        self._birthList.append(births)

        for i, agent in enumerate(self._agents):
            agent.setID(i)
            agent.forgetAgents(deceased)

    def nextDay(self):
        for agent in self._agents:
            agent.age()

        self._dayList.append(self._currentDay)
        self._populationList.append(len(self._agents))

        self._currentDay += 1


world = World(AGENTS, DAYS, INTERACTIONS)


if __name__ == '__main__':
    world.run()
