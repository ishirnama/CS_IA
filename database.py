import sqlite3
from tkinter import filedialog
from PIL import Image
import os

q_create_user_records = """
CREATE TABLE IF NOT EXISTS user_records (
   record_id INTEGER PRIMARY KEY AUTOINCREMENT,
   org_id INTEGER NOT NULL,
   purpose_of_visit TEXT NOT NULL,
   visit_date TEXT NOT NULL,
   username TEXT NOT NULL,
   FOREIGN KEY (username) 
      REFERENCES users (username)
);
"""

q_create_users_table = """
CREATE TABLE IF NOT EXISTS users (
   username TEXT PRIMARY KEY NOT NULL,
   password TEXT NOT NULL,
   email TEXT NOT NULL,
   forename TEXT NOT NULL,
   surname TEXT NOT NULL,
   age INTEGER,
   is_admin INTEGER,
   fingerprint BLOB,
   dob TEXT,
   pixelsum INTEGER,
   join_date TEXT,
   contour_count INTEGER,
   org_id TEXT,
   hide_metadata INTEGER,
   hide_userinformation INTEGER,
   time_of_failed_login INTEGER,
   failed_login_attempts INTEGER,
   color_theme TEXT,
   FOREIGN KEY (org_id) 
      REFERENCES user_records (org_id)
);
"""
# function that creates table
def create_table(query):
	# connect to db
	conn = sqlite3.connect("sql.db")
	# create a cursor to read and write data
	cur = conn.cursor()
	cur.execute( query )
	conn.commit()
	conn.close()


# function that creates table
def drop_table(table_name):
	# connect to db
	conn = sqlite3.connect("sql.db")
	# create a cursor to read and write data
	cur = conn.cursor()
	cur.execute( f"DROP TABLE {table_name};" )
	conn.commit()
	conn.close()

def insert_user_record( org_id, purpose_of_visit, visit_date, username):
	if (len(list_tables())==0):
		create_table(q_create_user_records)
		create_table(q_create_users_table)
	conn = sqlite3.connect("sql.db")
	cur = conn.cursor()
	cur.execute( "INSERT INTO user_records(org_id, purpose_of_visit, visit_date, username) VALUES(?, ?, ?, ? )", (org_id, purpose_of_visit, visit_date, username) )
	conn.commit()
	conn.close()

