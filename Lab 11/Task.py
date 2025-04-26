import psycopg2
import csv
import os

conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="1111",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

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

def insert_from_csv(file_path):
    try:
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 2:
                    cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (row[0], row[1]))
                else:
                    print(f"Ескерту: {row} жолы дұрыс емес форматта.")
            conn.commit()
            print("📥 CSV деректері қосылды.")
    except Exception as e:
        print(f"Қате орын алды: {e}")
        conn.rollback()

def insert_from_input():
    try:
        name = input("Атыңызды енгізіңіз: ")
        phone = input("Телефон нөмірі: ")
        cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, phone))
        conn.commit()
        print("✅ Жаңа контакт қосылды.")
    except Exception as e:
        print(f"Қате орын алды: {e}")
        conn.rollback()

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

def delete_contact():
    try:
        contact_id = input("Қай ID өшіргің келеді? ")
        cur.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
        conn.commit()
        print("❌ Контакт өшірілді.")
    except Exception as e:
        print(f"Қате орын алды: {e}")
        conn.rollback()

def menu():
    run = True
    check_table_exists()

    while run:
        print("\n📱 PHONEBOOK MENU:")
        print("1 - insert csv")
        print("2 - from input")
        print("3 - update contact")
        print("4 - query with filter")
        print("5 - delete contact")
        print("6 - break")

        choice = input("Таңдаңыз (1–6): ")

        if choice == '1':
            file_path = input("CSV файлдың толық жолын енгізіңіз: ")
            insert_from_csv(file_path)
        elif choice == '2':
            insert_from_input()
        elif choice == '3':
            update_contact()
        elif choice == '4':
            query_with_filter()
        elif choice == '5':
            delete_contact()
        elif choice == '6':
            run = False
        else:
            print("❗ Қате таңдау.")

menu()
cur.close()
conn.close()
