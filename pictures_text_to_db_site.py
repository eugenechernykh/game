import MySQLdb
import random
from collections import namedtuple
from os import path
import configparser
from DBUtils.PooledDB import PooledDB

config = configparser.ConfigParser()
config.read('C:\\Users\echernykh.ECHERNYKH\mysql\config.ini')
pool = PooledDB(creator=MySQLdb,
                mincached=1,
                maxcached=4,
                host=config['mysqlDB']['host'],
                user=config['mysqlDB']['user'],
                passwd=config['mysqlDB']['pass'],
                db=config['mysqlDB']['db'], charset='utf8')
db = pool.connection()


# directories initialisation
game_dir = path.dirname(__file__)
img_dir = path.join(game_dir, 'img')
data_dir = path.join(game_dir, 'data')

Images = namedtuple("Images", "pic text questions")


def load_files(text_file_name):
    my_images = []
    with open(path.join(data_dir, text_file_name), 'r',
              encoding='utf8') as inFile:
        for line in inFile:
            my_list = list(line.strip().split(','))
            if line == '\n':
                continue
            pic, text, que = my_list[0], my_list[1], my_list[2:]
            questions = {}
            for i in range(len(que)):
                if i % 2 == 1:
                    questions[que[i - 1]] = que[i]
            my_images.append(Images(pic, text, questions))

    return my_images


def insert_from_file_to_db(my_list):
    # Подготовка объекта cursor с помощью метода cursor()
    cursor = db.cursor()
    # my code:
    for img in my_list:
        try:
            sql_pics = """INSERT INTO first_picture (name, description) VALUES (%s, %s)"""
            cursor.execute(sql_pics, (img.pic, img.text))
            pics_id = cursor.lastrowid

            sql_qa = """INSERT INTO first_question (pics_id, question, answer)
                  VALUES (%s, %s, %s)"""
            img_parameters = [(pics_id, key, img.questions[key]) for key in img.questions.keys()]
            cursor.executemany(sql_qa, img_parameters)
            db.commit()
        except:
           # Откат в случае ошибки
            db.rollback()
            print('FAILED with {}'.format(img))
    cursor.close()


insert_from_file_to_db(load_files('images_1.csv'))
#insert_from_file_to_db(load_files('mysql_insert.csv'))
db.close()
