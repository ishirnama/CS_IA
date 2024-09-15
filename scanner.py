import cv2
import numpy as np
import os
from tkinter import filedialog
from PIL import Image, ImageFilter
import cv2
import numpy as np
import database
import io

class Scanner:
    def matcher(self, img1, img2):
        pil_image1 = img1.convert('RGB')
        open_cv_image1 = np.array(pil_image1)
        open_cv_image1 = open_cv_image1[:, :, ::-1].copy()

        pil_image2 = img2.convert('RGB')
        open_cv_image2 = np.array(pil_image2)
        open_cv_image2 = open_cv_image2[:, :, ::-1].copy()

        sift = cv2.xfeatures2d.SIFT_create()
        keypoints_1, descriptors_1 = sift.detectAndCompute(open_cv_image1, None)
        keypoints_2, descriptors_2 = sift.detectAndCompute(open_cv_image2, None)

        matches = cv2.FlannBasedMatcher(dict(algorithm=1, trees=10), 
                dict()).knnMatch(descriptors_1, descriptors_2, k=2)
        match_points = []
        
        for p, q in matches:
            if p.distance < 0.1*q.distance:
                match_points.append(p)
        keypoints = 0
        if len(keypoints_1) <= len(keypoints_2):
            keypoints = len(keypoints_1)            
        else:
            keypoints = len(keypoints_2)

        if (len(match_points) / keypoints)>0.95:
            print("% match: ", len(match_points) / keypoints * 100)
            result = cv2.drawMatches(open_cv_image1, keypoints_1, open_cv_image2, 
                                    keypoints_2, match_points, None) 
            result = cv2.resize(result, None, fx=2.5, fy=2.5)
            cv2.imshow("result", result)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def match_in_db(self, img1):
        pil_image1 = img1.convert('RGB')
        open_cv_image1 = np.array(pil_image1)
        open_cv_image1 = open_cv_image1[:, :, ::-1].copy()

        rows = database.get_all_users()
        for entry in rows:
            if entry[7]:
                img2 = Image.open(io.BytesIO(entry[7]))
                img2 = img2.resize((200, 200), Image.Resampling.LANCZOS)
                pil_image2 = img2.convert('RGB')
                open_cv_image2 = np.array(pil_image2)
                open_cv_image2 = open_cv_image2[:, :, ::-1].copy()

                sift = cv2.xfeatures2d.SIFT_create()
                keypoints_1, descriptors_1 = sift.detectAndCompute(open_cv_image1, None)
                keypoints_2, descriptors_2 = sift.detectAndCompute(open_cv_image2, None)

                matches = cv2.FlannBasedMatcher(dict(algorithm=1, trees=10), 
                        dict()).knnMatch(descriptors_1, descriptors_2, k=2)
                match_points = []
                
                for p, q in matches:
                    if p.distance < 0.1*q.distance:
                        match_points.append(p)
                keypoints = 0
                if len(keypoints_1) <= len(keypoints_2):
                    keypoints = len(keypoints_1)            
                else:
                    keypoints = len(keypoints_2)

                if (len(match_points) / keypoints)>0.95:
                    print("% match: ", len(match_points) / keypoints * 100)
                    return entry
        return None

    def get_pixel_sum(self, image_data):
        image = Image.open(io.BytesIO(image_data))
        image = image.filter(ImageFilter.GaussianBlur(radius = 2))
        # height, width, number of channels in image
        width, height = image.size
        print('Image Height       : ',height)
        print('Image Width        : ',width)

        rgbImage = image.convert('RGB')
        pixelSum = 0
        white = 254
        for i in range(0,height):
            for j in range(0,width):
                r, g, b = rgbImage.getpixel((j, i))
                if (r != white) and (g != white) and (b != white):
                    pixelSum = pixelSum +1
        print(f"Total number of black pixels = {pixelSum}")
        return pixelSum

    def blur_image(self, image_data):
        img2 = Image.open(io.BytesIO(image_data))
        img2 = img2.resize((200, 200), Image.Resampling.LANCZOS)
        pil_image2 = img2.convert('RGB')
        open_cv_image2 = np.array(pil_image2)
        cv_img = cv2.blur(open_cv_image2, (10, 10))
        return cv_img

    def get_contours(self, image_data):
        img2 = Image.open(io.BytesIO(image_data))
        img2 = img2.resize((200, 200), Image.Resampling.LANCZOS)
        pil_image2 = img2.convert('RGB')
        open_cv_image2 = np.array(pil_image2)
        open_cv_image2 = cv2.cvtColor(open_cv_image2, cv2.COLOR_BGR2GRAY)
        cnts = cv2.findContours(open_cv_image2, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        print(cnts)
        return cnts


if __name__ == "__main__":
    scanner = Scanner()
    # file_path1 = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Finger Print", filetypes=[("BMP Files", "*.BMP"),("PNG Files", "*.png"),("JPG Files","*.jpg"),("JPEG Files","*.jpeg"),("GIF Files","*.gif")])
    # if not file_path1:
    #     print("file not selected")
    # else:
    #     img1 = Image.open(file_path1)
    #     img1 = img1.resize((200, 200), Image.Resampling.LANCZOS)
    # scanner.match_in_db(img1)

    # file_path2 = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Finger Print", filetypes=[("BMP Files", "*.BMP"),("PNG Files", "*.png"),("JPG Files","*.jpg"),("JPEG Files","*.jpeg"),("GIF Files","*.gif")])
    # if not file_path2:
    #     print("file not selected")
    # else:
    #     img2 = Image.open(file_path2)
    #     img2 = img2.resize((200, 200), Image.Resampling.LANCZOS)
    # scanner.matcher(img1, img2)

    file_path1 = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Finger Print", filetypes=[("BMP Files", "*.BMP"),("PNG Files", "*.png"),("JPG Files","*.jpg"),("JPEG Files","*.jpeg"),("GIF Files","*.gif")])
    if not file_path1:
        print("file not selected")
    else:
        with open(file_path1, 'rb') as file:
            image_data = file.read()
            scanner = Scanner()
            print(scanner.get_pixel_sum(image_data))