from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PASTA_GRAFICOS = Path("graficos")

plt.style.use("seaborn-v0_8-whitegrid")


def garantir_pasta_graficos() -> None:
    PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)


def _ordenar_grupos(df: pd.DataFrame) -> pd.DataFrame:
    ordem = [
        "0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39",
        "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80+",
    ]
    return df.assign(grupo_etario=pd.Categorical(df["grupo_etario"], categories=ordem, ordered=True)).sort_values("grupo_etario")


def gerar_piramide_etaria(df: pd.DataFrame, ano: int, nome_arquivo: str) -> Path:
    garantir_pasta_graficos()
    dados = _ordenar_grupos(df[df["ano"] == ano].copy())
    resumo = dados.pivot_table(index="grupo_etario", columns="sexo", values="populacao", aggfunc="sum", fill_value=0)
    ordem = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80+"]
    resumo = resumo.reindex(index=ordem, fill_value=0)

    homens = -resumo.get("Masculino", pd.Series(dtype=float))
    mulheres = resumo.get("Feminino", pd.Series(dtype=float))

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(resumo.index, homens, color="#4C78A8", label="Homens")
    ax.barh(resumo.index, mulheres, color="#F58518", label="Mulheres")
    ax.set_title(f"Pirâmide etária do Distrito Federal - {ano}")
    ax.set_xlabel("População")
    ax.set_ylabel("Grupo etário")
    ax.legend()
    ax.axvline(0, color="black", linewidth=0.8)
    ax.text(0.5, -0.08, "Fonte: IBGE/SIDRA", transform=ax.transAxes, ha="center", fontsize=9)
    plt.tight_layout()
    caminho = PASTA_GRAFICOS / nome_arquivo
    fig.savefig(caminho, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return caminho


def gerar_distribuicao_percentual(df: pd.DataFrame, nome_arquivo: str) -> Path:
    garantir_pasta_graficos()
    resumo = df.groupby(["ano", "grupo_etario"], as_index=False)["populacao"].sum()
    resumo["percentual"] = resumo.groupby("ano")["populacao"].transform(lambda s: (s / s.sum()) * 100)

    fig, ax = plt.subplots(figsize=(12, 6))
    for ano in sorted(resumo["ano"].unique()):
        dados = resumo[resumo["ano"] == ano]
        ax.plot(dados["grupo_etario"], dados["percentual"], marker="o", label=str(ano))
    ax.set_title("Distribuição percentual por grupos etários")
    ax.set_xlabel("Grupo etário")
    ax.set_ylabel("Percentual da população")
    ax.legend(title="Ano")
    plt.xticks(rotation=45)
    plt.tight_layout()
    caminho = PASTA_GRAFICOS / nome_arquivo
    fig.savefig(caminho, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return caminho


def gerar_barra_jovens_adultos_idosos(df_indicadores: pd.DataFrame, nome_arquivo: str) -> Path:
    garantir_pasta_graficos()
    categorias = ["0_14", "15_64", "65_mais"]
    labels = ["Jovens", "Adultos", "Idosos"]
    fig, ax = plt.subplots(figsize=(10, 6))
    largura = 0.35
    anos = df_indicadores["ano"].tolist()
    x = range(len(categorias))
    for idx, ano in enumerate(anos):
        linha = df_indicadores[df_indicadores["ano"] == ano].iloc[0]
        valores = [linha["percentual_jovens"], linha["percentual_adultos"], linha["percentual_idosos"]]
        deslocamento = [pos + (idx * largura) - (largura / 2) for pos in x]
        ax.bar(deslocamento, valores, width=largura, label=str(ano))
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_title("Jovens, adultos e idosos no Distrito Federal")
    ax.set_ylabel("Percentual")
    ax.legend(title="Ano")
    plt.tight_layout()
    caminho = PASTA_GRAFICOS / nome_arquivo
    fig.savefig(caminho, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return caminho


def gerar_razao_sexo_por_grupo_etario(df: pd.DataFrame, nome_arquivo: str) -> Path:
    garantir_pasta_graficos()
    dados = df.copy()
    ordem = [
        "0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39",
        "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80+",
    ]
    fig, ax = plt.subplots(figsize=(12, 6))
    for ano in sorted(dados["ano"].unique()):
        sub = dados[dados["ano"] == ano].copy()
        sub["grupo_etario"] = pd.Categorical(sub["grupo_etario"], categories=ordem, ordered=True)
        sub = sub.sort_values("grupo_etario")
        ax.plot(sub["grupo_etario"], sub["razao_sexo"], marker="o", label=str(ano))
    ax.set_title("Razão de sexo por grupo etário")
    ax.set_xlabel("Grupo etário")
    ax.set_ylabel("Homens por 100 mulheres")
    ax.legend(title="Ano")
    plt.xticks(rotation=45)
    plt.tight_layout()
    caminho = PASTA_GRAFICOS / nome_arquivo
    fig.savefig(caminho, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return caminho
