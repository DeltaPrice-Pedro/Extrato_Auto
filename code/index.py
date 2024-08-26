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

    def leitura_simples(self, pg = 'all'):
        return tb.read_pdf(self.caminho, pages= pg, stream=True)

    def leitura_custom(self, area_lida, pg = 'all'):
        return tb.read_pdf(self.caminho, pages= pg, stream= True,\
                        relative_area=True, area= area_lida)

    def leitura_excel(self):
        return pd.read_excel(self.caminho)

    def inserir(self, label):
        self.caminho = askopenfilename()

        if self.caminho == '':
            raise Exception('Operação cancelada')

        if self.__tipo() not in ['pdf', 'lsx']:
            raise Exception('Formato de arquivo inválido')
        
        ultima_barra = self.caminho.rfind('/')
        label['text'] = self.caminho[ultima_barra+1:]

    def abrir(self,arquivo_final):
        file = asksaveasfilename(title='Favor selecionar a pasta onde será salvo', filetypes=((".xlsx","*.xlsx"),))

        arquivo_final.style.hide().to_excel(file+'.xlsx')

        messagebox.showinfo(title='Aviso', message='Abrindo o arquivo gerado!')

        os.startfile(file+'.xlsx')

    def __tipo(self):
        return self.caminho[ len(self.caminho) -3 :]

class Banco:
    def __init__(self):
        self.formatos_disp = []
        self.titulo = ''

    def inserir_espacos(self, valor = 'Valor'):
        #Trocar a posição de "Histórico" e "Valor"
        self.df.insert(1,'Valor', self.df.pop(valor))
        self.df.insert(2,'Histórico' ,self.df.pop('Histórico'))

        #Add espaços vazios
        self.df.insert(1,'Cód. Conta Débito','')
        self.df.insert(2,'Cód. Conta Crédito','')
        self.df.insert(4,'Cód. Histórico','')

    #talvez todos os bancos usam o for de filt_colunas

    def to_string(self):
        return self.titulo
    #Cada banco possui uma gerar_extrato próprio!!

class Caixa(Banco):
    def __init__(self):
        super().__init__()
        self.titulo = 'Caixa'

    def gerar_extrato(self, arquivo):
        self.__filt_colunas(arquivo.leitura_simples())
        self.inserir_espacos()
        self.__col_inf()
        self.__filt_linhas()

        return self.df
    
    def __filt_colunas(self,arquivo):
        for tabelas in arquivo:
            tabelas.columns = ["Data Mov.", "", "Histórico",'', "Valor"]
            
        self.df = pd.concat(arquivo, ignore_index=True)
        self.df = self.df.drop('', axis=1)

    def __col_inf(self):
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

        self.df.insert(6,'Inf.',coluna_inf)

    def __filt_linhas(self):
        lista_tabelas = []

        self.df.fillna(0.0, inplace=True)
        lista_tabelas.append(self.df.loc[self.df['Histórico'] != 0.0])

        self.df = pd.concat(lista_tabelas, ignore_index=True)

