
import pymysql
import config

class TableTests:
    def __connect(self):
        return pymysql.connect(host=config.HOST, 
                               user=config.USER, 
                               passwd=config.PASSWORD, 
                               db=config.DATABASE)

    def add(self, data):
        connection = self.__connect()

        with connection as cursor:
            query = '''INSERT INTO tests
                       (
                           examiner,
                           title, 
                           description,
                           date,
                           subject,
                           standard, 
                           score_easy,
                           score_medium,
                           score_hard, 
                           score_threshold 
                        ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

            cursor.execute(query, tuple(data.values()))
            connection.commit()

    def get_by_test_id(self, test_id):
        connection = self.__connect()

        with connection as cursor:
            query = 'SELECT * FROM tests WHERE test_id = %s;'

            cursor.execute(query, test_id)
            data = cursor.fetchone()

            if not data:
                return None

            fields = (
                'test_id', 
                'examiner',
                'title', 
                'description',
                'date',
                'subject',
                'standard', 
                'score_easy',
                'score_medium',
                'score_hard' ,
                'score_threshold', 
            )

            return dict(zip(fields, data))

    def get_by_examiner(self, examiner):
        connection = self.__connect()

        with connection as cursor:
            query = 'SELECT * FROM tests WHERE examiner = %s;'

            cursor.execute(query, examiner)
            data = cursor.fetchall()

            if not data:
                return None

            fields = (
                'test_id', 
                'examiner',
                'title', 
                'description',
                'date',
                'subject',
                'standard', 
                'score_easy',
                'score_medium',
                'score_hard' ,
                'score_threshold' 
            )

            records = []
            for row in data:
                records.append(dict(zip(fields, row)))

            return records

    
    def get_new_id(self):
        connection = self.__connect()

        with connection as cursor:
            query = '''SELECT AUTO_INCREMENT FROM information_schema.TABLES
                       WHERE TABLE_SCHEMA = "{}"
                       AND TABLE_NAME = "tests";
                    '''.format(config.DATABASE)

            cursor.execute(query)
            return cursor.fetchone()[0]

    def search(self, title, subject, date, standard):
        connection = self.__connect()

        if not title:
            title = '%'
        if subject == 'All':
            subject = '%'
        if not date:
            date = '%'

        query = ''' SELECT
                        test_id, 
                        title, 
                        description, 
                        date, 
                        subject, 
                        examiner 
                    FROM tests 
                    WHERE 
                        title LIKE %s 
                    AND date LIKE %s
                    AND subject LIKE %s 
                    AND standard = %s;'''
                    
        with connection as cursor:
            cursor.execute(query, (title, date, subject, standard))
            data = cursor.fetchall()

            if not data:
                return None

            fields = (
                'test_id',
                'title', 
                'description', 
                'date', 
                'subject',
                'examiner'
            )
            records = []
            for row in data:
                records.append(dict(zip(fields, row)))

            return records

    def get_scores(self, test_id):
        connection = self.__connect()

        with connection as cursor:
            query = '''SELECT 
                            score_easy, 
                            score_medium, 
                            score_hard 
                        FROM tests 
                        WHERE test_id = %s;'''

            cursor.execute(query, test_id)
            data = cursor.fetchone()

            if not data:
                return None

            fields = (
                'score_easy',
                'score_medium',
                'score_hard' 
            )

            return dict(zip(fields, data))

    def get_threshold_score(self, test_id):
        connection = self.__connect()

        with connection as cursor:
            query = '''SELECT 
                            score_threshold
                        FROM tests 
                        WHERE test_id = %s;'''

            cursor.execute(query, test_id)
            data = cursor.fetchone()

            if not data:
                return None

            return data[0]
