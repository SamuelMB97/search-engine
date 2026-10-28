from haystack import HayStack
import pprint
import sys


def driver_code():
    engine = HayStack('http://roversgame.net/cs3270/page1.html',4)
    for w in ['pages','links','you','have','I']:
        print(w)
        pprint.pprint(engine.lookup(w))
    print()
    print('index:')
    pprint.pprint(engine.index)
    print()
    print('graph:')
    pprint.pprint(engine.graph)
    print()
    print('ranks:')
    pprint.pprint({page:round(rank,4) for page,rank in engine.ranks.items()})


def print_to_file(file, function):
    with open(file, "w", encoding="utf-8") as f:
        orig_stdout = sys.stdout
        sys.stdout = f
        function()
        sys.stdout = orig_stdout



if __name__ == '__main__':
    #driver_code()
    print_to_file("results.txt", driver_code)


    """You only have to write about 30 lines of code. Redirect this 
    output to a text file named results.txt and submit it along with 
    your source code."""