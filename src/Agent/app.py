import streamlit as st
from agent import SemanaExerciciosAgent
from datetime import datetime

st.set_page_config(page_title="📚 Lista de Exercícios por Semana", layout="wide")

st.markdown("<h1 style='text-align: center;'>🎓 Gerador de Exercícios Semanais</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Clique na semana desejada para gerar uma lista de exercícios baseada no plano de ensino.</p>", unsafe_allow_html=True)
st.markdown("---")

if "selected_week" not in st.session_state:
    st.session_state.selected_week = None

# Botões de semana (1 a 9) centralizados
colunas = st.columns(9)
for i, col in enumerate(colunas):
    with col:
        if col.button(f"Semana {i+1}"):
            st.session_state.selected_week = i + 1  # salva no estado

# Botão central para gerar exercícios
if st.session_state.selected_week:
    st.markdown(
        f"<p style='text-align: center;'>Semana selecionada: <strong>{st.session_state.selected_week}</strong></p>",
        unsafe_allow_html=True
    )

    col_central = st.columns([3, 2, 3])[1]
    with col_central:
        gerar = st.button("🧠  GERAR EXERCÍCIOS", use_container_width=True)

    if gerar:
        with st.spinner("Gerando exercícios..."):
            agente = SemanaExerciciosAgent()
            resposta = agente.gerar_exercicios(st.session_state.selected_week)

            # Captura apenas o conteúdo do LLM
            if hasattr(resposta, "content"):
                resposta_texto = resposta.content
            elif isinstance(resposta, dict) and "content" in resposta:
                resposta_texto = resposta["content"]
            else:
                resposta_texto = str(resposta)

        st.success("✅ Exercícios gerados com sucesso!")
        st.subheader(f"📋 Exercícios para a Semana {st.session_state.selected_week}")
        st.markdown(resposta_texto, unsafe_allow_html=True)

        with st.expander("Copiar toda a resposta gerada"):
            st.code(resposta_texto)

        st.markdown("---")
        st.markdown(
            f"<p style='text-align: center; color: grey;'>💡 Última atualização: {datetime.today().strftime('%d/%m/%Y')}</p>",
            unsafe_allow_html=True
        )
