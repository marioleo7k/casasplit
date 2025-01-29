# Importação das bibliotecas necessárias
import streamlit as st  # Biblioteca para criar aplicativos web interativos
import pandas as pd  # Biblioteca para manipulação de dados em formato de tabela (DataFrame)
import matplotlib.pyplot as plt  # Biblioteca para criação de gráficos
import seaborn as sns  # Biblioteca para visualização de dados baseada no Matplotlib
import locale  # Biblioteca para configuração de localidade (idioma, formato de números, datas, etc.)

# Configurar o locale para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Função para carregar os dados corretamente
def carregar_dados():
    try:
        df = pd.read_csv('contas.csv')  # Carrega os dados do arquivo CSV
        df['Data'] = pd.to_datetime(df['Data']).dt.strftime('%Y-%m')  # Converte a coluna 'Data' para o formato ano-mês
        df['Valor'] = df['Valor'].astype(str).str.replace(',', '.').astype(float)  # Converte a coluna 'Valor' para float
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=['Data', 'Conta', 'Valor'])  # Retorna um DataFrame vazio se o arquivo não for encontrado

# Função para carregar os integrantes
def carregar_integrantes():
    try:
        df_integrantes = pd.read_csv('integrantes.csv')  # Carrega os dados do arquivo CSV
        return df_integrantes['Integrantes'].tolist()  # Retorna a lista de integrantes
    except FileNotFoundError:
        return []  # Retorna uma lista vazia se o arquivo não for encontrado

# Função para formatar valores em BRL sem erro
def formatar_valor(valor):
    return locale.currency(valor, grouping=True)  # Formata o valor para o formato de moeda brasileira

# Carregar dados
df = carregar_dados()
integrantes = carregar_integrantes()

# Criar interface Streamlit
st.set_page_config(page_title="Dashboard de Gastos", page_icon="💰", layout="wide")  # Configura a página do Streamlit
st.title('💰 Dashboard de Gastos')  # Define o título da página

# Sidebar para seleção do mês e ano
st.sidebar.header("📅 Filtros")  # Adiciona um cabeçalho na barra lateral
if not df.empty:
    meses_disponiveis = df['Data'].unique()  # Obtém os meses disponíveis nos dados
    mes_selecionado = st.sidebar.selectbox("Selecione o mês e ano:", meses_disponiveis, index=len(meses_disponiveis)-1)  # Cria uma caixa de seleção para os meses
else:
    mes_selecionado = None

