
import pymysql

import config

connection = pymysql.connect(host=config.HOST,
                             user=config.USER,
                             passwd=config.PASSWORD)

with connection as cursor:
    query = 'CREATE DATABASE IF NOT EXISTS {};'.format(config.DATABASE)
    cursor.execute(query)
    query = 'USE {};'.format(config.DATABASE)
    cursor.execute(query)   
    query = '''CREATE TABLE IF NOT EXISTS users
               (
                    username VARCHAR(50),
                    salt     CHAR(128)      NOT NULL,
                    hashed   CHAR(128)      NOT NULL,
                    type     CHAR           NOT NULL,

                    PRIMARY KEY(username)
               );'''

    cursor.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS candidates
               (
                   username   VARCHAR(50),
                   first_name VARCHAR(50) NOT NULL,
                   last_name  VARCHAR(50) NOT NUll,
                   dob        DATE        NOT NULL,
                   gender     CHAR(8)     NOT NULL,
                   standard   CHAR(8)     NOT NULL,
                   school     VARCHAR(20),
                   email      VARCHAR(20),
                   phone      VARCHAR(20),

                   PRIMARY KEY(username),
                   FOREIGN KEY(username) REFERENCES users(username)
               );'''
    cursor.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS examiners
               (
                   username     VARCHAR(50),
                   first_name   VARCHAR(50) NOT NULL,
                   last_name    VARCHAR(50) NOT NULL,
                   subject      VARCHAR(50) NOT NULL,
                   school       VARCHAR(50),

                   PRIMARY KEY(username),
                   FOREIGN KEY(username) REFERENCES users(username)
               );'''
    cursor.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS tests
               (
                   test_id          INT             AUTO_INCREMENT,
                   examiner         VARCHAR(50)     NOT NULL,
                   title            VARCHAR(50)     NOT NULL,
                   description      VARCHAR(500)    NOT NULL,
                   date             DATE            NOT NULL,
                   subject          VARCHAR(50)     NOT NULL,
                   standard         VARCHAR(50)     NOT NULL,
                   score_easy       FLOAT           NOT NULL,
                   score_medium     FLOAT           NOT NULL,
                   score_hard       FLOAT           NOT NULL,
                   score_threshold  FLOAT           NOT NULL,

                   PRIMARY KEY(test_id),
                   FOREIGN KEY(examiner) REFERENCES examiners(username)
               );'''
    cursor.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS results
               (
                   result_id    INT         AUTO_INCREMENT,
                   test         INT         NOT NULL,
                   candidate    VARCHAR(50) NOT NULL,
                   date         DATE        NOT NULL,
                   score        INT         NOT NULL,
                   passed       BOOL        NOT NULL,

                   PRIMARY KEY(result_id),
                   FOREIGN KEY(test)      REFERENCES tests(test_id),
                   FOREIGN KEY(candidate) REFERENCES candidates(username)
               );'''
    cursor.execute(query)

    connection.commit()
    