
# 💸 **CasaSplit: Cálculo e Divisão de Contas**

Bem-vindo ao **CasaSplit**, um projeto em Python que permite calcular e dividir as contas de uma casa entre seus integrantes. O sistema utiliza uma interface gráfica simples e intuitiva, construída com **tkinter**, para facilitar o processo de cadastro e cálculo e usamos o **streamlit**, para visualizar e divulgar os gastos entre os integrantes no templathe (site).

Com este projeto, você poderá:
- Cadastrar os integrantes da sua casa.
- Registrar as contas mensais (como luz, água, internet, etc.).
- Calcular automaticamente o valor que cada integrante deve pagar.

---

## Versão Atual

O projeto está na versão v1.0.0. Você pode acessar a release completa [aqui](https://github.com/marioleo7k/casasplit/releases/tag/v1.0.0).

### Novidades na v1.0.0:
- Sistema de cadastro de integrantes.
- Sistema de cadastro de contas mensais.
- Dashboard online com cálculo automático da divisão de contas.

---

## 📜 **Propósito do Projeto**

O objetivo deste projeto é demonstrar habilidades em:
- **Desenvolvimento de Interfaces Gráficas**: Criando uma interface simples e eficiente para interação com o usuário.
- **Manipulação de Dados**: Usando o Pandas para organizar e calcular as divisões de contas.
- **Automatização de Processos**: Facilitar a divisão de contas de forma justa entre os integrantes da casa.

Além disso, é uma oportunidade para aprender e explorar bibliotecas poderosas como:
- `tkinter`: Para interfaces.
- `Pandas`: Para manipulação e análise de dados.
- `Streamlit`: Para criação de dashboards.

---

## 🚀 **Como Executar o Projeto**

### 1. Clone este repositório:
```bash
git clone https://github.com/marioleo7k/casasplit
cd casasplit
```

### 2. Instale as dependências:
Certifique-se de que você tem o Python instalado e execute o comando:
```bash
pip install -r requirements.txt
```

### 3. Cadastre os integrantes:
Execute o executável `integrantes.exe` para abrir a interface e cadastrar os integrantes da casa ou utilize sua IDE para executar o script
```bash
python integrantes.py
```

### 4. Cadastre as contas:
Execute o executável `contas.exe` para abrir a interface e cadastrar os integrantes da casa ou utilize sua IDE para executar o script
```bash
python contas.py
```

### 5. Calcule a divisão:
Após cadastrar todos os integrantes e contas, o sistema calculará automaticamente quanto cada integrante deve pagar.

### 6. Divulgue a dashboard:
Execute a dashboard interativa:
```bash
streamlit run dashboard/dashboard.py
```

Acesse a URL local exibida no terminal, como `http://localhost:8501`.

---

## 🛠️ **Principais Funcionalidades**

### **1. Cadastro de Integrantes:**
- O script `integrantes.py` permite adicionar os nomes de todos os integrantes da casa.
- O número de integrantes será utilizado para dividir as contas igualmente.
- O script criará ou atualizará o `integrantes.csv` como database dos integrantes da casa

### **2. Cadastro de Contas:**
- O script `contas.py` permite adicionar as contas mensais (como luz, água, internet, etc.) e o valor correspondente.
- O sistema calcula automaticamente o total das contas e divide o valor entre os integrantes.
- O script criará ou atualizará o `contas.csv` como database das contas da casa

### **3. Cálculo Automático:**
- O sistema calcula o valor que cada integrante deve pagar após o cadastro das contas atráves do botão da interface do `contas.py`

### **4. Dashboard Dinâmica:**
- O script cria uma dashboard interativa e dinâmica na web para visualizarmos as contas da casa no script `dashboard.py`

---

## 🖼️ **Exemplos de Visualizações**

### :
<img src="" width="400" height="200" />

### :
<img src="" width="400" height="200" />

---

## 📂 **Estrutura do Repositório**
```
casasplit/
├── integrantes/              # Pasta com scripts e executáveis para cadastro de integrantes
│   ├── integrantes.py        # Script para cadastrar os integrantes da casa
│   └── integrantes.exe       # Executável para cadastro de integrantes
├── contas/                   # Pasta com scripts e executáveis para cadastro de contas
│   ├── contas.py             # Script para cadastrar as contas e calcular a divisão
│   └── contas.exe            # Executável para cadastro de contas e cálculo
├── dashboard/                # Pasta com script do streamlit 
│   └── dashboard.py          # Script para criar dashboard no streamlit
├── .streamlit                # Dependências do streamlit
│   └── config.toml           # Configuração de temas
├── .images                   # Imagens dos executáveis
│   ├── .png                  # 
│   ├── .png                  # 
│   ├── .ico                  # 
│   └── .ico                  #  
├── requirements.txt          # Dependências do projeto
├── .gitignore                # Arquivos ignorados pelo Git
└── README.md                 # Documentação do projeto

```

---

## 🌟 **Contribuição**
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests para melhorias no projeto.

---

## ⚖️ **Licença**
Este projeto é distribuído sob a licença MIT. Consulte o arquivo [LICENSE](./LICENSE) para mais informações.

![MIT License](https://img.shields.io/badge/license-MIT-blue)

---

## 💬 **Contato**
Para dúvidas ou feedback, você pode me encontrar no LinkedIn:
[Mario Leonardo da Silva](https://www.linkedin.com/in/marioleo7k/).

---

## 🌐 **Dashboard Publicada**
Você também pode acessar a versão publicada da dashboard [aqui](https://bookscraper-dashboard.streamlit.app/).