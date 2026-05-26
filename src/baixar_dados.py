from __future__ import annotations

from pathlib import Path

import pandas as pd
import requests

PASTA_BRUTOS = Path("dados/brutos")


def garantir_pastas() -> None:
    """Cria as pastas necessárias do projeto."""
    for pasta in [PASTA_BRUTOS, Path("dados/tratados"), Path("graficos")]:
        pasta.mkdir(parents=True, exist_ok=True)


def chamar_sidra_api(url: str, salvar_em: str | None = None) -> pd.DataFrame:
    """
    Chama a API do SIDRA/IBGE e retorna os dados em um DataFrame.

    A API retorna a primeira linha como cabeçalho e as demais como registros.
    """
    try:
        resposta = requests.get(url, timeout=120)
        resposta.raise_for_status()
        dados = resposta.json()

        cabecalho = dados[0]
        linhas = dados[1:]

        df = pd.DataFrame(linhas)
        df.columns = [cabecalho[coluna] for coluna in df.columns]

        if salvar_em:
            caminho = Path(salvar_em)
            caminho.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(caminho, index=False, encoding="utf-8-sig")

        return df
    except requests.exceptions.RequestException as erro:
        raise RuntimeError(f"Erro ao acessar a API do SIDRA: {erro}") from erro
    except Exception as erro:
        raise RuntimeError(f"Erro ao processar os dados do SIDRA: {erro}") from erro


def arquivo_bruto_tem_detalhamento(caminho: Path) -> bool:
    """Verifica se o arquivo bruto traz dimensões detalhadas do SIDRA."""
    if not caminho.exists():
        return False
    try:
        df = pd.read_csv(caminho, dtype=str)
    except Exception:
        return False
    colunas = {str(col).strip().upper() for col in df.columns}
    return any(col.startswith("D") for col in colunas) and any(col == "V" for col in colunas)


def baixar_dados_2022(atualizar: bool = False) -> Path:
    """
    Baixa os dados do Censo 2022 para o Distrito Federal.

    A URL segue o padrão da API SIDRA com as classificações informadas pelo
    usuário, que permitem obter sexo, idade e forma de declaração da idade.
    """
    caminho = PASTA_BRUTOS / "populacao_df_2022.csv"
    if arquivo_bruto_tem_detalhamento(caminho) and not atualizar:
        return caminho

    url_2022_df = (
        "https://apisidra.ibge.gov.br/values/"
        "t/9514"
        "/n3/53"
        "/v/allxp"
        "/p/all"
        "/c2/allxt"
        "/c287/6653,49108,49109,60040,60041,93070,93084,93085,93086,93087,93088,93089,93090,93091,93092,93093,93094,93095,93096,93097,93098"
        "/c286/113635"
    )
    chamar_sidra_api(url_2022_df, salvar_em=str(caminho))
    return caminho


def baixar_dados_2010(atualizar: bool = False) -> Path:
    """
    Baixa os dados do Censo 2010 para o Distrito Federal.

    A consulta é separada da de 2022 para manter os tratamentos distintos.
    """
    caminho = PASTA_BRUTOS / "populacao_df_2010.csv"
    if arquivo_bruto_tem_detalhamento(caminho) and not atualizar:
        return caminho

    url_2010_df = (
        "https://apisidra.ibge.gov.br/values/"
        "t/3107"
        "/n3/53"
        "/v/allxp"
        "/p/all"
        "/c1/0"
        "/c2/allxt"
        "/c58/0,1140,1141,1142,1143,1144,1145,1146,1147,1148,1149,1150,1151,1152,1153,1154,1155,6802,6803,92963,92964,92965"
    )
    chamar_sidra_api(url_2010_df, salvar_em=str(caminho))
    return caminho


def baixar_todos_os_dados(atualizar: bool = False) -> dict[str, Path]:
    """Baixa os arquivos brutos de 2010 e 2022."""
    return {
        "2010": baixar_dados_2010(atualizar=atualizar),
        "2022": baixar_dados_2022(atualizar=atualizar),
    }
