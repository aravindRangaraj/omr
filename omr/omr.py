import cv2
import numpy as np
import utlis

def omr(imgpath,field,answer):

    pathImage = imgpath
    heightImg = 700
    widthImg = 700
    questions=5
    choices=5
    ans= answer


    img = cv2.imread(pathImage)
    img = cv2.resize(img, (widthImg, heightImg)) # RESIZE IMAGE
    imgFinal = img.copy()
    imgBlank = np.zeros((heightImg,widthImg, 3), np.uint8) # CREATE A BLANK IMAGE FOR TESTING DEBUGGING IF REQUIRED
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # CONVERT IMAGE TO GRAY SCALE
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1) # ADD GAUSSIAN BLUR
    imgCanny = cv2.Canny(imgBlur,10,70) # APPLY CANNY


    ## FIND ALL COUNTOURS
    imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # FIND ALL CONTOURS
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10) # DRAW ALL DETECTED CONTOURS
    rectCon = utlis.rectContour(contours) # FILTER FOR RECTANGLE CONTOURS
    biggestPoints= utlis.getCornerPoints(rectCon[0]) # GET CORNER POINTS OF THE BIGGEST RECTANGLE
    # gradePoints = utlis.getCornerPoints(rectCon[1]) # GET CORNER POINTS OF THE SECOND BIGGEST RECTANGLE



    if biggestPoints.size != 0:

        # BIGGEST RECTANGLE WARPING
        biggestPoints=utlis.reorder(biggestPoints) # REORDER FOR WARPING
        cv2.drawContours(imgBigContour, biggestPoints, -1, (0, 255, 0), 20) # DRAW THE BIGGEST CONTOUR
        pts1 = np.float32(biggestPoints) # PREPARE POINTS FOR WARP
        pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
        matrix = cv2.getPerspectiveTransform(pts1, pts2) # GET TRANSFORMATION MATRIX
        imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg)) # APPLY WARP PERSPECTIVE


        # APPLY THRESHOLD
        imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY) # CONVERT TO GRAYSCALE
        imgThresh = cv2.threshold(imgWarpGray, 170, 255,cv2.THRESH_BINARY_INV )[1] # APPLY THRESHOLD AND INVERSE

        boxes = utlis.splitBoxes(imgThresh) # GET INDIVIDUAL BOXES
        # cv2.imshow("Split Test ", boxes[3])
        countR=0
        countC=0
        myPixelVal = np.zeros((questions,choices)) # TO STORE THE NON ZERO VALUES OF EACH BOX
        nonPixelVal = np.zeros((1,1))
        nonPixelVal[0][0] = 5
        for image in boxes:
            #cv2.imshow(str(countR)+str(countC),image)
            totalPixels = cv2.countNonZero(image)
            myPixelVal[countR][countC]= totalPixels
            countC += 1
            if (countC==choices):countC=0;countR +=1

        # FIND THE USER ANSWERS AND PUT THEM IN A LIST
        myIndex=[]
        for x in range (0,questions):
            arr = myPixelVal[x]
            print("arrrr",arr)
            max1 = np.amax(arr)
            myIndexVal = np.where(arr == np.amax(arr))
            print(max1)
            temp =np.delete(arr,myIndexVal)
            print("arrrr", temp)
            max2= np.amax(temp)
            myIndexVal1 = np.where(arr == max2)
            if(max1.tolist()/1000 - max2.tolist()/1000  < 2):
                print("masbcjasfjhds",max1,max2)
                myIndexVal = nonPixelVal
            myIndex.append(myIndexVal[0][0])
        print("USER ANSWERS",myIndex)

            # COMPARE THE VALUES TO FIND THE CORRECT ANSWERS


        if field == 1:
            grading=[]
            for x in range(0,questions):
                if ans[x] == myIndex[x]:
                    grading.append(1)
                else:grading.append(0)
            #print("GRADING",grading)
            score = (sum(grading)/questions)*50 # FINAL GRADE
            print("SCORE",score)
            
        
            imageArray = ([img,imgGray,imgBlur, imgCanny],
                          [imgContours,imgBigContour,imgThresh,imgBlank])
            lables = [["Original","Gray","Blur","Edges"],
                      ["Contours","Biggest Contour","Threshold"," "]]

            stackedImage = utlis.stackImages(imageArray,0.5,lables)
            cv2.imshow('Result', stackedImage)
            # cv2.imwrite('r.jpg', stackedImage)
            cv2.waitKey()
            return(str(score))

    return(myIndex)