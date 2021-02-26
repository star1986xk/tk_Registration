import tkinter as tk
from tkinter import messagebox
import sqlite3
import re


class DB():

    def create_conn(self):
        # 创建连接
        self.conn = sqlite3.connect('db.db')
        self.conn.isolation_level = None
        # 创建游标
        self.cursor = self.conn.cursor()

    def create_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS user (
    id       INTEGER       PRIMARY KEY AUTOINCREMENT,
    username VARCHAR (255) UNIQUE,
    password VARCHAR (255) 
); '''
        self.cursor.execute(sql)
        self.conn.commit()
        return True

    def select_username(self, username):
        sql = 'select username from user where username=?;'
        self.cursor.execute(sql, (username,))
        if self.cursor.fetchall():
            return True

    def select_all(self):
        sql = 'select * from user;'
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def insert_user(self, username, password):
        sql = 'insert into user values(null,?,?);'
        self.cursor.execute(sql, (username, password))
        self.conn.commit()
        return True

    def delete_user(self):
        sql = 'delete from user'
        sql1 = 'DELETE FROM sqlite_sequence;'
        self.conn.execute(sql)
        self.conn.execute(sql1)
        self.conn.execute("VACUUM")
        self.conn.commit()
        return True

    def close(self):
        # 关闭游标
        self.cursor.close()
        # 关闭连接
        self.conn.close()


class Application(tk.Tk):

    def __init__(self):
        '''初始化'''
        super().__init__()  # 有点相当于tk.Tk()
        # self.state("zoomed") #最大化
        self.wm_title("Registration Page")
        self.geometry('650x450')
        self.resizable(width=False, height=False)  # 禁止拉伸
        self.createWidgets()
        self.init_table()

    def init_table(self):
        db = DB()
        db.create_conn()
        db.create_table()
        db.close()

    def createWidgets(self):
        '''界面'''
        tk.Label(self, text="Enter your username:").place(x=50, y=30)
        self.username = tk.Entry(self)
        self.username.place(x=200, y=30, width=200)

        tk.Label(self, text="Enter your password:").place(x=50, y=70)
        self.password = tk.Entry(self)
        self.password.place(x=200, y=70, width=200)

        tk.Button(master=self, text='Save', command=self.save).place(x=200, y=110, width=80, height=25)
        tk.Button(master=self, text='Clear', command=self.clear).place(x=300, y=110, width=80, height=25)

        tk.Button(master=self, text='Display', command=self.display).place(x=100, y=240, width=80, height=25)
        tk.Label(self, text="Display all usernames and associated passwords in the database").place(x=200, y=180)
        self.text_display = tk.Text(self)
        self.text_display.place(x=200, y=210, width=350, height=220)

        self.del_btn = tk.Button(master=self, text='Delete', command=self.delete)
        # self.del_btn.place(x=100, y=280, width=80, height=25)

    def check(self, username, password):
        if not username or not password: return
        if not len(password) > 7 or not re.search('[A-Za-z]', password) or not re.search('[0-9]', password):
            tk.messagebox.showwarning('warning',
                                      'Password is too short (minimum is 8 characters), needs at least 1 number and at least 1 letter')
            return
        db = DB()
        db.create_conn()
        result = db.select_username(username)
        db.close()
        if result:
            tk.messagebox.showwarning('warning', 'Username already exists')
            return
        return True

    def save(self):
        username = self.username.get().strip()
        password = self.password.get().strip()
        if self.check(username, password):
            db = DB()
            db.create_conn()
            result = db.insert_user(username, password)
            db.close()
            if result:
                tk.messagebox.showinfo('info', 'registered successfully')

    def clear(self):
        self.username.delete(0, "end")
        self.password.delete(0, "end")
        self.text_display.delete(0.0, "end")

    def display(self):
        db = DB()
        db.create_conn()
        result = db.select_all()
        db.close()
        self.text_display.delete(0.0, "end")
        self.text_display.insert('insert', '\n'.join([' '.join([str(li) for li in row]) for row in result]))

    def delete(self):
        db = DB()
        db.create_conn()
        result = db.delete_user()
        db.close()
        if result:
            self.text_display.delete(0.0, "end")
            tk.messagebox.showinfo('info', 'clear user data')


if __name__ == '__main__':
    # 实例化Application
    app = Application()
    # 主消息循环:
    app.mainloop()
