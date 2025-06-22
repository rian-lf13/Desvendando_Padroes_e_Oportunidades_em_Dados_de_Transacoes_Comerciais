import pandas as pd
import numpy as np

def carregar_dados(data):

    try:
        df= pd.read_csv(data)
        print(f'Dados carregados com sucesso de {data}')
        return df
    
    except FileNotFoundError:
        print(f'Erro: O arquivo "{data}" não foi encontrado.')
        return None
    
    except Exception as e:
        print(f'Ocorreu um erro ao carregar o arquivo: {e}')

def pre_processamento_dados(dados):
    
    if dados is None:
        return None

    dados_processados = dados.copy() # PAra evitar o SettingWithCopyWarning

    print('\n--- Iniciando Pré-Processamento dos Dados ---')

# Verificação e conversão da coluna 'Data_Pedido'
    if 'Data_Pedido' in dados_processados.columns:
        try:
            dados_processados['Data_Pedido'] = pd.to_datetime(dados_processados['Data_Pedido'], dayfirst= True, errors= 'coerce')
            if dados_processados['Data_Pedido'].isnull().any():
                linhas_removidas = dados_processados['Data_Pedido'].isnull().sum()
                print(f'Aviso: {linhas_removidas} foram removidas da coluna "Data_pedido"')
                dados_processados.dropna(subset= ['Data_Pedido'], inplace=True)
        except Exception as e:
            print(f'Erro ao converter "Data_Pedido" para datetime: {e}')
    else:
        print('Aviso: Coluna "Data_Pedido" não encontrada para conversão.')

# Extraindo o ano 
    if 'Data_Pedido' in dados_processados.columns and pd.api.types.is_datetime64_any_dtype(dados_processados['Data_Pedido']):
        dados_processados['Ano'] = dados_processados['Data_Pedido'].dt.year
        print('Coluna "Ano" extraída com sucesso.')
    else:
        print('Aviso: "Ano" não pode ser extraído. "Data_Pedido" não é datetime ou não existe.')

# Tratando duplicatas
    if dados_processados.duplicated().any():
        num_duplicatas = dados_processados.duplicated().sum()
        dados_processados.drop_duplicates(inplace= True)
        print(f'Duplicatas removidas: {num_duplicatas} linhas duplicadas foram encontradas e removidas.')
    else:
        print('Nenhuma linha duplicada encontrada.')

# Verificando valores nulos
    valores_nulos = dados_processados.isnull().sum()
    if valores_nulos.sum() > 0:
        print('\n--- Valores Nulos Por Coluna Após Pré-Processamento ---' )
        print(valores_nulos[valores_nulos > 0])
        print('Sugestão: Considere um tratamento específico para esses valores nulos, se necessário.')
    else:
        print('Nenhum valor nulo encontrado após o pré-processamento.') 

    print('\n--- Pré-Processamento Concluído ---')
    return dados_processados   

def obter_visao_geral(dados):
    if dados is None:
        print('Nenhum dado carregado para mostrar a visão geral.')
        return

    print('\n--- Visão Geral do DataFrame ---')
    print(f'Formato(linhas, colunas): {dados.shape}')
    print('\nPrimeiras 5 linhas:')
    print(dados.head())
    print('\nÚltimas 5 linhas:')
    print(dados.tail())
    print('\nTipos de Dados por Coluna:')
    print(dados.dtypes)
    print('\nContagem de Valores Nulos por Colunas (antes do pré-processamento específico):')
    print(dados.isnull().sum())

# Bloco para testar o módulo individualmente
if __name__ == '__main__':
    print('--- Testando módulo processamento_dados.py ---')
    exemplo= 'data/dados_teste.csv'
    dados_teste = carregar_dados(exemplo)
    if dados_teste is not None:
        obter_visao_geral(dados_teste)
        dados_processado_teste= pre_processamento_dados(dados_teste)
        if dados_processado_teste is not None:
            obter_visao_geral(dados_processado_teste)