import matplotlib.pyplot as plt

# Grafico da resposta gerada pelo dataset
def plotar_resposta(tempo, entrada, saida, titulo="Resposta do Sistema"):
    plt.figure(figsize=(12, 6))
    plt.plot(tempo, entrada, label='Entrada', color='blue')
    plt.plot(tempo, saida, label='Saída', color='orange')
    plt.title(titulo)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Resposta')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()


def plotar_resposta_modelo(tempo, saida_real, saida_modelo, titulo="Comparação entre Modelo e Resposta Real"):
    plt.figure(figsize=(12, 6))
    plt.plot(tempo, saida_real, label='Saída Real', color='orange')
    plt.plot(tempo, saida_modelo, label='Modelo Estimado', color='green', linestyle='--')
    plt.title(titulo)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Resposta')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()
