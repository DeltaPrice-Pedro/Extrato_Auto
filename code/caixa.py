from bank import Bank
from file import File
import pandas as pd

class Caixa(Bank):
    def __init__(self):
        super().__init__()
        self.titulo = 'Caixa'

    def gerar_extrato(self, arquivo: File):
        arquivor = arquivo.simple_read()[0]
        arquivor.fillna(0.0, inplace=True)
        if arquivor.iloc[0,0] == 0.0:
            self.filt_colunas(self.leitura_alternativa(arquivo),["Data Mov.", "", "Histórico", "Valor"])
        else:
            self.filt_colunas(arquivo.simple_read(),["Data Mov.", "", "Histórico", "", "Valor"])
        self.inserir_espacos()
        self.col_inf()

        self.df.fillna(0.0, inplace=True)
        if arquivor.iloc[0,0] == 0.0:
            return self.df.loc[self.df['Histórico'] != 'SALDO DIA']
        return self.df.loc[self.df['Histórico'] != 0.0]

    def leitura_alternativa(self, arquivo: File) -> list[pd.DataFrame]:
        qnt_pages = arquivo.lenght()
        tabela1 = arquivo.custom_read([30,0,95,80], '1', False)[0]

        if qnt_pages > 1:
            arquivor = []
            if qnt_pages - 1 > qnt_pages:
                arquivor = arquivo.custom_read([2,0,95,80], f'2-{qnt_pages - 1}', False)
            
            for baixo in range(95, 2, -10):
                ultima = arquivo.custom_read([2,0,baixo,80], qnt_pages)[0]
                ultima.fillna(0.0, inplace=True)
                if ultima.iloc[len(ultima) - 1, 3] != 0.0:
                    break

        arquivor.append(ultima)
        arquivor.insert(0,tabela1)
        return arquivor