def insert_user(username, password, email, forename, surname, age=None, is_admin=0, 
        fingerprint=None, dob=None, pixelsum=0, join_date=None, contour_count=0,org_id=None, hide_metadata=0, hide_userinformation=0, time_of_failed_login=0,failed_login_attempts=0, color_theme="DARK"):
	if (len(list_tables())==0):
		create_table(q_create_user_records)
		create_table(q_create_users_table)
	conn = sqlite3.connect("sql.db")
	cur = conn.cursor()
	cur.execute( """INSERT INTO users(username, password, email, forename, surname, age, is_admin, 
        fingerprint, dob, pixelsum, join_date, contour_count,org_id,hide_metadata, hide_userinformation, time_of_failed_login, failed_login_attempts, color_theme) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
        (username, password, email, forename, surname, age, is_admin, 
        fingerprint, dob, pixelsum, join_date, contour_count,org_id,hide_metadata,hide_userinformation, time_of_failed_login, failed_login_attempts, color_theme) )
	conn.commit()
	conn.close()
	insert_user_record(username, "consultation","15/12/2024",username)
	insert_user_record(username, "consultation","26/04/202",username)

def update_user(user_record):
	if (len(list_tables())==0):
		create_table(q_create_user_records)
		create_table(q_create_users_table)
	conn = sqlite3.connect("sql.db")
	cur = conn.cursor()
	cur.execute( f"""UPDATE users SET password='{user_record[1]}', email='{user_record[2]}', forename='{user_record[3]}', surname='{user_record[4]}', age={user_record[5]}, is_admin={user_record[6]}, 
       dob='{user_record[8]}', pixelsum={user_record[9]}, join_date='{user_record[10]}', contour_count={user_record[11]},org_id='{user_record[12]}',hide_metadata={user_record[13]}, hide_userinformation={user_record[14]}, time_of_failed_login={user_record[15]},failed_login_attempts={user_record[16]}, color_theme='{user_record[17]}'
						WHERE username='{user_record[0]}'""" )
	conn.commit()
	conn.close()

# def view():
# 	conn = sqlite3.connect("sql.db")
# 	cur = conn.cursor()
# 	cur.execute( "SELECT * FROM store" )
# 	rows = cur.fetchall()
# 	conn.close()
# 	return rows

def find_user(username, password):
	if (len(list_tables())==0):
		create_table(q_create_user_records)
		create_table(q_create_users_table)
	conn = sqlite3.connect("sql.db")
	cur = conn.cursor()
	cur.execute( f"SELECT * FROM users WHERE username='{username}' AND password='{password}'" )
	rows = cur.fetchone()
	conn.close()
	return rows

def find_user_by_username(username):
	if (len(list_tables())==0):
		create_table(q_create_user_records)
		create_table(q_create_users_table)
	conn = sqlite3.connect("sql.db")
	cur = conn.cursor()
	cur.execute( f"SELECT * FROM users WHERE username='{username}'" )
	rows = cur.fetchone()
	conn.close()
	return rows

def update_hide_metadata_by_username(username, hide_metadata):
	if (len(list_tables())==0):
		create_table(q_create_user_records)
		create_table(q_create_users_table)
	conn = sqlite3.connect("sql.db")
	cur = conn.cursor()
	cur.execute( f"UPDATE users SET hide_metadata={hide_metadata} WHERE username='{username}'" )
	conn.commit()
	conn.close()

def update_hide_userinformation_by_username(username, hide_userinformation):
	if (len(list_tables())==0):
		create_table(q_create_user_records)
		create_table(q_create_users_table)
	conn = sqlite3.connect("sql.db")
	cur = conn.cursor()
	cur.execute( f"UPDATE users SET hide_userinformation={hide_userinformation} WHERE username='{username}'" )
	conn.commit()
	conn.close()

def update_theme_by_username(username, theme):
	if (len(list_tables())==0):
		create_table(q_create_user_records)
		create_table(q_create_users_table)
	conn = sqlite3.connect("sql.db")
	cur = conn.cursor()
	cur.execute( f"UPDATE users SET color_theme='{theme}' WHERE username='{username}'" )
	conn.commit()
	conn.close()

def get_all_users():
	if (len(list_tables())==0):
		create_table(q_create_user_records)
		create_table(q_create_users_table)
	conn = sqlite3.connect("sql.db")
	cur = conn.cursor()
	cur.execute( f"SELECT * FROM users" )
	rows = cur.fetchall()
	conn.close()
	return rows

def find_user_records(org_id):
	if (len(list_tables())==0):
		create_table(q_create_user_records)
		create_table(q_create_users_table)
	conn = sqlite3.connect("sql.db")
	cur = conn.cursor()
	cur.execute( f"SELECT * FROM user_records WHERE org_id='{org_id}'" )
	rows = cur.fetchall()
	conn.close()
	return rows

def find_user_records_by_username(username):
	if (len(list_tables())==0):
		create_table(q_create_user_records)
		create_table(q_create_users_table)
	conn = sqlite3.connect("sql.db")
	cur = conn.cursor()
	cur.execute( f"SELECT * FROM user_records WHERE username='{username}'" )
	rows = cur.fetchall()
	conn.close()
	return rows

def delete_user( username ):
	if (len(list_tables())==0):
		create_table(q_create_user_records)
		create_table(q_create_users_table)
	conn = sqlite3.connect("sql.db")
	cur = conn.cursor()
	cur.execute( "DELETE FROM users WHERE username=?", (username) )
	conn.commit()
	conn.close()

def update( quantity, price, item ):
	if (len(list_tables())==0):
		create_table(q_create_user_records)
		create_table(q_create_users_table)
	conn = sqlite3.connect("sql.db")
	cur = conn.cursor()
	cur.execute( "UPDATE store SET quantity=?, price=? WHERE item=?", (quantity, price, item) )
	conn.commit()
	conn.close()

def list_tables():
    conn = sqlite3.connect("sql.db")
    cur = conn.cursor()
    # res = cur.execute("SELECT name FROM sqlite_master WHERE name='login'")
    res = cur.execute("SELECT name FROM sqlite_master")
    rows = cur.fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
		
	# create_table("""
	# CREATE TABLE IF NOT EXISTS people (
	#    person_id INTEGER PRIMARY KEY,
	#    first_name TEXT,
	#    last_name TEXT,
	#    address_id INTEGER,
	#    FOREIGN KEY (address_id) 
	#       REFERENCES addresses (address_id)
	# );
	# """)

	# create_table(q_create_user_records)
	# create_table(q_create_users_table)

	# print(drop_table("user_records"))
	# print(drop_table("users"))
	print(list_tables())

	# file_path1 = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Finger Print", filetypes=[("BMP Files", "*.BMP"),("PNG Files", "*.png"),("JPG Files","*.jpg"),("JPEG Files","*.jpeg"),("GIF Files","*.gif")])
	# if not file_path1:
	#     print("file not selected")
	# else:
	#     with open(file_path1, 'rb') as file:
	#         image_data = file.read()
	#         insert_user( "a", "b", "a@a.com", "a", "aa",fingerprint=image_data)
	# insert_user_record(1, "consultation","26/04/2025","aa")
	# print(find_user("a","b"))
	# print(find_user_records(1))

	# print(find_user_by_username("a"))
	# print(find_user_records_by_username("a"))
	# user = find_user_by_username("a")
	# update_hide_metadata_by_username("abc",0)
	# update_hide_userinformation_by_username("abc",0)
	# user = find_user_by_username("abc")
	# print(user[13])
	# print(user[14])