## martrec
A simple python script to automate the process of extracting images of trucks and cars on the road from a video file to uploading extracted images to AWS (Amazon Web Services) S3 to generating a .csv file of the objects' URLs for Mechanical Turk.

Crowdsourcing processes can be tedious to setup. You'll have to upload the data somewhere and grab their URLs individually and compile them into a .csv file for Mechanical Turk to create HITs (Human Intelligence Tasks). This can take a while. The purpose of this repo is to automate most of that process and can be applied to multiple applications.

While Martrec does support GUI using the TKinter package, it's recommended to use the CLI version instead of the GUI since the GUI doesn't have the full functionality of the CLI version.


## Tech/Framework Used
<b>Built with</b>
- [YOLOv3](https://pjreddie.com/darknet/yolo/)
- [AWS CLI](https://aws.amazon.com/cli/)



## Installation
- Prerequisites
  - The repo was built and tested on Python 3.7+. Make sure you have python3-pip installed and install the required packages. (Use pip3 if you have Python 2 installed so the system doesn't get confused)
    ```sh
    pip install opencv-python numpy awscli
    ```
  - Tkinter, a Python GUI library, should come with most Python distributions. In case if you don't have Tkinter, you can install it using:
    ```sh
    sudo apt install python3-tk (Ubuntu)
    ```
  - You may need to also pip3 install "requests" if you're on Windows in order to download the yolov3 weights model.
    ```sh
    pip install requests
    ```

- Cloning the Repo
  ```sh
  git clone https://github.com/Dishoungh/martrec.git
  ```
- If you haven't configured your AWS CLI environment to your AWS account, you can either do it manually through the command line:
  ```sh
  aws configure
  ```
  
  Or you can have martrec.py automatically enter your information with keys.py in the config folder.
  ```sh
  AWS_ACCESS_KEY_ID = [Your Access Key ID]
  AWS_SECRET_KEY = [Your Secret Key]
  AWS_REGION_NAME = [Your Region Name]
  AWS_OUTPUT_FORMAT = [Your Default Output Format (usually 'text')]
  ```

## Usage
To ensure martrec is working. Run:
```sh
python martrec.py -h
```
This command pulls up the help menu that gives a list of valid commands to the CLI. An example of this can be viewed in Screenshot (1).

Many of the values for the arguments have defaults. If you are first configuring martrec and would like to start processing images, download the yolov3.weights file if you haven't already by issuing this command:  
```sh
python martrec.py --download-model=True
```
This will send an HTTP request to download the yolov3.weights to the specified config folder. Screenshot (2) demonstrates this functionality.  

To process videos or images, I recommend creating two folders for martrec to find the incoming file to process and to save output files into. By default, the script will look into the folders called "input_data" and "output_data". The script will also generate .csv files inside a folder called "csv_files". Create those folders inside the project folder. Your folders should look like screenshot (3). By default, the repo should provide those folders now. As of this edit, Martrec should automatically process everything in "input_data" folder.
The command to process videos/images:  
```sh
python martrec.py --process=True --option=option
```

This command uses YOLOv3 to process the image or video and outputs image file(s) and every time a truck or car is detected, the script will extract the image as whatever is specified in --output-name. What --option does is specify how the extracted image should be saved. Option is an integer value from 0 to 2. By default, option is 0. Screenshot (4) demonstrates this functionality.
  - 0 = Save Raw Image Only (Doesn't put labeling data into the extracted image)
  - 1 = Save Labeled Image Only (Puts labeling data into the extracted image)
  - 2 = Save Both Raw and Labeled Images  
  
 The command to create an AWS bucket, send extracted images to the specified bucket, and create a .csv file is:  
 ```sh
 python martrec.py --create-bucket=True --bucket-name='awsbucketname' --send-images=True --generate-csv=True
 ```
 
Screenshots (5), (6), (7), (8) all show the functionality of the command. In Screenshot 6, a bucket has been created with the objects in 7. Screenshot 8 shows that the objects' public URLs have been extracted into a .csv file for Mechanical Turk to create HITs. 

## Screenshots
(1) ![Alt text](https://user-images.githubusercontent.com/47036723/106171779-984a7e80-6157-11eb-85ff-f93928a3cd57.png "Help Menu")

(2) ![Alt text](https://user-images.githubusercontent.com/47036723/106180680-3c392780-6162-11eb-816d-ba6b97e5811a.png "Download Model")

(3) ![Alt text](https://user-images.githubusercontent.com/47036723/106174980-30963280-615b-11eb-85bb-0e6d9648c8e3.png "Files")

(4) ![Alt text](https://user-images.githubusercontent.com/47036723/106178013-de571080-615e-11eb-8427-32788d69fc6d.png "Process Video")

(5) ![Alt text](https://user-images.githubusercontent.com/47036723/106178416-5d4c4900-615f-11eb-9016-4a8c9cd03f0f.png "AWS Functionality")

(6) ![Alt text](https://user-images.githubusercontent.com/47036723/106192809-4b27d600-6172-11eb-9670-f1714664341b.png "S3 Console")
    
(7) ![Alt text](https://user-images.githubusercontent.com/47036723/106192816-4e22c680-6172-11eb-8203-d5b16b1bb292.png "Objects in Created Bucket")

(8) ![Alt text](https://user-images.githubusercontent.com/47036723/106179123-36424700-6160-11eb-8000-19eebc6e15f9.png "CSV File")


## Credits
- Most of the code from utils/yolo_utils.py is from the repo: https://github.com/iArunava/YOLOv3-Object-Detection-with-OpenCV


## License
MIT © [Dishoungh]()
