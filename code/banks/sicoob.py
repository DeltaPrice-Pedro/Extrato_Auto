from bank import Bank
from file import File
import pandas as pd

class Sicoob(Bank):
    """
    Classe para processamento de extratos do Sicoob.
    """
    def __init__(self):
     super().__init__()
     self.titulo = 'Sicoob'

    def buscarLinhaPai(self,index, tabela):
        """
        Busca a linha pai (com data) para concatenação de históricos.
        """
        linhaAcima = tabela.iloc[index]
        if linhaAcima['Data'] != '':
            #se tiver data, é a linha pai
            return index
        #senao retorna a função com Index -1
        return self.buscarLinhaPai(index - 1, tabela)

    def gerar_extrato(self, arquivo: File):
        """
        Gera o extrato do Sicoob a partir do arquivo fornecido.
        """
        qnt_pages = arquivo.lenght()
        
        # if qnt_pages == 1:
        arq_complt = self.opcao_simples(arquivo, qnt_pages)
        #Não sei se a opção completa ainda é necessária
        # else:
            # arq_complt = self.opcao_completa(arquivo, qnt_pages)

        self.filt_colunas(arq_complt, ["Data", "", "Histórico", "Valor"])
        self.inserir_espacos()
        self.col_inf()
        self.__filt_linhas()

        return self.df

    def opcao_simples(self, arquivo: File, qnt_pages: int) -> list[pd.DataFrame]:
        """
        Lê o extrato do Sicoob no modo simples.
        """
        # index = 100
        # tabela1 = arquivo.leitura_custom([13,0,75,100])
        # while len(tabela1[0].iloc[2,0]) > 10:
        #     index = index - 10
        #     tabela1 = arquivo.leitura_custom([13,0,index,100])
        # return tabela1

        table_cplt = []
        table = arquivo.custom_read([19,0,95,100], pg=1)[0]
        if qnt_pages == 1:
            table.dropna(thresh=3, inplace = True)
            na_col = table.pop("Unnamed: 0")
            for index, row in table.iterrows():
                value = row.values[0]
                row.replace(value, value[:9], inplace= True)
            table.insert(1, "", na_col)
                            
        else:
            table_cplt = arquivo.custom_read(
                [3,0,95,100], pg=f'2-{qnt_pages}'
            ) 
        
        table_cplt.insert(0, table)
        return table_cplt

    def opcao_completa(self, arquivo: File, qnt_pages: int) -> list[pd.DataFrame]:
        """
        Lê o extrato do Sicoob no modo completo.
        """
        ver_incolor = False
        tabela1 = arquivo.custom_read(area_lida=[15,0,100,94], pg=1)[0]
        
        if tabela1.iloc[0,1] == 'Lançamentos':
            ver_incolor = True
            tabela1 = arquivo.custom_read(area_lida=[18,0,95,100], pg=1)[0]
        else:
            if len(tabela1.columns) == 5:
                tabela1.columns = ["Data", "Excluir", "Histórico","", "Valor"]
            else:
                tabela1.columns = ["Data", "Excluir", "Histórico", "Valor"]
            tabela1 = tabela1.drop('', axis=1, errors='ignore')

        if ver_incolor == True:
            arquivo_complt = arquivo.custom_read(
                area_lida=[3,0,95,100], pg=f'2-{qnt_pages}', header=False)
        else:
            arquivo_complt = arquivo.custom_read(area_lida=[0,0,100,100], pg=f'2-{qnt_pages - 1}', header=False)

            index = 70
            while True:
                ultima_pagina = arquivo.custom_read(area_lida=[0,0,index,100], pg=f'{qnt_pages}', header=False)[0]
                ultima_pagina.fillna('', inplace=True)
                if ultima_pagina.iloc[len(ultima_pagina) - 1,3] != '':
                    break
                index = index - 10
            arquivo_complt.append(ultima_pagina)
                    
        arquivo_complt.insert(0,tabela1)
        return arquivo_complt

    def __filt_linhas(self):
        """
        Ajusta linhas do extrato do Sicoob, concatenando históricos e filtrando linhas inválidas.
        """
        self.df.fillna('', inplace=True)
        for index, row in self.df.iterrows():
            if row['Data'] == ''\
                and 'SALDO DO DIA' not in row['Histórico']\
                    and index + 1 != len(self.df):
                linhaAbaixo = self.df.iloc[index + 1]
                if linhaAbaixo['Histórico'] != '':
                    indexPai = self.buscarLinhaPai(index - 1, self.df)
                    linhaPai = self.df.iloc[indexPai]
                    self.df.loc[[indexPai], ['Histórico']] = str(linhaPai['Histórico']) + ' - ' + str(row['Histórico'])
                else:
                    self.df.loc[[index + 1],['Histórico']] = str(linhaAbaixo['Histórico']) + ' - ' + str(row['Histórico'])

        self.df = self.df[self.df['Data'] != '']
        self.df = self.df[self.df['Inf.'] != '']