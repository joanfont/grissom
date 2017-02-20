NUMBER_MAPPING = {
    0: 'cero',
    1: 'un',
    2: 'dos',
    3: 'tres',
    4: 'cuatro',
    5: 'cinco',
    6: 'seis',
    7: 'siete',
    8: 'ocho',
    9: 'nueve',
}

MAX_NUMBER = 9


def number_to_text(number):
    if number > MAX_NUMBER:
        raise ValueError()

    return NUMBER_MAPPING.get(number)
