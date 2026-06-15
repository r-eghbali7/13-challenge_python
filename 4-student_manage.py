# bale -> @parsaeghbali
# address bot -> @python_learnbot

import sqlite3

# اتصال به دیتابیس
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# ساخت جدول
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    average REAL
)
""")

conn.commit()


# افزودن دانشجو
def add_student():
    name = input("نام دانشجو: ")
    age = int(input("سن: "))
    average =float(input("معدل: ")) 

    cursor.execute(
        "INSERT INTO students(name, age, average) VALUES (?, ?, ?)", (name, age, average)
    )

    conn.commit()
    print("✅ دانشجو ذخیره شد.\n")


# نمایش همه دانشجوها
def show_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if not students:
        print("هیچ دانشجویی ثبت نشده است.\n")
        return

    print("\n📋 لیست دانشجویان")
    print("-" * 40)

    for student in students:
        print(
            f"ID: {student[0]} | "
            f"نام: {student[1]} | "
            f"سن: {student[2]} | "
            f"معدل: {student[3]}"
        )

    print()


# جستجوی دانشجو
def search_student():
    name = input("نام دانشجو: ")

    cursor.execute(
        "SELECT * FROM students WHERE name LIKE ?",
        (f"%{name}%",)
    )

    students = cursor.fetchall()

    if students:
        for student in students:
            print(student)
    else:
        print("دانشجویی پیدا نشد.")

    print()


# حذف دانشجو
def delete_student():
    student_id = int(input("ID دانشجو: "))

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (student_id,)
    )

    conn.commit()

    if cursor.rowcount:
        print("🗑️ دانشجو حذف شد.")
    else:
        print("چنین دانشجویی وجود ندارد.")

    print()


# منوی برنامه
while True:
    print("""
======== مدیریت دانشجویان ========

1) افزودن دانشجو
2) نمایش دانشجویان
3) جستجو
4) حذف
5) خروج

==================================
""")

    choice = input("انتخاب شما: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        show_students()

    elif choice == "3":
        search_student()

    elif choice == "4":
        delete_student()

    elif choice == "5":
        print("خروج از برنامه...")
        break

    else:
        print("گزینه نامعتبر!\n")

conn.close()