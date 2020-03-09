from ._utile import *


class Bloc_base(list):
    
    def __init__(self):

        self.__name__ = ''
        self.__defauts__= {}

        self.__vars__ = [
                [],
                self,
                [],
                [self.__defauts__]
            ]
        
    def __ne__(self, obj):
        return None != obj


class bloc:

    def __init__(self, var_import):
        make_id(self)

        if not isinstance(var_import, list):
            var_import = []

        self.__name__ = ''
        self.__main__ = None
        self.__defauts__ = {}

        self.__vars__ = [
                        [], #Variable objets
                        var_import, #Variable local
                        [], #Variables global
                        [self.__defauts__]
                    ]

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return '<:bloc: %s>'%self.__name__

    def __repr__(self): 
        return '<:bloc: %s>'%self.__name__

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):

        if key == "N#":
            self.__name__ = value
        elif key == "D#":
            self.__doc__ = value
        elif key == "B#":
            for key, value in value.items():
                self.__defauts__[key] = value
        elif key == "M#":
            self.__main__ = value
        elif key == "I#":
            for key, value in value.items():
                self.__dict__[key] = value
        else:
            self.__dict__[key] = value

    def __call__(self, cle, ops, variables):
        main = self.__main__
        if not main:
            return None

        func = self.__dict__.get(main)
        if callable(func):
            return func(cle, ops, variables)
        else:
            return func

    def __iter__(self):
        for item in self.__dict__:
            yield item