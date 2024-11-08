import os
import torchvision
from sklearn.model_selection import train_test_split

path = "downloads"
images_horse = []
images_panda = []

images_horse_cleaned = []
images_panda_cleaned = []

for file in os.listdir("downloads/horse"):
    img = torchvision.io.read_image(os.path.join("downloads/horse", file))
    images_horse.append(img)

for file in os.listdir("downloads/panda"):
    img = torchvision.io.read_image(os.path.join("downloads/panda", file))
    images_panda.append(img)

horse_count = 0
panda_count = 0
for img in images_horse:  
    if img.shape[1] >= 180  and img.shape[2] >= 180 and horse_count < 100:
        images_horse_cleaned.append(img)
        horse_count += 1

for img in images_panda:
    if img.shape[1] >= 180  and img.shape[2] >= 180 and panda_count < 100:
        images_panda_cleaned.append(img)
        panda_count += 1

tranform = torchvision.transforms.Resize((180, 180))
for i in range(len(images_horse_cleaned)):
    img = tranform(images_horse_cleaned[i])
    images_horse_cleaned[i] = img
for i in range(len(images_panda_cleaned)):
    img = tranform(images_panda_cleaned[i])
    images_panda_cleaned[i] = img

Horse_train, Horse_test = train_test_split(images_horse_cleaned, test_size=0.2)
Panda_train, Panda_test = train_test_split(images_panda_cleaned, test_size=0.2)

print(len(Horse_train), len(Horse_test), len(Panda_train), len(Panda_test))
print(Horse_test[12].shape)  #Sanity Check

if not os.path.exists("images"):
    os.mkdir("images")
save_path = "images"
for i in range(len(Horse_train)):
    if not os.path.exists(os.path.join(save_path, "Horse_train")):
        os.mkdir(os.path.join(save_path, "Horse_train"))
    torchvision.io.write_jpeg(Horse_train[i], os.path.join(save_path, "Horse_train", f"image_{i}.jpg"))
for i in range(len(Horse_test)):
    if not os.path.exists(os.path.join(save_path, "Horse_test")):
        os.mkdir(os.path.join(save_path, "Horse_test"))
    torchvision.io.write_jpeg(Horse_test[i], os.path.join(save_path, "Horse_test", f"image_{i}.jpg"))
for i in range(len(Panda_train)):
    if not os.path.exists(os.path.join(save_path, "Panda_train")):
        os.mkdir(os.path.join(save_path, "Panda_train"))
    torchvision.io.write_jpeg(Panda_train[i], os.path.join(save_path, "Panda_train", f"image_{i}.jpg"))
for i in range(len(Panda_test)):
    if not os.path.exists(os.path.join(save_path, "Panda_test")):
        os.mkdir(os.path.join(save_path, "Panda_test"))
    torchvision.io.write_jpeg(Panda_test[i], os.path.join(save_path, "Panda_test", f"image_{i}.jpg"))