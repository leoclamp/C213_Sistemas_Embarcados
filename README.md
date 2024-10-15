# Projeto Prático de Sistemas Embarcados

## Pré-requisitos

Para executar este projeto, você precisará ter algumas bibliotecas python instaladas em sua máquina:

```sh
    pip install numpy
```
```sh
    pip install scipy
```
```sh
    pip install matplotlib
```
```sh
    pip install control
```
```sh
    pip install tkinter
```

## Arquivos do Projeto de Controle PID
- `leitura_dataset`: Esse arquivo carrega e visualiza os dados de entrada e saída de um sistema de controle usando o dataset Dataset_Grupo3.mat.
- `metodo_smith_malha_aberta`: Esse arquivo utiliza o método de Smith para identificar e modelar um sistema de controle de motor em malha aberta.
- `metodo_smith_malha_fechada`: Esse arquivo utiliza o método de Smith para identificar e modelar um sistema de controle de motor em malha fechada.
- `metodo_sundaresan_malha_aberta`: Esse arquivo utiliza o método de Sundaresan para identificar e modelar um sistema de controle de motor em malha aberta.
- `metodo_sundaresan_malha_fechada`: Esse arquivo utiliza o método de Sundaresan para identificar e modelar um sistema de controle de motor em malha fechada.
- `comparando_resposta_metodo_escolhido(smith)`: Este arquivo identifica os parâmetros do sistema usando o Método de Smith, calcula e compara as respostas para os modelos de malha aberta e malha fechada.
- `Controlador_PID(IMC)`: Esse arquivo implementa um modelo de controle PID (método IMC) para o sistema em malha fechada.
- `Controlador_PID(CHR_sem_sobrevalor)`: Esse arquivo implementa um modelo de controle PID (método CHR sem sobrevalor) para o sistema em malha fechada.
- `interface_PID`: Esse arquivo cria uma interface gráfica usando Tkinter para permitir que o usuário insira os parâmetros do controlador PID (Kp, Ti, Td) e o setpoint desejado. Ele também gera um gráfico da resposta ao degrau do sistema com o controlador PID atualizado.

## Métodos de Smith e Sundaresan

 - A imagem abaixo apresenta a resposta ao degrau obtida pela identificação pelos métodos de Smith e Sundaresan, juntamente com suas respectivas funções de transferência.

![metodo_smith](./imagens/metodo_smith_malha_aberta.png)

![metodo_sundaresan](./imagens/metodo_sundaresan_malha_aberta.png)

![funções de transferência](./imagens/função_transferência_smith_e_sundaresan.png)

## Comparação entre malha (aberta e fechada) do método Smith

 - A imagem abaixo apresenta a comparação entre a malha aberta e fechada obtidas pelo método Smith

![comparação entre malha aberta e fechada](./imagens/comparação_malha_aberta_e_fechada.png)

## Controlador PID (IMC)

 - A imagem abaixo apresenta a sintonização de um Controlador PID de acordo com o método IMC

![sintonização PID com método IMC](./imagens/sistema_com_controle_PID_(IMC).png)

## Controlador PID (CHR sem sobrevalor)

 - A imagem abaixo apresenta a sintonização de um Controlador PID de acordo com o método CHR sem sobrevalor

![sintonização PID com método CHR sem sobrevalor](./imagens/sistema_com_controle_PID_(CHR_sem_sobrevalor).png)

