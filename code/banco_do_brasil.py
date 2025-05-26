from bank import Bank
from file import File

class BancoDoBrasil(Bank):
    """
    Classe para processamento de extratos do Banco do Brasil.
    """
    def __init__(self):
        super().__init__()
        self.titulo = 'Banco do Brasil'

    def gerar_extrato(self, arquivo: File):
        """
        Gera o extrato do Banco do Brasil a partir do arquivo fornecido.
        """
        qnt_pages = arquivo.lenght()

        tabela1 = arquivo.custom_read(area_lida=[25,0,98,90], pg=1, header=False)
        
        if qnt_pages > 1:
            arquivo_complt = arquivo.simple_read(pg=f'2-{qnt_pages}')
            
        arquivo_complt.insert(0,tabela1[0])

        self.filt_colunas(arquivo_complt, \
            ["Data","","", "Histórico", "", "Valor R$", ""])
        self.inserir_espacos(valor= 'Valor R$')
        self.col_inf()
        self.__filt_linhas()

        return self.df[self.df['Valor'] != 0.0]

    def __filt_linhas(self):
        """
        Ajusta linhas do DataFrame, tratando linhas sem data e concatenando históricos.
        """
        self.df.fillna(0.0, inplace=True)
        for index, row in self.df.iterrows():
            self.df.loc[[index],['Data']] = str(row['Data'])[:10]
            if row['Data'] == 0.0:
                linhaAcima = self.df.iloc[index - 1]
                self.df.loc[[index - 1],['Histórico']] =\
                    f"{str(linhaAcima['Histórico'])[3:]} {str(row['Histórico'])}"