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

    
#______________________________________________________________________


# 解析数据库的方法
def deserialize_props_ext(o):
    print("------------ deserialize_props_ext ------------------")
    print("unique_id:\t",           o.read_uint32())
    print("scale:\t",               o.read_uint32())
    print("HP:\t",                  o.read_uint32())
    print("RP:\t",                  o.read_uint32())
    print("是否死亡:\t",            o.read_uint8())

    print("invicible:\t",           o.read_uint8())
    print("invicible2plr:\t",       o.read_uint8())
    print("invincible2c:\t",        o.read_uint32())
    print("move_anim:\t",           o.read_uint8())

    print("def_faction:\t",         o.read_uint32())
    print("_chg_weapon_ts:\t",      o.read_uint32())

    print("队伍ID:\t",              o.read_uint32())
    print("帮会ID:\t",              o.read_uint32())

    # 装备外观
    print("武器:\t",                o.read_uint32())
    print("外观 身体:\t",           o.read_uint32())
    print("外观 手:\t",             o.read_uint32())
    print("外观 脚:\t",             o.read_uint32())
    print("外观 肩:\t",             o.read_uint32())
    print("gear_fashion:\t",        o.read_uint32())
    print("wing_lv:\t",             o.read_uint32())
    print("horse_lv:\t",            o.read_uint32())

    print("称号:\t",                o.read_uint32())
    print("经验:\t",                o.read_uint32())
    print("元气:\t",                o.read_uint32())

    print("PK值:\t",                o.read_int32())
    print("pkv_dim_t:\t",           o.read_uint32())

    # currency
    print("银两:\t",                o.read_uint32())
    print("金子:\t",                o.read_uint32())
    print("元宝:\t",                o.read_uint32())
    print("jf_pay:\t",              o.read_uint32())
    print("consume:\t",             o.read_uint32())
    print("repu_city:\t",           o.read_uint32())
    print("repu_instance:\t",       o.read_uint32())
    print("repu_arena:\t",          o.read_uint32())
    print("repu_bf:\t",             o.read_uint32())

    print("madness:\t",             o.read_uint8())
    print("mad_open:\t",            o.read_uint8())

    print("mad_ptr:\t",             o.read_int32())
    print("mad_ptr_max:\t",         o.read_int32())

    print("魔身 id:",               o.read_int32())
    print("魔身 lv:",               o.read_int32())

    print("fashion:\t",             o.read_uint8())

    print("vip等级:\t",             o.read_int32())
    print("vip经验:\t",             o.read_int32())

    print("arena_ptr:\t",           o.read_uint32())
    print("成就点数:\t",            o.read_uint32())

    print("偃石:\t",                o.read_uint32())
    print("仓库银两:\t",            o.read_uint32())
    print("仓库金子:\t",            o.read_uint32())

    print("武器:\t",                o.read_int32())
    print("武器战斗力:\t",          o.read_int32())

    print("翅膀:\t",                o.read_int32())
    print("翅膀战斗力:\t",          o.read_int32())

    print("坐骑:\t",                o.read_int32())
    print("坐骑战斗力:\t",          o.read_int32())

    print("flwr_protoid:\t",        o.read_uint32())
    print("flwr_tele_guid:\t",      o.read_uint64())

    # 好了，写到这里算了
    size = o.read_uint16()
    o.skip_bytes(size)
    print("obj_vis size = ", size, " skiped")

    # schedule
    print("last_sched_day:\t",      o.read_uint32())
    print("last_sched_week:\t",     o.read_uint32())

    # chariot
    print("chariot teleid:\t",      o.read_uint64())
    print("chariot_info:\t",        o.read_uint32())

    # skip user settingb
    o.skip_bytes(32)

    # guild_name
    print("帮会名:\t",              o.read_string())
    print("ol_base:\t",             o.read_uint32())
    print("cloud config:\t",        o.read_string())



def deserialize_item_detail(protoid, o):

        print("\t原型ID = {0}".format(protoid))
        cnt = o.read_uint16()
        while cnt:
            cnt -= 1
            idx = o.read_uint16()
            val = o.read_uint32()
            print("\t\t属性:{0}->{1}".format(idx, val))
        print("\t\texpire:", o.read_uint32())

        #varblock: skiped
        save_cnt = o.read_uint16()
        o.skip_bytes(4*save_cnt)

        # script tab
        script_table(o, 2)


