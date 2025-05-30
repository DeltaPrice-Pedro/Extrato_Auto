from PySide6.QtCore import QObject, Signal
from traceback import print_exc
from tkinter import messagebox
from bank import Bank
from file import File
import pandas as pd

class Generator(QObject):
    """
    Classe responsável por gerar o extrato processado e emitir sinais para a interface.
    """
    inicio = Signal(bool)
    fim = Signal(bool)
    open = Signal(pd.DataFrame)

    def __init__(self, banco: Bank, arquivo: File, bank_account: int, relacoes: dict[int, str]) -> None:
        """
        Inicializa o gerador com o banco, arquivo, id do banco e relações de referência.
        """
        super().__init__()
        self.banco = banco
        self.arquivo = arquivo
        self.bank_account = bank_account
        self.relacoes = relacoes

    def extrato(self):
        """
        Executa o processamento do extrato e emite sinais para a interface.
        """
        try:
            self.inicio.emit(True)
            arquivo_final = self.banco.gerar_extrato(self.arquivo)

            if self.relacoes != {}:
                arquivo_final = self.prog_contabil(arquivo_final)

            self.open.emit(arquivo_final)
            self.fim.emit(False)

        except Exception as error:
            print_exc()
            messagebox.showerror(title='Aviso', message= f"Erro ao extrair a tabela: confira se o banco foi selecionado corretamente, caso contrário, comunique o desenvolvedor \n\n- erro do tipo: {error}")
        finally:
            self.fim.emit(False)

    def prog_contabil(self, arquivo_final: pd.DataFrame):
        """
        Aplica as relações contábeis ao DataFrame do extrato.
        """
        #relações = listas de word, value, release_letter
        arquivo_novo = arquivo_final.copy(True)
        df_release = pd.DataFrame(self.relacoes)

        word_value_c = self.words_reference(df_release, 'C')
        word_value_d = self.words_reference(df_release, 'D')

        for index, row in arquivo_novo.iterrows():
            if row['Inf.'] == 'C':
                row['Cód. Conta Débito'] = self.bank_account
                value = self.search_word(word_value_c, row)
                if value != None:
                    row['Cód. Conta Crédito'] = value

            else:
                row['Cód. Conta Crédito'] = self.bank_account
                value = self.search_word(word_value_d, row)
                if value != None:
                    row['Cód. Conta Débito'] = value

        return arquivo_novo
    
    def words_reference(self, df: pd.DataFrame, release: str):
        """
        Filtra as referências por tipo de lançamento (C/D).
        """
        df_release = df.loc[df['release_letter'] == release]
        list_release = df_release.loc[:, ['word','account']].values
        return list_release

    def search_word(self, words, row):
        """
        Busca a palavra-chave no histórico da linha.
        """
        finding_word = str(row['Histórico']).lower()
        for word, value in words:
            if word.lower() in finding_word:
                return value    
        return None
