# -*- coding: utf8 -*-
import os
import os.path

import opencc

import sys
reload(sys)
# sys.setdefaultencoding('utf8')
# sys.setdefaultencoding('gbk')  gb18030  gb2312
sys.setdefaultencoding('gb18030')

# print(sys.getdefaultencoding()  )



# rootdir = "d:\Workspace\world\gs_scripts"                                   # 指明被遍历的文件夹
# os.system("rmdir /S /Q d:\workspace\world_2")

rootdir = "E:/projects_tw/server/fy/bin/world"
os.system("rmdir /S /Q E:/projects_tw/server/fy/bin/world_2")



files = []

def scan_file(dn):  # dn 文件夹名 不包含\
    for f in os.listdir(dn):
        fn = dn + "\\" + f
        if os.path.isfile(fn):
            suffix = os.path.splitext(f)[1]
            if suffix != ".Nav" and suffix != ".nav" and suffix != ".data":
                files.append(fn)
        elif os.path.isdir(fn):
            scan_file(fn)
        else:
            print "unknown file"


scan_file(rootdir)

files.sort()

# 获得后缀
su = {}

cc = opencc.OpenCC('s2t')


def file_cc(fns, fnd):
    content = []
    f = open(fns)
    for line in f.readlines():
        try:
            text_tw = cc.convert(line)
        except:
            text_tw = cc.convert(line.decode('utf8').encode('gb18030'))
        content.append(text_tw)
        #n print "ater conv: ",  type(bytes(text_tw))
    f.close()
    # print content
    
    try:
        os.makedirs(os.path.dirname(fnd))
    except:
        pass

    fd = open(fnd, "w")

    for line in content:
        fd.write(line.encode('big5', 'ignore'))
        # fd.write(line.encode('utf8')).decode('unicode')
    
    fd.close()




#fs = "e:/Workspace/world/creatures.conf"
#fd = "e:/Workspace/world_2/creatures.conf"
#file_cc(fs, fd)


for f in files:
    # nf = f[0:18] + '_2' + f[18:]
    nf = f[0:34] + '_2' + f[34:]            # for tw path
    print "file: ", f
    file_cc(f, nf)
    # break