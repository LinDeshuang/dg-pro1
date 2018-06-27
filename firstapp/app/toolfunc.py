import hashlib
import io
import os
import random
import string

from PIL import Image, ImageDraw, ImageFont
from django.conf import settings

# md5摘要密码
from firstapp.settings import BASE_DIR


def md5HashPwd(text):
    md5 = hashlib.md5()
    md5.update((text + settings.SECRET_KEY).encode('utf-8'))
    return md5.hexdigest()


# 创建验证码
def createVcode(vlength=4):
    # 随机生成验证码
    vcode = ''.join(random.sample(string.ascii_letters + string.digits, vlength))
    # 定义背景
    background = (255, 255, 255)
    # 画布
    img = Image.new('RGB', (170,50), background )
    # 获取画笔
    draw = ImageDraw.Draw(img)
    # 画上验证码
    for i in range(len(vcode)):
        # 设置字体
        path = os.path.join(BASE_DIR,'static','my-fonts','ttfs',str(random.randint(1,6))+'.ttf')
        font = ImageFont.truetype(path, size=40)
        draw.text((15*random.random()+30*i,8*random.random()), vcode[i], fill=getRandomColor(), font=font)
    # 画上干扰点
    for i in range(300):
        position = (random.randint(0,170),random.randint(0,50))
        draw.point(position, fill=getRandomColor())

    # 保存图片
    buff = io.BytesIO()
    img.save(buff, 'png')

    return (vcode, buff.getvalue())

# 随机生成颜色
def getRandomColor():
    red = random.randint(0,255)
    green = random.randint(0,255)
    blue = random.randint(0,255)
    return (red,green,blue)