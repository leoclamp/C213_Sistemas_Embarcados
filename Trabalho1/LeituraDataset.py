import scipy.io as sio
import numpy as np

#Gerar dados do dataset
def carregar_dados():
    mat_data = sio.loadmat('Dataset_Grupo3.mat')
    entrada = mat_data['TARGET_DATA____ProjetoC213_Degrau'][1].flatten()  # Entrada
    saida = mat_data['TARGET_DATA____ProjetoC213_PotenciaMotor'][1].flatten()  # Saída
    tempo = mat_data['TARGET_DATA____ProjetoC213_Degrau'][0].flatten()  # Tempo
    
    return entrada, saida, tempo
