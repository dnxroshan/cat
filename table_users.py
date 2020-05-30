
import pymysql
import config


class TableUsers():
    def __connect(self):
        return pymysql.connect(host=config.HOST,
                               user=config.USER,
                               passwd=config.PASSWORD,
                               db = config.DATABASE)

    def get_user(self, username):
        with self.__connect() as cursor:
            query = 'SELECT * FROM users WHERE username = %s;'
            cursor.execute(query, username)
            data = cursor.fetchall()

            if not data: return None

            data = data[0]

            return {
                    'username' : data[0], 
                    'salt'     : data[1], 
                    'hashed'   : data[2], 
                    'type'     : int(data[3])
            }

    def add_user(self, new_user):

        connection = self.__connect()
        with connection as cursor:
            query = 'INSERT INTO users VALUES(%s, %s, %s, %s);'
            cursor.execute(query, tuple(new_user.values()))
            connection.commit()
