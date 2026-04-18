import streamlit as st
import pandas as pd
import google.generativeai as genai
import json
import os

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="AnyaFinanças 💜", page_icon="💜", layout="centered")
st.title("AnyaFinanças 💜")
st.markdown("Sua mentora de saúde financeira. Vamos organizar essas contas?")

# --- 2. CHAVE DA API ---
# Pede a chave da API na barra lateral para você não precisar expor no código
api_key = st.sidebar.text_input("Insira sua API Key do Gemini:", type="password")

if not api_key:
    st.warning("👈 Por favor, insira sua API Key do Google Gemini na barra lateral para começar.")
    st.stop()

# Configura o Gemini
genai.configure(api_key=api_key)

# --- 3. CARREGAMENTO DE DADOS (BASE DE CONHECIMENTO) ---
@st.cache_data
def carregar_dados():
    # Simulando a leitura dos arquivos da pasta data/
    # Adapte os caminhos caso a estrutura de pastas mude
    try:
        df_transacoes = pd.read_csv("../data/transacoes.csv")
        # Exemplo simples: somar gastos (você pode melhorar esse agrupamento depois)
        total_gasto = df_transacoes['valor'].sum()
        resumo_gastos = f"Total gasto no período: R$ {total_gasto:.2f}"
    except:
        resumo_gastos = "Dados de transações não encontrados."

    try:
        with open("../data/produtos_financeiros.json", "r") as f:
            produtos = json.load(f)
            resumo_produtos = json.dumps(produtos, indent=2, ensure_ascii=False)
    except:
        resumo_produtos = "Catálogo de produtos não encontrado."
        
    return resumo_gastos, resumo_produtos

resumo_gastos, resumo_produtos = carregar_dados()

# --- 4. CONFIGURAÇÃO DO PROMPT E MODELO ---
system_instruction = f"""
Você é a AnyaFinanças (ou Anya 💜), uma Analista de Saúde Financeira inteligente, empática e didática.
Seu foco é ajudar clientes a saírem do rotativo do cartão e organizarem o fluxo de caixa.

REGRAS:
1. EMPATIA: Nunca julgue o cliente. Seja acolhedora.
2. GROUNDING: Baseie-se apenas nos dados abaixo.
3. SEM INVESTIMENTOS: Não recomende ações ou cripto.
4. FAÇA PERGUNTAS: Não dê a solução de cara, investigue a situação primeiro.

[CONTEXTO DO SISTEMA]
Resumo de Gastos do Cliente: {resumo_gastos}
Produtos de Crédito Disponíveis no Banco: {resumo_produtos}
"""

# Inicializa o modelo Gemini (Usando o Flash, que é rápido e gratuito)
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_instruction
)

# --- 5. INTERFACE DE CHAT ---
# Botão para limpar a memória caso dê algum bug
if st.sidebar.button("Limpar Histórico de Chat"):
    st.session_state.chat_session = model.start_chat(history=[])
    st.rerun()

# Inicializa o histórico garantindo que o modelo certo seja usado
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

user_input = st.chat_input("Ex: Minha fatura veio alta, o que eu faço?")

if user_input:
    st.chat_message("user").markdown(user_input)
    with st.chat_message("assistant"):
        with st.spinner("Anya está analisando... 💜"):
            response = st.session_state.chat_session.send_message(user_input)
            st.markdown(response.text)