def deserialize_item(o):
    print("------------ deserialize_item ------------------")

    sz = o.read_uint32()
    if sz == 0:
        return

    # cooldown(skip, no print)
    while True:
        sid = o.read_uint32()
        if sid == 0:
            break
        val = o.read_uint32()
        print("sid, val = ", sid, val)

    print("背包大小:",          o.read_uint16())
    print("仓库大小:",          o.read_uint16())
    print("_last_update_ts:",   o.read_uint32())

    # read 道具
    count = 0
    while True:
        protoid = o.read_uint32()
        if protoid == 0:
            break
        count += 1
        deserialize_item_detail(protoid, o)

    # sold history
    hsz = o.read_uint8()
    for i in range(hsz):
        protoid = o.read_uint32()
        deserialize_item_detail(protoid, o)

    # 仓库相关
    print("仓库状态:\t",         o.read_uint8())
    print("仓库open_day:\t",     o.read_uint8())

    o.skip_bytes(4)


def deserialize_pet(o):
    print("------------ deserialize_pet ------------------")


def deserialize_quest(o):
    print("------------ deserialize_quest ------------------")
    sz = o.read_uint16()
    for i in range(sz):
        id  = o.read_uint32()
        cnt = o.read_uint16()
        print("id, cnt = {0}, {1}".format(id, cnt))

    sz = o.read_uint16()
    while sz:
        sz -= 1
        # proto_id >> _state >> _stage >> _cur_stage_flag >> rem_t >> _end_t;
        print("\t任务ID:\t",        o.read_uint32())
        print("\t任务state:\t",     o.read_uint16())
        print("\t任务stage:\t",     o.read_uint16())
        print("\t任务flag:\t",      o.read_uint16())
        print("\t任务rem_t:\t",     o.read_uint32())
        print("\t任务end_t:\t",     o.read_uint32())

        cnt = o.read_uint8()
        for i in range(cnt):
            _data_block = o.read_uint32()
            #print("data_block:\t", _data_block, cnt)

        lv      = o.read_uint16()
        exp     = o.read_uint32()
        silver  = o.read_uint32()
        yq      = o.read_uint32()
        _data   = o.read_uint8()

    sz = o.read_uint16()
    while sz:
        sz -= 1
        id = o.read_uint32()

    eat_limit       = o.read_uint8()
    eat_cnt         = o.read_uint8()
    magic_quest_cnt = o.read_uint16()
    magic_daily_cnt = o.read_uint16()



def deserialize_app(o):
    print("------------ deserialize_app ------------------")
    cnt = o.read_uint32()

    if cnt != 0:
        print("老子干不了，异常的APP数据表")
        sys.exit()


def deserialize_friend(o):
    print("------------ deserialize_friend ------------------")
    _signature = o.read_string()

    cnt = o.read_uint16()
    for i in range(cnt):
        plrid = o.read_uint32()

    cnt = o.read_uint16()
    for i in range(cnt):
        name = o.read_string()
        plrid = o.read_uint32()

    cnt = o.read_uint16()
    for i in range(cnt):
        plrid = o.read_uint32()

    # Foe
    cnt = o.read_uint16()
    for i in range(cnt):
        plrid = o.read_uint32()

    cnt = o.read_uint16()
    for i in range(cnt):
        plrid = o.read_uint32()


def deserialize_mad(o):
    print("------------ deserialize_mad ------------------")
    sz = o.read_uint16()
    for i in range(sz):
        id = o.read_uint16()
        lv = o.read_uint16()
        print("魔身:id={0}, lv={1}".format(id, lv))

def parse_aura(o):
    aid = o.read_uint32()
    if aid == 0:
        return False
    sz = o.read_uint16()
    paused = o.read_uint8()
    rem_t = o.read_int32()
    caster_id = o.read_uint64()
    #effectctx
    caster_guid = o.read_uint64()
    # vb serial
    save_cnt = o.read_uint16()
    o.skip_bytes(4*save_cnt)
    # continue
    atk         = o.read_uint32()
    add_dmg     = o.read_float()
    caster_lv   = o.read_uint32()
    dmg_coeff   = o.read_float()
    print("aid = ", aid, "数据暂不解析")
    return True

