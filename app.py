import streamlit as st
import re
import math
import json
from typing import Dict, List, Any

# Configuração da Página Web (Tema Escuro Cyberpunk)
st.set_page_config(
    page_title="SIGMA CORE v10 - Cognitive Graph",
    page_icon="🧠",
    layout="wide"
)

# Estilização CSS para transformar o Streamlit numa interface de produto SaaS profissional
st.markdown("""
    <style>
        .stApp { background-color: #0b0f19; color: #ecf0f1; }
        h1, h2, h3 { font-family: 'Courier New', monospace !important; color: #3b82f6 !important; }
        .saas-card { background-color: #111827; border: 1px solid #1e293b; padding: 25px; border-radius: 8px; border-left: 5px solid #3b82f6; margin-bottom: 20px; }
        .premium-box { background-color: #1e1b4b; border: 2px dashed #6366f1; padding: 20px; border-radius: 8px; text-align: center; margin-top: 15px; }
        .stButton>button { background-color: #1e293b; color: #38bdf8; border: 1px solid #38bdf8; font-family: 'Courier New', monospace; font-weight: bold; width: 100%; height: 45px; transition: all 0.3s; }
        .stButton>button:hover { background-color: #38bdf8; color: #0b0f19; box-shadow: 0 0 15px #38bdf8; }
        .monetize-btn a { display: block; background: linear-gradient(90deg, #3b82f6, #6366f1); color: white !important; text-align: center; padding: 12px; border-radius: 6px; font-weight: bold; text-decoration: none; box-shadow: 0 4px 10px rgba(99, 102, 241, 0.4); transition: 0.3s; }
        .monetize-btn a:hover { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(99, 102, 241, 0.6); }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# MOTOR COGNITIVO EM GRAFO v10.0 (ENGINE INTERNA)
# =====================================================================
class SigmaCognitiveGraphV10:
    def __init__(self):
        if 'nodes' not in st.session_state:
            st.session_state.nodes = {
                "estabilidade": {"activation": 50.0, "base_decay": 0.12},
                "ideacao": {"activation": 50.0, "base_decay": 0.15},
                "execucao": {"activation": 50.0, "base_decay": 0.18},
                "magnetismo": {"activation": 50.0, "base_decay": 0.10},
                "resistencia": {"activation": 50.0, "base_decay": 0.08}
            }
        if 'synapses' not in st.session_state:
            st.session_state.synapses = {
                ("ideacao", "execucao"): -0.35,
                ("execucao", "estabilidade"): 0.40,
                ("resistencia", "execucao"): 0.35,
                ("estabilidade", "ideacao"): -0.20,
                ("execucao", "ideacao"): -0.30
            }
        self.lexicon = {
            "estabilidade": {"calmo": 2.5, "ansioso": -2.0, "rotina": 1.8, "medo": -2.5, "foco": 2.0},
            "ideacao": {"ia": 3.0, "agi": 3.5, "sistema": 1.5, "criar": 2.0, "complexo": 2.5},
            "execucao": {"fazer": 1.5, "código": 2.5, "executar": 3.0, "entregar": 3.5, "build": 2.5},
            "magnetismo": {"liderar": 2.5, "pessoas": 1.5, "vender": 2.5, "influenciar": 2.0},
            "resistencia": {"persistir": 3.0, "continuar": 2.0, "aguentar": 2.5, "falhar": -1.5}
        }

    def _activation_function(self, x: float) -> float:
        return round(100.0 / (1.0 + math.exp(-0.08 * (x - 50.0))), 2)

    def process_cycle(self, input_text: str, external_grounding: bool = False):
        clean_text = input_text.lower()
        words = re.findall(r'\w+', clean_text)
        
        input_injection = {node: 0.0 for node in st.session_state.nodes}
        for word in words:
            for node in st.session_state.nodes:
                if word in self.lexicon[node]:
                    input_injection[node] += self.lexicon[node][word]
        
        current_activations = {node: st.session_state.nodes[node]["activation"] for node in st.session_state.nodes}
        
        for target_node in st.session_state.nodes:
            meta = st.session_state.nodes[target_node]
            decay = current_activations[target_node] * meta["base_decay"]
            
            synaptic_influence = 0.0
            for (source, target), weight in st.session_state.synapses.items():
                if target == target_node and current_activations[source] > 20.0:
                    synaptic_influence += (current_activations[source] * weight)
            
            grounding_bonus = 18.0 if (external_grounding and target_node in ["execucao", "resistencia"]) else 0.0
            
            net_force = current_activations[target_node] - decay + (input_injection[target_node] * 4.5) + (synaptic_influence * 0.5) + grounding_bonus
            st.session_state.nodes[target_node]["activation"] = self._activation_function(net_force)

# =====================================================================
# INTERFACE DE USUÁRIO (DASHBOARD SAAS)
# =====================================================================
def main():
    st.title("🧠 S.I.G.M.A. Cognitive Graph Engine v10")
    st.subheader("Auditoria Dinâmica de Sistemas e Comportamento Humano Intermediado por Grafo")
    st.write("---")

    engine = SigmaCognitiveGraphV10()

    # Layout em colunas: Painel de Controle e Resultados
    col_input, col_display = st.columns([1, 1.2])

    with col_input:
        st.markdown("### 📥 Entrada de Estímulo Semântico")
        user_input = st.text_area(
            "Digite o log operacional, padrão de texto ou relatório diário do alvo:",
            value="Estou planejando um novo ecossistema de inteligência artificial complexo com agentes autônomos e AGI.",
            height=120
        )
        
        # Variáveis de controle de ancoragem material
        grounding_active = st.checkbox("🔥 Ativar Grounding de Ação Física (Código rodando / Hardware ESP32 conectado)")
        
        if st.button("🔴 PROCESSAR CICLO COGNITIVO"):
            engine.process_cycle(user_input, external_grounding=grounding_active)
            st.success("Ciclo processado no grafo local com sucesso!")

        # ════════════════════════════════════════════════════════════
        # FUNIL DE MONETIZAÇÃO ATIVO (GANHAR DINHEIRO DE IMEDIATO)
        # ════════════════════════════════════════════════════════════
        st.markdown("<div class='premium-box'>", unsafe_allow_html=True)
        st.markdown("### ⚡ VERSÃO CORPORATIVA COMPLETA (B2B)")
        st.write("Precisa de rastreamento persistente para a sua equipa de engenharia, exportação de laudos executivos em PDF com CSS tático e integração direta com APIs de agentes baseados em LLM?")
        
        # LINK DE PAGAMENTO / CAPTURA (Substitua pelo seu link do Stripe, MercadoPago ou WhatsApp)
        st.markdown("""
            <div class='monetize-btn'>
                <a href='https://wa.me/SEUNUMERO' target='_blank'>💼 COMPRAR LICENÇA COMERCIAL / ACESSO PREMIUM</a>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<p style='font-size: 8pt; color: #64748b; margin-top: 5px;'>Licenças a partir de $49/mês ou setup personalizado.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_display:
        st.markdown("### 📊 Telemetria de Ativação dos Nós do Grafo")
        
        # Renderização dos indicadores em tempo real
        for node, data in st.session_state.nodes.items():
            activation_val = data["activation"]
            
            # Alertas Visuais de Estado Baseado em Limiares Biológicos
            if activation_val > 75.0:
                status_label = f"🔥 {node.upper()} : {activation_val}% [SATURAÇÃO DE FLUXO]"
            elif activation_val < 30.0:
                status_label = f"🛑 {node.upper()} : {activation_val}% [CRÍTICO / ENERGIA BAIXA]"
            else:
                status_label = f"⚙️ {node.upper()} : {activation_val}% [ESTÁVEL]"
                
            st.write(f"**{status_label}**")
            st.progress(int(activation_val))

        # Painel Explicativo da Caixa-Transparente do Grafo
        st.write("---")
        st.markdown("### 🔗 Matriz Sináptica Dinâmica Atual")
        st.json({
            "Ideação -> Inibição de Execução (Sombra de Ar)": st.session_state.synapses[("ideacao", "execucao")],
            "Execução -> Estabilidade (Aterramento Material)": st.session_state.synapses[("execucao", "estabilidade")],
            "Execução -> Inibição de Excesso de Ideação": st.session_state.synapses[("execucao", "ideacao")]
        })

if __name__ == "__main__":
    main()