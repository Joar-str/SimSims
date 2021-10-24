import random


class Transitions:

    def __int__(self):
        self.road_in = None
        self.road_out = None
        self.food_road = None
        self.product_road = None

    def set_road_in(self, road):
        self.road_in = road

    def set_road_out(self, road):
        self.road_out = road

    def set_food_road(self, road):
        self.food_road = road

    def set_pdt_road(self, road):
        self.product_road = road


class Places:
    def __int__(self):
        self.barn_inventory = []
        self.storage_inventory = []


class Road:

    def __init__(self, road_name):
        self.road_name = road_name
        self._deque = []

    def __len__(self):
        return len(self._deque)

    def __str__(self):
        return f'Hållplats {self.road_name}'

    def has_worker(self):
        return len(self._deque) > 0

    """FIFO"""

    def worker_out(self):
        return self._deque.pop(0)

    def worker_in(self, worker):

        if worker.current_life > 0 and worker.current_life > len(self._deque):
            self._deque.append(worker)
            for worker in self._deque:
                if worker.current_life <= 0:
                    self._deque.remove(worker)
        else:
            print(f'{worker} med {worker.current_life} dog')

    def get_list(self):
        return self._deque


class DinningHall(Transitions):
    """Klassen ska ta in en arbetare från Road() och en enhet mat från Barn()"""

    def __init__(self):
        super().__init__()

    """Simulergin av intag av mat och arbetare"""

    def simulation_step(self):

        """Tar in en arbetare och en enhet mat från Road1 och barn1 om antalet arbetare är över 2"""

        if self.road_in.has_worker() and self.food_road.has_food():
            eating_worker = self.road_in.worker_out()
            food = self.food_road.barn_food_out()
            print(f'{eating_worker} med {eating_worker.current_life}i livskraft går från \n'
                  f'{self.road_in} till matsalen och äter mat med kvaliten {food}\n'
                  f'----------')

            """för varje arbetare som äter tas en enhet mat bort, och flyttar arbetaren till vägen"""
            if eating_worker.current_life < 100:
                if int(food.quality) >= 2:
                    eating_worker.increase_life()
                else:
                    eating_worker.decrease_life()
            else:
                if int(food.quality) == 1:
                    eating_worker.decrease_life()
                else:
                    eating_worker.current_life = 100

            eating_worker.current_life = max(int(eating_worker.current_life) - len(self.road_out.get_list()), 0)
            if eating_worker.current_life > 0:
                self.road_out.worker_in(eating_worker)

            print(f'{eating_worker} med {eating_worker.current_life} i livskraft flyttades till {self.road_out}\n'
                  f'----------')
        else:
            print(f'i {self.road_in} finns det {len(self.road_in)} personer\n'
                  '---------')


class Field(Transitions):
    """Klassen tar in en arbetare från Road() och returnerar en enhet mat"""

    def __init__(self):
        super().__init__()

    def _create_food(self):
        return Food()

    def simulation_step(self):
        """simulering som hämtar en arbetare från road och skickar en enhet mat till lada"""
        if self.road_in.has_worker():
            worker = self.road_in.worker_out()
            food = self._create_food()
            self.food_road.barn_food_in(food)
            worker.current_life = max(int(worker.current_life) - len(self.road_out.get_list()), 0)
            if random.randint(1, 7) > 2:
                print(f'{worker} med {worker.current_life} i liv producerar en enhet {food} och skickar det\n'
                    f'till {self.food_road}\n'
                    f'----------')

                if worker.current_life > 0:
                    self.road_out.worker_in(worker)
            else:
                worker.decrease_life()
                self.road_out.worker_in(worker)
                print(f'{worker} skadade sig och har nu {worker.current_life} i liv\n'
                      f'----------')
        else:
            print(f'i {self.road_in} finns det {len(self.road_in)} personer\n'
                  '----------')


class Barn:
    """tar in mat från Food() och returnerar till DinningHall()"""

    def __init__(self):
        self.inventory = []

    def __len__(self):
        return len(self.inventory)

    def __str__(self):
        return f'ladan'

    def has_food(self):
        return len(self.inventory) > 0

    def barn_food_out(self):
        value = self.inventory.pop(0)
        return value

    def barn_food_in(self, food):
        self.inventory.append(food)


class Food:
    """tar in en enehet mat från Field() och returnerar till Barn()"""

    def __init__(self):
        self.quality = random.randint(1, 3)

    def food_quality(self):
        self.quality = random.randint(1, 3)

    def __str__(self):
        return f' matkvalité {self.quality}'

    @property
    def food(self):
        return int(self.quality)


class Worker:

    def __init__(self, name):
        self.current_life = 100
        self.name = name

    def __str__(self):
        return self.name

    def decrease_life(self):
        self.current_life = max(self.current_life - random.randint(1, 4), 0)

    def increase_life(self):
        self.current_life = min(self.current_life + random.randint(1, 4), 100)

    @property
    def getworker(self):
        return self.current_life