def deserialize_aura(o):
    print("------------ deserialize_aura ------------------")
    while parse_aura(o):
        pass

def deserialize_spell(o):
    print("------------ deserialize_spell ------------------")
    while True:
        val = o.read_uint32()
        if val == 0:
            break
    # spell cd
    while True:
        sid = o.read_uint32()
        if sid == 0:
            break
        else:
            val = o.read_uint32()


def deserialize_shortcuts(o):
    print("------------ deserialize_shortcuts (不想显示) ------------------")
    cnt = o.read_uint8()
    for i in range(cnt):
        if i < 32:
            shortcut_type = o.read_uint8()
            if shortcut_type != 0:
                item_proto = o.read_uint32()
        else:
            tp = o.read_uint8()
            if tp != 0:
                proto = o.read_uint32()




def deserialize_dialog(o):
    print("------------ deserialize_dialog (不想显示) ------------------")
    while True:
        id = o.read_uint32()
        if id == 0:
            break

        sender_id   = o.read_uint32()
        udata       = o.read_uint32()
        dur         = o.read_uint32()
        bf          = o.read_string()
        style       = o.read_uint8()
        text        = o.read_string()
        sz = o.read_uint32()
        o.skip_bytes(sz)


def deserialize_varblock(o):
    print("------------ deserialize_varblock (不想显示) ------------------")
    save_cnt = o.read_uint16()
    o.skip_bytes(4*save_cnt)

def deserialize_script_table(o):
    print("------------ deserialize_script_table (重要) ------------------")
    script_table(o, 1)

def deserialize_patch(o):
    print("------------ deserialize_patch (不想显示) ------------------")
    u8 = o.read_uint8()


def deserialize_record_value(o):
    print("------------ deserialize_patch (不重要也不想显示) ------------------")
    sz = o.read_uint32()
    o.skip_bytes(sz)


def deserialize_exp_fix(o):
    print("------------ deserialize_exp_fix (杀怪数据：不重要也不想显示) ------------------")
    sz = o.read_uint32()
    if sz == 0:
        return
    o.skip_bytes(sz)

def deserialize_prop_ext_1(o):
    print("------------ deserialize_prop_ext_1 (不想显示) ------------------")
    sz = o.read_uint16()
    if sz == 0:
        return
    o.skip_bytes(sz)


def deserialize_only_event(o):
    print("------------ deserialize_only_event (不想显示) ------------------")
    sz = o.read_uint16()
    if sz == 0:
        return
    o.skip_bytes(sz)

def deserialize_class(o):
    print("------------ deserialize_class (不想显示) ------------------")
    sz = o.read_uint16()
    if sz == 0:
        return
    o.skip_bytes(sz)


def deserialize_var_props(o):
    print("------------ deserialize_var_props (不想显示) ------------------")
    sz = o.read_uint16()
    if sz == 0:
        return
    o.skip_bytes(sz)




def main():
    # connect to db
    conn = pymysql.connect(host='172.31.248.17', port=3306, user='dev',passwd='dev', db='dev_world', charset='gbk')
    cur = conn.cursor()
    cur.execute("select id, bin1 from player_data where id = '1570028430'")

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

    deserialize_props_ext(o)
    deserialize_item(o)
    deserialize_pet(o)
    deserialize_quest(o)
    deserialize_app(o)
    deserialize_friend(o)
    deserialize_mad(o)
    deserialize_aura(o)
    deserialize_spell(o)
    deserialize_shortcuts(o)
    deserialize_dialog(o)
    deserialize_varblock(o)
    
    print("after varblock")    
    o.print_offset()

    deserialize_script_table(o)

    print("after table")    
    o.print_offset()

    deserialize_patch(o)
    deserialize_record_value(o)
    deserialize_exp_fix(o)
    deserialize_prop_ext_1(o)
    deserialize_only_event(o)
    deserialize_class(o)
    deserialize_var_props(o)

    cur.close()
    conn.close()





if __name__ == "__main__":
    main()
