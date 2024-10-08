import tkinter as tk
from tkinter import ttk
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
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


# Função para atualizar o PID com os parâmetros definidos pelo usuário
def atualizar_PID():
    # Obter os parâmetros de entrada do usuário
    kp = float(entry_kp.get())
    ti = float(entry_ti.get())
    td = float(entry_td.get())
    setpoint = float(entry_setpoint.get())

    # Configurar a função de transferência do PID
    pid = ctrl.tf([kp * td, kp, kp / ti], [1, 0])

    # Sistema em malha fechada com PID e modelo identificado
    sistema_em_malha_fechada = ctrl.feedback(ctrl.series(pid, resposta_modelo))

    # Simular resposta ao degrau considerando o setpoint fornecido
    t_sim, y_modelo = ctrl.step_response(sistema_em_malha_fechada * setpoint)

    # Plotar a resposta
    plt.figure(figsize=(12, 6))
    plt.plot(t_sim, y_modelo, 'orange', label='Resposta do sistema com PID')
    plt.axhline(setpoint, color='blue', linestyle='--', label='Setpoint')
    plt.title('Resposta do sistema com controle PID')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Potência do Motor')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

# Configurar a janela principal
root = tk.Tk()
root.title("Controle PID")

# Parâmetros PID
frame_pid = ttk.LabelFrame(root, text="Parâmetros PID", padding=(20, 10))
frame_pid.grid(row=0, column=0, padx=20, pady=10)

ttk.Label(frame_pid, text="Kp:").grid(row=0, column=0)
entry_kp = ttk.Entry(frame_pid)
entry_kp.grid(row=0, column=1)

ttk.Label(frame_pid, text="Ti:").grid(row=1, column=0)
entry_ti = ttk.Entry(frame_pid)
entry_ti.grid(row=1, column=1)

ttk.Label(frame_pid, text="Td:").grid(row=2, column=0)
entry_td = ttk.Entry(frame_pid)
entry_td.grid(row=2, column=1)

# Parâmetro Setpoint
frame_setpoint = ttk.LabelFrame(root, text="Setpoint", padding=(20, 10))
frame_setpoint.grid(row=1, column=0, padx=20, pady=10)

ttk.Label(frame_setpoint, text="Setpoint:").grid(row=0, column=0)
entry_setpoint = ttk.Entry(frame_setpoint)
entry_setpoint.grid(row=0, column=1)

# Botão para atualizar o gráfico
button_update = ttk.Button(root, text="Atualizar Gráfico", command=atualizar_PID)
button_update.grid(row=2, column=0, pady=20)

root.mainloop()

