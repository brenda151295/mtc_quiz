import re

import xlrd

from quiz.models import Pregunta
from quiz import constants


def limpiar_string(s):
    return re.sub(' +', ' ', s.replace('\n', ' '))

def limpiar_enunciado(s):
    return limpiar_string(re.sub('\xa0+','__________',s))

def limpiar_alternativa(s):
    return s[3:]

def cargar_excel(ruta):
    x = xlrd.open_workbook(ruta)
    sheet = x.sheet_by_name(x.sheet_names()[0])
    num_rows = sheet.nrows
    for row in range(1,num_rows):
        tema = limpiar_string(sheet.cell_value(row, 3))
        pregunta = {
            'tema' : constants.CONVERT.get(tema),
            'enunciado' : limpiar_enunciado(sheet.cell_value(row, 4)),
            'alternativa_1' : limpiar_alternativa(sheet.cell_value(row, 5)),
            'alternativa_2' : limpiar_alternativa(sheet.cell_value(row, 6)),
            'alternativa_3' : limpiar_alternativa(sheet.cell_value(row, 7)),
            'alternativa_4' : limpiar_alternativa(sheet.cell_value(row, 8)),
            'alternativa_correcta' : sheet.cell_value(row, 10),
        }
        print (limpiar_enunciado(sheet.cell_value(row, 4)),'/n')
        print (limpiar_alternativa(sheet.cell_value(row, 5)),'/n')
        print (limpiar_alternativa(sheet.cell_value(row, 6)),'/n')
        print (limpiar_alternativa(sheet.cell_value(row, 7)),'/n')
        print (limpiar_alternativa(sheet.cell_value(row, 8)),'/n')
        print ('__________________________________________________________________________')
        Pregunta.objects.create(**pregunta)