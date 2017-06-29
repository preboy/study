import pymysql

from unpacker import DataUnpacker


#_____________ complex lua table ___________________________________


#_____
def deserialize_guild(o):
    _id         = o.read_uint8()
    _lv         = o.read_uint8()
    _state    = o.read_uint8()
    _exp     = o.read_int32()
    _power  = o.read_int32()
    _build     = o.read_int32()
    _money    = o.read_int64()
    _token    = o.read_uint32() 
    _name     = o.read_string() 
    _notice     = o.read_string() 
    pres_id    = o.read_uint32() 
    gversion  = o.read_uint16() 
    dummy    = o.read_uint16() 
    _create_ts   = o.read_uint32() 
    
    _th_plrid   = o.read_uint32() 
    _th_ts          = o.read_uint32() 

    if gversion >= 3:
        last_active_t = o.read_uint32() 
        
    size = o.read_uint16() 
    
    print("mumber szie:", size, _name)



def main():
    # connect to db
    conn = pymysql.connect(host='172.31.248.17', port=3306, user='dev',passwd='dev', db='dev_world', charset='gbk')
    cur = conn.cursor()
    cur.execute("select id, bin from guild where id = '3538681856'")

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
