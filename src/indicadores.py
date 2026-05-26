from __future__ import annotations

from pathlib import Path

import pandas as pd

PASTA_TRATADOS = Path("dados/tratados")


def calcular_indicadores_por_ano(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        raise ValueError(
            "A base tratada ficou vazia. Verifique se o download do SIDRA "
            "retornou sexo e idade corretamente para as tabelas 3107 e 9514."
        )
    registros = []
    for ano, grupo in df.groupby("ano"):
        total = int(grupo["populacao"].sum())
        homens = int(grupo.loc[grupo["sexo"] == "Masculino", "populacao"].sum())
        mulheres = int(grupo.loc[grupo["sexo"] == "Feminino", "populacao"].sum())

        jovem = int(grupo.loc[grupo["idade"] <= 14, "populacao"].sum())
        adulto = int(grupo.loc[(grupo["idade"] >= 15) & (grupo["idade"] <= 64), "populacao"].sum())
        idoso = int(grupo.loc[grupo["idade"] >= 65, "populacao"].sum())

        def pct(valor: int) -> float:
            return round((valor / total) * 100, 2) if total else 0.0

        def pct_base(valor: int, base: int) -> float:
            return round((valor / base) * 100, 2) if base else 0.0

        registros.append(
            {
                "ano": int(ano),
                "uf": "Distrito Federal",
                "codigo_uf": 53,
                "populacao_total": total,
                "populacao_masculina": homens,
                "populacao_feminina": mulheres,
                "percentual_masculino": pct_base(homens, total),
                "percentual_feminino": pct_base(mulheres, total),
                "razao_sexo": round((homens / mulheres) * 100, 2) if mulheres else 0.0,
                "populacao_0_14": jovem,
                "populacao_15_64": adulto,
                "populacao_65_mais": idoso,
                "percentual_jovens": pct(jovem),
                "percentual_adultos": pct(adulto),
                "percentual_idosos": pct(idoso),
                "indice_envelhecimento": round((idoso / jovem) * 100, 2) if jovem else 0.0,
                "razao_dependencia": round(((jovem + idoso) / adulto) * 100, 2) if adulto else 0.0,
            }
        )

    resultado = pd.DataFrame(registros)
    if resultado.empty:
        raise ValueError("Não foi possível calcular indicadores porque não há registros válidos.")
    return resultado.sort_values("ano")


def calcular_razao_sexo_por_grupo_etario(df: pd.DataFrame) -> pd.DataFrame:
    resumo = (
        df.pivot_table(index=["ano", "grupo_etario"], columns="sexo", values="populacao", aggfunc="sum", fill_value=0)
        .reset_index()
    )
    resumo["razao_sexo"] = resumo.apply(
        lambda linha: round((linha.get("Masculino", 0) / linha.get("Feminino", 0)) * 100, 2)
        if linha.get("Feminino", 0)
        else 0.0,
        axis=1,
    )
    return resumo


def salvar_indicadores(df_indicadores: pd.DataFrame) -> Path:
    caminho = PASTA_TRATADOS / "indicadores_df_2010_2022.csv"
    df_indicadores.to_csv(caminho, index=False, encoding="utf-8-sig")
    return caminho
