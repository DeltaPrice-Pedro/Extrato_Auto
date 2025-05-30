from PySide6.QtWidgets import (
    QMainWindow, QApplication, QRadioButton, QVBoxLayout, QWidget,
    QTableWidgetItem, QComboBox, QSpinBox, QLineEdit,
)
from PySide6.QtGui import (
    QPixmap, QIcon, QMovie, Qt, QFont, QMouseEvent, QBrush, QColor
)
from tkinter.filedialog import askopenfilename, asksaveasfilename
from src.window_extratos import Ui_MainWindow
from PySide6.QtCore import QThread, QSize
from banks.banco_do_brasil import BancoDoBrasil
from banks.mercado_pago import MercadoPago
from generator import Generator
from tkinter import messagebox
from dotenv import load_dotenv
from database import DataBase
from banks.bradesco import Bradesco
from banks.pag_bank import PagBank
from banks.santa_fe import SantaFe
from changes import Change
from banks.sicoob import Sicoob
from os import startfile
from pathlib import Path
from banks.caixa import Caixa
from banks.inter import Inter
from banks.itau import Itau
from file import File
from bank import Bank
import pandas as pd
import sys

load_dotenv(Path(__file__).parent / 'src' / 'env' / '.env')

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Classe principal da interface gráfica do Conversor de Extrato.
    Gerencia a interação do usuário, operações de CRUD e execução do processamento dos extratos.
    """
    PLCHR_COMBOBOX = 'Selecione a opção'

    def __init__(self, parent = None) -> None:
        """
        Inicializa a janela principal, widgets, conexões e variáveis de estado.
        """
        super().__init__(parent)
        self.setupUi(self)

        self.db = DataBase()
        self.companies_checkbox = {}
        self.min_carc_companie = 6
        self.disable_status = True

        self.message_select = 'Primeiro, clique 1 vez na empresa que deseja {0}'
        self.message_remove = 'Confirma a remoção desta empresa?\nTodas suas contas cadastradas também serão excluídas'
        self.message_save = 'Tem certeza que deseja salvar estas alterações?'
        self.message_no_save = 'Não há alterações a serem salvas'
        self.message_exit_save = 'Tem certeza que deseja sair da referência SEM SALVAR as mudanças feitas nela?\n\nCaso não queira PERDER as alterações, selecione "não" e as salve'

        self.font_text = QFont()
        self.font_text.setFamilies([u"Bahnschrift"])
        self.font_text.setPointSize(12)

        self.current_operation = ''
        self.ref_operation = {
            'add': self.confirm_add_refence,
            'updt': self.confirm_updt_reference
        }

        self.add_brush = QBrush(QColor(179, 255, 178, 255))
        self.add_brush.setStyle(Qt.BrushStyle.Dense1Pattern)

        self.updt_brush = QBrush(QColor(189, 253, 254, 255))
        self.updt_brush.setStyle(Qt.BrushStyle.Dense1Pattern)

        self.remove_brush = QBrush(QColor(254, 139, 139, 255))
        self.remove_brush.setStyle(Qt.BrushStyle.Dense1Pattern)

        self.no_brush = QBrush(Qt.BrushStyle.NoBrush)

        self.default_resp = [
            '', '0', 'C'
        ]

        self.ref_input = {
            QComboBox : lambda value, widget: widget.\
                setCurrentIndex(['C','D'].index(value)),
            QSpinBox : lambda value, widget: widget.setValue(int(value)),
            QLineEdit : lambda value, widget: widget.setText(value)
        }

        self.ref_input_text = {
            QComboBox : lambda widget: widget.currentText(),
            QLineEdit : lambda widget: widget.text(),
            QSpinBox : lambda widget: widget.text(),
        }

        self.inputs = [
            self.lineEdit_word, self.spinBox_value, self.comboBox_release
        ]

        self.dict_nick_bank = {
            'caixa': Caixa(),
            'santa fé' : SantaFe(),
            'santa fe' :SantaFe(),
            'banco do brasil': BancoDoBrasil(),
            'bb' : BancoDoBrasil(),
            'sicoob': Sicoob(),
            'inter' : Inter(),
            'itaú': Itau(),
            'itau': Itau(),
            'mercado pago': MercadoPago(),
            'bradesco': Bradesco(),
            'pagbank': PagBank(),
        }

        self.connections = {}
        self.ref_universal = {
            'companies': [
                {
                    self.pushButton_add: self.add_companie,
                    self.pushButton_remove: self.remove_companie,
                    self.pushButton_update: self.updt_companie,
                    self.pushButton_reload: self.fill_companie,
                    self.pushButton_confirm: self.confirm_companie,
                    self.pushButton_cancel: self.cancel_companie
                },
                {
                    self.pushButton_add: 'Adciona empresa a lista de empresas cadastradas',
                    self.pushButton_remove: 'Remove empresa cadastrada',
                    self.pushButton_update: 'Edita o nome de empresa cadastrada',
                    self.pushButton_reload: 'Recarrega as empresas salvas no servidor',
                }
            ],
            'reference': [
                {
                    self.pushButton_add: self.add_reference,
                    self.pushButton_remove: self.remove_reference,
                    self.pushButton_save: self.save_reference,
                    self.pushButton_reload: lambda : self.fill_reference(
                        self.dict_bank_text[
                            self.comboBox.currentText()
                        ]
                    ),
                    self.pushButton_confirm: self.confirm_reference,
                    self.pushButton_cancel:
                        lambda: self.stackedWidget_reference.setCurrentIndex(0)
                },
                {
                    self.pushButton_add: 'Adciona imposto a lista de impostos cadastrados',
                    self.pushButton_remove: 'Remove imposto cadastrado',
                    self.pushButton_save: 'Edita o nome de imposto cadastrado',
                    self.pushButton_reload: 'Recarrega a relações de palavra do servidor',
                }
            ]
        }

        self.enable_status = True
        self.extend_disable = [
            self.pushButton_upload,
            self.comboBox
        ]
        self.ref_disable_btns = [
            self.pushButton_add,
            self.pushButton_remove,
            self.pushButton_save,
            self.pushButton_update,
            self.pushButton_execute,
            self.pushButton_exit,
            self.pushButton_reload,
        ]
        self.disable_buttons(False)
        self.label_companie_info.hide()
        self.frame_operations.hide()
        self.switch_focus('companies')

        self.dict_bank_text = self.db.bank()
        self.comboBox.setPlaceholderText(self.PLCHR_COMBOBOX)
        self.comboBox.addItems(list(self.dict_bank_text.keys()))
        
        self.checkBox_font = QFont()
        self.checkBox_font.setFamilies([u"Bahnschrift"])
        self.checkBox_font.setWeight(QFont.Weight.Light)
        self.checkBox_font.setPointSize(14)

        self.arquivo = File()
        self.setWindowIcon(QIcon(
            (Path(__file__).parent / 'src' / 'imgs' / 'extr-icon.ico').__str__()
            )
        )
        self.setWindowTitle('Conversor de Extrato')

        self.movie = QMovie(
            (Path(__file__).parent / 'src'/ 'imgs' / 'load.gif').__str__()
        )
        self.label_load.setMovie(self.movie)

        icon = QIcon()
        icon.addFile(
            (Path(__file__).parent / 'src'/ 'imgs' / 'upload-icon.png').__str__(),
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off
        )
        self.pushButton_upload.setIcon(icon)

        #Logo
        self.logo_hori.setPixmap(QPixmap(
                (Path(__file__).parent / 'src' / 'imgs' / 'extrato_horizontal.png').__str__()
            )
        )
        self.pushButton_save.setHidden(True)

        self.table_reference.itemDoubleClicked.connect(self.updt_reference)
        self.comboBox.currentTextChanged.connect(self.search_companie)
        self.pushButton_upload.clicked.connect(self.attach)
        self.pushButton_execute.clicked.connect(self.execute)

        self.pushButton_add.clicked.connect(self.in_operation)
        self.pushButton_update.clicked.connect(self.in_operation)
        self.pushButton_cancel.clicked.connect(self.in_operation)
        self.pushButton_confirm.clicked.connect(self.in_operation)
        self.pushButton_exit.clicked.connect(self.exit)
            
    def exit(self):
        """
        Gerencia a saída da tela de referência, verificando alterações não salvas.
        """
        if self.has_change():
            if messagebox.askyesno('Aviso', self.message_exit_save) == False:
                return None
        
        self.pushButton_save.setHidden(True)
        self.pushButton_update.setHidden(False)
        self.stackedWidget_companie.setCurrentIndex(0)
        self.switch_focus('companies')

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        """
        Detecta duplo clique em radio buttons para abrir referências.
        """
        widget = self.childAt(event.position())
        if widget is not None and type(widget) == QRadioButton :
            self.open_reference(widget)

    def in_operation(self):
        """
        Alterna o estado de operação (edição/adicionar/cancelar).
        """
        self.disable_buttons()
        hide = not self.frame_operations.isHidden()
        self.frame_operations.setHidden(hide)
        
    def disable_buttons(self, extend = True):
        """
        Habilita/desabilita botões conforme o estado da interface.
        """
        self.enable_status = not self.enable_status
        disable_list = self.ref_disable_btns 
        if extend == True:
            disable_list.extend(self.extend_disable)

        for item in disable_list:
            item.setEnabled(self.enable_status) 

    def switch_focus(self, current_widget: str):
        """
        Alterna o foco entre empresas e referências.
        """
        ref_connection = {}
        ref_tool_tip = {}

        ref_connection, ref_tool_tip = self.ref_universal[current_widget]
        self.re_connection(ref_connection)
        self.re_tool_tip(ref_tool_tip)

    def re_connection(self, ref):
        """
        Reconecta os sinais dos botões conforme o contexto.
        """
        for widget, connection in self.connections.items():
            widget.disconnect(connection)
        self.connections.clear()

        for widget, func in ref.items():
            self.connections[widget] = widget.clicked.connect(func)

    def re_tool_tip(self, ref):
        """
        Atualiza as tooltips dos botões.
        """
        for widget, text in ref.items():
            widget.setToolTip(text)

    def open_reference(self, radio: QRadioButton):
        """
        Abre a tela de referência para a empresa selecionada.
        """
        self.switch_focus('reference')
        self.label_current_companie.setText(radio.text())
        self.current_companie_id = self.companies_checkbox[radio]
        id_bank = self.dict_bank_text[self.comboBox.currentText()]

        self.fill_reference(id_bank)

        self.pushButton_save.setHidden(False)
        self.pushButton_update.setHidden(True)
        self.stackedWidget_companie.setCurrentIndex(1)

    def fill_reference(self, id_bank):
        """
        Preenche a tabela de referências com dados do banco.
        """
        self.table_reference.clearContents()

        ids, data = self.db.reference(id_bank, self.current_companie_id)
        self.table_reference.setColumnCount(len(data.keys()))
        self.table_reference.setRowCount(len(ids))
        for column, column_data in enumerate(data.values()):
            for row, value in enumerate(column_data):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.__setattr__('id', ids[row])
                item.__setattr__('edited', False)
                item.setText(str(value))
                self.table_reference.setItem(row, column, item)

    def confirm_reference(self):
        """
        Confirma a operação de adicionar ou atualizar referência.
        """
        self.ref_operation[self.current_operation]()

    def add_reference(self):
        """
        Prepara a interface para adicionar uma nova referência.
        """
        for column in range(self.table_reference.columnCount()):
            input = self.inputs[column]
            self.ref_input[type(input)](self.default_resp[column], input)
        
        self.current_operation = 'add'
        self.stackedWidget_reference.setCurrentIndex(1)

    def confirm_add_refence(self):
        """
        Confirma a adição de uma nova referência.
        """
        resp = self.__inputs_response()

        row = self.table_reference.rowCount()
        self.table_reference.setRowCount(row + 1)
        for column in range(self.table_reference.columnCount()):
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.__setattr__('id', None)
            item.__setattr__('edited', False)
            item.setText(resp[column])
            item.setBackground(self.add_brush)
            self.table_reference.setItem(row, column, item)
            
        self.stackedWidget_reference.setCurrentIndex(0)

    def __inputs_response(self):
        """
        Coleta os valores dos inputs da referência.
        """
        resp = []
        for input in self.inputs:
            text = self.ref_input_text[type(input)](input)
            resp.append(text)
        return resp
    
    def updt_reference(self):
        """
        Prepara a interface para atualizar uma referência existente.
        """
        self.in_operation()
        item = self.table_reference.selectedItems()[0]
        row = item.row()
        for column in range(self.table_reference.columnCount()):
            item = self.table_reference.item(row, column)
            input = self.inputs[column]
            self.ref_input[type(input)](item.text(), input)

        self.current_operation = 'updt'
        self.stackedWidget_reference.setCurrentIndex(1)

    def confirm_updt_reference(self):
        """
        Confirma a atualização de uma referência.
        """
        bush = ''
        edited = True

        resp = self.__inputs_response()
        item = self.table_reference.selectedItems()[0]
        row = item.row()

        #Mudou mesmo?
        if self.__check_updt(resp, row) == False:
            return self.stackedWidget_reference.setCurrentIndex(0)
        
        #Esses dados já existiram nessa sessão?
        # elif self.__check_season_updt(resp) == True:
        #     bush = self.no_brush
        #     edited = False

        else:
            if None == item.__getattribute__('id'):
                bush = self.add_brush
            else:
                bush = self.updt_brush
        
        for column in range(self.table_reference.columnCount()):
            item = self.table_reference.item(row, column)
            item.__setattr__('edited', edited)
            item.setBackground(bush)
            item.setText(resp[column])

        self.stackedWidget_reference.setCurrentIndex(0)

    def __check_updt(self, resp, row):
        """
        Verifica se houve alteração nos dados da referência.
        """
        for column in range(self.table_reference.columnCount()):
            item = self.table_reference.item(row, column)
            if item.text() != resp[column]:
                return True
        return False
    
    def remove_reference(self):
        """
        Marca uma referência para remoção ou desfaz a remoção.
        """
        try:
            item = self.table_reference.selectedItems()[0]
            row = item.row()
            if item.background() == self.add_brush:
                self.table_reference.removeRow(row)
                return None
            
            bush = self.remove_brush
            if item.background() == self.remove_brush:
                bush = self.updt_brush\
                    if True == item.__getattribute__('edited')\
                        else self.no_brush

            for column in range(self.table_reference.columnCount()):
                item = self.table_reference.item(row, column)
                item.setBackground(bush)
        except IndexError:
            messagebox.showerror('Aviso', 'Primeiro, selecione a referência que deseja remover')

    def save_reference(self):
        """
        Salva as alterações feitas nas referências no banco de dados.
        """
        try:
            self.disable_buttons()

            if self.has_change() == False:
                raise Exception(self.message_no_save)
            
            if messagebox.askyesno('Aviso', self.message_save) == False:
                return None
           
            id_bank = self.dict_bank_text.get(self.comboBox.currentText())
            self.db.execute_change(
                id_bank, self.current_companie_id, self.change_reference()
            )
            self.fill_reference(id_bank)
            
            self.disable_buttons()
        except Exception as err:
            self.disable_buttons()
            messagebox.showerror('Aviso', err)

    def has_change(self)-> bool:
        """
        Verifica se há alterações pendentes na tabela de referências.
        """
        for row in range(self.table_reference.rowCount()):
            item = self.table_reference.item(row, 0)
            if item.background() != self.no_brush:
                return True
        return False

    def change_reference(self) -> Change | None:
        """
        Coleta as alterações feitas na tabela de referências.
        """
        changes = Change()
        for row in range(self.table_reference.rowCount()):
            item = self.table_reference.item(row, 0)
            brush = item.background()
            if brush == self.no_brush:
                continue

            elif brush == self.add_brush:
                data = self.__data_row(row)
                changes.to_add(data)

            elif brush == self.updt_brush:
                data = self.__data_row(row)
                changes.to_updt(
                    self.table_reference.item(row, 0)\
                        .__getattribute__('id'), 
                    data
                )

            elif brush == self.remove_brush:
                changes.to_remove(
                    self.table_reference.item(row, 0)\
                        .__getattribute__('id')
                )
        return changes
    
    def __data_row(self, row) -> dict[str]:
        """
        Retorna os dados de uma linha da tabela de referências.
        """
        data = {}
        for column in range(self.table_reference.columnCount()):
            item = self.table_reference.item(row, column)
            key = self.table_reference.horizontalHeaderItem(column)
            data[key.text()] = item.text()
        return data

    def execute(self):
        """
        Executa o processamento do extrato selecionado.
        """
        try:  
            if self.arquivo.is_uploaded() == False:
                   raise FileNotFoundError() 
            
            if self.has_change() == True:
                raise Exception('Antes de executar, salve as alterações feitas ou as descarte clicando em "voltar"')

            option = self.comboBox.currentText()
            id_bank = self.dict_bank_text.get(option)
            reference = self.reference(id_bank)
            bank = self.bank()
            self._gerador = Generator(
                bank,
                self.arquivo,
                option[option.rfind('-')+2:],
                reference
            )
            self._thread = QThread()

            self._gerador.moveToThread(self._thread)
            self._thread.started.connect(self._gerador.extrato)
            self._gerador.fim.connect(self._thread.quit)
            self._gerador.fim.connect(self._thread.deleteLater)
            self._gerador.fim.connect(self.alter_estado)
            self._gerador.open.connect(self.open_result)
            self._gerador.inicio.connect(self.alter_estado)
            
            self._thread.finished.connect(self._gerador.deleteLater)
            self._thread.start() 

        except PermissionError:
            messagebox.showerror(title='Aviso', message= 'Feche o arquivo gerado antes de criar outro')
        except FileNotFoundError:
            messagebox.showerror(title='Aviso', message= "Primeiro, faça upload do extrato desejado")
        except Exception as error:
            messagebox.showerror(title='Aviso', message= error)
        finally:
            self.alter_estado(False)

    def open_result(self, arquivo_final: pd.DataFrame):
        """
        Salva e abre o arquivo de extrato processado.
        """
        file = asksaveasfilename(title='Favor selecionar a pasta onde será salvo', filetypes=((".xlsx","*.xlsx"),))

        if file == '':
            resp = messagebox.askyesno(title='Aviso', message= 'Deseja cancelar a operação?')
            if resp == True:
                messagebox.showinfo(title='Aviso', message= 'Operação cancelada!')
                return None
            else:
                return self.open_result(arquivo_final)

        arquivo_final.to_excel(file+'.xlsx', index=False)
        messagebox.showinfo(title='Aviso', message='Abrindo o arquivo gerado!')
        startfile(file+'.xlsx')

    def alter_estado(self, cond: bool):
        """
        Altera o estado da interface durante o processamento.
        """
        self.exec_load(cond)
        self.pushButton_execute.setDisabled(cond)

    def exec_load(self, action: bool):
        """
        Exibe ou oculta o indicador de carregamento.
        """
        if action == True:
            self.movie.start()
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.movie.stop()
            self.stackedWidget.setCurrentIndex(0)

    def search_companie(self):
        """
        Busca e exibe as empresas cadastradas para o banco selecionado.
        """
        if self.scrollArea.isEnabled() == False:
            self.scrollArea.setDisabled(False)
            self.label_aviso.hide()
            self.vbox = QVBoxLayout()
            self.label_companie_info.setHidden(False)
            self.disable_buttons()
        else:
            self.scrollArea.widget().destroy()
            for checkBox in self.companies_checkbox.keys():
                self.vbox.removeWidget(checkBox)
                checkBox.destroy()

        widget = QWidget()
        self.fill_companie()

        widget.setLayout(self.vbox)
        self.scrollArea.setWidget(widget)

    def fill_companie(self):
        """
        Preenche a lista de empresas cadastradas.
        """
        empresas_disp = self.db.companie(
            self.dict_bank_text[self.comboBox.currentText()]
        )

        for widget in self.companies_checkbox.keys():
            widget.deleteLater()

        self.companies_checkbox.clear()
        for id_emp, nome_emp in empresas_disp.items():
            self.create_companie(id_emp, nome_emp)

    def create_companie(self, id_emp, nome_emp):
        """
        Cria um radio button para uma empresa.
        """
        item = QRadioButton(nome_emp)
        item.__setattr__('id', id_emp)
        item.setFont(self.checkBox_font)
        self.companies_checkbox[item] = id_emp
        self.vbox.addWidget(item)

    def add_companie(self):
        """
        Prepara a interface para adicionar uma nova empresa.
        """
        self.disable_option()
        self.pushButton_confirm.hide()
        item = QLineEdit(placeholderText='Nome da empresa (min. 6 caracteres)')
        item.setFont(self.font_text)
        item.__setattr__('id', None)
        item.textChanged.connect(self.companie_valid)
        
        self.current_item_edited = item
        self.vbox.addWidget(item)

    def updt_companie(self):
        """
        Prepara a interface para atualizar o nome de uma empresa.
        """
        try:
            check_box = self.find_option()
            self.disable_option()
            check_box.hide()
            item = QLineEdit(text= check_box.text())
            item.setFont(self.font_text)
            item.__setattr__('id', check_box.__getattribute__('id'))
            item.textChanged.connect(self.companie_valid)

            
            self.current_item_edited = item
            self.vbox.addWidget(item)
        except Exception as error:
            messagebox.showerror(title='Aviso', message= error)
            self.in_operation()

    def remove_companie(self):
        """
        Remove uma empresa selecionada.
        """
        try:
            self.disable_buttons()
            self.disable_option()
            checkbox = self.find_option()
            if messagebox.askyesno('Aviso', self.message_remove) == False:
                self.disable_buttons()
                self.disable_option()
                return None
            
            self.db.remove_companie(checkbox.__getattribute__('id'))
            self.companies_checkbox.pop(checkbox)
            checkbox.deleteLater()
            self.disable_buttons()
            self.disable_option()
        except Exception as error:
            messagebox.showwarning('Aviso', error)
            self.disable_buttons()
            self.disable_option()

    def find_option(self):
        """
        Retorna o widget da empresa selecionada.
        """
        for widget in self.companies_checkbox.keys():
            if widget.isChecked():
                return widget
        raise Exception('Primeiro selecione a empresa')

    def disable_option(self):
        """
        Habilita/desabilita as opções de empresa.
        """
        disable = self.disable_status
        self.disable_status = not disable
        for widget in self.companies_checkbox.keys():
            widget.setDisabled(disable)

    def confirm_companie(self):
        """
        Confirma a adição ou atualização de uma empresa.
        """
        try:
            item = self.current_item_edited
            name = item.text()
            if name == '':
                raise Exception('Nome de empresa inválida')
            
            id = item.__getattribute__('id')
            if id == None:
                id_bank = self.dict_bank_text.get(self.comboBox.currentText())
                id = self.db.add_companie(id_bank, name)
                self.create_companie(id, name)
            else:
                check_box = self.find_option()
                if check_box.text() != name:
                    self.db.edit_companie(id, name)
                    check_box.setText(name)
                check_box.setHidden(False)

            self.disable_option()
            item.deleteLater()
        except Exception as error:
            messagebox.showwarning('Aviso', error)

    def cancel_companie(self):
        """
        Cancela a operação de adição/edição de empresa.
        """
        item = self.current_item_edited
        id = item.__getattribute__('id')
        if id != None:
            check_box = self.find_option()
            check_box.setHidden(False)
        self.disable_option()
        item.deleteLater()

    def companie_valid(self):
        """
        Valida o nome da empresa inserido.
        """
        hide = True
        if len(self.current_item_edited.text()) > self.min_carc_companie:
            hide = False
        self.pushButton_confirm.setHidden(hide)

    def reference(self, id_bank: int) -> int:
        """
        Retorna as referências cadastradas para a empresa selecionada.
        """
        for widget, id_emp in self.companies_checkbox.items():
            if widget.isChecked():
                return self.db.reference(id_bank, id_emp)[1]
        return {}

    def bank(self) -> Bank:
        """
        Retorna a instância do banco selecionado.
        """
        for key, bank in self.dict_nick_bank.items():
            if key in self.comboBox.currentText().lower():
                return bank

    def attach(self):
        """
        Realiza o upload do arquivo de extrato.
        """
        try:
            file_stem = self.arquivo.set_path(askopenfilename())
            if file_stem != None:
                self.pushButton_upload.setText(file_stem)
                self.pushButton_upload.setIcon(QPixmap(''))

                self.select_combo(file_stem)

        except PermissionError:
            messagebox.showerror(title='Aviso', message= 'O arquivo selecionado apresenta-se em aberto em outra janela, favor fecha-la')
        except FileExistsError:
            #apagar arquivo já existente e executar novamente
            messagebox.showerror(title='Aviso', message= 'O arquivo selecionado já apresenta uma versão sem acento, favor usar tal versão ou apagar uma delas')
        except Exception as error:
            messagebox.showerror(title='Aviso', message= error)

    def select_combo(self, file_stem: str):
        """
        Seleciona automaticamente o banco no combobox com base no nome do arquivo.
        """
        for key in self.dict_nick_bank.keys():
            if key in file_stem.lower():
                self.comboBox.setCurrentIndex(
                    self.comboBox.findText(
                        key, Qt.MatchFlag.MatchContains
                    )
                )

if __name__ == '__main__':
    """
    Ponto de entrada da aplicação.
    """
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()