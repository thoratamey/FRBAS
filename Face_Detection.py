import face_recognition
import cv2
import numpy as np
import os
import pandas as pd
import datetime
import yagmail


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)


# Initialize some variables
known_face_encodings = []
known_face_roll_no = []
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
attendance_record = set([])
roll_record = {}


# Reading the dataset
df = pd.read_csv("DATASET.csv")


print("Loading the picture and recognize the face in it.")
# And loading the picture and recognize the face of it.
for key, row in df.iterrows():
    roll_no = row['Roll no.']
    name = row['Name']
    image_path = row['Image']
    roll_record[roll_no] = name
    
    # Load a sample picture and learn how to recognize it.
    image = face_recognition.load_image_file("Images" + os.sep + image_path)
    
    # Create arrays of known face encodings and their names
    face_encoding = face_recognition.face_encodings(image)[0]
    
    # Create function for face_encoding and their roll_no 
    known_face_encodings.append(face_encoding)
    known_face_roll_no.append(roll_no)


# Making of attendence file
e=datetime.datetime.now()
d1=e.strftime("(%B %d , %Y) (%I-%M-%S %p)")
filename = "Attendance" + os.sep + "Attendance Record" + d1 + ".csv"
print("Attendance file is made!")


# Rows in attendence file
name_col = []
roll_no_col = []
time_col = []


print("Starting the Webcam for Face Recognition.\n")
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=1, fy=1)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # Find and manipulate facial features in webcam
        #face_landmarks_list=face_recoginition.face_landmarks(rgb_small_frame)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_roll_no[first_match_index]
            
            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                roll_no = known_face_roll_no[best_match_index]
                
                # Add this to the file
                name = roll_record[roll_no]
                if roll_no not in attendance_record:
                    attendance_record.add(roll_no)
                    # Display the data of recogined face
                    print(name , roll_no)
                    
                    name_col.append(name)
                    roll_no_col.append(roll_no)
                    time = datetime.datetime.now()
                    clock = time.strftime("%H:%M:%S")
                    time_col.append(clock)
                    
                    # Entrying data into attendance file
                    data = {'Name': name_col, 'Roll No.': roll_no_col, 'Time': time_col}
                    df=pd.DataFrame(data)
                    df.to_csv(filename ,index=False)


            face_names.append(name)


    process_this_frame = not process_this_frame
    
    

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        # top *= 2
        # right *= 2
        # bottom *= 2
        # left *= 2

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        font = cv2.FONT_HERSHEY_COMPLEX
        
        # Display the name of people which is recognised by help of webcam on top left of webcam window
        cv2.putText(frame, name, (10 , 40) ,font , 1.0 , (255, 255, 0)  , 1)

        # Display the roll no. of people which is recognised by help of webcam on top right of webcam window
        # And For displaying the number on webcam screen please convert number from int into str(string) 
       # if name != "Unknown" :
          #  cv2.putText(frame, str(roll_no), (600 , 40),font , 1.0 , (255, 255, 0) , 1)       


    # Display the resulting image
    cv2.imshow('WEBCAM', frame)

    
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) == ord('q'):
        break


# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()


# Attendance is register successful and file is made and saved
print("Attendance is registered Successful!\n")


#Sending email using yagmail library with help of smtp
yag=yagmail.SMTP('yash.patil1@vit.edu.in','Zxcos@6601' ,host='smtp.office365.com', port=587, smtp_starttls=True, smtp_ssl=False)

#Make your account enable for less secure apps
#Copy this for account enable :- https://www.google.com/settings/security/lesssecureapps

name=input('Enter the Email id for receiving the attendance sheet : ')
receiver=name.split(' , ')
d=datetime.datetime.now()
d2=d.strftime("%B %d , %Y (%I-%M-%S %p)")

yag.send(to = receiver, subject = 'Attendance Using Face Recognition via yagmail' , contents = 'Attendance Sheet with time - ' + d2 , attachments = filename)
print("\nGmail is Sended to all given mail id!")

