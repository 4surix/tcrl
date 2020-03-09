from .str import *


# Redirection Str -------------------------------------------------------------

class rstr():

    def __init__(self, texte, bloc):
        make_id(self)

        self.value = texte

        self.callable_with_not_call = False

        self.bloc = bloc

    def __eq__(self, obj):
        return self.value == obj
    def __ne__(self, obj):
        return self.value != obj

    def __str__(self): 
        return '%s'%self.value

    def __repr__(self): 
        return 'r"%s"'%self.value

    def __call__(self, cle, ops, vars_objets):
        v = get_vars(self, (), cle, {}, ops, vars_objets)
        return '%s'%self.verif(v)

    def __add__(self, obj):
        return rstr(self.value + py_str(obj))

    def __iadd__(self, obj):
        return rstr(self.value + py_str(obj))

    def __sub__(self, obj):
        return rstr(self.value.replace(py_str(obj), ''))

    def __isub__(self, obj):
        return rstr(self.value.replace(py_str(obj), ''))

    def __hash__(self):
        return hash(self.value)

    def verif(self, variables):

        texte = self.value[:]
        decode = self.bloc.__decode__

        for partie in texte.split("#")[1:-1:2]:

            partie_a_remplacer = '#%s#'%partie

            if '(' in partie and ')' == partie[-1]:
                
                variable, parametres = partie[:-1].split('(', 1)

                variable = call(variable, self.bloc)
                for param in decode(parametres):
                    variable.append(param)

            else:

                variable = redirection(self.bloc)
                for param in decode(partie):
                    variable.append(param)

            variable = variable((), {}, variables[0])

            texte = texte.replace(partie_a_remplacer, str(variable))

        nouv_texte = str(texte)
        nouv_texte.__id__ = self.__id__

        return nouv_texte