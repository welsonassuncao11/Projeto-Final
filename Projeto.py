# Importa os módulos necessários
import tkinter as tk
from tkinter import messagebox
import sqlite3

# -----------------------------
# 1. Função para criar o banco de dados e a tabela, caso ainda não exista
# -----------------------------
def create_db():
    conn = sqlite3.connect('horas_trabalhadas.db')  # Cria ou conecta ao banco de dados
    cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS horas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            colaborador TEXT NOT NULL,
            cliente TEXT NOT NULL,
            tarefa TEXT NOT NULL,
            data TEXT NOT NULL,
            horas REAL NOT NULL
        )
    ''')  # Cria a tabela "horas" com os campos especificados
    conn.commit()  # Salva as alterações
    conn.close()   # Fecha a conexão com o banco

# -----------------------------
# 2. Função que valida se todos os campos foram preenchidos corretamente
# -----------------------------
def validar_campos():
    if not entry_colaborador.get() or not entry_cliente.get() or not entry_tarefa.get() or not entry_data.get() or not entry_horas.get():
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return False
    if not entry_horas.get().replace('.', '', 1).isdigit():  # Verifica se horas é um número
        messagebox.showerror("Erro", "Horas devem ser um número válido.")
        return False
    return True

# -----------------------------
# 3. Adiciona um novo registro de horas no banco de dados
# -----------------------------
def adicionar():
    if validar_campos():  # Verifica se os campos estão válidos
        colaborador = entry_colaborador.get()
        cliente = entry_cliente.get()
        tarefa = entry_tarefa.get()
        data = entry_data.get()
        horas = float(entry_horas.get())  # Converte o texto para número real

        conn = sqlite3.connect('horas_trabalhadas.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO horas (colaborador, cliente, tarefa, data, horas) VALUES (?, ?, ?, ?, ?)",
                       (colaborador, cliente, tarefa, data, horas))  # Insere no banco
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Registro adicionado com sucesso!")
        limpar_campos()
        listar()

# -----------------------------
# 4. Lista todos os registros no listbox
# -----------------------------
def listar():
    conn = sqlite3.connect('horas_trabalhadas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM horas")
    registros = cursor.fetchall()
    conn.close()

    listbox.delete(0, tk.END)  # Limpa o listbox antes de adicionar novos
    for r in registros:
        listbox.insert(tk.END, f"ID: {r[0]} | {r[1]} - {r[2]} | {r[3]} | {r[4]} | {r[5]}h")

# -----------------------------
# 5. Busca um registro pelo ID e preenche os campos
# -----------------------------
def buscar():
    id = entry_id.get()
    if id.isdigit():
        conn = sqlite3.connect('horas_trabalhadas.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM horas WHERE id = ?", (id,))
        dado = cursor.fetchone()
        conn.close()
        if dado:
            entry_colaborador.delete(0, tk.END)
            entry_colaborador.insert(tk.END, dado[1])
            entry_cliente.delete(0, tk.END)
            entry_cliente.insert(tk.END, dado[2])
            entry_tarefa.delete(0, tk.END)
            entry_tarefa.insert(tk.END, dado[3])
            entry_data.delete(0, tk.END)
            entry_data.insert(tk.END, dado[4])
            entry_horas.delete(0, tk.END)
            entry_horas.insert(tk.END, dado[5])
        else:
            messagebox.showwarning("Atenção", "Registro não encontrado.")

# -----------------------------
# 6. Atualiza um registro existente com base no ID
# -----------------------------
def atualizar():
    if entry_id.get().isdigit() and validar_campos():
        id = int(entry_id.get())
        colaborador = entry_colaborador.get()
        cliente = entry_cliente.get()
        tarefa = entry_tarefa.get()
        data = entry_data.get()
        horas = float(entry_horas.get())

        conn = sqlite3.connect('horas_trabalhadas.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE horas SET colaborador=?, cliente=?, tarefa=?, data=?, horas=? WHERE id=?",
                       (colaborador, cliente, tarefa, data, horas, id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Registro atualizado com sucesso!")
        limpar_campos()
        listar()
    else:
        messagebox.showerror("Erro", "ID inválido ou campos incompletos.")

# -----------------------------
# 7. Exclui um registro do banco de dados pelo ID
# -----------------------------
def excluir():
    id = entry_id.get()
    if id.isdigit():
        conn = sqlite3.connect('horas_trabalhadas.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM horas WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Registro excluído com sucesso.")
        limpar_campos()
        listar()
    else:
        messagebox.showerror("Erro", "ID inválido.")

# -----------------------------
# 8. Limpa os campos de entrada
# -----------------------------
def limpar_campos():
    for entry in [entry_id, entry_colaborador, entry_cliente, entry_tarefa, entry_data, entry_horas]:
        entry.delete(0, tk.END)

# -----------------------------
# 9. Interface gráfica com Tkinter
# -----------------------------
root = tk.Tk()
root.title("Controle de Horas - Escritório de Advocacia")

frame = tk.Frame(root, padx=60, pady=60)
frame.pack()

# Campos de entrada
tk.Label(frame, text="ID:").grid(row=0, column=0)
entry_id = tk.Entry(frame)
entry_id.grid(row=0, column=1)

tk.Label(frame, text="Colaborador:").grid(row=1, column=0)
entry_colaborador = tk.Entry(frame)
entry_colaborador.grid(row=1, column=1)

tk.Label(frame, text="Cliente:").grid(row=2, column=0)
entry_cliente = tk.Entry(frame)
entry_cliente.grid(row=2, column=1)

tk.Label(frame, text="Tarefa:").grid(row=3, column=0)
entry_tarefa = tk.Entry(frame)
entry_tarefa.grid(row=3, column=1)

tk.Label(frame, text="Data (DD/MM/AAAA):").grid(row=4, column=0)
entry_data = tk.Entry(frame)
entry_data.grid(row=4, column=1)

tk.Label(frame, text="Horas trabalhadas:").grid(row=5, column=0)
entry_horas = tk.Entry(frame)
entry_horas.grid(row=5, column=1)

# Botões
tk.Button(frame, text="Adicionar", command=adicionar).grid(row=6, column=0, pady=5)
tk.Button(frame, text="Buscar", command=buscar).grid(row=6, column=1)
tk.Button(frame, text="Atualizar", command=atualizar).grid(row=7, column=0)
tk.Button(frame, text="Excluir", command=excluir).grid(row=7, column=1)

# Listbox para mostrar registros
listbox = tk.Listbox(frame, width=80)
listbox.grid(row=8, column=0, columnspan=2, pady=20)

# Inicializa o banco e lista os registros
create_db()
listar()

# Inicia o loop principal da interface gráfica
root.mainloop()
