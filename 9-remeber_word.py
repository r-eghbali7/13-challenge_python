# bale -> @parsaeghbali
# address bot -> @python_learnbot


import sqlite3
import random
from datetime import datetime, timedelta

DB_NAME = "vocabulary.db"

# فواصل مرور
REVIEW_STEPS = [1, 3, 7, 14, 30]


# ======================
# DATABASE
# ======================


def create_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS words(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        english TEXT NOT NULL,
        persian TEXT NOT NULL,
        level INTEGER DEFAULT 0,
        next_review TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


# ======================
# ADD WORD
# ======================


def add_word():

    eng = input("English Word: ").strip()
    per = input("Persian Meaning: ").strip()

    today = datetime.now()

    next_review = (today + timedelta(days=REVIEW_STEPS[0])).strftime("%Y-%m-%d")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
    INSERT INTO words
    (english,persian,level,next_review,created_at)
    VALUES(?,?,?,?,?)
    """,
        (eng, per, 0, next_review, today.strftime("%Y-%m-%d")),
    )

    conn.commit()
    conn.close()

    print("✅ Word Saved Successfully")


# ======================
# SHOW WORDS
# ======================


def show_words():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id,
           english,
           persian,
           level,
           next_review,
           created_at
    FROM words
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    print("\n========== WORD LIST ==========\n")

    for row in rows:

        print(
            f"ID:{row[0]} | "
            f"{row[1]} = {row[2]} | "
            f"Level:{row[3]} | "
            f"Next Review:{row[4]} | "
            f"Created:{row[5]}"
        )

    print("\n===============================\n")


# ======================
# SEARCH
# ======================


def search_word():

    keyword = input("Search English Word: ")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT english,persian
    FROM words
    WHERE english LIKE ?
    """,
        ("%" + keyword + "%",),
    )

    rows = cursor.fetchall()

    conn.close()

    if rows:

        print()

        for eng, per in rows:
            print(f"{eng} = {per}")

        print()

    else:
        print("❌ No Result Found")


# ======================
# REVIEW TODAY
# ======================


def review_today():

    today = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT id,
           english,
           persian,
           level
    FROM words
    WHERE next_review <= ?
    """,
        (today,),
    )

    words = cursor.fetchall()

    if not words:
        print("🎉 No Words Need Review Today")
        conn.close()
        return

    print(f"\n📚 {len(words)} Word(s) Need Review\n")

    for word_id, eng, per, level in words:

        print(f"\nWord: {eng}")

        input("Press Enter To Show Meaning...")

        print("Meaning:", per)

        remembered = input("Did You Remember It? (y/n): ").lower()

        if remembered == "y":

            if level < len(REVIEW_STEPS) - 1:
                level += 1

            next_date = (datetime.now() + timedelta(days=REVIEW_STEPS[level])).strftime(
                "%Y-%m-%d"
            )

            cursor.execute(
                """
            UPDATE words
            SET level=?,
                next_review=?
            WHERE id=?
            """,
                (level, next_date, word_id),
            )

            print(f"✅ Next Review: {next_date}")

        else:

            level = 0

            next_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

            cursor.execute(
                """
            UPDATE words
            SET level=?,
                next_review=?
            WHERE id=?
            """,
                (level, next_date, word_id),
            )

            print("🔁 Reset To Level 0")

    conn.commit()
    conn.close()


# ======================
# RANDOM REVIEW
# ======================


def random_review():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT english,persian
    FROM words
    """)

    words = cursor.fetchall()

    conn.close()

    if not words:
        print("No Words Found")
        return

    random.shuffle(words)

    print("\n===== RANDOM REVIEW =====\n")

    for eng, per in words:

        input(f"Word: {eng} " "(Press Enter)")

        print(f"Meaning: {per}")

        print("-" * 30)

    print("\nReview Finished")


# ======================
# QUIZ
# ======================


def quiz():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT english,persian
    FROM words
    """)

    words = cursor.fetchall()

    conn.close()

    if len(words) == 0:
        print("No Words Available")
        return

    random.shuffle(words)

    score = 0

    questions = min(10, len(words))

    print(f"\n📝 Quiz ({questions} Questions)\n")

    for eng, per in words[:questions]:

        answer = input(f"Meaning Of '{eng}' ? ")

        if answer.strip() == per:

            print("✅ Correct")
            score += 1

        else:

            print(f"❌ Correct Answer: {per}")

    print(f"\n🏆 Final Score: " f"{score}/{questions}\n")


# ======================
# STATS
# ======================


def statistics():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM words")

    total_words = cursor.fetchone()[0]

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(
        """
    SELECT COUNT(*)
    FROM words
    WHERE next_review <= ?
    """,
        (today,),
    )

    review_count = cursor.fetchone()[0]

    conn.close()

    print("\n===== STATISTICS =====")

    print(f"Total Words: {total_words}")

    print(f"Need Review Today: " f"{review_count}")

    print("======================\n")


# ======================
# MENU
# ======================


def menu():

    create_db()

    while True:

        print("""
==================================
      ENGLISH VOCABULARY APP
==================================

1. Add New Word
2. Review Today's Words
3. Show All Words
4. Search Word
5. Random Review
6. Quiz
7. Statistics
0. Exit

==================================
""")

        choice = input("Select: ")

        if choice == "1":
            add_word()

        elif choice == "2":
            review_today()

        elif choice == "3":
            show_words()

        elif choice == "4":
            search_word()

        elif choice == "5":
            random_review()

        elif choice == "6":
            quiz()

        elif choice == "7":
            statistics()

        elif choice == "0":

            print("👋 Goodbye")
            break

        else:
            print("❌ Invalid Choice")


if __name__ == "__main__":
    menu()
