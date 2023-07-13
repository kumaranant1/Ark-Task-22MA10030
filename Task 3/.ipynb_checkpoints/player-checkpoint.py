from utils import Player,WINDOW_WIDTH
import cv2 as cv
import numpy as np

player = Player()
    #Initializing a Player object with a random start position on a randomly generated Maze

def strategy():
    Map = player.getMap()
    original_shot = player.getSnapShot()
    res_original = cv.matchTemplate(Map, original_shot, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, original_loc = cv.minMaxLoc(res_original)
    
    
    ####################################################
    # for movement in Y - axis
    down = player.move_vertical(800)
    player.move_vertical(-down)
    up = player.move_vertical(-800)
    player.move_vertical(-up)
    # for movement in X - axis
    right = player.move_horizontal(800)
    player.move_horizontal(-right)
    left = player.move_horizontal(-800)
    player.move_horizontal(-left)
    
    # To refine similar cases
    r_right = player.move_horizontal(800)
    r_down = player.move_vertical(800)
    r_left = player.move_horizontal(-800)
    r_up = player.move_vertical(-800)
    player.move_vertical(-r_up)
    player.move_horizontal(-r_left)
    player.move_vertical(-r_down)
    player.move_horizontal(-r_right)
    rr_left = player.move_horizontal(-800)
    rr_down = player.move_vertical(800)
    rr_right = player.move_horizontal(800)
    rr_up = player.move_vertical(800)
    player.move_vertical(-rr_up)
    player.move_horizontal(-rr_right)
    player.move_vertical(-rr_down)
    player.move_horizontal(-rr_left)
    
    zz_right = player.move_horizontal(800)
    zz_up = player.move_vertical(-800)
    zz_right1 = player.move_horizontal(800)
    zz_down = player.move_vertical(800)
    zz_up1 = player.move_vertical(800)
    player.move_vertical(-zz_up1)
    player.move_vertical(-zz_down)
    player.move_horizontal(-zz_right1)
    player.move_vertical(-zz_up)
    player.move_horizontal(-zz_right)
    ####################################################
    def check_path_x(i,j,right, left):
        for k in range(j+left, j+right+1):
            if (int(Map[i][k]) == 0):
                return 0
        return 1
    def check_path_y(i,j,down,up):
        for k in range(i+up, i+down+1):
            if (int(Map[k][j]) == 0):
                return 0
        return 1
    def check_path_move_clockwise(i, j, r_right, r_down, r_left, r_up):
        for k in range(j, j+r_right+1):
            if (int(Map[i][k]) == 0):
                return 0
        for k in range(i, i+r_down+1):
            if (int(Map[k][j+r_right]) == 0):
                return 0
        for k in range(j+r_right+r_left, j+r_right+1):
            if (int(Map[i+r_down][k]) == 0):
                return 0
        for k in range(i+r_down+r_up, i+r_down+1):
            if (int(Map[k][j+r_right+r_left]) == 0):
                return 0
        return 1
    def check_path_move_anticlockwise(i, j , rr_left, rr_down, rr_right, rr_up):
        for k in range(j+rr_left, j+1):
            if(int(Map[i][k]) == 0):
                return 0
        for k in range(i, i+rr_down+1):
            if(int(Map[k][j+rr_left]) == 0):
                return 0
        for k in range(j+rr_left, j+rr_left+rr_right+1):
            if(int(Map[i+rr_down][k]) == 0):
                return 0
        for k in range(i+rr_down+rr_up, i+rr_down+1):
            if(int(Map[k][j+rr_left+rr_right]) == 0):
                return 0
        return 1
    def check_path__move_zig_zag_right(i, j , zz_right, zz_up , zz_right1, zz_down , zz_up1):
        for k in range(j,j+zz_right+1):
            if(int(Map[i][k]) == 0):
                return 0
        for k in range(i+zz_up, i+1):
            if(int(Map[k][j+zz_right]) == 0):
                return 0
        for k in range(j+zz_right, j+zz_right+zz_right1+1):
            if(int(Map[i+zz_up][k]) == 0):
                return 0
        for k in range(i+zz_up, i+zz_up+zz_down+1):
            if(int(Map[k][j+zz_right+zz_right1])== 0):
                return 0
        for k in range(i+zz_up+zz_down+zz_up1, i+zz_up+zz_down+1):
            if(int(Map[k][j+zz_right+zz_right1]) == 0):
                return 0
        return 1
    
    
    ####################################################
    
    # Here is the main alogoritm of my code how localization working !
    x = original_loc[0]
    y = original_loc[1]
    flag = 0
    sum_x = 0
    sum_y = 0
    for i in range(y , y+51):
        for j in range(x , x + 51):
            if((j+right+1 > 614) or (j+left-1 < 0) or ((i+down+1) > 614) or (i+up-1 < 0)):
                continue
            if((int(Map[i][j+right+1]) == 0) and (int(Map[i][j+left-1]) == 0) and (int(Map[i+down+1][j]) == 0) and (int(Map[i+up-1][j]) == 0)):
                if(check_path_x(i,j,right , left) == 1):
                    if(check_path_y(i,j,down , up) == 1):
                        if(check_path_move_clockwise(i, j, r_right, r_down, r_left, r_up) == 1):
                            if(check_path_move_anticlockwise(i, j , rr_left, rr_down, rr_right, rr_up) == 1):
                                if(check_path__move_zig_zag_right(i, j , zz_right, zz_up , zz_right1, zz_down , zz_up1)):
                                    Y = i
                                    X = j
                                    sum_x += X
                                    sum_y += Y
                                    flag += 1
    
    if(flag > 1):
        X = sum_x//flag
        Y = sum_y//flag
    
    #####################################################
    Map_copy = Map.copy()
    drone_loc = (X,Y)
    print("You can see a point inside a circle in {Map With Drone Revealed} image.")
    print("The Point which is inside the circle is exactly the position of drone in Map.") 
    if(flag == 1):
        print("Exact location of Drone in Map : " ,  drone_loc)
        print("The above position is Exact with no error !")
    else:
        print("Location of Drone in Map : ", drone_loc)
        print("Please note that : there may be possibility of some small error in above drone's position !")
    Map_Drone = cv.circle(Map_copy, drone_loc , radius=0, color=(0, 0, 255), thickness=4)
    Map_Drone = cv.circle(Map_copy, drone_loc , radius= 10, color = (0,0,0), thickness = 2)
    cv.imshow('Map With Drone Hidden', Map)
    cv.imshow('Map With Drone Revealed' , Map_Drone)
    cv.imshow('Original Shot', original_shot)
    cv.waitKey(0)
    cv.destroyAllWindows()
    #This function is to localize the position of the newly created player with respect to the map
    pass


if __name__ == "__main__":
    strategy()
    

























