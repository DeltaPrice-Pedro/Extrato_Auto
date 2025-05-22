from abc import ABCMeta, abstractmethod
import pandas as pd

class Bank:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.formatos_disp = []
        self.titulo = ''

    @abstractmethod
    def gerar_extrato(self, arquivo) -> pd.DataFrame:
        raise NotImplementedError("Implemente este método")

    def filt_colunas(self,arquivo, colunas):
        for tabelas in arquivo:
            tabelas.columns = colunas
            
        self.df = pd.concat(arquivo, ignore_index=True)
        self.df = self.df.drop('', axis=1, errors='ignore')

    def inserir_espacos(self, valor = 'Valor', troca = True,\
        ordem_espacos = [1,2,4]):
        if troca == True:
            #Trocar a posição de "Histórico" e "Valor"
            self.df.insert(1,'Valor', self.df.pop(valor))
            self.df.insert(2,'Histórico' ,self.df.pop('Histórico'))

        #Add espaços vazios
        self.df.insert(ordem_espacos[0],'Cód. Conta Débito','')
        self.df.insert(ordem_espacos[1],'Cód. Conta Crédito','')
        self.df.insert(ordem_espacos[2],'Cód. Histórico','')

    def col_inf(self, col = 6):
        coluna_inf =[]
        #Tirar C e D de "Valor"
        for index, row in self.df.iterrows():
            if 'C' in str(row['Valor']):
                coluna_inf.append('C')
                self.df.loc[[index],['Valor']] = str(row['Valor']).replace('C','')
            elif 'D' in str(row['Valor']):
                coluna_inf.append('D')
                self.df.loc[[index],['Valor']] = str(row['Valor']).replace('D','')
            else:
                coluna_inf.append('')

        self.df.insert(col,'Inf.',coluna_inf)

    def col_inf_sinal(self, col = 5):
        coluna_inf = []
        #Tirar "-" de "Valor"
        for index, row in self.df.iterrows():
            if '-' in str(row['Valor']):
                coluna_inf.append('D')
                self.df.loc[[index],['Valor']] = str(row['Valor']).replace('-','')
            else:
                coluna_inf.append('C')

        self.df.insert(col,'Inf.',coluna_inf)

    def __str__(self) -> str:
        return self.titulo
    #Cada banco possui uma gerar_extrato próprio!!