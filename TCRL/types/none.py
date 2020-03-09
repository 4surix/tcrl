from .bool import *


### None

class none:

    def __init__(self, commentaire=''):
         make_id(self)

         self.commentaire = commentaire

    def __eq__(self, obj):
        return None == obj

    def __ne__(self, obj):
        return None != obj
    

    def __str__(self):
        return 'O"%s"'%(self.commentaire)

    def __repr__(self):
        return '%s'%None


    def __iter__(self):
        yield None

    def __hash__(self):
        return hash(None)