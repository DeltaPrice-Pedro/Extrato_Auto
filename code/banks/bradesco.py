from bank import Bank
from file import File
import pandas as pd

class Bradesco(Bank):
    """
    Classe para processamento de extratos do Bradesco.
    """
    def __init__(self):
        super().__init__()
        self.titulo = 'Bradesco'

    def gerar_extrato(self, arquivo: File):
        """
        Gera o extrato do Bradesco a partir do arquivo fornecido.
        """
        qnt_pages = arquivo.lenght()

        tabela1 = arquivo.custom_read(area_lida=[25,0,100,100], pg=1)
        
        if qnt_pages > 1:
            arquivo_complt = arquivo.custom_read(pg=f'2-{qnt_pages}',\
                area_lida=[9,0,100,100])
            
        arquivo_complt.insert(0,tabela1[0])

        self.__filtro_colunas(arquivo_complt)
        self.inserir_espacos(troca=False, ordem_espacos=[1,2,3])
        self.__col_inf()
        self.__col_data()
        self.__filtro_linhas()

        return self.df

    def __filtro_colunas(self, arquivo):
        """
        Ajusta as colunas dos DataFrames conforme o padrão do Bradesco.
        """
        for tabelas in arquivo:
            tabelas.columns = ["Data", "Histórico", "", "Crédito", "Débito", ""]

        self.df = pd.concat(arquivo, ignore_index=True)
        self.df = self.df.drop('', axis=1)

    def __col_inf(self):
        """
        Cria as colunas 'Inf.' e 'Valor' baseadas nos valores de crédito e débito.
        """
        coluna_inf = []
        coluna_valor = []
        self.df.fillna('', inplace=True)
        for index, row in self.df.iterrows():
            if str(row['Débito']) != '':
                coluna_inf.append('D')
                coluna_valor.append(str(row['Débito']).replace('-',''))
            elif str(row['Crédito']) != '':
                    coluna_inf.append('C')
                    coluna_valor.append(str(row['Crédito']))
            else:
                    coluna_valor.append('')
                    coluna_inf.append('')

        self.df.insert(3, 'Valor', coluna_valor)
        self.df.insert(6,'Inf.', coluna_inf)
        self.df = self.df.drop('Débito', axis=1)
        self.df = self.df.drop('Crédito', axis=1)

    def __col_data(self):
        """
        Preenche datas ausentes com a última data válida.
        """
        data_atual = ''
        for index, row in self.df.iterrows():
            if str(row['Data']) == '':
                self.df.loc[[index], ['Data']] = data_atual
            else:
                data_atual = str(row['Data'])

    def __filtro_linhas(self):
        """
        Ajusta linhas sem histórico e filtra linhas inválidas.
        """
        for index, row in self.df.iterrows():
            if str(row['Histórico']) == '' or\
                str(row['Histórico'])[0].isnumeric():
                linhaPai = self.df.iloc[index - 1]
                if index + 1 == len(self.df):
                    linhaFilho = self.df.iloc[index]
                else:
                    linhaFilho = self.df.iloc[index + 1]
                self.df.loc[[index], ['Histórico']] = \
                    f"{str(linhaPai['Histórico'])}  {str(linhaFilho['Histórico'])}"

        self.df = self.df[self.df.Valor != '']
        self.df = self.df[self.df.Data.apply(lambda x: x[0].isnumeric())]