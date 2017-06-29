import MySQLdb


db_log    = "dev_log"
db_user   = "dev"
db_pass   = "dev"
db_server = "172.31.251.130"   # "172.31.251.130"


user_table = ("moling", "hj", "lw", "zy", "rxj",  "yjh", "fxy", "ly", "zcg", "hkx", "lqy" "zzs", "ylr")


# deal with fy_uname
conn = MySQLdb.connect(host=db_server, user=db_user, passwd=db_pass, db=db_log, charset="utf8")
cur = conn.cursor()
cur.execute("truncate auth")

# add for server side.
for user_name in user_table:
    str_sql = "insert into auth (`acct`, `pwd`) values('{0}', '1');".format(user_name)
    # print(str_sql)
    cur.execute(str_sql)

# add for test.
for x in xrange(0, 1000):
    user_name = "test{0:03d}".format(x)
    str_sql = "insert into auth (`acct`, `pwd`) values('{0}', '1');".format(user_name)
    print(str_sql)
    cur.execute(str_sql)

cur.close()
conn.commit()


raw_input("done! press enter to exit.")