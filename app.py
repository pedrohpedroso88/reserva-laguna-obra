import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Gestão de Obras - Reserva Laguna Lote 16 QC", layout="wide", page_icon="🏗️")

st.title("🏗️ Sistema de Gestão de Obras - Reserva Laguna (Lote 16 QC)")
st.markdown("---")

# Centros de Custo baseados na planilha oficial
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

# Inicializa dados reais da planilha na sessão
if "despesas" not in st.session_state:
    dados_iniciais = [
        {"Fornecedor": "Diogo A Silva Dias", "NF/DOC": "PIX", "Data": "2025-10-21", "Descrição": "Levantamento planialtimétrico", "CC": 2, "Valor Total": 1300.00, "Valor Pago": 1300.00, "Observações": "Pago por Sônia dos Santos Carvalho"},
        {"Fornecedor": "Marco Flávio de Magalhães Matos", "NF/DOC": "PIX", "Data": "2025-11-13", "Descrição": "Projeto arquitetônico - 1ª parcela", "CC": 0, "Valor Total": 12000.00, "Valor Pago": 12000.00, "Observações": "Pago por Sônia dos Santos Carvalho"},
        {"Fornecedor": "Associação de moradores Reserva Laguna", "NF/DOC": "PIX", "Data": "2025-12-03", "Descrição": "Taxa de análise de projeto residencial", "CC": 19, "Valor Total": 1400.00, "Valor Pago": 1400.00, "Observações": "Pago por Sônia dos Santos Carvalho"},
        {"Fornecedor": "Bate & Sonda", "NF/DOC": "PIX", "Data": "2026-02-02", "Descrição": "Sondagem", "CC": 2, "Valor Total": 1600.00, "Valor Pago": 1600.00, "Observações": "Pago por Sônia dos Santos Carvalho"},
        {"Fornecedor": "WM Engenharia e Consultorias Ltda (DWT)", "NF/DOC": "20/27/30/08", "Data": "2026-03-02", "Descrição": "Projetos estrutural, hidráulico e elétrico", "CC": 0, "Valor Total": 12300.00, "Valor Pago": 12300.00, "Observações": "Pago por Sônia dos Santos Carvalho"},
        {"Fornecedor": "Marco Flávio de Magalhães Matos", "NF/DOC": "PIX", "Data": "2026-03-09", "Descrição": "Projeto arquitetônico - 2ª parcela", "CC": 0, "Valor Total": 12000.00, "Valor Pago": 12000.00, "Observações": "Pago por Sônia dos Santos Carvalho"},
        {"Fornecedor": "Prefeitura Municipal de Nova Lima", "NF/DOC": "3332403332", "Data": "2026-03-12", "Descrição": "Taxa de análise de projeto residencial", "CC": 19, "Valor Total": 491.71, "Valor Pago": 491.71, "Observações": "Pago por Sônia dos Santos Carvalho"},
        {"Fornecedor": "Prefeitura Municipal de Nova Lima", "NF/DOC": "PIX", "Data": "2026-06-08", "Descrição": "Taxa de análise de projeto terraplanagem", "CC": 19, "Valor Total": 250.74, "Valor Pago": 250.74, "Observações": "Pago por Marco Flávio - Reembolsado"},
        {"Fornecedor": "Prefeitura Municipal de Nova Lima", "NF/DOC": "Boleto", "Data": "2026-08-18", "Descrição": "Taxa de movimentação complementar de terra", "CC": 19, "Valor Total": 25.35, "Valor Pago": 25.35, "Observações": "Pago por Sônia dos Santos Carvalho"},
        {"Fornecedor": "Lais Bertini", "NF/DOC": "PIX", "Data": "2026-08-26", "Descrição": "Documentação ambiental - Aterro", "CC": 19, "Valor Total": 1774.73, "Valor Pago": 1774.73, "Observações": "Pago por Sônia dos Santos Carvalho"},
        {"Fornecedor": "Prefeitura Municipal de Nova Lima", "NF/DOC": "Boleto", "Data": "2026-09-10", "Descrição": "Taxa de alvará de construção", "CC": 19, "Valor Total": 570.40, "Valor Pago": 570.40, "Observações": "Pago por Sônia dos Santos Carvalho"},
        {"Fornecedor": "Lançamento Pendente (Exemplo)", "NF/DOC": "S/N", "Data": "2026-09-15", "Descrição": "Despesa em aberto na planilha", "CC": 0, "Valor Total": 100.00, "Valor Pago": 0.00, "Observações": "Aguardando pagamento"}
    ]
    st.session_state.despesas = pd.DataFrame(dados_iniciais)

