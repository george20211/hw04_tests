import sqlite3 as lite
import sys
 
con = lite.connect('db.sqlite3')
 
with con:    
    cur = con.cursor()    
    cur.execute(
        "SELECT * FROM posts_post WHERE id<5"
        )
    rows = cur.fetchall()
 
    for row in rows:
        print (row)
