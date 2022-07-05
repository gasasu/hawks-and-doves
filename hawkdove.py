import random
import tkinter
random.seed()

def plot(xvals, yvals):
    # This is a function for creating a simple scatter plot.  You will use it,
    # but you can ignore the internal workings.
    root = tkinter.Tk()
    c = tkinter.Canvas(root, width=700, height=400, bg='white') #was 350 x 280
    c.grid()
    #create x-axis
    c.create_line(50,350,650,350, width=3)
    for i in range(5):
        x = 50 + (i * 150)
        c.create_text(x,355,anchor='n', text='%s'% (.5*(i+2) ) )
    #y-axis
    c.create_line(50,350,50,50, width=3)
    for i in range(5):
        y = 350 - (i * 75)
        c.create_text(45,y, anchor='e', text='%s'% (.25*i))
    #plot the points
    for i in range(len(xvals)):
        x, y = xvals[i], yvals[i]
        xpixel = int(50 + 300*(x-1))
        ypixel = int(350 - 300*y)
        c.create_oval(xpixel-3,ypixel-3,xpixel+3,ypixel+3, width=1, fill='red')
    root.mainloop()

#Constants: setting these values controls the parameters of your experiment.
injurycost = 10 #Cost of losing a fight
displaycost = 1 #Cost of displaying
foodbenefit = 8 #Value of the food being fought over
init_hawk = 0
init_dove = 0
init_defensive = 0
init_evolving = 150

########
# Your code here
########
class World:
    def __init__(self):
        self.birds = []

    def update(self):
        for bird in self.birds:
            bird.update()

    def free_food(self, number):
        for _ in range(number):
            ran = random.randint(0,len(self.birds)-1)
            bird = self.birds[ran]
            bird.eat()

    def conflict(self,number):
        for _ in range(number):
            ran, run = 0,0
            while ran == run:
                ran = random.randint(0,len(self.birds)-1)
                run = random.randint(0,len(self.birds)-1)
            self.birds[ran].encounter(self.birds[run])

    def status(self):
        doves, hawks, defensive = 0,0,0
        for bird in self.birds:
            if bird.species == "Dove":
                doves +=1
            elif bird.species == "Hawk":
                hawks+=1
            else:
                defensive += 1

        print(f"Number of Doves: {doves}")
        print(f"Number of Hawks: {hawks}")
        print(f"Number of Defensive birds: {defensive}")

    def evolvingPlot(self):
        weights = []
        aggs = []
        for bird in self.birds:
            weights.append(bird.weight)
            aggs.append(bird.agg)
        plot(weights, aggs)

class Bird:
    def __init__(self, world):
        self.world = world
        self.health = 100
        world.birds.append(self)

    def eat(self):
        self.health += foodbenefit

    def injured(self):
        self.health -= injurycost

    def display(self):
        self.health -= displaycost

    def die(self):
        self.world.birds.remove(self)

    def update(self):
        self.health -= 1
        if self.health <= 0:
            self.die()

class Dove(Bird):
    species = "Dove"
    def update(self):
        Bird.update(self)
        if self.health >= 200:
            self.health -= 100
            Dove(self.world)

    def defend_choice(self):
        return False

    def encounter(self, bird):
        if bird.defend_choice():
            bird.eat()
        else:
            self.display()
            bird.display()
            if random.randint(0,1):
                self.eat()
            else:
                bird.eat()



class Hawk(Bird):
    species = "Hawk"
    def update(self):
        Bird.update(self)
        if self.health >= 200:
            self.health -= 100
            Hawk(self.world)

    def defend_choice(self):
        return True

    def encounter(self,bird):
        if not bird.defend_choice():
            self.eat()
        else:
            if random.randint(0,1):
                self.eat()
                bird.injured()
            else:
                bird.eat()
                self.injured()

class Defensive(Dove):
    species = "Defensive"
    def update(self):
        Bird.update(self)
        if self.health >= 200:
            self.health -= 100
            Defensive(self.world)

    def defend_choice(self):
        return True

class Evolving(Bird):
    def __init__(self, World, weight=0,agg=0):
        self.world = World
        World.birds.append(self)
        self.health = 100
        self.weight = weight if weight else random.uniform(1,3)
        self.agg = agg if agg else random.uniform(0,1)# represents the agressiveness of a bird



    def defend_choice(self):
        if self.agg >= random.random():
            return True
        return False

    def update(self):
        self.health -= (0.4 + 0.6*self.weight)
        if self.health <= 0:
            Bird.die(self)
        if self.health >= 200:
            self.health -= 100
            b = random.uniform(-0.1, 0.1)
            new_weight = self.weight + b
            c = random.uniform(-0.05, 0.05)
            new_agg = self.agg + c
            if new_weight >= 1:
                if new_weight > 3:
                    new_weight = 3
            else:
                new_weight = 1
            if new_agg >= 0:
                if new_agg > 1:
                    new_agg = 1
            else:
                new_agg = 0
            Evolving(self.world,new_weight, new_agg)

    def encounter(self, bird):
        if not bird.defend_choice():
            if self.agg >= random.random():
                self.eat()
            else:
                self.display()
                bird.display()
                #if bird.weight / (self.weight + bird.weight)  >= random.random():
                if random.randint(0,1):
                    bird.eat()
                else:
                    self.eat()
        else:
            attack = random.random()
            if self.agg > attack:
                winner = random.uniform(0, self.weight+ bird.weight)
                if winner <= self.weight:

                    self.eat()
                    bird.injured()
                else:
                    bird.eat()
                    self.injured()
            else:
                bird.eat()

########
# The code below actually runs the simulation.  You shouldn't have to do anything to it.
########
w = World()
for i in range(init_dove):
    Dove(w)
for i in range(init_hawk):
    Hawk(w)
for i in range(init_defensive):
    Defensive(w)
for i in range(init_evolving):
    Evolving(w)

for t in range(10000):
    w.free_food(10)
    w.conflict(50)
    w.update()
#w.status()
w.evolvingPlot()  #This line adds a plot of evolving birds. Uncomment it when needed.