if "diario" not in st.session_state:
    st.session_state.diario = pd.DataFrame([
        {"Data": "2026-09-10", "Etapa": "19 - TAXAS ADM. / IMPOSTOS / ENCARGOS", "Responsável": "Eng. Responsável", "Clima": "Sol", "Equipe": 2, "Ocorrências": "Alvará de construção emitido pela Prefeitura de Nova Lima."}
    ])

# Menu Lateral do Sistema
menu = st.sidebar.radio("Navegação do Sistema", [
    "📊 Dashboard & Etapas",
    "➕ Lançar Nova Despesa",
    "📋 Extrato & Edição de Notas",
    "👷 Diário de Obra (Gestão)"
])

df = st.session_state.despesas.copy()
df["Saldo a Pagar"] = df["Valor Total"] - df["Valor Pago"]
df["Etapa"] = df["CC"].map(ETAPAS)

# TELA 1: DASHBOARD
if menu == "📊 Dashboard & Etapas":
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Custo Total Lançado", f"R$ {df['Valor Total'].sum():,.2f}")
    col2.metric("Total Pago", f"R$ {df['Valor Pago'].sum():,.2f}")
    col3.metric("Saldo a Pagar", f"R$ {df['Saldo a Pagar'].sum():,.2f}")
    col4.metric("Lançamentos", len(df))

    st.subheader("Resumo por Centro de Custo / Etapa")
    resumo_etapas = df.groupby(["CC", "Etapa"])[["Valor Total", "Valor Pago", "Saldo a Pagar"]].sum().reset_index()
    
    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.dataframe(resumo_etapas, use_container_width=True, hide_index=True)
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
        data = col3.date_input("Data da Despesa")
        cc_selecionado = col4.selectbox("Centro de Custo / Etapa *", options=list(ETAPAS.keys()), format_func=lambda x: ETAPAS[x])
        
        descricao = st.text_input("Descrição da Despesa *")
        
        col5, col6 = st.columns(2)
        valor_total = col5.number_input("Valor Total (R$) *", min_value=0.0, step=50.0)
        valor_pago = col6.number_input("Valor Já Pago (R$)", min_value=0.0, step=50.0)
        
        obs = st.text_input("Observações (Ex: Pago por..., parcelamento, etc.)")
        
        enviado = st.form_submit_button("✅ Salvar Lançamento")
        if enviado and fornecedor and valor_total > 0:
            novo = pd.DataFrame([{
                "Fornecedor": fornecedor, "NF/DOC": nf_doc, "Data": str(data),
                "Descrição": descricao, "CC": cc_selecionado, "Valor Total": valor_total,
                "Valor Pago": valor_pago, "Observações": obs
            }])
            st.session_state.despesas = pd.concat([st.session_state.despesas, novo], ignore_index=True)
            st.success("Despesa registrada com sucesso!")

# TELA 3: EXTRATO E EDIÇÃO DIRETA
elif menu == "📋 Extrato & Edição de Notas":
    st.subheader("Controle e Edição Direta de Lançamentos")
    st.info("💡 **Dica:** Você pode clicar diretamente nas células da tabela abaixo para editar valores, fornecedores, descrições ou status de pagamento. As alterações são salvas na hora!")
    
    # Tabela editável direto na tela
    df_editado = st.data_editor(
        st.session_state.despesas,
        num_rows="dynamic",
        use_container_width=True,
        key="editor_despesas"
    )
    
    # Atualiza o estado da sessão com as edições feitas pelo usuário na tabela
    st.session_state.despesas = df_editado

# TELA 4: DIÁRIO DE OBRA
elif menu == "👷 Diário de Obra (Gestão)":
    st.subheader("Registro Diário de Obra (RDO)")
    with st.form("form_rdo", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        data_rdo = c1.date_input("Data")
        etapa_rdo = c2.selectbox("Etapa em Execução", list(ETAPAS.values()))
        clima = c3.selectbox("Clima", ["Sol", "Nublado", "Chuva"])
        
        c4, c5 = st.columns(2)
        resp = c4.text_input("Responsável pelo Registro")
        qtd_equipe = c5.number_input("Qtd. Trabalhadores na Obra", min_value=0, step=1)
        ocorrencias = st.text_area("Atividades Executadas e Observações")
        
        if st.form_submit_button("Registrar Diário"):
            novo_rdo = pd.DataFrame([{"Data": str(data_rdo), "Etapa": etapa_rdo, "Responsável": resp, "Clima": clima, "Equipe": qtd_equipe, "Ocorrências": ocorrencias}])
            st.session_state.diario = pd.concat([st.session_state.diario, novo_rdo], ignore_index=True)
            st.success("Diário registrado com sucesso!")
            
    st.dataframe(st.session_state.diario, use_container_width=True, hide_index=True)