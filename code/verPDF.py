import tabula as tb
import camelot

arquivo = tb.read_pdf("BRADESCO.pdf", pages="all", multiple_tables=True)
tabela = arquivo[0]
tabela.fillna(0.0, inplace=True)

display(arquivo)
#tabela.to_excel('BRADESCO_result.xlsx')

###################################################

tables = camelot.read_pdf('BRADESCO.pdf', flavor='stream', pages='all')

tables.export('output', f='excel')