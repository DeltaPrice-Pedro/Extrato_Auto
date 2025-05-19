from PySide6.QtWidgets import (
    QMainWindow, QApplication, QRadioButton, QVBoxLayout, QWidget,
    QTableWidgetItem, QComboBox, QSpinBox, QLineEdit, QDialogButtonBox
)
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PySide6.QtCore import QThread, QObject, Signal, QSize
from PySide6.QtGui import QPixmap, QIcon, QMovie, Qt, QFont, QMouseEvent, QBrush, QColor
from src.window_extratos import Ui_MainWindow
from os import renames, startfile, getenv
from abc import abstractmethod, ABCMeta
from traceback import print_exc
from unidecode import unidecode
from tkinter import messagebox
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from pymysql import connect
from pathlib import Path
import tabula as tb
import pandas as pd
import sys

load_dotenv(Path(__file__).parent / 'src' / 'env' / '.env')

class Change:
    def __init__(self):
        self.add = []
        self.updt = {}
        self.remove = []
        pass
    def to_add(self, *args):
        self.add.append(*args)

    def to_updt(self, id, *args):
        self.updt[id] = args
    
    def to_remove(self, id):
        self.remove.append(id)

    def data(self):
        return self.add, self.updt, self.remove


class DataBase:
    COMPANIE_TABLE = 'Companie'
    BANK_TABLE = 'Bank'
    REFERENCE_TABLE = 'Reference'

    def __init__(self) -> None:
        self.connection = connect(
                host= getenv('IP_HOST'),
                port= int(getenv('PORT_HOST')),
                user= getenv('USER'),
                password= getenv('PASSWORD'),
                database= getenv('DB'),
            )
        
        self.columns_reference = [
            'id_reference', 'word', 'value', 'release_letter' 
        ]

        self.query_bank = (
            f'SELECT id_bank, name, code FROM {self.BANK_TABLE} '
        )

        self.query_companie = (
            f'SELECT id_companie, name FROM {self.COMPANIE_TABLE} '
            'WHERE id_bank = %s '
        )

        self.query_reference =  (
            f'SELECT {', '.join(self.columns_reference)} '
            f'FROM {self.REFERENCE_TABLE} '
            'WHERE id_bank = %s AND id_companie = %s'
        )

        self.insert_pedency = (
            f'INSERT INTO {self.REFERENCE_TABLE} '
            '(id_bank, id_companie, word, '
            'value, release_letter) '
            'VALUES (%(id_bank)s, %(id_companie)s,'
            '%(Palavra)s, %(Conta)s, %(Lançamento)s)'
        )

        self.insert_companie = (
            f'INSERT INTO {self.COMPANIE_TABLE} '
            '(id_bank, name) VALUES (%s, %s) '
        )

        self.update_reference = (
            f'UPDATE {self.REFERENCE_TABLE} SET '
            'word = %(Palavra)s, value = %(Conta)s, '
            'release_letter = %(Lançamento)s '
            'WHERE id_reference = %(id_reference)s '
        )

        self.delete_reference = (
            f'DELETE FROM {self.REFERENCE_TABLE} '
            'WHERE id_reference = %s ; '
        )

        pass

    def add_companie(self, id_bank, name):
        cursor = self.__request(self.insert_companie, (id_bank, name,))
        return cursor.lastrowid

    def companie(self, id_bank: int) -> dict[int, str]:
        cursor = self.__request(self.query_companie, (id_bank,))
        return { id: nome for id, nome in cursor.fetchall() }

    def bank(self) -> dict[str, int]:
        cursor = self.__request(self.query_bank)
        return { 
            f'{name} - {code}': id for id, name, code in cursor.fetchall()
        }
    
    def reference(self, id_bank: int, id_companie: int):
        cursor = self.__request(self.query_reference, (id_bank, id_companie))
        data = {key: [] for key in self.columns_reference}
        for sub in cursor.fetchall():
            for index, i in enumerate(sub):
                data[self.columns_reference[index]].append(i)
            
        ids = data.pop('id_reference')
        return ids, data
    
    def execute_change(self, id_bank, id_companie: str, change: Change):
        #list[dict], dict[tuple[dict]], list[int]
        add, updt, remove = change.data()

        #ADD
        if any(add):
            self.__tranform_add(id_bank, id_companie, add)
            self.__request(self.insert_pedency, add, True)

        #UPDATE
        if any(updt):
            for id_reference, data in updt.items():
                data['id_reference'] = id_reference
            self.__request(self.update_reference, updt, True)

        #REMOVE
        if any(remove):
            # ([id_companie, id_data] for id_data in data)
            self.__request(self.delete_reference, remove, True)


    def __tranform_add(self, id_bank, id_companie, add):
        for data in add:
            data['id_bank'] = id_bank
            data['id_companie'] = id_companie

    def __request(self, query, input = (), many = False):
        with self.connection.cursor() as cursor:
            func = cursor.executemany if many else cursor.execute
            func(query, input)
            self.connection.commit()
        return cursor

