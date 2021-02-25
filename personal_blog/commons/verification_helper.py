import base64
import random
import string
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
from io import BytesIO
from smtplib import SMTP_SSL, SMTPException

from PIL import Image, ImageFont, ImageDraw


class ImageVerificationHelper:
    def generate_code(self):
        return ''.join(random.sample(string.ascii_letters + string.digits, 4))

    def generate_color(self):
        red = random.randint(50, 200)
        green = random.randint(50, 200)
        blue = random.randint(50, 200)
        return red, green, blue

    def generate_line(self, draw, width, height):
        for i in range(2):
            x1 = random.randint(0, width / 2)
            y1 = random.randint(0, height / 2)
            x2 = random.randint(width / 2, width)
            y2 = random.randint(height / 2, height)
            draw.line(((x1, y1), (x2, y2)), 'black', 1)

    def generate_image_code(self):
        code = self.generate_code()
        width, height = 100, 50
        image = Image.new('RGB', (width, height), 'white')
        font = ImageFont.truetype('arial.ttf', 30)
        draw = ImageDraw.Draw(image)
        for i in range(4):
            draw.text((10 + random.randint(-10, 10) + 20 * i, 10 + random.randint(-10, 10)), code[i], self.generate_color(), font)
        self.generate_line(draw, width, height)
        return image, code

    def get_code(self):
        image, code = self.generate_image_code()
        buffer = BytesIO()
        image.save(buffer, 'jpeg')
        byte_code = buffer.getvalue()
        base64_code = base64.b64encode(byte_code)
        base64_str = base64_code.decode()
        return code, 'data:image/jpeg;base64,%s' % base64_str
        # return code, base64_code


class EmailVerificationHelper:
    def send_email(self, receiver, code):
        sender = '945871257@qq.com'
        content = f"<br/>Welcome to register for Phoenix Blog account, your email verification code is <span style='color:orange;'>{code}</span><br/>Please enter this verification code in the registration form to complete the registration"
        message = MIMEText(content, 'html', 'utf-8')
        message['Subject'] = Header('Email verification code for Phoenix Blog', 'utf-8')
        message['From'] = formataddr(('Phoenix', 'guoc9@cardiff.ac.uk'))
        message['To'] = receiver
        try:
            smtp = SMTP_SSL('smtp.qq.com', 465)
            smtp.login(sender, 'uppfznrxulnabbjc')
            smtp.sendmail(sender, receiver, str(message))
            smtp.quit()
        except SMTPException:
            return 'Fail: Send failed'

    def generate_code(self):
        return ''.join(random.sample(string.ascii_letters + string.digits, 6))


class EmailContactHelper:
    def send_email(self, sender, name, message_content):
        sender = '945871257@qq.com'
        content = '<b>' + name + '</b>' + '<hr>' + message_content
        message = MIMEText(content, 'html', 'utf-8')
        message['Subject'] = Header(name + ' contact you', 'utf-8')
        message['From'] = formataddr((name, sender))
        message['To'] = 'guoc9@cardiff.ac.uk'
        try:
            smtp = SMTP_SSL('smtp.qq.com', 465)
            smtp.login(sender, 'uppfznrxulnabbjc')
            smtp.sendmail(sender, 'guoc9@cardiff.ac.uk', str(message))
            smtp.quit()
        except SMTPException:
            return 'Fail: Send failed'


class ForgetPasswordHelper:
    def send_email(self, receiver, password):
        sender = '945871257@qq.com'
        content = f"<br/>Welcome to login Phoenix Blog, your password is reset as <span style='color:orange;'>{password}</span>"
        message = MIMEText(content, 'html', 'utf-8')
        message['Subject'] = Header('Password for Phoenix Blog', 'utf-8')
        message['From'] = formataddr(('Phoenix', 'guoc9@cardiff.ac.uk'))
        message['To'] = receiver
        try:
            smtp = SMTP_SSL('smtp.qq.com', 465)
            smtp.login(sender, 'uppfznrxulnabbjc')
            smtp.sendmail(sender, receiver, str(message))
            smtp.quit()
        except SMTPException:
            return 'Fail: Send failed'

    def generate_password(self):
        return ''.join(random.sample(string.ascii_letters + string.digits, 5))
