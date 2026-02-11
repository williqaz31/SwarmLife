import random


class Fourmi:
    def __init__(self):
        self.duree_de_vie = Duree_de_vie()  # gere la durer de vie selon la moyenne des fourmi soit de 1.5 a 2 ans
        self.age = 0
        self.jours_sans_manger  = 0
    def manger(self):
        self.jours_sans_manger = 0

    def affamer(self):
        self.jours_sans_manger += 1
        if self.jours_sans_manger >= 7:
            return self
        return None
    def f_vieillir(self):
        self.age += 1
        if self.age >= self.duree_de_vie:
            return self
        else:
            return None


class Reine(Fourmi):
    def __init__(self):
        super().__init__()
        self.duree_de_vie = random.randint(3650, 7300)


class Oeuf:
    def __init__(self):
        self.delai = 21
        self.age = 0

    def vieillir(self):
        self.age += 1
        if self.age >= self.delai:
            return self
        else:
            return None


def Duree_de_vie():
    low = 548
    high = 730
    low_outside = 0
    high_outside = 900
    outside_prop = 0.3
    if random.random() < outside_prop:
        return random.randint(low_outside, high_outside)
    else:
        return random.randint(low, high)