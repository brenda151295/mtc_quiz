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
        categoria = "categoria_" + limpiar_string(sheet.cell_value(row, 2))
        tema = limpiar_string(sheet.cell_value(row, 3))
        enunciado = limpiar_enunciado(sheet.cell_value(row, 4))
        alternativa_1 = limpiar_alternativa(sheet.cell_value(row, 5))
        print ('ENUNCIADO: ',enunciado)
        ocurrencia = Pregunta.objects.filter(enunciado=enunciado, alternativa_1=alternativa_1).first()
        if ocurrencia is None:
            pregunta = {
                'tema' : constants.CONVERT.get(tema),
                'enunciado' : enunciado,
                'alternativa_1' : alternativa_1,
                'alternativa_2' : limpiar_alternativa(sheet.cell_value(row, 6)),
                'alternativa_3' : limpiar_alternativa(sheet.cell_value(row, 7)),
                'alternativa_4' : limpiar_alternativa(sheet.cell_value(row, 8)),
                'alternativa_correcta' : sheet.cell_value(row, 10),
                categoria : True
            }
            # print (limpiar_enunciado(sheet.cell_value(row, 4)),'/n')
            # print (limpiar_alternativa(sheet.cell_value(row, 5)),'/n')
            # print (limpiar_alternativa(sheet.cell_value(row, 6)),'/n')
            # print (limpiar_alternativa(sheet.cell_value(row, 7)),'/n')
            # print (limpiar_alternativa(sheet.cell_value(row, 8)),'/n')
            print ('__________________________________________________________________________')
            Pregunta.objects.create(**pregunta)

        else:
            setattr(ocurrencia, categoria, True)
            ocurrencia.save()
