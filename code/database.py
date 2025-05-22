from pymysql import connect
from changes import Change
from os import getenv

class DataBase:
    COMPANIE_TABLE = 'Companie'
    BANK_TABLE = 'Bank'
    REFERENCE_TABLE = 'Reference'

    def __init__(self) -> None:
        self.connection = connect(
                host= getenv('IP_HOST'),
                port= int(getenv('PORT_HOST')),
                user= getenv('USER'),
                password= getenv('PASSWORD'),
                database= getenv('DB'),
            )
        
        self.columns_reference = [
            'id_reference', 'word', 'account', 'release_letter' 
        ]

        self.query_bank = (
            f'SELECT id_bank, name, code FROM {self.BANK_TABLE} '
        )

        self.query_companie = (
            f'SELECT id_companie, name FROM {self.COMPANIE_TABLE} '
            'WHERE id_bank = %s '
        )

        self.query_reference =  (
            f'SELECT {', '.join(self.columns_reference)} '
            f'FROM {self.REFERENCE_TABLE} '
            'WHERE id_bank = %s AND id_companie = %s'
        )

        self.insert_pedency = (
            f'INSERT INTO {self.REFERENCE_TABLE} '
            '(id_bank, id_companie, word, '
            'account, release_letter) '
            'VALUES (%(id_bank)s, %(id_companie)s,'
            '%(Palavra)s, %(Conta)s, %(Lançamento)s)'
        )

        self.insert_companie = (
            f'INSERT INTO {self.COMPANIE_TABLE} '
            '(id_bank, name) VALUES (%s, %s) '
        )

        self.update_companie = (
            f'UPDATE {self.COMPANIE_TABLE} SET '
            'name = %s '
            'WHERE id_companie = %s'
        )

        self.delete_companie = (
            f'DELETE FROM {self.COMPANIE_TABLE} '
            'WHERE id_companie = %s ; '
        )

        self.update_reference = (
            f'UPDATE {self.REFERENCE_TABLE} SET '
            'word = %(Palavra)s, account = %(Conta)s, '
            'release_letter = %(Lançamento)s '
            'WHERE id_reference = %(id_reference)s '
        )

        self.delete_reference = (
            f'DELETE FROM {self.REFERENCE_TABLE} '
            'WHERE id_reference = %s ; '
        )

        pass

    def add_companie(self, id_bank, name):
        cursor = self.__request(self.insert_companie, (id_bank, name,))
        return cursor.lastrowid
    
    def edit_companie(self, id, name):
        self.__request(self.update_companie, (name, id))

    def remove_companie(self, id):
        self.__request(self.delete_companie, (id,))

    def companie(self, id_bank: int) -> dict[int, str]:
        cursor = self.__request(self.query_companie, (id_bank,))
        return { id: nome for id, nome in cursor.fetchall() }

    def bank(self) -> dict[str, int]:
        cursor = self.__request(self.query_bank)
        return { 
            f'{name} - {code}': id for id, name, code in cursor.fetchall()
        }
    
    def reference(self, id_bank: int, id_companie: int):
        cursor = self.__request(self.query_reference, (id_bank, id_companie))
        data = {key: [] for key in self.columns_reference}
        for sub in cursor.fetchall():
            for index, i in enumerate(sub):
                data[self.columns_reference[index]].append(i)
            
        ids = data.pop('id_reference')
        return ids, data
    
    def execute_change(self, id_bank, id_companie: str, change: Change):
        #list[dict], dict[tuple[dict]], list[int]
        add, updt, remove = change.data()

        #ADD
        if any(add):
            self.__tranform_add(id_bank, id_companie, add)
            self.__request(self.insert_pedency, add, True)

        #UPDATE
        if any(updt):
            updt_list = []
            for id_reference, data in updt.items():
                data[0]['id_reference'] = id_reference
                updt_list.append(data[0])
            self.__request(self.update_reference, updt_list, True)

        #REMOVE
        if any(remove):
            # ([id_companie, id_data] for id_data in data)
            self.__request(self.delete_reference, remove, True)


    def __tranform_add(self, id_bank, id_companie, add):
        for data in add:
            data['id_bank'] = id_bank
            data['id_companie'] = id_companie

    def __request(self, query, input = (), many = False):
        with self.connection.cursor() as cursor:
            func = cursor.executemany if many else cursor.execute
            func(query, input)
            self.connection.commit()
        return cursor