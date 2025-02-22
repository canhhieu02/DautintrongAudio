from tkinter import *
import pygame
from tkinter import filedialog
from tkinter.ttk import *
import base64
from tkinter import messagebox

from AudioStegnographyAlgo.LSBAudioStego import LSBAudioStego
from AudioStegnographyAlgo.PhaseEncodingAudioStego import PhaseEncodingAudioStego

root = Tk()

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.fileSelected = ""
        self.fileSelectedForDecode = ""

    def init_window(self):
        self.master.title("Audio Steganography - Nhóm 08")
        self.pack(fill=BOTH, expand=1)
        self.drawEncoding()
        self.drawDecoding()

    def drawEncoding(self):
        self.encodeVar = StringVar()
        self.encodelabel = Label(root, textvariable=self.encodeVar)
        self.encodelabel.place(x=10, y=10)
        self.encodeVar.set("Encoding ")

        self.optionsVar = StringVar()
        self.optionsVar.set("Choose method")

        self.encodingOptionsMenu = OptionMenu(root, self.optionsVar, "Choose method", "Phase Coding","Least Significant Bit")
        self.encodingOptionsMenu.place(x=5, y=50)

        self.selectFileButton = Button(self, text="Select File  To Encode", command=self.selectFile)
        self.selectFileButton.place(x=10, y=100)

        self.var = StringVar()
        self.label = Label(root, textvariable=self.var, relief=RAISED)
        self.label.place(x=10, y=140)

        self.entryText = Entry(root, width=50)
        self.entryText.place(x=10, y=180)
        self.entryText.insert(0, "Enter String to encode ")

        self.encodeButton = Button(self, text="Encode", command=self.encode)
        self.encodeButton.place(x=10, y=220)

        self.enocdedLocation = StringVar()
        self.locationOfEncodeFile = Label(root, textvariable=self.enocdedLocation)
        self.locationOfEncodeFile.place(x=10, y=260)


    def drawDecoding(self):
        self.decodeVar = StringVar()
        self.decodelabel = Label(root, textvariable=self.decodeVar)
        self.decodelabel.place(x=410, y=10)
        self.decodeVar.set("Decoding ")

        self.decodeOptionsVar = StringVar()
        self.decodeOptionsVar.set("Choose method")

        self.decodingOptionsMenu = OptionMenu(root, self.decodeOptionsVar, "Choose method", "Least Significant Bit", "Phase Coding")
        self.decodingOptionsMenu.place(x=405, y=50)

        self.selectFileDecodeButton = Button(self, text="Select  File To Decode ", command=self.selectFileDecode)
        self.selectFileDecodeButton.place(x=410, y=100)

        self.decodeFileVar = StringVar()
        self.decodeFileLabel = Label(root, textvariable=self.decodeFileVar, relief=RAISED)
        self.decodeFileLabel.place(x=410, y=140)

        self.decodeButton = Button(self, text="Decode", command=self.decode)
        self.decodeButton.place(x=410, y=200)

        self.decodedString = StringVar()
        self.decodedStringlabel = Label(root, textvariable=self.decodedString, font=(None, 10))
        self.decodedStringlabel.place(x=410, y=250)

    # textvariable=self.decodedString

    def client_exit(self):
        exit()

    def selectFile(self):
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("jpeg files", "*.wav"), ("all files", "*.*")))
        self.fileSelected = root.filename
        self.var.set(root.filename)

    def selectFileDecode(self):
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("jpeg files", "*.wav"), ("all files", "*.*")))
        self.fileSelectedForDecode = root.filename
        self.decodeFileVar.set(root.filename)

    def encode(self):
        if self.optionsVar.get() == "Least Significant Bit":
            algo = LSBAudioStego()
        elif self.optionsVar.get() == "Phase Coding":
            algo = PhaseEncodingAudioStego()
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn một phương pháp giấu tin.")
            return
        
        if self.fileSelected:
            encoded_data1 = self.ma_hoa_tieng_viet(self.entryText.get())
            result = algo.encodeAudio(self.fileSelected, encoded_data1)
            self.enocdedLocation.set(result)
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn một tệp âm thanh để giấu tin.")

    def decode(self):
        if self.decodeOptionsVar.get() == "Least Significant Bit":
            algo = LSBAudioStego()
        elif self.decodeOptionsVar.get() == "Phase Coding":
            algo = PhaseEncodingAudioStego()
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn một phương pháp tách tin.")
            return

        if self.fileSelectedForDecode:
            result = algo.decodeAudio(self.fileSelectedForDecode)
            self.decodedString.set(result)
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn một tệp âm thanh để tách tin.")


    def ma_hoa_tieng_viet(self, text):
        encoded_bytes = text.encode('utf-8')
        encoded_text = base64.b64encode(encoded_bytes)
        return encoded_text.decode('utf-8')
    
    def play_audio(self, audio_file):
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play(-1)  # Loop indefinitely

    def stop_audio(self):
        pygame.mixer.music.stop()

# resolution
root.geometry("800x500")
app = Window(root)

# Initialize pygame mixer
pygame.mixer.init()

play_button = Button(root, text="Start", command=lambda: app.play_audio(app.fileSelected))
play_button.place(x=10, y=300)

stop_button = Button(root, text="Stop", command=app.stop_audio)
stop_button.place(x=100, y=300)

play_button = Button(root, text="Start", command=lambda: app.play_audio(app.fileSelectedForDecode))
play_button.place(x=410, y=300)

stop_button = Button(root, text="Stop", command=app.stop_audio)
stop_button.place(x=500, y=300)

root.mainloop()
