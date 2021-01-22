import subprocess
import os
import time
import csv
import config.keys

ACCESS_ID = config.keys.AWS_ACCESS_KEY_ID
SECRET_ID = config.keys.AWS_SECRET_KEY
CANONICAL = config.keys.CANONICAL_USER_ID

def send_to_s3(args):
    print("Sending to S3...")

    # Upload all files in args.save_path
    try:
        subprocess.run(['aws', 's3', 'sync', args.save_path, 's3://{bn}'.format(bn=args.bucket_name),
                        '--acl', 'public-read'], stdout=subprocess.DEVNULL)
    except Exception as err:
        print("Error: {e}".format(e=err))


def get_csv(args):
    try:
        # Grab all items stored in AWS bucket
        objects = subprocess.run(["aws", "s3api", "list-objects", "--bucket", args.bucket_name,
                        "--query", 'Contents[].{Key: Key}'], text=True,
                        stdout=subprocess.PIPE).stdout.splitlines()

        # Open a CSV file and put all objects in bucket in CSV
        with open(os.path.join(args.csv_save, '{d}.csv'.format(d=time.strftime("%Y%m%d-%H%M%S"))), 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['image_url'])
            for o in objects:
                writer.writerow(["https://{bn}.s3.amazonaws.com/{obj}".format(bn=args.bucket_name, obj=o)])
        print('[INFO] CSV Generation Complete...')
    except Exception as err:
        print("Error: {e}".format(e=err))


def send_batch(csv_path):
    # Get latest file in csv_path
    files = os.listdir(csv_path)
    target_file = max([os.path.join(csv_path, filename) for filename in files])

    # Send csv file to MTurk