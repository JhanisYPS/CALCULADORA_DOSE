import pandas as pd
import math
from datetime import datetime
import tkinter as tk
from tkinter import Label, Entry, Button, Frame, ttk, StringVar, OptionMenu

MV = {
    'Elemento': ["Tecnécio", "Iodo123", "Iodo131", "Gálio", "Flúor"],
    'Tempo_Meia_Vida': [6, 13.2, 192, 1.13, 1.82]
}

MV = pd.DataFrame(MV)
agenda = pd.DataFrame(columns=['Paciente', 'Peso', 'Horário', 'Elemento', 'Dose Agendada', 'Resto'])

def calcular_dose():
    peso_paciente = float(peso_entry.get())
    horario_exame = datetime.strptime(horario_exame_entry.get(), '%H:%M')
    escolha = elemento_var.get()
    elemento_selecionado = MV["Elemento"].iloc[escolha]
    meia_vida = MV["Tempo_Meia_Vida"].iloc[escolha]
    horario_chegada_elemento = datetime.strptime(horario_chegada_elemento_entry.get(), '%H:%M')
    qtd_inicial_elemento = float(qtd_inicial_elemento_entry.get())

    if len(agenda) > 0:
        qtd_inicial_elemento = agenda.iloc[-1]['Resto']

    dose = qtd_inicial_elemento * math.exp(((-math.log(2)) / meia_vida) * (horario_chegada_elemento - horario_exame).total_seconds() / 3600)
    resto = dose - (peso_paciente * 0.1)

    resultado_label.config(text=f"Elemento: {elemento_selecionado}\nMeia Vida: {meia_vida}\nDose do paciente agendado: {dose:.2f}\nResto de elemento ativo pós exame: {resto:.2f} mCi")

    agenda.loc[len(agenda)] = [len(agenda) + 1, peso_paciente, horario_exame.time(), elemento_selecionado, dose, resto]

def atualizar_agenda():
    agenda_frame.destroy()
    agenda_frame_update()

def agenda_frame_update():
    global agenda_frame
    agenda_frame = Frame(tab2)
    agenda_frame.pack()

    Label(agenda_frame, text="Agenda", font=("Helvetica", 14, "bold")).grid(row=0, columnspan=4, pady=10)

    for idx, row in agenda.iterrows():
        Label(agenda_frame, text=f"Paciente {int(row['Paciente'])}", font=("Helvetica", 12, "bold")).grid(row=idx + 1, column=0, pady=5)
        Label(agenda_frame, text=f"Peso: {row['Peso']} kg").grid(row=idx + 1, column=1, pady=5)
        Label(agenda_frame, text=f"Horário: {row['Horário']}").grid(row=idx + 1, column=2, pady=5)
        Label(agenda_frame, text=f"Elemento: {row['Elemento']}").grid(row=idx + 1, column=3, pady=5)
        Label(agenda_frame, text=f"Dose Agendada: {row['Dose Agendada']}").grid(row=idx + 1, column=4, pady=5)
        Label(agenda_frame, text=f"Resto: {row['Resto']:.2f} mCi").grid(row=idx + 1, column=5, pady=5)

root = tk.Tk()
root.title("Agenda de Exames")

tab_control = ttk.Notebook(root)

tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)

tab_control.add(tab1, text='Inserir/Remover Exame')
tab_control.add(tab2, text='Visualizar Agenda')

tab_control.pack(expand=1, fill='both')

# Tab 1 - Inserir/Remover Exame
peso_label = Label(tab1, text="Peso do Paciente (kg):")
peso_label.pack()

peso_entry = Entry(tab1)
peso_entry.pack()

horario_exame_label = Label(tab1, text="Horário do Exame (HH:MM):")
horario_exame_label.pack()

horario_exame_entry = Entry(tab1)
horario_exame_entry.pack()

elemento_label = Label(tab1, text="Escolha o Elemento:")
elemento_label.pack()

elemento_var = tk.StringVar()
elemento_menu = OptionMenu(tab1, elemento_var, *range(len(MV)))
elemento_menu.pack()

horario_chegada_elemento_label = Label(tab1, text="Horário de Chegada do Elemento (HH:MM):")
horario_chegada_elemento_label.pack()

horario_chegada_elemento_entry = Entry(tab1)
horario_chegada_elemento_entry.pack()

qtd_inicial_elemento_label = Label(tab1, text="Quantidade Inicial do Elemento (mCi):")
qtd_inicial_elemento_label.pack()

qtd_inicial_elemento_entry = Entry(tab1)
qtd_inicial_elemento_entry.pack()

calcular_button = Button(tab1, text="Calcular", command=calcular_dose)
calcular_button.pack()

resultado_label = Label(tab1, text="")
resultado_label.pack()

# Tab 2 - Visualizar Agenda
atualizar_button = Button(tab2, text="Atualizar Agenda", command=atualizar_agenda)
atualizar_button.pack()

agenda_frame_update()

root.mainloop()
