import numpy as np
import cv2 as cv
import time
import os
import sys
import multiprocessing

def init(labelfile, config, weights):
    # Get the labels
    labels = open(labelfile).read().strip().split('\n')

    # Initializing colors to represent each label uniquely
    colors = np.random.randint(0, 255, size=(len(labels), 3), dtype='uint8')

    # Load the weights and configuration to form the pretrained YOLOv3 model
    net = cv.dnn.readNetFromDarknet(config, weights)

    # Get the output layer names of the model
    layer_names = net.getLayerNames()
    layer_names = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    
    return labels, colors, net, layer_names

def parse_input_path(input_path):
    data = []
    # Get everything from input path
    for path in os.listdir(input_path):
        if ('.png' in path) or ('.jpg' in path) or ('jpeg' in path) or ('.mp4' in path) or ('.avi' in path):
            data.append(path)

    return data

def start_yolo_process(args):
    fileslist = parse_input_path(args.input_path)
    processes = []
    tag = []
    

    # Parse through Input Data Folder
    for idx, file in enumerate(fileslist):
        pid = 0
        while ((pid < multiprocessing.cpu_count()) and (idx < len(fileslist))):
            if ((idx + pid) < len(fileslist)):
                # Create Processes
                try:
                    tFile = fileslist[idx+pid]
                    in_path = str(args.input_path + tFile)
                    processed_path = str(args.processed_folder + tFile)
                    
                    arguments = (tFile,
                                 in_path,
                                 processed_path,
                                 tFile[:tFile.find('.')],
                                 args.labels,
                                 args.config,
                                 args.weights,
                                 args.output_path,
                                 args.delay_time,
                                 args.save_video,
                                 args.option,
                                 args.video_output_path,
                                 args.confidence,
                                 args.threshold,
                                 pid,
                                 False,
                                 None)

                    
                    process = multiprocessing.Process(target=yolo_process, args=arguments)
                    
                    if in_path not in tag:
                        processes.append(process)
                        tag.append(in_path)
                except Exception as err:
                    print("[ERROR] {e}".format(e=err))
            pid += 1
        
        # Execute Processes
        for process in processes:
            try:
                process.start()
            except Exception as err:
                print("[ERROR] {e}".format(e=err))
            
        for process in processes:
            try:
                process.join()
            except Exception as err:
                print("[ERROR] {e}".format(e=err))
                
        processes.clear()

