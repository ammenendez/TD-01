# Dados DF - Censo 2010 e 2022

## Objetivo

Este projeto baixa, trata, analisa e visualiza a população do Distrito Federal por sexo e idade, comparando os Censos Demográficos de 2010 e 2022.

## Fonte dos dados

- IBGE / SIDRA
- Censo Demográfico 2022, tabela 9514: população residente, por sexo, idade e forma de declaração da idade
- Censo Demográfico 2010, tabela 3107 do SIDRA. Se a API não devolver o detalhamento necessário, o arquivo deve ser exportado manualmente do SIDRA e salvo em `dados/brutos/populacao_df_2010.csv`.

## Estrutura do projeto

```text
dados_df/
├── dados/
│   ├── brutos/
│   └── tratados/
├── graficos/
├── src/
│   ├── baixar_dados.py
│   ├── tratar_dados.py
│   ├── indicadores.py
│   ├── graficos.py
│   └── main.py
├── requirements.txt
└── README.md
```

## Instalação

Crie um ambiente virtual e instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução

Execute o fluxo principal:

```bash
python src/main.py
```

Para forçar atualização dos arquivos baixados:

```bash
python src/main.py --atualizar
```

## Arquivos gerados

- `dados/brutos/populacao_df_2010.csv`
- `dados/brutos/populacao_df_2022.csv`
- `dados/tratados/populacao_df_2010_tratada.csv`
- `dados/tratados/populacao_df_2022_tratada.csv`
- `dados/tratados/populacao_df_2010_2022_tratada.csv`
- `dados/tratados/indicadores_df_2010_2022.csv`
- `graficos/piramide_etaria_df_2010.png`
- `graficos/piramide_etaria_df_2022.png`
- `graficos/distribuicao_percentual_grupos_etarios_2010_2022.png`
- `graficos/jovens_adultos_idosos_2010_2022.png`
- `graficos/razao_sexo_por_grupo_etario.png`

## Indicadores calculados

- população total
- população masculina
- população feminina
- percentual masculino
- percentual feminino
- razão de sexo
- população de 0 a 14 anos
- população de 15 a 64 anos
- população de 65 anos ou mais
- percentual de jovens
- percentual de adultos
- percentual de idosos
- índice de envelhecimento
- razão de dependência

## Observação sobre 2010

A estrutura do SIDRA para 2010 pode ser diferente da de 2022. O código usa uma função separada para 2010 e documenta essa diferença. Neste trabalho, a fonte metodológica adotada para 2010 é a tabela 3107 do SIDRA. Quando a API não devolve o detalhamento correto, o fluxo depende do arquivo bruto exportado manualmente do SIDRA.

## Como adaptar para download manual de 2010

Se a tabela do Censo 2010 precisar ser baixada manualmente no site do IBGE:

1. Baixe o arquivo oficial no SIDRA usando a opção de exportação da tabela 3107.
2. Salve o arquivo em `dados/brutos/populacao_df_2010.csv`.
3. Exporte a tabela com as colunas completas, incluindo códigos e nomes das dimensões.
4. Se o arquivo vier em formato diferente, adapte a função `tratar_dados_2010()` em `src/tratar_dados.py` para padronizar as colunas.

## Nota metodológica

Os grupos etários são padronizados em quinquênios:

- 0-4
- 5-9
- 10-14
- 15-19
- 20-24
- 25-29
- 30-34
- 35-39
- 40-44
- 45-49
- 50-54
- 55-59
- 60-64
- 65-69
- 70-74
- 75-79
- 80+
