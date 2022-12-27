#!/usr/bin/env python
from importlib import import_module
import datetime
import os
from flask import Flask, render_template, Response
import cv2
import torch
from utils.torch_utils import *
from utils.general import check_img_size, non_max_suppression, scale_coords
from models.experimental import attempt_load
from models.yolo import Model
from utils.datasets import LoadStreams, LoadImages
import random
from utils.plots import plot_one_box
import sys
from kakao.kakao_friend import Kakao_friend
# from kakao.send_msg_friend import Kakao_friend_message


app = Flask(__name__)

@app.route('/')
def index():
    # global inf
    """Video streaming home page."""
    # print(inf.counts)
    return render_template('index.html') #, variable=inf.counts)


def stream():
    now = datetime.datetime.now()
    kakao_msg = Kakao_friend()
    # kakao_msg = Kakao_friend_message()
    # WEIGHT = '/root/Public/pretrained/1213_model.pt'
    WEIGHT = 'models/1213_model.pt'
    model = attempt_load(WEIGHT, map_location=select_device('0')).half()

    imgsz = 640
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check img_size
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    # Run inference
    model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    
    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]
    old_img_w = old_img_h = imgsz
    old_img_b = 1

    """Video streaming generator function."""
    # cap = cv2.VideoCapture('rtsp://astrodom:hdci12@192.168.170.73:554/stream1')
    dataset = LoadStreams('rtsp://astrodom:hdci12@192.168.170.73:554/stream1', img_size=imgsz, stride=stride)

    while True:
        # ret, frame = cap.read()
        for path, img, im0s, vid_cap in dataset:
            img = torch.from_numpy(img).to(device)
            img = img.half() if True else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Warmup
            if device.type != 'cpu' and (old_img_b != img.shape[0] or old_img_h != img.shape[2] or old_img_w != img.shape[3]):
                old_img_b = img.shape[0]
                old_img_h = img.shape[2]
                old_img_w = img.shape[3]
                for i in range(3):
                    model(img, augment=True)[0]

            with torch.no_grad():   # Calculating gradients would cause a GPU memory leak
                pred = model(img, augment=True)[0]
 
            # Apply NMS
            pred = non_max_suppression(pred, 0.50, 0.40)

            # Process detections
            for i, det in enumerate(pred):  # detections per image
                # batch_size >= 1
                p, s, im0, frame = path[i], '%g: ' % i, im0s[i].copy(), dataset.count

                p = Path(p)  # to Path
                # gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                    tmp = 0
                    # Print results
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string
                        tmp += 1

                    # Write results
                    for *xyxy, conf, cls in reversed(det):
                    #     if save_txt:  # Write to file
                    #         xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                    #         line = (cls, *xywh, conf) if opt.save_conf else (cls, *xywh)  # label format
                    #         with open(txt_path + '.txt', 'a') as f:
                    #             f.write(('%g ' * len(line)).rstrip() % line + '\n')

                        # Add bbox to image
                        label = f'{names[int(cls)]} {conf:.2f}'
                        plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=1)
                        # inf(label)
                        
                        # 20221216 추가
                        str1 = s[3:].split(',')[0] + '\n' + s[3:].split(',')[1][1:]

                        y0, dy = 50, 50
                        for  i , line in enumerate (str1.split ('\n')): 
                            y = y0 + i*dy
                            cv2.putText(im0 , line, (im0.shape[1] - 250 , y), cv2.FONT_HERSHEY_SIMPLEX , 1.5, (0, 255, 0), thickness = 3)
                            kakao_msg.send_to_mutli_friend(text="test messsage From SSAI Alarm, 2022.12.14, HDCLabs 7F " + now.strftime("%Y-%M-%D:%h-%m-%S"))
                            

                image_bytes = cv2.imencode('.jpg', im0)[1].tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')
                
                
@app.route('/video')
def video():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(stream(), content_type='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__' :
    app.run(host='0.0.0.0', port=10016, threaded=True, debug=True)