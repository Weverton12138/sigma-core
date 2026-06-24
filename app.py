import streamlit as st
import re
import math
import json

# Configuração da Página Web (Interface Escura / Foco Operacional)
st.set_page_config(
    page_title="ActionOS // Powered by SIGMA v10",
    page_icon="🧠",
    layout="wide"
)

# Estilização CSS para transformar o layout padrão em um Produto Web Premium
st.markdown("""
    <style>
        .stApp { background-color: #080c14; color: #e2e8f0; }
        h1, h2, h3 { font-family: 'Courier New', monospace !important; color: #38bdf8 !important; }
        .diagnostic-box { background-color: #0f172a; border: 1px solid #38bdf8; padding: 20px; border-radius: 6px; margin-top: 15px; box-shadow: 0 0 15px rgba(56, 189, 248, 0.1); }
        .action-order { background-color: #1e1b4b; border-left: 5px solid #6366f1; padding: 15px; border-radius: 4px; font-weight: bold; font-family: 'Courier New', monospace; margin-top: 10px; color: #f472b6; }
        .premium-card { background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%); border: 2px solid #6366f1; padding: 25px; border-radius: 8px; text-align: center; margin-top: 25px; }
        .stButton>button { background-color: #1e293b; color: #38bdf8; border: 1px solid #38bdf8; font-family: 'Courier New', monospace; font-weight: bold; width: 100%; height: 45px; }
        .stButton>button:hover { background-color: #38bdf8; color: #080c14; box-shadow: 0 0 20px #38bdf8; }
        .checkout-btn a { display: block; background: linear-gradient(90deg, #6366f1, #3b82f6); color: white !important; text-align: center; padding: 14px; border-radius: 6px; font-weight: bold; text-decoration: none; font-size: 11pt; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4); }
        .checkout-btn a:hover { transform: scale(1.02); }
    </style>
""", unsafe_allow_html=True)

class SigmaCognitiveGraphV10:
    def __init__(self):
        # Inicializa os nós do grafo se não existirem na sessão atual
        if 'nodes' not in st.session_state:
            st.session_state.nodes = {
                "estabilidade": {"activation": 50.0, "base_decay": 0.12},
                "ideacao": {"activation": 50.0, "base_decay": 0.15},
                "execucao": {"activation": 50.0, "base_decay": 0.18},
                "magnetismo": {"activation": 50.0, "base_decay": 0.10},
                "resistencia": {"activation": 50.0, "base_decay": 0.08}
            }
        # Pesos sinápticos e conexões inibidoras/excitatórias do motor cognitivo
        if 'synapses' not in st.session_state:
            st.session_state.synapses = {
                ("ideacao", "execucao"): -0.35, # Hiper-ideação esmaga a execução física
                ("execucao", "estabilidade"): 0.40,
                ("resistencia", "execucao"): 0.35,
                ("execucao", "ideacao"): -0.30
            }
        # Dicionário de pesos léxicos para análise de texto
        self.lexicon = {
            "estabilidade": {"calmo": 2.5, "ansioso": -2.0, "rotina": 1.8, "medo": -2.5, "foco": 2.0},
            "ideacao": {"ia": 3.0, "agi": 3.5, "sistema": 1.5, "criar": 2.0, "complexo": 2.5, "planejar": 1.5, "arquitetura": 2.0},
            "execucao": {"fazer": 1.5, "código": 2.5, "executar": 3.0, "entregar": 3.5, "build": 2.5, "programar": 2.0, "ide": 1.5},
            "magnetismo": {"liderar": 2.5, "pessoas": 1.5, "vender": 2.5, "influenciar": 2.0},
            "resistencia": {"persistir": 3.0, "continuar": 2.0, "aguentar": 2.5, "falhar": -1.5}
        }

    def _activation_function(self, x: float) -> float:
        # Função sigmóide para normalizar ativações entre 0% e 100%
        return round(100.0 / (1.0 + math.exp(-0.08 * (x - 50.0))), 2)

    def process_cycle(self, input_text: str, external_grounding: bool = False):
        clean_text = input_text.lower()
        words = re.findall(r'\w+', clean_text)
        
        # Injeção de forças de entrada baseada no texto do usuário
        input_injection = {node: 0.0 for node in st.session_state.nodes}
        for word in words:
            for node in st.session_state.nodes:
                if word in self.lexicon[node]:
                    input_injection[node] += self.lexicon[node][word]
        
        current_activations = {node: st.session_state.nodes[node]["activation"] for node in st.session_state.nodes}
        
        # Processamento de dinâmica de grafos
        for target_node in st.session_state.nodes:
            meta = st.session_state.nodes[target_node]
            decay = current_activations[target_node] * meta["base_decay"]
            
            synaptic_influence = 0.0
            for (source, target), weight in st.session_state.synapses.items():
                if target == target_node and current_activations[source] > 20.0:
                    synaptic_influence += (current_activations[source] * weight)
            
            # Bônus caso o usuário marque que está com o ambiente de desenvolvimento ativo
            grounding_bonus = 22.0 if (external_grounding and target_node in ["execucao", "resistencia"]) else 0.0
            
            net_force = current_activations[target_node] - decay + (input_injection[target_node] * 5.0) + (synaptic_influence * 0.5) + grounding_bonus
            st.session_state.nodes[target_node]["activation"] = self._activation_function(net_force)

