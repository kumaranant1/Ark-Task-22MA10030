# Libraries to import
import cv2 as cv
import numpy as np
import math
from mpmath import mp


# count the occurence of every digits in a list 
def count_everything(LIST):
    k = {}
    for j in LIST:
        if j in k:
            k[j] += 1
        else:
            k[j] = 1
    return k


# Reading all images
pi_image = cv.imread('Images/pi_image.png')
art_picasso = cv.imread('Images/artwork_picasso.png')
Rick = cv.imread('Images/collage.png')



# making a list of pixel values of distorted pi image
distort_pi_list = list()
for i in range(50):
    for j in range(50):
        if pi_image[i][j][0] < 100:
            distort_pi_list.append((pi_image[i][j][0])//10)
        else:
            distort_pi_list.append((pi_image[i][j][0])//100)
# len(distort_pi_list) is equal to 2500


# Now we have to generate all digits of pi upto 2500 total digits
# using mpmath for that
mp.dps = 2500 # set no. of digits
actual_pi_list = list()
for letter in str(mp.pi).replace('.', ''):
    actual_pi_list.append(int(letter))
    
    

# Check occurrence of every digit in actual_pi and distort_pi
print("Actual pi - ", count_everything(actual_pi_list))
print("Distorted pi - ", count_everything(distort_pi_list))
print("Distorted Digits are - 9, 8, 3, 0")

# So, Distorted Digits are clearly visible in the output of above :-
# 3
# 9
# 8
# 0



# Calculating Filter :-
temp_list = np.array([3,9,8,0])
temp_list = np.multiply(temp_list, math.pi*10)
for i in range(len(temp_list)):
    temp_list[i] = math.floor(temp_list[i])
temp_list = [int(temp_list[i]) for i in range(len(temp_list))]
temp_list.sort(reverse = True)
temp_list = np.clip(temp_list, 0 , 255)
Filter = np.zeros((2,2,3) , dtype = 'uint8')
j = 0
for i in range(2):
        Filter[i][0] = temp_list[j]
        Filter[i][1] = temp_list[j+1]
        j+=2
print("Filter would be : \n ",Filter)



# Bitwise AND :-
art_picasso_for_AND = art_picasso.copy()
for i in range(0,100,2):
    for j in range(0,100,2):
        distorted_art_and4 = cv.bitwise_and(Filter , art_picasso_for_AND[i:i+2,j:j+2])
        art_picasso_for_AND[i:i+2,j:j+2] = distorted_art_and4
        
# Bitwise OR :-
art_picasso_for_OR = art_picasso.copy()
for i in range(0,100,2):
    for j in range(0,100,2):
        distorted_art_and4 = cv.bitwise_or(Filter , art_picasso_for_OR[i:i+2,j:j+2])
        art_picasso_for_OR[i:i+2,j:j+2] = distorted_art_and4
        
# Bitwise XOR :-
art_picasso_for_XOR = art_picasso.copy()
for i in range(0,100,2):
    for j in range(0,100,2):
        distorted_art_and4 = cv.bitwise_xor(Filter , art_picasso_for_XOR[i:i+2,j:j+2])
        art_picasso_for_XOR[i:i+2,j:j+2] = distorted_art_and4

        


# Now, creating Template Matching function !!
# The mathematical relation i have used is written in documentation is written in my documentation
def match_template(Template, Image):
    res = np.empty((8,8) , dtype = 'i')
    min_score = np.inf
    for x in range(0,800,100):
        for y in range(0,800,100):
            temp = Image[x:x+100, y:y+100] - Template
            temp = np.square(temp)
            score = np.sum(temp)
            res[x//100,y//100] = score
            if min_score > score:
                min_score = score
                x_y = (x, y)
    return x_y
TM_x_y_XOR = match_template(art_picasso_for_XOR, Rick)
Rick_copy = Rick.copy()
cv.rectangle(Rick_copy , TM_x_y_XOR , np.add(TM_x_y_XOR, (art_picasso_for_XOR.shape[0],art_picasso_for_XOR.shape[1])) , (0,255,0) , thickness = 4)
cv.putText(Rick_copy, text = str(TM_x_y_XOR) , org = (35, 90), color = (0,0,255) ,  fontFace = cv.FONT_HERSHEY_SIMPLEX , fontScale = 0.7 , thickness = 2)
cv.circle(Rick_copy, TM_x_y_XOR , 5 , (0,0,255) , thickness = cv.FILLED)



# Hence, Password to Zip Folder :-
Sum = TM_x_y_XOR[0] + TM_x_y_XOR[1]
Password = Sum*math.pi
Password = math.floor(Password)
print('Password - ', Password)



# Showing some images
cv.imshow('AND' , art_picasso_for_AND) # image produced after applying AND operator on famous potrait
cv.imshow('OR' , art_picasso_for_OR) # image produced after applying OR operator on famous potrait
cv.imshow('XOR' , art_picasso_for_XOR) # image produced after applying XOR operator on famous potrait
cv.imshow('Template Matcing Result' , Rick_copy) # result of template matching 
cv.waitKey(0)
cv.destroyAllWindows()