from bank import Bank
from file import File

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

        tabela1 = arquivo.custom_read(area_lida=[16,0,100,100], pg=1)
        
        if qnt_pages > 1:
            arquivo_complt = arquivo.custom_read(pg=f'2-{qnt_pages}',\
                area_lida=[0,0,100,100])
            
        arquivo_complt.insert(0,tabela1[0])

        self.filt_colunas(arquivo_complt, ["Data","", "Histórico","", "Valor"])
        self.inserir_espacos(troca=True)
        self.col_inf_sinal(6)
        self.__filtro_linhas()

        return self.df

    def __filtro_linhas(self):
        """
        Ajusta linhas do extrato do PagBank.
        """
        self.df.fillna('', inplace=True)
        for index, row in self.df.iterrows():
            self.df.loc[[index], ['Data']] = row.Data[:10]
            self.df.loc[[index], ['Histórico']] = str(row.Histórico).replace('A receber', '').replace('Disponível','')

        self.df = self.df[self.df.Data != '']
        self.df = self.df[self.df.Data.apply(lambda x: x[0].isnumeric())]