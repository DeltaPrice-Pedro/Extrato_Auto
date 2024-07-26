import pandas as pd

arquivo_origem = pd.read_excel("EXTRATO_origem.xlsx")

arquivo_final = arquivo_origem[["Dt. lancto", "Vlr. lancto", "Compl. histór."]]

display(arquivo_final.head(10))

arquivo_final.to_excel('EXTRATO_final_TESTE.xlsx')