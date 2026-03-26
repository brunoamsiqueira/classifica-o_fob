import streamlit as st

# ==========================================
# 1. BASE DE DADOS E REGRAS (EXTRAÍDAS DO EXCEL)
# ==========================================

PESOS = {
    "Estrutura": 25,
    "Cobertura": 20,
    "Acabamento Interno": 12,
    "Acabamento Externo": 12,
    "Instalações Elétricas": 7,
    "Instalações Hidráulicas": 7,
    "Pisos": 7,
    "Forro": 5,
    "Idade Real Aproximada": 5
}

OPCOES = {
    "Estrutura": {
        "Estrutura em perfeito estado (sem patologias ou necessidade de intervenção estrutural)": {"classe": "ÓTIMO", "nota": 8},
        "Estrutura íntegra (sem necessidade de reparos estruturais)": {"classe": "MUITO BOM", "nota": 7},
        "Estrutura estável (sem comprometimento estrutural)": {"classe": "BOM", "nota": 6},
        "Estrutura estável (ainda sem necessidade de intervenção estrutural)": {"classe": "INTERMEDIÁRIO", "nota": 5},
        "Estrutura sem necessidade de recuperação (sem intervenção estrutural)": {"classe": "REGULAR", "nota": 4},
        "Estabilização ou recuperação localizada do sistema estrutural (intervenção estrutural pontual)": {"classe": "DEFICIENTE", "nota": 3},
        "Estabilização ou recuperação de grande parte do sistema estrutural (comprometimento estrutural significativo)": {"classe": "RUIM", "nota": 2},
        "Estabilização ou recuperação estrutural significativa (estrutura comprometida)": {"classe": "MUITO RUIM", "nota": 1}
    },
    "Cobertura": {
        "Cobertura em bom estado (sem infiltrações ou falhas)": {"classe": "ÓTIMO", "nota": 8},
        "Cobertura em bom estado (sem necessidade de reparos)": {"classe": "MUITO BOM", "nota": 7},
        "Cobertura em condições normais (sem danos significativos)": {"classe": "BOM", "nota": 6},
        "Possível revisão da cobertura (verificação de telhas e vedação)": {"classe": "INTERMEDIÁRIO", "nota": 5},
        "Revisão necessária (possíveis reparos na impermeabilização ou telhado)": {"classe": "REGULAR", "nota": 4},
        "Revisão da impermeabilização ou substituição parcial de telhas (reparos na cobertura)": {"classe": "DEFICIENTE", "nota": 3},
        "Reparações importantes ou substituição parcial do telhado (problemas relevantes de cobertura)": {"classe": "RUIM", "nota": 2},
        "Substituição da impermeabilização ou do telhado (cobertura sem condições de uso)": {"classe": "MUITO RUIM", "nota": 1}
    },
    "Acabamento Interno": {
        "Sem fissuras ou trincas (alvenaria íntegra)/Apenas sinais de desgaste natural na pintura (manutenção estética)": {"classe": "ÓTIMO", "nota": 8},
        "Sem danos relevantes (alvenaria preservada)/Necessita apenas uma demão leve de pintura (manutenção estética simples)": {"classe": "MUITO BOM", "nota": 7},
        "Eventuais fissuras e trincas superficiais (pequenas manifestações)/Pintura interna necessária (manutenção comum)": {"classe": "BOM", "nota": 6},
        "Fissuras e trincas superficiais (desgaste natural da construção)/ Pintura necessita renovação ": {"classe": "INTERMEDIÁRIO", "nota": 5},
        "Fissuras e trincas superficiais generalizadas e alguns panos de reboco (reparos localizados)/ Pintura interna necessita de restauração do acabamento": {"classe": "REGULAR", "nota": 4},
        "Reparos em fissuras e trincas (correção de patologias na alvenaria)/ Pintura interna (recuperação estética)": {"classe": "DEFICIENTE", "nota": 3},
        "Substituição de panos de regularização da alvenaria (reconstrução parcial)/Pintura interna recuperação geral": {"classe": "RUIM", "nota": 2},
        "Alvenaria Comprometida/Pintura comprometida ou Sem pintura": {"classe": "MUITO RUIM", "nota": 1}
    },
    "Acabamento Externo": {
        "Sem fissuras ou trincas (alvenaria íntegra)/Apenas sinais de desgaste natural na pintura (manutenção estética)": {"classe": "ÓTIMO", "nota": 8},
        "Sem danos relevantes (alvenaria preservada)/Necessita apenas uma demão leve de pintura (manutenção estética simples)": {"classe": "MUITO BOM", "nota": 7},
        "Eventuais fissuras e trincas superficiais (pequenas manifestações)/Pintura interna necessária (manutenção comum)": {"classe": "BOM", "nota": 6},
        "Fissuras e trincas superficiais (desgaste natural da construção)/ Pintura necessita renovação ": {"classe": "INTERMEDIÁRIO", "nota": 5},
        "Fissuras e trincas superficiais generalizadas e alguns panos de reboco (reparos localizados)/ Pintura interna necessita de restauração do acabamento": {"classe": "REGULAR", "nota": 4},
        "Reparos em fissuras e trincas (correção de patologias na alvenaria)/ Pintura interna (recuperação estética)": {"classe": "DEFICIENTE", "nota": 3},
        "Substituição de panos de regularização da alvenaria (reconstrução parcial)/Pintura interna recuperação geral": {"classe": "RUIM", "nota": 2},
        "Pintura comprometida/Sem pintura": {"classe": "MUITO RUIM", "nota": 1}
    },
    "Instalações Elétricas": {
        "Instalações em perfeito funcionamento (sem necessidade de revisão)": {"classe": "ÓTIMO", "nota": 8},
        "Funcionamento normal (instalações operando adequadamente)": {"classe": "MUITO BOM", "nota": 7},
        "Funcionamento normal (instalações adequadas)": {"classe": "BOM", "nota": 6},
        "Eventual revisão do sistema elétrico (manutenção preventiva)": {"classe": "INTERMEDIÁRIO", "nota": 5},
        "Revisão das instalações elétricas (manutenção corretiva)": {"classe": "REGULAR", "nota": 4},
        "Revisão geral com substituição eventual de peças desgastadas (troca de componentes)": {"classe": "DEFICIENTE", "nota": 3},
        "Substituição de peças aparentes (componentes deteriorados)": {"classe": "RUIM", "nota": 2},
        "Substituição completa das instalações (sistemas deteriorados)": {"classe": "MUITO RUIM", "nota": 1}
    },
    "Instalações Hidráulicas": {
        "Instalações em perfeito funcionamento (sem necessidade de revisão)": {"classe": "ÓTIMO", "nota": 8},
        "Funcionamento normal (instalações operando adequadamente)": {"classe": "MUITO BOM", "nota": 7},
        "Funcionamento normal (instalações adequadas)": {"classe": "BOM", "nota": 6},
        "Eventual revisão do sistema hidráulico (manutenção preventiva)": {"classe": "INTERMEDIÁRIO", "nota": 5},
        "Revisão das instalações hidráulicas (manutenção corretiva)": {"classe": "REGULAR", "nota": 4},
        "Revisão geral com substituição eventual de peças desgastadas (troca de componentes)": {"classe": "DEFICIENTE", "nota": 3},
        "Substituição de peças aparentes (componentes deteriorados)": {"classe": "RUIM", "nota": 2},
        "Substituição completa das instalações (sistemas deteriorados)": {"classe": "MUITO RUIM", "nota": 1}
    },
    "Pisos": {
        "Pisos íntegros (sem desgaste relevante)": {"classe": "ÓTIMO", "nota": 8},
        "Pequeno desgaste natural (revestimentos preservados)": {"classe": "MUITO BOM", "nota": 7},
        "Pequenos reparos pontuais (desgaste localizado)": {"classe": "BOM", "nota": 6},
        "Desgaste moderado (necessidade de pequenos reparos)": {"classe": "INTERMEDIÁRIO", "nota": 5},
        "Desgaste visível em alguns ambientes (possível troca parcial)": {"classe": "REGULAR", "nota": 4},
        "Substituição pontual em alguns cômodos (revestimentos deteriorados)": {"classe": "DEFICIENTE", "nota": 3},
        "Substituição da maioria dos pisos (desgaste acentuado)": {"classe": "RUIM", "nota": 2},
        "Substituição generalizada (revestimentos comprometidos)": {"classe": "MUITO RUIM", "nota": 1}
    },
    "Forro": {
        "Forros íntegros (sem desgaste relevante)": {"classe": "ÓTIMO", "nota": 8},
        "Pequeno desgaste natural (forros
