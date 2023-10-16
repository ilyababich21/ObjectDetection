import time

import cv2
from ultralytics import YOLO


class Detector():
    modelObject = YOLO('D:\\PythonProjects\\YOLO888\\runs\\detect\\train43\\weights\\last.pt')
    modelPose = YOLO('yolov8n-pose.pt')
    skeleton = [[16, 14],
                [14, 12],
                [17, 15],
                [15, 13],
                [12, 13],
                [6, 12],
                [7, 13],
                [6, 7],
                [6, 8],
                [7, 9],
                [8, 10],
                [9, 11],
                [1, 2],
                [1, 3],
                [2, 4],
                [3, 5]]

    shape = (640, 640)

    bgrPose = (255, 255, 0)
    bgrWeapon = (0, 255, 0)

    pTime = 0
    weapon_conf = 0.30
    weapon_iou = 0.5
    pose_conf = 0.5
    weapon_thickness = 2
    pose_thickness = 2

    def weapon_detect(self, frame):

        # face recognition
        # resultObject = self.modelObject.predict(frame, conf=self.weapon_conf, iou=self.weapon_iou, imgsz=640)[0]
        resultObject = self.modelObject.predict(frame,verbose=False)[0]
        # resultObject = self.modelObject.predict(frame, conf=self.weapon_conf, iou=self.weapon_iou)[0]
        resultPOse = self.modelPose(frame, conf=self.pose_conf,verbose=False)[0]

        class_name = self.findClassNames(resultObject)
        class_name2 = self.findClassNames(resultPOse)

        cTime = time.time()
        fps = 1 / (cTime - self.pTime)
        self.pTime = cTime

        self.draw_boxes(frame, resultObject, self.bgrWeapon, class_name, (0, 0, 255))
        self.draw_boxes(frame, resultPOse, self.bgrPose, class_name2, (255, 255, 255))
        self.draw_skeleton(frame, resultPOse)
        cv2.putText(frame, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        return frame

    def findClassNames(self, result):
        classes_ = result.boxes.cls.tolist()
        classes = list(map(lambda x: int(x), classes_))
        cls_dict = result.names
        class_name = list(map(lambda x: cls_dict[x], classes))
        return class_name

    def draw_boxes(self, frame, result, rectangle_bgr, class_name, text_bgr):
        for num, ich in enumerate(result.boxes.xyxy):
            ich = ich.tolist()
            x1, x2, x3, x4 = ich[0], ich[1], ich[2], ich[3]
            cv2.rectangle(frame, (int(x1), int(x2)), (int(x3), int(x4)), rectangle_bgr, int(self.pose_thickness))
            cv2.putText(frame, class_name[num], (int(x1) - 3, int(x2)), cv2.FONT_HERSHEY_PLAIN, 3,
                        text_bgr, 3)

    def draw_skeleton(self, frame, resultPose):
        for result in resultPose:
            # print(result.keypoints.xy.tolist()," piska")
            ndim = result.keypoints.shape[-1]
            for id, keypoint in enumerate(result.keypoints.xy.tolist()):
                for idx in range(len(keypoint)):
                    pass
                    # print(int(keypoint[idx][0]),int(keypoint[idx][1]))
                    # cv2.putText(frame, str(idx), (int(keypoint[idx][0]), int(keypoint[idx][1])),
                    #                                 cv2.FONT_HERSHEY_COMPLEX,0.4,(255,255,255),1)

                for i, sk in enumerate(self.skeleton):
                    # pointX = int(keypoint[sk[0]-1][0])

                    pos1 = (int(keypoint[sk[0] - 1][0]),
                            int(keypoint[sk[0] - 1][1]))
                    pos2 = (int(keypoint[sk[1] - 1][0]),
                            int(keypoint[sk[1] - 1][1]))
                    if ndim == 3:
                        # print(result.keypoints.conf.tolist())
                        conf1 = result.keypoints.conf[id][(sk[0] - 1)]
                        conf2 = result.keypoints.conf[id][(sk[1] - 1)]
                        if conf1 < 0.5 or conf2 < 0.5:
                            continue
                    if pos1[0] % self.shape[1] == 0 or pos1[1] % self.shape[0] == 0 or pos1[0] < 0 or pos1[1] < 0:
                        continue
                    if pos2[0] % self.shape[1] == 0 or pos2[1] % self.shape[0] == 0 or pos2[0] < 0 or pos2[1] < 0:
                        continue
                    cv2.line(frame, pos1, pos2, (255, 255, 255), thickness=2, lineType=cv2.LINE_AA)
