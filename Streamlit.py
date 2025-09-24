import streamlit as st
import Conector as con

# Initialize session state for login status and current section
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_section' not in st.session_state:
    st.session_state.current_section = "Introdução"

# This is the login page. It will be shown if the user is not logged in.
def login_page():
    st.set_page_config(
        page_title="Projeto KC",
        page_icon="📊",
        layout="centered"
    )

    # Background
    page_bg = """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #010136;
    }

    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }

    div[data-testid="stMarkdownContainer"] h1 {
        color: #fafafa !important;
        font-size: 52px !important;
        font-weight: bold !important;
        text-align: center !important;
    }

    div[data-testid="stTextInput"] label {
        color: #fafafa !important;
        font-weight: bold;
    }

    .stButton button {
        color: #010136 !important;
        border-radius: 8px !important;
        border: 1px solid #fafafa !important;
        font-weight: bold !important;
        padding: 8px 16px !important;
        background-color: #fafafa !important;
    }

    .stButton button:hover{
        background-color: rgba(75, 123, 236, 0.3) !important;
        color: #fafafa !important;
    }
    </style>
    """

    st.markdown(page_bg, unsafe_allow_html=True)

    st.title("Kautz-Collioni & Cia.", anchor=False)
    st.markdown("---")
    
    username = st.text_input("Usuário", key="user")
    password = st.text_input("Senha", type="password")
    
    if st.button("Enviar"):
        if username == "teste" and password == "teste123":
            st.session_state.logged_in = True
            st.success("Bem-vindo!")
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")

def voltar_login():
    st.session_state.logged_in = False

