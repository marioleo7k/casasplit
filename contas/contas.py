import pandas as pd  # Biblioteca pandas para manipulação de dados em formato de tabela
import tkinter as tk  # Biblioteca tkinter para criar interfaces gráficas
from tkinter import messagebox  # Para exibir caixas de mensagem
from tkinter import ttk  # Para widgets estilizados

import locale  # Biblioteca para configuração de localidade (idioma, formato de números, datas, etc.)

# Configurar o locale para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Variável global para armazenar a ordem de classificação das colunas
ordem_colunas = {"Data": True, "Conta": True, "Valor": True}

# Função para carregar os integrantes do arquivo CSV
def carregar_integrantes():
    try:
        df = pd.read_csv('integrantes.csv')  # Carrega os dados do arquivo CSV
        return list(df['Integrantes'])  # Retorna os nomes dos integrantes como uma lista
    except FileNotFoundError:
        return ["Nenhum integrante cadastrado"]  # Retorna uma mensagem se o arquivo não for encontrado

# Função para exibir os integrantes na interface
def exibir_integrantes():
    integrantes = carregar_integrantes()  # Carrega a lista de integrantes
    integrantes_texto = " | ".join(integrantes)  # Junta os nomes dos integrantes com " | " como separador
    label_integrantes.config(text=f"Integrantes: {integrantes_texto}")  # Atualiza o texto do label com os integrantes

# Função para salvar as contas no arquivo CSV
def salvar_contas():
    try:
        mes_ano = f"{mes_combobox.get()}-{ano_combobox.get()}"  # Obtém o mês e ano selecionados
        conta = conta_combobox.get()  # Obtém o tipo de conta selecionado
        valor = entrada_valor.get()  # Obtém o valor inserido

        if not conta or not valor:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")  # Exibe um erro se algum campo estiver vazio
            return

        data = pd.to_datetime(mes_ano, format='%m-%Y').strftime('%Y-%m')  # Converte a data para o formato ano-mês
        nova_linha = pd.DataFrame({'Data': [data], 'Conta': [conta], 'Valor': [float(valor)]})  # Cria um DataFrame com a nova linha

        try:
            df = pd.read_csv('contas.csv')  # Tenta ler o arquivo CSV existente
            df = pd.concat([df, nova_linha], ignore_index=True)  # Adiciona a nova linha ao DataFrame existente
        except FileNotFoundError:
            df = nova_linha  # Se o arquivo não existir, usa apenas a nova linha

        df.to_csv('contas.csv', index=False)  # Salva o DataFrame atualizado no arquivo CSV

        atualizar_tabela()  # Atualiza a tabela na interface
        conta_combobox.set('')  # Limpa a seleção da combobox de conta
        entrada_valor.delete(0, tk.END)  # Limpa o campo de entrada de valor

        messagebox.showinfo("Sucesso", "Conta salva com sucesso!")  # Exibe uma mensagem de sucesso
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar dados: {str(e)}")  # Exibe uma mensagem de erro se algo der errado

# Função para calcular o preço por integrante
def calcular_preco_por_integrante():
    try:
        df_contas = pd.read_csv('contas.csv')  # Carrega os dados das contas do arquivo CSV
        integrantes = carregar_integrantes()  # Carrega a lista de integrantes

        if not integrantes:
            messagebox.showerror("Erro", "Nenhum integrante cadastrado.")  # Exibe um erro se não houver integrantes cadastrados
            return

        mes_ano = f"{mes_combobox.get()}-{ano_combobox.get()}"  # Obtém o mês e ano selecionados
        df_contas['Data'] = pd.to_datetime(df_contas['Data'], format='%Y-%m')  # Converte a coluna Data para o formato datetime
        df_filtrada = df_contas[df_contas['Data'].dt.strftime('%m-%Y') == mes_ano]  # Filtra as contas pelo mês e ano selecionados

        if df_filtrada.empty:
            messagebox.showerror("Erro", "Nenhuma conta encontrada para o mês e ano selecionados.")  # Exibe um erro se não houver contas para o período selecionado
            return

        total_contas = df_filtrada['Valor'].sum()  # Calcula o total das contas
        preco_por_integrante = total_contas / len(integrantes)  # Calcula o preço por integrante
        preco_formatado = locale.currency(preco_por_integrante, grouping=True)  # Formata o preço para o formato de moeda brasileira

        messagebox.showinfo("Resultado", f"O preço por integrante para o mês {mes_ano} é: {preco_formatado}")  # Exibe o resultado
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao calcular o preço: {str(e)}")  # Exibe uma mensagem de erro se algo der errado

