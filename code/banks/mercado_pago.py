from bank import Bank
from file import File
import pandas as pd

class MercadoPago(Bank):
    """
    Classe para processamento de extratos do Mercado Pago.
    """
    def __init__(self):
        super().__init__()
        self.titulo = 'Mercado Pago'

    def gerar_extrato(self, arquivo: File):
        """
        Gera o extrato do Mercado Pago a partir do arquivo fornecido.
        """
        qnt_pages = arquivo.lenght()

        tabela1 = arquivo.custom_read(area_lida=[27,0,100,100], pg=1)
        
        if qnt_pages > 1:
            arquivo_complt = arquivo.simple_read(pg=f'2-{qnt_pages}')
            
        arquivo_complt.insert(0,tabela1[0])

        self.filt_colunas(arquivo_complt, ["Data", "Histórico", "", "Valor", ""])
        self.inserir_espacos(troca=True)
        self.col_inf_sinal(6)
        self.__filtro_linhas()

        return self.df

    def __filtro_linhas(self):
        """
        Ajusta linhas do extrato do Mercado Pago.
        """
        lista_tabelas = []
        self.df.fillna('', inplace=True)
        for index, row in self.df.iterrows():
            if str(row['Data']) == '':
                if index != len(self.df) and self.df.iloc[index + 1]['Data'] != ''\
                    and self.df.iloc[index - 2]['Data'] != '' \
                        or self.df.iloc[index - 2]['Histórico'] not in self.df.iloc[index - 1]['Histórico']:
                    linhaFilho = self.df.iloc[index + 1]
                    self.df.loc[[index + 1], ['Histórico']] = \
                    f"{str(row['Histórico'])}  {str(linhaFilho['Histórico'])}" 
                else:
                    linhaPai = self.df.iloc[index - 1]
                    self.df.loc[[index - 1], ['Histórico']] = \
                    f"{str(linhaPai['Histórico'])}  {str(row['Histórico'])}"

        lista_tabelas.append(self.df.loc[self.df['Data'] != ''])
        self.df = pd.concat(lista_tabelas, ignore_index=True)