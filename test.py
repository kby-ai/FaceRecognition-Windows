import sys
sys.path.append('.')

from PIL import Image
import numpy as np

from facesdk import getMachineCode
from facesdk import setActivation
from facesdk import faceDetection
from facesdk import initSDK
from facesdk import templateExtraction
from facesdk import similarityCalculation
from facebox import FaceBox

verifyThreshold = 0.7

maxFaceCount = 1

licensePath = "license.txt"
license = ""

machineCode = getMachineCode()
print("machineCode: ", machineCode.decode('utf-8'))

try:
    with open(licensePath, 'r') as file:
        license = file.read()
except IOError as exc:
    print("failed to open license.txt: ", exc.errno)
print("license: ", license)


ret = setActivation(license.encode('utf-8'))
print("activation: ", ret)

ret = initSDK("D:/Temp/kby_face/github/FaceRecognition-Windows/data".encode('utf-8'))
print("init: ", ret)

def compare_face(file1, file2):
    result = "None"
    similarity = -1
    face1 = None
    face2 = None

    try:
        image1 = Image.open(file1)
    except:
        result = "Failed to open file1"
        response = jsonify({"compare_result": result, "compare_similarity": similarity, "face1": face1, "face2": face2})

        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response


    try:
        image2 = Image.open(file2)
    except:
        result = "Failed to open file2"
        response = jsonify({"compare_result": result, "compare_similarity": similarity, "face1": face1, "face2": face2})

        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

    image_np1 = np.asarray(image1)
    image_np2 = np.asarray(image2)

    faceBoxes1 = (FaceBox * maxFaceCount)()
    faceCount1 = faceDetection(image_np1, image_np1.shape[1], image_np1.shape[0], faceBoxes1, maxFaceCount)

    faceBoxes2 = (FaceBox * maxFaceCount)()
    faceCount2 = faceDetection(image_np2, image_np2.shape[1], image_np2.shape[0], faceBoxes2, maxFaceCount)

    if faceCount1 == 1 and faceCount2 == 1:
        templateExtraction(image_np1, image_np1.shape[1], image_np1.shape[0], faceBoxes1[0])
        templateExtraction(image_np2, image_np2.shape[1], image_np2.shape[0], faceBoxes2[0])
        similarity = similarityCalculation(faceBoxes1[0].templates, faceBoxes2[0].templates)
        if similarity > verifyThreshold:
            result = "Same person"
        else:
            result = "Different person"
    elif faceCount1 == 0:
        result = "No face1"
    elif faceCount2 == 0:
        result = "No face2"

    if faceCount1 == 1:
        # landmark_68 = []
        # for j in range(68):
        #     landmark_68.append({"x": faceBoxes1[0].landmark_68[j * 2], "y": faceBoxes1[0].landmark_68[j * 2 + 1]})

        face1 = {"x1": faceBoxes1[0].x1, "y1": faceBoxes1[0].y1, "x2": faceBoxes1[0].x2, "y2": faceBoxes1[0].y2, 
                      "yaw": faceBoxes1[0].yaw, "roll": faceBoxes1[0].roll, "pitch": faceBoxes1[0].pitch,
                      "face_quality": faceBoxes1[0].face_quality, "face_luminance": faceBoxes1[0].face_luminance, "eye_dist": faceBoxes1[0].eye_dist,
                      "left_eye_closed": faceBoxes1[0].left_eye_closed, "right_eye_closed": faceBoxes1[0].right_eye_closed,
                      "face_occlusion": faceBoxes1[0].face_occlusion, "mouth_opened": faceBoxes1[0].mouth_opened}
                    #   "landmark_68": landmark_68}

    if faceCount2 == 1:
        # landmark_68 = []
        # for j in range(68):
        #     landmark_68.append({"x": faceBoxes2[0].landmark_68[j * 2], "y": faceBoxes2[0].landmark_68[j * 2 + 1]})

        face2 = {"x1": faceBoxes2[0].x1, "y1": faceBoxes2[0].y1, "x2": faceBoxes2[0].x2, "y2": faceBoxes2[0].y2, 
                      "yaw": faceBoxes2[0].yaw, "roll": faceBoxes2[0].roll, "pitch": faceBoxes2[0].pitch,
                      "face_quality": faceBoxes2[0].face_quality, "face_luminance": faceBoxes2[0].face_luminance, "eye_dist": faceBoxes2[0].eye_dist,
                      "left_eye_closed": faceBoxes2[0].left_eye_closed, "right_eye_closed": faceBoxes2[0].right_eye_closed,
                      "face_occlusion": faceBoxes2[0].face_occlusion, "mouth_opened": faceBoxes2[0].mouth_opened}
                    #   "landmark_68": landmark_68}

    response = {"compare_result": result, "compare_similarity": similarity, "face1": face1, "face2": face2}
    return response

if __name__ == "__main__":
    ret = compare_face('D:/Temp/kby_face/github/FaceRecognition-Windows/face_examples/1.jpg', 'D:/Temp/kby_face/github/FaceRecognition-Windows/face_examples/2.jpg')
    print(ret)