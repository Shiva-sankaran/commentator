import csv
import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='annotation_sql',
                             cursorclass=pymysql.cursors.DictCursor)

cur = connection.cursor()
result = cur.execute("SELECT * FROM UserTagList WHERE uid = 1")
data = cur.fetchall()
print(data)
cur.close()


index = 0
with open('./csv/data.csv', 'w', encoding='utf-8', newline="") as f:
    writer = csv.writer(f)

    writer.writerow(['utid', 'uid', 'sid', 'stag'])
    for i in data:
        data_row = i
        row = [data_row['utid'], data_row['uid'],
               data_row['sid'], data_row['stag']]
        print(row)
        writer.writerow(row)
