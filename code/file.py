from unidecode import unidecode
from tkinter import messagebox
from PyPDF2 import PdfReader
from os import renames
import tabula as tb
import pandas as pd

class File:
    """
    Classe para manipulação de arquivos de extrato (PDF/Excel).
    """
    #Cada arquivo possui um banco
    def __init__(self):
        """
        Inicializa o caminho do arquivo.
        """
        self.path = ''

    def is_uploaded(self):
        """
        Verifica se um arquivo foi carregado.
        """
        return True if self.path != '' else False

    def simple_read(self, pg = 'all', header = True) -> list[pd.DataFrame]:
        """
        Lê o arquivo PDF de forma simples, retornando DataFrames.
        """
        if header == False:
            return tb.read_pdf(self.path, pages= pg, stream=True, encoding="ISO-8859-1", pandas_options={'header': None})
        
        return tb.read_pdf(self.path, pages= pg, stream=True, 
        encoding="ISO-8859-1")

    def custom_read(self, area_lida, pg = 'all', header = True) -> list[pd.DataFrame]:
        """
        Lê o arquivo PDF em uma área específica, retornando DataFrames.
        """
        if header == False:
            return tb.read_pdf(self.path, pages= pg, stream= True,\
                        relative_area=True, area= area_lida,\
                            pandas_options={"header":None}, encoding="ISO-8859-1")
        
        return tb.read_pdf(self.path, pages= pg, stream= True,\
                        relative_area=True, area= area_lida, encoding="ISO-8859-1")
    
    def excel_read(self):
        """
        Lê o arquivo Excel.
        """
        return pd.read_excel(self.path)
    
    def lenght(self):
        """
        Retorna o número de páginas do PDF.
        """
        return len(PdfReader(self.path).pages)

    def set_path(self, caminho) -> str:
        """
        Define e valida o caminho do arquivo.
        """
        if caminho == '':
            return None
        self.path = self.valided_path(caminho)
        return self.path[self.path.rfind('/') + 1:]
    
    def get_path(self) -> str:
        """
        Retorna apenas o nome do arquivo.
        """
        return self.path[self.path.rfind('/') + 1:]

    def __type(self, caminho) -> str:
        """
        Retorna a extensão do arquivo.
        """
        return caminho[ len(caminho) -3 :].lower()
    
    def valided_path(self, caminho) -> str:
        """
        Valida o caminho do arquivo e converte para ASCII se necessário.
        """
        if self.__type(caminho).lower() not in ['pdf', 'lsx']:
            raise Exception('Formato de arquivo inválido')

        caminho_acsii = self.__ascii(caminho)
        if caminho != caminho_acsii:
            caminho = caminho_acsii
            messagebox.showinfo(title='Aviso', message='O caminho do arquivo precisou ser mudado, para encontrá-lo novamente siga o caminho a seguir: \n' + caminho)
        
        return caminho

    def __ascii(self, caminho) -> str:
        """
        Remove acentos do caminho do arquivo e renomeia o arquivo.
        """
        caminho_uni = unidecode(caminho)
        renames(caminho, caminho_uni)
        return caminho_uni