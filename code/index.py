from tkinter.filedialog import askopenfilename, asksaveasfilename
from abc import abstractmethod, ABCMeta
from unidecode import unidecode
from tkinter import messagebox
from PyPDF2 import PdfReader
import tabula as tb
import pandas as pd
from traceback import print_exc
from sqlite3 import connect
import sys
from os import renames, startfile, path

from PySide6.QtWidgets import (
    QMainWindow, QApplication, QRadioButton, QVBoxLayout, QWidget
)
from PySide6.QtGui import QPixmap, QIcon, QMovie
from PySide6.QtCore import QThread, QObject, Signal, QSize
from src.window_extratos import Ui_MainWindow

def resource_path(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        path.dirname(path.abspath(__file__)))
    return path.join(base_path, relative_path)

class DataBase:
    NOME_DB = 'prog_contabil.sqlite3'
    ARQUIVO_DB = resource_path(f'src\\db\\{NOME_DB}')
    TABELA_BANCO = 'Banco'
    TABELA_RELACAO = 'Relacao'
    TABELA_EMP = 'Empresa'

    def __init__(self) -> None:
        self.query_id_banco = 'SELECT id_banco FROM {0} WHERE nome = "{1}"'

        self.query_id_nome_emp = 'SELECT id_empresa, nome  FROM {0} WHERE id_banco = "{1}"'

        self.query_codEmp_keyBanco =  'SELECT codigo_emp, chave_banco FROM {0} WHERE id_banco = "{1}" AND id_empresa = "{2}"'


        self.connection = connect(self.ARQUIVO_DB)
        self.cursor = self.connection.cursor()
        pass

    def clientes_do_banco(self, id_banco: int) -> dict[int, str]:
        self.cursor.execute(
            self.query_id_nome_emp.format(
                self.TABELA_EMP, id_banco
            )
        )
        return { id: nome for id, nome in self.cursor.fetchall() }

    def id_banco(self, nome:str) -> int:
        self.cursor.execute(
            self.query_id_banco.format(self.TABELA_BANCO, nome)
        )
        return self.cursor.fetchone()[0]
    
    def relacoes(self, id_banco: int, id_empresa: int) -> dict[int, str]:
        self.cursor.execute(
           self.query_codEmp_keyBanco.format(
               self.TABELA_RELACAO, id_banco, id_empresa
           )
        )
        return { 
            id_emp: key_banco for id_emp, key_banco in self.cursor.fetchall()
        }

    def exit(self):
        self.cursor.close()
        self.connection.close()

class Arquivo:
    #Cada arquivo possui um banco
    def __init__(self):
        self.caminho = ''

    def leitura_simples(self, pg = 'all', header = True) -> list[pd.DataFrame]:
        if header == False:
            return tb.read_pdf(self.caminho, pages= pg, stream=True, encoding="ISO-8859-1", pandas_options={'header': None})
        
        return tb.read_pdf(self.caminho, pages= pg, stream=True, 
        encoding="ISO-8859-1")

    def leitura_custom(self, area_lida, pg = 'all', header = True) -> list[pd.DataFrame]:
        if header == False:
            return tb.read_pdf(self.caminho, pages= pg, stream= True,\
                        relative_area=True, area= area_lida,\
                            pandas_options={"header":None}, encoding="ISO-8859-1")
        
        return tb.read_pdf(self.caminho, pages= pg, stream= True,\
                        relative_area=True, area= area_lida, encoding="ISO-8859-1")
    
    def leitura_excel(self):
        return pd.read_excel(self.caminho)
    
    def qnt_paginas(self):
        return len(PdfReader(self.caminho).pages)

    def set_caminho(self, caminho) -> str:
        if caminho == '':
            return None
        self.caminho = self.caminho_valido(caminho)
        return self.caminho[self.caminho.rfind('/') + 1:]
    
    def get_caminho(self) -> str:
        return self.caminho[self.caminho.rfind('/') + 1:]

    def __tipo(self, caminho) -> str:
        return caminho[ len(caminho) -3 :].lower()
    
    def caminho_valido(self, caminho) -> str:
        if self.__tipo(caminho).lower() not in ['pdf', 'lsx']:
            raise Exception('Formato de arquivo inválido')

        caminho_acsii = self.formato_ascii(caminho)
        if caminho != caminho_acsii:
            caminho = caminho_acsii
            messagebox.showinfo(title='Aviso', message='O caminho do arquivo precisou ser mudado, para encontrá-lo novamente siga o caminho a seguir: \n' + caminho)
        
        return caminho

    def formato_ascii(self, caminho) -> str:
        caminho_uni = unidecode(caminho)
        renames(caminho, caminho_uni)
        return caminho_uni

