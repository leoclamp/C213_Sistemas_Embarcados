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

# 5. função de tranferencia do modelo
def modelo_identificado(k, tau, theta):
    G_s = ctrl.tf([k], [tau, 1])
    H_s = ctrl.feedback(G_s, 1)
    # Aproximação de Pade para o atraso
    num_pade, den_pade = ctrl.pade(theta, 5)  # Aproximação de ordem 5
    Pade_approx = ctrl.tf(num_pade, den_pade)
    # Função de transferência com atraso
    return ctrl.series(H_s, Pade_approx)

# 6. Calcular a resposta estimada usando o modelo
resposta_modelo = modelo_identificado(k, tau, theta)

# Calculando os valores de kp, ti e td
lamb = 20 # lambda tem que ser maior que 10.2 (lamb/theta > 0.8)
kp = ((2*tau)+theta)/(k*((2*lamb)+theta))
ti = tau+(theta/2)
td = (tau*theta)/((2*tau)+theta)

# 7. função do PID
def funcao_PID(kp, ti, td):
    pid = ctrl.tf([kp*td, kp, kp/ti], [1, 0])
    return pid

PID = funcao_PID(kp, ti, td)

# Sistema em malha fechada com controlador PID e modelo identificado
sistema_em_malha_fechada = ctrl.feedback(ctrl.series(PID, resposta_modelo))

# Simulação da resposta ao degrau
t_sim, y_modelo = ctrl.step_response(sistema_em_malha_fechada)

# 9. Visualização dos Resultados
plt.figure(figsize=(12, 6))
plt.plot(t_sim, y_modelo, 'orange', label='PID')
plt.title('Sistema com controle PID\n Sistema lento, sem overshoot (ts elevado)')
plt.xlabel('Tempo (s)')
plt.ylabel('Potência do Motor')
plt.legend()
plt.grid()
plt.tight_layout()

info = ctrl.step_info(sistema_em_malha_fechada)

# Adicionando os parâmetros identificados no gráfico em uma caixa delimitada
props = dict(boxstyle='round', facecolor='white', alpha=0.6)  # Estilo da caixa

textstr = '\n'.join((
    f'Tempo de subida(tr): {info['RiseTime']:.4f} s',
    f'Tempo de acomodação(ts): {info['SettlingTime']:.4f} s'))

# Posicionar a caixa com os resultados no gráfico
plt.text(tempo[-1] * 6, 0.7, textstr, fontsize=10, bbox=props)

plt.show()

# Exibir os resultados
print(f'Sistema com controle PID')
print(f'respostas:')

info = ctrl.step_info(sistema_em_malha_fechada)
print(f"Tempo de subida(tr): {info['RiseTime']:.4f} s")
print(f"Tempo de acomodação(ts): {info['SettlingTime']:.4f} s")
print(f"valor de pico: {info['Peak']:.4f}")

