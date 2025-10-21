import streamlit as st
import time
import base64
import Conector as con

# ========================= 1. PAGE CONFIGURATION AND STYLE LOADING =========================

st.set_page_config(
    page_title = "Relatório Integrado | Kautz-Collioni & Cia.",
    layout = "wide",
    initial_sidebar_state = "expanded",
    menu_items = {
        'Get Help': 'https://docs.streamlit.io/',
        'Report a bug': "https://github.com/streamlit/streamlit/issues",
        'About': "Aplicação de Relatório Integrado."
    }
)

def load_css(file_name):
    with open(file_name, encoding = 'utf-8') as f:
        st.markdown(f'''<style>{f.read()}</style>''', unsafe_allow_html = True)

# ======================== 2. SESSION STATE INITIALIZATION ========================

# Controls the user's login state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Controls the current section in the main application
if 'current_section' not in st.session_state:
    st.session_state.current_section = "Introdução"

if 'logout_pending' not in st.session_state:
    st.session_state.logout_pending = False

if st.session_state.logout_pending:
    time.sleep(2.0)
    st.session_state.logout_pending = False 
    st.rerun()

if st.session_state.get('logout_pending', False):
    load_css("logout_style.css")

# ======================== 3. LOGIN PAGE ========================

def login_page():

    load_css("common_style.css")
    load_css("login_style.css")

    # Logo loading
    try:
        with open("Cabeçalho Escuro - Streamlit.png", "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode()
        
        st.markdown(
            f"""
            <div style='text-align: center; margin-bottom: 1rem;'>
                <img src='data:image/png;base64,{image_base64}' style='width: 70%; height: auto; pointer-events: none; user-select: none; -webkit-user-drag: none;' draggable='false'>
            </div>
            """,
            unsafe_allow_html = True
        )
    except FileNotFoundError:
        st.markdown('<div class="login-logo"><h2>Kautz-Collioni & Cia.</h2></div>', unsafe_allow_html = True)

    # Login form
    username = st.text_input("Usuário", key = "user_login")
    password = st.text_input("Senha", type = "password")

    # Login button
    if st.button("Entrar", key = "login_btn", use_container_width = True):
        if username == "João Silva" and password == "123456":  # Credentials
            st.success("Bem-vindo!")
            time.sleep(1)
            st.session_state.logged_in = True
            st.session_state.username = username
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

# ======================== 4. LOGOUT FUNCTION ========================

def back_to_login():
    keys_to_delete = list(st.session_state.keys())
    for key in keys_to_delete:
        del st.session_state[key]
    st.session_state.logout_pending = True

# ======================== 5. MAIN APPLICATION ========================

def main_app():
    # Load main application CSS
    load_css("common_style.css")
    load_css("sidebar_style.css")

    # Main application title
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

    with st.sidebar:
        # Loading the sidebar header logo
        try:
            with open("Cabecalho.svg", "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode()
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
            st.markdown("<h4>Kautz-Collioni & Cia.</h4>", unsafe_allow_html=True)

        # User greeting
        st.markdown(f'<div class="user-greeting">Olá, {st.session_state.username}!</div>', unsafe_allow_html=True)
        
        # Navigation menu - Sidebar buttons
        sidebar_options = ["Introdução", "Análise Exploratória", "Elasticidades", "Forecasting", "Gerencial", "Decomposição", "Entregáveis"]
        
        try:
            current_index = sidebar_options.index(st.session_state.current_section)
        except ValueError:
            current_index = 0

        section = st.radio(
            "Navegação", 
            sidebar_options, 
            index=current_index,
            key="nav_radio", 
            label_visibility="collapsed"
        )

        if section != st.session_state.current_section:
            st.session_state.current_section = section
            st.rerun()
        
        # Exit button - Logout
        st.button("Sair", key="logout_btn", on_click=back_to_login, use_container_width=True)

        # Sidebar footer
        st.markdown(
            '<div class="sidebar-footer">Todos os direitos reservados © 2025 | Kautz-Collioni & Cia.</div>',
            unsafe_allow_html=True
        )

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

    # Section: Elasticidades
    elif st.session_state.current_section == "Elasticidades":
        st.header("Elasticidades")
        st.subheader("Elasticidades-preço da Demanda Atuais")
        st.plotly_chart(con.figure3, use_container_width=True)
        st.subheader("Elasticidades-preço nos Pontos Ótimos")
        st.plotly_chart(con.figure9, use_container_width=True)

    # Section: Forecasting
    elif st.session_state.current_section == "Forecasting":
        st.header("Forecasting e Relacionados")
        st.subheader("Otimização de Preços Usando Modelos Aditivos Generalizados (GAM)")
        st.plotly_chart(con.figure8, use_container_width=True)

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
        st.plotly_chart(con.figure10, use_container_width=True)

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
        unsafe_allow_html=True
    )

# ======================== 6. MAIN CONTROLLER ========================

if st.session_state.logged_in:
    main_app()
else:
    login_page()