class Banco:
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

    def to_string(self) -> str:
        return self.titulo
    #Cada banco possui uma gerar_extrato próprio!!

class Caixa(Banco):
    def __init__(self):
        super().__init__()
        self.titulo = 'Caixa'

    def gerar_extrato(self, arquivo: Arquivo):
        arquivor = arquivo.leitura_simples()[0]
        arquivor.fillna(0.0, inplace=True)
        if arquivor.iloc[0,0] == 0.0:
            self.filt_colunas(self.leitura_alternativa(arquivo),["Data Mov.", "", "Histórico", "Valor"])
        else:
            self.filt_colunas(arquivo.leitura_simples(),["Data Mov.", "", "Histórico", "", "Valor"])
        self.inserir_espacos()
        self.col_inf()

        self.df.fillna(0.0, inplace=True)
        if arquivor.iloc[0,0] == 0.0:
            return self.df.loc[self.df['Histórico'] != 'SALDO DIA']
        return self.df.loc[self.df['Histórico'] != 0.0]

    def leitura_alternativa(self, arquivo: Arquivo) -> list[pd.DataFrame]:
        qnt_pages = arquivo.qnt_paginas()
        tabela1 = arquivo.leitura_custom([30,0,95,80], '1', False)[0]

        if qnt_pages > 1:
            arquivor = []
            if qnt_pages - 1 > qnt_pages:
                arquivor = arquivo.leitura_custom([2,0,95,80], f'2-{qnt_pages - 1}', False)
            
            for baixo in range(95, 2, -10):
                ultima = arquivo.leitura_custom([2,0,baixo,80], qnt_pages)[0]
                ultima.fillna(0.0, inplace=True)
                if ultima.iloc[len(ultima) - 1, 3] != 0.0:
                    break

        arquivor.append(ultima)
        arquivor.insert(0,tabela1)
        return arquivor

class BancoDoBrasil(Banco):
    def __init__(self):
        super().__init__()
        self.titulo = 'Banco do Brasil'

    def gerar_extrato(self, arquivo: Arquivo):
        qnt_pages = arquivo.qnt_paginas()

        tabela1 = arquivo.leitura_custom(area_lida=[25,0,98,90], pg=1, header=False)
        
        if qnt_pages > 1:
            arquivo_complt = arquivo.leitura_simples(pg=f'2-{qnt_pages}')
            
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

class SantaFe(Banco):
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

