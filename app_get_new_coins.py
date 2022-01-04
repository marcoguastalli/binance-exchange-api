import os
import sys
from datetime import datetime

from db_client.create_connection import create_connection
from db_client.execute_query import execute_query
from bnc_api_client.get_exchangeInfo import GetExchangeInformation
from db_client.select_query import select_query

DATABASE = "/Users/marcoguastalli/opt/sqlite/coins.sqlite"
REST_API_ENDPOINT_SANDBOX = "https://testnet.binance.vision"
REST_API_ENDPOINT_PRODUCTION = "https://api.binance.com"
REST_API_ENDPOINT = REST_API_ENDPOINT_SANDBOX


def main():
    init_database(DATABASE)
    conn = create_connection(DATABASE)
    try:
        if conn is not None:
            # call api
            url = REST_API_ENDPOINT + '/api/v3/exchangeInfo'
            print("Reading exchange information from API url '%s' at '%s'" % (url, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")))
            exchange_info = GetExchangeInformation(url)
            response = exchange_info.do_get()
            # parse response
            symbols_dictionary = exchange_info.parse_response(response)
            for symbol in symbols_dictionary:
                symbol_item = symbols_dictionary.get(symbol)
                # read SQLite table 'new_coins' and get existing symbol
                symbol_in_ddbb = select_query(conn, f"SELECT symbol FROM new_coins WHERE symbol = '{symbol}'")
                if symbol_in_ddbb is not None and len(symbol_in_ddbb) > 0:
                    print(f"{symbol} already exists in DDBB")
                else:
                    # insert new symbol
                    created = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                    query_insert = f"INSERT INTO new_coins (symbol, base_asset, quote_asset, status, created) " \
                                   f"VALUES ('{symbol}', '{symbol_item['baseAsset']}', '{symbol_item['quoteAsset']}', '{symbol_item['status']}', '{created}')"
                    execute_query(conn, query_insert)
                    print(f"NEW symbol: {symbol}  -->  {symbol_item['baseAsset']}_{symbol_item['quoteAsset']}  -->  status: {symbol_item['status']}")
            # commit
            conn.commit()
        else:
            print("Error Connection to DDBB:" + database)
    finally:
        if conn is not None:
            conn.close()


def init_database(database: str):
    conn = create_connection(database)
    try:
        if conn is not None:
            # check for previously created table
            table_already_exists = select_query(conn, f"SELECT symbol FROM new_coins")
            if table_already_exists is not None:
                print(f"table already exists {table_already_exists}")
            else:
                print(f"table does not exist {table_already_exists}")
                # drop table
                # execute_query(conn, "DROP TABLE IF EXISTS new_coins")
                # conn.commit()
                # create table
                sql_create_table = '''CREATE TABLE IF NOT EXISTS new_coins (
                                             symbol TEXT PRIMARY KEY NOT NULL,
                                             base_asset TEXT NOT NULL,
                                             quote_asset TEXT NOT NULL,
                                             status TEXT NOT NULL,
                                             created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                             updated TEXT NOT NULL DEFAULT "")'''
                execute_query(conn, sql_create_table)
                conn.commit()
        else:
            print("Error Connection to DDBB:" + database)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os.error()
