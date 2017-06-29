#coding=utf8
# 取某段时间内某人(某群人的)SVN上更新日志，并去除重复保存到当前目录下的svn_log.txt文件中。


import os


#----------------------------- the config ------------------------------

# only get svn log committed by who in the follow table.
user_table  = ("longwei", "zhangyi", "renxujie", "yujunhong", "fengxiyao", "liyang", "zhangchaoguo",)
# user_table    = ("zhangchaoguo",)  # 当只有一项时，一定要有最后的','，否则出错。
svn_log     = "svn_log.txt"


# 撸的方式: 时间段、 两个版本号之间
LOL_by_version = True


################# 取两次版本号之间的日志 #################
# 每一次打版本只需要把当前最新的SVN版本号加到vers这个tuple末尾就可以了。
# vers 这个元组只会用到最后两项，所以请保证它至少有两项
vers        = (12548, 12634, )
vlen        = len(vers)
prev_ver    = vers[vlen-2]+1
curr_ver    = vers[vlen-1]


################# 取一段时间这内的日志 #################
begin_time = "2014-8-20"
close_time = "2014-9-1"




#----------------------------- Do not edit below -------------------------

line_dict = {}
for user_item in user_table:
    str_file = "%s.txt"%(user_item)
    if LOL_by_version:
        str_cmd = format("svn log e:\projects\server -r %d:%d --search %s > %s"%(prev_ver, curr_ver,  user_item, str_file))
    else:
        str_cmd = format("svn log e:\projects\server -r {%s}:{%s} --search %s > %s"%(begin_time, close_time,  user_item, str_file))
#   print(str_cmd)
    os.system(str_cmd)

    _f = open(str_file)
    _lines = _f.readlines()
    _f.close()

    for _line in _lines:
        if len(_line) <= 1 or _line[0:6] == "------" or _line[1:4].isdigit():
            continue
        line_dict[_line] = True

    os.remove(str_file)


# keep repeat line
_svn_log = open(svn_log, 'w')
for k, _ in line_dict.items():
    _svn_log.write(k)
_svn_log.close()


os.system("start editplus.exe %s"%(svn_log))
