import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


# Função para consultar dados de Produção usando requests
def consultar_producao(ano):
    url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02'
    params = {'ano': ano}  # Adapte conforme necessário para passar o ano
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Erro ao acessar a página para o ano {ano}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    tabela = soup.find('table', {'class': 'tb_base tb_dados'})

    if not tabela:
        print(f"Tabela não encontrada para o ano {ano}.")
        return None

    dados_tabela = []
    for linha in tabela.find_all('tr'):
        colunas = linha.find_all('td')
        dados_linha = [coluna.get_text(strip=True) for coluna in colunas]
        if dados_linha:
            dados_linha.append(ano)
            dados_tabela.append(dados_linha)

    return dados_tabela


# Função para consultar dados de outras seções com subopções
def consultar_dados_ano_tipo(ano, subopcao, url):
    params = {'subopcao': subopcao, 'ano': ano}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Erro ao acessar a página para o ano {ano} e subopção {subopcao}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    tabela = soup.find('table', {'class': 'tb_base tb_dados'})

    if not tabela:
        print(f"Tabela não encontrada para o ano {ano} e subopção {subopcao}.")
        return None

    dados_tabela = []
    for linha in tabela.find_all('tr'):
        colunas = linha.find_all('td')
        dados_linha = [coluna.get_text(strip=True) for coluna in colunas]
        if dados_linha:
            dados_linha.append(ano)
            dados_linha.append(subopcao)
            dados_tabela.append(dados_linha)

    return dados_tabela


# Função principal que coleta dados de todas as abas e salva em CSV
def coletar_dados():
    anos = list(range(1970, 2024))
    diretorio_salvar = './tabelas/'
    os.makedirs(diretorio_salvar, exist_ok=True)

    # Produção
    dados_producao = []
    for ano in anos:
        print(f"Consultando dados de Produção para o ano {ano}...")
        dados_ano = consultar_producao(ano)
        if dados_ano:
            dados_producao.extend(dados_ano)

    if dados_producao:
        df_producao = pd.DataFrame(dados_producao, columns=['Produto', 'Quantidade', 'Ano'])
        df_producao.to_csv(os.path.join(diretorio_salvar, 'base_producao.csv'), index=False)

    # Processamento
    url_processamento = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03'
    subopcoes_processamento = ['subopt_01', 'subopt_02', 'subopt_03', 'subopt_04']
    dados_processamento = []
    for subopcao in subopcoes_processamento:
        for ano in anos:
            print(f"Consultando dados de Processamento para o ano {ano} e subopção {subopcao}...")
            dados_ano_tipo = consultar_dados_ano_tipo(ano, subopcao, url_processamento)
            if dados_ano_tipo:
                dados_processamento.extend(dados_ano_tipo)

    if dados_processamento:
        df_processamento = pd.DataFrame(dados_processamento, columns=['Cultivar', 'Quantidade', 'Ano', 'Subopcao'])
        df_processamento.to_csv(os.path.join(diretorio_salvar, 'base_processamento.csv'), index=False)

    # Comercialização
    url_comercializacao = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04'
    dados_comercializacao = []
    for ano in anos:
        print(f"Consultando dados de Comercialização para o ano {ano}...")
        dados_ano = consultar_dados_ano_tipo(ano, 'subopt_01',
                                             url_comercializacao)  # Ajuste a subopção conforme necessário
        if dados_ano:
            dados_comercializacao.extend(dados_ano)

    if dados_comercializacao:
        df_comercializacao = pd.DataFrame(dados_comercializacao, columns=['Produto', 'Quantidade', 'Ano'])
        df_comercializacao.to_csv(os.path.join(diretorio_salvar, 'base_comercializacao.csv'), index=False)

    # Importação
    url_importacao = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05'
    subopcoes_importacao = ['subopt_01', 'subopt_02', 'subopt_03', 'subopt_04', 'subopt_05']
    dados_importacao = []
    for subopcao in subopcoes_importacao:
        for ano in anos:
            print(f"Consultando dados de Importação para o ano {ano} e subopção {subopcao}...")
            dados_ano_tipo = consultar_dados_ano_tipo(ano, subopcao, url_importacao)
            if dados_ano_tipo:
                dados_importacao.extend(dados_ano_tipo)

    if dados_importacao:
        df_importacao = pd.DataFrame(dados_importacao, columns=['Paises', 'Quantidade', 'Valor', 'Ano', 'Subopcao'])
        df_importacao.to_csv(os.path.join(diretorio_salvar, 'base_importacao.csv'), index=False)

    # Exportação
    url_exportacao = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06'
    subopcoes_exportacao = ['subopt_01', 'subopt_02', 'subopt_03', 'subopt_04']
    dados_exportacao = []
    for subopcao in subopcoes_exportacao:
        for ano in anos:
            print(f"Consultando dados de Exportação para o ano {ano} e subopção {subopcao}...")
            dados_ano_tipo = consultar_dados_ano_tipo(ano, subopcao, url_exportacao)
            if dados_ano_tipo:
                dados_exportacao.extend(dados_ano_tipo)

    if dados_exportacao:
        df_exportacao = pd.DataFrame(dados_exportacao, columns=['Paises', 'Quantidade', 'Valor', 'Ano', 'Subopcao'])
        df_exportacao.to_csv(os.path.join(diretorio_salvar, 'base_exportacao.csv'), index=False)


# Executando a coleta de dados
if __name__ == "__main__":
    coletar_dados()

