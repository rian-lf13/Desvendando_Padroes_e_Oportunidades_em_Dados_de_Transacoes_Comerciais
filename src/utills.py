import matplotlib.pyplot as plt
import pandas as pd
import os

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def salvar_grafico(figura, nome_arquivo='grafico_padrao.png', diretorio_saida= 'saida/graficos'):
    if figura is None:
        print('Erro: Não há gráfico válido para salvar.')
        return
    
    os.makedirs(diretorio_saida, exist_ok=True) # Garanter que o diretório exista
    caminho_completo= os.path.join(diretorio_saida, nome_arquivo)
    try:
        figura.savefig(caminho_completo, bbox_inches='tight')
        print(f'Gráfico salvo com sucesso em {caminho_completo}')
    except Exception as e:
        print(f'Erro ao salvar o gráfico "{nome_arquivo}": {e}')
    finally:
        plt.close(figura) # Fecha a figura para liberar memória

def salvar_df_csv(dados_ou_serie, nome_arquivo='dados_padrao.csv', diretorio_saida= 'saida/dados_csv'):

    if dados_ou_serie is None:
        print('Erro: Não há dados váliddos para salvar em CSV.')
        return
    
    os.makedirs(diretorio_saida, exist_ok=True)
    caminho_completo= os.path.join(diretorio_saida, nome_arquivo)
    try:
        # Se for uma Series, converte para DataFrame para salvar com nome da coluna
        if isinstance(dados_ou_serie, pd.Series):
            df_salvar= dados_ou_serie.reset_index()
            # Tenta usar o nome da Série como nome da coluna de valor, ou 'Valor'
            if dados_ou_serie.name:
                df_salvar.rename(columns={dados_ou_serie.name: 'Valor'}, inplace= True)
            else: 
                df_salvar.columns= ['Indice', 'Valor'] # Nome padrão se a série não tiver nome
        else:
            df_salvar = dados_ou_serie

        df_salvar.to_csv(caminho_completo, index=False, encoding='utf-8')
        print(f'Dados salvos com sucesso em: {caminho_completo}')
    except Exception as e:
        print(f'Erro ao salvar o arquivo CSV "{nome_arquivo}": {e}')

def exibir_grafico(figura):
    if figura:
        plt.show()
    else:
        print('Nenhum gráfico para exibir.')

def exibir_df(dados_ou_serie, titulo= 'Dados Resultados'):
    if dados_ou_serie is not None:
        print(f'--- {titulo} ---')
        print(dados_ou_serie.to_string())
    else:
        print(f'Nenhum {titulo.lower()} para exibir.')

if __name__ =='__main__':
    print('--- Testando módulo ---')
    import numpy as np

    # Teste para salvar CSV
    dados_teste= pd.DataFrame({'Coluna1': [10,20], 'Coluna2': ['A', 'B']})
    salvar_df_csv(dados_teste, nome_arquivo='teste_saida_df.csv')

    serie_teste= pd.Series([100, 200, 300], name='VendasTotal')
    salvar_df_csv(serie_teste, nome_arquivo='teste_saida_serie.csv')

    # TEste para salvar gráfico
    fig_teste, ax_teste= plt.subplots()
    ax_teste.plot(np.random.rand(5), np.random.rand(5))
    ax_teste.set_title('Gráfico de Teste (Exemplo)')
    salvar_grafico(fig_teste, nome_arquivo='teste_saida_grafico.png')

    # Teste para exibir DataFrame
    exibir_df(dados_teste, titulo='DAtaFrame Exemplo')
    exibir_df(serie_teste, titulo='Série Exemplo')


