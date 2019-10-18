#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This script will:
1. Login into mySQL database
2. Grab all the tables and columns
3. Generate fluent.conf file:
    <match {FLUENT_TAG}.{TABLE_NAME}>
    @type mysql_bulk
    host {DB_HOST}
    database {DB_DB}
    username {DB_USER}
    password {DB_PWD}
    column_names {COLUMN_NAMES}
    table {TABLE_NAME}
    flush_interval {DB_FLUSH_INTERVAL}s
    </match>

Install mysql connector macOS: pip3 install mysql-connector-python
"""

import os
import mysql.connector
import json

DB_HOST = "localhost"
DB_USER = "root"
DB_PWD = "root"
DB_DB = "mydb"
DB_FLUSH_INTERVAL = 60

FLUENTD_TAG = "log"


def db_conn():
    """Connect to database"""
    db = mysql.connector.connect(user=DB_USER, password=DB_PWD, host=DB_HOST)
    cursor = db.cursor()

    return db, cursor


def get_columns(table):
    """Get all columns from table"""

    columns = []

    sql = "SHOW COLUMNS FROM mydb.{}".format(table)
    cursor.execute(sql)
    for row in cursor.fetchall():
        if row[0] != "id":
            columns.append(row[0])

    return ",".join(columns)


def get_tables():
    """Get all tables from database"""

    tables = {}
    sql = "SHOW tables FROM {}".format(DB_DB)
    cursor.execute(sql)
    for table, in cursor.fetchall():
        tables[table] = get_columns(table)

    return tables


def gen_conf():
    source = [
        "<source>",
        "  @type forward",
        "  port 24224",
        "  bind 0.0.0.0",
        "</source>"
    ]
    source = "\n".join(source)

    tables = get_tables()
    matches = []
    for table in tables:
        match = [
            "<match {}.{}>".format(FLUENTD_TAG, table),
            "  @type mysql_bulk",
            "  host {}".format(DB_HOST),
            "  database {}".format(DB_DB),
            "  username {}".format(DB_USER),
            "  password {}".format(DB_PWD),
            "  column_names {}".format(table),
            "  table {}".format(table),
            "  flush_interval {}s".format(DB_FLUSH_INTERVAL),
            "</match>"
        ]
        match = "\n".join(match)

        matches.append(match)
    matches = "\n".join(matches)

    conf = "{}\n{}".format(source, matches)

    with open("{}/fluent.conf".format(path), "w+", encoding="utf8") as f:
        f.write(conf)

    print(conf)


if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    db, cursor = db_conn()

    gen_conf()
