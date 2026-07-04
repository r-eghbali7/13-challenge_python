import random
import time

# شماره موبایل -> (کد، زمان ایجاد)
otp_storage = {}

OTP_EXPIRE_TIME = 120  # 2 دقیقه


def send_otp(phone):
    """
    تولید و نمایش کد OTP
    """

    code = random.randint(100000, 999999)

    otp_storage[phone] = (
        str(code),
        time.time()
    )

    print("\n==============================")
    print("      SMS SIMULATOR")
    print("==============================")
    print(f"Phone : {phone}")
    print(f"OTP   : {code}")
    print("==============================\n")

    return code


def verify_otp(phone, entered_code):
    """
    بررسی صحت OTP
    """

    if phone not in otp_storage:
        return False

    real_code, create_time = otp_storage[phone]

    # منقضی شدن کد
    if time.time() - create_time > OTP_EXPIRE_TIME:
        del otp_storage[phone]
        print("OTP Expired.")
        return False

    if entered_code == real_code:
        del otp_storage[phone]
        return True

    return False


def resend_otp(phone):
    """
    ارسال مجدد OTP
    """
    send_otp(phone)


# تست فایل
if __name__ == "__main__":

    phone = input("Phone Number : ")

    send_otp(phone)

    code = input("Enter OTP : ")

    if verify_otp(phone, code):
        print("OTP Verified Successfully.")
    else:
        print("Invalid OTP.")