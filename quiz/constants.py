TEMAS = (
    ('T1', 'Reglamento de Tránsito y Manual de Dispositivos de Control de Tránsito'),
    ('T2', 'Mercancías peligrosas'),
    ('T3', 'Reglamento Nacional de Vehículos'),
    ('T4', 'Funcionamiento del Sistema Nacional de Emisión de Licencias de Conducir'),
    ('T5', 'Mecánica para la conducción'),
    ('T6', 'Regulación de actividad de transporte'),
    ('T7', 'Mecánica avanzada para la conducción'),
)

TEMAS_MAPPING = dict(TEMAS)


ALTERNATIVAS = (
    ('a', '1'),
    ('b', '2'),
    ('c', '3'),
    ('d', '4'),
)

ALTERNATIVA_CORRECTA = dict(ALTERNATIVAS)

CONVERT = {
    'Reglamento de Tránsito y Manual de Dispositivos de Control de Tránsito' : 'T1',
    'Mercancías peligrosas' : 'T2',
    'Reglamento Nacional de Vehículos' : 'T3',
    'Funcionamiento del Sistema Nacional de Emisión de Licencias de Conducir' : 'T4',
    'Mecánica para la conducción' : 'T5',
    'Regulación de actividad de transporte' : 'T6',
    'Mecánica avanzada para la conducción' : 'T7',
}

SESSION_DATA = {}
GENERATORS = {}
EXAMEN = []
EXAMEN_DATA = {}
TIEMPO_EXAMEN = None
NUM_PREGUNTAS = 4
NUM_PREGUNTAS_APROBAR = 1
