import control as ctrl
import numpy as np

def controlador_imc(k, tau, theta, lambda_):
    # Função de transferência do sistema de primeira ordem com atraso
    G_s = ctrl.tf([tau, 1], [k * lambda_, k])
    num_pade, den_pade = ctrl.pade(theta, 1)  # feito a Aproximação de Padé
    Pade_approx = ctrl.tf(num_pade, den_pade)
    return G_s * Pade_approx

def sintonizar_pid_imc(k, tau, theta, lambda_=1.0):
    Kp = (((2*tau) + theta)/ (k * (2*lambda_ + theta)))
    Ti = (tau + (theta/2))
    Td = ((tau * theta) / ((2*tau)+theta))
    return Kp, Ti, Td

def chr_sem_sobrevalor(k, tau, theta):
    Kp = ((0.6 * tau)/ (k * theta))
    Ti = tau
    Td = 0.5 * theta
    return Kp, Ti, Td

def resposta_malha_aberta(k, tau, tempo):
    # Função de transferência de malha aberta
    G_s = ctrl.tf([k], [tau, 1])
    t_out, y_out = ctrl.step_response(G_s, T=tempo)
    return t_out, y_out

def resposta_malha_fechada(k, tau, tempo):
    # Função de transferência de malha fechada (feedback unitário)
    G_s = ctrl.tf([k], [tau, 1])
    H_s = ctrl.feedback(G_s, 1)
    t_out, y_out = ctrl.step_response(H_s, T=tempo)
    return t_out, y_out
