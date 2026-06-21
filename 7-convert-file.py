# bale -> @parsaeghbali
# address bot -> @python_learnbot

from PIL import Image
from pdf2docx import Converter
from docx2pdf import convert
import os


def jpeg_to_webp(input_file, output_file=None, quality=80):
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + ".webp"

    img = Image.open(input_file)
    img.save(output_file, "WEBP", quality=quality)

    print(f"تبدیل شد: {output_file}")


def webp_to_jpeg(input_file, output_file=None):
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + ".jpg"

    img = Image.open(input_file)

    if img.mode in ("RGBA", "LA"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        img = background
    else:
        img = img.convert("RGB")

    img.save(output_file, "JPEG", quality=95)

    print(f"تبدیل شد: {output_file}")


def pdf_to_word(input_file, output_file=None):
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + ".docx"

    cv = Converter(input_file)
    cv.convert(output_file)
    cv.close()

    print(f"تبدیل شد: {output_file}")


def word_to_pdf(input_file, output_file=None):
    if output_file:
        convert(input_file, output_file)
    else:
        convert(input_file)

    print("تبدیل با موفقیت انجام شد.")


def menu():
    while True:
        print("\n===== File Converter =====")
        print("1. JPEG -> WEBP")
        print("2. WEBP -> JPEG")
        print("3. PDF -> WORD")
        print("4. WORD -> PDF")
        print("5. خروج")

        choice = input("انتخاب کنید: ")

        if choice == "1":
            file = input("مسیر فایل JPEG: ")
            jpeg_to_webp(file)

        elif choice == "2":
            file = input("مسیر فایل WEBP: ")
            webp_to_jpeg(file)

        elif choice == "3":
            file = input("مسیر فایل PDF: ")
            pdf_to_word(file)

        elif choice == "4":
            file = input("مسیر فایل DOCX: ")
            word_to_pdf(file)

        elif choice == "5":
            break

        else:
            print("گزینه نامعتبر است.")


if __name__ == "__main__":
    menu()