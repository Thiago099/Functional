import mysql.connector
import pandas as pd
import json

class sql:
  def __init__(self, database):
    conn= json.load(open('sql.json'))
    self.mysql = mysql.connector.connect(
      host = conn['host'],
      user = conn['user'],
      password = conn['password'],
      database = database
    )
    self.mysql.autocommit=True
    self.db = self.mysql.cursor()

  def query(self, sql):
    self.db.execute(sql)
    data = self.db.fetchall()
    columns = self.db.column_names
    result = []
    for i in data:
        cur = {}
        for j in range(len(columns)):
            cur[columns[j]] = i[j]
        result.append(cur)
    return result
  
  def query_pd(self, sql):
    self.db.execute(sql)
    df = pd.DataFrame(
        data = self.db.fetchall(),
        columns = self.db.column_names
    )
    if("id" in df.columns):
      df.set_index("id", inplace = True)
    return df

  def run(self, sql):
    self.db.execute(sql)
    return self.db._last_insert_id
  
  def close(self):
    self.mysql.close()
    self.db.close()
  
