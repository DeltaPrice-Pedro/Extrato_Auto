from file import File
from bank import Bank
import pandas as pd

class IColorido_Inter():
    """
    Classe para processamento do extrato colorido do Banco Inter.
    """
    def extrato(self, arquivo: File):
        """
        Processa o extrato colorido do Banco Inter.
        """
        qnt_pages = arquivo.lenght()

        tabela1 = arquivo.custom_read(area_lida=[27,0,90,100], pg=1, header=False)
        
        if qnt_pages > 1:
            arquivo_complt = arquivo.custom_read(
                area_lida=[25,0,90,100], pg=f'2-{qnt_pages}', header=False)
            
        arquivo_complt.insert(0,tabela1[0])

        self.filt_colunas(arquivo_complt, ["Data","Histórico","Valor"])
        self.inserir_espacos()
        self.col_inf_sinal(6)
        self.__filtro_linhas()

        return self.df

    def __filtro_linhas(self):
        """
        Ajusta linhas do extrato colorido do Inter.
        """
        lista_tabelas = []
        data_atual = ''
        self.df.fillna('', inplace=True)
        for index, row in self.df.iterrows():
            if str(row['Data']) == '':
                linhaPai = self.df.iloc[index - 1]
                self.df.loc[[index - 1], ['Histórico']] = str(linhaPai['Histórico']) + str(row['Histórico'])
            elif str(row['Data'][0]).isdigit():
                data_atual = str(row['Data'])
            elif str(row['Data'][0]).isalpha():
                self.df.loc[[index], ['Histórico']] = str(row['Data']) + ' - ' + str(row['Histórico'])
                self.df.loc[[index], ['Data']] = data_atual
        
        lista_tabelas.append(self.df.loc[self.df['Valor'] != ''])

        self.df = pd.concat(lista_tabelas, ignore_index=True)

class IClassico_Inter():
    """
    Classe para processamento do extrato clássico do Banco Inter.
    """
    def extrato(self, arquivo: File):
        """
        Processa o extrato clássico do Banco Inter.
        """
        self.filt_colunas(
            arquivo.custom_read(area_lida= [0,0,93,77], header=False),["Data", "Valor"])
        self.__inserir_espacos()
        self.col_inf_sinal()
        self.__col_data()
        
        self.df = self.df.loc[self.df['Data'] != '']
        self.df = self.df[self.df['Valor'] != '']
        self.df = self.df[self.df['Valor'] != 'Deficiência de fala e a']

        return self.df.reset_index(drop=True)

    def __inserir_espacos(self):
        """
        Insere colunas e ajusta a ordem para o extrato clássico do Inter.
        """
        #Trocar a posição de "Histórico" e "Valor"
        self.df.insert(1,'Histórico', self.df.pop('Data'))

        #Add espaços vazios
        self.df.insert(0,'Cód. Conta Débito','')
        self.df.insert(1,'Cód. Conta Crédito','')
        self.df.insert(3,'Cód. Histórico','')

        self.df = self.df.drop([0,1,2,3,4]).reset_index(drop=True)

    def __col_data(self):
        """
        Adiciona coluna de data ao DataFrame.
        """
        coluna_data = []
        data = ''
        #Adcionar coluna data
        self.df.fillna('', inplace=True)
        for index, row in self.df.iterrows():
            if str(row['Histórico'][0]).isdigit() and 'Saldo' in str(row['Histórico']):
                pos_saldo = str(row['Histórico']).index('Saldo')
                data = str(row['Histórico'][:pos_saldo - 1])
                coluna_data.append('')
            else:
                coluna_data.append(data)

        self.df.insert(0,'Data',coluna_data) 

class Inter(Bank, IClassico_Inter, IColorido_Inter):
    """
    Classe principal para processamento de extratos do Banco Inter.
    """
    def __init__(self):
        super().__init__()
        self.titulo = 'Inter'

    def tipo(self, arquivo: File):
        """
        Determina o tipo de extrato (colorido ou clássico).
        """
        arquivo_teste = arquivo.custom_read(area_lida=[0,0,100,77], pg=1, header=False)
        arquivo_teste[0].fillna('', inplace=True)

        if arquivo_teste[0].iloc[0,0] == '':
            return True
        return False

    def gerar_extrato(self, arquivo):
        """
        Gera o extrato do Inter conforme o tipo detectado.
        """
        if self.tipo(arquivo) == True:
            return IColorido_Inter.extrato(self, arquivo)
        return IClassico_Inter.extrato(self, arquivo)