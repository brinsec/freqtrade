# SQL 帮助

如果您想查询您的 sqlite 数据库，本页包含一些帮助。

!!! Tip "其他数据库系统"
    要使用其他数据库系统（如 PostgreSQL 或 MariaDB），您可以使用相同的查询，但需要使用相应数据库系统的客户端。[点击此处](advanced-setup.md#use-a-different-database-system)了解如何为 freqtrade 设置不同的数据库系统。

!!! Warning "警告"
    如果您不熟悉 SQL，在数据库上运行查询时应非常小心。
    在运行任何查询之前，请始终确保对数据库进行了备份。

## 安装 sqlite3

Sqlite3 是基于终端的 sqlite 应用程序。
如果您觉得更舒适，可以随意使用像 SqliteBrowser 这样的可视化数据库编辑器。

### Ubuntu/Debian installation

```bash
sudo apt-get install sqlite3
```

### Using sqlite3 via docker

The freqtrade docker image does contain sqlite3, so you can edit the database without having to install anything on the host system.

``` bash
docker compose exec freqtrade /bin/bash
sqlite3 <database-file>.sqlite
```

## Open the DB

```bash
sqlite3
.open <filepath>
```

## Table structure

### List tables

```bash
.tables
```

### Display table structure

```bash
.schema <table_name>
```

### Get all trades in the table

```sql
SELECT * FROM trades;
```

## Destructive queries

Queries that write to the database.
These queries should usually not be necessary as freqtrade tries to handle all database operations itself - or exposes them via API or telegram commands.

!!! Warning
    Please make sure you have a backup of your database before running any of the below queries.

!!! Danger
    You should also **never** run any writing query (`update`, `insert`, `delete`) while a bot is connected to the database.
    This can and will lead to data corruption - most likely, without the possibility of recovery.

### Fix trade still open after a manual exit on the exchange

!!! Warning
    Manually selling a pair on the exchange will not be detected by the bot and it will try to sell anyway. Whenever possible, /forceexit <tradeid> should be used to accomplish the same thing.  
    It is strongly advised to backup your database file before making any manual changes.

!!! Note
    This should not be necessary after /forceexit, as force_exit orders are closed automatically by the bot on the next iteration.

```sql
UPDATE trades
SET is_open=0,
  close_date=<close_date>,
  close_rate=<close_rate>,
  close_profit = close_rate / open_rate - 1,
  close_profit_abs = (amount * <close_rate> * (1 - fee_close) - (amount * (open_rate * (1 - fee_open)))),
  exit_reason=<exit_reason>
WHERE id=<trade_ID_to_update>;
```

#### Example

```sql
UPDATE trades
SET is_open=0,
  close_date='2020-06-20 03:08:45.103418',
  close_rate=0.19638016,
  close_profit=0.0496,
  close_profit_abs = (amount * 0.19638016 * (1 - fee_close) - (amount * (open_rate * (1 - fee_open)))),
  exit_reason='force_exit'  
WHERE id=31;
```

### Remove trade from the database

!!! Tip "Use RPC Methods to delete trades"
    Consider using `/delete <tradeid>` via telegram or rest API. That's the recommended way to deleting trades.

If you'd still like to remove a trade from the database directly, you can use the below query.

!!! Danger
    Some systems (Ubuntu) disable foreign keys in their sqlite3 packaging. When using sqlite - please ensure that foreign keys are on by running `PRAGMA foreign_keys = ON` before the above query.

```sql
DELETE FROM trades WHERE id = <tradeid>;

DELETE FROM trades WHERE id = 31;
```

!!! Warning
    This will remove this trade from the database. Please make sure you got the correct id and **NEVER** run this query without the `where` clause.
