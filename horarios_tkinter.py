# encoding: utf-8
# Graphical User Interface for the application
import tkinter as tk
from tkinter import filedialog
from algoritmo_genetico import prueba




ROOT = tk.Tk()

def run_algorithm():
    prueba(filedialog.askopenfilename(initialdir="", title="choose your assignments file"))


def startx():
    ## base window

    ROOT.title("Generador de horarios")
    ROOT.minsize(300, 300)
    ROOT.geometry("400x400")
    btn_run = tk.Button(ROOT, text="Generate schedule", command=run_algorithm)
    btn_run.pack()
    ROOT.mainloop()

    ## base window


startx()








