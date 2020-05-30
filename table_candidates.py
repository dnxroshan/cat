
import pymysql
import config

class TableCandidates():
    def __connect(self):
        return pymysql.connect(host=config.HOST,
                               user=config.USER,
                               passwd=config.PASSWORD,
                               db=config.DATABASE
        )

    def add_candidate(self, data):
        connection = self.__connect()

        with connection as cursor:
            query = 'INSERT INTO candidates VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);'
            cursor.execute(query, tuple(data.values()))

    def get_candidate(self, username):
        connection = self.__connect()

        with connection as cursor:
            query = 'SELECT * FROM candidates WHERE username = %s;'
            cursor.execute(query, username)
            data = cursor.fetchall()

            if not data:
                return None

            data = data[0]

            fields = (  
                        'username', 
                        'first_name',
                        'last_name',
                        'dob',
                        'gender',
                        'standard',
                        'school',
                        'email',
                        'phone'
            )

            return dict(zip(fields, data))


