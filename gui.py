from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from utils.martrec_utils import download_model
from utils.yolo_utils import *
from utils.aws_utils import *
import os

def help():
	helpWin = Toplevel()
	helpWin.title("Help Menu")
	helpText = Text(helpWin, wrap="word", width=150, height=20)
	helpText.pack()
	text = """There are two segments in the GUI: YOLO and AWS.
		YOLO:
			Process: Set 'yes' if you wish to process a video or image with YOLO
			Image or Video: Specifies to martrec if the incoming data is a video file or image file
	   		Path: Specifies location of the incoming data
 			Delay Time: An integer value between 1 and 1000 that specifies the number of frames to skip during process. 
   			Extraction Option: An integer value between 0 and 3 that specifies how you want the output data to be saved. 
   				0 means save raw images. 
   				1 means save labeled images. 
   				2 means save both raw and labeled. 
   				3 means save no images (useful if you wish to only save a video)
			Output Name: Specifies the name of the output during processing
   			Save Video: Specifies if you wish to save an output video with labeled images from processing
		   
   		AWS:
   			Configure AWS: Set 'yes' if you wish to configures awscli to your account profile
   			Create Bucket: Set 'yes' if you wish to create a new AWS bucket
   			Bucket Name: Specifies bucket name for creation or editing
   			Send Data: Set 'yes' if you wish to send the output data to the specified AWS bucket
   			Generate CSV: Set 'yes' if you wish to generate CSV file from objects in the bucket"""

	helpText.insert("1.0", text)
	okButton = Button(helpWin, text="Ok", command=helpWin.destroy).pack()							 



def start(processVar, videoorimgVar, filename, delayVar, optionVar, nameVar, saveVideoVar, configureVar, createBucketVar, bucketVar, sendDataVar, generateCSVVar):
	if (processVar == 1):
		if (videoorimgVar == 1): # Image
			if ('.png' not in filename) or ('.jpeg' not in filename):
				message.showerror("Invalid File Extension for Image", "You've chosen to process a file that isn't a .png or .jpeg file.")
				return
			else:
				print("Process Image")
		else: # Video
			if ('.mp4' not in filename):
				message.showerror("Invalid File Extension for Video", "You've chosen to process a file that isn't a .mp4 for video processing.")
				return
			else:
				if ((delayVar < 1) or (delayVar > 1000)) and (delayVar is not None):
					message.showerror("Invalid Delay Setting", "The value for 'delay' is not between 1 and 1000.")
					return
				elif ((optionVar < 0) or (optionVar > 3)) and (optionVar is not None):
					message.showerror("Invalid Image Extraction Option Setting", "The value for 'option' is not between 0 and 3.")
					return
				else:
					print("Process Video")
			

	
	if ((bucketVar is None) and ((createBucketVar == 1) or (sendDataVar == 1) or (generateCSVVar == 1))):			
		message.showerror("Unspecified Bucket Name", "You must specify a bucket name for AWS to apply the commands")
		return
	else:
		print("Execute Stuff")

def browse():
    filename = filedialog.askopenfilename(initialdir="./", title="Select a File")
    pathText.delete(1.0, END)
    pathText.insert(END, filename)
    return

root = Tk()
root.eval('tk::PlaceWindow . center')
root.title("Martrec")
root.geometry("860x420")
root.resizable(0,0)

icon = PhotoImage(file = './icon.ico')
root.iconphoto(False, icon)

welcomeLabel = Label(root, text="Welcome to the Martrec GUI!")
welcomeLabel.grid(row=0, column=2)

####### YOLO Configuration #######
yoloLabel = Label(root, text="YOLO Configuration")
yoloLabel.grid(row=1, column=0)

processLabel = Label(root, text="Process?: ")
processLabel.grid(row=2, column=1)
processVar = IntVar()
processYesRadioButton = Radiobutton(root, text="Yes", variable=processVar, value=1)
processYesRadioButton.grid(row=2, column=3)
processNoRadioButton  = Radiobutton(root, text="No", variable=processVar, value=0)
processNoRadioButton.grid(row=2, column=4)

videoorimgLabel = Label(root, text="Image or Video?: ")
videoorimgLabel.grid(row=3, column=1)
videoorimgVar = IntVar()
videoimgImageRadioButton = Radiobutton(root, text="Image", variable=videoorimgVar, value=1)
videoimgImageRadioButton.grid(row=3, column=3)
videoimgVideoRadioButton = Radiobutton(root, text="Video", variable=videoorimgVar, value=0)
videoimgVideoRadioButton.grid(row=3, column=4)

