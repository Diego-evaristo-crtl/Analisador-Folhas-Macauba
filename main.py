import tkinter as tk
from PIL import Image
from collections import Counter
import os
from colorsys import rgb_to_hls

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # set's 2 rows and 2 columns for dashboard interface
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)
 
        self.Frame_middle = tk.Frame(self)
        self.Frame_r = tk.Frame(self.Frame_middle)
        self.Frame_l = tk.Frame(self.Frame_middle)

        # stats for the percentage of contaminated and non-contaminated parts
        self.stats = Counter()
        self.stats['good'] = 0
        self.stats['bad'] = 0

        # saves the imgs to show them
        self.imgs = []
        
        # creates entries and vars to get filename, dictpath, 
        # buttons to show images, and labels to output results 
        self.FileVar = tk.StringVar()

        # gets file name
        self.FileEnt = tk.Entry(self.Frame_r, 
                                    textvariable=self.FileVar,
                                    width=45)
        
        self.DirVar = tk.StringVar()

        # get dictionary location
        self.DirEnt = tk.Entry(self.Frame_r,
                                textvariable=self.DirVar,
                                width=45)
        
        self.sizeVar = tk.StringVar()
        self.sizeEnt = tk.Entry(self.Frame_r,
                                 textvariable=self.sizeVar,
                                 width=15)
        
        # showcase, respectivily, wich parts aren't and are 'contaminated'
        self.LabelGdVar = tk.StringVar(value='')
        self.LabelGd = tk.Label(self.Frame_l, 
                                 textvariable=self.LabelGdVar,
                                 width=20)
        self.LabelBdVar = tk.StringVar(value='')
        self.LabelBd = tk.Label(self.Frame_l, 
                                 textvariable=self.LabelBdVar,
                                 width=20) 
        self.LabelSifVar = tk.StringVar(value='')
        self.LabelSif = tk.Label(self.Frame_l,
                                 textvariable=self.LabelSifVar,
                                 width=25)
        self.LabelSidVar = tk.StringVar(value='')
        self.LabelSid = tk.Label(self.Frame_l,
                                  textvariable=self.LabelSidVar,
                                  width=25)
               
            # button that scans the images
        scanButton = tk.Button(self.Frame_r, 
                                text='scanear imagem', 
                                command=lambda: self.scan(self.DirEnt.get(), self.FileEnt.get()))
            # button that shows the image and it's map
        showButton = tk.Button(self.Frame_l, 
                                text='mostrar imagem',
                                command=lambda: self.showImg())
        
        
        self.infoF2Var = tk.StringVar(value='pasta/arquivo/proporções(altura,comprimento) abaixo:')
        infoF2 = tk.Label(self.Frame_r, 
                           textvariable=self.infoF2Var, 
                           width=45)

            # bind's enter shortcut for scanning
        self.FileEnt.bind('<Return>', func=lambda _: self.scan(self.DirEnt.get(),
                                                               self.FileEnt.get()))
        self.DirEnt.bind('<Return>', func=lambda _: self.scan(self.DirEnt.get(),
                                                              self.FileEnt.get()))
        self.sizeEnt.bind('<Return>', func=lambda _: self.scan(self.DirEnt.get(),
                                                               self.FileEnt.get()))

            # packs all the frame2 widgets, aka the interactive ones.
        infoF2.pack(pady=5, padx=5, side='top', expand=False)
        self.DirEnt.pack(pady=5, padx=5, side='top', expand=False)
        self.FileEnt.pack(pady=5, padx=5, side='top', expand=False)
        self.sizeEnt.pack(pady=5, padx=5, side='top', expand=False)
        
        self.LabelSif.pack(pady=5, padx=5, side='top', expand=False)
        self.LabelSid.pack(pady=5, padx=5, side='top', expand=False)
        self.LabelGd.pack(pady=5, padx=5, side='top', expand=False)
        self.LabelBd.pack(pady=5, padx=5, side='top', expand=False)
        showButton.pack(pady=5, padx=3, side='top', expand=False)
        scanButton.pack(pady=5, padx=3, side='top', expand=False)
        
        self.Frame_r.pack(pady=5, side='right')
        self.Frame_l.pack(pady=5, side='left')
        self.Frame_middle.place(relx=0.5, rely=0.5, anchor="center")

        self.bind('<Return>', func=lambda _: self.scan(self.DirEnt.get(), self.FileEnt.get()))
    
    
    
    def percent(self):
        percentages = {'good':0, 'bad':0}
        for key, value in self.stats.items():
            percentages[key] = (value/self.stats.total()) * 100
        return percentages
       
    # scans the photos
    def scan(self, dirpath, filename):
            # get's path and tests if it is valid
        path = os.path.join(dirpath, filename)
        if not os.path.exists(path) and os.path.isfile(path):
            return           
        
            # creates opens image and creates img map
        try:
            img = Image.open(path)
        except:
            return
        imgMap = Image.new(img.mode, img.size)
            
            # scans image to fill the img map
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                
                pixel = img.getpixel((x, y)) # get's pixel (RGB)
                try: 
                    hsl_pixel = rgb_to_hls(pixel[0], pixel[1], pixel[2]) # get's pixel (HSL)
                        
                        # good
                    if pixel[1] > pixel[0]-10 and pixel[1] > pixel[2]-10 and hsl_pixel[0] < 150: 
                        self.stats['good'] += 1
                        imgMap.putpixel((x,y), value=(0,255,0))
                    
                    elif pixel[0] > pixel[1] and pixel[0] > pixel[2]:
                            self.stats['bad'] += 1
                            imgMap.putpixel((x,y), value=(255,0,0))
                    else: # none
                        imgMap.putpixel((x,y), value=(0,0,255))
                except (ZeroDivisionError, ValueError):
                        # none   
                    imgMap.putpixel((x,y), value=(0,0,255))
                
    
            # gives statistics
        percentages = self.percent()
        self.LabelGdVar.set('bom: '+str(percentages['good'])[:6]+'%')
        self.LabelBdVar.set('ruim: '+str(percentages['bad'])[:6]+'%')
        
            # calculates and show's size proportions
        size = img.size[0]*img.size[1]
        proportions = self.sizeVar.get().split(',')
        try:
            tamanho_bom = (self.stats['good']/size)*float(proportions[0])
            tamanho_ruim = (self.stats['bad']/size)*float(proportions[1])
            self.LabelSifVar.set(f"tamanho folha: {str(tamanho_bom)[:7]}")
            self.LabelSidVar.set(f"tamanho doença: {str(tamanho_ruim)[:7]}")
        
        except ValueError:
            self.LabelSifVar.set('')
            self.LabelSidVar.set('')
            
            # set's all the image stats to 0, so a new image may be processed
        self.stats['good'] = 0
        self.stats['bad'] = 0
        
            # saves the images to be used when 'show' button is triggered
        self.imgs = [img, imgMap]
       
    # shows the last processed images
    def showImg(self):
        try:
            self.imgs[0].show()
            self.imgs[1].show()
        except IndexError:
            pass
        
    # runs the program   
root = App()
try:
    root.mainloop()
except KeyboardInterrupt:
    exit()
