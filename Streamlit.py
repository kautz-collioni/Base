import streamlit as st
import Conector as con

st.set_page_config(
    page_title = "Projeto KC",
    page_icon = "📊",
    layout = "wide",
    initial_sidebar_state = "auto",
    menu_items = {
        'Get Help': 'https://docs.streamlit.io/',
        'Report a bug': "https://github.com/streamlit/streamlit/issues",
        'About': ""
    }
)

st.markdown("""
    <style>
    .nav-button {
        background: transparent !important;
        color: #262730 !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0.5rem 0.75rem !important;
        margin: 0 !important;
        width: 100% !important;
        text-align: center;
        font-weight: 500;
        border-radius: 0 !important;
        transition: all 0.2s ease;
    }
    .nav-button:hover {
        background: rgba(0, 0, 0, 0.05) !important;
        color: #4b7bec !important;
    }
    .nav-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 1rem;
        border-bottom: 1px solid #e6e6e6;
        padding-bottom: 0.5rem;
        width: 100%;
    }
    .stColumn {
        flex: 1;
        min-width: 0;
    }
    .current-section {
        font-size: 1.5rem;
        font-weight: 600;
        color: #4b7bec;
        margin: 1rem 0;
        padding: 0.5rem;
        border-left: 4px solid #4b7bec;
        background: rgba(75, 123, 236, 0.05);
    }
    </style>
""", unsafe_allow_html = True)

st.markdown(
    """
    <h2 style='text-align: center; color: gray; font-weight: normal;'>
        Projeto KC
    </h2>
    """,
    unsafe_allow_html = True
)

st.markdown('<div class="nav-container">', unsafe_allow_html = True)
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
with col1: introducao_btn = st.button("Introdução", key = "intro_btn", use_container_width = True)
with col2: analise_btn = st.button("Análise Exploratória", key = "analise_btn", use_container_width = True)
with col3: elasticidades_btn = st.button("Elasticidades", key = "elastic_btn", use_container_width = True)
with col4: forecasting_btn = st.button("Forecasting", key = "forecast_btn", use_container_width = True)
with col5: alternativos_btn = st.button("Alternativos", key = "alt_btn", use_container_width = True)
with col6: decomposicao_btn = st.button("Decomposição", key = "decomp_btn", use_container_width = True)
with col7: entregaveis_btn = st.button("Entregáveis", key = "entreg_btn", use_container_width = True)
st.markdown('</div>', unsafe_allow_html = True)

st.markdown("""
<style>
.nav-button {
    background-color: transparent !important;
    color: #262730 !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
    text-align: center;
    font-weight: 500;
    border-radius: 0 !important;
    transition: all 0.2s ease;
    cursor: pointer;
}
.nav-button:hover {
    color: #4b7bec !important;
    background-color: transparent !important;
}
.stButton button {
    all: unset;
    cursor: pointer;
}
</style>
<script>
document.querySelectorAll('.stButton button').forEach(button => {
    button.classList.add('nav-button');
});
</script>
""", unsafe_allow_html = True)

if 'current_section' not in st.session_state:
    st.session_state.current_section = "Introdução"
if introducao_btn: st.session_state.current_section = "Introdução"
if analise_btn: st.session_state.current_section = "Análise Exploratória"
if elasticidades_btn: st.session_state.current_section = "Elasticidades"
if forecasting_btn: st.session_state.current_section = "Forecasting"
if alternativos_btn: st.session_state.current_section = "Alternativos"
if decomposicao_btn: st.session_state.current_section = "Decomposição"
if entregaveis_btn: st.session_state.current_section = "Entregáveis"

database = con.database

if st.session_state.current_section == "Introdução":
    st.header("Amostra dos Dados")
    st.markdown("Qual é a fundamentação do estudo?")
    st.dataframe(database.sample(25))
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
elif st.session_state.current_section == "Elasticidades":
    st.header("Elasticidades")
    st.subheader("Elasticidades-preço da Demanda Atuais")
    st.plotly_chart(
        (lambda fig: ([setattr(trace, "width", 0.6) for trace in fig.data if hasattr(trace, "width")], fig)[1])(con.figure3),
        use_container_width = True
    )
    st.subheader("Elasticidades-preço nos Pontos Ótimos")
    st.plotly_chart(
        (lambda fig: ([setattr(trace, "width", 0.6) for trace in fig.data if hasattr(trace, "width")], fig)[1])(con.figure9),
        use_container_width = True
    )
elif st.session_state.current_section == "Forecasting":
    st.header("Forecasting e Relacionados")
    st.subheader("Otimização de Preços Usando Modelos Aditivos Generalizados (GAM)")
    st.plotly_chart(con.figure8, use_container_width = True)
elif st.session_state.current_section == "Alternativos":
    st.header("Modelos Alternativos")
    st.subheader("Modelo Paramétrico Alternativo")
elif st.session_state.current_section == "Decomposição":
    st.header("Decomposição de Séries")
    st.subheader("Decomposição: Tendência, Sazonalidade e Resíduo")
    st.plotly_chart(con.figure10, use_container_width = True)
elif st.session_state.current_section == "Entregáveis":
    st.header("Entregáveis")
    st.dataframe(con.comparison_table)

st.markdown("---")