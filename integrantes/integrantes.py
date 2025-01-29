# Importação das bibliotecas necessárias
import pandas as pd  # Biblioteca pandas para manipulação de dados em formato de tabela (DataFrame)
import tkinter as tk  # Biblioteca tkinter para criar interfaces gráficas
from tkinter import messagebox  # Para exibir caixas de mensagem

# Função que será chamada para salvar os dados no formato CSV
def salvar_csv():
    arquivo_csv = "integrantes.csv"  # Nome do arquivo CSV a ser gerado
    
    # Capturar a entrada do usuário na interface gráfica
    integrantes = entrada.get()  # Obtém o texto inserido no campo de entrada de dados
    
    # Separar os nomes, remover espaços em branco extras e criar uma lista de integrantes
    integrantes = [nome.strip() for nome in integrantes.split(',')]  # Divide o texto pelo separador vírgula e limpa espaços extras
    
    # Criar um DataFrame usando o pandas, onde cada nome será uma linha na coluna 'Integrantes'
    df = pd.DataFrame({'Integrantes': integrantes})
    
    # Salvar o DataFrame no arquivo CSV, sem incluir o índice na primeira coluna
    df.to_csv(arquivo_csv, index=False)
    
    # Exibir uma mensagem de sucesso ao usuário
    messagebox.showinfo("Sucesso", f"Arquivo '{arquivo_csv}' criado com sucesso!")

# Função para criar a interface gráfica
def criar_interface():
    global entrada  # Declarando a variável de entrada como global para ser acessada em outras funções
    
    root = tk.Tk()  # Criação da janela principal da interface gráfica
    root.title("Cadastro de Integrantes da Casa")  # Definindo o título da janela
    root.geometry("600x250")  # Definindo o tamanho da janela (largura x altura)
    root.configure(bg="#f5f5f5")  # Definindo a cor de fundo da janela
    
    # Criar um frame dentro da janela principal para organizar os widgets (botões, labels, etc)
    frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, relief=tk.GROOVE, bd=2)
    frame.pack(pady=30, padx=30, fill=tk.BOTH, expand=True)  # Adiciona o frame à janela principal e configura seu posicionamento
    
    # Adicionar uma Label (texto) no frame para dar instruções ao usuário
    tk.Label(frame, text="Digite os nomes dos integrantes (separados por vírgula):", bg="#ffffff", font=("Helvetica", 14)).pack(pady=(0, 10))
    
    # Criar o campo de entrada (caixa de texto) para o usuário digitar os nomes
    entrada = tk.Entry(frame, width=50, font=("Helvetica", 12), bg="#e8e8e8", relief=tk.FLAT)  # Definindo a aparência da caixa de texto
    entrada.pack(pady=(0, 20))  # Adiciona a caixa de entrada ao frame com um espaçamento vertical
    
    # Criar o botão que, quando clicado, chama a função salvar_csv para salvar os dados no arquivo CSV
    botao = tk.Button(frame, text="Salvar", command=salvar_csv, bg="#007BFF", fg="white", font=("Helvetica", 12, "bold"), padx=20, pady=10, relief=tk.FLAT)
    botao.pack(pady=10)  # Adiciona o botão ao frame com espaçamento vertical
    
    root.mainloop()  # Inicia o loop principal da interface gráfica, fazendo a janela ficar ativa

# Checar se o script está sendo executado diretamente
if __name__ == "__main__":  # Verifica se o script está sendo executado como o programa principal
    criar_interface()  # Chama a função que cria a interface gráfica