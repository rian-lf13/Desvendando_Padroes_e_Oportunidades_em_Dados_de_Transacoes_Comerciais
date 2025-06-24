from src.data_handler import carregar_dados, pre_processamento_dados, obter_visao_geral
from src.analysis import (
    analisar_vendas_office_supplies,
    grafico_vendas_data,
    grafico_venda_estado,
    top_cidades_vendas,
    grafico_vendas_segmento,
    vendas_segmento_ano
)
from src.utills import(
    limpar_tela,
    salvar_grafico,
    salvar_df_csv,
    exibir_grafico,
    exibir_df
)

# Gerencia a interação com o usuário para slavar ou exibir o resultado.
def gerenciar_saida(dado_saida, nome_base_arquivo, tipo_saida):
    if dado_saida is None:
        print('Nenhum dado ou gráfico válido para gerar saída.')
        return
    
    print('\n--- Opções de Saída ---')
    print('1. Salvar arquivo')
    print('2. Exibir no terminal/tela')
    opcao_saida= input('Escolha uma opção [1] ou [2]: ').strip()

    if opcao_saida == '1':
        extensao= 'png' if tipo_saida == 'grafico' else 'csv'
        nome_sugerido= f'{nome_base_arquivo}.{extensao}'
        nome_arq_digitado= input(f'Digite o nome do arquivo (sugestão: {nome_sugerido}:)') or nome_sugerido
        if tipo_saida == 'grafico':
            salvar_grafico(dado_saida, nome_arquivo=nome_arq_digitado)
        else:
            salvar_df_csv(dado_saida, nome_arquivo=nome_arq_digitado)
    elif opcao_saida == '2':
        if tipo_saida == 'grafico':
            exibir_grafico(dado_saida)
        else:
            exibir_df(dado_saida, titulo=f'Resultado da Análise: {nome_base_arquivo}')
    else:
        print('Opção de saída inválida. Nenhuma ação realizada.')

def menu_principal():
    df_dados = None #O DataFrame principal, será iniciado com None.

    while True:
        limpar_tela() # Limpa o terminal a cada iteração do menu.
        print("╔════════════════════════════════════════════════════╗")
        print("║          PAINEL DE ANÁLISE DE VENDAS             ║")
        print("╠════════════════════════════════════════════════════╣")
        print("║ 1. Carregar e Pré-processar Dados                  ║")
        print("║ 2. Ver Visão Geral dos Dados                       ║")
        print("║ 3. Análise: Vendas de 'Office Supplies'            ║")
        print("║ 4. Análise: Vendas Por Data do Pedido              ║")
        print("║ 5. Análise: Vendas por Estado                      ║")
        print("║ 6. Análise: Top 10 Cidades em Vendas               ║")
        print("║ 7. Análise: Vendas por Segmento                    ║")
        print("║ 8. Análise: Vendas por Segmento e Ano              ║")
        print("║ 0. Sair do Programa                                ║")
        print("╚════════════════════════════════════════════════════╝") # Usei o ChatGPT para criar a borda do menu.

        opcao = input('Digite o número da opção desejada: ').strip()

        if opcao == '1':
            caminho = input('Digite o caminho do arquivo CSV (ex: data/dados.csv): ') 
            dados_carregados = carregar_dados(caminho)
            if dados_carregados is not None:
                df_dados = pre_processamento_dados(dados_carregados)
                if df_dados is None:
                    print('Pré-processamento falhou. Dados não disponíveis')
            input('\nPressione Enter para continuar...')
        
        elif opcao == '2':
            if df_dados is None:
                print('Por favor, carregue e pré-processe os dados primeiro (Opção 1).')
            else:
                obter_visao_geral(df_dados)
            input('\nPressione Enter para continuar...')

        elif opcao == '3':
            if df_dados is None:
                print('Por favor, carregue e pré-processe os dados primeiro (Opção 1).')
            else:
                resultado_analise, _ = analisar_vendas_office_supplies(df_dados)
                if resultado_analise is not None:
                    gerenciar_saida(resultado_analise, 'vendas_office_supplies_por_cidade', 'dataframe')
            input('\nPressione Enter para continuar...')
        
        elif opcao == '4':
            if df_dados is None:
                print('Por favor, carregue e pré-processe os dados primeiro (Opção 1).')
            else:
                figura = grafico_vendas_data(df_dados)
                gerenciar_saida(figura, 'grafico_vendas_por_data', 'grafico')
            input('\nPressione Enter para continuar...')
        
        elif opcao == '5':
            if df_dados is None:
                print('Por favor, carregue e pré-processe os dados primeiro (Opção 1).')
            else:
                figura = grafico_venda_estado(df_dados)
                gerenciar_saida(figura, 'grafico_vendas_por_estado', 'grafico')
            input('\nPressione Enter para continuar...')
        
        elif opcao == '6':
            if df_dados is None:
                print('Por favor, carregue e pré-processe os dados primeiro (Opção 1).')
            else:
                figura = top_cidades_vendas(df_dados)
                gerenciar_saida(figura, 'grafico_top_cidades_vendas', 'grafico')
            input('\nPressione Enter para continuar...')
        
        elif opcao == '7':
            if df_dados is None:
                print('Por favor, carregue e pré-processe os dados primeiro (Opção 1).')
            else:
                figura = grafico_vendas_segmento(df_dados)
                gerenciar_saida(figura, 'grafico_vendas_segmento', 'grafico')
            input('\nPressione Enter para continuar...')
        
        elif opcao == '8':
            if df_dados is None:
                print('Por favor, carregue e pré-processe os dados primeiro (Opção 1).')
            else:
                resultado_analise = vendas_segmento_ano(df_dados)
                if resultado_analise is not None:
                    gerenciar_saida(resultado_analise, 'tabela_vendas_segmento_ano', 'dataframe')
            input('\nPressione Enter para continuar...')

        elif opcao == '0':
            print('Saindo do Painel de Análise de Vendas. Até a próxima!')
            break
        else:
            print('Opção inválida. Por favor, digite um número de 0 a 8.')
            input('\nPressione Enter para continuar...')

if __name__ == '__main__':
    menu_principal()