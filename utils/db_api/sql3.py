import sqlite3


class Database:
    def __init__(self, path_to_db='main.db'):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None,
                fetch_one=False, fetch_all=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetch_one:
            data = cursor.fetchone()
        if fetch_all:
            data = cursor.fetchall()
        connection.close()
        return data

    # ================= USERS =================

    def create_users_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            fullname TEXT,
            phone TEXT,
            district TEXT,
            mfy TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.execute(sql, commit=True)

    def add_user(self, telegram_id, fullname, phone, district, mfy):
        sql = """
        INSERT INTO users (telegram_id, fullname, phone, district, mfy)
        VALUES (?, ?, ?, ?, ?)
        """
        self.execute(sql, (telegram_id, fullname, phone, district, mfy), commit=True)

    def select_user(self, id):
        sql = "SELECT * FROM users WHERE id=?"
        return self.execute(sql, (id,), fetch_one=True)
    
    def select_users(self, telegram_id):
        sql = "SELECT * FROM users WHERE telegram_id=?"
        return self.execute(sql, (telegram_id,), fetch_one=True)
    

    # ================= DISTRICTS =================

    def create_districts_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS districts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """
        self.execute(sql, commit=True)

    def add_district(self, name):
        sql = "INSERT INTO districts (name) VALUES (?)"
        self.execute(sql, (name,), commit=True)

    def select_districts(self):
        sql = "SELECT * FROM districts"
        return self.execute(sql, fetch_all=True)

    # ================= MFY =================

    def create_mfys_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS mfys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            district_id INTEGER,
            name TEXT
        )
        """
        self.execute(sql, commit=True)

    def add_mfy(self, district_id, name):
        sql = "INSERT INTO mfys (district_id, name) VALUES (?, ?)"
        self.execute(sql, (district_id, name), commit=True)

    def select_mfys(self, district_id):
        sql = "SELECT * FROM mfys WHERE district_id=?"
        return self.execute(sql, (district_id,), fetch_all=True)

    # ================= MEDICINES =================

    def create_medicines_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            crop TEXT,
            description TEXT,
            price INTEGER,
            is_active INTEGER DEFAULT 1
        )
        """
        self.execute(sql, commit=True)

    def add_medicine(self, name, crop, description, price):
        sql = """
        INSERT INTO medicines (name, crop, description, price)
        VALUES (?, ?, ?, ?)
        """
        self.execute(sql, (name, crop, description, price), commit=True)

    def select_medicines(self, crop):
        sql = "SELECT * FROM medicines WHERE crop=? AND is_active=1"
        return self.execute(sql, (crop,), fetch_all=True)
    

    def delete_dori(self, id):
        sql = """DELETE FROM medicines WHERE id=?"""
        return self.execute(sql, (id, ), commit=True)
    
    def select_all_dori(self, page: int = 1, page_size: int = 10):
        offset = (page - 1) * page_size
        sql = """
            SELECT  * FROM medicines
            LIMIT ? OFFSET ?
        """
        return self.execute(sql, (page_size, offset), fetch_all=True)
    
    def select_all_dori_user(self,crop, page: int = 1, page_size: int = 10):
        offset = (page - 1) * page_size
        sql = """
            SELECT  * FROM medicines
            where crop = ?
            LIMIT ? OFFSET ?
        """
        return self.execute(sql, (crop, page_size, offset), fetch_all=True)

    def dori_count(self):
        sql = """SELECT count(*) FROM medicines"""
        return self.execute(sql, fetch_one=True)
    
    def dori_count_user(self, crop):
        sql = """SELECT count(*) FROM medicines where crop = ?"""
        return self.execute(sql, (crop, ),fetch_one=True)
    
    def user_dori(self, id):
        sql = """SELECT * FROM medicines where id = ?"""
        return self.execute(sql, (id,), fetch_one=True)
    
    def update_medicine(
            self,
            medicine_id: int,
            name: str = None,
            crop: str = None,
            description: str = None,
            price: int = None,
            is_active: int = None   
    ):
        fields = []
        values = []

        if name is not None:
            fields.append("name = ?")
            values.append(name)

        if crop is not None:
            fields.append("crop = ?")
            values.append(crop)

        if description is not None:
            fields.append("description = ?")
            values.append(description)

        if price is not None:
            fields.append("price = ?")
            values.append(price)

        if is_active is not None:
            fields.append("is_active = ?")
            values.append(is_active)

        # Hech narsa o'zgarmasa
        if not fields:
            return False

        sql = f"""
            UPDATE medicines
            SET {', '.join(fields)}
            WHERE id = ?
        """

        values.append(medicine_id)
        self.execute(sql, tuple(values), commit=True)
        return True


    # ================= QUESTIONS =================

    def create_questions_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            question TEXT,
            answer TEXT,
            status TEXT DEFAULT 'new',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.execute(sql, commit=True)

    def add_question(self, telegram_id, question):
        sql = "INSERT INTO questions (telegram_id, question) VALUES (?, ?)"
        self.execute(sql, (telegram_id, question), commit=True)

    def select_new_questions(self):
        sql = "SELECT * FROM questions WHERE status='new'"
        return self.execute(sql, fetch_all=True)

    def answer_question(self, q_id, answer):
        sql = """
        UPDATE questions SET answer=?, status='answered'
        WHERE id=?
        """
        self.execute(sql, (answer, q_id), commit=True)

    # ================= INIT =================

    # ================= ORDERS =================

    def create_orders_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            medicine_id INTEGER,
            status TEXT DEFAULT 'yangi',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (medicine_id) REFERENCES medicines (id)
        )
        """
        self.execute(sql, commit=True)

    def orders_count(self, user_id):
        sql = """SELECT count(*) FROM orders where user_id = ?"""
        return self.execute(sql, (user_id, ),fetch_one=True)
    
    def orders_all_count(self):
        sql = """SELECT count(*) FROM orders"""
        return self.execute(sql, fetch_one=True)
    
    def select_order_user(self, user_id, page: int = 1, page_size: int = 10):
        offset = (page - 1) * page_size
        sql = """
            SELECT *
            FROM orders
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ? OFFSET ?
        """
        return self.execute(sql, (user_id, page_size, offset), fetch_all=True)


    
    def select_all_order(self, page: int = 1, page_size: int = 10):
        offset = (page - 1) * page_size
        sql = """
            SELECT  * FROM orders
            LIMIT ? OFFSET ?
        """
        return self.execute(sql, (page_size, offset), fetch_all=True)
    
    def add_order(self, user_id, medicine_id):
        sql = """
        INSERT INTO orders (user_id, medicine_id) VALUES (?, ?)
        """
        self.execute(sql, (user_id, medicine_id), commit=True)

    def delete_order(self, id):
        sql = """
        DELETE FROM orders WHERE id = ?
        """
        return self.execute(sql, (id, ), commit=True)

    def update_order_status(self, order_id, status):
        sql = "UPDATE orders SET status=? WHERE id=?"
        self.execute(sql, (status, order_id), commit=True)
    
    # ================= ADMINS =================
    def create_admins_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            fullname TEXT,
            role TEXT DEFAULT 'admin'
        )
        """
        self.execute(sql, commit=True)

    # Yangi admin qo'shish
    def add_admin(self, telegram_id: int, fullname: str, role: str = 'admin'):
        sql = "INSERT INTO admins (telegram_id, fullname, role) VALUES (?, ?, ?)"
        self.execute(sql, (telegram_id, fullname, role), commit=True)

    # Adminni o'chirish
    def delete_admin(self, telegram_id: int):
        sql = "DELETE FROM admins WHERE telegram_id=?"
        self.execute(sql, (telegram_id,), commit=True)

    # Bitta adminni olish
    def select_admin(self, telegram_id: int):
        sql = "SELECT * FROM admins WHERE telegram_id=?"
        return self.execute(sql, (telegram_id,), fetch_one=True)
    
    def select_all_admin(self, page: int = 1, page_size: int = 10):
        offset = (page - 1) * page_size
        sql = """
            SELECT  * FROM admins
            LIMIT ? OFFSET ?
        """
        return self.execute(sql, (page_size, offset), fetch_all=True)
    def admin_count(self):
        sql = """SELECT count(*) FROM admins"""
        return self.execute(sql, fetch_one=True)

    # Barcha adminlarni olish
    def select_all_admins(self):
        sql = "SELECT * FROM admins"
        return self.execute(sql, fetch_all=True)

    # Adminmi yoki yo'qmi tekshirish
    def is_admin(self, telegram_id: int):
        return self.select_admin(telegram_id) is not None



    def create_aloqa_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS aloqa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matn TEXT
        )
        """
        self.execute(sql, commit=True)

    # Yangi admin qo'shish
    def add_aloqa(self, matn):
        sql = "INSERT INTO aloqa (matn) VALUES (?)"
        self.execute(sql, (matn,), commit=True)


    # Adminni o'chirish
    def delete_aloqa(self):
        sql = "DELETE FROM aloqa"
        self.execute(sql, commit=True)

    def update_aloqa_status(self, id, matn):
        sql = "UPDATE aloqa SET matn=? WHERE id=?"
        self.execute(sql, (matn, id), commit=True)

    def select_all_aloqa(self):
        sql = "SELECT * FROM aloqa"
        return self.execute(sql, fetch_one=True)

    def create_user_messages_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS user_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message_id INTEGER,
            message_type TEXT,
            status TEXT DEFAULT 'new',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.execute(sql, commit=True)


    def add_user_message(self, user_id, message_id, message_type):
        sql = """
        INSERT INTO user_messages (user_id, message_id, message_type)
        VALUES (?, ?, ?)
        """
        self.execute(sql, (user_id, message_id, message_type), commit=True)


    def close_user_chat(self, user_id):
        sql = """
        UPDATE user_messages
        SET status = 'seen'
        WHERE user_id = ? AND status = 'new'
        """
        self.execute(sql, (user_id,), commit=True)



    def get_users_with_new_messages(self):
        sql = """
        SELECT DISTINCT u.telegram_id, u.fullname, m.status
        FROM user_messages m
        JOIN users u ON u.telegram_id = m.user_id
        ORDER BY m.created_at DESC
        """
        return self.execute(sql, fetch_all=True)

    def select_user_messages(self):
        sql = """
        select * from user_messages
        """

    def get_user_messages(self, user_id):
        sql = """
        SELECT message_id
        FROM user_messages
        WHERE user_id = ?
        ORDER BY id
        """
        return self.execute(sql, (user_id,), fetch_all=True)


    def mark_messages_seen(self, user_id):
        sql = """
        UPDATE user_messages
        SET status = 'seen'
        WHERE user_id = ? AND status = 'new'
        """
        self.execute(sql, (user_id,), commit=True)


    def add_admin_message(self, user_id, message_id, message_type):
        sql = """
        INSERT INTO user_messages (user_id, message_id, message_type, status)
        VALUES (?, ?, ?, 'seen')
        """
        self.execute(sql, (user_id, message_id, message_type), commit=True)

    def create_all_tables(self):
        self.create_user_messages_table()
        self.create_aloqa_table()
        self.create_admins_table()
        self.create_users_table()
        self.create_districts_table()
        self.create_mfys_table()
        self.create_medicines_table()
        self.create_questions_table()
        self.create_orders_table()

