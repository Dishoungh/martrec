import subprocess
import os
import time
import csv
import config.keys

def create_bucket(bucket_name):
    try:
        subprocess.run(['aws', 's3api', 'create-bucket', '--bucket', bucket_name, '--region', 'us-east-1'], stdout=subprocess.DEVNULL)
        print("[SUCCESS]: AWS Bucket Created as {bn}".format(bn=bucket_name))
    except:
        try:
            subprocess.run(['aws', 's3api', 'create-bucket', '--bucket', bucket_name, '--region', 'us-east-2'], stdout=subprocess.DEVNULL)
            print("[SUCCESS]: AWS Bucket Created as {bn}".format(bn=bucket_name))

        except Exception as e:
            print("[ERROR]: {err}".format(err=e)) 

def send_to_s3(args):
    # Upload all files in args.save_path
    try:
        subprocess.run(['aws', 's3', 'sync', args.save_path, 's3://{bn}'.format(bn=args.bucket_name),
                        '--acl', 'public-read'], stdout=subprocess.DEVNULL)
        print("[SUCCESS]: Images successfully uploaded to {bn}".format(bn=args.bucket_name))
    except Exception as err:
        print("[ERROR]: {e}".format(e=err))


def get_csv(args):
    try:
        # Grab all items stored in AWS bucket
        objects = subprocess.run(["aws", "s3api", "list-objects", "--bucket", args.bucket_name,
                        "--query", 'Contents[].{Key: Key}'], text=True,
                        stdout=subprocess.PIPE).stdout.splitlines()
        with open(os.path.join(args.csv_save, '{d}.csv'.format(d=time.strftime("%Y%m%d-%H%M%S"))), 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['image_url'])
            for obj in objects:
                writer.writerow(["https://{bn}.s3.amazonaws.com/{o}".format(bn=args.bucket_name, o=obj)])
        print('[SUCCESS] CSV Generation Complete...')
    except Exception as err:
        print("[ERROR]: {e}".format(e=err))


def send_batch(csv_path):
    # Get latest file in csv_path
    files = os.listdir(csv_path)
    target_file = max([os.path.join(csv_path, filename) for filename in files])

    # Send csv file to MTurk
    print(target_file)
