import streamlit as st
import streamlit.components.v1 as components
import Conector as con
import time
import base64

# ======================== SESSION STATE INITIALIZATION ========================
# Control login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Control current section in the app
if 'current_section' not in st.session_state:
    st.session_state.current_section = "Introdução"

# ======================== STYLE CONFIGURATION ========================
def apply_common_styles():
    common_style = """
    <style>
    /* Common button styles for both login and logout */
    .stButton button {
        width: 85px !important;
        height: 30px !important;
        font-size: 16px !important;
        text-align: center !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        color: black !important;
        background-color: #f0f2f6 !important;
        border: 1px solid #d3d3d3 !important;
        border-radius: 5px !important;
        font-weight: normal !important;
        padding: 0.5rem 1rem !important;
        margin: 0 !important;
    }

    .stButton button:hover {
        background-color: #e2e4e8 !important;
        color: black !important;
    }
    
    /* Logout button specific positioning */
    .logout-btn {
        position: absolute;
        top: 5px;
        right: 5px;
    }
    
    /* Login button specific positioning */
    .login-btn-container {
        display: flex;
        justify-content: center;
        width: 100%;
        margin-top: 1rem;
    }
    </style>
    """
    st.markdown(common_style, unsafe_allow_html = True)

# ======================== LOGIN PAGE ========================
def login_page():
    # Page configuration
    st.set_page_config(
        page_title = "Área de Acesso | Kautz-Collioni & Cia.",
        layout = "centered"
    )

    # Apply common styles
    apply_common_styles()

    # Compact style
    compact_style = """
    <style>
    [data-testid="stAppViewContainer"] {
        padding: 1rem 1rem 0.5rem 1rem !important;
    }

    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0.5rem !important;
    }
    </style>
    """
    st.markdown(compact_style, unsafe_allow_html = True)

    # Minimalist Apple-like style
    page_style = """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #ffffff;
    }

    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0);
    }

    div[data-testid="stTextInput"] input {
        background-color: #f0f2f6 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 16px !important;
        font-size: 16px !important;
        color: #000000 !important;
        font-weight: normal !important;
    }

    div[data-testid="stTextInput"] label,
    div[data-testid="stTextInput"] label p {
        color: #000000 !important;
        font-size: 16px !important;
        font-weight: normal !important;
    }

    .login-title {
        text-align: center;
        font-size: 46px;
        font-weight: 700;
        color: #31333F;
        margin-bottom: 0.2rem;
    }
    </style>
    """
    st.markdown(page_style, unsafe_allow_html = True)

    # Logo as background-like element
    try:
        with open("Cabeçalho Escuro - Streamlit.png", "rb") as f:
            image_data = f.read()
            image_base64 = base64.b64encode(image_data).decode()
        
        st.markdown(
            f"""
            <div style='text-align: center; margin-bottom: 1rem;'>
                <img src='data:image/png;base64,{image_base64}' style='width: 70%; height: auto; pointer-events: none; user-select: none; -webkit-user-drag: none;' draggable='false'>
            </div>
            """,
            unsafe_allow_html = True
        )
    except:
        st.markdown('<div style="text-align: center; font-size: 24px; margin-bottom: 1rem;">Kautz-Collioni & Cia.</div>', unsafe_allow_html = True)

    # Login form: username and password inputs
    username = st.text_input("Usuário", key = "user")
    password = st.text_input("Senha", type = "password")

    # Login button using Streamlit native button with custom styling
    if st.button("Entrar", key = "login_btn", use_container_width = True):
        if username == "João Silva" and password == "123456":
            st.success("Bem-vindo!")
            time.sleep(1)
            st.session_state.logged_in = True
            st.session_state.username = username  # Store username in session state
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos!")
    
    # Footer
    st.markdown(
        """
        <div style="width:100%; text-align:center; font-size:12px; color:#999999; margin-top:0.5rem;">
        Todos os direitos reservados © 2025 | Kautz-Collioni & Cia.
        </div>
        """,
        unsafe_allow_html = True
    )

# ======================== LOGOUT FUNCTION ========================
def back_to_login():
    # Reset login status
    st.session_state.logged_in = False
    st.session_state.current_section = "Introdução"


