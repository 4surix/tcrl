from .bytes import *


### Bool

class bool:

    def __init__(self, value, commentaire=''):
         make_id(self)

         self.value = py_bool(value)
         self.commentaire = commentaire

    def __bool__(self):
        return self.value

    def __eq__(self, obj):
        return self.value == obj

    def __ne__(self, obj):
        return self.value != obj


    def __str__(self):
        return '%s"%s"'%(self.value*1, self.commentaire)

    def __repr__(self):
        return '%s'%self.value


    def __iter__(self):
        yield None

    def __index__(self): 
        return self.value*1

    def __hash__(self):
        return hash(self.value)