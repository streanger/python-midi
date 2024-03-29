import pprint
from collections import OrderedDict
import json

def create_notes(initValue=21, shapeX=4, shapeY=12, swap=False, strData=False, constantValue=None):
    # if constantValue is specified, all data is filled with this value
    data = []
    if not swap:
        for x in range(shapeY):
            if not constantValue is None:
                row = [constantValue for y in range(shapeX)]
            else:
                row = [initValue + y + x*shapeX for y in range(shapeX)]
            if strData:
                row = list(map(str, row))
            data.append(row)
    else:
        for x in range(shapeY):
            if not constantValue is None:
                row = [constantValue for y in range(shapeX)]
            else:
                row = [initValue + shapeY*y + x for y in range(shapeX)]
            if strData:
                row = list(map(str, row))
            data.append(row)
    out = ',\n'.join([str(item) for item in data])
    out = '{\n' + out.replace('[', '{').replace(']', '}') + '\n};'
    return out
    
    
def notes_to_list(notes):
    ''' put notes array(as str) as parameter and u will get list of element '''
    clear = notes.strip().replace('{', '').replace('}', '').replace("'", "")
    out = [item.strip() for item in clear.split(',')]
    return out
    
    
if __name__ == "__main__":
    # notes = create_notes(initValue=17, shapeX=4, shapeY=12, swap=True, strData=False, constantValue=0)
    # notes = create_notes(initValue=17, shapeX=8, shapeY=12, swap=True, strData=False)
    notes = create_notes(initValue=25, shapeX=8, shapeY=12, swap=True, strData=False)
    print(notes)
    
    
    '''
    # this is to convert back
    notes = """    {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b'},
    {'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n'},
    {'o', 'p', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '!'},
    {'@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-'}"""
    out = notes_to_list(notes)
    dictio = OrderedDict()
    for key, item in enumerate(out):
        dictio[item] = key+17
    # pprint.pprint(dictio)
    print(json.dumps(dictio, indent=4))
    '''
    