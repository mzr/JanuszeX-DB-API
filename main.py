#!/usr/bin/python3
import json
import psycopg2
import sys
import argparse

# czy potrzebne?
import secrets
import hashlib
import codecs

# https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04
# http://www.davejsaunders.com/2016/11/10/user-authentication-with-postgres.html

def make_hash(pt_password):
    salt = secrets.token_bytes(16)
    hashed_salted_pass_hex = hashlib.sha256(pt_password + salt).hexdigest()
    return (salt.hex(), hashed_salted_pass_hex)

class JanuszeXAPI:
    conn = None

    def __init__(self, need_db_init=False):
        self.need_db_init = need_db_init

    def api_call(self, name, args):
        return getattr(self, name)(args)

    def connect(self, login, password, db_name):
        try:
            # jesli user jest "init" to chyba jest to pierwsze uruchomienie
            connect_str = "dbname='{}' user='{}' host='{}' password='{}'" \
                .format(db_name, login, 'localhost', password)
            self.conn = psycopg2.connect(connect_str)
        except Exception as e:
            print(e)

    def disconnect(self):
        self.conn.close()

    def initialize_db(self):
        with self.conn.cursor() as cursor:
            cursor.execute(open("schema.sql", "r").read())

    def authenticate(self, login, password):
        # hash + salt compare
        return False

    def api_return(self, status, data=None):
        r = { 'status' : status }
        if data == None:
            return  r
        r['data'] = data
        return r

    ''' KorpoX API calls begin here '''

    def open(self, args):
        self.connect(args['login'], args['password'], args['baza'])
        if self.need_db_init:
            self.initialize_db()
            self.need_db_init = False
        return self.api_return("OK")


    def root(self, args):
        return self.api_return("OK")

    def new(self, args):
        return self.api_return("OK")

    def remove(self, args):
        return self.api_return("OK")

    def child(self, args):
        return self.api_return("OK")

    def parent(self, args):
        return self.api_return("OK")

    def ancestors(self, args):
        return self.api_return("OK")

    def descendants(self, args):
        return self.api_return("OK")

    def ancestor(self, args):
        return self.api_return("OK")

    def read(self, args):
        return self.api_return("OK")

    def update(self, args):
        return self.api_return("OK")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='JanuszeX DB API')
    parser.add_argument('-init', action='store_true', help='initialize database')

    args = parser.parse_args()

    if args.init:
        init_db = True

    api = JanuszeXAPI(init_db)

    for line in sys.stdin:
        cmd = json.loads(line)
        cmd_name = list(cmd.keys())[0]
        rtn = getattr(api, cmd_name)(cmd[cmd_name]) # albo api.api_call(command_type, command[command_type]) 
        print(rtn)
