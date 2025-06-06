from file import File
from bank import Bank
from pandas import isna

class PruWallet(Bank):
    """
    Classe para processamento de extratos do PruWallet.
    """
    def __init__(self):
        super().__init__()
        self.titulo = 'PruWallet'

    def gerar_extrato(self, arquivo: File):
        """
        Gera o extrato do Bradesco a partir do arquivo fornecido.
        """
        qnt_pages = arquivo.lenght()

        tabela1 = arquivo.custom_read(area_lida=[25,0,85,100], pg=1, header=False)
        
        if qnt_pages > 1:
            arquivo_complt = arquivo.custom_read(pg=f'2-{qnt_pages}',\
                area_lida=[15,0,85,100], header= False)
            
        arquivo_complt.insert(0,tabela1[0])

        self.filt_colunas(arquivo_complt, ["", "Data", "Histórico", "Valor"])
        self.inserir_espacos()
        self.__filtro_linhas()
        self.col_inf_sinal(6)

        return self.df

    def __filtro_linhas(self):
        """
        Ajusta linhas sem histórico e filtra linhas inválidas.
        """
        to_remove = []
        for index, row in self.df.iterrows():
            if str(row.Data)[0].isnumeric():
                if isna(row.Histórico):
                    self.df.loc[[index],['Histórico']] = ' '.join(
                        [self.df['Histórico'].loc[index + sub] for sub in [-2, -1, 1]]
                    )
                    self.df.loc[[index],['Valor']] = self.df['Valor'].loc[index - 2]
                else:
                    self.df.loc[[index],['Histórico']] = ' '.join(
                        [self.df['Histórico'].loc[index + sub] for sub in [-1,0]]
                    )
                    self.df.loc[[index],['Valor']] = self.df['Valor'].loc[index - 1]
            else:
                to_remove.append(index)

        self.df.drop(to_remove, inplace=True)