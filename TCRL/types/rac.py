
from .bloc import *


class importation:
    def __init__(self):
        self.value = []

    def module(self):
        return self.value.value[0]

    def append(self, obj):
        #Toujours redirection
        self.value = obj


class rac(py_str):
    def __init__(self, value):
        self.value = value

        self.bloc = None

    def __call__(self, params, kwargs, variables):
        variables = get_vars(self, (), params, {}, kwargs, variables)
        variable = get_var(self.value, variables)
        return verif_callable(variable, (), {}, variables[0])

    def __str__(self):
        return '%s'%self.value

    def __repr__(self):
        return '#%s#'%self.value

    def __iter__(self):
        yield None


class call:
    def __init__(self, variable, bloc):
        self.values = []
        self.variable = variable

        self.bloc = bloc

    def __call__(self, params, kwargs, vars_objets):
        variables = get_vars(self, (), params, {}, kwargs, vars_objets)

        parametres = self.values

        args, kwargs = get_args_kwargs(parametres, variables)

        variable = get_var(self.variable, variables)
        return variable(args, kwargs, variables[0])

    def __iter__(self):
        yield None

    def append(self, obj):
        self.values = obj


class redirection:
    def __init__(self, bloc):
        self.value = []

        self.bloc = bloc

    def __call__(self, params, kwargs, vars_objets):
        variables = get_vars(self, (), params, {}, kwargs, vars_objets)

        variable = self.value[0]
        if callable(variable):
            variable = variable((), {}, variables[0])

        for index in self.value[1:]:
            variable = variable[verif_callable(index, (), {}, variables[0])]
            
        if not self.value[1:]:
            variable = get_var(variable, variables)

        return variable #verif_callable(variable, (), {}, variables[0])

    def __str__(self):
        return '#%s#|'%(self.value)

    def __repr__(self):
        return '#%s#|'%(self.value)

    def __iter__(self):
        yield None

    def append(self, obj):
        self.value.append(obj)