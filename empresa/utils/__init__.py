from .json_generation import *
from .whatsapp import *
from calendar import monthrange

def ultimo_dia_mes(year, month):
    return monthrange(year, month)[1]