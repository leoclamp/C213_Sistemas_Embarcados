import matplotlib.pyplot as plt
import scipy.io as sio

# Carregar o dataset
file_path = 'Dataset_Grupo3.mat'  # Altere o nome do arquivo conforme necessário
data = sio.loadmat(file_path)

# Exibir as chaves para entender a estrutura do dataset
print(data.keys())

# Extraindo entrada e saída
entrada = data['TARGET_DATA____ProjetoC213_Degrau'][1]  # A segunda linha é a entrada
saida = data['TARGET_DATA____ProjetoC213_PotenciaMotor'][1]  # A segunda linha é a saída
tempo = data['TARGET_DATA____ProjetoC213_Degrau'][0]  # A primeira linha é o tempo

# Visualizando os dados em um único gráfico
plt.figure(figsize=(12, 6))
plt.plot(tempo, entrada, label='Entrada (Degrau)', color='blue')
plt.plot(tempo, saida, label='Saída (Potência do Motor)', color='orange')
plt.title('Entrada e Saída do Sistema')
plt.xlabel('Tempo (s)')
plt.ylabel('Valores')
plt.legend()
plt.grid()
plt.tight_layout()  # Ajusta o layout para evitar sobreposição
plt.show()