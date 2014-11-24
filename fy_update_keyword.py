import os

keyword_file_1="./server/fy/bin/world/gs_scripts/keyword.fy"
keyword_file_2="./server/fy/bin/world/ws_scripts/keyword.fy"
keyword_file_3="./server/fy/bin/world/ds_scripts/keyword.fy"
keyword_file_4="./server/fy/bin/world/lg_scripts/keyword.fy"

syntax_file="D:/Tools/EditPlus 3/lua51.stx"

def update_keyword():
    _f = open(keyword_file_1)
    _keywords_1 = _f.read()
    _f.close()

    _f = open(keyword_file_2)
    _keywords_2 = _f.read()
    _f.close()

    _f = open(keyword_file_3)
    _keywords_3 = _f.read()
    _f.close()

    _f = open(keyword_file_4)
    _keywords_4 = _f.read()
    _f.close()

    _o = []
    _f = open(syntax_file)
    for _line in _f.readlines():
        _o.append(_line)
        if _line.find("#KEYWORD=fy API") != -1:
            break
    _f.close()

    _f = open(syntax_file, 'w')
    for _str in _o:
        _f.write(_str)
    _f.write(_keywords_1)
    _f.write(_keywords_2)
    _f.write(_keywords_3)
    _f.write(_keywords_4)
    _f.close()

    print("done! need to restart your editplus.")
    raw_input("press enter to exit")

if __name__ == "__main__":
    update_keyword()