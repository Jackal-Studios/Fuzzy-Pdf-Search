# # # from fuzzysearch import find_near_matches
# # # sequence = '''тири пири в нас нема однорідної матриці'''
# # # subsequence = 'однорідна матриця' # distance = 1
# # # print(find_near_matches(subsequence, sequence, max_l_dist=4))
# # import PyPDF2
# # from tkinter import *
# # from tkinter import filedialog
# # from tkPDFViewer import tkPDFViewer as pdf
# # #Create an instance of tkinter frame
# # win= Tk()
# # #Set the Geometry
# # win.geometry("750x450")
# # #Create a Text Box
# # text= Text(win,width= 80,height=30)
# # text.pack(pady=20)
# # #Define a function to clear the text
# # def clear_text():
# #    text.delete(1.0, END)
# # #Define a function to open the pdf file
# # def open_pdf():
# #    file= filedialog.askopenfilename(title="Select a PDF", filetype=(("PDF    Files","*.pdf"),("All Files","*.*")))
# #    if file:
# #       #print(file)   path to pdf
# #       #Open the PDF File
# #       pdf_file= PyPDF2.PdfFileReader(file)
# #       #Select a Page to read
# #       page= pdf_file.getPage(0)
# #       #Get the content of the Page
# #       content=page.extractText()
# #       #Add the content to TextBox
# #       text.insert(1.0,content)
# #
# # #Define function to Quit the window
# # def quit_app():
# #    win.destroy()
# # #Create a Menu
# # my_menu= Menu(win)
# # win.config(menu=my_menu)
# # #Add dropdown to the Menus
# # file_menu=Menu(my_menu,tearoff=False)
# # my_menu.add_cascade(label="File",menu= file_menu)
# # file_menu.add_command(label="Open",command=open_pdf)
# # file_menu.add_command(label="Clear",command=clear_text)
# # file_menu.add_command(label="Quit",command=quit_app)
# # win.mainloop()
# ##################################
#
# # import os
# # from tkinter import *
# #
# # # Importing tkPDFViewer to place pdf file in gui.
# # # In tkPDFViewer library there is
# # # an tkPDFViewer module. That I have imported as pdf
# # from tkPDFViewer import tkPDFViewer as pdf
# # # Initializing tk
# # root = Tk()
# #
# # # Set the width and height of our root window.
# # root.geometry("550x750")
# #
# # # creating object of ShowPdf from tkPDFViewer.
# # v1 = pdf.ShowPdf()
# #
# # # Adding pdf location and width and height.
# # v2 = v1.pdf_view(root,
# #                  pdf_location=r"E:\PythonProjects\Fuzzy-Pdf-Search\pure_electron\my-electron-app\testpdf.pdf",
# #                  width=100, height=100)
# #
# # # Placing Pdf in my gui.
# # v2.pack()
# # root.mainloop()
# ##################################
# path="E:\PythonProjects\Fuzzy-Pdf-Search\pure_electron\my-electron-app\\testpdf.pdf"
#
#
#
#
#
# import fitz
# from PIL import Image
# from tkinter import *
# from PIL import Image,ImageTk
# import tkinter
# import ctypes
# user32 = ctypes.windll.user32
# screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
# print(screensize)
# class ScrollableImage(tkinter.Frame):
#    def __init__(self, master=None, **kw):
#       self.image = kw.pop('image', None)
#       sw = kw.pop('scrollbarwidth', 10)
#       super(ScrollableImage, self).__init__(master=master, **kw)
#       self.cnvs = tkinter.Canvas(self, highlightthickness=0, **kw)
#       self.cnvs.create_image(0, 0, anchor='nw', image=self.image)
#       # Vertical and Horizontal scrollbars
#       self.v_scroll = tkinter.Scrollbar(self, orient='vertical', width=sw)
#       self.h_scroll = tkinter.Scrollbar(self, orient='horizontal', width=sw)
#       # Grid and configure weight.
#       self.cnvs.grid(row=0, column=0, sticky='nsew')
#       self.h_scroll.grid(row=1, column=0, sticky='ew')
#       self.v_scroll.grid(row=0, column=1, sticky='ns')
#       self.rowconfigure(0, weight=1)
#       self.columnconfigure(0, weight=1)
#       # Set the scrollbars to the canvas
#       self.cnvs.config(xscrollcommand=self.h_scroll.set,
#                        yscrollcommand=self.v_scroll.set)
#       # Set canvas view to the scrollbars
#       self.v_scroll.config(command=self.cnvs.yview)
#       self.h_scroll.config(command=self.cnvs.xview)
#       # Assign the region to be scrolled
#       self.cnvs.config(scrollregion=self.cnvs.bbox('all'))
#       self.cnvs.bind_class(self.cnvs, "<MouseWheel>", self.mouse_scroll)
#
#    def mouse_scroll(self, evt):
#       if evt.state == 0:
#          self.cnvs.yview_scroll(-1 * (evt.delta), 'units')  # For MacOS
#          self.cnvs.yview_scroll(int(-1 * (evt.delta / 120)), 'units')  # For windows
#       if evt.state == 1:
#          self.cnvs.xview_scroll(-1 * (evt.delta), 'units')  # For MacOS
#          self.cnvs.xview_scroll(int(-1 * (evt.delta / 120)), 'units')  # For window
#
#
#
#
#
#
#
#
#
#
#
# win = Tk()
# # win.geometry("1920x1080")
# win.geometry("1920x1080")
#
# #Create a canvas
# # canvas= Canvas(win, width= 1920, height= 1080)
# # canvas.pack()
# import io
# doc = fitz.open(path)     # or fitz.Document(filename)
# print(doc.page_count)
# page=doc.load_page(0)
# text_instances = page.searchFor("Timers")
# for inst in text_instances:
#    highlight = page.addHighlightAnnot(inst)
#    highlight.update()
# pix=page.get_pixmap(dpi=300)
# img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
# # data = pix.getImageData("format")
# # img = Image.open(io.BytesIO(data))
# import math
# img2= ImageTk.PhotoImage(img.resize((math.floor(pix.width*0.3),math.floor(pix.height*0.3))))
#
#
#
# canvas1 = tkinter.Canvas(win, width=400, height=600)
# canvas1.pack(side=tkinter.LEFT)
#
# entry1 = tkinter.Entry(win)
# canvas1.create_window(100, 40, window=entry1)
#
#
# def getSquareRoot():
#    x1 = entry1.get()
#
#    label1 = tkinter.Label(win, text=float(x1) ** 0.5)
#    canvas1.create_window(100, 160, window=label1)
# def findnext():
#    pass
#
# button1 = tkinter.Button(text='Search', command=getSquareRoot)
# button2 = tkinter.Button(text='find next', command=findnext())
#
# canvas1.create_window(100, 80, window=button1)
# canvas1.create_window(100, 120, window=button2)
#
#
#
#
#
#
#
#
# #Add image to the Canvas Items
# #canvas.create_image(0,0,anchor=NW,image=img2)
#
# image_window = ScrollableImage(win, image=img2, scrollbarwidth=15,
#                                width=pix.width*0.3, height=pix.height*0.3)
# image_window.pack(pady=(0,50),side=tkinter.LEFT)
# #win.update_idletasks()
# #print(win.winfo_width())
#
# # import time
# # def some_function():
# #    while True:
# #       print(win.winfo_width())
# #       time.sleep(0.5)
# #
# # import threading
# # a_thread = threading.Thread(target = some_function)
# #
# # a_thread.start()
#
#
# win.mainloop()



