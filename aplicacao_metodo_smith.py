import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import control as ctrl

# Carregar o dataset
file_path = 'Dataset_Grupo3.mat'  # Altere o nome do arquivo conforme necessário
data = sio.loadmat(file_path)

# Extraindo entrada, saída e tempo
entrada = data['TARGET_DATA____ProjetoC213_Degrau'][1]  # A segunda linha é a entrada
saida = data['TARGET_DATA____ProjetoC213_PotenciaMotor'][1]  # A segunda linha é a saída
tempo = data['TARGET_DATA____ProjetoC213_Degrau'][0]  # A primeira linha é o tempo

# 1. Determinar o valor final da saída
valor_final = saida[-1]

# 2. Encontrar os tempos correspondentes a 28,3% e 63,2% do valor final
y1 = 0.283 * valor_final
y2 = 0.632 * valor_final

# Encontrar t1 e t2 nos dados
t1 = tempo[np.where(saida >= y1)[0][0]]
t2 = tempo[np.where(saida >= y2)[0][0]]

# 3. Calcular τ e θ usando o Método de Smith
tau = 1.5 * (t2 - t1)
theta = t2 - tau

# 4. Calcular o ganho k
amplitude_degrau = entrada.mean()  # Amplitude do degrau de entrada
k = (valor_final - saida[0]) / amplitude_degrau

# 5. Modelo Identificado usando a Função de Transferência
# Modelo: G(s) = k * exp(-theta*s) / (tau * s + 1)
def modelo_identificado(k, tau, theta):
    # Função de transferência do sistema de primeira ordem: G(s) = k / (tau * s + 1)
    G_s = ctrl.tf([k], [tau, 1])
    # Aproximação de Pade para o atraso
    num_pade, den_pade = ctrl.pade(theta, 5)  # Aproximação de ordem 5
    Pade_approx = ctrl.tf(num_pade, den_pade)
    # Função de transferência com atraso
    return G_s * Pade_approx

# 6. Calcular a resposta estimada usando o modelo
resposta_modelo = modelo_identificado(k, tau, theta)

# 7. Simular a resposta ao degrau do modelo identificado
t_sim, y_modelo = ctrl.step_response(resposta_modelo*amplitude_degrau, T=tempo)

# 8. Cálculo do Erro Quadrático Médio (EQM)
EQM = np.sqrt(np.sum((y_modelo - saida) ** 2) / len(saida))

# 9. Visualização dos Resultados
plt.figure(figsize=(12, 6))
plt.plot(tempo, saida, 'orange', label='Resposta Real do Sistema')
plt.plot(tempo, entrada, label='Entrada (Degrau)', color='blue')
plt.plot(t_sim, y_modelo, 'r--', label='Modelo Identificado (Smith)')
plt.title('Identificação da Planta pelo Método de Smith')
plt.xlabel('Tempo (s)')
plt.ylabel('Potência do Motor')
plt.legend()
plt.grid()
plt.tight_layout()

# Adicionando os parâmetros identificados no gráfico em uma caixa delimitada
props = dict(boxstyle='round', facecolor='white', alpha=0.6)  # Estilo da caixa

textstr = '\n'.join((
    f'Ganho (k): {k:.4f}',
    f'Tempo de Atraso (θ): {theta:.4f} s',
    f'Constante de Tempo (τ): {tau:.4f} s',
    f'(EQM): {EQM:.4f}'))

# Posicionar a caixa com os resultados no gráfico
plt.text(tempo[-1] * 0.77, max(saida) * 0.7, textstr, fontsize=10, bbox=props)

plt.show()

# Exibir os resultados
print(f'Método de Identificação: Smith')
print(f'Parâmetros Identificados:')
print(f'Ganho (k): {k:.4f}')
print(f'Tempo de Atraso (θ): {theta:.4f} s')
print(f'Constante de Tempo (τ): {tau:.4f} s')
print(f'Erro Quadrático Médio (EQM): {EQM}')

