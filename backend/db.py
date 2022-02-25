import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='annotation_sql',
                             cursorclass=pymysql.cursors.DictCursor)

cur = connection.cursor()
result = cur.execute("ALTER TABLE UserTagList ADD COLUMN grammar CHAR(1)")
print(result)
cur.close()