class File:
    #Cada arquivo possui um banco
    def __init__(self):
        self.path = ''

    def simple_read(self, pg = 'all', header = True) -> list[pd.DataFrame]:
        if header == False:
            return tb.read_pdf(self.path, pages= pg, stream=True, encoding="ISO-8859-1", pandas_options={'header': None})
        
        return tb.read_pdf(self.path, pages= pg, stream=True, 
        encoding="ISO-8859-1")

    def custom_read(self, area_lida, pg = 'all', header = True) -> list[pd.DataFrame]:
        if header == False:
            return tb.read_pdf(self.path, pages= pg, stream= True,\
                        relative_area=True, area= area_lida,\
                            pandas_options={"header":None}, encoding="ISO-8859-1")
        
        return tb.read_pdf(self.path, pages= pg, stream= True,\
                        relative_area=True, area= area_lida, encoding="ISO-8859-1")
    
    def excel_read(self):
        return pd.read_excel(self.path)
    
    def lenght(self):
        return len(PdfReader(self.path).pages)

    def set_path(self, caminho) -> str:
        if caminho == '':
            return None
        self.path = self.valided_path(caminho)
        return self.path[self.path.rfind('/') + 1:]
    
    def get_path(self) -> str:
        return self.path[self.path.rfind('/') + 1:]

    def __type(self, caminho) -> str:
        return caminho[ len(caminho) -3 :].lower()
    
    def valided_path(self, caminho) -> str:
        if self.__type(caminho).lower() not in ['pdf', 'lsx']:
            raise Exception('Formato de arquivo inválido')

        caminho_acsii = self.__ascii(caminho)
        if caminho != caminho_acsii:
            caminho = caminho_acsii
            messagebox.showinfo(title='Aviso', message='O caminho do arquivo precisou ser mudado, para encontrá-lo novamente siga o caminho a seguir: \n' + caminho)
        
        return caminho

    def __ascii(self, caminho) -> str:
        caminho_uni = unidecode(caminho)
        renames(caminho, caminho_uni)
        return caminho_uni

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

class BancoDoBrasil(Bank):
    def __init__(self):
        super().__init__()
        self.titulo = 'Banco do Brasil'

    def gerar_extrato(self, arquivo: File):
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
        self.df.fillna(0.0, inplace=True)
        for index, row in self.df.iterrows():
            self.df.loc[[index],['Data']] = str(row['Data'])[:10]
            if row['Data'] == 0.0:
                linhaAcima = self.df.iloc[index - 1]
                self.df.loc[[index - 1],['Histórico']] =\
                    f"{str(linhaAcima['Histórico'])[3:]} {str(row['Histórico'])}"

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

