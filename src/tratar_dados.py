from __future__ import annotations

from pathlib import Path

import pandas as pd

PASTA_TRATADOS = Path("dados/tratados")

GRUPOS_ETARIOS = [
    "0-4",
    "5-9",
    "10-14",
    "15-19",
    "20-24",
    "25-29",
    "30-34",
    "35-39",
    "40-44",
    "45-49",
    "50-54",
    "55-59",
    "60-64",
    "65-69",
    "70-74",
    "75-79",
    "80+",
]

def garantir_pasta_tratados() -> None:
    PASTA_TRATADOS.mkdir(parents=True, exist_ok=True)


def _faixa_para_grupo_etario(faixa: str) -> str:
    texto = str(faixa).strip().lower()
    if "100 anos ou mais" in texto:
        return "80+"
    if "95 a 99" in texto or "90 a 94" in texto or "85 a 89" in texto or "80 a 84" in texto:
        return "80+"
    if "75 a 79" in texto:
        return "75-79"
    if "70 a 74" in texto:
        return "70-74"
    if "65 a 69" in texto:
        return "65-69"
    if "60 a 64" in texto:
        return "60-64"
    if "55 a 59" in texto:
        return "55-59"
    if "50 a 54" in texto:
        return "50-54"
    if "45 a 49" in texto:
        return "45-49"
    if "40 a 44" in texto:
        return "40-44"
    if "35 a 39" in texto:
        return "35-39"
    if "30 a 34" in texto:
        return "30-34"
    if "25 a 29" in texto:
        return "25-29"
    if "20 a 24" in texto:
        return "20-24"
    if "15 a 19" in texto:
        return "15-19"
    if "10 a 14" in texto:
        return "10-14"
    if "5 a 9" in texto:
        return "5-9"
    if "0 a 4" in texto:
        return "0-4"
    return pd.NA


def _faixa_para_idade_inicial(faixa: str) -> int | pd.NA:
    texto = str(faixa).strip().lower()
    mapa = {
        "0 a 4": 0,
        "5 a 9": 5,
        "10 a 14": 10,
        "15 a 19": 15,
        "20 a 24": 20,
        "25 a 29": 25,
        "30 a 34": 30,
        "35 a 39": 35,
        "40 a 44": 40,
        "45 a 49": 45,
        "50 a 54": 50,
        "55 a 59": 55,
        "60 a 64": 60,
        "65 a 69": 65,
        "70 a 74": 70,
        "75 a 79": 75,
        "80 a 84": 80,
        "85 a 89": 80,
        "90 a 94": 80,
        "95 a 99": 80,
        "100 anos ou mais": 80,
    }
    for chave, valor in mapa.items():
        if chave in texto:
            return valor
    return pd.NA


def tratar_arquivo_bruto(caminho_bruto: Path, ano: int) -> pd.DataFrame:
    df = pd.read_csv(caminho_bruto, dtype=str)

    colunas = {coluna.strip().lower(): coluna for coluna in df.columns}
    coluna_uf = next((col for nome, col in colunas.items() if "unidade da federação" in nome and "(código)" not in nome), None)
    coluna_sexo = next((col for nome, col in colunas.items() if nome == "sexo"), None)
    coluna_idade = next((col for nome, col in colunas.items() if nome == "idade"), None)
    coluna_valor = next((col for nome, col in colunas.items() if nome == "valor"), None)

    if not all([coluna_uf, coluna_sexo, coluna_idade, coluna_valor]):
        raise ValueError(
            "Não foi possível identificar as colunas esperadas no CSV bruto. "
            "Verifique se o arquivo é a exportação tabular do SIDRA."
        )

    df = df[df[coluna_sexo].isin(["Homens", "Mulheres"])].copy()
    df = df[df[coluna_idade].ne("Total")].copy()
    df["grupo_etario"] = df[coluna_idade].map(_faixa_para_grupo_etario)
    df = df[df["grupo_etario"].notna()].copy()

    df["sexo"] = df[coluna_sexo].map({"Homens": "Masculino", "Mulheres": "Feminino"})
    df["populacao"] = pd.to_numeric(df[coluna_valor], errors="coerce").fillna(0).astype(int)
    df["idade"] = df[coluna_idade].map(_faixa_para_idade_inicial)
    df["ano"] = ano
    df["uf"] = df[coluna_uf].fillna("Distrito Federal")
    df["codigo_uf"] = 53

    registros = df[["ano", "uf", "codigo_uf", "sexo", "idade", "grupo_etario", "populacao"]].copy()
    registros = registros.dropna(subset=["idade"]).copy()
    registros["idade"] = registros["idade"].astype(int)

    if registros.empty:
        raise ValueError("A base tratada ficou vazia ao processar o arquivo bruto exportado.")
    return registros.sort_values(["sexo", "idade"]).reset_index(drop=True)


