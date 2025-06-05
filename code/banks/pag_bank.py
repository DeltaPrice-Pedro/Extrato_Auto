from bank import Bank
from file import File
from pandas import isna

class PagBank(Bank):
    """
    Classe para processamento de extratos do PagBank.
    """
    def __init__(self):
        super().__init__()
        self.titulo = 'PagBank'

    def gerar_extrato(self, arquivo: File):
        """
        Gera o extrato do PagBank a partir do arquivo fornecido.
        """
        qnt_pages = arquivo.lenght()

        tabela1 = self.read_firt_page(arquivo)
        
        if qnt_pages > 1:
            arquivo_complt = arquivo.custom_read(pg=f'2-{qnt_pages}',\
                area_lida=[0,0,100,100], header= False)
            
        arquivo_complt.insert(0,tabela1)

        arquivo_complt = list(
            map(lambda x: x.dropna(axis=1, how='all'), arquivo_complt)
        )
        self.filt_colunas(arquivo_complt, ["Data", "Histórico", "Valor"])
        self.inserir_espacos(troca=True)
        self.col_inf_sinal(6)
        self.__filtro_linhas()

        return self.df
    
    def read_firt_page(self, arquivo):
        tabela1 = arquivo.custom_read(area_lida=[25,0,100,100], pg=1)[0]
        return tabela1 if len(tabela1.columns) == 3 else \
            arquivo.custom_read(area_lida=[30,0,100,100], pg=1)[0]

    def __filtro_linhas(self):
        """
        Ajusta linhas do extrato do PagBank.
        """
        for index, row in self.df.iterrows():
            if isna(row.Histórico):
                self.df.loc[[index],['Histórico']] =\
                f"{self.df['Histórico'].loc[index - 1]} {self.df['Histórico'].loc[index + 1]}"

        self.df.dropna(inplace=True)
        self.df = self.df[self.df.Histórico != 'Saldo do dia']