# Calcular e mostrar valor por integrante
st.subheader('👥 Valor por Integrante')  # Subcabeçalho na página principal
if mes_selecionado and not df.empty:
    df_filtrado = df[df['Data'] == mes_selecionado]  # Filtra os dados pelo mês selecionado
    
    if not df_filtrado.empty and integrantes:
        total_gastos = df_filtrado['Valor'].sum()  # Calcula o total de gastos no mês selecionado
        valor_por_integrante = total_gastos / len(integrantes)  # Calcula o valor por integrante
        valor_formatado = formatar_valor(valor_por_integrante)  # Formata o valor para moeda brasileira

        st.markdown(
            f"""
            <div style="padding: 20px; border-radius: 12px; background-color: #10B981; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <h2>💵 Cada integrante deve pagar: {valor_formatado}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )  # Exibe o valor por integrante em um box estilizado

        st.write(f'📌 Integrantes: {", ".join(integrantes)}')  # Exibe a lista de integrantes
    else:
        st.write("❌ Não há dados suficientes para calcular o valor por integrante.")  # Mensagem de erro
else:
    st.write("🔍 Selecione um mês e ano para visualizar os valores.")  # Mensagem de instrução

# Mostrar tabela de gastos
st.subheader('📜 Tabela de Gastos')  # Subcabeçalho na página principal
if mes_selecionado and not df.empty:
    df_exibir = df_filtrado.copy()
    df_exibir['Valor'] = df_exibir['Valor'].apply(formatar_valor)  # Formata os valores para exibição
    st.dataframe(df_exibir, hide_index=True)  # Exibe a tabela de gastos
else:
    st.write("Nenhuma conta cadastrada ou selecione um mês e ano.")  # Mensagem de erro

# Indicadores de Performance
st.subheader('📊 Indicadores de Performance')  # Subcabeçalho na página principal
if not df.empty:
    total_gastos = df['Valor'].sum()  # Calcula o total de gastos
    media_gastos = df['Valor'].mean()  # Calcula a média de gastos
    max_gasto = df['Valor'].max()  # Calcula o maior gasto
    min_gasto = df['Valor'].min()  # Calcula o menor gasto

    col1, col2, col3, col4 = st.columns(4)  # Cria quatro colunas para os indicadores
    col1.metric("💵 Total de Gastos", formatar_valor(total_gastos))  # Exibe o total de gastos
    col2.metric("📊 Média de Gastos", formatar_valor(media_gastos))  # Exibe a média de gastos
    col3.metric("📈 Maior Gasto", formatar_valor(max_gasto))  # Exibe o maior gasto
    col4.metric("📉 Menor Gasto", formatar_valor(min_gasto))  # Exibe o menor gasto
else:
    st.write("Nenhum dado disponível para os indicadores.")  # Mensagem de erro

# Gráfico de tendência
st.subheader('📈 Tendência de Gastos')  # Subcabeçalho na página principal
if not df.empty:
    df_tendencia = df.groupby('Data')['Valor'].sum().reset_index()  # Agrupa os dados por data e soma os valores

    fig, ax = plt.subplots(figsize=(8, 5))  # Cria um gráfico
    ax.plot(df_tendencia['Data'], df_tendencia['Valor'], marker='o', linestyle='-', color='#1E3A8A', linewidth=2)  # Plota a linha de tendência
    ax.set_title('Tendência de Gastos ao Longo do Tempo', fontsize=16, weight='bold', color='#4B5563')
    ax.set_xlabel('Data (Ano-Mês)', fontsize=12, color='#6B7280')
    ax.set_ylabel('Gastos em BRL', fontsize=12, color='#6B7280')
    ax.grid(True, axis='y', linestyle='--', alpha=0.7, color='#D1D5DB')
    plt.xticks(rotation=45)

    # Adicionar rótulos aos pontos
    for i, row in df_tendencia.iterrows():
        ax.text(row['Data'], row['Valor'], formatar_valor(row['Valor']), ha='center', va='bottom', fontsize=10, color='#1F2937')

    # Estilo
    plt.tight_layout()

    st.pyplot(fig)  # Exibe o gráfico
else:
    st.write("Nenhum dado disponível para o gráfico.")  # Mensagem de erro

# Gráfico de Barras para Gastos por Categoria
st.subheader('📊 Gastos por Categoria')  # Subcabeçalho na página principal
if not df.empty:
    df_categoria = df.groupby('Conta')['Valor'].sum().reset_index()  # Agrupa os dados por categoria e soma os valores

    fig, ax = plt.subplots(figsize=(8, 5))  # Cria um gráfico de barras
    sns.barplot(x='Valor', y='Conta', data=df_categoria, palette='viridis', ax=ax)  # Plota as barras
    ax.set_title('Gastos por Categoria', fontsize=16, weight='bold', color='#4B5563')
    ax.set_xlabel('Gastos em BRL', fontsize=12, color='#6B7280')
    ax.set_ylabel('Categoria', fontsize=12, color='#6B7280')
    ax.grid(True, axis='x', linestyle='--', alpha=0.7, color='#D1D5DB')

    st.pyplot(fig)  # Exibe o gráfico
else:
    st.write("Nenhum dado disponível para o gráfico.")  # Mensagem de erro

# Gráfico de Pizza para Distribuição de Gastos
st.subheader('🍰 Distribuição de Gastos')  # Subcabeçalho na página principal
if not df.empty:
    df_pizza = df.groupby('Conta')['Valor'].sum().reset_index()  # Agrupa os dados por categoria e soma os valores

    fig, ax = plt.subplots(figsize=(8, 5))  # Cria um gráfico de pizza
    ax.pie(df_pizza['Valor'], labels=df_pizza['Conta'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('viridis', len(df_pizza)))  # Plota a pizza
    ax.set_title('Distribuição de Gastos por Categoria', fontsize=16, weight='bold', color='#4B5563')

    st.pyplot(fig)  # Exibe o gráfico
else:
    st.write("Nenhum dado disponível para o gráfico.")  # Mensagem de erro