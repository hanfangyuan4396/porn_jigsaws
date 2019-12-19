from PIL import Image

size = [840, 865, 1200]
num = 5

for i in range(0,3):

 
    box = size[i] / num
    img0 = Image.open(f'{i + 6}.jpg')

    img1 = img0.crop((0,0,size[i],size[i]))

    for j in range(num ** 2):
        x = j % num
        y = j // num
        crop_img = img1.crop((x * box, y * box, x * box + box, y * box + box))
        crop_img.save(f'{i + 6}\\{j}.png')


