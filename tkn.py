import sqlite3
import tkinter as tk
from tkinter import messagebox

# Criar ou conectar ao banco de dados
conn = sqlite3.connect("ecobairro.db")
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT NOT NULL,
    pontos INTEGER NOT NULL,
    concluida INTEGER DEFAULT 0
)
""")
conn.commit()

# Função para adicionar uma nova tarefa
def adicionar_tarefa():
    nome = entry_nome.get()
    descricao = entry_descricao.get()
    pontos = int(combo_pontos.get())

    if nome and descricao:
        cursor.execute("INSERT INTO tarefas (nome, descricao, pontos) VALUES (?, ?, ?)", (nome, descricao, pontos))
        conn.commit()
        entry_nome.delete(0, tk.END)
        entry_descricao.delete(0, tk.END)
        atualizar_lista()
        messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")
    else:
        messagebox.showwarning("Erro", "Preencha todos os campos!")

# Função para concluir uma tarefa
def concluir_tarefa():
    try:
        selecao = lista_tarefas.curselection()
        if not selecao:
            messagebox.showwarning("Erro", "Selecione uma tarefa para concluir!")
            return

        tarefa_id = lista_tarefas.get(selecao).split(" - ")[0]
        cursor.execute("UPDATE tarefas SET concluida = 1 WHERE id = ?", (tarefa_id,))
        conn.commit()
        atualizar_lista()
        atualizar_ranking()
        messagebox.showinfo("Sucesso", "Tarefa concluída com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Função para excluir uma tarefa
def excluir_tarefa():
    try:
        selecao = lista_tarefas.curselection()
        if not selecao:
            messagebox.showwarning("Erro", "Selecione uma tarefa para excluir!")
            return

        tarefa_id = lista_tarefas.get(selecao).split(" - ")[0]
        cursor.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
        conn.commit()
        atualizar_lista()
        atualizar_ranking()
        messagebox.showinfo("Sucesso", "Tarefa excluída com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Função para atualizar a lista de tarefas
def atualizar_lista(filtro=None):
    lista_tarefas.delete(0, tk.END)

    query = "SELECT id, nome, descricao, pontos, concluida FROM tarefas"
    if filtro is not None:
        query += f" WHERE concluida = {filtro}"
    
    cursor.execute(query)
    for tarefa in cursor.fetchall():
        status = "✅" if tarefa[4] else "⏳"
        lista_tarefas.insert(tk.END, f"{tarefa[0]} - {tarefa[1]} ({tarefa[2]}) - {tarefa[3]} pontos {status}")

# Função para exibir apenas tarefas pendentes
def filtrar_pendentes():
    atualizar_lista(filtro=0)

# Função para exibir apenas tarefas concluídas
def filtrar_concluidas():
    atualizar_lista(filtro=1)

# Função para atualizar o ranking
def atualizar_ranking():
    lista_ranking.delete(0, tk.END)

    cursor.execute("SELECT nome, SUM(pontos) FROM tarefas WHERE concluida = 1 GROUP BY nome ORDER BY SUM(pontos) DESC")
    for i, (nome, pontos) in enumerate(cursor.fetchall(), start=1):
        lista_ranking.insert(tk.END, f"{i}º {nome} - {pontos} pontos")

# Criar interface gráfica
root = tk.Tk()
root.title("EcoBairro - Gerenciador de Tarefas")
root.geometry("600x600")

# Seção para adicionar tarefa
tk.Label(root, text="Nome do colaborador:").pack()
entry_nome = tk.Entry(root)
entry_nome.pack()

tk.Label(root, text="Descrição da tarefa:").pack()
entry_descricao = tk.Entry(root)
entry_descricao.pack()

tk.Label(root, text="Pontos:").pack()
combo_pontos = tk.StringVar(value="50")
tk.OptionMenu(root, combo_pontos, "50", "30", "20").pack()

# Botões de ações
tk.Button(root, text="Adicionar Tarefa", command=adicionar_tarefa).pack(pady=5)
tk.Button(root, text="Concluir Tarefa", command=concluir_tarefa).pack(pady=5)
tk.Button(root, text="Excluir Tarefa", command=excluir_tarefa).pack(pady=5)

# Seção para visualizar tarefas
tk.Label(root, text="Tarefas:").pack()
lista_tarefas = tk.Listbox(root, width=80, height=10)
lista_tarefas.pack()

# Botões de filtro
tk.Button(root, text="Mostrar Pendentes", command=filtrar_pendentes).pack(side=tk.LEFT, padx=5)
tk.Button(root, text="Mostrar Concluídas", command=filtrar_concluidas).pack(side=tk.LEFT, padx=5)
tk.Button(root, text="Mostrar Todas", command=atualizar_lista).pack(side=tk.LEFT, padx=5)

# Seção de ranking
tk.Label(root, text="Ranking dos Colaboradores").pack(pady=10)
lista_ranking = tk.Listbox(root, width=50, height=10)
lista_ranking.pack()

atualizar_lista()
atualizar_ranking()

# Iniciar a aplicação
root.mainloop()

# Fechar conexão com o banco ao sair
conn.close()
