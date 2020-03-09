from .types import *

from functools import partial


class Conteneur:

    def __init__(self, last_conteneur, value, bloc, in_=''):
        self.texte = []
        self.value = value

        self.key = ''
        
        self.type = ''
        self.sous_type = ''

        self.bloc = bloc

        self.in_ = in_

        self.last_conteneur = last_conteneur

    def __iadd__(self, carac):
        """
        """
        self.texte.append(carac)
        return ss

    def config_type(self, balise, bloc_base):

        if balise in balises[:7] + ['<#']:
            return self.add_profondeur(balise, bloc_base)
        else:
            if balise in ["r", "1", "0", "O"]:
                self.sous_type = balise
            else:
                self.type = balise
            return ss

    def config_call(self):

        value = self.end(return_value=True)
        conteneur = Conteneur(self, call(value, self.bloc), self.bloc, self.in_)
        return conteneur

    def del_profondeur(self):
        """
        """
        conteneur = self.last_conteneur
        conteneur.save(self.value)
        return conteneur

    def add_profondeur(self, balise, bloc_base):
        """
        """
        in_ = self.in_

        if balise == '<':
            value = bloc(bloc_base)
            value.__decode__ = self.bloc.__decode__
            value.__chemin__ = self.bloc.__chemin__
            self.bloc = value
        elif balise == '{':
            value = {}
        elif balise == '[':
            value = []
        elif balise == '(':
            value = ()
        elif balise == ':':
            value = cond(self.bloc, (self.key if self.key != '' else self.value[-1] if isinstance(self.value, (tuple, list)) and self.value else ''))
            in_ = 'cond'
        elif balise == '=':
            value = calc(self.bloc)
            in_ = 'calc'
        elif balise == '#':
            value = redirection(self.bloc)
        elif balise == '<#':
            value = importation()

        conteneur = Conteneur(self, value, self.bloc, in_)
        return conteneur
    
    def end(self, return_value=False):
        """
        """
        type_ = self.sous_type + self.type
        texte = ''.join(self.texte)
        
        if type_ == '"':
            value = str(texte)
        elif type_ == 'r"':
            value = rstr(texte, self.bloc)
        elif type_ == "'":
            value = bytes(texte.encode())
        elif type_ == '+':
            value = pos(texte)
        elif type_ == '-':
            value = neg(texte)
        elif type_ == 'n+-':
            value = nbr(texte)
        elif type_ == '1"':
            value = bool(True)
        elif type_ == '0"':
            value = bool(False)
        elif type_ == 'O"':
            value = none(texte)
        elif type_ == '##':
            value = rac(texte)
            value.bloc = self.bloc
        else:
            value = texte

        if return_value:
            return value
        else:
            self.save(value)

    def save(self, obj):
        """
        """

        #Importation
        if isinstance(obj, importation):
            module = obj.module()
            data = get_data_module(module, self.bloc.__chemin__)

            obj = self.bloc.__decode__(data)

            value_vars_local = obj.__vars__[1]
            value_vars_global = obj.__vars__[2]

            bloc_vars_local = self.bloc.__vars__[1]
            bloc_vars_global = self.bloc.__vars__[2]

            bloc_vars_global.extend(value_vars_local + value_vars_global)

            value_vars_global.extend(bloc_vars_local)

        if isinstance(self.value, bloc):
            if self.key != '':
                self.value[self.key] = obj
                self.key = ''
            else:
                self.key = obj
                
        elif isinstance(self.value, dict):
            if self.key != '':
                self.value[self.key] = obj
                self.key = ''
            else:
                self.key = obj

        elif isinstance(self.value, (list, cond, calc, call, importation, redirection, Bloc_base)):
            self.value.append(obj)
            
        elif isinstance(self.value, tuple):
            self.value = self.value + (obj,)
        
        self.texte = []

        self.type = ''
        self.sous_type = ''

