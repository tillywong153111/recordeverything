# 太阳黑子图形程序的第一个原型

from reportlab.lib import colors
from reportlab.graphics.shapes import *
from reportlab.graphics import renderPDF

data = [
#   UTC      Radio Flux   Planetary   Largest
#  Date       10.7 cm      A Index    Kp Index
    (2, 230, 8 ,3),
    (3, 240, 5, 2), 
    (4, 245, 5, 2),
    (5, 250, 5, 2),
    (6, 240, 5, 2),
    (7, 240, 5, 2),
    (8, 245, 10, 3),
    (9, 245, 5, 2),
    (10, 240, 5, 2),
    (11, 240, 5, 2),   
]