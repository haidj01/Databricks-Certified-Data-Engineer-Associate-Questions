CREATE OR REPLACE STREAMING TABLE target_table(
  id INT,
  product_name STRING,
  ...
  order_time timestamp,
  order_qty INT
  ...
  CONSTRAINT order_time_not_null EXPECT (order_time IS NOT NULL) ON VIOLATION DROP ROW,
  CONSTRAINT valid_qty EXPECT(order_qty >=0) ON VIOLATION DROP ROW,
  CONSTRAINT valid_id EXPECT(id IS NOT NULL) ON VIOLATION FAIL UPDATE
)
COMMENT 'basic syntax for streaming table creation'

CLUSTER BY AUTO --liquid Clustering for optimization

AS

SELECT
...
FROM STREAM source_streaming_table
