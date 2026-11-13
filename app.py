import streamlit as st
import pandas as pd
import plotly.express as px
import os
import io

# Configuração da página
st.set_page_config(page_title="Gestão de Obras - Reserva Laguna Lote 16 QC", layout="wide", page_icon="🏗️")

st.title("🏗️ Sistema de Obra - Reserva Laguna (Lote 16 QC)")
st.markdown("---")

ETAPAS = {
    0: "0 - ORÇAMENTOS E PROJETOS",
    1: "1 - SERVIÇOS PRELIMINARES",
    2: "2 - TRABALHOS EM TERRA / FUNDAÇÃO",
    3: "3 - ESTRUTURA DE CONCRETO",
    4: "4 - ALVENARIAS E DIVISÕES",
    5: "5 - ESQUADRIAS / SERRALHERIA",
    6: "6 - INSTALAÇÕES HIDRO-SANITÁRIAS",
    7: "7 - INSTALAÇÕES ELÉTRICAS",
    8: "8 - REVESTIMENTOS",
    9: "9 - PISOS, SOLEIRAS E RODAPÉS",
    10: "10 - FORROS",
    11: "11 - COBERTURA",
    12: "12 - COMPLEMENTARES",
    13: "13 - BANCADA",
    14: "14 - PINTURAS",
    15: "15 - MARCENARIA",
    16: "16 - DIVERSOS",
    17: "17 - SERVIÇOS FINAIS",
    18: "18 - ELETRODOMÉSTICOS / AUTOMAÇÃO",
    19: "19 - TAXAS ADM. / IMPOSTOS / ENCARGOS",
    20: "20 - LOTE",
    21: "21 - MÃO DE OBRA"
}

ARQUIVO_DADOS = "dados_obra.csv"
ARQUIVO_DIARIO = "diario_obra.csv"

# Função auxiliar para formatar em Reais (Padrão BR)
def fmt_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Carregamento seguro dos dados
if "despesas" not in st.session_state:
    if os.path.exists(ARQUIVO_DADOS):
        st.session_state.despesas = pd.read_csv(ARQUIVO_DADOS)
    else:
        dados_iniciais = [
            {"Fornecedor": "Diogo A Silva Dias", "NF/DOC": "PIX", "Data": "21/10/2025", "Descrição": "Levantamento planialtimétrico", "CC": 2, "Valor Total": 1300.00, "Valor Pago": 1300.00, "Observações": "Pago por Sônia dos Santos Carvalho"},
            {"Fornecedor": "Marco Flávio de Magalhães Matos", "NF/DOC": "PIX", "Data": "13/11/2025", "Descrição": "Projeto arquitetônico - 1ª parcela", "CC": 0, "Valor Total": 12000.00, "Valor Pago": 12000.00, "Observações": "Pago por Sônia dos Santos Carvalho"},
            {"Fornecedor": "Associação de moradores Reserva Laguna", "NF/DOC": "PIX", "Data": "03/12/2025", "Descrição": "Taxa de análise de projeto residencial", "CC": 19, "Valor Total": 1400.00, "Valor Pago": 1400.00, "Observações": "Pago por Sônia dos Santos Carvalho"},
            {"Fornecedor": "Bate & Sonda", "NF/DOC": "PIX", "Data": "02/02/2026", "Descrição": "Sondagem", "CC": 2, "Valor Total": 1600.00, "Valor Pago": 1600.00, "Observações": "Pago por Sônia dos Santos Carvalho"},
            {"Fornecedor": "WM Engenharia e Consultorias Ltda (DWT)", "NF/DOC": "20/27/30/08", "Data": "02/03/2026", "Descrição": "Projetos estrutural, hidráulico e elétrico", "CC": 0, "Valor Total": 12300.00, "Valor Pago": 12300.00, "Observações": "Pago por Sônia dos Santos Carvalho"},
            {"Fornecedor": "Marco Flávio de Magalhães Matos", "NF/DOC": "PIX", "Data": "09/03/2026", "Descrição": "Projeto arquitetônico - 2ª parcela", "CC": 0, "Valor Total": 12000.00, "Valor Pago": 12000.00, "Observações": "Pago por Sônia dos Santos Carvalho"},
            {"Fornecedor": "Prefeitura Municipal de Nova Lima", "NF/DOC": "3332403332", "Data": "12/03/2026", "Descrição": "Taxa de análise de projeto residencial", "CC": 19, "Valor Total": 491.71, "Valor Pago": 491.71, "Observações": "Pago por Sônia dos Santos Carvalho"},
            {"Fornecedor": "Prefeitura Municipal de Nova Lima", "NF/DOC": "PIX", "Data": "08/06/2026", "Descrição": "Taxa de análise de projeto terraplanagem", "CC": 19, "Valor Total": 250.74, "Valor Pago": 250.74, "Observações": "Pago por Marco Flávio - Reembolsado"},
            {"Fornecedor": "Prefeitura Municipal de Nova Lima", "NF/DOC": "Boleto", "Data": "18/08/2026", "Descrição": "Taxa de movimentação complementar de terra", "CC": 19, "Valor Total": 25.35, "Valor Pago": 25.35, "Observações": "Pago por Sônia dos Santos Carvalho"},
            {"Fornecedor": "Lais Bertini", "NF/DOC": "PIX", "Data": "26/08/2026", "Descrição": "Documentação ambiental - Aterro", "CC": 19, "Valor Total": 1774.73, "Valor Pago": 1774.73, "Observações": "Pago por Sônia dos Santos Carvalho"},
            {"Fornecedor": "Prefeitura Municipal de Nova Lima", "NF/DOC": "Boleto", "Data": "10/09/2026", "Descrição": "Taxa de alvará de construção", "CC": 19, "Valor Total": 570.40, "Valor Pago": 570.40, "Observações": "Pago por Sônia dos Santos Carvalho"},
            {"Fornecedor": "Lançamento Pendente (Exemplo)", "NF/DOC": "S/N", "Data": "15/09/2026", "Descrição": "Despesa em aberto na planilha", "CC": 0, "Valor Total": 100.00, "Valor Pago": 0.00, "Observações": "Aguardando pagamento"}
        ]
        st.session_state.despesas = pd.DataFrame(dados_iniciais)
        st.session_state.despesas.to_csv(ARQUIVO_DADOS, index=False, sep=';', encoding='utf-8-sig')

