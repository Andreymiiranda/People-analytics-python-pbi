# =============================================================================
# TRATAMENTO DE DADOS — BASE RH
# =============================================================================

import pandas as pd
import os

ENTRADA = "./"
SAIDA   = "./dados_tratados/"
os.makedirs(SAIDA, exist_ok=True)

pd.set_option("display.max_columns", None)


# ── FUNÇÕES UTILITÁRIAS ───────────────────────────────────────────────────────

def ler(arquivo):
    df = pd.read_csv(os.path.join(ENTRADA, arquivo), encoding="utf-8-sig")
    print(f"\n{'='*55}\n{arquivo}  →  {df.shape[0]} linhas | {df.shape[1]} colunas")
    nulos = df.isnull().sum()
    nulos = nulos[nulos > 0]
    if not nulos.empty:
        for col, n in nulos.items():
            print(f"  ⚠  {col}: {n} nulos ({n/len(df):.1%})")
    return df

def salvar(df, arquivo):
    # Correção: Adicionado sep=';' e decimal=',' para compatibilidade com Excel BR
    df.to_csv(os.path.join(SAIDA, arquivo), index=False, encoding="utf-8-sig", sep=";", decimal=",")
    print(f"  💾 Salvo: {arquivo}  →  {df.shape[0]} linhas | {df.shape[1]} colunas")

def remover_duplicatas(df, subset):
    antes = len(df)
    df = df.drop_duplicates(subset=subset, keep="first")
    print(f"  🔁 Duplicatas removidas: {antes - len(df)}")
    return df

def preencher_com_mediana(df, col, grupo=None):
    """Preenche nulos com mediana do grupo; fallback = mediana geral."""
    if grupo:
        df[col] = df[col].fillna(df.groupby(grupo)[col].transform("median"))
    df[col] = df[col].fillna(df[col].median())
    return df

def converter_datas(df, colunas):
    for col in colunas:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    return df

def strip_texto(df):
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    return df


# ── 1. FUNCIONÁRIOS ───────────────────────────────────────────────────────────

df = ler("funcionarios.csv")
df = remover_duplicatas(df, subset=["ID_Funcionario"])
df = converter_datas(df, ["Data_Admissao", "Data_Desligamento"])

# Ativos com desligamento indevido → limpar
mask = (df["Status"] == "Ativo") & df["Data_Desligamento"].notnull()
print(f"  🔧 Ativos com desligamento indevido: {mask.sum()} → corrigidos")
df.loc[mask, ["Data_Desligamento", "Motivo_Desligamento"]] = None

# Correção: Limpa os pontos e vírgulas da string antes de converter para número
if df["Salario_Bruto"].dtype == "object":
    df["Salario_Bruto"] = (
        df["Salario_Bruto"]
        .astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
    )

# Garante que Salario_Bruto é numérico com 2 casas decimais
df["Salario_Bruto"] = pd.to_numeric(df["Salario_Bruto"], errors="coerce").round(2)
print(f"  💰 Salário mín: {df['Salario_Bruto'].min():.2f} | máx: {df['Salario_Bruto'].max():.2f} | média: {df['Salario_Bruto'].mean():.2f}")

# Campos obrigatórios nulos
df["flag_admissao_ausente"]   = df["Data_Admissao"].isnull()
df["flag_avaliacao_imputada"] = (df["Status"] == "Ativo") & df["Avaliacao_Desempenho"].isnull()
df = preencher_com_mediana(df, "Salario_Bruto",        grupo="Cargo")
df = preencher_com_mediana(df, "Avaliacao_Desempenho", grupo="Departamento")
df = strip_texto(df)

salvar(df, "funcionarios_tratado.csv")


# ── 2. AVALIAÇÕES DE DESEMPENHO ───────────────────────────────────────────────

df = ler("avaliacoes_desempenho.csv")
df = remover_duplicatas(df, subset=["ID_Avaliacao", "ID_Funcionario", "Periodo"])