class Sicoob(Banco):
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

    def gerar_extrato(self, arquivo: Arquivo):
        qnt_pages = arquivo.qnt_paginas()
        
        if qnt_pages == 1:
            arq_complt = self.opcao_simples(arquivo)
        else:
            arq_complt = self.opcao_completa(arquivo, qnt_pages)

        self.filt_colunas(arq_complt, ["Data", "", "Histórico", "Valor"])
        self.inserir_espacos()
        self.col_inf()
        self.__filt_linhas()

        return self.df

    def opcao_simples(self, arquivo: Arquivo) -> list[pd.DataFrame]:
        index = 100
        tabela1 = arquivo.leitura_custom([13,0,75,100])
        while len(tabela1[0].iloc[2,0]) > 10:
            index = index - 10
            tabela1 = arquivo.leitura_custom([13,0,index,100])
        return tabela1

    def opcao_completa(self, arquivo: Arquivo, qnt_pages: int) -> list[pd.DataFrame]:
        ver_incolor = False
        tabela1 = arquivo.leitura_custom(area_lida=[15,0,100,94], pg=1)[0]
        
        if tabela1.iloc[0,1] == 'Lançamentos':
            ver_incolor = True
            tabela1 = arquivo.leitura_custom(area_lida=[18,0,95,100], pg=1)[0]
        else:
            if len(tabela1.columns) == 5:
                tabela1.columns = ["Data", "Excluir", "Histórico","", "Valor"]
            else:
                tabela1.columns = ["Data", "Excluir", "Histórico", "Valor"]
            tabela1 = tabela1.drop('', axis=1, errors='ignore')

        if ver_incolor == True:
            arquivo_complt = arquivo.leitura_custom(
                area_lida=[3,0,95,100], pg=f'2-{qnt_pages}', header=False)
        else:
            arquivo_complt = arquivo.leitura_custom(area_lida=[0,0,100,100], pg=f'2-{qnt_pages - 1}', header=False)

            index = 70
            while True:
                ultima_pagina = arquivo.leitura_custom(area_lida=[0,0,index,100], pg=f'{qnt_pages}', header=False)[0]
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
    def extrato(self, arquivo: Arquivo):
        qnt_pages = arquivo.qnt_paginas()

        tabela1 = arquivo.leitura_custom(area_lida=[27,0,90,100], pg=1, header=False)
        
        if qnt_pages > 1:
            arquivo_complt = arquivo.leitura_custom(
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
    def extrato(self, arquivo: Arquivo):
        self.filt_colunas(
            arquivo.leitura_custom(area_lida= [0,0,100,77], header=False),["Data", "Valor"])
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

class Inter(Banco, IClassico_Inter, IColorido_Inter):
    def __init__(self):
        super().__init__()
        self.titulo = 'Inter'

    def tipo(self, arquivo: Arquivo):
        arquivo_teste = arquivo.leitura_custom(area_lida=[0,0,100,77], pg=1, header=False)
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
    
    def ler_extensao(self, arquivor: Arquivo, pg_inicio: int, pg_fim: int, topo = 10):
        arquivo = []
        baixo = 98
        for i in range(pg_inicio + 1, arquivor.qnt_paginas() - pg_fim):
            print(i)
            for baixo in range(98, topo, -10):
                arquivos = arquivor.leitura_custom([topo, 20, baixo, 80], i)[0]
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

class Itau(Banco, IDecorado_Itau, IClassico_Itau):
    def __init__(self):
        super().__init__()
        self.titulo = 'Itau'

    def tipo(self, arquivo: Arquivo):
        arquivo_teste = arquivo.leitura_custom(area_lida=[0,0,100,100], pg=1)[0]
        arquivo_teste.fillna('', inplace=True)

        if arquivo_teste.iloc[0,0] == '':
            return True
        return False

    def gerar_extrato(self, arquivo):
        if self.tipo(arquivo) == True:
            return IDecorado_Itau.extrato(self, arquivo)
        return IClassico_Itau.extrato(self, arquivo)

class MercadoPago(Banco):
    def __init__(self):
        super().__init__()
        self.titulo = 'Mercado Pago'

    def gerar_extrato(self, arquivo: Arquivo):
        qnt_pages = arquivo.qnt_paginas()

        tabela1 = arquivo.leitura_custom(area_lida=[27,0,100,100], pg=1)
        
        if qnt_pages > 1:
            arquivo_complt = arquivo.leitura_simples(pg=f'2-{qnt_pages}')
            
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

class Bradesco(Banco):
    def __init__(self):
        super().__init__()
        self.titulo = 'Bradesco'

    def gerar_extrato(self, arquivo: Arquivo):
        qnt_pages = arquivo.qnt_paginas()

        tabela1 = arquivo.leitura_custom(area_lida=[25,0,100,80], pg=1)
        
        if qnt_pages > 1:
            arquivo_complt = arquivo.leitura_custom(pg=f'2-{qnt_pages}',\
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

class PagBank(Banco):
    def __init__(self):
        super().__init__()
        self.titulo = 'PagBank'

    def gerar_extrato(self, arquivo: Arquivo):
        qnt_pages = arquivo.qnt_paginas()

        tabela1 = arquivo.leitura_custom(area_lida=[16,0,100,100], pg=1)
        
        if qnt_pages > 1:
            arquivo_complt = arquivo.leitura_custom(pg=f'2-{qnt_pages}',\
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

    def __init__(self, banco: Banco, arquivo: Arquivo, id_banco: int, relacoes: dict[int, str]) -> None:
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
        self.id_banco = -1
        self.options = {}
        self.ref = {
            'caixa': Caixa(),
            'santa fé' : SantaFe(),
            'santa fe' :SantaFe(),
            'bb' : BancoDoBrasil(),
            'banco do brasil': BancoDoBrasil(),
            'sicoob': Sicoob(),
            'inter' : Inter(),
            'itaú': Itau(),
            'itau': Itau(),
            'mercado pago': MercadoPago(),
            'bradesco': Bradesco(),
            'pagbank': PagBank(),
        }

        self.arquivo = Arquivo()

        self.setWindowIcon(QIcon(resource_path('src\\imgs\\extr-icon.ico')))
        self.setWindowTitle('Conversor de Extrato')

        self.movie = QMovie(resource_path("src\\imgs\\load.gif"))
        self.label_load.setMovie(self.movie)

        icon = QIcon()
        icon.addFile(resource_path("src\\imgs\\upload-icon.png"), QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_upload.setIcon(icon)

        #Logo
        self.logo_hori.setPixmap(QPixmap
        (resource_path('src\\imgs\\extrato_horizontal.png')))

        self.comboBox.currentTextChanged.connect(
            self.pesquisar_empresas
        )
        
        self.pushButton_upload.clicked.connect( 
            self.inserir
        )

        self.pushButton_executar.clicked.connect(
            self.executar
        )
        
        self.comboBox.setPlaceholderText(self.PLCHR_COMBOBOX)
        self.comboBox.addItems(
             ["Caixa","Banco do Brasil","Santa Fé","Sicoob", "Inter", "Itaú", "Mercado Pago", "Bradesco","PagBank"]
        )

    def executar(self):
        try:       
            id_emp = self.option_escolhida()
            if self.id_banco == -1:
                raise Exception('Escolha um banco e uma empresa, caso a que deseja não esteja disponível, marque "Não Encontrado"')

            banco = self.banco_desejado()
            relacoes = self.db.relacoes(self.id_banco, id_emp)

            self._gerador = Gerador(
                banco,
                self.arquivo,
                self.id_banco,
                relacoes
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

    def pesquisar_empresas(self):
        if self.scrollArea.isEnabled() == False:
            self.scrollArea.setDisabled(False)
            self.label_aviso.hide()
            self.vbox = QVBoxLayout()
        else:
            self.widget.destroy()
            for widget in self.options.values():
                self.vbox.removeWidget(widget)
                widget.destroy()

        self.widget = QWidget()

        self.add_options()

        self.widget.setLayout(self.vbox)
        self.scrollArea.setWidget(self.widget)

    def add_options(self):
        self.id_banco = self.db.id_banco(self.comboBox.currentText())
        empresas_disp = self.db.clientes_do_banco(self.id_banco)

        self.options.clear()
        self.options[-1] = QRadioButton('Não Encontrado')
        self.vbox.addWidget(self.options[-1])
        
        for id_emp, nome_emp in empresas_disp.items():
            self.options[id_emp] = QRadioButton(nome_emp)
            self.vbox.addWidget(self.options[id_emp])

    def option_escolhida(self) -> int:
        for id_emp, widget in self.options.items():
            if widget.isChecked():
                return id_emp
        return -1

    def banco_desejado(self) -> Banco:
        if self.comboBox.currentText() != self.PLCHR_COMBOBOX:
            for key, obj in self.ref.items():
                if key in self.comboBox.currentText().lower():
                    return obj
        else:
            nome_arq = self.arquivo.get_caminho().lower()
            for chave, obj in self.ref.items():
                if chave in nome_arq:
                    return obj
        raise Exception('Nome do banco não identificado no arquivo, favor seleciona-lo')

    def inserir(self):
        try:
            caminho = self.arquivo.set_caminho(askopenfilename())
            if caminho != None:
                self.pushButton_upload.setText(caminho)
                self.pushButton_upload.setIcon(QPixmap(''))

        except PermissionError:
            messagebox.showerror(title='Aviso', message= 'O arquivo selecionado apresenta-se em aberto em outra janela, favor fecha-la')
        except FileExistsError:
            messagebox.showerror(title='Aviso', message= 'O arquivo selecionado já apresenta uma versão sem acento, favor usar tal versão ou apagar uma delas')
        except Exception as error:
            messagebox.showerror(title='Aviso', message= error)

if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()