class Sicoob(Bank):
    def __init__(self):
     super().__init__()
     self.titulo = 'Sicoob'

    def buscarLinhaPai(self,index, tabela):
        linhaAcima = tabela.iloc[index]
        if linhaAcima['Data'] != '':
            #se tiver data, é a linha pai
            return index
        #senao retorna a função com Index -1
        return self.buscarLinhaPai(index - 1, tabela)

    def gerar_extrato(self, arquivo: File):
        qnt_pages = arquivo.lenght()
        
        # if qnt_pages == 1:
        arq_complt = self.opcao_simples(arquivo, qnt_pages)
        #Não sei se a opção completa ainda é necessária
        # else:
            # arq_complt = self.opcao_completa(arquivo, qnt_pages)

        self.filt_colunas(arq_complt, ["Data", "", "Histórico", "Valor"])
        self.inserir_espacos()
        self.col_inf()
        self.__filt_linhas()

        return self.df

    def opcao_simples(self, arquivo: File, qnt_pages: int) -> list[pd.DataFrame]:
        # index = 100
        # tabela1 = arquivo.leitura_custom([13,0,75,100])
        # while len(tabela1[0].iloc[2,0]) > 10:
        #     index = index - 10
        #     tabela1 = arquivo.leitura_custom([13,0,index,100])
        # return tabela1

        table_cplt = []
        table = arquivo.custom_read([19,0,95,100], pg=1)[0]
        if qnt_pages == 1:
            table.dropna(thresh=3, inplace = True)
            na_col = table.pop("Unnamed: 0")
            for index, row in table.iterrows():
                value = row.values[0]
                row.replace(value, value[:9], inplace= True)
            table.insert(1, "", na_col)
                            
        else:
            table_cplt = arquivo.custom_read(
                [3,0,95,100], pg=f'2-{qnt_pages}'
            ) 
        
        table_cplt.insert(0, table)
        return table_cplt

    def opcao_completa(self, arquivo: File, qnt_pages: int) -> list[pd.DataFrame]:
        ver_incolor = False
        tabela1 = arquivo.custom_read(area_lida=[15,0,100,94], pg=1)[0]
        
        if tabela1.iloc[0,1] == 'Lançamentos':
            ver_incolor = True
            tabela1 = arquivo.custom_read(area_lida=[18,0,95,100], pg=1)[0]
        else:
            if len(tabela1.columns) == 5:
                tabela1.columns = ["Data", "Excluir", "Histórico","", "Valor"]
            else:
                tabela1.columns = ["Data", "Excluir", "Histórico", "Valor"]
            tabela1 = tabela1.drop('', axis=1, errors='ignore')

        if ver_incolor == True:
            arquivo_complt = arquivo.custom_read(
                area_lida=[3,0,95,100], pg=f'2-{qnt_pages}', header=False)
        else:
            arquivo_complt = arquivo.custom_read(area_lida=[0,0,100,100], pg=f'2-{qnt_pages - 1}', header=False)

            index = 70
            while True:
                ultima_pagina = arquivo.custom_read(area_lida=[0,0,index,100], pg=f'{qnt_pages}', header=False)[0]
                ultima_pagina.fillna('', inplace=True)
                if ultima_pagina.iloc[len(ultima_pagina) - 1,3] != '':
                    break
                index = index - 10
            arquivo_complt.append(ultima_pagina)
                    
        arquivo_complt.insert(0,tabela1)
        return arquivo_complt

    def __filt_linhas(self):
        self.df.fillna('', inplace=True)
        for index, row in self.df.iterrows():
            if row['Data'] == ''\
                and 'SALDO DO DIA' not in row['Histórico']\
                    and index + 1 != len(self.df):
                linhaAbaixo = self.df.iloc[index + 1]
                if linhaAbaixo['Histórico'] != '':
                    indexPai = self.buscarLinhaPai(index - 1, self.df)
                    linhaPai = self.df.iloc[indexPai]
                    self.df.loc[[indexPai], ['Histórico']] = str(linhaPai['Histórico']) + ' - ' + str(row['Histórico'])
                else:
                    self.df.loc[[index + 1],['Histórico']] = str(linhaAbaixo['Histórico']) + ' - ' + str(row['Histórico'])

        self.df = self.df[self.df['Data'] != '']
        self.df = self.df[self.df['Inf.'] != '']

class IColorido_Inter():
    def extrato(self, arquivo: File):
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
    def extrato(self, arquivo: File):
        self.filt_colunas(
            arquivo.custom_read(area_lida= [0,0,100,77], header=False),["Data", "Valor"])
        self.__inserir_espacos()
        self.col_inf_sinal()
        self.__col_data()
        
        self.df = self.df.loc[self.df['Data'] != '']
        self.df = self.df[self.df['Valor'] != '']
        self.df = self.df[self.df['Valor'] != 'Deficiência de fala e a']

        return self.df.reset_index(drop=True)

    def __inserir_espacos(self):
        #Trocar a posição de "Histórico" e "Valor"
        self.df.insert(1,'Histórico', self.df.pop('Data'))

        #Add espaços vazios
        self.df.insert(0,'Cód. Conta Débito','')
        self.df.insert(1,'Cód. Conta Crédito','')
        self.df.insert(3,'Cód. Histórico','')

        self.df = self.df.drop([0,1,2,3,4]).reset_index(drop=True)

    def __col_data(self):
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
    def __init__(self):
        super().__init__()
        self.titulo = 'Inter'

    def tipo(self, arquivo: File):
        arquivo_teste = arquivo.custom_read(area_lida=[0,0,100,77], pg=1, header=False)
        arquivo_teste[0].fillna('', inplace=True)

        if arquivo_teste[0].iloc[0,0] == '':
            return True
        return False

    def gerar_extrato(self, arquivo):
        if self.tipo(arquivo) == True:
            return IColorido_Inter.extrato(self, arquivo)
        return IClassico_Inter.extrato(self, arquivo)

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

class MercadoPago(Bank):
    def __init__(self):
        super().__init__()
        self.titulo = 'Mercado Pago'

    def gerar_extrato(self, arquivo: File):
        qnt_pages = arquivo.lenght()

        tabela1 = arquivo.custom_read(area_lida=[27,0,100,100], pg=1)
        
        if qnt_pages > 1:
            arquivo_complt = arquivo.simple_read(pg=f'2-{qnt_pages}')
            
        arquivo_complt.insert(0,tabela1[0])

        self.filt_colunas(arquivo_complt, ["Data", "Histórico", "", "Valor", ""])
        self.inserir_espacos(troca=True)
        self.col_inf_sinal(6)
        self.__filtro_linhas()

        return self.df

    def __filtro_linhas(self):
        lista_tabelas = []
        self.df.fillna('', inplace=True)
        for index, row in self.df.iterrows():
            if str(row['Data']) == '':
                if index != len(self.df) and self.df.iloc[index + 1]['Data'] != ''\
                    and self.df.iloc[index - 2]['Data'] != '' \
                        or self.df.iloc[index - 2]['Histórico'] not in self.df.iloc[index - 1]['Histórico']:
                    linhaFilho = self.df.iloc[index + 1]
                    self.df.loc[[index + 1], ['Histórico']] = \
                    f"{str(row['Histórico'])}  {str(linhaFilho['Histórico'])}" 
                else:
                    linhaPai = self.df.iloc[index - 1]
                    self.df.loc[[index - 1], ['Histórico']] = \
                    f"{str(linhaPai['Histórico'])}  {str(row['Histórico'])}"

        lista_tabelas.append(self.df.loc[self.df['Data'] != ''])
        self.df = pd.concat(lista_tabelas, ignore_index=True)

