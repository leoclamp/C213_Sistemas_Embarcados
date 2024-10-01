from LeituraDataset import carregar_dados
from IdentificarModelo import metodo_smith, metodo_sundaresan
from Controladores import controlador_imc, sintonizar_pid_imc,chr_sem_sobrevalor, resposta_malha_aberta, resposta_malha_fechada
from Plotagem import plotar_resposta, plotar_resposta_modelo

def main():
    # Carregar dados do dataset
    entrada, saida, tempo = carregar_dados()

    # método de identificação (Smith ou Sundaresan)
    metodo = "Smith"
    if metodo == "Smith":
        tau, theta = metodo_smith(tempo, saida)
    else:
        tau, theta = metodo_sundaresan(tempo, saida)

    # Calcular ganho k
    valor_final = saida[-1]
    k = (valor_final - saida[0]) / entrada.mean()

    # IMC
    lambda_ = 1.0  # Parâmetro de suavização
    Kp_imc, Ti_imc, Td_imc = sintonizar_pid_imc(k, tau, theta, lambda_)
    

    # CHR sem sobrevalor
    Kp_chr, Ti_chr, Td_chr = chr_sem_sobrevalor(k, tau, theta)

    # Resposta em malha aberta e fechada
    t_aberta, y_aberta = resposta_malha_aberta(k, tau, tempo)
    t_fechada, y_fechada = resposta_malha_fechada(k, tau, tempo)

    # Plotar as respostas
    plotar_resposta(tempo, entrada, saida, "Entrada e Saída do Sistema")
    plotar_resposta_modelo(tempo, saida, y_aberta, "Resposta em Malha Aberta")
    plotar_resposta_modelo(tempo, saida, y_fechada, "Resposta em Malha Fechada")

if __name__ == "__main__":
    main()
