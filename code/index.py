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
        self.window.resizable(False,False)
        self.window.geometry('860x500')
        # self.window.minsize(width=860, height=500)
        # self.window.maxsize(width=860, height=500)
        self.window.iconbitmap('')
        self.window.title('Gerador de CPS')

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
                .place(relx=0.15,rely=0.3)

        self.nome_arq = ''
        self.arqLabel = Label(self.index)
        self.arqLabel.config(font=("Arial", 8, 'bold italic'))
        self.arqLabel.place(relx=0.21,rely=0.37,relwidth=0.35, relheight=0.055)
        
        Button(self.index, text='Enviar',\
            command= lambda: self.inserir_arq())\
                .place(relx=0.15,rely=0.37,relwidth=0.06,relheight=0.055)
        
        Label(self.index, text='Ordem da coluna de "Datas":',\
            background='lightblue', font=(10))\
                .place(relx=0.15,rely=0.5)
        
        self.rdButton = BooleanVar()

        self.rdButton.set(True)

        Radiobutton(self.index, text='Crescente', value=True, variable=self.rdButton).place(relx=0.15,rely=0.57,relwidth=0.2,relheight=0.04)

        Radiobutton(self.index, text='Decrescente', value=False,variable=self.rdButton).place(relx=0.31,rely=0.57,relwidth=0.2,relheight=0.04)

        ###########Banco
        Label(self.index, text='Escolha o banco emissor:',\
            background='lightblue', font=(10))\
                .place(relx=0.6,rely=0.3)
        
        self.bancoEntry = StringVar(self.index)

        self.bancoEntryOpt = ('Caixa','Banco do Brasil','Santa Fé','Bradesco','Inter','Itaú','Mercado Pago','Nubank','Pagbank','Santander','Stone','Sicob')

        self.bancoEntry.set('Escolha aqui')

        self.popup = OptionMenu(self.index, self.bancoEntry, *self.bancoEntryOpt)\
            .place(relx=0.6,rely=0.37,relwidth=0.2,relheight=0.06)
        
        #Botão enviar
        Button(self.index, text='Gerar Extrato',\
            command= lambda: self.ler_arq(self.nome_arq,self.bancoEntry, self.rdButton))\
                .place(relx=0.35,rely=0.8,relwidth=0.35,relheight=0.12)
        
    def inserir_arq(self):
        self.nome_arq = filedialog.askopenfilename()
        ultima_barra = self.nome_arq.rfind('/')
        self.arqLabel['text'] = self.nome_arq[ultima_barra+1:]

    def definir_tipo(self, arquivo):
        tamanho = len(arquivo)
        return arquivo[tamanho-3 : tamanho]

    def custom_banco(self, arquivo, banco, ordem):
        if banco.get() == 'Caixa':
            lista_tabelas = []

            for tabelas in arquivo:
                tabelas.fillna(0.0, inplace=True)
                tabelas.columns = ["Data Mov.", "Nr. Doc.", "Histórico",'', "Valor"]
                lista_tabelas.append(tabelas.loc[tabelas['Histórico'] != 0.0])

                arquivoFinal = pd.concat(lista_tabelas, ignore_index=True)

                arquivoFinal = arquivoFinal.sort_values('Data Mov.', ascending= ordem.get())

        elif banco.get() == 'Banco do Brasil':
            lista_tabelas = []

            for tabelas in arquivo:
                tabelas.fillna(0.0, inplace=True)
                for index, row in tabelas.iterrows():
                    if row['balancete'] == 0.0:
                        linhaAcima = tabelas.iloc[index - 1]
                        tabelas.loc[[index - 1],['Histórico']] = linhaAcima['Histórico']+ ': ' + row['Histórico']
                lista_tabelas.append(tabelas.loc[tabelas['balancete'] != 0.0])

            arquivoFinal = pd.concat(lista_tabelas, ignore_index=True)

            arquivoFinal = arquivoFinal.sort_values('balancete', ascending= ordem.get())

        elif banco.get() == 'Santa Fé':
            lista= ["Data", "Observação", "Data Balancete","Agência Origem","Lote","Num. Documento","Cod. Histórico","Histórico","Valor R$","Inf.","Detalhamento Hist."]
            arquivo = arquivo.rename(columns=dict(zip(arquivo.columns, lista)))
            arquivo = arquivo.drop(0, axis=0)
            arquivo = arquivo.drop(1, axis=0)

            arquivoFinal = arquivo[["Data", "Agência Origem","Histórico","Valor R$","Inf."]]

            arquivoFinal = arquivoFinal.sort_values('Data', ascending= ordem.get())

        else:
            return None
        
        return arquivoFinal

    def ler_arq(self, arquivo, banco, ordem):
        try:
            if arquivo == '':
                raise FileNotFoundError('Insira um arquivo')
            
            if banco.get() == 'Escolha aqui':
                raise ValueError('Banco inválido, favor selecioná-lo')
            
            tipo = self.definir_tipo(arquivo)
            arquivoFinal = ''

            if tipo == 'pdf':
                arquivoLido = tb.read_pdf(arquivo, pages='all', stream=True)
            elif tipo == 'lsx':
                arquivoLido = pd.read_excel(arquivo)
            else:
                raise ValueError('Formato de arquivo inválido')

            arquivoFinal = self.custom_banco(arquivoLido, banco, ordem)
            arquivoFinal.to_excel('Arquivo_result.xlsx')

            messagebox.showinfo(title='Aviso', message='Abrindo o arquivo gerado!')
            os.startfile('arquivo_result.xlsx')

        except (ValueError, FileNotFoundError) as error:
            messagebox.showinfo(title='Aviso', message= error)
        except PermissionError:
            messagebox.showinfo(title='Aviso', message= 'Feche o arquivo gerado antes de criar outro')


application()

#Sesas