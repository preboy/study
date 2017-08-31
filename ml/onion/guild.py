from __future__ import print_function
import pymysql

from unpacker import DataUnpacker


#_____________ complex lua table ___________________________________


def lua_table(o, n = 0):
    for i in range(n-1):
        print("\t", end='')
    print("{")
    et = o.read_uint8()
    arr_i = 0
    while et:
        etk = et >> 4;
        etv = et & 0x0f;

        if etk >= 1 and etk <= 10:
            arr_i = arr_i + 1
        
        key = 1
        val = 1

        if etk == 1:
            key = o.read_int8()
        elif etk == 2:
            key = o.read_int16()
        elif etk == 3:
            key = o.read_int32()
        elif etk == 4:
            key = o.read_int64()
        elif etk == 5:
            key = o.read_uint8()
        elif etk == 6:
            key = o.read_uint16()
        elif etk == 7:
            key = o.read_uint32()
        elif etk == 8:
            key = o.read_uint64()
        elif etk == 9:
            key = o.read_float()
        elif etk == 10:
            key = arr_i
        elif etk == 11:
            key = o.read_string()
        else:
            print("unsupported key type")
        
        for i in range(n):
            print("\t", end='')
        if etk >= 1 and etk <= 10:
            print("[{0}] = ".format(key), end=' ')
        else:
            print("\"{0}\" = ".format(key), end=' ')

        if etv == 0:
            val = "nil"
        elif etv == 1:
            val = o.read_int8()
        elif etv == 2:
            val = o.read_int16()
        elif etv == 3:
            val = o.read_int32()
        elif etv == 4:
            val = o.read_int64()
        elif etv == 5:
            val = o.read_uint8()
        elif etv == 6:
            val = o.read_uint16()
        elif etv == 7:
            val = o.read_uint32()
        elif etv == 8:
            val = o.read_uint64()
        elif etv == 9:
            val = o.read_float()
        elif etv == 11:
            val = o.read_string()
        elif etv == 12:
            val = 0
        elif etv == 13:
            val = 1

        if etv == 15:
            print()
            lua_table(o, n+1)
        else:
            print("{0},".format(val))

        et = o.read_uint8()
    
    for i in range(n-1):
        print("\t", end='')
    print("}")

def script_table(o, tab_count):
    flag = o.read_uint8()
    if flag == 0:
        return
    lua_table(o)

#_____
def deserialize_guild(o):
    _id         = o.read_uint32()
    _lv         = o.read_uint8()
    _state      = o.read_uint8()
    _exp        = o.read_int32()
    _power      = o.read_int32()
    _build      = o.read_int32()
    _money      = o.read_int64()
    _token      = o.read_uint32() 
    _name       = o.read_string() 
    _notice     = o.read_string() 
    pres_id     = o.read_uint32() 
    gversion    = o.read_uint16() 
    _dummy      = o.read_uint16() 
    _create_ts  = o.read_uint32() 
    _th_plrid   = o.read_uint32() 
    _th_ts      = o.read_uint32() 

    if gversion >= 3:
        last_active_t = o.read_uint32() 
        
    size = o.read_uint16() 
    
    if size == 0:
        return

    print("mumber szie:", size, _name)
    while size:
        size -= 1
        if gversion >=2:
            plrid   = o.read_uint32()
            rank    = o.read_uint8()
            sex     = o.read_uint8()
            online  = o.read_uint8()
            map_id  = o.read_uint32()
            power   = o.read_uint32()
            level   = o.read_uint32()
            contribute       = o.read_uint32()
            total_contribute = o.read_uint32()
            join_us     = o.read_uint32()
            logout_ts   = o.read_uint32()
            name        = o.read_string()
        else:
            plrid   = o.read_uint32()
            rank    = o.read_uint8()
            sex     = o.read_uint8()
            online  = o.read_uint8()
            map_id  = o.read_uint32()
            power   = o.read_uint32()
            level   = o.read_uint32()
            contribute  = o.read_uint32()
            join_us     = o.read_uint32()
            logout_ts   = o.read_uint32()
            name        = o.read_string()
            total_contribute = 0
    
    # vice president member id
    size = o.read_uint16()
    while size:
        size -= 1
        plrid = o.read_uint32()

    # match list
    size = o.read_uint16()
    while size:
        size -= 1
        plrid = o.read_uint32()

    # match list
    size = o.read_uint16()
    while size:
        size -= 1
        spell_id = o.read_uint32()
        spell_lv = o.read_uint32()
    
    #lua data script 
    script_table(o, 1)

def main():
    # connect to db
    conn = pymysql.connect(host='219.84.160.45', port=3306, user='root',passwd='Tm!t51kjAW', db='fy996_world', charset='utf8')
    cur = conn.cursor()
    cur.execute("select id, bin from guild where id = '1137973506'")

    bin1 = None

    for i in cur:
        bin1 = i[1]
        break
    # deal with data bin1
    print("---------------- guild data ------------------")

    if bin1 == None:
        print("error in query")
        return

    o = DataUnpacker(bin1)

    deserialize_guild(o)

    cur.close()
    conn.close()




if __name__ == "__main__":
    main()
