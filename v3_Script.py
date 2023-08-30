import pandas as pd
import math
from datetime import datetime
import tkinter as tk
from tkinter import Label, Entry, Button, Frame, ttk, StringVar, OptionMenu, messagebox

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

    if len(agenda) == 0:
        dose = qtd_inicial_elemento
        resto = dose
    else:
        dose_anterior = agenda.iloc[-1]['Resto']
        elemento_idx = MV.index[MV['Elemento'] == elemento_selecionado].tolist()[0]
        meia_vida = MV.iloc[elemento_idx]['Tempo_Meia_Vida']
        horario_anterior = datetime.strptime(agenda.iloc[-1]['Horário'], '%H:%M')
        horario_atual = horario_exame
        dose = dose_anterior * math.exp(((-math.log(2)) / meia_vida) * (horario_atual - horario_anterior).total_seconds() / 3600)
        resto = dose - (peso_paciente * 0.1)


    if len(agenda) == 0 or (len(agenda) > 0 and resto >= 0):
        if messagebox.askyesno("Confirmação", f"Tem certeza que deseja adicionar o encaixe?\nDose disponível: {resto:.2f} mCi"):
            agenda.loc[len(agenda)] = [len(agenda) + 1, peso_paciente, horario_exame.time(), elemento_selecionado, dose, resto]
            atualizar_doses()
            atualizar_agenda()
            messagebox.showinfo("Sucesso", "Encaixe adicionado com sucesso!")
    else:
        messagebox.showerror("Erro", "Não há dose suficiente para este encaixe!")

def excluir_agendamento(paciente):
    if messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o agendamento do paciente {paciente}?"):
        agenda.drop(paciente - 1, inplace=True)
        atualizar_doses()
        atualizar_agenda()

def atualizar_doses():
    for idx, row in agenda.iterrows():
        if idx == 0:
            agenda.at[idx, 'Resto'] = row['Dose Agendada']
        else:
            elemento_idx = MV.index[MV['Elemento'] == row['Elemento']].tolist()[0]
            meia_vida = MV.iloc[elemento_idx]['Tempo_Meia_Vida']
            dose_anterior = agenda.iloc[idx - 1]['Resto']
            horario_anterior = datetime.strptime(agenda.iloc[idx - 1]['Horário'], '%H:%M')
            horario_atual = datetime.strptime(row['Horário'], '%H:%M')
            dose_atual = dose_anterior * math.exp(((-math.log(2)) / meia_vida) * (horario_atual - horario_anterior).total_seconds() / 3600)
            agenda.at[idx, 'Dose Agendada'] = dose_atual
            agenda.at[idx, 'Resto'] = dose_atual

def atualizar_agenda():
    agenda_frame.destroy()
    agenda_frame_update()

def agenda_frame_update():
    global agenda_frame
    agenda_frame = Frame(tab2)
    agenda_frame.pack()

    Label(agenda_frame, text="Agenda", font=("Segoe UI", 14, "bold")).grid(row=0, columnspan=5, pady=10)

    for idx, row in agenda.iterrows():
        paciente = int(row['Paciente'])
        Label(agenda_frame, text=f"Paciente {paciente}", font=("Segoe UI", 12, "bold")).grid(row=idx + 1, column=0, pady=5)
        Label(agenda_frame, text=f"Peso: {row['Peso']} kg", font=("Segoe UI", 10)).grid(row=idx + 1, column=1, pady=5)
        Label(agenda_frame, text=f"Horário: {row['Horário']}", font=("Segoe UI", 10)).grid(row=idx + 1, column=2, pady=5)
        Label(agenda_frame, text=f"Elemento: {row['Elemento']}", font=("Segoe UI", 10)).grid(row=idx + 1, column=3, pady=5)
        Label(agenda_frame, text=f"Dose Agendada: {row['Dose Agendada']:.2f} mCi", font=("Segoe UI", 10)).grid(row=idx + 1, column=4, pady=5)
        Label(agenda_frame, text=f"Resto: {row['Resto']:.2f} mCi", font=("Segoe UI", 10)).grid(row=idx + 1, column=5, pady=5)
        Button(agenda_frame, text="Excluir", font=("Segoe UI", 10), command=lambda p=paciente: excluir_agendamento(p)).grid(row=idx + 1, column=6, pady=5)

root = tk.Tk()
root.title("Agenda PET CT")
root.geometry("800x600")

tab_control = ttk.Notebook(root)

tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)

tab_control.add(tab1, text="Agendar Encaixe")
tab_control.add(tab2, text="Visualizar Agenda")
tab_control.pack(expand=1, fill="both")

elemento_var = tk.IntVar()
elemento_var.set(0)

Label(tab1, text="Agendar Encaixe", font=("Segoe UI", 14, "bold")).pack(pady=10)

peso_label = Label(tab1, text="Peso do Paciente (kg):")
peso_label.pack()
peso_entry = Entry(tab1)
peso_entry.pack()

horario_exame_label = Label(tab1, text="Horário do Exame (HH:MM):")
horario_exame_label.pack()
horario_exame_entry = Entry(tab1)
horario_exame_entry.pack()

elemento_label = Label(tab1, text="Elemento:")
elemento_label.pack()
elemento_dropdown = OptionMenu(tab1, elemento_var, *range(len(MV["Elemento"])))
elemento_dropdown.pack()

horario_chegada_elemento_label = Label(tab1, text="Horário de Chegada do Elemento (HH:MM):")
horario_chegada_elemento_label.pack()
horario_chegada_elemento_entry = Entry(tab1)
horario_chegada_elemento_entry.pack()

qtd_inicial_elemento_label = Label(tab1, text="Quantidade Inicial do Elemento (mCi):")
qtd_inicial_elemento_label.pack()
qtd_inicial_elemento_entry = Entry(tab1)
qtd_inicial_elemento_entry.pack()

calcular_button = Button(tab1, text="Calcular Dose e Agendar", command=calcular_dose)
calcular_button.pack()

atualizar_button = Button(tab2, text="Atualizar Agenda", command=atualizar_agenda)
atualizar_button.pack()

agenda_frame_update()

root.mainloop()
