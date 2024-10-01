import numpy as np

# funçãp utilizando o método smith
def metodo_smith(tempo, saida):
    valor_final = saida[-1]
    y1 = 0.283 * valor_final
    y2 = 0.632 * valor_final
    t1 = tempo[np.where(saida >= y1)[0][0]]
    t2 = tempo[np.where(saida >= y2)[0][0]]
    tau = 1.5 * (t2 - t1)
    theta = t2 - tau
    return tau, theta

# funçãp utilizando o método sundaresan
def metodo_sundaresan(tempo, saida):
    valor_final = saida[-1]
    y1 = 0.353 * valor_final
    y2 = 0.853 * valor_final
    t1 = tempo[np.where(saida >= y1)[0][0]]
    t2 = tempo[np.where(saida >= y2)[0][0]]
    tau = 0.6 * (t2 - t1) 
    theta = ((1,3*t1)-(0.29*t2))
    return tau, theta
