import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Identifica a cidade com maior valor de venda para produtos "Office Supplies".
def analisar_vendas_office_supplies(dados):
    if dados is None or 'Categoria' not in dados.columns or 'Valor_Venda' not in dados.columns or 'Cidade' not in dados.columns:
        print('Dados insuficientes (colunas "Categoria", "Valor_Venda" ou "Cidade" ausentes) para esta análise.')
        return None, None
    
    dados_off_sup = dados[dados['Categoria'] == 'Office Supplies']

    if dados_off_sup.empty:
        print('Não foram encontrados produtos na categoria "Office Supplies" nos dados.')
        return None, None
    
    vendas_cidade= dados_off_sup.groupby('Cidade')['Valor_Venda'].sum()
    cidade_maior_venda = vendas_cidade.idxmax()

    print(f'\n--- Análise de Vendas de "Office Supplies" ---')
    print(f'A cidade com MAIOR venda de produtos "Office Supplies" é: {cidade_maior_venda}')
    print('\nTop 5 Cidades para "Office Supplies":')
    print(vendas_cidade.sort_values(ascending= False).head())

    return vendas_cidade, cidade_maior_venda        


# Gera um gráfico de linha do total de vendas por data do pedido.
def grafico_vendas_data(dados):
    if dados is None or 'Data_Pedido' not in dados.columns or 'Valor_Venda' not in dados.columns:
        print('Dados insuficientes (colunas "Data_Pedido" ou "Valor_Venda" ausentes) para esta plotagem.')
        return None
    
    if not pd.api.types.is_datetime64_any_dtype(dados['Data_Pedido']):
        print('Aviso: "Data_Pedido" não no formato de data/hora. Por favor, pré-processe os dados primeiro.')
        return None
    
    vendas_agrupadas_datas= dados.groupby('Data_Pedido')['Valor_Venda'].sum()

    fig, ax = plt.subplots(figsize=(20, 6))
    vendas_agrupadas_datas.plot(ax= ax, color= 'green')
    ax.set_title('Total de Vendas Por Data do Pedido')
    ax.set_xlabel('Data do Pedido')
    ax.set_ylabel('Total de Vendas')
    plt.grid(True, linestyle= '--', alpha= 0.7) # Melhorando a legibiliadade
    plt.tight_layout() # Evitando sobreposição de labels 
    return fig


# Gera gráfico de barras do total de vendas por Estado
def grafico_venda_estado(dados):
    if dados is None or 'Estado' not in dados.columns or 'Valor_Venda' not in dados.columns:
        print('Dados insuficientes (colunas "Estado" ou "Valor_Venda" ausentes) para esta plotagem.')
        return None
    vendas_estado = dados.groupby('Estado')['Valor_Venda'].sum().reset_index()
    

    fig, ax = plt.subplots(figsize=(16, 6))
    sns.barplot(data= vendas_estado, 
                x= 'Estado',
                y='Valor_Venda',
                palette= 'husl',
                ax = ax,
                legend= False)
    ax.set_title('Total de Vendas por Estado')
    ax.set_xlabel('Estado')
    ax.set_ylabel('Total de Vendas')
    plt.xticks(rotation= 90)
    plt.tight_layout()
    return fig


# Gera gráfico de barras das cidades com maior total de vendas.
def top_cidades_vendas(dados, n_cidades= 10):
    if dados is None or 'Cidade' not in dados.columns or 'Valor_Venda' not in dados.columns:
        print('Dados insuficientes (colunas "Cidade" ou "Valor_Venda" ausentes) para esta plotagem.')
        return None
    
    cidades_vendas= dados.groupby('Cidade')['Valor_Venda'].sum().reset_index().sort_values(
        by= 'Valor_Venda', ascending= False).head(n_cidades)
    
    print(f'\n--- Top {n_cidades} Cidades com Maior Venda ---')
    print(cidades_vendas)

    fig, ax = plt.subplots(figsize=(16, 6))
    sns.set_palette('coolwarm')
    sns.barplot(data= cidades_vendas,
                x= 'Cidade',
                y= 'Valor_Venda',
                ax= ax)
    ax.set_title(f'Top {n_cidades} Cidade com Maior Total de Vendas')
    ax.set_xlabel('Cidade')
    ax.set_ylabel('Total de Vendas')
    plt.tight_layout()
    return fig 

