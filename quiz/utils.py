import re

import xlrd
import xlsxwriter

from quiz.models import Pregunta
from quiz import constants


def limpiar_string(s):
    return re.sub(' +', ' ', s.replace('\n', ' '))


def limpiar_enunciado(s):
    return limpiar_string(re.sub('\xa0+', '__________', s))


def limpiar_alternativa(s):
    return s[3:]


def cargar_excel(ruta):
    x = xlrd.open_workbook(ruta)
    sheet = x.sheet_by_name(x.sheet_names()[0])
    num_rows = sheet.nrows
    for row in range(1, num_rows):
        categoria = "categoria_" + limpiar_string(sheet.cell_value(row, 2))
        tema = limpiar_string(sheet.cell_value(row, 3))
        enunciado = limpiar_enunciado(sheet.cell_value(row, 4))
        alternativa_1 = limpiar_alternativa(sheet.cell_value(row, 5))
        print ('ENUNCIADO: ', enunciado)
        ocurrencia = Pregunta.objects.filter(
            enunciado=enunciado, alternativa_1=alternativa_1).first()
        if ocurrencia is None:
            # FIXME: AIIIA no funciona :/
            id_tema = constants.CONVERT.get(tema, 'T6')
            pregunta = {
                'tema': id_tema,
                'enunciado': enunciado,
                'alternativa_1': alternativa_1,
                'alternativa_2': limpiar_alternativa(sheet.cell_value(row, 6)),
                'alternativa_3': limpiar_alternativa(sheet.cell_value(row, 7)),
                'alternativa_4': limpiar_alternativa(sheet.cell_value(row, 8)),
                'alternativa_correcta': sheet.cell_value(row, 9),
                categoria: True
            }
            # print (limpiar_enunciado(sheet.cell_value(row, 4)),'/n')
            # print (limpiar_alternativa(sheet.cell_value(row, 5)),'/n')
            # print (limpiar_alternativa(sheet.cell_value(row, 6)),'/n')
            # print (limpiar_alternativa(sheet.cell_value(row, 7)),'/n')
            # print (limpiar_alternativa(sheet.cell_value(row, 8)),'/n')
            print ('_________________________________________________________')
            Pregunta.objects.create(**pregunta)

        else:
            setattr(ocurrencia, categoria, True)
            ocurrencia.save()


def generar_reporte(path, categoria):
    """
    categoria
    AI
    AIIA
    AIIB
    AIIIA
    AIIIB
    AIIIC
    valid filter name
    categoria_AI
    categoria_AIIA
    categoria_AIIB
    categoria_AIIIA
    categoria_AIIIB
    categoria_AIIIC
    """
    workbook = xlsxwriter.Workbook('%s/%s.xlsx' % (path, categoria))
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'TEMA')
    worksheet.write(0, 1, 'PREGUNTA')
    worksheet.write(0, 2, 'RESPUESTA')
    categoria = 'categoria_%s' % (categoria, )
    query_filter = {categoria: True}
    for idx_row, pregunta in enumerate(
        Pregunta.objects.filter(**query_filter), 1
    ):
        tema = constants.TEMAS_MAPPING.get(pregunta.tema, '-')
        alternativa_correcta = constants.ALTERNATIVA_CORRECTA.get(
            pregunta.alternativa_correcta, '-')
        alternativa_correcta = getattr(
            pregunta, 'alternativa_' + alternativa_correcta, '-')

        worksheet.write(idx_row, 0, tema)
        worksheet.write(idx_row, 1, pregunta.enunciado)
        worksheet.write(idx_row, 2, alternativa_correcta)
    workbook.close()