def tratar_dados_2022(caminho_bruto: Path) -> pd.DataFrame:
    return tratar_arquivo_bruto(caminho_bruto, 2022)


def tratar_dados_2010(caminho_bruto: Path) -> pd.DataFrame:
    df = pd.read_csv(caminho_bruto, dtype=str)

    coluna_uf = next((col for col in df.columns if "Unidade da Federação" in col and "(Código)" not in col), None)
    coluna_sexo = next((col for col in df.columns if col == "Sexo"), None)
    coluna_idade = next((col for col in df.columns if "Grupo de idade" in col and "(Código)" not in col), None)
    coluna_valor = next((col for col in df.columns if col == "Valor"), None)
    coluna_situacao = next((col for col in df.columns if "Situação do domicílio" in col and "(Código)" not in col), None)

    if not all([coluna_uf, coluna_sexo, coluna_idade, coluna_valor, coluna_situacao]):
        raise ValueError("Não foi possível identificar as colunas esperadas no CSV de 2010.")

    df = df[df[coluna_situacao].eq("Total")].copy()
    df = df[df[coluna_sexo].isin(["Homens", "Mulheres"])].copy()
    df = df[df[coluna_idade].ne("Total")].copy()
    df["grupo_etario"] = df[coluna_idade].map(_faixa_para_grupo_etario)
    df = df[df["grupo_etario"].notna()].copy()

    df["sexo"] = df[coluna_sexo].map({"Homens": "Masculino", "Mulheres": "Feminino"})
    df["populacao"] = pd.to_numeric(df[coluna_valor], errors="coerce").fillna(0).astype(int)
    df["idade"] = df[coluna_idade].map(_faixa_para_idade_inicial)
    df["ano"] = 2010
    df["uf"] = df[coluna_uf].fillna("Distrito Federal")
    df["codigo_uf"] = 53

    registros = df[["ano", "uf", "codigo_uf", "sexo", "idade", "grupo_etario", "populacao"]].copy()
    registros = registros.dropna(subset=["idade"]).copy()
    registros["idade"] = registros["idade"].astype(int)

    if registros.empty:
        raise ValueError("A base tratada de 2010 ficou vazia ao processar o arquivo bruto exportado.")
    return registros.sort_values(["sexo", "idade"]).reset_index(drop=True)


def salvar_dados_tratados(df: pd.DataFrame, nome_arquivo: str) -> Path:
    garantir_pasta_tratados()
    caminho = PASTA_TRATADOS / nome_arquivo
    df.to_csv(caminho, index=False, encoding="utf-8-sig")
    return caminho


def tratar_todos_os_dados(caminho_2010: Path, caminho_2022: Path) -> pd.DataFrame:
    df_2010 = tratar_dados_2010(caminho_2010)
    df_2022 = tratar_dados_2022(caminho_2022)
    salvar_dados_tratados(df_2010, "populacao_df_2010_tratada.csv")
    salvar_dados_tratados(df_2022, "populacao_df_2022_tratada.csv")
    consolidado = pd.concat([df_2010, df_2022], ignore_index=True)
    salvar_dados_tratados(consolidado, "populacao_df_2010_2022_tratada.csv")
    return consolidado
