import pymysql

from unpacker import DataUnpacker


#_____________ complex lua table ___________________________________


#______________________________________________________________________


def deserialize_mail(o):
    id      = o.read_uint32()
    send_t  = o.read_uint32()
    mtype   = o.read_uint8()
    readflag= o.read_uint8()
    sender  = o.read_string()
    subject = o.read_string()
    text    = o.read_string()
    sliver  = o.read_uint32()
    yb      = o.read_uint32()
    print("___new mail _______________")
    print("id"              , id)
    print("send_t"          , send_t)
    print("mtype"           , mtype)
    print("readflag"        , readflag)
    print("sender"          , sender)
    print("subject"         , subject)
    print("text"            , text)
    print("sliver"          , sliver)
    print("yb"              , yb)
    
    for i in range(6):
        n = o.read_uint32()
        if n:
            id = o.read_uint32()
            o.skip_bytes(n-4)
            print("物品{0}：id={1}".format(i+1, id))
    


def deserialize_mails(o):
    seq_mailid = o.read_uint32()
    n = o.read_uint32()
    for i in range(n):
        deserialize_mail(o)


def main():
    # connect to db
    conn = pymysql.connect(host='172.31.248.17', port=3306, user='dev',passwd='dev', db='dev_world', charset='gbk')
    cur = conn.cursor()
    cur.execute("select id, bin1 from player_mbox where id = '3139456318'")

    bin1 = None

    for i in cur:
        bin1 = i[1]
        break
    # deal with data bin1
    print("---------------- 玩家数据解析表 ------------------")

    if bin1 == None:
        print("查询不正确")
        return

    o = DataUnpacker(bin1)

    deserialize_mails(o)

    cur.close()
    conn.close()




if __name__ == "__main__":
    main()
