from database import create_tables
from task_service import (
    add_task,
    show_tasks,
    complete_task,
    edit_task,
    delete_task,
    search_task,
    show_completed_tasks
)

create_tables()

while True:

    print("""
===== TODO APP =====

1. افزودن تسک
2. نمایش همه تسک ها
3. جستجو بر اساس عنوان
4. ویرایش تسک
5. تکمیل تسک
6. نمایش تسک های انجام شده
7. حذف تسک
8. خروج

====================
""")

    choice = input("انتخاب: ")

    if choice == "1":
        add_task()

    elif choice == "2":
        show_tasks()

    elif choice == "3":
        search_task()

    elif choice == "4":
        edit_task()

    elif choice == "5":
        complete_task()

    elif choice == "6":
        show_completed_tasks()

    elif choice == "7":
        delete_task()

    elif choice == "8":
        print("خروج...")
        break

    else:
        print("گزینه نامعتبر است")