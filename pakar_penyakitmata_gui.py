import tkinter as tk
from tkinter import ttk, messagebox
from pyswip import Prolog

prolog = Prolog()
prolog.consult("pakar_penyakitmata_gui.pl")

# Variabel global
penyakit = []
gejala = {}
index_penyakit = 0
index_gejala = 0
current_penyakit = ""
current_gejala = ""

# Fungsi mulai diagnosa
def mulai_diagnosa():
    global penyakit, gejala, index_penyakit, index_gejala
    prolog.retractall("gejala_pos(_)")  # Reset jawaban
    prolog.retractall("gejala_neg(_)")

    start_btn.configure(state=tk.DISABLED)
    yes_btn.configure(state=tk.NORMAL)
    no_btn.configure(state=tk.NORMAL)

    penyakit = [p["X"].decode() for p in prolog.query("penyakit(X)")]
    gejala.clear()
    for p in penyakit:
        gejala[p] = [g["X"] for g in prolog.query(f'gejala(X, "{p}")')]

    index_penyakit = 0
    index_gejala = -1
    pertanyaan_selanjutnya()

# Fungsi navigasi pertanyaan
def pertanyaan_selanjutnya(ganti_penyakit=False):
    global current_penyakit, current_gejala, index_penyakit, index_gejala

    if ganti_penyakit:
        index_penyakit += 1
        index_gejala = -1

    if index_penyakit >= len(penyakit):
        hasil_diagnosa()
        return

    current_penyakit = penyakit[index_penyakit]
    index_gejala += 1

    if index_gejala >= len(gejala[current_penyakit]):
        hasil_diagnosa(current_penyakit)
        return

    current_gejala = gejala[current_penyakit][index_gejala]

    if list(prolog.query(f"gejala_pos({current_gejala})")):
        pertanyaan_selanjutnya()
        return
    elif list(prolog.query(f"gejala_neg({current_gejala})")):
        pertanyaan_selanjutnya(ganti_penyakit=True)
        return

    pertanyaan = prolog.query(f"pertanyaan({current_gejala}, Y)").__next__()["Y"].decode()
    tampilkan_pertanyaan(pertanyaan)

# Tampilkan pertanyaan
def tampilkan_pertanyaan(pertanyaan):
    kotak_pertanyaan.configure(state=tk.NORMAL)
    kotak_pertanyaan.delete(1.0, tk.END)
    kotak_pertanyaan.insert(tk.END, pertanyaan)
    kotak_pertanyaan.configure(state=tk.DISABLED)

# Fungsi jawaban
def jawaban(jwb):
    if jwb:
        prolog.assertz(f"gejala_pos({current_gejala})")
        pertanyaan_selanjutnya()
    else:
        prolog.assertz(f"gejala_neg({current_gejala})")
        pertanyaan_selanjutnya(ganti_penyakit=True)

# Fungsi hasil
def hasil_diagnosa(penyakit=""):
    if penyakit:
        messagebox.showinfo("Hasil Diagnosa", f"💡 Kemungkinan Anda mengalami: {penyakit}")
    else:
        messagebox.showinfo("Hasil Diagnosa", "❗Tidak dapat menentukan jenis penyakit mata berdasarkan gejala Anda.")

    yes_btn.configure(state=tk.DISABLED)
    no_btn.configure(state=tk.DISABLED)
    start_btn.configure(state=tk.NORMAL)

# GUI
root = tk.Tk()
root.title("Sistem Pakar Diagnosis Penyakit Mata")
root.configure(bg="#f0f4f8")
root.geometry("500x350")
root.resizable(False, False)

style = ttk.Style()
style.configure("TFrame", background="#f0f4f8")
style.configure("TLabel", background="#f0f4f8", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)

mainframe = ttk.Frame(root, padding="20")
mainframe.pack(fill="both", expand=True)

judul = ttk.Label(mainframe, text="🧠 Diagnosa Penyakit Mata", font=("Segoe UI", 16, "bold"))
judul.pack(pady=(0, 10))

kotak_pertanyaan = tk.Text(mainframe, height=4, width=55, state=tk.DISABLED, wrap=tk.WORD, font=("Segoe UI", 10))
kotak_pertanyaan.pack(pady=10)

btn_frame = ttk.Frame(mainframe)
btn_frame.pack(pady=10)

yes_btn = ttk.Button(btn_frame, text="✅ Ya", state=tk.DISABLED, width=12, command=lambda: jawaban(True))
yes_btn.grid(row=0, column=0, padx=10)

no_btn = ttk.Button(btn_frame, text="❌ Tidak", state=tk.DISABLED, width=12, command=lambda: jawaban(False))
no_btn.grid(row=0, column=1, padx=10)

start_btn = ttk.Button(mainframe, text="▶️ Mulai Diagnosa", width=25, command=mulai_diagnosa)
start_btn.pack(pady=15)

root.mainloop()
