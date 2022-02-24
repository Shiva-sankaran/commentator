import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='annotation_sql',
                             cursorclass=pymysql.cursors.DictCursor)

cur = connection.cursor()
result = cur.execute("SELECT * FROM UserTagList")
print(result)
cur.close()
