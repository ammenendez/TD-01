from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from baixar_dados import baixar_todos_os_dados
from graficos import (
    gerar_barra_jovens_adultos_idosos,
    gerar_distribuicao_percentual,
    gerar_piramide_etaria,
    gerar_razao_sexo_por_grupo_etario,
)
from indicadores import calcular_indicadores_por_ano, calcular_razao_sexo_por_grupo_etario, salvar_indicadores
from tratar_dados import salvar_dados_tratados, tratar_todos_os_dados


def gerar_tabelas_comparativas(df_tratado: pd.DataFrame, df_indicadores: pd.DataFrame) -> None:
    tabela_idade = (
        df_tratado.groupby(["ano", "grupo_etario"], as_index=False)["populacao"].sum().pivot(
            index="grupo_etario", columns="ano", values="populacao"
        )
    )
    salvar_dados_tratados(tabela_idade.reset_index(), "tabela_comparativa_grupos_etarios.csv")
    salvar_dados_tratados(df_indicadores, "tabela_indicadores_comparativos.csv")


def executar_fluxo(atualizar: bool = False) -> None:
    caminhos = baixar_todos_os_dados(atualizar=atualizar)
    df_tratado = tratar_todos_os_dados(caminhos["2022"])

    df_indicadores = calcular_indicadores_por_ano(df_tratado)
    salvar_indicadores(df_indicadores)
    gerar_tabelas_comparativas(df_tratado, df_indicadores)

    df_razao = calcular_razao_sexo_por_grupo_etario(df_tratado)

    gerar_piramide_etaria(df_tratado, 2022, "piramide_etaria_df_2022.png")
    gerar_distribuicao_percentual(df_tratado, "distribuicao_percentual_grupos_etarios_2022.png")
    gerar_barra_jovens_adultos_idosos(df_indicadores, "jovens_adultos_idosos_2022.png")
    gerar_razao_sexo_por_grupo_etario(df_razao, "razao_sexo_por_grupo_etario.png")


def main() -> None:
    parser = argparse.ArgumentParser(description="Análise da população do Distrito Federal por sexo e idade.")
    parser.add_argument("--atualizar", action="store_true", help="Força o novo download dos dados.")
    args = parser.parse_args()
    executar_fluxo(atualizar=args.atualizar)


if __name__ == "__main__":
    main()
