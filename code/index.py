from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tabula as tb
import pandas as pd
import subprocess
import os

window = Tk()

class Arquivo:
    #Cada arquivo possui um banco
    def __init__(self):
        self.caminho = ''

    def leitura_simples(self):
        return tb.read_pdf(self.caminho, pages='all', stream=True)

    def leitura_custom(self, area_lida):
        return tb.read_pdf(self.caminho, pages='all', stream= True,\
                        relative_area=True, area= area_lida)

    def leitura_excel(self):
        return pd.read_excel(self.caminho)

    def inserir(self, label):
        self.caminho = askopenfilename()
        self.__definir_tipo(self.caminho)

        #def mudarLabel(self, label):
        ultima_barra = self.caminho.rfind('/')
        label['text'] = self.caminho[ultima_barra+1:]

    def abrir(arquivo_final):
        file = asksaveasfilename(title='Favor selecionar a pasta onde será salvo', filetypes=((".xlsx","*.xlsx"),))

        arquivo_final.style.hide().to_excel(file+'.xlsx')

        messagebox.showinfo(title='Aviso', message='Abrindo o arquivo gerado!')

        os.startfile(file+'.xlsx')

    def __definir_tipo(self, arquivo):
        tipo = arquivo[ len(arquivo) -3 :]

        if tipo not in ['pdf', 'xlx']:
            raise Exception('Formato de arquivo inválido')
        
        return tipo

class Banco:
    def __init__(self):
        self.arquivo = Arquivo()
        self.formatos_disp = []

    def gerar_extrato(self):
        self.ler_tabela()
        ...
    #Cada banco possui uma lógica de transformação

class Caixa(Banco):
    def __init__(self):
     super().__self__()

    def to_string():
        return 'Caixa'

class BancoDoBrasil(Banco):
    def __init__(self):
     super().__self__()

    def to_string():
        return 'Banco do Brasil'

class SantaFe(Banco):
    def __init__(self):
     super().__self__()

    def to_string():
        return 'Santa Fé'

class Sicoob(Banco):
    def __init__(self):
     super().__self__()

    def buscarLinhaPai(self,index, tabela):
        linhaAcima = tabela.iloc[index]
        if linhaAcima['Data'] != '':
            #se tiver data, é a linha pai
            return index
        #senao retorna a função com Index -1
        return self.buscarLinhaPai(index - 1, tabela)

    def to_string():
        return 'Sicoob'

