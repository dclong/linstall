CREATE TABLE `db1`.`table1` (
    `item_id` DECIMAL(18, 0),
    `site_id` DECIMAL(4, 0),
    `user_id` DECIMAL(18, 0)
) USING parquet
OPTIONS (
  `compression` 'snappy',
  `serialization.format` '1',
  path '/sys/edw/snt/db1/snt/table1/snapshot/dt=20200709'
)