# Função para atualizar a tabela na interface
def atualizar_tabela(coluna_ordenar=None):
    try:
        df = pd.read_csv('contas.csv')  # Carrega os dados das contas do arquivo CSV

        # Ordena os dados caso uma coluna tenha sido clicada
        if coluna_ordenar:
            ordem_colunas[coluna_ordenar] = not ordem_colunas[coluna_ordenar]  # Alterna a ordem de classificação
            df['Valor'] = df['Valor'].replace(r'[R$\s,]', '', regex=True).astype(float)  # Remove símbolos antes de ordenar
            df = df.sort_values(by=coluna_ordenar, ascending=ordem_colunas[coluna_ordenar])  # Ordena o DataFrame

        for i in tabela.get_children():
            tabela.delete(i)  # Remove todas as linhas da tabela

        for _, row in df.iterrows():
            valor_formatado = locale.currency(row['Valor'], grouping=True)  # Formata o valor para o formato de moeda brasileira
            tabela.insert("", "end", values=(row['Data'], row['Conta'], valor_formatado))  # Insere os dados na tabela
    except FileNotFoundError:
        pass  # Não faz nada se o arquivo não for encontrado

# Função para excluir a linha selecionada
def excluir_linha():
    selected_item = tabela.selection()  # Obtém a linha selecionada
    if not selected_item:
        messagebox.showerror("Erro", "Selecione uma linha para excluir.")  # Exibe um erro se nenhuma linha estiver selecionada
        return

    resposta = messagebox.askyesno("Confirmar Exclusão", "Você tem certeza que deseja excluir esta linha?")  # Confirma a exclusão
    if resposta:
        item = selected_item[0]
        valores = tabela.item(item, "values")  # Obtém os valores da linha selecionada

        tabela.delete(item)  # Remove a linha da tabela

        try:
            df = pd.read_csv('contas.csv')  # Carrega os dados das contas do arquivo CSV
            df['Valor'] = df['Valor'].replace(r'[R$\s,]', '', regex=True).astype(float)  # Remove símbolos antes de converter

            # Remove a linha correspondente do DataFrame
            df = df[~((df['Data'] == valores[0]) & (df['Conta'] == valores[1]) & (df['Valor'] == float(valores[2].replace('R$', '').replace('.', '').replace(',', '.'))))]

            df.to_csv('contas.csv', index=False)  # Salva o DataFrame atualizado no arquivo CSV
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir: {str(e)}")  # Exibe uma mensagem de erro se algo der errado

