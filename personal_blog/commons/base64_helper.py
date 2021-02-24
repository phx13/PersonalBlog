import base64
import os
import time


class Base64Helper(object):
    def __init__(self, path, choice, picture):
        self.path = path
        self.choice = choice
        self.picture = picture

    def run(self):
        try:
            self.is_picture()
        except Exception as e:
            return "is_picture fail"
        if self.choice == 1:
            result = self.picture_to_base64()
            return result
        else:
            try:
                return self.base64_to_picture()
            except Exception as e:
                return "base64_to_picture fail"

    def is_picture(self):
        suffix = self.path.split(".")[-1]
        is_qualified = ["png", "jpg"]
        if suffix not in is_qualified:
            raise Exception

    def picture_to_base64(self):
        with open(self.path, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            s = base64_data.decode()
            return 'data:image/jpeg;base64,%s' % s

    def base64_to_picture(self):
        if self.picture.startswith("data:image/"):
            is_live = os.path.exists('personal_blog/resources/images')
            if not is_live:
                os.mkdir('personal_blog/resources/images')
            img_data = base64.b64decode(self.picture.split(",")[-1].encode("utf-8"))
            create_time = time.strftime("%Y-%m-%d-%H-%M-%S")
            with open('personal_blog/resources/images/{0}.jpg'.format(create_time), 'wb') as f:
                f.write(img_data)
            return '/images/{0}.jpg'.format(create_time)
        else:
            raise Exception