def main():
    st.title("🧠 ActionOS // Powered by SIGMA v10")
    st.subheader("O motor analítico focado em quebrar a inércia e forçar a execução prática.")
    st.write("---")

    engine = SigmaCognitiveGraphV10()
    col_control, col_telemetry = st.columns([1, 1.2])

    with col_control:
        st.markdown("### 📥 Auditoria de Estado Atual")
        user_text = st.text_area(
            "Descreva detalhadamente o que você está planejando, codificando ou o que está bloqueando seu progresso material:",
            placeholder="Exemplo: Estou cheio de ideias para um novo microsserviço, mas não sei por onde começar a codificar a API e acabo revisando a arquitetura...",
            height=130
        )
        
        grounding = st.checkbox("🔥 Ambiente de Produção / IDE aberta no monitor")
        
        if st.button("🔴 CALCULAR TENSORES COGNITIVOS"):
            engine.process_cycle(user_text, external_grounding=grounding)
            st.rerun()

        # MÓDULO DE DIAGNÓSTICO DO PRODUTO WEB
        st.markdown("<div class='diagnostic-box'>", unsafe_allow_html=True)
        st.markdown("### 🔍 Diagnóstico Operacional do Sistema")
        
        ideation_val = st.session_state.nodes["ideacao"]["activation"]
        execution_val = st.session_state.nodes["execucao"]["activation"]
        stability_val = st.session_state.nodes["estabilidade"]["activation"]

        if ideation_val > 70.0 and execution_val < 45.0:
            st.error("⚠️ ANOMALIA: LOOP DE HIPER-IDEAÇÃO (PARÁLISE)")
            st.write("Seu nível de processamento abstrato está sufocando a mecânica de entrega. Você está refinando cenários teóricos para mascarar a resistência de testar o código no mundo real.")
            st.markdown("<div class='action-order'>ORDEM DO SISTEMA: Interrompa o planejamento. Escreva um script bruto de teste com apenas 10 linhas. Force o primeiro erro de execução hoje.</div>", unsafe_allow_html=True)
        elif stability_val < 35.0:
            st.warning("⚠️ ALERTA: SUBSISTEMA DE ESTABILIDADE EM DESENCAIXE")
            st.write("A instabilidade de foco está pulverizando a energia dos seus nós. Tentar atacar uma meta muito grande está gerando ansiedade operacional.")
            st.markdown("<div class='action-order'>ORDEM DO SISTEMA: Reduza o escopo do projeto em 80%. Defina apenas uma única função para finalizar nas próximas 2 horas.</div>", unsafe_allow_html=True)
        else:
            st.success("✅ COMPORTAMENTO EM EQUILÍBRIO SINÁPTICO")
            st.write("Os níveis de ideação técnica e tração física estão balanceados. O fluxo está convergindo para entregas estáveis e limpas.")
            st.markdown("<div class='action-order'>ORDEM DO SISTEMA: Mantenha o ritmo atual de build. Não mude a pilha de tecnologia até concluir este ciclo.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        #ÁREA DE CONVERSÃO PREMIUM DO MICROSaaS
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.markdown("### 💎 UPGRADE: PLANO DE ANÁLISE PERSISTENTE")
        st.write("Desbloqueie o histórico semanal em banco de dados, telemetria de evolução de foco e relatórios profundos de performance de engenharia.")
        st.markdown("""
            <div class='checkout-btn'>
                <a href='#' target='_blank'>🚀 ADQUIRIR ACESSO PRO — R$ 19,90/mês</a>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_telemetry:
        st.markdown("### 📊 Monitoramento de Carga Latente")
        
        for node, data in st.session_state.nodes.items():
            val = data["activation"]
            tag = " [🔥 SATURAÇÃO]" if val > 75.0 else " [🛑 INÉRCIA]" if val < 30.0 else " [⚙️ TRAÇÃO]"
            st.write(f"**{node.upper()} : {val}%** {tag}")
            st.progress(int(val))
            
        st.write("---")
        st.markdown("### 🧬 Vetores de Análise Linear (JSON)")
        st.json({
            "Diferencial Pensar vs Fazer": round(ideation_val - execution_val, 2),
            "Desvio Base de Estabilidade": round(stability_val - 50.0, 2),
            "Reserva de Elasticidade Operacional": st.session_state.nodes["resistencia"]["activation"]
        })

if __name__ == "__main__":
    main()
