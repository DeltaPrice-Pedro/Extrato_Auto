from bank import Bank

class SantaFe(Bank):
    def __init__(self):
        super().__init__()
        self.titulo = 'Santa Fé'

    def gerar_extrato(self, arquivo):
        self.__filt_colunas(arquivo.leitura_excel())
        self.inserir_espacos(valor= 'Valor R$')

        return self.df

    def __filt_colunas(self,arquivo):
        lista= ["Data", "Observação", "Data Balancete","Agência Origem","Lote","Num. Documento","Cod. Histórico","Histórico","Valor R$","Inf.","Detalhamento Hist."]
        self.df = arquivo.rename(columns=dict(zip(arquivo.columns, lista)))
        #Juntar históricos
        for index, row in self.df.iterrows():
            self.df.loc[[index],['Histórico']] = str(row['Histórico']).strip() + ' ' + str(row["Detalhamento Hist."]).strip()

        #Filtrando as colunas
        self.df = self.df[["Data","Histórico","Valor R$","Inf."]]

        self.df = self.df.drop([0,1,2,len(self.df)-1]).reset_index(drop=True)