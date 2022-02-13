from fuzzysearch import find_near_matches
from pathlib import Path
from typing import Iterable, Any
from pdfminer.high_level import extract_pages

#pagecount = 0
# pagesizex = 0
# pagesizey = 0
#allmatches = []
class FuzzySearchEngine:
    def __init__(self,searchphrase):
        self.allmatches = []
        self.pagecount = 0
        self.search=searchphrase
    def show_ltitem_hierarchy(self,o: Any, depth=0):
        # global pagecount
        # global pagesizex
        # global pagesizey

        """Show location and text of LTItem and all its descendants"""
        #if depth == 0:
            # print('element                        x1  y1  x2  y2   text')
            # print('------------------------------ --- --- --- ---- -----')
        if ("LTPage" in self.get_indented_name(o, depth)):
            # if (pagecount == 0):
                # pagesizex = get_optional_bbox(o).split(" ")[-3]
                # pagesizey = get_optional_bbox(o).split(" ")[-2]
            self.pagecount += 1
        res = find_near_matches(self.search, self.get_optional_text(o), max_l_dist=2)
        # print(res)
        if (len(res) > 0):
            #print(pagecount)
            for n in res:
                self.allmatches.append([n.matched, self.pagecount])
                #print(n)


        if isinstance(o, Iterable):
            for i in o:
                self.show_ltitem_hierarchy(i, depth=depth + 1)


    def get_indented_name(self,o: Any, depth: int) -> str:
        """Indented name of LTItem"""
        return '  ' * depth + o.__class__.__name__


    def get_optional_bbox(self,o: Any) -> str:
        """Bounding box of LTItem if available, otherwise empty string"""
        if hasattr(o, 'bbox'):
            return ''.join(f'{i:<4.0f}' for i in o.bbox)
        return ''


    def get_optional_text(self,o: Any) -> str:
        """Text of LTItem if available, otherwise empty string"""
        if hasattr(o, 'get_text'):
            return o.get_text().strip()
        return ''

filepath='testpdf.pdf'
searchphrase="Important"
x=FuzzySearchEngine(searchphrase)
path = Path(filepath).expanduser()
pages = extract_pages(path)

x.show_ltitem_hierarchy(pages)
print(x.allmatches)
#import time

#t = time.time()
#path = Path('testpdf.pdf').expanduser()
#print(path)
#pages = extract_pages(path)
#show_ltitem_hierarchy(pages,search=)
#print(allmatches)
#print(time.time() - t)
# def getmatches(filepath,searchphrase):
#     if(filepath and searchphrase):
#         path = Path(filepath).expanduser()
#         pages = extract_pages(path)
#         show_ltitem_hierarchy(pages, search=searchphrase)
