from .pos_neg_nbr import *

# Bytes ---------------------------------------------------------

class bytes(py_bytes):

    def __init__(self, texte):
        make_id(self)

        self.value = texte.encode() if isinstance(texte, py_str) else py_bytes(texte)
        self.value_str = texte.decode() if isinstance(texte, py_bytes) else py_str(texte)
        
    def __eq__(self, obj):
        return self.value_str == obj

    def __ne__(self, obj):
        return self.value_str != obj


    def __str__(self):
        return "%s" % self.value_str

    def __repr__(self):
        return "'%s'" % self.value_str


    def __add__(self, value):
        if not isinstance(value, (int, pos, nbr)):
            raise TypeError("%s objet n'est pas additionable pour les types bytes, 'pos' 'nbr' seulement"%type(value).__name__)

        l = list(self.value)
        l.append(value)

        return bytes(py_bytes(l))

    def __hash__(self):
        return hash(self.value_str)