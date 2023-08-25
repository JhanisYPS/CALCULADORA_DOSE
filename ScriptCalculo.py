import pandas as pd
import math
from datetime import datetime

MV = {
    'Elemento':["Tecnécio","Iodo123","Iodo131","Gálio","Flúor"],
    'Tempo_Meia_Vida':[6,13.2,192,1.13,1.82]
}

MV = pd.DataFrame(MV)

#Dados necessários
Peso_Paciente = float(input("Qual o peso do paciente em kg?"))

Dose = Peso_Paciente*0.1

Horario_Exame = datetime.strptime(input("Qual o horário do exame?(HH:MM)"),'%H:%M')

print("Escolha o elemento a ser utilizado informando o index:\n",MV["Elemento"],"\nElemento: ")

Escolha=int(input())

Elemento_Selecionado = MV["Elemento"].filter(items = [Escolha], axis=0)

Meia_Vida = MV["Tempo_Meia_Vida"].filter(items = [Escolha], axis=0)

Horario_Chegada_Elemento = datetime.strptime(input("Qual o horário de chegada do elemento?(HH:MM)"),'%H:%M')

QTD_Inicial_Elemento = input("Qual é a quantidade de elemento que chegou ao hospital?(em mCI)")

print(Meia_Vida.loc[])

Resto = (QTD_Inicial_Elemento*math.exp(((-math.log(2))/Meia_Vida.values())*(Horario_Chegada_Elemento-Horario_Exame).total_seconds()/3600))-Dose

print(
    "O Elemento escolhido foi: {}",
    "O Tempo de Meia Vida dele é: {}",
    "A dose do paciente agendado é: {}",
    "O resto de elemento ativo pós exame é:{}".format(Elemento_Selecionado,Meia_Vida,Dose,Resto)
)

