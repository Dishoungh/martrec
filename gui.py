import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, ttk 
import utils.martrec_utils
from utils.yolo_utils import *
from utils.aws_utils import *

class Application:
	def __init__(self, window):
		self.window = window
		self.initialize()
		self.create_widgets()
		
	def initialize(self):
		# Master Window
		self.window.eval('tk::PlaceWindow . center')
		self.window.title("Martrec")
		self.window.geometry("860x420")
		self.window.resizable(0,0)
		
		# Icon
		self.icon = PhotoImage(file = './icon.ico')
		self.window.iconphoto(False, self.icon)
        	
	def create_widgets(self):
		# Variables #
		self.processVar      = IntVar()
		self.videoorimgVar   = IntVar()
		self.saveVideoVar    = IntVar()
		self.configureVar    = IntVar()
		self.createBucketVar = IntVar()
		self.sendDataVar     = IntVar()
		self.generateCSVVar  = IntVar()
		
		######### Welcome Label ##########
		self.welcomeLabel = Label(self.window, text="Welcome to the Martrec GUI!")
		self.welcomeLabel.grid(row=0, column=2)
		    
		####### YOLO Configuration #######
		self.yoloLabel = Label(self.window, text="YOLO Configuration")
		self.yoloLabel.grid(row=1, column=0)
		    
		self.processLabel = Label(self.window, text="Process?: ")
		self.processLabel.grid(row=2, column=1)
		self.processYesRadioButton = Radiobutton(self.window,
	                                             text="Yes",
	                                             variable=self.processVar,
	                                             value=1)
		self.processYesRadioButton.grid(row=2, column=3)
		self.processNoRadioButton = Radiobutton(self.window,
	                                            text="No",
	                                            variable=self.processVar,
	                                            value=0)
		self.processNoRadioButton.grid(row=2, column=4)
		    
		self.videoorimgLabel = Label(self.window, text="Image or Video?: ")
		self.videoorimgLabel.grid(row=3, column=1)
		self.videoimgImageRadioButton = Radiobutton(self.window,
													text="Image",
													variable=self.videoorimgVar,
													value=1)
		self.videoimgImageRadioButton.grid(row=3, column=3)
		self.videoimgVideoRadioButton = Radiobutton(self.window, 
													text="Video", 
													variable=self.videoorimgVar, 
													value=0)
		self.videoimgVideoRadioButton.grid(row=3, column=4)
		            
		self.pathLabel = Label(self.window, text="Path: ")
		self.pathLabel.grid(row=4, column=1)
		self.pathText = Text(self.window, height=1, width=50)
		self.pathText.grid(row=4, column=2)
		self.pathButton = Button(self.window, text="...", command=lambda:self.browse())
		self.pathButton.grid(row=4, column=3)

		#self.delayLabel = Label(self.window, text="Delay Time [1-1000]: ")
		#self.delayLabel.grid(row=5, column=1)
		#self.delayEntry = Entry(self.window, width=5)
		#self.delayEntry.grid(row=5, column=3)
		    
		#self.optionLabel = Label(self.window, text="Extraction Option [0-3]: ")
		#self.optionLabel.grid(row=6, column=1)
		#self.optionEntry = Entry(self.window, width=5)
		#self.optionEntry.grid(row=6, column=3)
		    
		self.nameLabel = Label(self.window, text="Output Name: ")
		self.nameLabel.grid(row=7, column=1)
		self.nameEntry = Entry(self.window, width=15)
		self.nameEntry.grid(row=7, column=3)

		self.saveVideoLabel = Label(self.window, text="Save Video?: ")
		self.saveVideoLabel.grid(row=8, column=1)
		self.saveVideoYesRadioButton = Radiobutton(self.window,
												   text="Yes",
												   variable=self.saveVideoVar,
												   value=1)
		self.saveVideoYesRadioButton.grid(row=8, column=3)
		self.saveVideoNoRadioButton = Radiobutton(self.window,
												  text="No",
												  variable=self.saveVideoVar,
												  value=0)
		self.saveVideoNoRadioButton.grid(row=8, column=4)


		#######  AWS Configuration #######
		self.awsLabel = Label(self.window, text="AWS Configuration")
		self.awsLabel.grid(row=9, column=0)

		self.configureLabel = Label(self.window, text="Configure AWS?: ")
		self.configureLabel.grid(row=10, column=1)
		self.configureYesRadioButton = Radiobutton(self.window,
												   text="Yes",
												   variable=self.configureVar,
												   value=1)
		self.configureYesRadioButton.grid(row=10, column=3)
		self.configureNoRadioButton = Radiobutton(self.window,
												  text="No",
												  variable=self.configureVar,
												  value=0)
		self.configureNoRadioButton.grid(row=10, column=4)

		self.createBucketLabel = Label(self.window, text="Create Bucket?: ")
		self.createBucketLabel.grid(row=11, column=1)
		self.createBucketYesRadioButton = Radiobutton(self.window,
													  text="Yes",
													  variable=self.createBucketVar,
													  value=1)
		self.createBucketYesRadioButton.grid(row=11, column=3)
		self.createBucketNoRadioButton = Radiobutton(self.window,
												     text="No",
												     variable=self.createBucketVar,
												     value=0)
		self.createBucketNoRadioButton.grid(row=11, column=4)

		self.bucketLabel = Label(self.window, text="Bucket Name: ")
		self.bucketLabel.grid(row=12, column=1)
		self.bucketEntry = Entry(self.window, width=15)
		self.bucketEntry.grid(row=12, column=3)

		self.sendDataLabel = Label(self.window, text="Send Data?: ")
		self.sendDataLabel.grid(row=13, column=1)
		self.sendDataYesRadioButton = Radiobutton(self.window,
												  text="Yes",
												  variable=self.sendDataVar,
												  value=1)
		self.sendDataYesRadioButton.grid(row=13, column=3)
		self.sendDataNoRadioButton  = Radiobutton(self.window,
												  text="No",
												  variable=self.sendDataVar,
												  value=0)
		self.sendDataNoRadioButton.grid(row=13, column=4)

		self.generateCSVLabel = Label(self.window, text="Generate CSV?: ")
		self.generateCSVLabel.grid(row=14, column=1)
		self.generateCSVYesRadioButton = Radiobutton(self.window,
													 text="Yes",
													 variable=self.generateCSVVar,
													 value=1)
		self.generateCSVYesRadioButton.grid(row=14, column=3)
		self.generateCSVNoRadioButton  = Radiobutton(self.window,
													 text="No",
													 variable=self.generateCSVVar,
													 value=0)
		self.generateCSVNoRadioButton.grid(row=14, column=4)

		######## Bottom Buttons ##########
		self.pathButton = Button(self.window, text="Start", command=lambda:self.execute())
		self.pathButton.grid(row=15, column=2)

		self.pathButton = Button(self.window, text="Help", command=lambda:self.help())
		self.pathButton.grid(row=16, column=2)


	def browse(self):
		filename = filedialog.askopenfilename(initialdir="./", title="Select a File")
		self.pathText.delete(1.0, END)
		self.pathText.insert(END, filename)
		return
		
	def help(self):
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

	def execute(self):
		processflag = self.processVar.get()
		vidimg      = self.videoorimgVar.get()
		filename    = self.pathText.get("1.0", 'end-1c')
		outname     = self.nameEntry.get()
		savevid     = self.saveVideoVar.get()
		config      = self.configureVar.get()
		createbuck  = self.createBucketVar.get()
		buckname    = self.bucketEntry.get()
		senddata    = self.sendDataVar.get()
		gencsv      = self.generateCSVVar.get()

		if outname is None:
			outname = utils.martrec_utils.DEFAULT_YOLO_OUTPUT_NAME_SETTING

		if (processflag == 1): 											# Use YOLOv3
			if (vidimg == 1): 										# Image
				if ('.png' not in filename) and ('.jpeg' not in filename):
					messagebox.showerror("Invalid File Extension for Image", "You've chosen to process a file that isn't a .png or .jpeg file.")
					return
				else:
					try:
						labels, colors, net, layer_names = init(labelfile=utils.martrec_utils.DEFAULT_YOLO_LABELS_SETTING,
																config=utils.martrec_utils.DEFAULT_YOLO_CONFIG_SETTING,
																weights=utils.martrec_utils.DEFAULT_YOLO_WEIGHTS_SETTING)

						process(image_path=filename,
								video_path=None,
								output_name=outname,
								save_path=utils.martrec_utils.DEFAULT_YOLO_SAVE_PATH_SETTING,
								delay_time=utils.martrec_utils.DEFAULT_YOLO_DELAY_TIME_SETTING,
								save_video=utils.martrec_utils.DEFAULT_YOLO_SAVE_VIDEO_SETTING,
								option=utils.martrec_utils.DEFAULT_YOLO_IMAGE_EXTRACTION_SETTING,
								video_output_path=utils.martrec_utils.DEFAULT_YOLO_VIDEO_OUTPUT_PATH,
								confidence=utils.martrec_utils.DEFAULT_YOLO_CONFIDENCE_SETTING,
								threshold=utils.martrec_utils.DEFAULT_YOLO_THRESHOLD_SETTING,
								labels=labels,
								colors=colors,
								net=net,
								layer_names=layer_names,
								gui=False,
								gui_obj=None)

						messagebox.showinfo("Success", "Image Processing Success")
					except Exception as err:
						messagebox.showerror("Image Processing Error", err)
			else:												# Video
				if ('.mp4' not in filename) and ('.avi' not in filename):
					messagebox.showerror("Invalid File Extension for Video", "You've chosen to process a file that isn't a .mp4 for video processing.")
					return
				else:
					####### Progress Bar ######
					self.bar = ttk.Progressbar(self.window,
											   orient=HORIZONTAL,
											   length=200,
											   mode='determinate')
					self.bar.grid(row=18, column=2)
					try:
						labels, colors, net, layer_names = init(labelfile=utils.martrec_utils.DEFAULT_YOLO_LABELS_SETTING,
																config=utils.martrec_utils.DEFAULT_YOLO_CONFIG_SETTING,
																weights=utils.martrec_utils.DEFAULT_YOLO_WEIGHTS_SETTING)
						if savevid == 0:
							process(image_path=None,
									video_path=filename,
									output_name=outname,
									save_path=utils.martrec_utils.DEFAULT_YOLO_SAVE_PATH_SETTING,
									delay_time=utils.martrec_utils.DEFAULT_YOLO_DELAY_TIME_SETTING,
									save_video=utils.martrec_utils.DEFAULT_YOLO_SAVE_VIDEO_SETTING,
									option=utils.martrec_utils.DEFAULT_YOLO_IMAGE_EXTRACTION_SETTING,
									video_output_path=utils.martrec_utils.DEFAULT_YOLO_VIDEO_OUTPUT_PATH,
									confidence=utils.martrec_utils.DEFAULT_YOLO_CONFIDENCE_SETTING,
									threshold=utils.martrec_utils.DEFAULT_YOLO_THRESHOLD_SETTING,
									labels=labels,
									colors=colors,
									net=net,
									layer_names=layer_names,
									gui=True,
									gui_obj=self)
						else:
							process(image_path=None,
									video_path=filename,
									output_name=outname,
									save_path=utils.martrec_utils.DEFAULT_YOLO_SAVE_PATH_SETTING,
									delay_time=utils.martrec_utils.DEFAULT_YOLO_DELAY_TIME_SETTING,
									save_video=True,
									option=utils.martrec_utils.DEFAULT_YOLO_IMAGE_EXTRACTION_SETTING,
									video_output_path=utils.martrec_utils.DEFAULT_YOLO_VIDEO_OUTPUT_PATH,
									confidence=utils.martrec_utils.DEFAULT_YOLO_CONFIDENCE_SETTING,
									threshold=utils.martrec_utils.DEFAULT_YOLO_THRESHOLD_SETTING,
									labels=labels,
									colors=colors,
									net=net,
									layer_names=layer_names,
									gui=True,
									gui_obj=self)

							messagebox.showinfo("Success", "Video Processing Success")
					except Exception as err:
						messagebox.showerror("Video Processing Error", err)
					self.bar.grid_forget()
		if (config == 1):
			try:
				configure_aws()
				messagebox.showinfo("Success", "AWS Configuration Success")
			except Exception as err:
				messagebox.showerror("AWS Configuration Error", err)

		if ((buckname is None) and ((createbuck == 1) or (senddata == 1) or (gencsv == 1))):
			messagebox.showerror("Unspecified Bucket Name",
						 		 "You must specify a bucket name for AWS to apply the commands")
			return
		else:
			try:
				if (createbuck == 1):
					create_bucket(buckname)
					set_cors(buckname, utils.martrec_utils.DEFAULT_AWS_CORS_FILE_SETTING)
					messagebox.showinfo("Success", "AWS Bucket Creation Success")
				elif (senddata == 1):
						send_to_s3(utils.martrec_utils.DEFAULT_YOLO_SAVE_PATH_SETTING, buckname)
						messagebox.showinfo("Success", "Data Sent to AWS Bucket")
				elif (gencsv == 1):
					get_csv(utils.martrec_utils.DEFAULT_AWS_CSV_FILE_SETTING, buckname)
					messagebox.showinfo("Success", "CSV Generated")
			except Exception as err:
				messagebox.showerror("AWS Function Error", err)

		if (processflag == 0) and ((buckname is None) or ((createbuck == 0) and (senddata == 0) and (gencsv == 0))):
			messagebox.showerror("Nothing Done",
					 			 "You chose not to process a video/image nor use any AWS functions.")

		return


def main():
    root = tk.Tk()
    gui = Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()
