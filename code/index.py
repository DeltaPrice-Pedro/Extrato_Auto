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

        if self.caminho == '':
            raise Exception('Operação cancelada')

        if self.__tipo() not in ['pdf', 'xlx']:
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

    def inserir_espacos(self):
        #Trocar a posição de "Histórico" e "Valor"
        self.df.insert(1,'Valor', self.df.pop('Valor'))
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
            if 'C' in row['Valor']:
                coluna_inf.append('C')
                self.df.loc[[index],['Valor']] = str(row['Valor']).replace('C','')
            elif 'D' in row['Valor']:
                coluna_inf.append('D')
                self.df.loc[[index],['Valor']] = str(row['Valor']).replace('D','')

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

class SantaFe(Banco):
    def __init__(self):
        super().__init__()
        self.titulo = 'Santa Fé'

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

class Inter(Banco):
    def __init__(self):
        super().__self__()
        self.titulo = 'Inter'

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
        Label(self.index, text='Conversor de Extrato', background='lightblue', font=('arial',30,'bold')).place(relx=0.23,rely=0.2,relheight=0.15)

        #Logo
        self.logo = PhotoImage(file='Z:\\18 - PROGRAMAS DELTA\\code\\imgs\\deltaprice-hori.png')
        
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
            command= lambda: self.arquivo.inserir(self.arqLabel))\
                .place(relx=0.15,rely=0.47,relwidth=0.06,relheight=0.055)

        ###########Banco
        Label(self.index, text='Escolha o banco emissor:',\
            background='lightblue', font=(10))\
                .place(relx=0.6,rely=0.4)
        
        self.bancoEntry = StringVar()

        self.bancoEntryOpt = ["Caixa","BancoDoBrasil","SantaFe","Sicoob", "Inter"]

        self.bancoEntry.set('Escolha aqui')

        self.popup = OptionMenu(self.index, self.bancoEntry, *self.bancoEntryOpt)\
            .place(relx=0.6,rely=0.47,relwidth=0.2,relheight=0.06)
        
        #Botão enviar
        Button(self.index, text='Gerar Extrato',\
            command= lambda: self.executar())\
                .place(relx=0.35,rely=0.8,relwidth=0.35,relheight=0.12)

    def definir_banco(self):
        banco_selecionado = self.bancoEntry.get()

        if banco_selecionado == 'Caixa':
            return Caixa()
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