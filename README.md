# Conversor de Extrato Bancário

## Descrição

Este projeto é uma aplicação desktop para conversão e padronização de extratos bancários de diferentes bancos brasileiros. O sistema permite importar arquivos de extrato em PDF ou Excel, processá-los conforme o layout de cada banco e exportar os dados em formato Excel padronizado, facilitando a conciliação contábil e integração com sistemas de gestão.

Além disso, o sistema possui uma interface gráfica para cadastro de empresas, bancos e referências contábeis (palavras-chave associadas a contas contábeis), permitindo a automação do lançamento contábil a partir do histórico dos extratos.

## Principais Funcionalidades

- Upload de extratos bancários em PDF ou Excel.
- Processamento automático dos layouts dos principais bancos (Caixa, Banco do Brasil, Bradesco, Itaú, Sicoob, Inter, PagBank, Mercado Pago, Santa Fé).
- Cadastro e edição de empresas e suas referências contábeis.
- Associação de palavras-chave a contas contábeis para automação do lançamento.
- Exportação do extrato processado em formato Excel.
- Interface gráfica amigável (PySide6/Qt).
- Integração com banco de dados MySQL para persistência de empresas, bancos e referências.

## Estrutura dos Arquivos

- `main.py`: Interface gráfica principal e lógica de interação com o usuário.
- `bank.py`: Classe base abstrata para bancos.
- `file.py`: Manipulação de arquivos PDF/Excel.
- `database.py`: Conexão e operações com o banco de dados MySQL.
- `changes.py`: Controle de alterações (add, update, remove) em referências.
- `generator.py`: Geração do extrato processado e integração com a interface.
- `banco_do_brasil.py`, `bradesco.py`, `caixa.py`, `itau.py`, `inter.py`, `mercado_pago.py`, `pag_bank.py`, `santa_fe.py`, `sicoob.py`: Classes específicas para cada banco, responsáveis por interpretar e padronizar os extratos conforme o layout de cada instituição.

## Como Funciona

1. O usuário seleciona o banco e faz upload do extrato.
2. O sistema identifica o layout e processa o arquivo, extraindo as informações relevantes.
3. O usuário pode cadastrar empresas e associar palavras-chave a contas contábeis.
4. O sistema aplica as regras de referência para automatizar a classificação contábil.
5. O extrato padronizado pode ser exportado para Excel.

## Tecnologias Utilizadas

- Python 3
- PySide6 (Qt for Python)
- pandas
- tabula-py (leitura de PDFs)
- PyPDF2
- pymysql
- unidecode
- dotenv

## Requisitos

- Python 3.8+
- Java (para tabula-py)
- MySQL Server
- Dependências Python (ver requirements.txt)

## Instalação

1. Clone o repositório.
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Configure o arquivo `.env` com as credenciais do banco de dados.
4. Execute o programa:
   ```
   python main.py
   ```

## Observações

- O sistema foi desenvolvido para facilitar a rotina contábil de escritórios e empresas que recebem extratos de múltiplos bancos.
- O layout dos extratos pode variar conforme o banco e o tipo de conta. O sistema possui lógica específica para cada caso.
- Para dúvidas ou sugestões, entre em contato com o desenvolvedor.