class Bradesco(Bank):
    def __init__(self):
        super().__init__()
        self.titulo = 'Bradesco'

    def gerar_extrato(self, arquivo: File):
        qnt_pages = arquivo.lenght()

        tabela1 = arquivo.custom_read(area_lida=[25,0,100,80], pg=1)
        
        if qnt_pages > 1:
            arquivo_complt = arquivo.custom_read(pg=f'2-{qnt_pages}',\
                area_lida=[8,0,100,100])
            
        arquivo_complt.insert(0,tabela1[0])

        self.__filtro_colunas(arquivo_complt)
        self.inserir_espacos(troca=False, ordem_espacos=[1,2,3])
        self.__col_inf()
        self.__col_data()
        self.__filtro_linhas()

        return self.df

    def __filtro_colunas(self, arquivo):
        for tabelas in arquivo:
            if len(tabelas.columns) != 6:
                tabelas.columns = ["Data", "Histórico", "Crédito", "Débito", ""]
                continue 
            tabelas.columns = ["Data", "Histórico", "", "Crédito", "Débito"]

        self.df = pd.concat(arquivo, ignore_index=True)
        self.df = self.df.drop('', axis=1)

    def __col_inf(self):
        coluna_inf = []
        coluna_valor = []
        self.df.fillna('', inplace=True)
        for index, row in self.df.iterrows():
            if str(row['Débito']) != '':
                coluna_inf.append('D')
                coluna_valor.append(str(row['Débito']).replace('-',''))
            elif str(row['Crédito']) != '':
                    coluna_inf.append('C')
                    coluna_valor.append(str(row['Crédito']))
            else:
                    coluna_valor.append('')
                    coluna_inf.append('')

        self.df.insert(3, 'Valor', coluna_valor)
        self.df.insert(6,'Inf.', coluna_inf)
        self.df = self.df.drop('Débito', axis=1)
        self.df = self.df.drop('Crédito', axis=1)

    def __col_data(self):
        data_atual = ''
        for index, row in self.df.iterrows():
            if str(row['Data']) == '':
                self.df.loc[[index], ['Data']] = data_atual
            else:
                data_atual = str(row['Data'])

    def __filtro_linhas(self):
        for index, row in self.df.iterrows():
            if str(row['Histórico']) == '' or\
                str(row['Histórico'])[0].isnumeric():
                linhaPai = self.df.iloc[index - 1]
                if index + 1 == len(self.df):
                    linhaFilho = self.df.iloc[index]
                else:
                    linhaFilho = self.df.iloc[index + 1]
                self.df.loc[[index], ['Histórico']] = \
                    f"{str(linhaPai['Histórico'])}  {str(linhaFilho['Histórico'])}"

        self.df = self.df[self.df.Valor != '']
        self.df = self.df[self.df.Data.apply(lambda x: x[0].isnumeric())]

class PagBank(Bank):
    def __init__(self):
        super().__init__()
        self.titulo = 'PagBank'

    def gerar_extrato(self, arquivo: File):
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
        self.df.fillna('', inplace=True)
        for index, row in self.df.iterrows():
            self.df.loc[[index], ['Data']] = row.Data[:10]
            self.df.loc[[index], ['Histórico']] = str(row.Histórico).replace('A receber', '').replace('Disponível','')

        self.df = self.df[self.df.Data != '']
        self.df = self.df[self.df.Data.apply(lambda x: x[0].isnumeric())]