class House(Transitions):
    """Tar in en produkt och returnerar en arbetare"""

    def __init__(self):
        super().__init__()

    def simulation_step(self):
        people = []
        worker = self.road_in.worker_out()
        product = self.product_road.strg_pro_out()
        if self.road_in.has_worker() and self.product_road.has_product():
            if random.randint(1, 5) > 3:
                for _ in range(2):
                    people.append(self.road_in.worker_out())
                people.append(Worker('Ny arbetare'))

                print(f'I huset är {people[0]} och {people[1]} konsumerar en {product}\n'
                      f'och producerar en arbetare med {people[2].current_life} liv\n'
                      f'----------')
            else:
                worker.increase_life()
                people.append(worker)
                print(f'{people[0]} med {people[0].current_life} konsumerar en {product}\n'
                      f'----------')

        for person in people:
            person.current_life = max(int(person.current_life) - len(self.road_out.get_list()), 0)
            if person.current_life > 0:
                self.road_out.worker_in(person)
        else:
            print(f'i {self.road_in} finns det {len(self.road_in)} personer\n'
                  f'-----------')


class Storage:
    """tar in enhet från Produkt() och returnerar till House()"""

    def __init__(self):
        self.products = []

    def __len__(self):
        return len(self.products)

    def __str__(self):
        return f'lager'

    def has_product(self):
        return len(self.products) > 0

    def strg_pro_in(self, product):
        self.products.append(product)

    """LIFO"""
    def strg_pro_out(self):
        return self.products.pop()


class Factory(Transitions):
    """Tar in en arbetare och returnerar en produkt"""

    def __init__(self):
        super().__init__()

    def _create_product(self):
        return Product()

    def simulation_step(self):

        if self.road_in.has_worker():
            worker = self.road_in.worker_out()
            product = self._create_product()
            self.product_road.strg_pro_in(product)
            print(f'{worker} med {worker.current_life} i livskraft går från \n'
                  f'{self.road_in} till fabriken och tillverkar en {product} och skickar den till {self.product_road}\n'
                  f'----------')

            '''20 % risk att arbterare dör'''
            if random.randint(1, 5) > 3:
                worker.current_life = max(int(worker.current_life) - len(self.road_out.get_list()), 0)
                if worker.current_life > 0:
                    self.road_out.worker_in(worker)
                    print(f'{worker} med {worker.current_life} i livskraft går sedan till {self.road_out}')
            else:
                worker.current_life = 0
                print(f'{worker} med {worker.current_life} i livskraft dog\n'
                        f'----------')
        else:
            print(f'i {self.road_in} finns det {len(self.road_in)} personer\n'
                  f'---------')


class Product:
    def __init__(self):
        pass

    def __str__(self):
        return f'Produkt'


if __name__ == "__main__":
    workers = ['Philip', 'Terry','Max','Oskar','Noa','Doug','Lerry','William', 'Shaun', 'Sofie','Amanda']
    workers1 = ['Tom', 'Ken', 'Mattias', 'Jacob', 'Sarah', 'Wilma', 'Emma']

    r1 = Road(1)
    r2 = Road(2)

    for i in workers:
        r1.worker_in(Worker(i))
    for i in workers1:
        r2.worker_in(Worker(i))

    d1 = DinningHall()
    d2 = DinningHall()
    d3 = DinningHall()

    f1 = Field()
    f2 = Field()

    b1 = Barn()
    b2 = Barn()

    h1 = House()
    h2 = House()

    fa1 = Factory()
    fa2 = Factory()
    fa3 = Factory()
    fa4 = Factory()

    s1 = Storage()
    for _ in range(5):
        s1.strg_pro_in(Product())
    """kopplingar för matsalen"""
    d1.set_road_in(r1)
    d1.set_road_out(r1)
    d1.set_food_road(b1)

    d2.set_road_in(r1)
    d2.set_road_out(r2)
    d2.set_food_road(b2)

    d3.set_road_in(r2)
    d3.set_road_out(r1)
    d3.set_food_road(b2)
    """koplpingar för fältet"""
    f1.set_road_in(r1)
    f1.set_road_out(r1)
    f1.set_food_road(b1)

    f2.set_road_in(r2)
    f2.set_road_out(r2)
    f2.set_food_road(b2)

    """kopplingar för fabriken"""
    fa1.set_road_in(r1)
    fa1.set_road_out(r1)
    fa1.set_pdt_road(s1)

    fa2.set_road_in(r2)
    fa2.set_road_out(r2)
    fa2.set_pdt_road(s1)

    """kopplingar för husen """
    h1.set_road_in(r1)
    h1.set_road_out(r1)
    h1.set_pdt_road(s1)

    h2.set_road_in(r2)
    h2.set_road_out(r2)
    h2.set_pdt_road(s1)

    while r2.has_worker() or r1.has_worker():
        try:
            if not b1.has_food() and not b2.has_food():
                f1.simulation_step()
                f2.simulation_step()

            else:
                fa1.simulation_step()
                fa2.simulation_step()
                h2.simulation_step()
                d1.simulation_step()
                d3.simulation_step()
                h1.simulation_step()
                d2.simulation_step()
        except:
            pass

    print('simulationen är slut')


    print(r2.get_list())
    print(r1.get_list())
    print(b2.inventory)
    print(b1.inventory)















