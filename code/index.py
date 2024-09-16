from tkinter.filedialog import askopenfilename, asksaveasfilename
from unidecode import unidecode
from tkinter import messagebox
from tkinter import *
import tabula as tb
import pandas as pd
import subprocess
import string
import sys
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
    
    def leitura_custom_pandas(self, area_lida, pg = 'all'):
        return tb.read_pdf(self.caminho, pages= pg, stream= True,\
                        relative_area=True, area= area_lida,\
                            pandas_options={"header":None}, encoding="ISO-8859-1")

    def leitura_excel(self):
        return pd.read_excel(self.caminho)

    def inserir(self, label):
        caminho = askopenfilename()

        if caminho == '':
            return None
        
        self.caminho = self.validar_entrada(caminho)
        label['text'] = caminho[caminho.rfind('/') +1:]

    def abrir(self,arquivo_final):
        file = asksaveasfilename(title='Favor selecionar a pasta onde será salvo', filetypes=((".xlsx","*.xlsx"),))

        arquivo_final.style.hide().to_excel(file+'.xlsx')

        messagebox.showinfo(title='Aviso', message='Abrindo o arquivo gerado!')

        os.startfile(file+'.xlsx')

    def __tipo(self, caminho):
        return caminho[ len(caminho) -3 :]
    
    def validar_entrada(self, caminho):
        if any(c not in string.ascii_letters for c in caminho):
            caminho = self.formato_ascii(caminho)

        if self.__tipo(caminho) not in ['pdf', 'lsx']:
            raise Exception('Formato de arquivo inválido')
        
        return caminho

    def formato_ascii(self, caminho):
        caminho_uni = unidecode(caminho)
        os.renames(caminho, caminho_uni)
        return caminho_uni

class Banco:
    def __init__(self):
        self.formatos_disp = []
        self.titulo = ''

    def filt_colunas(self,arquivo, colunas):
        for tabelas in arquivo:
            tabelas.columns = colunas
            
        self.df = pd.concat(arquivo, ignore_index=True)
        self.df = self.df.drop('', axis=1, errors='ignore')

    def inserir_espacos(self, valor = 'Valor', troca = True):
        if troca == True:
            #Trocar a posição de "Histórico" e "Valor"
            self.df.insert(1,'Valor', self.df.pop(valor))
            self.df.insert(2,'Histórico' ,self.df.pop('Histórico'))

        #Add espaços vazios
        self.df.insert(1,'Cód. Conta Débito','')
        self.df.insert(2,'Cód. Conta Crédito','')
        self.df.insert(4,'Cód. Histórico','')

    def col_inf(self):
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

    def col_inf_sinal(self):
        coluna_inf = []
        #Tirar "-" de "Valor"
        for index, row in self.df.iterrows():
            if '-' in str(row['Valor']):
                coluna_inf.append('D')
                self.df.loc[[index],['Valor']] = str(row['Valor']).replace('-','')
            else:
                coluna_inf.append('C')

        self.df.insert(5,'Inf.',coluna_inf)

    def to_string(self):
        return self.titulo
    #Cada banco possui uma gerar_extrato próprio!!

class Caixa(Banco):
    def __init__(self):
        super().__init__()
        self.titulo = 'Caixa'

    def gerar_extrato(self, arquivo):
        self.filt_colunas(arquivo.leitura_simples(),["Data Mov.", "", "Histórico",'', "Valor"])
        self.inserir_espacos()
        self.col_inf()

        self.df.fillna(0.0, inplace=True)
        return self.df.loc[self.df['Histórico'] != 0.0]

class BancoDoBrasil(Banco):
    def __init__(self):
        super().__init__()
        self.titulo = 'Banco do Brasil'

    def gerar_extrato(self, arquivo):
        self.filt_colunas(arquivo.leitura_simples(),\
            ["balancete","","","","Histórico","","Valor R$",""])
        self.inserir_espacos(valor= 'Valor R$')
        self.col_inf()
        self.__filt_linhas()

        return self.df.loc[self.df['Valor'] != 0.0]

    def __filt_linhas(self):
        self.df.fillna(0.0, inplace=True)
        for index, row in self.df.iterrows():
            if row['balancete'] == 0.0:
                linhaAcima = self.df.iloc[index - 1]
                self.df.loc[[index - 1],['Histórico']] = linhaAcima['Histórico']+ ': ' + row['Histórico']


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
        self.filt_colunas(tabela2, ["Data", "", "Histórico", "Valor"])
        self.inserir_espacos()
        self.col_inf()
        self.__filt_linhas()

        return self.df

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
        self.filt_colunas(
            arquivo.leitura_custom_pandas(area_lida= [0,0,100,77]),["Data", "Valor"])
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
            if str(row['Histórico'][0]).isdigit():
                pos_saldo = str(row['Histórico']).index('Saldo')
                data = str(row['Histórico'][:pos_saldo - 1])
                coluna_data.append('')
            else:
                coluna_data.append(data)

        self.df.insert(0,'Data',coluna_data) 

