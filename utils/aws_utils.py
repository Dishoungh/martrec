import subprocess
import os
import time
import csv
import sys
import errno
import platform

def create_bucket(bucket_name):
    try:
        subprocess.run(['aws', 's3api', 'create-bucket', '--bucket', bucket_name, '--region', 'us-east-1'], stdout=subprocess.DEVNULL)
        print("[SUCCESS] AWS Bucket Created as {bn}".format(bn=bucket_name))
    except:
        try:
            subprocess.run(['aws', 's3api', 'create-bucket', '--bucket', bucket_name, '--region', 'us-east-2'], stdout=subprocess.DEVNULL)
            print("[SUCCESS] AWS Bucket Created as {bn}".format(bn=bucket_name))

        except Exception as e:
            print("[ERROR] {err}".format(err=e))
            sys.exit()

def configure_aws():
    print("[INFO] Configuring AWS...")

    if ('Linux' in platform.platform()):
        process = subprocess.Popen(['aws', 'configure'], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL)
    elif ('Windows' in platform.platform()):
        process = subprocess.Popen('aws configure', stdin=subprocess.PIPE, stdout=subprocess.DEVNULL)
    else:
        print("[ERROR] AWS Configuration failed due to unknown platform detection. Exiting...")
        sys.exit()
    
    import config.keys

    for x in range(4):
        # Enter Access Key ID
        ans = None
        if x == 0:
            ans = config.keys.AWS_ACCESS_KEY_ID
        elif x == 1:
            ans = config.keys.AWS_SECRET_KEY
        elif x == 2:
            ans = config.keys.AWS_REGION_NAME
        elif x == 3:
            ans = config.keys.AWS_OUTPUT_FORMAT

        line = ('{a}\n'.format(a=ans)).encode()

        try:
            process.stdin.write(line)
        except IOError as e:
            if e.errno == errno.EPIPE or e.errno == errno.EINVAL:
                break
            else:
                raise
    
    print("[SUCCESS] AWS Configured...")


def send_to_s3(save_path, bucket_name):
    # Upload all files in save_path
    try:
        subprocess.run(['aws', 's3', 'sync', save_path, 's3://{bn}'.format(bn=bucket_name),
                        '--acl', 'public-read'], stdout=subprocess.DEVNULL)
        print("[SUCCESS] Images successfully uploaded to {bn}".format(bn=bucket_name))
    except Exception as err:
        print("[ERROR] {e}".format(e=err))
        sys.exit()

def get_csv(csv_save, bucket_name):
    try:
        # Grab all items stored in AWS bucket
        objects = subprocess.run(["aws", "s3api", "list-objects", "--bucket", bucket_name,
                        "--query", 'Contents[].{Key: Key}'], text=True,
                        stdout=subprocess.PIPE).stdout.splitlines()
        with open(os.path.join(csv_save, '{d}.csv'.format(d=time.strftime("%Y%m%d-%H%M%S"))), 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['image_url'])
            for obj in objects:
                writer.writerow(["https://{bn}.s3.amazonaws.com/{o}".format(bn=bucket_name, o=obj)])
        print('[SUCCESS] CSV Generation Complete...')
    except Exception as err:
        print("[ERROR] {e}".format(e=err))
        sys.exit()


def set_cors(bucket_name, cors_file):
    try:
        subprocess.run(['aws', 's3api', 'put-bucket-cors', '--bucket', bucket_name, '--cors-configuration', 'file://{c}'.format(c=cors_file)], stdout=subprocess.DEVNULL)
        print("[SUCCESS] CORS Settings Applied in Bucket: {bn}".format(bn=bucket_name))
    except Exception as err:
        print("[ERROR] {e}".format(e=err))
        sys.exit()

