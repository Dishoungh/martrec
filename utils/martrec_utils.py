import argparse
import os
import sys
import subprocess
import platform

def parse_arguments():
    # Grab arguments from command line
    parser = argparse.ArgumentParser()
    
    # Arguments for parser
    
    parser.add_argument('-aws', '--configure-aws',
                        type=bool,
                        default=False,
                        help='Initiates AWS configuration. Requires an ID and Secret Key in the keys.py file')
    
    parser.add_argument('-bn,', '--bucket-name',
                        type=str,
                        default=None,
                        help='Specifies name of the S3 bucket')
    
    parser.add_argument('-c', '--confidence',
                        type=float,
                        default=0.5,
                        help='The model will reject boundaries which '
                             'has a probability less than the confidence value. '
                             'default: 0.5')
    
    parser.add_argument('-cb', '--create-bucket',
                        type=bool,
                        default=False,
                        help='Creates AWS bucket')
    
    parser.add_argument('-cfg', '--config',
                        type=str,
                        default='./config/yolov3.cfg',
                        help='Path to the configuration file for the '
                             'YOLOv3 model.')
                             
    parser.add_argument('-co', '--clear-outputs',
                        type=bool,
                        default=False,
                        help='Clears the data in the output folder including any generated csv files')                 
    
    parser.add_argument('-cor', '--cors-file',
                        type=str,
                        default='config/cors.json',
                        help='Specifies location of cors json file')
    
    parser.add_argument('-csv', '--csv-save',
                        type=str,
                        default='./csv_files',
                        help='Specifies where to save the AWS csv file')
    
    parser.add_argument('-dm', '--download-model',
                        type=bool,
                        default=False,
                        help='Set to True, if the model weights and '
                             'configurations are not present on your local machine.')
    
    parser.add_argument('-dt', '--delay-time',
                        type=int,
                        default=100,
                        help='Sets the delay time for extracting images. '
                             'Purpose of this is to not spam the output folder.'
                             '\nAcceptable values are: [1-1000]')
    
    parser.add_argument('-g', '--gui',
                        type=bool,
                        default=False,
                        help='Initiates GUI')
    
    parser.add_argument('-gen', '--generate-csv',
                        type=bool,
                        default=False,
                        help='Generates a CSV file, listing all objects in the specified AWS bucket')
    
    parser.add_argument('-i', '--image-path',
                        type=str,
                        default=None,
                        help='The path to the image file to process.')
    
    parser.add_argument('-l', '--labels',
                        type=str,
                        default='./config/coco-labels',
                        help='Path to the file having the labels in a '
                             'new-line separated way.')
    
    parser.add_argument('-m', '--model-path',
                        type=str,
                        default='./config/',
                        help='The directory where the model weights '
                             'and configuration files are.')
    
    parser.add_argument('-o', '--option',
                        type=int,
                        default=0,
                        help='Determines how the program will save images\n'
                             'Options:\n'
                             '0 = Save Raw Image Only\n'
                             '1 = Save Labeled Image Only\n'
                             '2 = Save Both Raw and Labeled\n'
                             '3 = Save No Images\n'
                             'Default: 0')
                             
    parser.add_argument('-on', '--output-name',
                        type=str,
                        default='output',
                        help='Sets the name of the output image. Default is: output')
    
    parser.add_argument('-p', '--process',
                        type=bool,
                        default=False,
                        help='Uses YOLOv3 to process a video file or image or webcam stream')                          
    
    parser.add_argument('-s', '--save-path',
                        type=str,
                        default='./output_data/',
                        help='Sets where to save output images. Default is: ./output_data/')
    
    parser.add_argument('-s3', '--send-images',
                        type=bool,
                        default=False,
                        help='Sends images specified in --save-path to Amazon S3 after process')
    
    parser.add_argument('-sb', '--send-batch',
                        type=bool,
                        default=False,
                        help='Sends CSV file in csv save path to MTurk')      
    
    parser.add_argument('-sv', '--save-video',
                        type=bool,
                        default=False,
                        help='Save an output video file? Default is: False')
    
    parser.add_argument('-th', '--threshold',
                        type=float,
                        default=0.3,
                        help='The threshold to use when applying the '
                             'Non-Max Suppression')
    
    parser.add_argument('-v', '--video-path',
                        type=str,
                        default=None,
                        help='The path to the video file to process.')
    
    parser.add_argument('-vo', '--video-output-path',
                        type=str,
                        default='./output.avi',
                        help='The path of the output video file. '
                             'Default is: ./output.avi.')                            
    
    parser.add_argument('-w', '--weights',
                        type=str,
                        default='./config/yolov3.weights',
                        help='Path to the file which contains the '
                             'weights for YOLOv3.')
    
    args, _ = parser.parse_known_args()
    return args


def check_parsed(args):
    # Checks if directory from save path exists or not
    if not os.path.isdir(args.save_path):
        os.mkdir(args.save_path)

    if not os.path.isdir(args.csv_save):
        os.mkdir(args.csv_save)

    # Checks if delay time is valid
    if args.delay_time <= 0 or args.delay_time > 1000:
        print("[ERROR] Invalid delay settings. Acceptable values are: [1-1000]")
        sys.exit()

    # Checks if there is a save path specified
    if args.save_path is None:
        print("[ERROR] Invalid save path")
        sys.exit()

    # Checks if save options are valid
    if args.option < 0 or args.option > 3:
        print("[ERROR] Invalid option settings. Acceptable values are: [0-3]")
        sys.exit()
    else:
        if args.option != 3 and args.process is True:
            print("[INFO] Images will be saved under: {sp}".format(sp=args.save_path))

    # Download the YOLOv3 models if needed
    if args.download_model:
    	download_model()

    if args.clear_outputs is True:
        print("[INFO] Clearing Outputs")
        clear_outputs(args.save_path, args.csv_save)

def download_model():
    link = 'https://pjreddie.com/media/files/yolov3.weights'
    
    print("[INFO] Downloading YOLOv3 Model...")
    if 'Linux' in platform.platform():
        try:
            subprocess.run(['wget', '--no-check-certificate', link, '-P', args.model_path])
            print("[SUCCESS] YOLOv3 Model Downloaded...")
        except Exception as err:
            print("[ERROR] {e}".format(e=err))
    elif 'Windows' in platform.platform():
        import requests
        from utils.yolo_utils import show_progress_bar
        with open(args.weights, 'wb') as f:
            response = requests.get(link, stream=True)
            total_length = response.headers.get('content-length')
            
            if total_length is None:
                f.write(response.content)
            else:
                data_length = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    f.write(data)
                    data_length += len(data)
                    show_progress_bar(data_length, total_length, 0, 2e-7)
        print("\n[SUCCESS] YOLOv3 Model Downloaded...")
    else:
        print("[ERROR] Unknown platform. Download link through https://pjreddie.com/media/files/yolov3.weights. Exiting...")
        sys.exit()

def clear_outputs(output_path, csv_path):
    for file in os.listdir(output_path):
        os.remove(os.path.join(output_path, file))

    for file in os.listdir(csv_path):
        os.remove(os.path.join(csv_path, file))

    print("[SUCCESS] Cleared Output Files")