class Gerador(QObject):
    inicio = Signal(bool)
    fim = Signal(bool)

    def __init__(self, banco: Bank, arquivo: File, id_banco: int, relacoes: dict[int, str]) -> None:
        super().__init__()
        self.banco = banco
        self.arquivo = arquivo
        self.id_banco = id_banco
        self.relacoes = relacoes

    def extrato(self):
        try:
            self.inicio.emit(True)
            arquivo_final = self.banco.gerar_extrato(self.arquivo)

            if self.relacoes != {}:
                arquivo_final = self.prog_contabil(arquivo_final)

            self.abrir(arquivo_final)
            self.fim.emit(False)

        except Exception as error:
            print_exc()
            messagebox.showerror(title='Aviso', message= f"Erro ao extrair a tabela: confira se o banco foi selecionado corretamente, caso contrário, comunique o desenvolvedor \n\n- erro do tipo: {error}")
        finally:
            self.fim.emit(False)

    def prog_contabil(self, arquivo_final: pd.DataFrame):
        arquivo_novo = arquivo_final.copy(True)

        for index, row in arquivo_novo.iterrows():
            if row['Inf.'] == 'C':
                row['Cód. Conta Débito'] = self.id_banco
            else:
                row['Cód. Conta Crédito'] = self.id_banco

            for id_emp, key_banco in self.relacoes.items():
                if key_banco in str(row['Histórico']).lower():
                    if  row['Cód. Conta Débito'] == '':
                        row['Cód. Conta Débito'] = id_emp
                    else:
                        row['Cód. Conta Crédito'] = id_emp
                    continue

        return arquivo_novo
    
    def abrir(self, arquivo_final: pd.DataFrame):
        file = asksaveasfilename(title='Favor selecionar a pasta onde será salvo', filetypes=((".xlsx","*.xlsx"),))

        if file == '':
            resp = messagebox.askyesno(title='Aviso', message= 'Deseja cancelar a operação?')
            if resp == True:
                messagebox.showinfo(title='Aviso', message= 'Operação cancelada!')
                return None
            else:
                return self.abrir(arquivo_final)

        arquivo_final.to_excel(file+'.xlsx', index=False)
        messagebox.showinfo(title='Aviso', message='Abrindo o arquivo gerado!')
        startfile(file+'.xlsx')

