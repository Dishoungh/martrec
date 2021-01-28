## Dishoungh/martrec
A simple python script to automate the process of extracting images of trucks and cars on the road from a video file to uploading extracted images to AWS (Amazon Web Services) S3 to generating a .csv file of the objects' URLs for Mechanical Turk.

Crowdsourcing processes can be tedious to setup. You'll have to upload the data somewhere and grab their URLs individually and compile them into a .csv file for Mechanical Turk to create HITs (Human Intelligence Tasks). This can take a while. The purpose of this repo is to automate most of that process and can be applied to applied to multiple applications.

 
## Screenshots


## Tech/Framework Used

<b>Built with</b>
- [YOLOv3](https://pjreddie.com/darknet/yolo/)
- [AWS CLI](https://aws.amazon.com/cli/)



## Installation
Provide step by step series of examples and explanations about how to get a development env running.




## Credits
- Most of the code from utils/yolo_utils.py is from the repo: https://github.com/iArunava/YOLOv3-Object-Detection-with-OpenCV


## License

MIT © [Dishoungh]()