def decode(data, chemin=None, *, bloc_vars=None):

    data = ' '+data.strip().replace('\n', ' ').replace('\t', ' ')+' '

    echappement = False
    in_commentaire = False
    debut_commentaire = False
    sortie_de_cond_red = False

    bloc_base = Bloc_base()

    if not bloc_vars:
        bloc_vars = bloc_base

    bloc_base.__decode__ = partial(decode, bloc_vars=bloc_vars)
    bloc_base.__chemin__ = chemin

    conteneur = Conteneur(None, bloc_base, bloc_vars)
    
    for place, carac in enumerate(data):

        #Print pour débuger
        #print(place, carac, conteneur.type, conteneur.texte, conteneur, conteneur.value, conteneur.key)

        if in_commentaire:
            if carac == '/' and data[place-1] == '/' and not debut_commentaire:
                in_commentaire = False
            if debut_commentaire:
                debut_commentaire = False
            continue

        elif (not conteneur.type and carac in balises
              #Pour les bool/none et les chiffres/variable commançant par 1, 0 ou O
              and (carac not in ["r", "1", "0", "O"] or data[place+1] == '"')
              #Pour les calculs et les comparaisons = == === =>, et les fermeture
              and (carac != '=' or data[place+1] not in ['=', " ", '>'])
              #Pour fermeture de condition et redirection
              and (carac not in [':', '#'] 
                        or data[place+1] not in ['|'] 
                            and data[place-1] not in balises_categories)
              #Pour la comparaison < <=
              and (carac not in ['<'] or data[place+1] not in ['=', " "])
              #Pour les calcul, -1 + 1
              and (carac not in ['+', '-'] 
                or (conteneur.in_ != 'calc' 
                    or (not conteneur.value[:]
                        or str(conteneur.value[-1])[-1] in operations)))):

            #Si il reste du texte
            if conteneur.texte:
                conteneur.end()

            #Pour les importations <#math#>
            if carac == '<' and data[place+1] == '#':
                carac = '<#'
                
            conteneur = conteneur.config_type(carac, bloc_base)

        elif (not conteneur.type and carac in balises_categories and data[place+1] == '#'):
            conteneur.save(carac+'#')

        elif ((carac in ["}", "]", ")", ";"] 
            or (carac in [':', '#'] and data[place+1] == '|') 
                or (carac in ['>'] and isinstance(conteneur.value, (bloc, importation))))
                    and conteneur.type not in ['"', "'"]):

            if conteneur.texte:
                conteneur.end()

            conteneur = conteneur.del_profondeur()

            #Dans la cas d'une fermeture d'un call, pouet() "pomme"()
            if carac == ')' and isinstance(conteneur.value, call):
                conteneur = conteneur.del_profondeur()
            elif carac in [':', '#']:
                sortie_de_cond_red = True
                continue

        elif((carac == conteneur.type
              and carac in ['"', "'"])
            and not echappement):
            #Dans le cas d'un call "pomme"()
            if data[place+1] == '(':
                conteneur = conteneur.config_call()
            else:
                conteneur.end()

        elif conteneur.type in ['+', '-', 'n+-']:
            conteneur += carac
            
            if data[place+1] not in chiffres + ['.']:
                conteneur.end()

        elif carac == '\\':
            if echappement:
                echappement = False
                conteneur += '\\'
            else:
                echappement = True
                continue

        elif echappement:
            if carac == 'n':
                conteneur += '\n'
            elif carac == 't':
                conteneur += '\t'

        elif conteneur.type in ['"', "'"]:
            conteneur += carac

        elif carac == '/' and data[place+1] == '/':
            in_commentaire = True
            debut_commentaire = True
            
        elif carac in operations and conteneur.in_ == 'calc':
            if conteneur.texte:
                conteneur.end()

            conteneur.save(carac)

        elif (carac in comparaisons 
                and conteneur.in_ == 'cond' 
                    #and conteneur.value.type in ['up','cond']
                        and not sortie_de_cond_red):
            if conteneur.texte and not all([symb in comparaisons for symb in conteneur.texte]):
                conteneur.end()

            conteneur += carac
            
        elif carac in lettres + chiffres + ['~', '_']:

            if not conteneur.type:
                if conteneur.texte:
                    conteneur.end()

                if carac in chiffres:
                    conteneur = conteneur.config_type('n+-', bloc_base)
                else:
                    conteneur = conteneur.config_type('##', bloc_base)

            conteneur += carac

            if conteneur.type == 'n+-' and data[place+1] not in chiffres + ['.']:
                conteneur.end()

            #Dans le cas d'un call, pouet()
            if data[place+1] == '(':
                conteneur = conteneur.config_call()
            
        elif conteneur.type in ['##']:
            conteneur.end()

        echappement = False
        sortie_de_cond_red = False
        
    return conteneur.value