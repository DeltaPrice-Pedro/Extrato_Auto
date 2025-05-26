from abc import ABCMeta, abstractmethod
import pandas as pd

class Bank:
    """
    Classe base abstrata para bancos. Define a interface e métodos utilitários para manipulação de extratos bancários.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        """
        Inicializa os atributos comuns dos bancos.
        """
        self.formatos_disp = []
        self.titulo = ''

    @abstractmethod
    def gerar_extrato(self, arquivo) -> pd.DataFrame:
        """
        Método abstrato para gerar o extrato a partir de um arquivo.
        Deve ser implementado pelas subclasses.
        """
        raise NotImplementedError("Implemente este método")

    def filt_colunas(self,arquivo, colunas):
        """
        Filtra e renomeia as colunas dos DataFrames extraídos do arquivo.
        """
        for tabelas in arquivo:
            tabelas.columns = colunas
            
        self.df = pd.concat(arquivo, ignore_index=True)
        self.df = self.df.drop('', axis=1, errors='ignore')

    def inserir_espacos(self, valor = 'Valor', troca = True,\
        ordem_espacos = [1,2,4]):
        """
        Insere colunas de espaços e ajusta a ordem das colunas 'Histórico' e 'Valor'.
        """
        if troca == True:
            #Trocar a posição de "Histórico" e "Valor"
            self.df.insert(1,'Valor', self.df.pop(valor))
            self.df.insert(2,'Histórico' ,self.df.pop('Histórico'))

        #Add espaços vazios
        self.df.insert(ordem_espacos[0],'Cód. Conta Débito','')
        self.df.insert(ordem_espacos[1],'Cód. Conta Crédito','')
        self.df.insert(ordem_espacos[2],'Cód. Histórico','')

    def col_inf(self, col = 6):
        """
        Cria a coluna 'Inf.' baseada nos valores de crédito e débito.
        """
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
        """
        Cria a coluna 'Inf.' baseada no sinal do valor (positivo/crédito ou negativo/débito).
        """
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
        """
        Retorna o título do banco.
        """
        return self.titulo
    #Cada banco possui uma gerar_extrato próprio!!