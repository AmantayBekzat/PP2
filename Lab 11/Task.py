import psycopg2
import csv
import os

# PostgreSQL-ға қосылу үшін параметрлерді орнату
conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="1111",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# contacts кестесінің бар екенін тексеру функциясы
def check_table_exists():
    try:
        cur.execute("SELECT to_regclass('public.contacts');")
        result = cur.fetchone()[0]
        if result is None:
            print("Кесте жоқ, оны жасау керек.")
            cur.execute("""
                CREATE TABLE contacts (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    phone VARCHAR(20)
                );
            """)
            conn.commit()
            print("Кесте жасалды.")
        else:
            print("Кесте бар.")
    except Exception as e:
        print(f"Қате орын алды: {e}")
        conn.rollback()

# Үлгі (pattern) бойынша барлық жазбаларды қайтаратын функция
def search_contacts(pattern):
    try:
        cur.execute("SELECT * FROM contacts WHERE name ILIKE %s OR phone ILIKE %s", (f'%{pattern}%', f'%{pattern}%'))
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("Мәлімет табылмады.")
    except Exception as e:
        print(f"Қате орын алды: {e}")

# Аты мен телефоны бойынша жаңа пайдаланушыны енгізуге арналған процедура, егер пайдаланушы бар болса, телефонын жаңартады
def insert_or_update_user(user_name, user_phone):
    try:
        cur.execute("SELECT id FROM contacts WHERE name = %s", (user_name,))
        result = cur.fetchone()
        if result:
            cur.execute("UPDATE contacts SET phone = %s WHERE name = %s", (user_phone, user_name))
            print(f"User {user_name} phone updated.")
        else:
            cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (user_name, user_phone))
            print(f"User {user_name} added.")
        conn.commit()
    except Exception as e:
        print(f"Қате орын алды: {e}")
        conn.rollback()

# Аты мен телефоны тізімі бойынша көптеген жаңа пайдаланушыларды енгізу процедурасы, телефон дұрыстығын тексереді
def insert_multiple_users(users_list):
    try:
        for user_data in users_list:
            name_part, phone_part = user_data.split(',')
            if not phone_part.isdigit() or len(phone_part) < 10:
                print(f"Қате дерек: {user_data} дұрыс емес телефон.")
            else:
                insert_or_update_user(name_part, phone_part)
        print("Барлық деректер қосылды.")
    except Exception as e:
        print(f"Қате орын алды: {e}")

# Пагинацияға арналған функция (limit және offset)
def get_contacts_paginated(limit_size, offset_size):
    try:
        cur.execute("SELECT * FROM contacts LIMIT %s OFFSET %s", (limit_size, offset_size))
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("Мәлімет табылмады.")
    except Exception as e:
        print(f"Қате орын алды: {e}")

# Пайдаланушы аты немесе телефоны бойынша контактіні өшіру процедурасы
def delete_contact_by_user_or_phone(user_name=None, user_phone=None):
    try:
        if user_name:
            cur.execute("DELETE FROM contacts WHERE name = %s", (user_name,))
        elif user_phone:
            cur.execute("DELETE FROM contacts WHERE phone = %s", (user_phone,))
        conn.commit()
        print("❌ Контакт өшірілді.")
    except Exception as e:
        print(f"Қате орын алды: {e}")
        conn.rollback()

# CSV файлынан деректерді енгізу функциясы
def insert_from_csv(file_path):
    try:
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 2:
                    insert_or_update_user(row[0], row[1])
                else:
                    print(f"Ескерту: {row} жолы дұрыс емес форматта.")
            print("📥 CSV деректері қосылды.")
    except Exception as e:
        print(f"Қате орын алды: {e}")

# Қолмен енгізу арқылы деректерді енгізу функциясы
def insert_from_input():
    try:
        name = input("Атыңызды енгізіңіз: ")
        phone = input("Телефон нөмірі: ")
        insert_or_update_user(name, phone)
    except Exception as e:
        print(f"Қате орын алды: {e}")

# Контактіні жаңарту функциясы (ID бойынша)
def update_contact():
    try:
        contact_id = input("Қай ID жаңартасың? ")
        new_name = input("Жаңа аты: ")
        new_phone = input("Жаңа телефон: ")
        cur.execute("UPDATE contacts SET name = %s, phone = %s WHERE id = %s", (new_name, new_phone, contact_id))
        conn.commit()
        print("♻️ Контакт жаңартылды.")
    except Exception as e:
        print(f"Қате орын алды: {e}")
        conn.rollback()

# Фильтрмен сұраныс жасау функциясы
def query_with_filter():
    try:
        keyword = input("Аты не номер бойынша ізде: ")
        cur.execute("SELECT * FROM contacts WHERE name ILIKE %s OR phone ILIKE %s", (f'%{keyword}%', f'%{keyword}%'))
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("Мәлімет табылмады.")
    except Exception as e:
        print(f"Қате орын алды: {e}")

# Негізгі меню
def menu():
    run = True
    check_table_exists()

    while run:
        print("\n📱 PHONEBOOK MENU:")
        print("1 - Search by pattern")
        print("2 - Insert from CSV")
        print("3 - Insert from input")
        print("4 - Update contact")
        print("5 - Query with filter")
        print("6 - Delete contact")
        print("7 - Exit")
        print("8 - Paginate contacts")

        choice = input("Таңдаңыз (1–8): ")

        if choice == '1':
            pattern = input("Іздеу үшін үлгі енгізіңіз: ")
            search_contacts(pattern)
        elif choice == '2':
            file_path = input("CSV файлдың толық жолын енгізіңіз: ")
            insert_from_csv(file_path)
        elif choice == '3':
            insert_from_input()
        elif choice == '4':
            update_contact()
        elif choice == '5':
            query_with_filter()
        elif choice == '6':
            user_name_or_phone = input("Өшірілетін контактінің аты немесе телефон нөмірін енгізіңіз: ")
            delete_contact_by_user_or_phone(user_name=user_name_or_phone)
        elif choice == '7':
            run = False
        elif choice == '8':
            limit_size = int(input("Көрсету санын енгізіңіз: "))
            offset_size = int(input("Басталатын орын енгізіңіз: "))
            get_contacts_paginated(limit_size, offset_size)
        else:
            print("❗ Қате таңдау.")

menu()

cur.close()
conn.close()
