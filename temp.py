"D E P A R T E M E N   F I S I K A"
"Reizkian Yesaya_15/383192/PA/16852"
"program: Euler Method_practice"
"created: 31 Juli 2018"

import numpy as np
import matplotlib.pyplot as plt

def differential(x):
    dy_dx=2*x
    return dy_dx

"variable definition"
h=0.01     #performance
x_0=1.0     #initial value x_0
y_0=1.0     #initial value y_0

while x_0<10:
    print(x_0,"    ",y_0)
    y_ii=differential(x_0)*h+y_0
    y_0=y_ii
    x_0=x_0+h
