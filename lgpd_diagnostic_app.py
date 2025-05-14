"""
LGPD Self-Diagnosis App – Agentes de Pequeno Porte
Coelho Lima Advocacia · v1.3 · Maio/2025
Descrição: questionário Streamlit para avaliação preliminar de conformidade LGPD
focado em Microempresas (ME), Empresas de Pequeno Porte (EPP) e Startups,
conforme Resolução CD/ANPD nº 2/2022.
"""

import streamlit as st
from pathlib import Path

# —————————————————— Configuráveis —————————————————— #
WHATSAPP_LINK = "https://wa.me/5521974072870"        # ← substitua pelo número oficial
MANUAL_LINK   = "https://example.com/manual-lgpd.pdf"  # opcional (PDF externo)
TEMPLATE_PATH = Path(__file__).parent / "INV-01.xlsx"   # caminho do modelo Excel

# —————————————————— Page Config —————————————————— #
st.set_page_config(
    page_title="Diagnóstico LGPD – Pequeno Porte | Coelho Lima Advocacia",
    layout="centered",
    menu_items={
        "Get Help": WHATSAPP_LINK,
        "Report a bug": "mailto:marcos.lima@coelholima.com",
        "About": (
            "Ferramenta de autoavaliação simplificada baseada na Resolução CD/ANPD nº 2/2022. "
            "Não substitui parecer jurídico profissional."
        ),
    },
)

# —————————————————— Header —————————————————— #
st.title("📈 Diagnóstico Prévio de Conformidade LGPD – Pequeno Porte")

st.markdown(
    f"<a href='{WHATSAPP_LINK}' target='_blank' style='text-decoration:none;'>"
    "📞  Atendimento WhatsApp – <b>Coelho&nbsp;Lima&nbsp;Advocacia</b></a>",
    unsafe_allow_html=True,
)

# —————————————————— Glossário Completo —————————————————— #
with st.expander("📚 Glossário – clique para entender cada termo usado", expanded=False):
    st.markdown(
        """
| Termo | Explicação Rápida |
|-------|------------------|
| **Agente de Pequeno Porte (ATPP)** | ME, EPP ou Startup (art. 2º Res. 2/2022). |
| **Dados Pessoais** | Informação que identifique ou possa identificar alguém (ex.: nome, CPF, IP). |
| **Dados Sensíveis** | Saúde, biometria, opinião política, religião, orientação sexual, origem racial/étnica. |
| **Larga Escala** | Tratamento ≥ 10 000 titulares/ano ou volume que afete grande número de pessoas. |
| **Tratamento de Alto Risco** | Dados sensíveis **ou** larga escala **ou** vigilância sistemática; remove benefícios simplificados. |
| **Canal de Comunicação** | E-mail ou formulário disponível para titulares exercerem direitos. |
| **Encarregado (DPO)** | Pessoa de contato com titulares/ANPD; para pequeno porte é **dispensável**, mantém-se o canal. |
| **Registro das Operações (INV-01)** | Inventário simplificado das atividades de tratamento (Excel). |
| **Política de Privacidade** | Documento público com dados coletados, finalidades, bases legais e direitos. |
| **Processo de Atendimento (SOP-01)** | Procedimento interno para responder solicitações do titular em ≤ 15 dias. |
| **Controles Mínimos de Segurança** | Senha forte/2FA, backup 3-2-1, antivírus, criptografia, atualização. |
| **Plano de Incidentes (PRI-01)** | Detecção → análise → contenção → notificação (≤ 2 dias úteis) → lições aprendidas. |
| **ANPD** | Autoridade Nacional de Proteção de Dados – fiscaliza e aplica sanções. |
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
Este questionário avalia **6 controles essenciais** exigidos pela LGPD para
entidades de pequeno porte. Se selecionar “Média Empresa”, o sistema lembrará
que o regime simplificado não se aplica.
    """
)

# —————————————————— Download do Modelo de Registro —————————————————— #
if TEMPLATE_PATH.exists():
    with open(TEMPLATE_PATH, "rb") as f:
        st.download_button(
            label="📥  Baixar modelo de registro INV-01.xlsx",
            data=f,
            file_name="INV-01.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
else:
    st.warning("⚠️  Arquivo INV-01.xlsx não encontrado no repositório.")

# —————————————————— Formulário —————————————————— #
with st.form("lgpd_form"):

    st.subheader("1 · Porte da organização")
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

    st.subheader("2 · Escopo do tratamento de dados")
    sensitive = st.radio("A empresa trata **dados sensíveis**?", ["Sim", "Não"])
    large_scale = st.radio("O tratamento é realizado em **larga escala**?", ["Sim", "Não"])

    st.markdown("---")
    st.subheader("3 · Controles de governança e segurança")

    dpo = st.radio("Existe **canal de comunicação** com titulares?", ["Sim", "Não"])
    register_ops = st.radio("Há **registro das operações** (INV-01) atualizado?", ["Sim", "Não"])
    privacy_policy = st.radio("Política de privacidade publicada?", ["Sim", "Não"])
    data_subject = st.radio("Processo p/ atender titulares (SOP-01)?", ["Sim", "Não"])
    security_controls = st.radio("Controles mínimos de segurança implementados?", ["Sim", "Não"])
    incident_plan = st.radio("Plano de resposta a incidentes (PRI-01)?", ["Sim", "Não"])

    submit = st.form_submit_button("Avaliar Conformidade")

# —————————————————— Avaliação —————————————————— #
if submit:

    if company_size.startswith("Média"):
        st.info(
            "**Média Empresa identificada:** o regime de pequeno porte não se aplica.\n"
            "Adote todas as obrigações integrais da LGPD (DPO, RIPD, registro completo etc.)."
        )

    score_map = {"Sim": 1, "Não": 0}
    score = sum(
        score_map[x]
        for x in (
            dpo,
            register_ops,
            privacy_policy,
            data_subject,
            security_controls,
            incident_plan,
        )
    )
    elevated_risk = sensitive == "Sim" or large_scale == "Sim"

    if score >= 5 and not elevated_risk:
        st.success(
            "**Diagnóstico: Conformidade Básica Adequada**\n\n"
            "- Revise políticas anualmente.\n"
            "- Mantenha o registro INV-01 atualizado."
        )
    elif 3 <= score < 5 or elevated_risk:
        st.warning(
            "**Diagnóstico: Conformidade Parcial ou Risco Elevado**\n\n"
            "- Recomenda-se avaliação especializada.\n"
            "- Avalie a necessidade de Relatório de Impacto (art. 38)."
        )
    else:
        st.error(
            "**Diagnóstico: Não Conformidade**\n\n"
            "- Implante um plano de adequação completo com apoio profissional."
        )

    st.markdown(
        f"**Pontuação:** {score}/6 &nbsp;|&nbsp; **Risco elevado?** {'Sim' if elevated_risk else 'Não'}"
    )
    st.caption("Ferramenta de triagem inicial; não substitui assessoria jurídica.")

    st.markdown(
        f"<br><a href='{WHATSAPP_LINK}' target='_blank'>"
        "<button style='background-color:#25D366;border:none;color:white;padding:10px 20px;"
        "border-radius:4px;cursor:pointer;'>✉️  Agendar Consultoria via WhatsApp</button></a>",
        unsafe_allow_html=True,
    )

    if MANUAL_LINK:
        st.markdown(
            f"<p style='text-align:center;'>📄  <a href='{MANUAL_LINK}' target='_blank'>Baixar Manual Completo (PDF)</a></p>",
            unsafe_allow_html=True,
        )
