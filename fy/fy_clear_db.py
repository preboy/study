import MySQLdb

db_server = "192.168.1.250"
db_user   = "fy"
db_pass   = "fy"
db_world  = "fy_world"
db_uname  = "fy_uname"


# deal with fy_uname
conn = MySQLdb.connect(host=db_server, user=db_user, passwd=db_pass, db=db_uname, charset="utf8")
cur = conn.cursor()
cur.execute("truncate guild_name")
cur.execute("truncate namestore")
cur.close()
conn.commit()



# deal with fy_world
conn = MySQLdb.connect(host=db_server, user=db_user, passwd=db_pass, db=db_world, charset="utf8")
cur = conn.cursor()
cur.execute("truncate guild")
cur.execute("truncate player_cache")
cur.execute("truncate player_data")
cur.execute("truncate player_mbox")
cur.execute("truncate player_stats")
cur.execute("truncate guild")
cur.execute("delete from player")
cur.execute("delete from account")
cur.close()
conn.commit()



print("done")
raw_input("done! press any key to exit.")


