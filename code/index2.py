from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename

import tabula as tb
import pandas as pd

import os
from sys import exit
import subprocess
import requests

window = Tk()

#Instalar o JDK e/ou instanciar o JAVA_HOME  
class JDK:
    if os.path.isdir("C:/Program Files/Java/jdk-22"):
        os.environ["JAVA_HOME"] ="C:/Program Files/Java/jdk-22"
        print("A variável JAVA_HOME foi definida")

    else:
        resp = messagebox.askyesno(title='Aviso', message= 'Verificamos que não possui um dos requisitos do sistema, podemos prosseguir com a instalação do Java JDK?')

        if resp == True:
            try:
                response = requests.get('https://download.oracle.com/java/22/latest/jdk-22_windows-x64_bin.exe', stream=True)

                #perguntar onde baixar o instalador
                with open('c:/Users/DELTAASUS/Downloads', 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            
                #jdk-22.0.0_windows-x64_bin.exe /s /d "C:/Program Files/Java/jdk-22"

                jdk_installer = "c:/Users/DELTAASUS/Downloads/jdk-22_windows-x64_bin.exe"
                jdk_install_dir = "C:/Program Files/Java/jdk-22"

                resultado = subprocess.run([jdk_installer, "/s", "/d", jdk_install_dir], capture_output=True, text=True)
                print(resultado.stdout)

                #os.environ["JAVA_HOME"] ="C:/Program Files/Java/jdk-22"
                messagebox.showwarning(title='Aviso', message= 'Download concluído, favor fechar e abrir o programa')
            except subprocess.CalledProcessError as e:
                print(f"Erro ao executar o comando: {e}")

        elif resp == False:
            exit() #Fechar programa

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

        self.bancoEntryOpt = ('Caixa','Banco do Brasil','Santa Fé','Bradesco','Inter','Itaú','Mercado Pago','Nubank','Pagbank','Santander','Stone','Sicob')

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
                raise Exception('Insira um arquivo')
            
            if banco.get() == 'Escolha aqui':
                raise Exception('Banco inválido, favor selecioná-lo')
            
            tipo = self.definir_tipo(arquivo)
            arquivoFinal = ''

            if tipo == 'pdf':
                try:
                    arquivoLido = tb.read_pdf(arquivo, stream=True)
                except subprocess.CalledProcessError as e:
                    messagebox.showinfo(title='Aviso', message=f"Erro ao extrair a tabela: {e}")
            elif tipo == 'lsx':
                arquivoLido = pd.read_excel(arquivo)
            else:
                raise Exception('Formato de arquivo inválido')

            arquivoFinal = self.custom_banco(arquivoLido, banco, ordem)

            file = asksaveasfilename(title='Favor selecionar a pasta onde será salvo', filetypes=((".xlsx","*.xlsx"),))

            arquivoFinal.to_excel(file+'.xlsx')

            messagebox.showinfo(title='Aviso', message='Abrindo o arquivo gerado!')

            os.startfile(file+'.xlsx')


        except (ValueError, FileNotFoundError) as error:
            messagebox.showerror(title='Aviso', message= error)
        except PermissionError:
            messagebox.showerror(title='Aviso', message= 'Feche o arquivo gerado antes de criar outro')
        except UnboundLocalError:
            messagebox.showerror(title='Aviso', message= 'Arquivo não compativel a esse banco')
        except Exception as error:
            messagebox.showerror(title='Aviso', message= error)

            #CalledProcessError

#JDK()
application()