class Inter(Banco):
    def __init__(self):
     super().__self__()

    def to_string():
        return 'Inter'

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
        self.window.iconbitmap('C:/Users/DELTAASUS/Documents/GitHub/Extrato_Auto/code/imgs/delta-icon.ico')
        self.window.title('Conversor de Extrato')

    def index(self):
        self.index = Frame(self.window, bd=4, bg='lightblue')
        self.index.place(relx=0.05,rely=0.05,relwidth=0.9,relheight=0.9)

        #Titulo
        Label(self.index, text='Conversor de Extrato', background='lightblue', font=('arial',30,'bold')).place(relx=0.23,rely=0.2,relheight=0.15)

        #Logo
        self.logo = PhotoImage(file='C:/Users/DELTAASUS/Documents/GitHub/Extrato_Auto/code/imgs/deltaprice-hori.png')
        
        self.logo = self.logo.subsample(4,4)
        
        Label(self.window, image=self.logo, background='lightblue')\
            .place(relx=0.175,rely=0.05,relwidth=0.7,relheight=0.2)


        #Labels e Entrys
        ###########Arquivo
        Label(self.index, text='Insira aqui o arquivo:',\
            background='lightblue', font=(10))\
                .place(relx=0.15,rely=0.4)

        self.nome_arq = ''
        self.arqLabel = Label(self.index)
        self.arqLabel.config(font=("Arial", 8, 'bold italic'))
        self.arqLabel.place(relx=0.21,rely=0.47,relwidth=0.35, relheight=0.055)
        
        Button(self.index, text='Enviar',\
            command= lambda: self.inserir_arq())\
                .place(relx=0.15,rely=0.47,relwidth=0.06,relheight=0.055)

        ###########Banco
        Label(self.index, text='Escolha o banco emissor:',\
            background='lightblue', font=(10))\
                .place(relx=0.6,rely=0.4)
        
        self.bancoEntry = StringVar(self.index)

        self.bancoEntryOpt = ('Caixa','Banco do Brasil','Santa Fé','Sicoob', 'Inter')

        self.bancoEntry.set('Escolha aqui')

        self.popup = OptionMenu(self.index, self.bancoEntry, *self.bancoEntryOpt)\
            .place(relx=0.6,rely=0.47,relwidth=0.2,relheight=0.06)
        
        #Botão enviar
        Button(self.index, text='Gerar Extrato',\
            command= lambda: self.ler_arq(self.nome_arq,self.bancoEntry, self.rdButton))\
                .place(relx=0.35,rely=0.8,relwidth=0.35,relheight=0.12)
        
    def executar(self):
        try:
            if self.caminho == '':
                raise Exception('Insira um arquivo')
            
            if self.bancoEntry.get() == 'Escolha aqui':
                raise Exception('Banco inválido, favor selecioná-lo')
            
            banco = self.definir_banco()
         
        except ValueError:
            messagebox.showerror(title='Aviso', message= 'Operação cancelada')
        except PermissionError:
            messagebox.showerror(title='Aviso', message= 'Feche o arquivo gerado antes de criar outro')
        except UnboundLocalError:
            messagebox.showerror(title='Aviso', message= 'Arquivo não compativel a esse banco')
        except subprocess.CalledProcessError:
            messagebox.showinfo(title='Aviso', message=f"Erro ao extrair a tabela, problema com o Java")
        except Exception as error:
            messagebox.showerror(title='Aviso', message= error)
       
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
                    linhaAbaixo = tabelas.iloc[index + 1]
                    if linhaAbaixo['Histórico'] != '':
                        indexPai = self.buscarLinhaPai(index - 1, tabelas)
                        linhaPai = tabelas.iloc[indexPai]
                        tabelas.loc[[indexPai], ['Histórico']] = str(linhaPai['Histórico']) + ' - ' + str(row['Histórico'])
                    else:
                        tabelas.loc[[index + 1],['Histórico']] = str(linhaAbaixo['Histórico']) + ' - ' + str(row['Histórico'])

            lista_tabelas.append(tabelas.loc[tabelas['Data'] != ''])

            arquivoFinal = pd.concat(lista_tabelas, ignore_index=True)

            arquivoFinal = arquivoFinal.sort_values('Data', ascending= ordem.get(), ignore_index=True)
        
        elif banco.get() == 'Inter':
            lista_tabelas = []
            coluna_inf = []
            coluna_data = []
            data = ''

            tabelas = arquivo

            

            #Trocar a posição de "Histórico" e "Valor"
            tabelas.insert(1,'Histórico', tabelas.pop('Data'))

            #Add espaços vazios
            tabelas.insert(0,'Cód. Conta Débito','')
            tabelas.insert(1,'Cód. Conta Crédito','')
            tabelas.insert(3,'Cód. Histórico','')

            tabelas = tabelas.drop([0,1,2,3,4]).reset_index(drop=True)

            #Tirar "-" de "Valor"
            for index, row in tabelas.iterrows():
                if '-' in str(row['Valor']):
                    coluna_inf.append('D')
                    tabelas.loc[[index],['Valor']] = str(row['Valor']).replace('-','')
                else:
                    coluna_inf.append('C')

            tabelas.insert(5,'Inf.',coluna_inf)

            #Adcionar coluna data
            tabelas.fillna('', inplace=True)
            for index, row in tabelas.iterrows():
                if str(row['Histórico'][0]).isdigit():
                    pos_saldo = str(row['Histórico']).index('Saldo') 
                    data = str(row['Histórico'][:pos_saldo - 1])
                    coluna_data.append('')
                else:
                    coluna_data.append(data)

            tabelas.insert(0,'Data',coluna_data)

            lista_tabelas.append(tabelas.loc[tabelas['Data'] != ''])

            arquivoFinal = pd.concat(lista_tabelas, ignore_index=True)

        else:
            return None
        
        return arquivoFinal

App()