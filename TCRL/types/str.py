from .rac import *


# Str -------------------------------------------------------------

class str(py_str):

    def __init__(self, texte):
        make_id(self)

        self.value = texte

    def __eq__(self, obj):
        return self.value == obj

    def __ne__(self, obj):
        return self.value != obj


    def __str__(self):
        return '%s'%self.value

    def __repr__(self):
        return '"%s"'%self.value


    def __add__(self, obj):
        return str(self.value + py_str(obj))

    def __iadd__(self, obj):
        return str(self.value + py_str(obj))

    def __sub__(self, obj):
        return str(self.value.replace(py_str(obj), ''))

    def __isub__(self, obj):
        return str(self.value.replace(py_str(obj), ''))


    def __hash__(self):
        return hash(self.value)