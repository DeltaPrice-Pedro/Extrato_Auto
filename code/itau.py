from file import File
from bank import Bank

class IClassico_Itau:
    def extrato(self, arquivo):
        self.filt_colunas(
            arquivo.leitura_custom(area_lida= [30,0,80,80]),\
                ["Data Mov.", "", "", "Valor"])
        self.inserir_espacos(troca=False)
        self.col_inf_sinal()
        self.__col_hist()
        
        return self.df.loc[self.df['Valor'] != ''].reset_index(drop=True)

    def __col_hist(self):
        coluna_hist = []
        hist = ''
        self.df.fillna('', inplace=True)
        for index, row in self.df.iterrows():
            hist = str(row['Data Mov.'][8:])
            coluna_hist.append(hist)

            #Tirar "Histórico" de "Valor"
            self.df.loc[[index],['Data Mov.']] = str(row['Data Mov.'])[:8]

        self.df.insert(5,'Histórico',coluna_hist) #precisa passar por todas linhas de uma vez

class IDecorado_Itau:
    def extrato(self, arquivo):
        tabela1 = arquivo.leitura_custom(area_lida=[70,25,98,80], pg=1)[0]
        pg = 1

        #Mudar condição para o que diferencia o decorado do personalite
        if len(tabela1.columns) != 4: 
            tabela1 = self.ler_extensao(arquivo, 1, 3, 42)[0]
            pg = 2  

        arquivos = self.ler_extensao(arquivo, pg, pg)
        arquivos.insert(0,tabela1)
        
        self.filt_colunas(arquivos, ["Data Mov.", "Histórico", "Valor", "valor-temp"])
        self.__juntar_valores()
        self.inserir_espacos()
        self.col_inf_sinal(6)
        self.__add_datas()

        self.df = self.df.loc[self.df['Valor'] != ''].reset_index(drop=True)
        self.df = self.df.loc[self.df['Valor'] != 'saída R$'].reset_index(drop=True)

        return self.df
    
    def ler_extensao(self, arquivor: File, pg_inicio: int, pg_fim: int, topo = 10):
        arquivo = []
        baixo = 98
        for i in range(pg_inicio + 1, arquivor.lenght() - pg_fim):
            print(i)
            for baixo in range(98, topo, -10):
                arquivos = arquivor.custom_read([topo, 20, baixo, 80], i)[0]
                arquivos = arquivos.loc[:, ~arquivos.columns.str.contains('^Unnamed')]
                if len(arquivos.columns) == 4 and arquivos.iloc[0,3] == '(débitos)':
                    break
            if len(arquivos.columns) != 4:
                break
            arquivo.append(arquivos)
        return arquivo
    
    def __juntar_valores(self):
        self.df.fillna('', inplace=True)
        for index, row in self.df.iterrows():
            if row['valor-temp'] != '':
             self.df.loc[[index],['Valor']] = str(row['valor-temp'])
        self.df = self.df.drop('valor-temp', axis=1)
        self.df = self.df.loc[self.df['Valor'] != '(débitos)'].reset_index(drop=True)
    
    def __add_datas(self):
        data_atual = self.df.loc[[0],['Data Mov.']]
        for index, row in self.df.iterrows():
            if row['Data Mov.'] == '':
                self.df.loc[[index],['Data Mov.']] = data_atual
            else:
                data_atual = row['Data Mov.']

class Itau(Bank, IDecorado_Itau, IClassico_Itau):
    def __init__(self):
        super().__init__()
        self.titulo = 'Itau'

    def tipo(self, arquivo: File):
        arquivo_teste = arquivo.custom_read(area_lida=[0,0,100,100], pg=1)[0]
        arquivo_teste.fillna('', inplace=True)

        if arquivo_teste.iloc[0,0] == '':
            return True
        return False

    def gerar_extrato(self, arquivo):
        if self.tipo(arquivo) == True:
            return IDecorado_Itau.extrato(self, arquivo)
        return IClassico_Itau.extrato(self, arquivo)