filename = StringVar()
pathLabel = Label(root, text="Path: ")
pathLabel.grid(row=4, column=1)
pathText = Text(root, height=1, width=50)
pathText.grid(row=4, column=2)
pathButton = Button(root, text="...", command=lambda:browse())
pathButton.grid(row=4, column=3)

delayLabel = Label(root, text="Delay Time [1-1000]: ")
delayLabel.grid(row=5, column=1)
delayEntry = Entry(root, width=5)
delayEntry.grid(row=5, column=3)
delayVar = delayEntry.get()

optionLabel = Label(root, text="Extraction Option [0-3]: ")
optionLabel.grid(row=6, column=1)
optionEntry = Entry(root, width=5)
optionEntry.grid(row=6, column=3)
optionVar = optionEntry.get()

nameLabel = Label(root, text="Output Name: ")
nameLabel.grid(row=7, column=1)
nameEntry = Entry(root, width=5)
nameEntry.grid(row=7, column=3)
nameVar = nameEntry.get()

saveVideoLabel = Label(root, text="Save Video?: ")
saveVideoLabel.grid(row=8, column=1)
saveVideoVar = IntVar()
saveVideoYesRadioButton = Radiobutton(root, text="Yes", variable=saveVideoVar, value=1)
saveVideoYesRadioButton.grid(row=8, column=3)
saveVideoNoRadioButton  = Radiobutton(root, text="No", variable=saveVideoVar, value=0)
saveVideoNoRadioButton.grid(row=8, column=4)


#######  AWS Configuration #######
awsLabel = Label(root, text="AWS Configuration")
awsLabel.grid(row=9, column=0)

configureLabel = Label(root, text="Configure AWS?: ")
configureLabel.grid(row=10, column=1)
configureVar = IntVar()
configureYesRadioButton = Radiobutton(root, text="Yes", variable=configureVar, value=1)
configureYesRadioButton.grid(row=10, column=3)
configureNoRadioButton  = Radiobutton(root, text="No", variable=configureVar, value=0)
configureNoRadioButton.grid(row=10, column=4)

createBucketLabel = Label(root, text="Create Bucket?: ")
createBucketLabel.grid(row=11, column=1)
createBucketVar = IntVar()
createBucketYesRadioButton = Radiobutton(root, text="Yes", variable=createBucketVar, value=1)
createBucketYesRadioButton.grid(row=11, column=3)
createBucketNoRadioButton  = Radiobutton(root, text="No", variable=createBucketVar, value=0)
createBucketNoRadioButton.grid(row=11, column=4)

bucketLabel = Label(root, text="Bucket Name: ")
bucketLabel.grid(row=12, column=1)
bucketEntry = Entry(root, width=5)
bucketEntry.grid(row=12, column=3)
bucketVar = bucketEntry.get()

sendDataLabel = Label(root, text="Send Data?: ")
sendDataLabel.grid(row=13, column=1)
sendDataVar = IntVar()
sendDataYesRadioButton = Radiobutton(root, text="Yes", variable=sendDataVar, value=1)
sendDataYesRadioButton.grid(row=13, column=3)
sendDataNoRadioButton  = Radiobutton(root, text="No", variable=sendDataVar, value=0)
sendDataNoRadioButton.grid(row=13, column=4)

generateCSVLabel = Label(root, text="Generate CSV?: ")
generateCSVLabel.grid(row=14, column=1)
generateCSVVar = IntVar()
generateCSVYesRadioButton = Radiobutton(root, text="Yes", variable=generateCSVVar, value=1)
generateCSVYesRadioButton.grid(row=14, column=3)
generateCSVNoRadioButton  = Radiobutton(root, text="No", variable=generateCSVVar, value=0)
generateCSVNoRadioButton.grid(row=14, column=4)

######## Bottom Buttons ##########
pathButton = Button(root, text="Start", command=lambda:start(processVar, videoorimgVar, filename, delayVar, optionVar, nameVar, saveVideoVar, configureVar, createBucketVar, bucketVar, sendDataVar, generateCSVVar))
pathButton.grid(row=15, column=2)

pathButton = Button(root, text="Help", command=lambda:help())
pathButton.grid(row=16, column=2)

root.mainloop()
