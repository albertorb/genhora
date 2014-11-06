#encoding: utf-8
# Graphical User Interface for the application
import tkinter as tk
#import algoritmo_genetico as ag


ASSIGNMENTS = {
    'Alberto': 'Matematicas 1A, Ingles 2B,Ingles 3B',
    'Eugenia': 'Ingles 4C',
    'Caridad': 'Aleman 2B,Fisica 1A,Ingles 2C',
    'Batman': 'Ingles 2B'
}
ROOT = tk.Tk()


def top_addprof():
    top_addprf = tk.Toplevel()
    lbl_name = tk.Label(top_addprf, text='NAME')
    lbl_name.grid(row=0, column=1)
    lbl_sbj = tk.Label(top_addprf, text='SUBJECTS')
    lbl_sbj.grid(row=0, column=2)
    if ASSIGNMENTS is not None:

        ro = 1
        for professor, subjects in ASSIGNMENTS.items():
            txt_prof = tk.Label(top_addprf, text=professor + ': ')
            txt_prof.grid(row=ro, column=1)
            txt_subj = tk.Label(top_addprf, text=subjects + ': ')
            txt_subj.grid(row=ro, column=2)
            ro += 1
    top_addprf.mainloop()


def startx():
    ## base window

    ROOT.title("Generador de horarios")
    ROOT.minsize(300, 300)
    ROOT.geometry("400x400")

    #label_entry_professorNumber = tk.Label(root, text="Professor name")
    #label_entry_professorNumber.pack()
    #entry_professorNumber = tk.Entry()
    #entry_professorNumber.pack()

    #label_entry_subjectNumber = tk.Label(root, text="Subject number")
    #label_entry_subjectNumber.pack()
    #entry_subjectNumber = tk.Entry()
    #entry_subjectNumber.pack()

    btn_addprof = tk.Button(ROOT, text="Add a professor", command=top_addprof)
    btn_addprof.pack()

    btn_run = tk.Button(ROOT, text="Start")
    btn_run.pack()
    ROOT.mainloop()

    ## base window


startx()


def insertData():
    profnumber = int(entry_professorNumber.get())
    ag.prueba(int(entry_professorNumber.get()), int(entry_subjectNumber.get()))


button_insertData = tk.Button(ROOT, text="Generate schedule", command=insertData)
button_insertData.pack()






