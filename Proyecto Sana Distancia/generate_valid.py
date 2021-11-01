import os

image_files = []
os.chdir(os.path.join("data", "images", "val"))
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".png"):
        image_files.append("data/images/val/" + filename)
os.chdir("../..")
with open("valid.txt", "w") as outfile:
    for image in image_files:
        outfile.write(image)
        outfile.write("\n")
    outfile.close()
os.chdir("..")
