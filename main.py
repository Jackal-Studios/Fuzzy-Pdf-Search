from tika import parser # pip install tika
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from fuzzysearch import find_near_matches
# i=input("pdf path:")
# #i='testpdf.pdf'
# search=input("search phrase: ")
# raw = parser.from_file(i)
# #print(raw['content'])
# #print(fuzz.token_sort_ratio("Catherine Gitau M. ", "Catheriny"))
# #sequence = '''hello sashas, i want to give sashi, sashu and sesha'''
# #subsequence = 'sasha' # distance = 1
# results=find_near_matches(search, raw['content'], max_l_dist=2)
# print("found {} matches".format(str(len(results))))
# for n in results:
#     #print(n['matched'])
#     print(n.matched)

#print(parser.from_file("testpdf.pdf", xmlContent=True))
i=input("pdf path:")
search=input("search phrase: ")
#find_near_matches(search, raw['content'], max_l_dist=2)
from pathlib import Path
from typing import Iterable, Any
from pdfminer.high_level import extract_pages
#from pdfminer3.high_level import ex
pagecount=0
pagesizex=0
pagesizey=0
allmatches=[]
def show_ltitem_hierarchy(o: Any, depth=0):
    global pagecount
    global pagesizex
    global pagesizey

    """Show location and text of LTItem and all its descendants"""
    if depth == 0:
        print('element                        x1  y1  x2  y2   text')
        print('------------------------------ --- --- --- ---- -----')

    # print(
    #     f'{get_indented_name(o, depth):<30.30s} '
    #     f'{get_optional_bbox(o)} '
    #     f'{get_optional_text(o)}'
    # )
    if("LTPage" in get_indented_name(o, depth)):
        if(pagecount==0):
            pagesizex=get_optional_bbox(o).split(" ")[-3]
            pagesizey=get_optional_bbox(o).split(" ")[-2]
        pagecount+=1
    res = find_near_matches(search, get_optional_text(o), max_l_dist=2)
    #print(res)
    if(len(res)>0):
        print(pagecount)
        # print(
        #          f'{get_optional_bbox(o)} '
        #          f'{get_optional_text(o)}'
        #      )
        for n in res:
            allmatches.append([n.matched,pagecount])
            print(n)
        
    # if("IMPORTANT" in get_optional_text(o)):
    #     print(
    #          f'{get_optional_bbox(o)} '
    #          f'{get_optional_text(o)}'
    #      )
    #     print(pagecount)
    #     #print(get_indented_name(o, depth))

    if isinstance(o, Iterable):
        for i in o:
            show_ltitem_hierarchy(i, depth=depth + 1)


def get_indented_name(o: Any, depth: int) -> str:
    """Indented name of LTItem"""
    return '  ' * depth + o.__class__.__name__


def get_optional_bbox(o: Any) -> str:
    """Bounding box of LTItem if available, otherwise empty string"""
    if hasattr(o, 'bbox'):
        return ''.join(f'{i:<4.0f}' for i in o.bbox)
    return ''


def get_optional_text(o: Any) -> str:
    """Text of LTItem if available, otherwise empty string"""
    if hasattr(o, 'get_text'):
        return o.get_text().strip()
    return ''


path = Path('testpdf.pdf').expanduser()

pages = extract_pages(path)
show_ltitem_hierarchy(pages)
print(allmatches)


#
#
#     LTCurve                    367 21  370 24
#   LTPage                       0   0   612 792
#     LTTextBoxHorizontal        59  652 547 714  IMPORTANT NOTICE AND DISCLAIMER
# TI PROVIDES TECHNICAL AND RELIABILITY DATA (INCLUDING DATA SHEETS), DESIGN RESOURCES (INCLUDING REFERENCE
# DESIGNS), APPLICATION OR OTHER DESIGN ADVICE, WEB TOOLS, SAFETY INFORMATION, AND OTHER RESOURCES “AS IS”
# AND WITH ALL FAULTS, AND DISCLAIMS ALL WARRANTIES, EXPRESS AND IMPLIED, INCLUDING WITHOUT LIMITATION ANY
# IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE OR NON-INFRINGEMENT OF THIRD
# PARTY INTELLECTUAL PROPERTY RIGHTS.
#       LTTextLineHorizontal     193 702 419 714  IMPORTANT NOTICE AND DISCLAIMER



# print(results)
# print(type(results[0]))
#print(find_near_matches(search, raw['content'], max_l_dist=2))

#[Match(start=3, end=24, dist=1, matched="TAGCACTGTAGGGATAACAAT")]