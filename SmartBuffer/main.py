import customtkinter as ctk
import pyperclip as ppp
import json
import threading as thd
import sqlite3
import time
from datetime import datetime
from PIL import Image
import DDL_DML

class ClipBoardDB:
    def __init__(self):
        self.conn = sqlite3.connect("clip_history.db", check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute(DDL_DML.create_history)
        self.conn.commit()

    def add_clip(self, text):
        self.cur.execute(DDL_DML.insert_history, text)
        self.conn.commit()

    def toggle_pin(self, text):
        self.cur.execute(DDL_DML.update_history, text)
        self.conn.commit()
    def get_all_history(self):
        self.cur.execute(DDL_DML.get_history)
        return self.cur.fetchall()
class Recipes:
    pass