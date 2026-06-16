# bale -> parsaeghbali 
# address bot -> @python_learnbot

from database import get_connection


def add_task():
    title = input("عنوان تسک: ")
    description = input("توضیحات: ")
    priority = input("اولویت (High/Medium/Low): ")
    due_date = input("تاریخ سررسید (YYYY-MM-DD): ")

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO tasks(title,description,priority,due_date)
    VALUES(%s,%s,%s,%s)
    """

    cursor.execute(
        query,
        (title, description, priority, due_date)
    )

    conn.commit()

    print("✅ تسک اضافه شد")

    cursor.close()
    conn.close()


def show_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")

    tasks = cursor.fetchall()

    print("\n------ TASKS ------")

    for task in tasks:
        print(
            f"""
ID: {task[0]}
Title: {task[1]}
Description: {task[2]}
Priority: {task[3]}
Status: {task[4]}
Due Date: {task[5]}
------------------------
"""
        )

    cursor.close()
    conn.close()


def search_task():
    keyword = input("عنوان برای جستجو: ")

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT * FROM tasks
    WHERE title LIKE %s
    """

    cursor.execute(query, (f"%{keyword}%",))

    tasks = cursor.fetchall()

    for task in tasks:
        print(task)

    cursor.close()
    conn.close()


def complete_task():
    task_id = input("شناسه تسک: ")

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE tasks
    SET status='completed'
    WHERE id=%s
    """

    cursor.execute(query, (task_id,))
    conn.commit()

    print("✅ تسک تکمیل شد")

    cursor.close()
    conn.close()


def edit_task():
    task_id = input("ID تسک: ")

    title = input("عنوان جدید: ")
    description = input("توضیحات جدید: ")
    priority = input("اولویت جدید: ")
    due_date = input("تاریخ جدید: ")

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE tasks
    SET title=%s,
        description=%s,
        priority=%s,
        due_date=%s
    WHERE id=%s
    """

    cursor.execute(
        query,
        (
            title,
            description,
            priority,
            due_date,
            task_id
        )
    )

    conn.commit()

    print("✏️ تسک ویرایش شد")

    cursor.close()
    conn.close()


def delete_task():
    task_id = input("ID تسک: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id=%s",
        (task_id,)
    )

    conn.commit()

    print("🗑️ حذف شد")

    cursor.close()
    conn.close()


def show_completed_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM tasks
    WHERE status='completed'
    """)

    tasks = cursor.fetchall()

    for task in tasks:
        print(task)

    cursor.close()
    conn.close()