class BancoDoBrasil(Banco):
    def __init__(self):
        super().__init__()
        self.titulo = 'Banco do Brasil'

    def gerar_extrato(self, arquivo):
        self.__filt_colunas(arquivo.leitura_simples())
        self.inserir_espacos(valor= 'Valor R$')
        self.__col_inf()
        self.__filt_linhas()

        return self.df
    
    def __filt_colunas(self,arquivo):
        for tabelas in arquivo:
            tabelas.columns = ["balancete","","","","Histórico","","Valor R$",""]
            
        self.df = pd.concat(arquivo, ignore_index=True)
        self.df = self.df.drop('', axis=1)

    def __col_inf(self): #identico ao Caixa
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

        self.df.insert(6,'Inf.',coluna_inf)

    def __filt_linhas(self):
        lista_tabelas = []
        self.df.fillna(0.0, inplace=True)
        for index, row in self.df.iterrows():
            if row['balancete'] == 0.0:
                linhaAcima = self.df.iloc[index - 1]
                self.df.loc[[index - 1],['Histórico']] = linhaAcima['Histórico']+ ': ' + row['Histórico']

        lista_tabelas.append(self.df.loc[self.df['Valor'] != 0.0])

        self.df = pd.concat(lista_tabelas, ignore_index=True)

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

    def gerar_extrato(self, arquivo):
        tabela1 = arquivo.leitura_custom(area_lida= [13,0,100,100], pg=1)
        tabela2 = arquivo.leitura_simples()
        tabela2.insert(0, tabela1[0])
        self.__filt_colunas(tabela2)
        self.inserir_espacos()
        self.__col_inf()
        self.__filt_linhas()

        return self.df
    
    def __filt_colunas(self,arquivo):
        for tabelas in arquivo:
            tabelas.columns = ["Data", "", "Histórico", "Valor"]
            
        self.df = pd.concat(arquivo, ignore_index=True)
        self.df = self.df.drop('', axis=1)

    def __col_inf(self):
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

        self.df.insert(6,'Inf.',coluna_inf)

    def __filt_linhas(self):
        lista_tabelas = []
        self.df.fillna('', inplace=True)
        for index, row in self.df.iterrows():
            if row['Data'] == '' and 'SALDO DO DIA ===== >' not in row['Histórico']:
                linhaAbaixo = self.df.iloc[index + 1]
                if linhaAbaixo['Histórico'] != '':
                    indexPai = self.buscarLinhaPai(index - 1, self.df)
                    linhaPai = self.df.iloc[indexPai]
                    self.df.loc[[indexPai], ['Histórico']] = str(linhaPai['Histórico']) + ' - ' + str(row['Histórico'])
                else:
                    self.df.loc[[index + 1],['Histórico']] = str(linhaAbaixo['Histórico']) + ' - ' + str(row['Histórico'])

        lista_tabelas.append(self.df.loc[self.df['Data'] != ''])

        self.df = pd.concat(lista_tabelas, ignore_index=True)

class Inter(Banco):
    def __init__(self):
        super().__init__()
        self.titulo = 'Inter'

    def gerar_extrato(self, arquivo):
        self.__filt_colunas(arquivo.leitura_custom(area_lida= [0,0,93,77]))
        self.__inserir_espacos()
        self.__col_inf()
        self.__col_data()
        
        lista_tabelas = []

        lista_tabelas.append(self.df.loc[self.df['Data'] != ''])

        return pd.concat(lista_tabelas, ignore_index=True)
    
    def __filt_colunas(self,arquivo):
        for tabelas in arquivo:
            tabelas.columns = ["Data", "Valor"]
            
        self.df = pd.concat(arquivo, ignore_index=True)

    def __inserir_espacos(self):
        #Trocar a posição de "Histórico" e "Valor"
        self.df.insert(1,'Histórico', self.df.pop('Data'))

        #Add espaços vazios
        self.df.insert(0,'Cód. Conta Débito','')
        self.df.insert(1,'Cód. Conta Crédito','')
        self.df.insert(3,'Cód. Histórico','')

        self.df = self.df.drop([0,1,2,3,4]).reset_index(drop=True)

    def __col_inf(self):
        coluna_inf = []
        #Tirar "-" de "Valor"
        for index, row in self.df.iterrows():
            if '-' in str(row['Valor']):
                coluna_inf.append('D')
                self.df.loc[[index],['Valor']] = str(row['Valor']).replace('-','')
            else:
                coluna_inf.append('C')

        self.df.insert(5,'Inf.',coluna_inf)

    def __col_data(self):
        coluna_data = []
        data = ''
        #Adcionar coluna data
        self.df.fillna('', inplace=True)
        for index, row in self.df.iterrows():
            if str(row['Histórico'][0]).isdigit():
                pos_saldo = str(row['Histórico']).index('Saldo')
                data = str(row['Histórico'][:pos_saldo - 1])
                coluna_data.append('')
            else:
                coluna_data.append(data)

        self.df.insert(0,'Data',coluna_data) #precisa passar por todas linhas de uma vez

