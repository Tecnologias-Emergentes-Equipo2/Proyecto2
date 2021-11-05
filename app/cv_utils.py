import cv2
import pafy
import numpy as np

def get_video(url, start = -1, end = -1):
    video = pafy.new(url)
    best = video.getbest(preftype='mp4')
    vf = cv2.VideoCapture(best.url)
    return vf 

def load_trained_yolo():
    net = cv2.dnn.readNet('yolov4-obj.cfg', 'yolov4-obj_last_1.weights')
    classes = []

    with open('obj.names', 'r') as objs:
        classes = [line.strip() for line in objs.readlines()]

    layers_names = net.getLayerNames()
    output_layers = [layers_names[i-1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size = (len(classes), 3))
    return net, classes, colors, output_layers

def draw_labels(boxes, confs, colors, class_ids, classes, img):
    indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_SIMPLEX
    for i in range(len(boxes)):
        if i in indexes: 
            x,y,w,h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x,y), (x+w,y+h), color, 2)
            cv2.putText(img,label,(x,y-5), font, 0.25, color,1)

    width = int(img.shape[1] * 2.2)
    height = int(img.shape[0] * 2.2)
    resized = cv2.resize(img, (width, height), interpolation = cv2.INTER_AREA)

    return resized

def get_boxes(outputs, height, width):
  boxes = []
  confs = []
  class_ids = []

  for o in outputs:
    for d in o:
      scores = d[5:]
      class_id = np.argmax(scores)
      conf = scores[class_id]
      if conf > 0.3:
        center_x = int(d[0] * width)
        center_y = int(d[1] * height)
        w = int(d[2] * width)
        h = int(d[3] * height)

        x = int(center_x - w/2)
        y = int(center_y - h/2)

        boxes.append([x,y,w,h])
        confs.append(float(conf))
        class_ids.append(class_id)

  return boxes, confs, class_ids

def detect_objs(img, net, output_layers):
    

    blob = cv2.dnn.blobFromImage(img, scalefactor = 0.00392, size = (416,416), mean = (0, 0, 0), swapRB = True, crop = False)
    net.setInput(blob)
    outputs = net.forward(output_layers)

    return blob, outputs

def load_image(img_path):
    img = cv2.imread(img_path)
    img = cv2.resize(img, None, fx = 0.4, fy = 0.4)
    height, width, channels = img.shape

    return img, height, width, channels


def image_detect(img_path, title):
    model, classes, colors, output_layers = load_trained_yolo()
    image, height, width, channels = load_image(img_path)
    blob, outputs = detect_objs(image, model, output_layers)
    boxes, confs, class_ids = get_boxes(outputs, height, width)
    res = draw_labels(boxes, confs, colors, class_ids, classes, image)
    cv2.imwrite(title+'.png', res)

