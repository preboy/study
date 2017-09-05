from __future__ import print_function
import pymysql

from unpacker import DataUnpacker


#_____________ complex lua table ___________________________________

guild_exp_info = {}
guild_exp_member= []

guild_spell_info=[]

spid_to_idx = { 2:7, 7:8, 8:9, 10:10, 12:11, 14:12, 16:13, 18:14, 20:15 }


def lua_table(_id, o, n = 0):
    for i in range(n-1):
        pass # print("\t", end='')
    # print("{")
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

        # for i in range(n):
        #     print("\t", end='')
        if etk >= 1 and etk <= 10:
            pass # print("[{0}] = ".format(key), end=' ')
        else:
            pass # print("\"{0}\" = ".format(key), end=' ')

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
            # print()
            lua_table(_id, o, n+1)
        else:
            pass # print("{0},".format(val))

        et = o.read_uint8()
        
        if n == 0:
            if key == "Level":
                guild_exp_info[_id][15] = val
                # print(_id, n, 15, val)
            elif key == "MarketLevel":
                guild_exp_info[_id][19] = val
                # print(_id, n, 19, val)
            elif key == "WushuLevel":
                guild_exp_info[_id][17] = val
                # print(_id, n, 17, val)
            elif key == "EscortLevel":
                guild_exp_info[_id][18] = val
                # print(_id, n, 18, val)
            elif key == "AltarLevel":
                guild_exp_info[_id][16] = val
                # print(_id, n, 16, val)

    # for i in range(n-1):
    #     print("\t", end='')
    # print("}")


def script_table(_id, o, tab_count):
    flag = o.read_uint8()
    if flag == 0:
        return
    lua_table(_id, o)


def deserialize_guild(_id, o):
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
    _member_size = size

    if size == 0:
        return

    # print("member szie:", size, _name)
    while size:
        size -= 1
        if gversion >=2:
            plrid       = o.read_uint32()
            rank        = o.read_uint8()
            sex         = o.read_uint8()
            online      = o.read_uint8()
            map_id      = o.read_uint32()
            power       = o.read_uint32()
            level       = o.read_uint32()
            contribute  = o.read_uint32()
            total_contribute = o.read_uint32()
            join_us     = o.read_uint32()
            logout_ts   = o.read_uint32()
            name        = o.read_string()
        else:
            plrid       = o.read_uint32()
            rank        = o.read_uint8()
            sex         = o.read_uint8()
            online      = o.read_uint8()
            map_id      = o.read_uint32()
            power       = o.read_uint32()
            level       = o.read_uint32()
            contribute  = o.read_uint32()
            join_us     = o.read_uint32()
            logout_ts   = o.read_uint32()
            name        = o.read_string()
            total_contribute = 0
        # insert guild member to list
        guild_exp_member.append( (_id, plrid, name, level, power, rank, contribute) )

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

    # spell list
    tmp_guild_data = [_id, _name, _lv, _member_size,  0,0,  0,0,0,0,0,0,0,0,0,  0,0,0,0,0 ]

    size = o.read_uint16()
    while size:
        size -= 1
        spell_id = o.read_uint32()
        spell_lv = o.read_uint32()

        idx = spid_to_idx[spell_id]
        tmp_guild_data[idx-1] = spell_lv

    # insert guild to list
    guild_exp_info[_id] = tmp_guild_data

    #lua data script
    script_table(_id, o, 1)