class App:
    #arquivo = Arquivo
    #Gerencia a entrada de dados, como o main
    def __init__(self):
        self.window = window
        self.arquivo = Arquivo()
        self.tela()
        self.index()
        window.mainloop()

    def tela(self):
        self.window.configure(background='darkblue')
        self.window.resizable(False,False)
        self.window.geometry('860x500')
        self.window.iconbitmap('Z:\\18 - PROGRAMAS DELTA\\code\\imgs\\delta-icon.ico')
        self.window.title('Conversor de Extrato')

    def index(self):
        self.index = Frame(self.window, bd=4, bg='lightblue')
        self.index.place(relx=0.05,rely=0.05,relwidth=0.9,relheight=0.9)

        #Titulo
        Label(self.index, text='Conversor de Extrato', background='lightblue', font=('arial',30,'bold')).place(relx=0.23,rely=0.25,relheight=0.15)

        #Logo
        self.logo = PhotoImage(file='Z:\\18 - PROGRAMAS DELTA\\code\\imgs\\deltaprice-hori.png')
        
        self.logo = self.logo.subsample(4,4)
        
        Label(self.window, image=self.logo, background='lightblue')\
            .place(relx=0.175,rely=0.1,relwidth=0.7,relheight=0.2)

        #Labels e Entrys
        ###########Arquivo
        Label(self.index, text='Insira aqui o arquivo:',\
            background='lightblue', font=(10))\
                .place(relx=0.15,rely=0.45)

        self.nome_arq = ''
        self.arqLabel = Label(self.index)
        self.arqLabel.config(font=("Arial", 8, 'bold italic'))
        self.arqLabel.place(relx=0.21,rely=0.52,relwidth=0.7, relheight=0.055)
        
        Button(self.index, text='Enviar',\
            command= lambda: self.arquivo.inserir(self.arqLabel))\
                .place(relx=0.15,rely=0.52,relwidth=0.06,relheight=0.055)

        ###########Banco
        Label(self.index, text='Caso o nome do banco não constar no nome do arquivo',\
                    background='lightblue', font=("Arial", 12, 'bold italic'))\
                        .place(relx=0.15,rely=0.7)

        Label(self.index, text='Escolha o banco emissor:',\
            background='lightblue', font=(10))\
                .place(relx=0.15,rely=0.75)
        
        self.bancoEntry = StringVar()

        self.bancoEntryOpt = ["Caixa","Banco do Brasil","Santa Fé","Sicoob", "Inter"]

        self.bancoEntry.set('Escolha aqui')

        self.popup = OptionMenu(self.index, self.bancoEntry, *self.bancoEntryOpt)\
            .place(relx=0.4,rely=0.75,relwidth=0.2,relheight=0.06)
        
        #Botão enviar
        Button(self.index, text='Gerar Extrato',\
            command= lambda: self.executar())\
                .place(relx=0.65,rely=0.8,relwidth=0.25,relheight=0.12)

    def definir_banco(self):
        banco_selecionado = self.bancoEntry.get()
        nome_arq = self.arqLabel['text']

        if banco_selecionado == 'Caixa' or\
            'caixa' in nome_arq.lower():
            return Caixa()
        elif banco_selecionado == 'Santa Fé' or\
            'santa fé' in nome_arq.lower() or\
            'santa fe' in nome_arq.lower():
            return SantaFe()
        elif banco_selecionado == 'Banco do Brasil' or\
            'BB' in nome_arq.upper() or\
            'banco do brasil' in nome_arq.lower():
            return BancoDoBrasil()
        elif banco_selecionado == 'Sicoob' or\
            'sicoob' in nome_arq.lower():
            return Sicoob()
        elif banco_selecionado == 'Inter' or\
            'inter' in nome_arq.lower():
            return Inter()
        raise Exception('Banco inválido, favor selecioná-lo')

    def executar(self):
        try:       
            banco = self.definir_banco()

            arquivo_final = banco.gerar_extrato(self.arquivo)

            self.arquivo.abrir(arquivo_final)
         
        except ValueError:
            messagebox.showerror(title='Aviso', message= 'Operação cancelada')
        except PermissionError:
            messagebox.showerror(title='Aviso', message= 'Feche o arquivo gerado antes de criar outro')
        except UnboundLocalError:
            messagebox.showerror(title='Aviso', message= 'Arquivo não compativel a esse banco')
        except subprocess.CalledProcessError:
            messagebox.showerror(title='Aviso', message= "Erro ao extrair a tabela, problema com o Java")
        except FileNotFoundError:
            messagebox.showerror(title='Aviso', message= "Arquivo indisponível")
        except Exception as error:
            messagebox.showerror(title='Aviso', message= error)
       
App()