from PIL import Image
import numpy as np
img = Image.open("more.png")
# img.show()

print(img.size)#获取图片大小（width， height）
print(img.mode)#获取图片模式{'1':1, 'L':8, 'P':8(带颜色表), 'RGB':24, 'RGBA':32,}
print(img.info)
sequ = img.getdata()
sequ0 = list(sequ)
print(sequ0)#获取图片像素值

if img.mode == 'P':
    print(img.palette.palette)#打印颜色表
    lut = img.resize((99, 99))
    lut.putdata(range(256))
    lut = lut.convert("RGB")#将图片转换为RGB图像
    print(list(lut.getdata()))#打印图像RGB像素值
    # pix = lut.load()
    # print(pix[1, 0])
    # lut.show()
    # lut now contains a sequence of (r, g, b) tuples

pix = img.load()
print(pix[img.size[0]/2, img.size[1]/2])#某个点（x, y）的像素值

# r,g,b, a = img.split()
# print(r.mode)
# print(r.size)
# print(img.size)

# with open('png_text.txt', 'w+') as f:
#     for i in range(0,img.size[0]):
#         for j in range(0,img.size[1]):
#             # value = img_array[i, j]
#             # print("",value)
#             (b, g, r, a) = pix[i, j]
#             if (b, g, r, a) != (0, 0, 0, 0):
#                 print("(%d, %d)-[%02x, %02x, %02x, %02x]" %(j, i, r, g, b, a))
#                 f.write("%d, %d, %02x, %02x, %02x,\n" %(j, i, a, (((r&0x001f)*2**11)|((g&0x3f)*2**5)|(b&0x1f))//256, (((r&0x001f)*2**11)|((g&0x3f)*2**5)|(b&0x1f))%256))


# img_array = np.array(img)#把图像转成数组格式img = np.asarray(image)
# shape = img_array.shape
# print(img_array.shape)
# with open('png_text.txt', 'w+') as f:
#     for i in range(0,shape[0]):
#         for j in range(0,shape[1]):
#             # value = img_array[i, j]
#             # print("",value)
#             (b, g, r, a) = img_array[i, j]
#             if (b, g, r, a) != (0, 0, 0, 0):
#                 print("(%d, %d)-[%02x, %02x, %02x, %02x]" %(j, i, r, g, b, a))
#                 f.write("%d, %d, %02x, %02x, %02x,\n" %(j, i, a, (((r&0x001f)*2**11)|((g&0x3f)*2**5)|(b&0x1f))//256, (((r&0x001f)*2**11)|((g&0x3f)*2**5)|(b&0x1f))%256))
        # if value[0] != 0:
        #     print("", value)
        
# height = shape[0]
# width = shape[1]
# dst = np.zeros((height,width,3))
# for h in range(0,height):
#     for w in range (0,width):
#         (b,g,r) = img_array[h,w]
#         if (b,g,r)==(255,255,255):#白色
#             img_array[h,w] = (0,255,255)#蓝色
#         if (b, g, r) == (85, 85, 85):  # 深灰
#             img_array[h, w] = (0, 128, 0)  # 绿色
#         if (b, g, r) == (170, 170, 170):  # 灰色
#             img_array[h, w] = (255, 255, 0)  # 黄色
#         if (b, g, r) == (0, 0, 0):  # 黑色
#             img_array[h, w] = (255, 0, 0)  # 红色
#         dst[h,w] = img_array[h,w]
# img2 = Image.fromarray(np.uint8(dst))
# img2.show(img2)
# img2.save("3.png","png")

