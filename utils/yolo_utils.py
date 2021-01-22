import numpy as np
import cv2 as cv
import time
import os
import sys


def init(args):
    # Get the labels
    labels = open(args.labels).read().strip().split('\n')

    # Initializing colors to represent each label uniquely
    colors = np.random.randint(0, 255, size=(len(labels), 3), dtype='uint8')

    # Load the weights and configuration to form the pretrained YOLOv3 model
    net = cv.dnn.readNetFromDarknet(args.config, args.weights)

    # Get the output layer names of the model
    layer_names = net.getLayerNames()
    layer_names = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return labels, colors, net, layer_names


def process(args, labels, colors, net, layer_names):
    # If both image and video files are given then raise error
    if args.image_path is None and args.video_path is None:
        print('Neither path to an image or path to video provided')
        print('Starting Inference on Webcam')

    # Do inference with given image
    if args.image_path:
        # Read the image
        try:
            img = cv.imread(args.image_path)
            height, width = img.shape[:2]
        except:
            raise Exception('Image cannot be loaded!\n'
                            'Please check the path provided!')
        finally:
            img, _, _, _, _ = infer_image(net, layer_names, height, width, img, colors, labels, args)
            save_image(img, args.output_name, args.save_path)
    elif args.video_path:
        if args.output_name is None:
            print("No output name specified. Exiting...")
            sys.exit()

        # Read the video
        try:
            vid = cv.VideoCapture(args.video_path)
            height, width = None, None
            writer = None
        except:
            raise Exception('Video cannot be loaded!\n'
                            'Please check the path provided!')
        finally:
            timings = np.array([])
            count = 0
            # Will attempt to count the number of frames in the video,
            # This is dependent on the OpenCV version
            try:
                total = int(vid.get(cv.CAP_PROP_FRAME_COUNT))
            except:
                try:
                    total = int(vid.get(cv.cv.CV_CAP_PROP_FRAME_COUNT))
                except:
                    print("Have to count frames manually. This might take a while...")
                    total = count_frames_manual(vid)
                    print("Count complete...")

            delay = args.delay_time
            num_images = 0

            # Scan each frame in video
            while True:
                grabbed, raw_frame = vid.read()
                try:
                    labeled_frame = raw_frame.copy()
                except:
                    labeled_frame = None

                # Checking if the complete video is read
                if not grabbed:
                    break

                if width is None or height is None:
                    height, width = labeled_frame.shape[:2]

                if writer is None and args.save_video is True:
                    # Initialize the video writer
                    fourcc = cv.VideoWriter_fourcc(*"MJPG")
                    writer = cv.VideoWriter(args.video_output_path, fourcc, 30,
                                            (labeled_frame.shape[1], labeled_frame.shape[0]), True)

                # Time frame inference and show progress
                start = time.time()
                if delay <= 0 and labeled_frame is not None:
                    labeled_frame, _, _, classids, _ = infer_image(net, layer_names, height, width,
                                                                   labeled_frame, colors, labels, args)

                    try:
                        obj = labels[classids[0]]
                    except:
                        obj = None

                    if ((obj == 'truck') or (obj == 'car')) and delay <= 0:
                        if (args.option == 0) or (args.option == 2):  # Save raw image
                            save_image(raw_frame, args.output_name, args.save_path, True)
                        elif (args.option == 1) or (args.option == 2):  # Save labeled image
                            save_image(labeled_frame, args.output_name, args.save_path, False)
                        num_images += 1
                        delay = args.delay_time

                delay -= 1
                if args.save_video is True:
                    writer.write(labeled_frame)

                end = time.time()
                timings = np.append(timings, (end - start))
                show_progress_bar(timings.size, total, num_images, np.average(timings))

            # End process
            print("\n[INFO] Cleaning up...")
            if writer is not None:
                writer.release()
            vid.release()
    else:
        # Infer real-time on webcam
        count = 0

        vid = cv.VideoCapture(0)
        while True:
            _, frame = vid.read()
            height, width = frame.shape[:2]

            if count == 0:
                frame, boxes, confidences, classids, index = infer_image(net, layer_names, height, width, frame, colors,
                                                                         labels, args)
                count += 1
            else:
                frame, boxes, confidences, classids, index = infer_image(net, layer_names, height, width, frame, colors,
                                                                         labels, args, boxes, confidences, classids,
                                                                         index, infer=False)
                count = (count + 1) % 6

            cv.imshow('webcam', frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        vid.release()
        cv.destroyAllWindows()

    print("Process done.")


def save_image(img, output_name, save_path, raw):
    num = 1
    while True:
        if raw is True:
            filename = '{s}{o}{n}_raw.jpg'.format(s=save_path, o=output_name, n=num)
        else:
            filename = '{s}{o}{n}_labeled.jpg'.format(s=save_path, o=output_name, n=num)
        if os.path.isfile(filename):
            num += 1
        else:
            cv.imwrite(filename, img)
            break


def draw_labels_and_boxes(img, boxes, confidences, classids, idxs, colors, labels):
    # If there are any detections
    if len(idxs) > 0:
        for i in idxs.flatten():
            # Get the bounding box coordinates
            x, y = boxes[i][0], boxes[i][1]
            w, h = boxes[i][2], boxes[i][3]

            # Get the unique color for this class
            color = [int(c) for c in colors[classids[i]]]

            # Draw the bounding box rectangle and label on the image
            cv.rectangle(img, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:4f}".format(labels[classids[i]], confidences[i])
            cv.putText(img, text, (x, y - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return img


def generate_boxes_confidences_classids(outs, height, width, tconf):
    boxes = []
    confidences = []
    classids = []

    for out in outs:
        for detection in out:
            # print(detection)
            # a = input('GO!')

            # Get the scores, class ID, and the confidence of the prediction
            scores = detection[5:]
            classid = np.argmax(scores)
            confidence = scores[classid]

            # Consider only the predictions that are above a certain confidence level
            if confidence > tconf:
                # TODO Check detection
                box = detection[0:4] * np.array([width, height, width, height])
                centerX, centerY, bwidth, bheight = box.astype('int')

                # Using the center x, y coordinates to derive the top
                # and the left corner of the bounding box
                x = int(centerX - (bwidth / 2))
                y = int(centerY - (bheight / 2))

                # Append to list
                boxes.append([x, y, int(bwidth), int(bheight)])
                confidences.append(float(confidence))
                classids.append(classid)

    return boxes, confidences, classids


def infer_image(net, layer_names, height, width, img, colors, labels, args,
                boxes=None, confidences=None, classids=None, idxs=None, infer=True):
    if infer:
        # Constructing a blob from the input image
        blob = cv.dnn.blobFromImage(img, 1 / 255.0, (416, 416),
                                    swapRB=True, crop=False)

        # Perform a forward pass of the YOLO object detector
        net.setInput(blob)

        # Getting the outputs from the output layers
        start = time.time()
        outs = net.forward(layer_names)
        end = time.time()

        if args.show_time:
            print("[INFO] YOLOv3 took {:6f} seconds".format(end - start))

        # Generate the boxes, confidences, and classIDs
        boxes, confidences, classids = generate_boxes_confidences_classids(outs, height, width, args.confidence)

        # Apply Non-Maxima Suppression to suppress overlapping bounding boxes
        idxs = cv.dnn.NMSBoxes(boxes, confidences, args.confidence, args.threshold)

    if boxes is None or confidences is None or idxs is None or classids is None:
        raise Exception('[ERROR] Required variables are set to None before drawing boxes on images.')

    # Draw labels and boxes on the image
    img = draw_labels_and_boxes(img, boxes, confidences, classids, idxs, colors, labels)

    return img, boxes, confidences, classids, idxs


def show_progress_bar(count, total, num_images, diff, status=''):
    bar_length = 40
    filled_length = int(round(bar_length * count / float(total)))

    percentage = round(100.0 * count / float(total), 1)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)

    sec_left = diff * (total - count)

    sys.stdout.write("[%s] %s%s (%s) %s ...%s\r" % (
        str(bar), str(percentage), '%', time.strftime('%Hh, %Mm, %Ss', time.gmtime(sec_left)),
        '[{i}]'.format(i=num_images), status))
    sys.stdout.flush()


def count_frames_manual(video):
    total = 0

    while True:
        grabbed, frame = video.read()

        if not grabbed:
            break

        total += 1

    video.release()
    return total

    video.release()
    return total
