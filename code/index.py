from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import tabula as tb
import pandas as pd
import os

window = Tk()

class application:
    def __init__(self):
        self.window = window
        self.tela()
        self.index()
        window.mainloop()

    def tela(self):
        self.window.configure(background='darkblue')
        self.window.resizable(True,True)
        self.window.minsize(width=860, height=500)
        self.window.maxsize(width=860, height=500)
        self.window.title('Gerador de CPS')

        self.menu = Frame(self.window, bd=4, bg='lightblue')
        self.menu.place(relx=0.05,rely=0.05,relwidth=0.9,relheight=0.9)

        self.textOrientacao = Label(self.menu, text='Selecione o tipo de CPS que deseja fazer:', background='lightblue', font=('Bold', 15))\
        .place(relx=0.12,rely=0.1,relheight=0.15)

        #Pessoa física
        self.btnPF = Button(self.menu, text='CPS Pessoa Física',\
            command= lambda: self.pagePF())\
                .place(relx=0.15,rely=0.7,relwidth=0.25,relheight=0.15)

        #Inatividade
        self.btnIN = Button(self.menu, text='CPS Inatividade',\
            command= lambda: self.pageIN())\
                .place(relx=0.60,rely=0.4,relwidth=0.25,relheight=0.15)

        #Lucro Presumido
        self.btnLP = Button(self.menu, text='CPS Lucro Presumido',\
            command= lambda: self.pageLP())\
                .place(relx=0.15,rely=0.4,relwidth=0.25,relheight=0.15)

        #Simples Nacional
        self.btnSN = Button(self.menu, text='CPS Simples Nacional',\
            command= lambda: self.pageSN())\
                .place(relx=0.60,rely=0.7,relwidth=0.25,relheight=0.15)

    def index(self):
        self.index = Frame(self.window, bd=4, bg='lightblue')
        self.index.place(relx=0.05,rely=0.05,relwidth=0.9,relheight=0.9)

        #Titulo
        Label(self.index, text='Conversor de Extrato', background='lightblue', font=('Bold', 17))\
            .place(relx=0.35,rely=0.05)

        #Labels e Entrys
        ###########Arquivo
        Label(self.index, text='Insira aqui o arquivo:',\
            background='lightblue', font=(10))\
                .place(relx=0.2,rely=0.3)

        self.nome_arq = ''
        self.arqLabel = Label(self.index, text=self.nome_arq,\
            background='white', font=(10))\
                .place(relx=0.2,rely=0.37,relwidth=0.2)
        
        Button(self.index, text='Enviar',\
            command= lambda: self.inserir_arq())\
                .place(relx=0.15,rely=0.37,relwidth=0.06,relheight=0.055)
        

        ###########Banco
        Label(self.index, text='Escolha o banco emissor:',\
            background='lightblue', font=(10))\
                .place(relx=0.6,rely=0.3)
        
        Label(self.index, text='POR ENQUANTO APENAS "CAIXA" FUNCIONA',\
            background='lightblue', font=(10))\
                .place(relx=0.4,rely=0.2)

        self.bancoEntry = StringVar(self.index)

        self.bancoEntryOpt = ('Caixa','Banco do Brasil','Bradesco','Inter','Itaú','Mercado Pago','Nubank','Pagbank','Santander','Stone','Sicob')

        self.bancoEntry.set('Escolha aqui')

        self.popup = OptionMenu(self.index, self.bancoEntry, *self.bancoEntryOpt)\
            .place(relx=0.6,rely=0.37,relwidth=0.2,relheight=0.06)

        #Botão enviar
        Button(self.index, text='Gerar CPS',\
            command= lambda: self.ler_arq(self.nome_arq,self.bancoEntry))\
                .place(relx=0.35,rely=0.8,relwidth=0.35,relheight=0.12)
        
    def inserir_arq(self):
        self.nome_arq = filedialog.askopenfilename()

    def definir_tipo(self, arquivo):
        tamanho = len(arquivo)
        return arquivo[tamanho-3 : tamanho]

    def custom_banco(self, arquivo, banco):
        if banco.get() == 'Caixa':
            lista_tabelas = []

            for tabelas in arquivo:
                tabelas.fillna(0.0, inplace=True)
                tabelas.columns = ["Data Mov.", "Nr. Doc.", "Histórico",'', "Valor"]
                lista_tabelas.append(tabelas.loc[tabelas['Histórico'] != 0.0])

                arquivoFinal = pd.concat(lista_tabelas, ignore_index=True)

        elif banco.get() == '':
            ...
        else:
            return None
        
        return arquivoFinal

    def ler_arq(self, arquivo, banco):
        try:
            tipo = self.definir_tipo(arquivo)
            arquivoFinal = ''

            if tipo == 'pdf':
                arquivoLido = tb.read_pdf(arquivo, pages='all', stream=True)

                arquivoFinal = self.custom_banco(arquivoLido, banco)

            elif tipo == 'lsx':
                arquivoLido = pd.read_excel(arquivo)
            
            else:
                raise ValueError('Formato de arquivo inválido')

            if banco == '':
                raise ValueError('Banco inválido, favor selecioná-lo')

            else:
                arquivoFinal.to_excel('Arquivo_result.xlsx')
                messagebox.showinfo(title='Aviso', message='Abrindo o arquivo gerado!')

                os.startfile('arquivo_result.xlsx')
        except:
            messagebox.showinfo(title='Aviso', message='Dados inválidos')
            #pegar valor do raise dps

application()
