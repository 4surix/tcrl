from .none import *


def _calcul(nbrs, variables):

    def get_nbrs(place):
        place_gauche = place - 1
        place_droite = place + 1

        n1, n2 = nbrs[place_gauche], nbrs[place_droite]

        del nbrs[place_gauche:place_droite]

        n1, n2 = verif_callable(n1, (), {}, variables), verif_callable(n2, (), {}, variables)

        def verif_priorités(obj):
            if isinstance(obj, (tuple, list)):
                return _calcul(obj, variables)
            return obj

        return verif_priorités(n1), verif_priorités(n2), place_gauche

    #Puissance et racine en priorité
    place = 0
    while nbrs.count('^') or nbrs.count('V'):

        partie = nbrs[place]

        if partie == '^':
            n1, n2, place = get_nbrs(place)
            if n2 > 1000:
                raise Exception('Exposant > 1000')
            nbrs[place] = n1 ** n2

        elif partie == 'V':
            n1, n2, place = get_nbrs(place)
            nbrs[place] = n1 ** (1 / n2)

        else:
            place += 1

    #Multiplication/Division/Modulo en seconde priorité
    place = 0
    while (nbrs.count('*') or nbrs.count('\\')
        or nbrs.count('%') or nbrs.count('/')):

        symb = nbrs[place]

        if symb == '*':
            n1, n2, place = get_nbrs(place)
            nbrs[place] = n1 * n2

        elif symb == '/':
            n1, n2, place = get_nbrs(place)
            nbrs[place] = n1 / n2

        elif symb == '\\':
            n1, n2, place = get_nbrs(place)
            nbrs[place] = n1 // n2

        elif symb == '%':
            n1, n2, place = get_nbrs(place)
            nbrs[place] = n1 % n2

        else:
            place += 1

    #Et pour finir addition et soustraction
    place = 0
    while nbrs.count('+') or nbrs.count('-'):

        partie = nbrs[place]

        if partie == '+':
            n1, n2, place = get_nbrs(place)
            nbrs[place] = n1 + n2

        elif partie == '-':
            n1, n2, place = get_nbrs(place)
            nbrs[place] = n1 - n2

        else:
            place += 1

    return mk_nbr(nbrs[-1])


class calc:

    def __init__(self, bloc):
        self.values = [pos(0), '+']

        self.bloc = bloc

    def append(self, obj):

        def conv_nbr_pos(obj):
            if isinstance(obj, nbr):
                obj = pos(obj)
            return obj

        if isinstance(obj, (list, tuple)):
            obj = [conv_nbr_pos(num) for num in obj]
        else:
            obj = conv_nbr_pos(obj)

        self.values.append(obj)


    def __call__(self, params, kwargs, vars_objets):
        variables = get_vars(self, (), params, {}, kwargs, vars_objets)

        def copie(liste):
            return [copie(element) if isinstance(element, (list, tuple)) and len(element) >= 3 else element for element in liste]

        return _calcul(copie(self.values), variables[0])


    def __iter__(self):
        yield None


    def __getitem__(self, index):

        if isinstance(index, slice):
            start, stop, step = index.start, index.stop, index.step
            return self.values[start:stop:step]
        else:
            return self.values[index]


    def __str__(self):
        return '=%s' % self.values

    def __repr__(self):
        return '=%s' % self.values