# Criar interface gráfica
def criar_interface():
    global mes_combobox, ano_combobox, conta_combobox, entrada_valor, tabela, label_integrantes

    root = tk.Tk()  # Cria a janela principal
    root.title("Cadastro de Contas")  # Define o título da janela
    root.geometry("800x600")  # Define o tamanho inicial da janela
    root.configure(bg="#f7f7f7")  # Define a cor de fundo da janela

    # Usar o gerenciador de layout grid para tornar a interface responsiva
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    frame_entrada = tk.Frame(root, bg="#ffffff", padx=20, pady=20, relief=tk.RIDGE, bd=2)  # Cria um frame para os campos de entrada
    frame_entrada.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

    # Configuração das colunas e linhas para tornar responsivo
    for i in range(3):
        frame_entrada.grid_columnconfigure(i, weight=1)

    # Cria e posiciona os widgets no frame de entrada
    tk.Label(frame_entrada, text="Selecione o Mês:", bg="#ffffff", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=10, sticky="e")
    mes_combobox = ttk.Combobox(frame_entrada, values=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"], state="readonly", width=10)
    mes_combobox.set("01")
    mes_combobox.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

    tk.Label(frame_entrada, text="Selecione o Ano:", bg="#ffffff", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=10, sticky="e")
    ano_combobox = ttk.Combobox(frame_entrada, values=["2025", "2024"], state="readonly", width=10)
    ano_combobox.set("2025")
    ano_combobox.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

    tk.Label(frame_entrada, text="Conta:", bg="#ffffff", font=("Helvetica", 12)).grid(row=2, column=0, padx=5, pady=10, sticky="e")
    conta_combobox = ttk.Combobox(frame_entrada, values=[
        "Energia", "Água", "Internet", "Telefone Fixo", "Celular", "TV a Cabo", "IPTU",
        "Aluguel", "Condomínio", "Seguro Residencial", "Gás", "Comida", "Supermercado",
        "Feira", "Farmácia", "Plano de Saúde", "Academia", "Transporte", "Manutenção do Carro",
        "Combustível", "Netflix", "Spotify", "Amazon Prime", "Disney+", "HBO Max",
        "Apple Music", "YouTube Premium", "PlayStation Plus", "Xbox Game Pass", "Steam",
        "Material de Escritório", "Materiais de Construção", "Móveis", "Eletrodomésticos",
        "Produtos de Limpeza", "Produtos de Higiene", "Pet Shop", "Veterinário",
        "Assinatura de Jornal/Revista", "Serviços de Streaming", "Taxa de Lixo",
        "IPVA", "Seguro do Carro", "Taxa Bancária", "Fatura do Cartão de Crédito",
        "Empréstimos", "Financiamento Imobiliário", "Financiamento de Veículo"
    ], 
    state="readonly", width=30)
    conta_combobox.grid(row=2, column=1, padx=5, pady=10, sticky="ew")

    tk.Label(frame_entrada, text="Valor:", bg="#ffffff", font=("Helvetica", 12)).grid(row=3, column=0, padx=5, pady=10, sticky="e")
    entrada_valor = tk.Entry(frame_entrada, width=20, font=("Helvetica", 12))
    entrada_valor.grid(row=3, column=1, padx=5, pady=10, sticky="ew")

    # Cria e posiciona os botões no frame de entrada
    botao_salvar = tk.Button(frame_entrada, text="Salvar Conta", command=salvar_contas, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), width=20)
    botao_salvar.grid(row=4, column=0, pady=10, padx=5, sticky="ew")

    botao_deletar = tk.Button(frame_entrada, text="Deletar", command=excluir_linha, bg="#FF5733", fg="white", font=("Helvetica", 12, "bold"), width=20)
    botao_deletar.grid(row=4, column=1, pady=10, padx=5, sticky="ew")

    botao_calcular = tk.Button(frame_entrada, text="Conta por integrante", command=calcular_preco_por_integrante, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"), width=20)
    botao_calcular.grid(row=4, column=2, pady=10, padx=5, sticky="ew")

    frame_integrantes = tk.Frame(root, bg="#ffffff", pady=5, relief=tk.RIDGE, bd=2)  # Cria um frame para exibir os integrantes
    frame_integrantes.grid(row=1, column=0, padx=20, sticky="ew")
    label_integrantes = tk.Label(frame_integrantes, text="Carregando integrantes...", bg="#ffffff", font=("Helvetica", 12, "bold"))
    label_integrantes.pack(pady=5)
    exibir_integrantes()

    frame_tabela = tk.Frame(root, bg="#f7f7f7")  # Cria um frame para a tabela
    frame_tabela.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

    frame_tabela.grid_rowconfigure(0, weight=1)
    frame_tabela.grid_columnconfigure(0, weight=1)

    # Cria a tabela e define as colunas
    tabela = ttk.Treeview(frame_tabela, columns=("Data", "Conta", "Valor"), show="headings")
    tabela.heading("Data", text="Data", command=lambda: atualizar_tabela("Data"))
    tabela.heading("Conta", text="Conta", command=lambda: atualizar_tabela("Conta"))
    tabela.heading("Valor", text="Valor", command=lambda: atualizar_tabela("Valor"))

    tabela.column("Data", width=120, anchor="center")
    tabela.column("Conta", width=200, anchor="center")
    tabela.column("Valor", width=150, anchor="center")

    tabela.grid(row=0, column=0, sticky="nsew")

    atualizar_tabela()  # Atualiza a tabela com os dados

    root.mainloop()  # Inicia o loop principal da interface gráfica

# Iniciar a interface gráfica se este script for executado diretamente
if __name__ == "__main__":
    criar_interface()