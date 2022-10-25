import psycopg2

# from main import read_config


class UploaderDB:
  def __init__(self, cfgdir=None):
    # if cfgdir:
    #   cfg = read_config(cfgdir)
    # else:
    #   cfg = read_config()

    # host = cfg.config["PSQL_HOST"]
    # password = cfg.config["PSQL_PASSWORD"]
    # dbname = cfg.config["PSQL_DBNAME"]
    # user = cfg.config["PSQL_USER"]
    host = "cpsc419db.clivpnbj4oho.us-east-1.rds.amazonaws.com"
    password = "08039797Wsj"
    dbname = "cpsc419db"
    user = "postgres"

    self.connect_to_db(host, password, dbname, user)

  def connect_to_db(self, host, password, dbname, user):
    try:
      self.conn = psycopg2.connect(host=host,
                                   user=user,
                                   dbname=dbname,
                                   password=password)
      self.conn.autocommit = True
      print("Success connect to db!")
    except Exception as e:
      print(e)
      print("*******Failed connect to db!*******")
      exit()

  def close(self):
    if self.conn:
      self.conn.close()