# ======================== MAIN APP ========================
def main_app():
    # Page configuration
    st.set_page_config(
        page_title = "Relatório Integrado | Kautz-Collioni & Cia.",
        layout = "wide",
        initial_sidebar_state = "expanded",
        menu_items = {
            'Get Help': 'https://docs.streamlit.io/',
            'Report a bug': "https://github.com/streamlit/streamlit/issues",
            'About': ""
        }
    )

    # Apply common styles
    apply_common_styles()

    # Sidebar custom CSS
    st.markdown(""" 
    <style>
    .user-greeting {
        background-color: #4b7bec;
        color: white;
        padding: 1rem;
        margin: 3rem -1rem 1.5rem -1rem;
        font-weight: 600;
        text-align: center;
        border-radius: 0 0 12px 12px;
        box-shadow: 0 4px 8px rgba(75, 123, 236, 0.2);
    }

    section[data-testid="stSidebar"] .stButton button {
        width: 100% !important;
        height: 40px !important;
        font-size: 16px !important;
        margin: 0 !important;
        background-color: #f8f9fa !important;
        border: 1px solid #dee2e6 !important;
        margin-bottom: 1rem !important;
    }
    
    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: #e9ecef !important;
        border: 1px solid #ced4da !important;
    }

    section[data-testid="stSidebar"] {
        position: relative;
        overflow-y: hidden !important;
        overflow-x: hidden !important;
        padding-bottom: 0px !important;
        padding-top: 15px;
    } 
    section[data-testid="stSidebar"]::-webkit-scrollbar {
        display: none;
    }

    div[data-testid="stSidebarContent"] {
        display: flex;
        flex-direction: column;
        height: 100%; 
        padding-bottom: 0px !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="radio"] div:first-child {display: none !important;}
    section[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {display: none !important;}
    section[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] {gap: 0 !important; margin-right: 0 !important;}
    section[data-testid="stSidebar"] .stRadio label {padding: 0.75rem 1rem !important; border-radius: 8px; cursor: pointer; transition: all 0.3s ease; border-left: 4px solid transparent;}
    section[data-testid="stSidebar"] .stRadio label:hover {background-color: rgba(75, 123, 236, 0.1) !important; border-left: 4px solid #4b7bec !important;}
    section[data-testid="stSidebar"] .stRadio [aria-checked="true"] label {background-color: rgba(75, 123, 236, 0.2) !important; border-left: 4px solid #4b7bec !important;}
    section[data-testid="stSidebar"] .stRadio [aria-checked="true"] label div[data-testid="stMarkdownContainer"] p {font-weight: 700 !important; color: #4b7bec !important;}
    section[data-testid="stSidebar"] .stRadio [aria-checked="false"] label div[data-testid="stMarkdownContainer"] p {font-weight: 400 !important; color: #31333F !important;}
    
    .sidebar-footer {
        width: 100%;
        text-align: center;
        font-size: 12px;
        color: #999999;
        
        margin-top: 2.25rem; \* This is the limit to the margin-botton */
                        
        position: initial; 
        
        padding: 1rem 0 0 0; 
        
        border-top: 1px solid #e6e6e6;
    }
    </style>
    """, unsafe_allow_html = True)

    # App title
    st.markdown("""
        <style>
        .app-title {
            text-align: center;
            font-size: 46px;
            font-weight: 700;
            color: #30333e;
            margin-bottom: 1rem;
        }
        </style>
        <div class="app-title">Porsche Brasil</div>
    """, unsafe_allow_html = True)

    st.markdown("---")

    # Sidebar navigation
    with st.sidebar:

        # Sidebar logo
        try:
            with open("cabecalho_sidebar.svg", "rb") as f:
                image_data = f.read()
                image_base64 = base64.b64encode(image_data).decode()
            
            st.markdown(
                f"""
                <div class="logo-container" style='text-align: center; margin-bottom: -15rem; z-index: 1; margin-top: -1rem;'>
                    <img src='data:image/svg+xml;base64,{image_base64}' style='width: 100%; height: 60%; pointer-events: none; user-select: none; -webkit-user-drag: none;' draggable='false; margin-bottom: -15rem; top: -4rem; position: relative; padding-bottom: 0rem; z-index: 1;'>
                </div>
                """,
                unsafe_allow_html = True
            )
        except Exception as e:
            st.error(f"Erro ao carregar a imagem: {e}")
            st.markdown('<div style="text-align: left; font-size: 12px; margin-bottom: 0.1rem;">Kautz-Collioni & Cia.</div>', unsafe_allow_html = True)

    
        # User greeting band
        st.markdown(f'<div class="user-greeting">Olá, {st.session_state.username}!</div>', unsafe_allow_html = True)
        
        sidebar_options = ["Introdução", "Análise Exploratória", "Elasticidades", "Forecasting", "Gerencial", "Decomposição", "Entregáveis"]

        try:
            current_index = sidebar_options.index(st.session_state.current_section)
        except ValueError:
            current_index = 0

        section = st.radio(
            "Selecione a seção:",
            sidebar_options,
            index = current_index,
            key = "nav_radio",
            label_visibility = "collapsed"
        )

        if section != st.session_state.current_section:
            st.session_state.current_section = section
            st.rerun()
        
        # Logout button in sidebar
        if st.button("Sair", key = "logout_btn", use_container_width = True):
            back_to_login()

        st.markdown("<br>", unsafe_allow_html = True)  # Add some space

        # Sidebar footer
        st.markdown(
            """
            <div class="sidebar-footer">
            Todos os direitos reservados © 2025 | Kautz-Collioni & Cia.
            </div>
            """,
            unsafe_allow_html = True
        )

    # Database connection
    database = con.database_vendas

    # ======================== APP SECTIONS ========================

    # Section: Introdução
    if st.session_state.current_section == "Introdução":
        st.header("Amostra dos Dados")
        st.markdown("Qual é a fundamentação do estudo?")
        st.dataframe(database.sample(25))

    # Section: Análise Exploratória
    elif st.session_state.current_section == "Análise Exploratória":
        st.header("Análise Exploratória")
        st.subheader("Relação entre Quantidade Vendida e Preço por Item de Café (Demandas inversas)")
        st.plotly_chart(con.figure1, use_container_width = True)
        st.subheader("Distribuições de Preços")
        st.plotly_chart(con.figure2, use_container_width = True)
        st.subheader("Análise Exploratória — Receitas Acumuladas")
        st.plotly_chart(con.figure4, use_container_width = True)
        st.subheader("Análise Exploratória — Receitas Diárias")
        st.plotly_chart(con.figure5, use_container_width = True)
        st.subheader("Análise Exploratória — Receita por Dia da Semana")
        st.plotly_chart(con.figure6, use_container_width = True)
        st.subheader("Análise Exploratória — Participação na Receita (Semanal)")
        st.plotly_chart(con.figure7, use_container_width = True)

    # Section: Elasticidades
    elif st.session_state.current_section == "Elasticidades":
        st.header("Elasticidades")
        st.subheader("Elasticidades-preço da Demanda Atuais")
        st.plotly_chart(con.figure3, use_container_width = True)
        st.subheader("Elasticidades-preço nos Pontos Ótimos")
        st.plotly_chart(con.figure9, use_container_width = True)

    # Section: Forecasting
    elif st.session_state.current_section == "Forecasting":
        st.header("Forecasting e Relacionados")
        st.subheader("Otimização de Preços Usando Modelos Aditivos Generalizados (GAM)")
        st.plotly_chart(con.figure8, use_container_width = True)

    # Section: Gerencial
    elif st.session_state.current_section == "Gerencial":
        st.subheader("Fluxo de caixa")
        st.text("Esse é o fluxo dos últimos x períodos.")
        st.plotly_chart(con.figure11, use_container_width=True)
        st.markdown("---")
        st.subheader("Liquidez")
        st.text("Aqui mostra a capacidade de liquidar as suas dívidas(passivos).")
        st.plotly_chart(con.figure12, use_container_width=True)
        st.markdown("---")
        st.subheader("Fluxo de Caixa Projetado")
        st.text("Projeção do resultado da empresa pelos próximos x períodos")
        st.table(con.df_tabela_final)
        st.markdown("---")
        st.subheader("Controle Gerencial de Estoques por Produto")
        st.plotly_chart(con.figure13, use_container_width=True)

    # Section: Decomposição
    elif st.session_state.current_section == "Decomposição":
        st.header("Decomposição de Séries")
        st.subheader("Decomposição: Tendência, Sazonalidade e Resíduo")
        st.plotly_chart(con.figure10, use_container_width = True)

    # Section: Entregáveis
    elif st.session_state.current_section == "Entregáveis":
        st.header("Entregáveis")
        st.dataframe(con.comparison_table)

    st.markdown("---")
    
    # Footer
    st.markdown(
        """
        <div style="width:100%; text-align:center; font-size:12px; color:#999999; margin-top:1rem; padding:1rem 0;">
        Elaboração realizada por Kautz-Collioni & Cia. Replicação desautorizada sem pedido prévio. | 
        E-mail: suporte@kautz.collioni_cia.com.br. |
        Telefone: (51) 9 8276-5730.
        </div>
        """,
        unsafe_allow_html = True
    )

# ======================== MAIN CONTROLLER ========================
if st.session_state.logged_in:
    main_app()
else:
    login_page()