def main():
    # connect to db
    conn = pymysql.connect(host='219.84.160.45', port=3306, user='root',passwd='Tm!t51kjAW', db='fy996_world', charset='big5')
    cur = conn.cursor()
    cur.execute("select id, bin from guild;")

    ret = cur.fetchall()
    for row in ret:
        _gid = row[0]
        bin1 = row[1]
        if bin1:
            o = DataUnpacker(bin1)
            deserialize_guild(_gid, o)

    # print(guild_exp_info, )
    # print(len(guild_exp_member) )
    # print("end")
    # exit()


    # DO INSERT
    sql = """
    DROP TABLE IF EXISTS `guild_exp_info`;
    CREATE TABLE `guild_exp_info` (
      `gid` bigint(11) NOT NULL,
      `name` varchar(32) DEFAULT NULL,
      `lv` int(11) DEFAULT NULL,
      `cnt` int(11) DEFAULT NULL,
      `occupy` int(11) DEFAULT NULL,
      `instance` int(11) DEFAULT NULL,
      `splv_hp` int(11) DEFAULT NULL,
      `splv_atk` int(11) DEFAULT NULL,
      `splv_def` int(11) DEFAULT NULL,
      `splv_accu` int(11) DEFAULT NULL,
      `splv_dodge` int(11) DEFAULT NULL,
      `splv_crit` int(11) DEFAULT NULL,
      `splv_anti_crit` int(11) DEFAULT NULL,
      `splv_block` int(11) DEFAULT NULL,
      `splv_anti_block` int(11) DEFAULT NULL,
      `bulv_main` int(11) DEFAULT NULL,
      `bulv_altar` int(11) DEFAULT NULL,
      `bulv_wushu` int(11) DEFAULT NULL,
      `bulv_escort` int(11) DEFAULT NULL,
      `bulv_market` int(11) DEFAULT NULL,
      PRIMARY KEY (`gid`)
    ) ENGINE=InnoDB DEFAULT CHARSET=big5;
    """
    cur.execute(sql);


    for i in guild_exp_info:
        x = guild_exp_info[i]
        sql = """insert into `guild_exp_info` (
          `gid`,
          `name`,
          `lv`,
          `cnt`,
          `occupy`,
          `instance`,
          `splv_hp`,
          `splv_atk`,
          `splv_def`,
          `splv_accu`,
          `splv_dodge`,
          `splv_crit`,
          `splv_anti_crit`,
          `splv_block`,
          `splv_anti_block`,
          `bulv_main`,
          `bulv_altar`,
          `bulv_wushu`,
          `bulv_escort`,
          `bulv_market`
        ) VALUES (
            {0},
            '{1}',
            {2},
            {3},
            {4},
            {5},
            {6},
            {7},
            {8},
            {9},
            {10},
            {11},
            {12},
            {13},
            {14},
            {15},
            {16},
            {17},
            {18},
            {19}
        );
        """.format(
            x[0],
            x[1],
            x[2],
            x[3],
            x[4],
            x[5],
            x[6],
            x[7],
            x[8],
            x[9],
            x[10],
            x[11],
            x[12],
            x[13],
            x[14],
            x[15],
            x[16],
            x[17],
            x[18],
            x[19]
        )
        # print( sql)
        cur.execute(sql)


    # DO INSERT guild member
    # DO INSERT
    sql = """
    DROP TABLE IF EXISTS `guild_exp_member`;
    CREATE TABLE `guild_exp_member` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `gid` bigint(11) DEFAULT NULL,
      `pid` bigint(11) DEFAULT NULL,
      `name` varchar(32) DEFAULT NULL,
      `level` int(11) DEFAULT NULL,
      `power` int(11) DEFAULT NULL,
      `rank` int(11) DEFAULT NULL,
      `contribute` int(11) DEFAULT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=big5;
    """
    cur.execute(sql)


    for x in guild_exp_member:
        sql = """insert into `guild_exp_member` (
        `gid`,
        `pid`,
        `name`,
        `level`,
        `power`,
        `rank`,
        `contribute`
        ) VALUES (
            {0},
            {1},
            '{2}',
            {3},
            {4},
            {5},
            {6}
        );""".format(
            x[0],
            x[1],
            x[2],
            x[3],
            x[4],
            x[5],
            x[6]
        )
        # print(sql)
        cur.execute(sql)


    cur.close()
    conn.commit()
    conn.close()




if __name__ == "__main__":
    main()
