from utils.yolo_utils import *
from utils.martrec_utils import *
from utils.aws_utils import *


# TODO: Clean up code, implement AWS, and redo README
def main():
    # Parse arguments from command line and check arguments
    args = parse_arguments()
    check_parsed(args)

    if args.process is True:
        # Initialize labels, colors, and pretrain model
        labels, colors, net, layer_names = init(args)

        # Extract images (using YOLO)
        process(args, labels, colors, net, layer_names)

    if args.create_bucket is True:
        # Create AWS bucket
        create_bucket(args.bucket_name)

    if args.send_images is True:
        # Upload extracted images to AWS S3 (if argument is set to true)
        send_to_s3(args)

    if args.generate_csv is True:
        # Pull key IDs from objects and get CSV file
        get_csv(args)

    if args.send_batch is True:
        # Once CSV file is made, parse it, create CSV in proper format, and upload it to MTurk as a batch
        # WARNING: The most recent csv file in the directory will be sent
        send_batch(args.csv_save)

    print('[INFO]: Program complete...')

if __name__ == '__main__':
    main()