antes = len(df)
df = df.dropna(subset=["ID_Funcionario"])
print(f"  🗑  Sem ID_Funcionario removidos: {antes - len(df)}")

fora = (~df["Nota_Geral"].between(1, 5)).sum()
print(f"  ⭐ Notas fora de [1-5]: {fora} → clip aplicado")
df["Nota_Geral"] = df["Nota_Geral"].clip(1.0, 5.0)

df["Observacao"] = df["Observacao"].fillna("Sem observação registrada")

# Colunas de tempo para o Power BI
df["Ano"]      = df["Periodo"].str[:4].astype(int)
df["Semestre"] = df["Periodo"].str[-1].astype(int)
df["Data_Referencia"] = pd.to_datetime(
    df.apply(lambda r: f"{r['Ano']}-{'06-30' if r['Semestre']==1 else '12-31'}", axis=1)
)

salvar(df, "avaliacoes_desempenho_tratado.csv")


# ── 3. TREINAMENTOS ───────────────────────────────────────────────────────────

df = ler("treinamentos.csv")
df = converter_datas(df, ["Data_Inicio", "Data_Fim"])

mask = (df["Status"] != "Concluído") & df["Nota_Final"].notnull()
print(f"  📝 Notas indevidas (não concluídos): {mask.sum()} → removidas")
df.loc[mask, "Nota_Final"] = None

df = preencher_com_mediana(df, "Carga_Horaria_h", grupo="Nome_Treinamento")
df["Carga_Horaria_h"] = df["Carga_Horaria_h"].astype(int)

df["Duracao_Dias"]       = (df["Data_Fim"] - df["Data_Inicio"]).dt.days
df["flag_data_invalida"] = df["Duracao_Dias"].apply(lambda x: pd.notnull(x) and x <= 0)

salvar(df, "treinamentos_tratado.csv")


# ── 4. ABSENTEÍSMO ────────────────────────────────────────────────────────────

df = ler("absenteismo.csv")

antes = len(df)
df = df.dropna(subset=["ID_Funcionario"])
print(f"  🗑  Sem ID_Funcionario removidos: {antes - len(df)}")

df = converter_datas(df, ["Data_Ausencia"])
df["flag_data_invalida"]     = df["Data_Ausencia"].isnull()
df["flag_qtd_dias_suspeita"] = df["Qtd_Dias"].apply(lambda x: pd.notnull(x) and not (1 <= x <= 90))
df["CID"] = df["CID"].fillna("Não Informado")

salvar(df, "absenteismo_tratado.csv")


# ── 5. RECRUTAMENTO ───────────────────────────────────────────────────────────

df = ler("recrutamento_vagas.csv")
df = converter_datas(df, ["Data_Abertura", "Data_Fechamento"])

mask = df["Candidatos_Entrevistados"] > df["Candidatos_Recebidos"]
print(f"  👥 Funil impossível: {mask.sum()} → corrigidos")
df["flag_funil_corrigido"] = mask
df.loc[mask, "Candidatos_Entrevistados"] = df.loc[mask, "Candidatos_Recebidos"]

df = preencher_com_mediana(df, "Salario_Ofertado", grupo="Cargo")
df["Salario_Ofertado"] = df["Salario_Ofertado"].round(2)

df["SLA_Calculado_Dias"] = (df["Data_Fechamento"] - df["Data_Abertura"]).dt.days
df["flag_sla_invalido"]  = df["SLA_Calculado_Dias"].apply(lambda x: pd.notnull(x) and x < 0)
print(f"  📅 SLA inválido (fechamento < abertura): {df['flag_sla_invalido'].sum()}")

salvar(df, "recrutamento_vagas_tratado.csv")


# ── RESUMO FINAL ──────────────────────────────────────────────────────────────

print(f"\n{'='*55}")
print("✅ Tratamento concluído! Arquivos em:", SAIDA)