def yolo_process(file, file_path, done_path, output_name, labels, config, weights, save_path, delay_time, save_video, option, video_output_path, confidence, threshold, process_id, gui, gui_obj):
    image_path = None
    video_path = None
    
    if ('.png' in file_path) or ('.jpg' in file_path) or ('.jpeg' in file_path):
        image_path = file_path
        
    if ('.mp4' in file_path) or ('.avi' in file_path):
        video_path = file_path
    
    # Initialize labels, colors, and pretrain model
    try:
        labels, colors, net, layer_names = init(labels,
                                                config, 
                                                weights)
    except Exception as err:
        print("[ERROR] {e}".format(e=err))
    
    # If both image and video files are given then raise error

    if image_path is None and video_path is None:
        print('[WARNING] Neither path to an image or path to video provided. Starting Inference on Webcam...')

    # Do inference with given image
    if image_path:
        print('[INFO] Starting image processing of {ip}...'.format(ip=str(image_path)))

        if not os.path.exists(image_path):
            print("[ERROR] Image path does not exist. Exiting...")
            sys.exit()

        # Read the image
        try:
            img = cv.imread(image_path)
            height, width = img.shape[:2]
        except:
            raise Exception('[ERROR] Image cannot be loaded!\n'
                            'Please check the path provided!')
        finally:
            img, _, _, _, _, _, _, _, _ = infer_image(net, layer_names, height, width, img, colors, labels, confidence, threshold)
            save_image(img, output_name, save_path)
            os.rename(file_path, done_path)
    elif video_path:
        print('[INFO] Starting video processing of {vp}...'.format(vp=str(video_path)))
    
        if output_name is None:
            print("[ERROR] No output name specified. Exiting...")
            sys.exit()

        if not os.path.exists(video_path):
            print("[ERROR] Video path does not exist. Exiting...")
            sys.exit()

        # Read the video
        try:
            vid = cv.VideoCapture(video_path)
            boxHeight, boxWidth = 0, 0
            height, width = None, None
            writer = None
        except:
            raise Exception('[ERROR] Video cannot be loaded!\n'
                            'Please check the path provided!')
        finally:
            timings = np.array([])

            # Will attempt to count the number of frames in the video,
            # This is dependent on the OpenCV version
            try:
                total = int(vid.get(cv.CAP_PROP_FRAME_COUNT))
            except:
                try:
                    total = int(vid.get(cv.CV_CAP_PROP_FRAME_COUNT))
                except:
                    print("[WARNING] Have to count frames manually. This might take a while...")
                    total = count_frames_manual(vid)
                    print("[SUCCESS] Count complete...")

            delay = delay_time
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

                if writer is None and save_video is True:
                    # Initialize the video writer
                    fourcc = cv.VideoWriter_fourcc(*"MJPG")
                    writer = cv.VideoWriter(video_output_path, fourcc, 30,
                                            (labeled_frame.shape[1], labeled_frame.shape[0]), True)

                # Time frame inference and show progress
                start = time.time()
                if delay <= 0 and labeled_frame is not None:
                    labeled_frame, _, _, classids, _, xPos, yPos, boxWidth, boxHeight = infer_image(net, 
                                                                                                    layer_names, 
                                                                                                    height, 
                                                                                                    width,
                                                                                                    labeled_frame, 
                                                                                                    colors, 
                                                                                                    labels, 
                                                                                                    confidence, 
                                                                                                    threshold)

                    try:
                        obj = labels[classids[0]]
                    except:
                        obj = None
                        
                    # Descriptions of a typical freight truck
                    if (((obj == 'truck') and (boxWidth >= (boxHeight * 1.5)) 
                                          and (boxHeight >= 0.4 * height)
                                          and (boxWidth >= 0.7 * width))):
                        # Extract Timestamp from Video (TODO: Explore with this: https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/)
                        try:
                            modified_name = output_name + ('_{time}'.format(time=str(int(vid.get(cv.CAP_PROP_POS_MSEC)))))
                            # print(modified_name)
                        except:
                            # print("[ERROR] Failed to get timestamp of video")
                            modified_name = output_name + '_?'

                        #report_image_attributes(modified_name, xPos, boxWidth, boxHeight, width, height)
                        
                        if (option == 0) or (option == 2):  # Save raw image
                            save_image(raw_frame, modified_name, save_path, True)
                            num_images += 1
                        if (option == 1) or (option == 2):  # Save labeled image
                            save_image(labeled_frame, modified_name, save_path, False)
                            num_images += 1
                        if (option == 3): # Save Collage 
                            try:
                                collage_name = str(modified_name + "_collage.png")
                                primary = raw_frame
                                
                                # Capture secondary frame (10 frames over)
                                for i in range(10):
                                    _, secondary = vid.read()

                                
                                # Put two images vertically on a collage
                                save_image(np.vstack([primary, secondary]), collage_name, save_path, True)
                                num_images += 1
                            except Exception as err:
                                print("[ERROR] {e}".format(e=err))

                        delay = delay_time

                delay -= 1
                if save_video is True:
                    writer.write(labeled_frame)

                end = time.time()
                timings = np.append(timings, (end - start))
                show_progress_bar(timings.size, total, num_images, np.average(timings), output_name, process_id)
                
                # Return progress bar value
                if gui is True:
                    gui_obj.bar['value'] = (timings.size / total) * 100
                    gui_obj.bar.update_idletasks()
                		
            # End process
            print("\n[INFO] Cleaning up...")
            if writer is not None:
                writer.release()
            vid.release()
            os.rename(file_path, done_path)

    else:
        # Infer real-time on webcam
        count = 0

        vid = cv.VideoCapture(0)
        while True:
            _, frame = vid.read()
            height, width = frame.shape[:2]

            if count == 0:
                frame, boxes, confidences, classids, index, _, _, _, _ = infer_image(net,
                                                                                     layer_names,
                                                                                     height,
                                                                                     width,
                                                                                     frame,
                                                                                     colors,
                                                                                     labels, 
                                                                                     confidence, 
                                                                                     threshold)
                count += 1
            else:
                frame, boxes, confidences, classids, index, _, _, _, _ = infer_image(net,
                                                                                     layer_names, 
                                                                                     height, 
                                                                                     width, 
                                                                                     frame, 
                                                                                     colors,
                                                                                     labels, 
                                                                                     confidence, 
                                                                                     threshold, 
                                                                                     boxes, 
                                                                                     confidences, 
                                                                                     classids,
                                                                                     index, 
                                                                                     infer=False)
                count = (count + 1) % 6

            cv.imshow('webcam', frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        vid.release()
        cv.destroyAllWindows()

    print("[SUCCESS] Image Processing Complete...")

def report_image_attributes(modified_name, xPos, boxWidth, boxHeight, width, height):
    print("Name: {n}".format(n=modified_name))
    print("X Position: {x}".format(x=xPos))
    print("BoxWidth: {bw}".format(bw=boxWidth))
    print("BoxHeight: {bh}".format(bh=boxHeight))
    print("Image Width: {iw}".format(iw=width))
    print("Image Height: {ih}\n\n".format(ih=height))


def save_image(img, output_name, save_path, raw):
    num = 1
    while True:
        if raw is True:
            filename = '{s}{o}_{n}_raw.png'.format(s=save_path, o=output_name, n=num)
        else:
            filename = '{s}{o}_{n}_labeled.png'.format(s=save_path, o=output_name, n=num)
        if os.path.isfile(filename):
            num += 1
        else:
            cv.imwrite(filename, img)
            break


def draw_labels_and_boxes(img, boxes, confidences, classids, idxs, colors, labels):
    # If there are any detections
    x, y, w, h = 0, 0, 0, 0
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

    return img, x, y, w, h


def generate_boxes_confidences_classids(outs, height, width, tconf):
    boxes = []
    confidences = []
    classids = []

    for out in outs:
        for detection in out:
            # Get the scores, class ID, and the confidence of the prediction
            scores = detection[5:]
            classid = np.argmax(scores)
            confidence = scores[classid]

            # Consider only the predictions that are above a certain confidence level
            if confidence > tconf:
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


def infer_image(net, layer_names, height, width, img, colors, labels, confidence, threshold, 
                boxes=None, confidences=None, classids=None, idxs=None, infer=True):
    if infer:
        # Constructing a blob from the input image
        blob = cv.dnn.blobFromImage(img, 1 / 255.0, (416, 416),
                                    swapRB=True, crop=False)

        # Perform a forward pass of the YOLO object detector
        net.setInput(blob)

        # Getting the outputs from the output layers
        outs = net.forward(layer_names)

        # Generate the boxes, confidences, and classIDs
        boxes, confidences, classids = generate_boxes_confidences_classids(outs, height, width, confidence)

        # Apply Non-Maxima Suppression to suppress overlapping bounding boxes
        idxs = cv.dnn.NMSBoxes(boxes, confidences, confidence, threshold)

    if boxes is None or confidences is None or idxs is None or classids is None:
        raise Exception('[ERROR] Required variables are set to None before drawing boxes on images.')

    # Draw labels and boxes on the image
    img, x, y, w, h = draw_labels_and_boxes(img, boxes, confidences, classids, idxs, colors, labels)

    return img, boxes, confidences, classids, idxs, x, y, w, h


def show_progress_bar(count, total, num_images, diff, name, pid, status=''):
    bar_length = 40
    filled_length = int(round(bar_length * count / float(total)))

    percentage = round(100.0 * count / float(total), 1)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)

    sec_left = diff * (total - count)
    
    sys.stdout.write("%s[%s] %s%s (%s) %s ...%s\r\n" % ('{p}:'.format(p=name),
                                                        str(bar), 
                                                        str(percentage), 
                                                        '%', 
                                                        time.strftime('%Hh, %Mm, %Ss', time.gmtime(sec_left)),
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
