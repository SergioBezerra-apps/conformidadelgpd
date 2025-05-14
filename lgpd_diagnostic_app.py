"""
LGPD Self-Diagnosis App – Pequeno Porte
Coelho Lima Advocacia · Maio/2025
Descrição: questionário simplificado para agentes de tratamento
de pequeno porte (ME, EPP, Startup etc) de acordo com a Res. CD/ANPD 2/2022.
"""

import streamlit as st

# 🔧 Substitua pelo número oficial do escritório
WHATSAPP_LINK = "https://wa.me/5521974072870"

# ----------------------- Configuração da página ----------------------- #
st.set_page_config(
    page_title="Diagnóstico LGPD – Pequeno Porte | Coelho Lima Advocacia",
    layout="centered",
    menu_items={
        "Get Help": WHATSAPP_LINK,
        "Report a bug": "mailto:marcoslima@coelholima.com",
        "About": (
            "Ferramenta de autoavaliação baseada na Resolução CD/ANPD nº 2/2022. "
            "Não substitui parecer jurídico."
        ),
    },
)

# ----------------------- Cabeçalho ----------------------- #
st.title("📈  Diagnóstico Prévio de Conformidade LGPD – Pequeno Porte")

st.markdown(
    f"<a href='{WHATSAPP_LINK}' target='_blank' style='text-decoration:none;'>"
    "📞  Atendimento WhatsApp – <b>Coelho&nbsp;Lima&nbsp;Advocacia</b></a>",
    unsafe_allow_html=True,
)

with st.expander("📚 Glossário rápido dos termos usados", expanded=False):
    st.markdown(
        """
- **Dados sensíveis** – saúde, biometria, opinião política etc.  
- **Larga escala** – ≥ 10 mil titulares/ano.  
- **Canal de comunicação** – e-mail ou formulário publicado para o titular.  
- **Registro de operações** – planilha simplificada INV-01.xlsx.  
- **Plano de incidentes** – documento PRI-01 com fluxo de notificação.
        """
    )

st.markdown(
    """
Este questionário avalia **6 controles essenciais** previstos para **agentes de
tratamento de pequeno porte (ME, EPP ou Startup)**.  
Se você selecionar “Média Empresa”, o app apenas alerta que o regime
simplificado **não se aplica**.
"""
)

# ----------------------- Formulário ----------------------- #
with st.form("lgpd_form"):
    st.subheader("1. Porte da organização")

    company_size = st.radio(
        "Selecione o enquadramento:",
        [
            "Microempresa (ME)",
            "Empresa de Pequeno Porte (EPP)",
            "Startup (LC 182/21)",
            "Média Empresa – fora do regime simplificado",
            "Outra",
        ],
    )

    st.subheader("2. Escopo do tratamento de dados")
    sensitive = st.radio("A empresa trata **dados sensíveis**?", ["Sim", "Não"])
    large_scale = st.radio("Trata dados **em larga escala** (≥ 10 mil titulares/ano)?", ["Sim", "Não"])

    st.markdown("---")
    st.subheader("3. Controles de governança e segurança")

    dpo = st.radio("Existe **canal de comunicação** com titulares?", ["Sim", "Não"])
    register_ops = st.radio("Há **registro das operações** (INV-01)?", ["Sim", "Não"])
    privacy_policy = st.radio("Política de privacidade publicada?", ["Sim", "Não"])
    data_subject = st.radio("Processo formal p/ atender titulares?", ["Sim", "Não"])
    security_controls = st.radio("Controles mínimos de segurança implementados?", ["Sim", "Não"])
    incident_plan = st.radio("Plano de resposta a incidentes (PRI-01)?", ["Sim", "Não"])

    submit = st.form_submit_button("Avaliar Conformidade")

# ----------------------- Avaliação ----------------------- #
if submit:
    # Alerta para médias empresas
    if company_size.startswith("Média"):
        st.info(
            """
**Média Empresa não é coberta pelo regime de pequeno porte.**  
Siga todas as obrigações integrais da LGPD (DPO, RIPD, registro completo etc.).
"""
        )

    score_map = {"Sim": 1, "Não": 0}
    score = sum(
        [
            score_map[dpo],
            score_map[register_ops],
            score_map[privacy_policy],
            score_map[data_subject],
            score_map[security_controls],
            score_map[incident_plan],
        ]
    )

    elevated_risk = sensitive == "Sim" or large_scale == "Sim"

    if score >= 5 and not elevated_risk:
        st.success(
            """
**Diagnóstico preliminar: Conformidade Básica Adequada.**

- Revise políticas e controles periodicamente (art. 50).
- Mantenha registros atualizados e treinamento anual.
"""
        )
    elif 3 <= score < 5 or elevated_risk:
        st.warning(
            """
**Diagnóstico preliminar: Conformidade Parcial ou Risco Elevado.**

- Recomenda-se avaliação especializada, sobretudo se houver sensíveis ou larga escala.
- Considere Relatório de Impacto (art. 38) e revisão contratual com operadores.
"""
        )
    else:
        st.error(
            """
**Diagnóstico preliminar: Não Conformidade.**

- Lacunas significativas em governança de privacidade.
- Implante um **Plano de Adequação** completo com apoio profissional.
"""
        )

    st.markdown(f"**Pontuação:** {score} / 6 &nbsp;|&nbsp; **Risco elevado?** {'Sim' if elevated_risk else 'Não'}")
    st.caption("*Ferramenta de triagem inicial; não dispensa assessoria jurídica.*")

    st.markdown(
        f"""
<br>
<a href='{WHATSAPP_LINK}' target='_blank'>
<button style='background-color:#25D366;border:none;color:white;padding:10px 20px;
border-radius:4px;cursor:pointer;'>✉️  Agendar Consultoria via WhatsApp
</button></a>
""",
        unsafe_allow_html=True,
    )