# Main app function
def main_app():
    st.set_page_config(
        page_title="Projeto KC",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://docs.streamlit.io/',
            'Report a bug': "https://github.com/streamlit/streamlit/issues",
            'About': ""
        }
    )

    # Botão de logout
    st.markdown(
        """
        <style>
            .sair-btn button {
                background-color: #f0f2f6 !important;
                color: black !important;
                border: 1px solid #d3d3d3 !important;
                border-radius: 5px !important;
                padding: 0.5rem 1rem !important;
                font-weight: normal !important;
            }
            .sair-btn {
                position: absolute;
                top: 10px;
                right: 20px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sair-btn">
            <button onclick="window.location.href='?logout'">Sair</button>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # CSS CORRIGIDO baseado no XPATH fornecido
    st.markdown("""
    <style>
    /* ESCONDE COMPLETAMENTE OS RADIO BUTTONS (círculos) */
    section[data-testid="stSidebar"] div[data-baseweb="radio"] div:first-child {
        display: none !important;
    }
    
    /* Escode os círculos dos radio buttons */
    section[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
        opacity: 0 !important;
        visibility: hidden !important;
    }
    
    /* Remove o espaço dos círculos ocultos */
    section[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] {
        gap: 0 !important;
        margin-right: 0 !important;
    }
    
    /* Ajusta o padding dos labels para compensar a remoção dos círculos */
    section[data-testid="stSidebar"] .stRadio label {
        padding: 0.75rem 1rem 0.75rem 1rem !important;
        margin: 0 !important;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        border-left: 4px solid transparent;
        background-color: transparent;
        width: 100% !important;
    }

    /* Container principal dos itens */
    section[data-testid="stSidebar"] .stRadio [role="radiogroup"] {
        display: flex;
        flex-direction: column;
        gap: 2px;
        width: 100%;
    }

    /* Efeito hover para todos os itens */
    section[data-testid="stSidebar"] .stRadio label:hover {
        background-color: rgba(75, 123, 236, 0.1) !important;
        border-left: 4px solid rgba(75, 123, 236, 0.5) !important;
    }

    /* Item selecionado - ESTILO PRINCIPAL */
    section[data-testid="stSidebar"] .stRadio [aria-checked="true"] label {
        background-color: rgba(75, 123, 236, 0.2) !important;
        border-left: 4px solid #4b7bec !important;
    }

    /* TEXTO EM NEGRITO BASEADO NO XPATH FORNECIDO */
    /* Estrutura: /html/body/div[1]/div[1]/div[1]/div/div[2]/section/div[1]/div[2]/div/div/div[2]/div/div/label[3]/div[2]/div/p */
    
    /* Para o item selecionado - texto em NEGRITO */
    section[data-testid="stSidebar"] .stRadio [aria-checked="true"] label div[data-testid="stMarkdownContainer"] p {
        font-weight: 700 !important;
        color: #4b7bec !important;
    }

    /* Para itens não selecionados - texto normal */
    section[data-testid="stSidebar"] .stRadio [aria-checked="false"] label div[data-testid="stMarkdownContainer"] p {
        font-weight: 400 !important;
        color: #31333F !important;
    }

    /* Alternativa mais específica baseada no XPATH */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"] div[data-testid="stMarkdownContainer"] p {
        transition: all 0.3s ease;
    }

    /* Item selecionado - versão alternativa */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"][aria-checked="true"] div[data-testid="stMarkdownContainer"] p {
        font-weight: 700 !important;
        color: #4b7bec !important;
    }

    /* Item não selecionado - versão alternativa */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"][aria-checked="false"] div[data-testid="stMarkdownContainer"] p {
        font-weight: 400 !important;
        color: #31333F !important;
    }

    /* Remove o focus outline */
    section[data-testid="stSidebar"] .stRadio label:focus {
        outline: none;
    }
    
    /* Garante que o texto ocupe todo o espaço */
    section[data-testid="stSidebar"] .stRadio label div[data-testid="stMarkdownContainer"] {
        width: 100% !important;
    }

    /* Estilo adicional para garantir o negrito */
    section[data-testid="stSidebar"] [aria-checked="true"] [data-testid="stMarkdownContainer"] {
        font-weight: 700 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Título da aplicação
    st.markdown(
        """
        <h1 style='text-align: center;'>
            Kautz-Collioni & Cia.
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Sidebar de navegação
    with st.sidebar:
        st.markdown("### Navegação")
        
        # Definir as opções da sidebar
        opcoes_sidebar = [
            "Introdução", 
            "Análise Exploratória", 
            "Elasticidades", 
            "Forecasting",
            "Operacional", 
            "Decomposição", 
            "Entregáveis"
        ]
        
        # Encontrar o índice atual
        try:
            current_index = opcoes_sidebar.index(st.session_state.current_section)
        except ValueError:
            current_index = 0
        
        # Radio button para navegação
        section = st.radio(
            "Selecione a seção:",
            opcoes_sidebar,
            index=current_index,
            key="nav_radio",
            label_visibility="collapsed"
        )
        
        # Atualizar a session state
        if section != st.session_state.current_section:
            st.session_state.current_section = section
            st.rerun()

    database = con.database

    # Resto do código das abas (mantido igual)
    # Aba 1 - Introdução
    if st.session_state.current_section == "Introdução":
        st.header("Amostra dos Dados")
        st.markdown("Qual é a fundamentação do estudo?")
        st.dataframe(database.sample(25))

    # Aba 2 - Análise Exploratória
    elif st.session_state.current_section == "Análise Exploratória":
        st.header("Análise Exploratória")
        st.subheader("Relação entre Quantidade Vendida e Preço por Item de Café (Demandas inversas)")
        st.plotly_chart(con.figure1, use_container_width=True)
        st.subheader("Distribuições de Preços")
        st.plotly_chart(con.figure2, use_container_width=True)
        st.subheader("Análise Exploratória — Receitas Acumuladas")
        st.plotly_chart(con.figure4, use_container_width=True)
        st.subheader("Análise Exploratória — Receitas Diárias")
        st.plotly_chart(con.figure5, use_container_width=True)
        st.subheader("Análise Exploratória — Receita por Dia da Semana")
        st.plotly_chart(con.figure6, use_container_width=True)
        st.subheader("Análise Exploratória — Participação na Receita (Semanal)")
        st.plotly_chart(con.figure7, use_container_width=True)

    # Aba 3 - Elasticidades
    elif st.session_state.current_section == "Elasticidades":
        st.header("Elasticidades")
        st.subheader("Elasticidades-preço da Demanda Atuais")
        st.plotly_chart(con.figure3, use_container_width=True)
        st.subheader("Elasticidades-preço nos Pontos Ótimos")
        st.plotly_chart(con.figure9, use_container_width=True)

    # Aba 4 - Forecasting     
    elif st.session_state.current_section == "Forecasting":
        st.header("Forecasting e Relacionados")
        st.subheader("Otimização de Preços Usando Modelos Aditivos Generalizados (GAM)")
        st.plotly_chart(con.figure8, use_container_width=True)

    # Aba 5 - Operacional     
    elif st.session_state.current_section == "Operacional":
        st.header("Painel Operacional")
        st.subheader("Indicadores e controle")
        st.markdown("---")
        st.subheader("Fluxo de caixa")
        
        import numpy as np
        import pandas as pd
        
        df = pd.DataFrame({
            "A": np.random.randn(10),
            "B": np.random.randn(10)
        })

        st.text("Esse é o fluxo dos últimos x períodos.")
        st.bar_chart(df)

        st.markdown("---")
        st.subheader("Liquidez")
        st.text("Aqui mostra a capacidade de liquidar as suas dívidas(passivos).")
        st.line_chart(df)

        st.markdown("---")
        st.subheader("Fluxo de Caixa Projetado")
        st.text("Projeção do resultado da empresa pelos próximos x períodos")
        tb = pd.DataFrame({
            "2025P": np.random.randn(3),
            "2026P": np.random.randn(3),
            "2027P": np.random.randn(3),
            "2028P": np.random.randn(3),
            "2029P": np.random.randn(3),
        }, index=['Receita Operacional Bruta', 'CMV', 'Lucro Bruto'])
        st.table(tb)
        st.markdown("---")
        st.subheader("Valuation - FCD dos últimos x períodos")

        df2 = pd.DataFrame({
            "Receita": [np.abs(np.random.randn()*1), np.abs(np.random.randn()*2), np.abs(np.random.randn()*3), np.abs(np.random.randn()*4)],
        }, index=[2025, 2026, 2027, 2028])
        st.bar_chart(df2)

    # Aba 6 - Decomposição
    elif st.session_state.current_section == "Decomposição":
        st.header("Decomposição de Séries")
        st.subheader("Decomposição: Tendência, Sazonalidade e Resíduo")
        st.plotly_chart(con.figure10, use_container_width=True)

    # Aba 7 - Entregáveis     
    elif st.session_state.current_section == "Entregáveis":
        st.header("Entregáveis")
        st.dataframe(con.comparison_table)

    st.markdown("---")

# Main application logic
if st.session_state.logged_in:
    main_app()
else:
    login_page()