class MainWindow(QMainWindow, Ui_MainWindow):
    PLCHR_COMBOBOX = 'Selecione a opção'

    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.db = DataBase()
        self.companies_checkbox = {}
        self.min_carc_companie = 6

        self.message_select = 'Primeiro, clique 1 vez na empresa que deseja {0}'
        self.message_remove = 'Confirma a remoção desta empresa?\nTodas suas pendências e emails cadastrados também serão excluídos'
        self.message_save = 'Tem certeza que deseja salvar estas alterações?'
        self.message_pending_save = 'Antes de recarregar os dados, faça ou cancele o salvamento das alterações pendentes'
        self.message_no_save = 'Não há alterações a serem salvas'
        self.message_exit_save = 'Tem certeza que deseja sair da empresa SEM SALVAR as mudanças feitas nela?\n\nCaso não queira PERDER as alterações, selecione "não" e as salve'
        self.message_send_email = 'Confirma o envio dessas pendências aos emails cadastrados?'

        self.current_operation = ''
        self.ref_operation = {
            'add': self.confirm_add_refence,
            'updt': self.confirm_updt_reference
        }

        self.add_brush = QBrush(QColor(179, 255, 178, 255))
        self.add_brush.setStyle(Qt.BrushStyle.Dense1Pattern)

        self.updt_brush = QBrush(QColor(189, 253, 254, 255))
        self.updt_brush.setStyle(Qt.BrushStyle.Dense1Pattern)

        self.remove_brush = QBrush(QColor(254, 139, 139, 255))
        self.remove_brush.setStyle(Qt.BrushStyle.Dense1Pattern)

        self.no_brush = QBrush(Qt.BrushStyle.NoBrush)

        self.default_resp = [
            '', '0', 'C'
        ]

        self.ref_input = {
            QComboBox : lambda value, widget: widget.\
                setCurrentIndex(['C','D'].index(value)),
            QSpinBox : lambda value, widget: widget.setValue(int(value)),
            QLineEdit : lambda value, widget: widget.setText(value)
        }

        self.ref_input_text = {
            QComboBox : lambda widget: widget.currentText(),
            QLineEdit : lambda widget: widget.text(),
            QSpinBox : lambda widget: widget.text(),
        }

        self.inputs = [
            self.lineEdit_word, self.spinBox_value, self.comboBox_release
        ]

        self.dict_nick_bank = {
            'caixa': Caixa(),
            'santa fé' : SantaFe(),
            'santa fe' :SantaFe(),
            'banco do brasil': BancoDoBrasil(),
            'bb' : BancoDoBrasil(),
            'sicoob': Sicoob(),
            'inter' : Inter(),
            'itaú': Itau(),
            'itau': Itau(),
            'mercado pago': MercadoPago(),
            'bradesco': Bradesco(),
            'pagbank': PagBank(),
        }

        self.connections = {}
        self.ref_universal = {
            'companies': [
                {
                    self.pushButton_add: self.add_companie,
                    # self.pushButton_remove: self.remove_companie,
                    # self.pushButton_update: self.update_companie,
                    # self.pushButton_reload: self.fill_companie,
                },
                {
                    self.pushButton_add: 'Adciona empresa a lista de empresas cadastradas',
                    self.pushButton_remove: 'Remove empresa cadastrada',
                    self.pushButton_update: 'Edita o nome de empresa cadastrada',
                }
            ],
            'reference': [
                {
                    self.pushButton_add: self.add_reference,
                    self.pushButton_remove: self.remove_reference,
                    self.pushButton_save: self.save_reference,
                    # self.pushButton_reload: self.fill_reference,
                },
                {
                    self.pushButton_add: 'Adciona imposto a lista de impostos cadastrados',
                    self.pushButton_remove: 'Remove imposto cadastrado',
                    self.pushButton_save: 'Edita o nome de imposto cadastrado',
                    # self.pushButton_reload: '',
                }
            ]
        }

        self.enable_status = True
        self.ref_disable_btns = [
            self.pushButton_add,
            self.pushButton_remove,
            self.pushButton_save,
            self.pushButton_update,
            self.pushButton_execute,
            self.pushButton_exit
        ]
        self.disable_buttons()
        self.label_companie_info.hide()
        self.frame_operations.hide()
        self.switch_focus('companies')

        self.dict_bank_text = self.db.bank()
        self.comboBox.setPlaceholderText(self.PLCHR_COMBOBOX)
        self.comboBox.addItems(list(self.dict_bank_text.keys()))
        
        self.checkBox_font = QFont()
        self.checkBox_font.setFamilies([u"Bahnschrift"])
        self.checkBox_font.setWeight(QFont.Weight.Light)
        self.checkBox_font.setPointSize(14)

        self.arquivo = File()
        self.setWindowIcon(QIcon(
            (Path(__file__).parent / 'src' / 'imgs' / 'extr-icon.ico').__str__()
            )
        )
        self.setWindowTitle('Conversor de Extrato')

        self.movie = QMovie(
            (Path(__file__).parent / 'src'/ 'imgs' / 'load.gif').__str__()
        )
        self.label_load.setMovie(self.movie)

        icon = QIcon()
        icon.addFile(
            (Path(__file__).parent / 'src'/ 'imgs' / 'upload-icon.png').__str__(),
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off
        )
        self.pushButton_upload.setIcon(icon)

        #Logo
        self.logo_hori.setPixmap(QPixmap(
                (Path(__file__).parent / 'src' / 'imgs' / 'extrato_horizontal.png').__str__()
            )
        )
        self.pushButton_save.setHidden(True)

        self.table_reference.itemDoubleClicked.connect(self.updt_reference)
        self.comboBox.currentTextChanged.connect(self.search_companie)
        self.pushButton_upload.clicked.connect(self.attach)
        self.pushButton_execute.clicked.connect(self.execute)
        self.pushButton_confirm.clicked.connect(self.confirm)

        self.pushButton_add.clicked.connect(self.in_operation)
        self.pushButton_update.clicked.connect(self.in_operation)
        self.pushButton_cancel.clicked.connect(self.in_operation)
        self.pushButton_confirm.clicked.connect(self.in_operation)
        self.pushButton_cancel.clicked.connect(
            lambda: self.stackedWidget_reference.setCurrentIndex(0)
        )
        self.pushButton_exit.clicked.connect(
            lambda: self.stackedWidget_companie.setCurrentIndex(0)
        )

    def in_operation(self):
        self.disable_buttons()
        hide = not self.frame_operations.isHidden()
        self.frame_operations.setHidden(hide)
        
    def disable_buttons(self):
        self.enable_status = not self.enable_status
        for item in self.ref_disable_btns:
            item.setEnabled(self.enable_status)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        widget = self.childAt(event.position())
        if widget is not None and type(widget) == QRadioButton :
            self.open_reference(widget) 

    def switch_focus(self, current_widget: str):
        ref_connection = {}
        ref_tool_tip = {}

        ref_connection, ref_tool_tip = self.ref_universal[current_widget]
        self.re_connection(ref_connection)
        self.re_tool_tip(ref_tool_tip)

    def re_connection(self, ref):
        for widget, connection in self.connections.items():
            widget.disconnect(connection)
        self.connections.clear()

        for widget, func in ref.items():
            self.connections[widget] = widget.clicked.connect(func)

    def re_tool_tip(self, ref):
        for widget, text in ref.items():
            widget.setToolTip(text)

    def open_reference(self, radio: QRadioButton):
        self.switch_focus('reference')
        self.label_current_companie.setText(radio.text())
        self.current_companie_id = self.companies_checkbox[radio]
        id_bank = self.dict_bank_text[self.comboBox.currentText()]

        self.fill_reference(id_bank)

        self.pushButton_save.setHidden(False)
        self.pushButton_update.setHidden(True)
        self.stackedWidget_companie.setCurrentIndex(1)

    def fill_reference(self, id_bank):
        self.table_reference.clearContents()

        ids, data = self.db.reference(id_bank, self.current_companie_id)
        self.table_reference.setColumnCount(len(data.keys()))
        self.table_reference.setRowCount(len(ids))
        for column, column_data in enumerate(data.values()):
            for row, value in enumerate(column_data):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.__setattr__('id', ids[row])
                item.__setattr__('edited', False)
                item.setText(str(value))
                self.table_reference.setItem(row, column, item)

    def confirm(self):
        self.ref_operation[self.current_operation]()

    def add_reference(self):
        for column in range(self.table_reference.columnCount()):
            input = self.inputs[column]
            self.ref_input[type(input)](self.default_resp[column], input)
        
        self.current_operation = 'add'
        self.stackedWidget_reference.setCurrentIndex(1)

    def confirm_add_refence(self):
        resp = self.__inputs_response()

        row = self.table_reference.rowCount()
        self.table_reference.setRowCount(row + 1)
        for column in range(self.table_reference.columnCount()):
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.__setattr__('id', None)
            item.__setattr__('edited', False)
            item.setText(resp[column])
            item.setBackground(self.add_brush)
            self.table_reference.setItem(row, column, item)
            
        self.stackedWidget_reference.setCurrentIndex(0)

    def __inputs_response(self):
        resp = []
        for input in self.inputs:
            text = self.ref_input_text[type(input)](input)
            resp.append(text)
        return resp
    
    def updt_reference(self):
        self.disable_buttons()
        item = self.table_reference.selectedItems()[0]
        row = item.row()
        for column in range(self.table_reference.columnCount()):
            item = self.table_reference.item(row, column)
            input = self.inputs[column]
            self.ref_input[type(input)](item.text(), input)

        self.current_operation = 'updt'
        self.stackedWidget_reference.setCurrentIndex(1)

    def confirm_updt_reference(self):
        bush = ''
        edited = True

        resp = self.__inputs_response()
        item = self.table_reference.selectedItems()[0]
        row = item.row()

        #Mudou mesmo?
        if self.__check_updt(resp, row) == False:
            return self.stackedWidget_reference.setCurrentIndex(0)
        
        #Esses dados já existiram nessa sessão?
        # elif self.__check_season_updt(resp) == True:
        #     bush = self.no_brush
        #     edited = False

        else:
            if None == item.__getattribute__('id'):
                bush = self.add_brush
            else:
                bush = self.updt_brush
        
        for column in range(self.table_reference.columnCount()):
            item = self.table_reference.item(row, column)
            item.__setattr__('edited', edited)
            item.setBackground(bush)
            item.setText(resp[column])

        self.stackedWidget_reference.setCurrentIndex(0)

    def __check_updt(self, resp, row):
        for column in range(self.table_reference.columnCount()):
            item = self.table_reference.item(row, column)
            if item.text() != resp[column]:
                return True
        return False
    
    def remove_reference(self):
        try:
            item = self.table_reference.selectedItems()[0]
            row = item.row()
            if item.background() == self.add_brush:
                self.table_reference.removeRow(row)
                return None
            
            bush = self.remove_brush
            if item.background() == self.remove_brush:
                bush = self.updt_brush\
                    if True == item.__getattribute__('edited')\
                        else self.no_brush

            for column in range(self.table_reference.columnCount()):
                item = self.table_reference.item(row, column)
                item.setBackground(bush)
        except IndexError:
            messagebox.showerror('Aviso', 'Primeiro, selecione a pendência que deseja remover')

    def save_reference(self):
        try:
            self.disable_buttons()

            if self.has_change() == False:
                raise Exception(self.message_no_save)
            
            if messagebox.askyesno('Aviso', self.message_save) == False:
                return None
           
            id_bank = self.dict_bank_text.get(self.comboBox.currentText())
            self.db.execute_change(
                id_bank, self.current_companie_id, self.change_reference()
            )
            self.fill_reference(id_bank)
            
            self.disable_buttons()
        except Exception as err:
            self.disable_buttons()
            messagebox.showerror('Aviso', err)

    def has_change(self)-> bool:
        for row in range(self.table_reference.rowCount()):
            item = self.table_reference.item(row, 0)
            if item.background() != self.no_brush:
                return True
        return False

    def change_reference(self) -> Change | None:
        changes = Change()
        for row in range(self.table_reference.rowCount()):
            item = self.table_reference.item(row, 0)
            brush = item.background()
            if brush == self.no_brush:
                continue

            elif brush == self.add_brush:
                data = self.__data_row(row)
                changes.to_add(data)

            elif brush == self.updt_brush:
                data = self.__data_row(row)
                changes.to_updt(
                    self.table_reference.item(row, 0)\
                        .__getattribute__('id'), 
                    data
                )

            elif brush == self.remove_brush:
                changes.to_remove(
                    self.table_reference.item(row, 0)\
                        .__getattribute__('id')
                )
        return changes
    
    def __data_row(self, row) -> dict[str]:
        data = {}
        for column in range(self.table_reference.columnCount()):
            item = self.table_reference.item(row, column)
            key = self.table_reference.horizontalHeaderItem(column)
            data[key.text()] = item.text()
        return data

    def execute(self):
        try:       
            id_bank = self.dict_bank_text.get(self.comboBox.currentText())
            reference = self.reference(id_bank)
            bank = self.bank()
            self._gerador = Gerador(
                bank,
                self.arquivo,
                id_bank,
                reference
            )
            self._thread = QThread()

            self._gerador.moveToThread(self._thread)
            self._thread.started.connect(self._gerador.extrato)
            self._gerador.fim.connect(self._thread.quit)
            self._gerador.fim.connect(self._thread.deleteLater)
            self._gerador.fim.connect(self.alter_estado)
            self._gerador.inicio.connect(self.alter_estado)
            
            self._thread.finished.connect(self._gerador.deleteLater)
            self._thread.start() 

        except PermissionError:
            messagebox.showerror(title='Aviso', message= 'Feche o arquivo gerado antes de criar outro')
        except FileNotFoundError:
            messagebox.showerror(title='Aviso', message= "Arquivo indisponível")
        except Exception as error:
            messagebox.showerror(title='Aviso', message= error)
        finally:
            self.alter_estado(False)

    def alter_estado(self, cond: bool):
        self.exec_load(cond)
        self.pushButton_executar.setDisabled(cond)

    def exec_load(self, action: bool):
        if action == True:
            self.movie.start()
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.movie.stop()
            self.stackedWidget.setCurrentIndex(0)

    def search_companie(self):
        if self.scrollArea.isEnabled() == False:
            self.scrollArea.setDisabled(False)
            self.label_aviso.hide()
            self.vbox = QVBoxLayout()
            self.label_companie_info.setHidden(False)
            self.disable_buttons()
        else:
            self.scrollArea.widget().destroy()
            for checkBox in self.companies_checkbox.keys():
                self.vbox.removeWidget(checkBox)
                checkBox.destroy()

        widget = QWidget()
        self.fill_companie()

        widget.setLayout(self.vbox)
        self.scrollArea.setWidget(widget)

    def fill_companie(self):
        empresas_disp = self.db.companie(
            self.dict_bank_text[self.comboBox.currentText()]
        )

        self.companies_checkbox.clear()
        for id_emp, nome_emp in empresas_disp.items():
            self.create_companie(id_emp, nome_emp)

    def create_companie(self, id_emp, nome_emp):
        item = QRadioButton(nome_emp)
        item.__setattr__('id', id_emp)
        item.setFont(self.checkBox_font)
        self.companies_checkbox[item] = id_emp
        self.vbox.addWidget(item)

    def add_companie(self):
        self.pushButton_confirm.hide()
        item = QLineEdit(placeholderText='Nome da empresa (min. 6 caracteres)')
        # item.setFont(self.font)
        item.__setattr__('id', None)
        item.textChanged.connect(self.companie_valid)
        
        self.current_item_edited = item
        self.vbox.addWidget(item)

    def confirm_add_companie(self):
        try:
            item = self.current_item_edited
            name = item.text()
            if name == '':
                raise Exception('Nome de empresa inválida')
            
            id = item.__getattribute__('id')
            if id == None:
                id_bank = self.dict_bank_text.get(self.comboBox.currentText())
                id = self.db.add_companie(id_bank, name)
                self.create_companie(id, name)
                item.deleteLater()
            else:
                self.db.edit_companie(id, name)

            self.in_operation()
        except Exception as error:
            messagebox.showwarning('Aviso', error)

    def companie_valid(self):
        hide = True
        if len(self.current_item_edited.text()) > self.min_carc_companie:
            hide = False
        self.pushButton_confirm.setHidden(hide)

    def reference(self, id_bank: int) -> int:
        for widget, id_emp in self.companies_checkbox.items():
            if widget.isChecked():
                return self.db.reference(id_bank, id_emp)
        return {}

    def bank(self) -> Bank:
        for key, bank in self.dict_nick_bank.items():
            if key in self.comboBox.currentText().lower():
                return bank

    def attach(self):
        try:
            file_stem = self.arquivo.set_path(askopenfilename())
            if file_stem != None:
                self.pushButton_upload.setText(file_stem)
                self.pushButton_upload.setIcon(QPixmap(''))

                self.select_combo(file_stem)

        except PermissionError:
            messagebox.showerror(title='Aviso', message= 'O arquivo selecionado apresenta-se em aberto em outra janela, favor fecha-la')
        except FileExistsError:
            messagebox.showerror(title='Aviso', message= 'O arquivo selecionado já apresenta uma versão sem acento, favor usar tal versão ou apagar uma delas')
        except Exception as error:
            messagebox.showerror(title='Aviso', message= error)

    def select_combo(self, file_stem: str):
        for key in self.dict_nick_bank.keys():
            if key in file_stem.lower():
                self.comboBox.setCurrentIndex(
                    self.comboBox.findText(
                        key, Qt.MatchFlag.MatchContains
                    )
                )

if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()