results = {'nummatches': 3,
               'matches': {
                   0: {
                       'match':"Important",
                       'page':7,
                       'matchesonpage':2
                   },
                   1: {
                       'match': "Omportant",
                       'page': 2,
                       'matchesonpage': 1
                   },
                   2: {
                       'match': "Important",
                       'page': 5,
                       'matchesonpage': 6
                   }
               },
               }
import json
from flask import jsonify
shit=[['important', 1], ['important', 1], ['Important', 22], ['Important', 22],['important',4]]


def arrelement(arr,position):
    arr2=[]
    for n in arr:
        arr2.append(n[position])
    return arr2
def FormatToJson(input):
    output={}
    output['nummatches']=len(input)
    i=0
    arr=[]
    lenght=len(input)
    while (i < lenght):
        arr.append(i)
        i+=1
    i = 0
    output['matches'] = dict.fromkeys(arr)
    uniquematches=[]
    for n in input:
        if(n[0] not in uniquematches):
            uniquematches.append(n[0])
    #print(uniquematches)
    UniqueMatchesExtended=[]
    for n in uniquematches:
        for j in input:
            if(j[0]==n):

                if((n not in arrelement(UniqueMatchesExtended,0))):
                    UniqueMatchesExtended.append([n,j[1],1])
                else:
                    UniqueMatchesExtended[uniquematches.index(n)]=[n,UniqueMatchesExtended[uniquematches.index(n)][1],UniqueMatchesExtended[uniquematches.index(n)][2]+1]

    #print(UniqueMatchesExtended)
    while(i<lenght):
        output['matches'][i]=dict.fromkeys(['match','page','matchesonpage'])
        output['matches'][i]['match'] = input[i][0]
        output['matches'][i]['page']=input[i][1]
        output['matches'][i]['matchesonpage']=1
        i+=1
    return output
print(FormatToJson(shit))
def formtable(results):
    arr = {}
    i = 0
    while (i < len(results['matches'])):
        if (results['matches'][i]['match'] in arr):
            pages = arr[results['matches'][i]['match']][0] + [results['matches'][i]['page']]
            # print(pages)
            # # print(type(pages))
            # print(set(pages))
            pages = list(set(pages))
            # pages=set(pages)
            arr[results['matches'][i]['match']] = [pages, results['matches'][i]['matchesonpage'] +
                                                   arr[results['matches'][i]['match']][1]]
        else:
            arr[results['matches'][i]['match']] = [[results['matches'][i]['page']],
                                                   results['matches'][i]['matchesonpage']]
        i += 1
    return arr
print(formtable(results))
print(formtable(FormatToJson(shit)))