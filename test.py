from fuzzysearch import find_near_matches
sequence = '''тири пири в нас нема однорідної матриці'''
subsequence = 'однорідна матриця' # distance = 1
print(find_near_matches(subsequence, sequence, max_l_dist=4))