def grafico_vendas_segmento(dados):
    if dados is None or 'Segmento' not in dados.columns or 'Valor_Venda' not in dados.columns:
        print('Dados insuficientes (colunas "Segmento" ou "Valor_Venda" ausentes) para esta plotagem.')
        return None
    
    vendas_segmento= dados.groupby('Segmento')['Valor_Venda'].sum().reset_index().sort_values(
        by= 'Valor_Venda', ascending= False)
    
    # Função auxiliar para formatar o autopct
    def formatar_autopct_valores_ab(valores):
        def formatar_percentual(pct):
            total= sum(valores)
            val = int(round(pct * total / 100))
            return f'R$ {val:,.2f}'.replace(',', 'x').replace('.', ',').replace('X', '.')
        return formatar_percentual
    
    fig, ax = plt.subplots(figsize=(16, 6))
    fatia, texto, auto_texto = ax.pie(vendas_segmento['Valor_Venda'],
                                      labels= vendas_segmento['Segmento'],
                                      autopct= formatar_autopct_valores_ab(vendas_segmento['Valor_Venda']),
                                      startangle= 90,
                                      pctdistance= 0.85)    
    
    # Círculo para transformar em donut chart
    circulo_central = plt.Circle((0,0),0.82, fc= 'white')
    ax.add_artist(circulo_central)

    # Anotação do total de vendas
    total_vendas = int(sum(vendas_segmento['Valor_Venda']))
    ax.annotate(f'Total Geral:\nR$ {total_vendas:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
                xy=(0,0), # Centro
                xytext=(0,0),
                ha= 'center', va= 'center',
                fontsize= 12, color= 'black',
                bbox=dict(boxstyle= 'round, pad=0.5', facecolor='white', alpha= 0.5)
                ) # Uma caixa
    ax.set_title('Segmento com Maior Total de Vendas')
    plt.tight_layout()
    return fig


# Calcula e retorna o total de vendas por segmento e por ano.
def vendas_segmento_ano(dados):
    if dados is None or 'Ano' not in dados.columns or 'Segmento' not in dados.columns or 'Valor_Venda' not in dados.columns:
        print('Dados insuficientes (colunas "Ano", "Segmento" ou "Valor_Venda" ausentes) para esta análise.')
        return None
    
    vendas_segmento_ano= dados.groupby(['Ano', 'Segmento'])['Valor_Venda'].sum()

    print('\n--- Total de Vendas Por Segmento e Ano ---')
    print(vendas_segmento_ano)
    return vendas_segmento_ano

if __name__ == '__main__':
    print('--- Testando ---')
    # DataFrame de exemplo para teste
    dados_exemplo = {
        'Data_Pedido': ['01/01/2023', '05/01/2023', '10/01/2023', '15/01/2023', '20/01/2023', '01/01/2024'],
        'Categoria': ['Office Supplies', 'Technology', 'Office Supplies', 'Furniture', 'Office Supplies', 'Technology'],
        'Cidade': ['São Paulo', 'Rio de Janeiro', 'São Paulo', 'Belo Horizonte', 'Rio de Janeiro', 'São Paulo'],
        'Estado': ['SP', 'RJ', 'SP', 'MG', 'RJ', 'SP'],
        'Segmento': ['Consumer', 'Corporate', 'Home Office', 'Consumer', 'Corporate', 'Consumer'],
        'Valor_Venda': [100, 250, 150, 300, 200, 400]
    }
    dados_teste = pd.DataFrame(dados_exemplo)
    dados_teste['Data_Pedido']= pd.to_datetime(dados_exemplo['Data_Pedido'], dayfirst=True)
    dados_teste['Ano']= dados_teste['Data_Pedido'].dt.year

    print('\nTeste: Vendas Office Supplies')
    vendas_of, cidade_maior = analisar_vendas_office_supplies(dados_teste)

    print('\nTeste: Gráfico Vendas por Data')
    fig_data= grafico_vendas_data(dados_teste)
    if fig_data is not None: 
        fig_data.show()

    print('\nTeste: Gráfico Vendas Por Estado')
    fig_estado = grafico_venda_estado(dados_teste)
    if fig_estado: plt.show()

    print('\nTeste: Gráfico Top Cidades')
    fig_top= top_cidades_vendas(dados_teste, n_cidades= 2)
    if fig_top: plt.show()

    print('\nTeste: Gráfico Vendas Por Segmento')
    fig_seg = grafico_vendas_segmento(dados_teste)
    if fig_seg: plt.show()

    print('\nTeste: Vendas Por Segmento e Ano')
    seg_ano_resultado= vendas_segmento_ano(dados_teste)