if "diario" not in st.session_state:
    if os.path.exists(ARQUIVO_DIARIO):
        st.session_state.diario = pd.read_csv(ARQUIVO_DIARIO)
    else:
        st.session_state.diario = pd.DataFrame([
            {"Data": "10/09/2026", "Etapa": "19 - TAXAS ADM. / IMPOSTOS / ENCARGOS", "Responsável": "Eng. Responsável", "Clima": "Sol", "Equipe": 2, "Ocorrências": "Alvará de construção emitido pela Prefeitura de Nova Lima."}
        ])
        st.session_state.diario.to_csv(ARQUIVO_DIARIO, index=False, sep=';', encoding='utf-8-sig')

# Menu Lateral
menu = st.sidebar.radio("Navegação do Sistema", [
    "📊 Dashboard & Etapas",
    "➕ Lançar Nova Despesa",
    "📋 Extrato & Edição de Notas",
    "👷 Diário de Obra (Gestão)",
    "💾 Central de Backup Geral"
])

df = st.session_state.despesas.copy()
df["Saldo a Pagar"] = df["Valor Total"] - df["Valor Pago"]
df["Etapa"] = df["CC"].map(ETAPAS)

# TELA 1: DASHBOARD
if menu == "📊 Dashboard & Etapas":
    total_geral = df['Valor Total'].sum()
    total_pago = df['Valor Pago'].sum()
    total_pendente = df['Saldo a Pagar'].sum()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Custo Total Lançado", fmt_brl(total_geral))
    col2.metric("Total Pago", fmt_brl(total_pago))
    col3.metric("Saldo a Pagar", fmt_brl(total_pendente))
    col4.metric("Lançamentos", len(df))

    st.subheader("Resumo por Centro de Custo / Etapa")
    resumo_etapas = df.groupby(["CC", "Etapa"])[["Valor Total", "Valor Pago", "Saldo a Pagar"]].sum().reset_index()
    
    resumo_exibicao = resumo_etapas.copy()
    resumo_exibicao["Valor Total"] = resumo_exibicao["Valor Total"].apply(fmt_brl)
    resumo_exibicao["Valor Pago"] = resumo_exibicao["Valor Pago"].apply(fmt_brl)
    resumo_exibicao["Saldo a Pagar"] = resumo_exibicao["Saldo a Pagar"].apply(fmt_brl)
    
    c1, c2 = st.columns([1.3, 1])
    with c1:
        st.dataframe(resumo_exibicao, use_container_width=True, hide_index=True)
    with c2:
        fig = px.pie(resumo_etapas, values="Valor Total", names="Etapa", title="Distribuição de Custos", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

# TELA 2: LANÇAR DESPESA
elif menu == "➕ Lançar Nova Despesa":
    st.subheader("Novo Lançamento de Despesa / Nota Fiscal")
    with st.form("form_despesa", clear_on_submit=True):
        col1, col2 = st.columns(2)
        fornecedor = col1.text_input("Fornecedor *")
        nf_doc = col2.selectbox("Forma / Documento *", ["PIX", "Boleto", "Nota Fiscal", "Transferência", "Dinheiro"])
        
        col3, col4 = st.columns(2)
        data_input = col3.date_input("Data da Despesa")
        data_str = data_input.strftime("%d/%m/%Y")
        cc_selecionado = col4.selectbox("Centro de Custo / Etapa *", options=list(ETAPAS.keys()), format_func=lambda x: ETAPAS[x])
        
        descricao = st.text_input("Descrição da Despesa *")
        
        col5, col6 = st.columns(2)
        valor_total = col5.number_input("Valor Total (
