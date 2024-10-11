import sqlite3

connection = sqlite3.connect("student")
cursor  = connection.cursor()

# table1_info = '''
# CREATE TABLE class(id INTEGER PRIMARY KEY, name VARCHAR,fee float);
# '''
# table2_info = ''' 
# CREATE TABLE student(id INTEGER PRIMARY KEY, name VARCHAR,class_id INTEGER );
# '''

# cursor.execute(table1_info)
# cursor.execute(table2_info)

# cursor.execute("INSERT INTO class (id, name, fee) VALUES (1, 'Mathematics', 2000.50)")
# cursor.execute("INSERT INTO class (id, name, fee) VALUES (2, 'Science', 2500.00)")
# cursor.execute("INSERT INTO class (id, name, fee) VALUES (3, 'English', 1800.75)")
# cursor.execute("INSERT INTO class (id, name, fee) VALUES (4, 'History', 2200.25)")
# cursor.execute("INSERT INTO class (id, name, fee) VALUES (5, 'Computer Science', 3000.00)")
# cursor.execute("INSERT INTO student (id, name, class_id) VALUES (1, 'John Doe', 1)")
# cursor.execute("INSERT INTO student (id, name, class_id) VALUES (2, 'Jane Smith', 2)")
# cursor.execute("INSERT INTO student (id, name, class_id) VALUES (3, 'Robert Brown', 3)")
# cursor.execute("INSERT INTO student (id, name, class_id) VALUES (4, 'Emily Davis', 4)")
# cursor.execute("INSERT INTO student (id, name, class_id) VALUES (5, 'Michael Wilson', 5)")
# cursor.execute("INSERT INTO student (id, name, class_id) VALUES (6, 'Jessica Johnson', 1)")
# cursor.execute("INSERT INTO student (id, name, class_id) VALUES (11, 'David Lee', 2)")
# cursor.execute("INSERT INTO student (id, name, class_id) VALUES (8, 'Sophia Clark', 3)")
# cursor.execute("INSERT INTO student (id, name, class_id) VALUES (9, 'Daniel Martinez', 4)")
# cursor.execute("INSERT INTO student (id, name, class_id) VALUES (10, 'Olivia Lewis', 5)")


data = cursor.execute("SELECT name FROM student WHERE class_id =2")
for row in data:
    print(row)

connection.commit()


cursor.close()