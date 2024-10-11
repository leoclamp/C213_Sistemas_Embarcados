import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import control as ctrl

# Carregar o dataset
file_path = 'Dataset_Grupo3.mat'
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
def modelo_identificado_malha_aberta(k, tau, theta):
    G_s = ctrl.tf([k], [tau, 1])
    # Aproximação de Pade para o atraso
    num_pade, den_pade = ctrl.pade(theta, 5)  # Aproximação de ordem 5
    Pade_approx = ctrl.tf(num_pade, den_pade)
    # Função de transferência com atraso
    return ctrl.series(G_s, Pade_approx)

# 6. Modelo Identificado usando a Função de Transferência
def modelo_identificado_malha_fechada(k, tau, theta):
    G_s = ctrl.tf([k], [tau, 1])
    H_s = ctrl.feedback(G_s, 1)
    # Aproximação de Pade para o atraso
    num_pade, den_pade = ctrl.pade(theta, 5)  # Aproximação de ordem 5
    Pade_approx = ctrl.tf(num_pade, den_pade)
    # Função de transferência com atraso
    return ctrl.series(H_s, Pade_approx)

# 7. Calcular a resposta estimada usando o modelo
resposta_malha_aberta = modelo_identificado_malha_aberta(k, tau, theta)
resposta_malha_fechada = modelo_identificado_malha_fechada(k, tau, theta)

# 8. Simular a resposta ao degrau dos modelos
t_sim_aberta, y_modelo_aberta = ctrl.step_response(resposta_malha_aberta * amplitude_degrau, T=tempo)
t_sim_fechada, y_modelo_fechada = ctrl.step_response(resposta_malha_fechada * amplitude_degrau, T=tempo)

# 9. Calcular o Erro Quadrático Médio (EQM) para ambos os modelos
EQM_aberta = np.sqrt(np.sum((y_modelo_aberta - saida) ** 2) / len(saida))
EQM_fechada = np.sqrt(np.sum((y_modelo_fechada - saida) ** 2) / len(saida))

info_aberta = ctrl.step_info(resposta_malha_aberta)
info_fechada = ctrl.step_info(resposta_malha_fechada)

# 10. Visualização dos Resultados malha aberta
plt.figure(figsize=(12, 6))
plt.plot(t_sim_aberta, y_modelo_aberta, 'r', label='Modelo Identificado (Smith) Malha Aberta')
plt.plot(t_sim_fechada, y_modelo_fechada, 'b', label='Modelo Identificado (Smith) Malha Fechada')
plt.title('Comparação entre Malha Aberta e Fechada')
plt.xlabel('Tempo (s)')
plt.ylabel('Potência do Motor')
plt.legend()
plt.grid()
plt.tight_layout()

# Adicionando os parâmetros identificados no gráfico em uma caixa delimitada
props = dict(boxstyle='round', facecolor='white', alpha=0.6)  # Estilo da caixa

textstr = '\n'.join((
    f'Tempo de subida (Malha Aberta): {info_aberta['RiseTime']:.4f} s',
    f'Tempo de acomodação (Malha Aberta): {info_aberta['SettlingTime']:.4f} s',
    f'Valor final(pico) (Malha Aberta): {info_aberta['Peak']:.4f}\n',
    f'Tempo de subida (Malha Fechada): {info_fechada['RiseTime']:.4f} s',
    f'Tempo de acomodação (Malha Fechada): {info_fechada['SettlingTime']:.4f} s',
    f'Valor final(pico) (Malha Fechada): {info_fechada['Peak']:.4f}'))

# Posicionar a caixa com os resultados no gráfico
plt.text(tempo[-1] * 0.68, max(saida) * 0.6, textstr, fontsize=10, bbox=props)

plt.show()

# Comparação entre os sistemas em malha aberta e fechada
print('\nComparação entre Resposta do Sistema em Malha Aberta e Fechada:\n')

if info_aberta['RiseTime'] < info_fechada['RiseTime']:
    print('  - O sistema em malha aberta tem menor tempo de subida.')
else:
    print('  - O sistema em malha fechada tem menor tempo de subida.')

if info_aberta['SettlingTime'] < info_fechada['SettlingTime']:
    print('  - O sistema em malha aberta tem menor tempo de acomodação.')
else:
    print('  - O sistema em malha fechada tem menor tempo de acomodação.')

if info_aberta['Peak'] > info_fechada['Peak']:
    print('  - O sistema em malha aberta tem maior valor final(pico).')
else:
    print('  - O sistema em malha fechada tem maior valor final(pico).')

