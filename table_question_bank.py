
import pymysql

import config
from table import Table

class TableQuestionBank(Table):

    def add(self, data):
        connection = self.connect()

        with connection as cursor:
            query = '''INSERT INTO question_bank
                       (
                           test, 
                           question, 
                           option_a, 
                           option_b, 
                           option_c, 
                           option_d,
                           answer,
                           difficulty
                        )
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s);'''

            cursor.executemany(query, data)
            connection.commit()

    def get_random_question(self, test, difficulty):
        connection = self.connect()

        with connection as cursor:
            query = ''' SELECT 
                            question_id, 
                            question, 
                            option_a, 
                            option_b, 
                            option_c, 
                            option_d 
                        FROM question_bank 
                        WHERE test = %s AND difficulty = %s
                        ORDER BY RAND()
                        LIMIT 1;'''

            cursor.execute(query, (test, difficulty))
            return cursor.fetchone()

    def get_answer(self, question_id):
        connection = self.connect()

        with connection as cursor:
            query = 'SELECT answer FROM question_bank WHERE question_id = %s;'

            cursor.execute(query, question_id)

            return cursor.fetchone()[0]