class Itau(Banco):
    def __init__(self):
        super().__init__()
        self.titulo = 'Itau'

    def gerar_extrato(self, arquivo):
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

class App:
    def __init__(self):
        self.ref = {
            'caixa': Caixa(),
            'santa fé' : SantaFe(),
            'santa fe' :SantaFe(),
            'bb' : BancoDoBrasil(),
            'banco do brasil': BancoDoBrasil(),
            'sicoob': Sicoob(),
            'inter' : Inter(),
            'itaú': Itau(),
            'itau': Itau()
        }

        self.window = window
        self.arquivo = Arquivo()
        self.tela()
        self.index()
        window.mainloop()

    def tela(self):
        self.window.configure(background='darkblue')
        self.window.resizable(False,False)
        self.window.geometry('860x500')
        self.window.iconbitmap(self.resource_path('imgs\\extr-icon.ico'))
        self.window.title('Conversor de Extrato')

    def resource_path(self,relative_path):
        base_path = getattr(
            sys,
            '_MEIPASS',
            os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def index(self):
        self.index = Frame(self.window, bd=4, bg='lightblue')
        self.index.place(relx=0.05,rely=0.05,relwidth=0.9,relheight=0.9)

        #Titulo
        Label(self.index, text='Conversor de Extrato', background='lightblue', font=('arial',30,'bold')).place(relx=0.23,rely=0.25,relheight=0.15)

        #Logo
        self.logo = PhotoImage(file=self.resource_path('imgs\\extrato_horizontal.png'))
        
        self.logo = self.logo.subsample(3,3)
        
        Label(self.window, image=self.logo, background='lightblue')\
            .place(relx=0.15,rely=0.1,relwidth=0.7,relheight=0.2)

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

        self.bancoEntryOpt = ["Caixa","Banco do Brasil","Santa Fé","Sicoob", "Inter", "Itaú"]

        self.bancoEntry.set('Escolha aqui')

        self.popup = OptionMenu(self.index, self.bancoEntry, *self.bancoEntryOpt)\
            .place(relx=0.4,rely=0.75,relwidth=0.2,relheight=0.06)
        
        #Botão enviar
        Button(self.index, text='Gerar Extrato',\
            command= lambda: self.executar())\
                .place(relx=0.65,rely=0.8,relwidth=0.25,relheight=0.12)

    def obj_banco(self):
        if self.bancoEntry.get() != 'Escolha aqui':
            for key, obj in self.ref.items():
                if key in self.bancoEntry.get().lower():
                    return obj
        else:
            nome_arq = self.arqLabel['text']
            for chave, obj in self.ref.items():
                if chave in nome_arq.lower():
                    return obj
            raise Exception('Nome do banco não identificado no arquivo, favor seleciona-lo')

    def executar(self):
        try:       
            banco = self.obj_banco()

            arquivo_final = banco.gerar_extrato(self.arquivo)

            self.arquivo.abrir(arquivo_final)
         
        except PermissionError:
            messagebox.showerror(title='Aviso', message= 'Feche o arquivo gerado antes de criar outro')
        except UnboundLocalError:
            messagebox.showerror(title='Aviso', message= 'Arquivo não compativel a esse banco')
        except subprocess.CalledProcessError:
            messagebox.showerror(title='Aviso', message= "Erro ao extrair a tabela, confira se o banco foi selecionado corretamente. Caso contrário, comunique o desenvolvedor")
        except FileNotFoundError:
            messagebox.showerror(title='Aviso', message= "Arquivo indisponível")
        except Exception as error:
            messagebox.showerror(title='Aviso', message= error)
       
App()