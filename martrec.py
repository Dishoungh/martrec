from utils.yolo_utils import *
from utils.martrec_utils import *
from utils.aws_utils import *

def main():
    # Parse arguments from command line and check arguments
    args = parse_arguments()
    check_parsed(args)

    if args.configure_aws is True:
        configure_aws()

    if args.process is True:
        # Initialize labels, colors, and pretrain model
        labels, colors, net, layer_names, data = init(args.labels,
        					      args.config, 
        					      args.weights,
                                                      args.input_path)

        # Parse through Input Data Folder
        for d in data:
            if ('.png' in d) or ('.jpg' in d) or ('.jpeg' in d):
                # Process Image
                process(str(args.input_path + d),
                        None,
                        d[:d.find('.')],
                        args.output_path,
                        args.delay_time,
                        args.save_video,
                        args.option,
                        args.video_output_path,
                        args.confidence,
                        args.threshold,
                        labels,
                        colors,
                        net,
                        layer_names,
                        gui=False,
                        gui_obj=None)
            else:
                if ('.mp4' in d) or ('.avi' in d):
                    # Process Video
                    process(None,
                            str(args.input_path + d),
                            d[:d.find('.')],
                            args.output_path,
                            args.delay_time,
                            args.save_video,
                            args.option,
                            args.video_output_path,
                            args.confidence,
                            args.threshold,
                            labels,
                            colors,
                            net,
                            layer_names,
                            gui=False,
                            gui_obj=None)
                            

    if args.create_bucket is True:
        # Create AWS bucket
        create_bucket(args.bucket_name)
        set_cors(args.bucket_name, args.cors_file)

    if args.send_images is True:
        # Upload extracted images to AWS S3 (if argument is set to true)
        send_to_s3(args.save_path, args.bucket_name)

    if args.generate_csv is True:
        # Pull key IDs from objects and get CSV file
        get_csv(args.csv_save, args.bucket_name)

    if args.send_batch is True:
        # Once CSV file is made, parse it, create CSV in proper format, and upload it to MTurk
        # WARNING: The most recent csv file in the directory will be sent
        send_batch(args.csv_save)

    print('[SUCCESS] Program complete...')

if __name__ == '__main__':
    main()
