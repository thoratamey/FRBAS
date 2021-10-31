import os
import pandas as pd

#Path for images
image = os.path.join("Images")
data = []


for index, filename in enumerate(os.listdir(image), start=1):
    if filename.endswith(".png"):
        # Getting the real name of given sample picture
        new_name=filename.rsplit('.',1)[0]
        print(new_name)
        
        # Making the data of given information for saving into excel csv file
        data.append([new_name, filename, index])
       

# Making the csv file and saving the data in it
df = pd.DataFrame(data, columns=['Name', 'Image', 'Roll no.'])
df.to_csv("DATASET.csv" , index=False)
print("\nCSV FILE IS MADE AND DATSET IS USED FOR FACE RECOGINITION.")
