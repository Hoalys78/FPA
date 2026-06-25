# ============================================================
# ETL - Dashboard FP&A | Financial Sample
# Autor: [Seu Nome]
# Descricao: Limpeza, tratamento e geracao de tabela Budget
# ============================================================

import pandas as pd
import numpy as np
import os

# ── Configuracao de caminhos ─────────────────────────────────
RAW_PATH       = "data/raw/financial_sample.xlsx"
PROCESSED_PATH = "data/processed/"
os.makedirs(PROCESSED_PATH, exist_ok=True)


# ============================================================
# BLOCO 1 — CARGA E INSPECAO INICIAL
# ============================================================

df = pd.read_excel(RAW_PATH)

print("=== INSPECAO INICIAL ===")
print(f"Shape: {df.shape}")
print(f"\nColunas:\n{df.dtypes}")
print(f"\nValores nulos:\n{df.isnull().sum()}")
print(f"\nPrimeiras linhas:\n{df.head()}")


# ============================================================
# BLOCO 2 — LIMPEZA DE DADOS
# ============================================================

# 2.1 Remover duplicatas
antes = len(df)
df.drop_duplicates(inplace=True)
print(f"\nDuplicatas removidas: {antes - len(df)}")

# 2.2 Padronizar nomes de colunas (sem espacos, snake_case)
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace(r"[^a-z0-9_]", "", regex=True)
)

# 2.3 Tratar valores nulos numericos com mediana
num_cols = df.select_dtypes(include="number").columns
df[num_cols] = df[num_cols].fillna(df[num_cols].median())

# 2.4 Padronizar colunas de texto
str_cols = df.select_dtypes(include="object").columns
for col in str_cols:
    df[col] = df[col].str.strip().str.title()

# 2.5 Garantir tipos corretos
df["units_sold"]          = df["units_sold"].astype(int)
df["manufacturing_price"] = pd.to_numeric(df["manufacturing_price"], errors="coerce")
df["sale_price"]          = pd.to_numeric(df["sale_price"],          errors="coerce")
df["gross_sales"]         = pd.to_numeric(df["gross_sales"],         errors="coerce")
df["discounts"]           = pd.to_numeric(df["discounts"],           errors="coerce")
df["sales"]               = pd.to_numeric(df["sales"],               errors="coerce")
df["cogs"]                = pd.to_numeric(df["cogs"],                errors="coerce")
df["profit"]              = pd.to_numeric(df["profit"],              errors="coerce")

print("\n=== APOS LIMPEZA ===")
print(f"Shape final: {df.shape}")
print(f"Nulos restantes:\n{df.isnull().sum()}")


# ============================================================
# BLOCO 3 — COLUNAS CALCULADAS (KPIs)
# ============================================================

# Margem bruta %
df["margem_bruta_pct"] = (df["profit"] / df["sales"]).replace([np.inf, -np.inf], 0).round(4)

# Ticket medio por unidade
df["ticket_medio"] = (df["sales"] / df["units_sold"]).round(2)

# Desconto % sobre gross sales
df["desconto_pct"] = (df["discounts"] / df["gross_sales"]).replace([np.inf, -np.inf], 0).round(4)

# Coluna de data completa (primeiro dia do mes)
df["data"] = pd.to_datetime(
    df["year"].astype(str) + "-" + df["month_number"].astype(str).str.zfill(2) + "-01"
)

# Trimestre
df["trimestre"] = df["data"].dt.quarter.map({1:"Q1", 2:"Q2", 3:"Q3", 4:"Q4"})

# Semestre
df["semestre"] = df["data"].dt.month.apply(lambda m: "S1" if m <= 6 else "S2")

print("\n=== COLUNAS CALCULADAS ===")
print(df[["sales","profit","margem_bruta_pct","ticket_medio","trimestre"]].describe())


# ============================================================
# BLOCO 4 — TABELA DE BUDGET SIMULADA
# ============================================================
# Logica: Budget = media mensal real por (segment + country + product)
#         com crescimento aplicado de 5% a 15%

np.random.seed(42)

# Calcula media mensal real por grupo
budget_base = (
    df.groupby(["segment", "country", "product", "year"])
    .agg(sales_media=("sales", "mean"), profit_media=("profit", "mean"))
    .reset_index()
)

# Cria tabela Budget com todos os meses
meses = list(range(1, 13))
budget_rows = []

for _, row in budget_base.iterrows():
    for mes in meses:
        crescimento = np.random.uniform(1.05, 1.15)   # meta 5% a 15% acima
        budget_rows.append({
            "segment":        row["segment"],
            "country":        row["country"],
            "product":        row["product"],
            "year":           row["year"],
            "month_number":   mes,
            "budget_sales":   round(row["sales_media"]  * crescimento, 2),
            "budget_profit":  round(row["profit_media"] * crescimento, 2),
        })

df_budget = pd.DataFrame(budget_rows)
df_budget["data"] = pd.to_datetime(
    df_budget["year"].astype(str) + "-" +
    df_budget["month_number"].astype(str).str.zfill(2) + "-01"
)

print(f"\n=== TABELA BUDGET ===")
print(f"Shape: {df_budget.shape}")
print(df_budget.head())


# ============================================================
# BLOCO 5 — TABELA CALENDARIO
# ============================================================

datas = pd.date_range(start="2013-01-01", end="2014-12-31", freq="D")
df_calendario = pd.DataFrame({"data": datas})
df_calendario["ano"]          = df_calendario["data"].dt.year
df_calendario["mes_numero"]   = df_calendario["data"].dt.month
df_calendario["mes_nome"]     = df_calendario["data"].dt.strftime("%B")
df_calendario["mes_abrev"]    = df_calendario["data"].dt.strftime("%b")
df_calendario["trimestre"]    = df_calendario["data"].dt.quarter.map({1:"Q1",2:"Q2",3:"Q3",4:"Q4"})
df_calendario["semestre"]     = df_calendario["mes_numero"].apply(lambda m: "S1" if m<=6 else "S2")
df_calendario["dia_semana"]   = df_calendario["data"].dt.day_name()
df_calendario["ano_mes"]      = df_calendario["data"].dt.strftime("%Y-%m")
df_calendario["ano_trim"]     = df_calendario["data"].dt.year.astype(str) + "-" + \
                                 df_calendario["trimestre"]

print(f"\n=== TABELA CALENDARIO ===")
print(f"Shape: {df_calendario.shape}")
print(df_calendario.head())


# ============================================================
# BLOCO 6 — EXPORTACAO
# ============================================================

df.to_excel(            PROCESSED_PATH + "ft_vendas.xlsx",    index=False)
df_budget.to_excel(     PROCESSED_PATH + "ft_budget.xlsx",    index=False)
df_calendario.to_excel( PROCESSED_PATH + "dim_calendario.xlsx", index=False)

print("\n=== EXPORTACAO CONCLUIDA ===")
print(f"  ft_vendas.xlsx    → {len(df)} linhas")
print(f"  ft_budget.xlsx    → {len(df_budget)} linhas")
print(f"  dim_calendario.xlsx → {len(df_calendario)} linhas")
print("\nETL finalizado com sucesso!")
