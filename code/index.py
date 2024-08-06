from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tabula as tb
import pandas as pd
import subprocess
import os

window = Tk()

class Arquivo:
    ...
    #Cada arquivo possui um banco

class Banco:
    ...
    def ler_tabela(self): #abstrato
        ...
    #Cada banco possui uma lógica de transformação

class Banco_caixa:
    ...

class App:
    #arquivo = Arquivo
    #Gerencia a entrada de dados, como o main
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
        self.window.title('Conversor de Extrato')

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

        self.bancoEntryOpt = ('Caixa','Banco do Brasil','Santa Fé','Sicoob')

        self.bancoEntry.set('Escolha aqui')

        self.popup = OptionMenu(self.index, self.bancoEntry, *self.bancoEntryOpt)\
            .place(relx=0.6,rely=0.37,relwidth=0.2,relheight=0.06)
        
        #Botão enviar
        Button(self.index, text='Gerar Extrato',\
            command= lambda: self.ler_arq(self.nome_arq,self.bancoEntry, self.rdButton))\
                .place(relx=0.35,rely=0.8,relwidth=0.35,relheight=0.12)
        
    def inserir_arq(self):
        self.nome_arq = askopenfilename()
        ultima_barra = self.nome_arq.rfind('/')
        self.arqLabel['text'] = self.nome_arq[ultima_barra+1:]

    def definir_tipo(self, arquivo):
        tamanho = len(arquivo)
        return arquivo[tamanho-3 : tamanho]

    def custom_banco(self, arquivo, banco, ordem):
        if banco.get() == 'Caixa':
            lista_tabelas = []

            for tabelas in arquivo:
                #Filtrando as colunas
                tabelas.columns = ["Data Mov.", "", "Histórico",'', "Valor"]
                tabelas = tabelas.drop('', axis=1)

                #Trocar a posição de "Histórico" e "Valor"
                tabelas.insert(1,'Valor', tabelas.pop('Valor'))
                tabelas.insert(2,'Histórico' ,tabelas.pop('Histórico'))

                #Add espaços vazios
                tabelas.insert(1,'Cód. Conta Débito','')
                tabelas.insert(2,'Cód. Conta Crédito','')
                tabelas.insert(4,'Cód. Histórico','')

                coluna_inf =[]
                #Tirar C e D de "Valor"
                for index, row in tabelas.iterrows():
                    if 'C' in row['Valor']:
                        coluna_inf.append('C')
                        tabelas.loc[[index],['Valor']] = str(row['Valor']).replace('C','')
                    elif 'D' in row['Valor']:
                        coluna_inf.append('D')
                        tabelas.loc[[index],['Valor']] = str(row['Valor']).replace('D','')
                
                tabelas.insert(6,'Inf.',coluna_inf)

                #Filtrando as linhas
                tabelas.fillna(0.0, inplace=True)
                lista_tabelas.append(tabelas.loc[tabelas['Histórico'] != 0.0])

            arquivoFinal = pd.concat(lista_tabelas, ignore_index=True)

            arquivoFinal = arquivoFinal.sort_values('Data Mov.', ascending= ordem.get())

        elif banco.get() == 'Banco do Brasil':
            lista_tabelas = []
            coluna_inf = []

            for tabelas in arquivo:
                #Filtrando as colunas
                tabelas = tabelas.loc[:,["balancete", "Histórico","Valor R$"]]

                #Trocar a posição de "Histórico" e "Valor" -auto
                tabelas.insert(1,'Valor R$', tabelas.pop('Valor R$'))
                tabelas.insert(2,'Histórico' ,tabelas.pop('Histórico'))

                #Add espaços vazios - auto
                tabelas.insert(1,'Cód. Conta Débito','')
                tabelas.insert(2,'Cód. Conta Crédito','')
                tabelas.insert(4,'Cód. Histórico','')

                #Tirar C e D de "Valor" - auto
                for index, row in tabelas.iterrows():
                    if 'C' in str(row['Valor R$']):
                        coluna_inf.append('C')
                        tabelas.loc[[index],['Valor R$']] = str(row['Valor R$']).replace('C','')
                    elif 'D' in str(row['Valor R$']):
                        coluna_inf.append('D')
                        tabelas.loc[[index],['Valor R$']] = str(row['Valor R$']).replace('D','')
                    else:
                        coluna_inf.append('')

                tabelas.insert(6,'Inf.',coluna_inf)

                #Filtrando linhas
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

        elif banco.get() == 'Sicoob':
            lista_tabelas = []
            coluna_inf = []

            tabelas = arquivo
            tabelas = tabelas.drop('', axis=1)

            #Trocar a posição de "Histórico" e "Valor"
            tabelas.insert(1,'Valor', tabelas.pop('Valor'))
            tabelas.insert(2,'Histórico' ,tabelas.pop('Histórico'))

            #Add espaços vazios
            tabelas.insert(1,'Cód. Conta Débito','')
            tabelas.insert(2,'Cód. Conta Crédito','')
            tabelas.insert(4,'Cód. Histórico','')

            #Tirar C e D de "Valor"
            for index, row in tabelas.iterrows():
                if 'C' in str(row['Valor']):
                    coluna_inf.append('C')
                    tabelas.loc[[index],['Valor']] = str(row['Valor']).replace('C','')
                elif 'D' in str(row['Valor']):
                    coluna_inf.append('D')
                    tabelas.loc[[index],['Valor']] = str(row['Valor']).replace('D','')
                else:
                    coluna_inf.append('')

            tabelas.insert(6,'Inf.',coluna_inf)

            #Filtrando as linhas
            tabelas.fillna('', inplace=True)
            for index, row in tabelas.iterrows():
                if row['Data'] == '' and 'SALDO DO DIA ===== >' not in row['Histórico']:
                    linhaAcima = tabelas.iloc[index - 1]
                    linhaAbaixo = tabelas.iloc[index + 1]
                    if linhaAbaixo['Histórico'] != '':
                        tabelas.loc[[index - 1],['Histórico']] = str(linhaAcima['Histórico']) + ' ' + str(row['Histórico'])
                        tabelas.drop(index)
                    else:
                        tabelas.loc[[index + 1],['Histórico']] = str(linhaAbaixo['Histórico']) + ' ' + str(row['Histórico'])
                        tabelas.drop(index)

            lista_tabelas.append(tabelas.loc[tabelas['Data'] != ''])

            arquivoFinal = pd.concat(lista_tabelas, ignore_index=True)

            arquivoFinal = arquivoFinal.sort_values('Data', ascending= ordem.get())
        else:
            return None
        
        return arquivoFinal

    def ler_arq(self, arquivo, banco, ordem):
        try:
            if arquivo == '':
                raise Exception('Insira um arquivo')
            
            if banco.get() == 'Escolha aqui':
                raise Exception('Banco inválido, favor selecioná-lo')
            
            tipo = self.definir_tipo(arquivo)
            arquivoFinal = ''

            if tipo == 'pdf':
                if banco.get() == 'Sicoob':
                    tabela1 = tb.read_pdf(arquivo, stream= True,relative_area=True ,area=[13,0,100,100])
                    tabela2 = tb.read_pdf(arquivo, stream= True, pages= 'all')

                    tabela2.insert(0,tabela1[0])
                    #Filtrando as colunas
                    for tabelas in tabela2:
                        tabelas.columns = ["Data", "", "Histórico", "Valor"]

                    arquivoLido = pd.concat(tabela2, ignore_index=True)
                else:
                    arquivoLido = tb.read_pdf(arquivo, pages='all', stream=True)
                
            elif tipo == 'lsx':
                arquivoLido = pd.read_excel(arquivo)
            else:
                raise Exception('Formato de arquivo inválido')

            arquivoFinal = self.custom_banco(arquivoLido, banco, ordem)

            file = asksaveasfilename(title='Favor selecionar a pasta onde será salvo', filetypes=((".xlsx","*.xlsx"),))

            arquivoFinal.style.hide().to_excel(file+'.xlsx')

            messagebox.showinfo(title='Aviso', message='Abrindo o arquivo gerado!')

            os.startfile(file+'.xlsx')


        except ValueError:
            messagebox.showerror(title='Aviso', message= 'Operação cancelada')
        except PermissionError:
            messagebox.showerror(title='Aviso', message= 'Feche o arquivo gerado antes de criar outro')
        except UnboundLocalError:
            messagebox.showerror(title='Aviso', message= 'Arquivo não compativel a esse banco')
        except subprocess.CalledProcessError:
            messagebox.showinfo(title='Aviso', message=f"Erro ao extrair a tabela")
        except Exception as error:
            messagebox.showerror(title='Aviso', message= error)

App()