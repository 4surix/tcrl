from .rstr import *


# Pos et Neg ------------------------------------------------

def mk_nbr(nbr, return_value=False):
    nbr = py_str(nbr)

    if ',' in nbr: value = nbr.replace(',', '.')

    if '.' in nbr: 
        if nbr.split('.')[-1] == '0': 
            value = int(nbr.split('.')[0])
        else:
            value = float(nbr)
    else: value = int(nbr)

    if return_value:
        return value
        
    if nbr[0] == '-':
        return neg(value)
    return pos(value)


class _nbr:

    def _if_pos_neg(self, obj, silent=False):
        if isinstance(obj, (neg, pos)):
            return obj.value
        elif not silent:
            raise TypeError('Type %s non valide pour les pos/neg, seulement pos/neg'%type(obj).__name__)
        else:
            return obj

    def __lt__(self, obj):
        return self.value < self._if_pos_neg(obj)
    def __le__(self, obj):
        return self.value <= self._if_pos_neg(obj)
    def __eq__(self, obj):
        return self.value == self._if_pos_neg(obj, True)
    def __ne__(self, obj):
        return self.value != self._if_pos_neg(obj, True)
    def __ge__(self, obj):
        return self.value >= self._if_pos_neg(obj)
    def __gt__(self, obj):
        return self.value > self._if_pos_neg(obj)
    
    def __iter__(self):
        yield None
    
    def __abs__(self):
        return nbr(abs(self.value))
    
    def __pos__(self):
        if isinstance(self, pos):
            return ss
        return pos(-self.value)
    def __neg__(self):
        if isinstance(self, neg):
            return ss
        return neg(-self.value)

    def __add__(self, obj):
        return mk_nbr(self.value + self._if_pos_neg(obj))
    def __sub__(self, obj):
        return mk_nbr(self.value - self._if_pos_neg(obj))
    def __mul__(self, obj):
        return mk_nbr(self.value * self._if_pos_neg(obj))
    def __truediv__(self, obj):
        return mk_nbr(self.value / self._if_pos_neg(obj))
    def __floordiv__(self, obj):
        return mk_nbr(self.value // self._if_pos_neg(obj))
    def __mod__(self, obj):
        return mk_nbr(self.value % self._if_pos_neg(obj))
    def __pow__(self, obj):
        return mk_nbr(self.value ** self._if_pos_neg(obj))

    def __hash__(self):
        return hash(repr(self))

    def __index__(self):
        return self.value

    def __float__(self):
        self.value = float(self.value)
        return ss

    def __int__(self):
        self.value = int(self.value)
        return ss


class nbr:
    def __init__(self, nbr_):
        make_id(self)

        if isinstance(nbr_, (neg, pos, nbr)):
            self.value = abs(nbr_.value)
        elif isinstance(nbr_, py_str):
            self.value = abs(mk_nbr(nbr_, return_value=True))
        else:
            self.value = abs(int(nbr_))

    def __str__(self):
        return '%s'%self.value

    def __repr__(self):
        return '%s'%self.value

    def __index__(self):
        return self.value


class pos(_nbr):
    def __init__(self, nbr_):
        make_id(self)

        if isinstance(nbr_, (neg, pos, nbr)):
            self.value = +abs(nbr_.value)
        elif isinstance(nbr_, py_str):
            self.value = +abs(mk_nbr(nbr_, return_value=True))
        else:
            self.value = +abs(nbr_)

    def __str__(self):
        return '+%s'%self.value
    def __repr__(self):
        return '+%s'%self.value


class neg(_nbr):
    def __init__(self, nbr_):
        make_id(self)

        if isinstance(nbr_, (neg, pos, nbr)):
            self.value = -abs(nbr_.value)
        elif isinstance(nbr_, py_str):
            self.value = -abs(mk_nbr(nbr_, return_value=True))
        else:
            self.value = -abs(nbr_)

    def __str__(self):
        return '%s'%self.value
    def __repr__(self):
        return '%s'%self.value