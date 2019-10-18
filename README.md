# fluentdMysql

Dump fluentd logs into mySQL.

## Versions

-   [Python v3.6+](https://www.python.org)
-   [Fluentd v1.7](https://www.fluentd.org)
-   [fluent-plugin-mysql](https://github.com/tagomoris/fluent-plugin-mysql)
-   [mysql2](https://github.com/brianmario/mysql2)

## Build and run fluentd container

```bash
# Build the container
docker build -t fluentd .

# Start container
docker run --rm -it --name fluentd -p 24224:24224 -p 8888:8888 -v PATH_TO_FOLDER/log:/fluentd/log fluentd
```

## Conf builder (optional)

If you have large database, you can use this python script to auto generate the conf file. This script will:

1. Login into mySQL database
2. Grab all the tables and columns
3. Generate fluent.conf file:

```xml
<match {FLUENT_TAG}.{TABLE_NAME}>
    @type mysql_bulk
    host {DB_HOST}
    database {DB_DB}
    username {DB_USER}
    password {DB_PWD}
    column_names {COLUMN_NAMES comma separated}
    table {TABLE_NAME}
    flush_interval {DB_FLUSH_INTERVAL}s
</match>
```

```bash
# Make sure to have installed python3 and mysql-connector-python
pip3 install mysql-connector-python

python3 fluentd_conf_builder.py
```

## Testing

```js
// node.JS

const logger = require("fluent-logger");

logger.configure("log", {
    host: "localhost",
    port: 24224,
    timeout: 3.0,
    reconnectInterval: 600000
});

logger.emit("table1", { colA: 1, colB: 2, colC: 3 });
logger.emit("table2", { colA: 1, colB: 2, colC: 3 });
```

```bash
# cURL

curl -X GET 'http://localhost:8888/log.table1?json={%22colA%22:%201,%20%22colB%22:%202,%20%22colC%22:%203}'

curl -X GET 'http://localhost:8888/log.table2?json={%22colA%22:%201,%20%22colB%22:%202,%20%22colC%22:%203}'
```
