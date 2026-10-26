from haystack import HayStack
import pprint


if __name__ == '__main__':
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

    """You only have to write about 30 lines of code. Redirect this 
    output to a text file named results.txt and submit it along with 
    your source code."""