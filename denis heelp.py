# # from tkinter import *
# #
# # class inputs(object):
# #     def __init__(self):
# #         # creating a tkinter window
# #         self.screen = Tk()
# #         self.screen.geometry("650x400+600+250")
# #         self.apple="234"
# #         self.__listofinput = []
# #         self.equation_text = Label(text="Input your equation for maximizing/minimizing", )
# #         self.equation_text.place(x=15, y=70)
# #         self.button = Button(self.screen, text='Done', command=self.screen.quit)
# #
# #         self.input_var = StringVar()
# #         self.input_get = self.input_var.get()
# #         self.__listofinput.append(self.input_get)
# #         self.input_entry = Entry(self.screen, textvariable=self.input_var)
# #         self.input_entry.pack()
# #         self.equation_text.pack()
# #         self.button.pack()
# #
# #         #binding key buttons for exiting the window
# #         self.screen.bind("<Return>", lambda e: self.screen.quit())
# #         self.screen.bind("<Escape>", lambda e: self.screen.quit())
# #
# #         self.screen.mainloop()
# #
# #     def returninput(self):
# #         return self.__listofinput
# #
# #
# # myclass = inputs()
# # caca = myclass.returninput()
# # print(caca)
#
#
# results = {'nummatches': 3,
#                'matches': {
#                    0:{
#                    'match':"Important",
#                    'page':7,
#                    'matchesonpage':2
#                           },
#                    1: {
#                        'match': "Omportant",
#                        'page': 2,
#                        'matchesonpage': 1
#                    },
#                    2: {
#                        'match': "Important",
#                        'page': 5,
#                        'matchesonpage': 6
#                    },
#                    3: {
#                        'match': "Important",
#                        'page': 9,
#                        'matchesonpage': 6
#                    },
#                    4: {
#                        'match': "Important",
#                        'page': 5,
#                        'matchesonpage': 7
#                    }
#                }
#                }
# print(len(results['matches']))
# # i=0
# # already_used=[]    #[["Important",[3,4,5],[5]]]
# # while(i<len(results['matches'])):
# #     j=0
# #     while(j<len(already_used)):
# #         if(results['matches'][i]['match']==already_used[j-1]):
# #             print(already_used[j-1])
# #             print(results['matches'][i])
# #             #n=results['matches'][i]['match'],n[1]+[results['matches'][i]['page']],n[2]+results['matches'][i]['matchesonpage']
# #             print(already_used[j-1])
# #             print("match")
# #             break
# #         else:
# #             j+=1
# #             already_used.append([results['matches'][i]['match'],[results['matches'][i]['page']],results['matches'][i]['matchesonpage']])
# #             print("here")
# #         j+=1
# #     if(len(already_used)==0):
# #         already_used.append([results['matches'][i]['match'],[results['matches'][i]['page']],results['matches'][i]['matchesonpage']])
# #         #print(n[0])
# #         #print(results['matches'][i]['match'])
# #     print(already_used)
# #     print(i)
# #     # if(results['matches'][i] in already_used):
# #     #     print("123")
# #     i+=1
# # print(already_used)
#
# # arr={}
# # i=0
# # while(i<len(results['matches'])):
# #     if(results['matches'][i]['match'] in arr):
# #         pages=arr[results['matches'][i]['match']][0]+[results['matches'][i]['page']]
# #         # print(pages)
# #         # # print(type(pages))
# #         # print(set(pages))
# #         pages=list(set(pages))
# #         #pages=set(pages)
# #         arr[results['matches'][i]['match']]=[pages,results['matches'][i]['matchesonpage']+arr[results['matches'][i]['match']][1]]
# #     else:
# #         arr[results['matches'][i]['match']] = [[results['matches'][i]['page']],results['matches'][i]['matchesonpage']]
# #     i+=1
# # print(arr)
# #
# #
#
# def formtable(results):
#     arr = {}
#     i = 0
#     while (i < len(results['matches'])):
#         if (results['matches'][i]['match'] in arr):
#             pages = arr[results['matches'][i]['match']][0] + [results['matches'][i]['page']]
#             # print(pages)
#             # # print(type(pages))
#             # print(set(pages))
#             pages = list(set(pages))
#             # pages=set(pages)
#             arr[results['matches'][i]['match']] = [pages, results['matches'][i]['matchesonpage'] +
#                                                    arr[results['matches'][i]['match']][1]]
#         else:
#             arr[results['matches'][i]['match']] = [[results['matches'][i]['page']],
#                                                    results['matches'][i]['matchesonpage']]
#         i += 1
#     return arr
# print(formtable(results))
# n={'nummatches': 3,
#    'matches': {
#        0: {
#            'match': 'Important',
#            'page': 7,
#            'matchesonpage': 2},
#        1:
#            {'match': 'Omportant',
#             'page': 2,
#             'matchesonpage': 1},
#        2: {'match': 'Important',
#            'page': 5,
#            'matchesonpage': 6}},
#    'tablematch':
#        {'Important': [[5, 7], 8],
#         'Omportant': [[2], 1]
#         }
#    }
import base64

with open("flasksolution/compressed.tracemonkey-pldi-09.pdf", "rb") as pdf_file:
    encoded_string = base64.b64encode(pdf_file.read())
    print(encoded_string[-10:])
    print(len(encoded_string))
    print((len(encoded_string) * (3/4)) - 1)
# def convert_and_save(b64_string):
#     with open("tst.pdf", "wb") as fh:
#         fh.write(base64.decodebytes(b64_string))
# convert_and_save(encoded_string)
