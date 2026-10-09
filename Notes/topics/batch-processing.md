# Batch Processing

**Category:** Data Processing
**Last Updated:** 2026-09-09

## Overview

Batch processing in Databricks for efficient data transformation and loading.

**Cross-Reference:** See [Databricks_Data_Engineering_Concepts.md](../Databricks_Data_Engineering_Concepts.md#2-batch-vs-streaming-data-processing)

## COPY INTO Command

**README Q12: Why might COPY INTO not work?**

### Overview

COPY INTO is an **idempotent batch ingestion command** that loads data from cloud object storage into Delta Lake tables. It automatically tracks loaded files in the Delta transaction log, preventing duplicate processing.

**Key Characteristics:**
- **Idempotent:** Running multiple times loads only new files
- **File tracking:** Delta log records processed file paths
- **Schema evolution:** Supports mergeSchema option
- **Cloud-native:** Works with S3, ADLS, GCS
- **Validation:** VALIDATE mode for testing before load

Documentation: https://docs.databricks.com/sql/language-manual/delta-copy-into.html

### Complete Syntax

```sql
COPY INTO [catalog.]schema.table_name
FROM 'cloud_storage_path'
FILEFORMAT = { CSV | JSON | AVRO | ORC | PARQUET | TEXT | BINARYFILE }
[ FORMAT_OPTIONS ( 'key' = 'value' [, ...] ) ]
[ COPY_OPTIONS ( 'key' = 'value' [, ...] ) ]
[ VALIDATE { ALL | n ROWS } ];
```

### Basic Examples

**Parquet (simplest case):**
```sql
COPY INTO target_table
FROM 'abfss://container@account.dfs.core.windows.net/path/'
FILEFORMAT = PARQUET;
```

**CSV with headers:**
```sql
COPY INTO sales_bronze
FROM 's3://mybucket/raw/sales/'
FILEFORMAT = CSV
FORMAT_OPTIONS (
  'header' = 'true',
  'delimiter' = ',',
  'inferSchema' = 'true'
);
```

**JSON with schema evolution:**
```sql
COPY INTO events_bronze
FROM 'gs://my-bucket/events/'
FILEFORMAT = JSON
FORMAT_OPTIONS ('mergeSchema' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true');
```

### FORMAT_OPTIONS Reference

**CSV Options:**
```sql
FORMAT_OPTIONS (
  'header' = 'true',           -- First row contains column names
  'delimiter' = ',',           -- Field separator (default: ,)
  'quote' = '"',               -- Quote character (default: ")
  'escape' = '\\',             -- Escape character (default: \)
  'nullValue' = 'NULL',        -- String representing NULL
  'dateFormat' = 'yyyy-MM-dd', -- Date parsing format
  'timestampFormat' = 'yyyy-MM-dd HH:mm:ss', -- Timestamp format
  'inferSchema' = 'true',      -- Automatically detect types
  'encoding' = 'UTF-8'         -- Character encoding
);
```

**JSON Options:**
```sql
FORMAT_OPTIONS (
  'multiLine' = 'true',        -- JSON object spans multiple lines
  'allowComments' = 'true',    -- Allow // and /* */ comments
  'dateFormat' = 'yyyy-MM-dd',
  'timestampFormat' = 'yyyy-MM-dd HH:mm:ss',
  'mergeSchema' = 'true'       -- Enable schema evolution
);
```

**Parquet/Avro/ORC Options:**
```sql
FORMAT_OPTIONS (
  'mergeSchema' = 'true'       -- Merge new columns into table schema
);
```

### COPY_OPTIONS Reference

```sql
COPY_OPTIONS (
  'mergeSchema' = 'true',      -- REQUIRED: Must match FORMAT_OPTIONS
  'force' = 'false'            -- Reload already processed files (default: false)
);
```

**CRITICAL:** For schema evolution, `mergeSchema` must be set in **BOTH** FORMAT_OPTIONS **AND** COPY_OPTIONS:

```sql
-- CORRECT: mergeSchema in both places
COPY INTO table
FROM 'path/'
FILEFORMAT = JSON
FORMAT_OPTIONS ('mergeSchema' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true');

-- WRONG: mergeSchema only in FORMAT_OPTIONS
COPY INTO table
FROM 'path/'
FILEFORMAT = JSON
FORMAT_OPTIONS ('mergeSchema' = 'true');  -- Schema won't evolve!
```

### Force Option (Reprocessing Files)

By default, COPY INTO skips already-processed files. Use `force = 'true'` to reload:

```sql
COPY INTO table
FROM 'path/'
FILEFORMAT = PARQUET
COPY_OPTIONS ('force' = 'true');  -- ⚠️ Reprocesses ALL files
```

**Use Cases for force:**
- Source data corrected/updated
- Initial load failed midway
- Schema changed and need full reload

**Risks:**
- **Duplicate data** if table doesn't have unique constraints
- **Performance impact** for large datasets
- **Cost increase** from reprocessing

**Safe Pattern with force:**
```sql
-- Reload into temporary table
COPY INTO temp_table
FROM 'path/'
FILEFORMAT = PARQUET
COPY_OPTIONS ('force' = 'true');

-- Deduplicate and merge
MERGE INTO production_table t
USING (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY id ORDER BY updated_at DESC) AS rn
  FROM temp_table
) s
ON t.id = s.id AND s.rn = 1
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

### VALIDATE Mode (Dry Run)

Test COPY INTO without loading data:

```sql
-- Validate all files
COPY INTO target_table
FROM 's3://bucket/path/'
FILEFORMAT = JSON
VALIDATE ALL;

-- Validate first 100 rows
COPY INTO target_table
FROM 's3://bucket/path/'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true')
VALIDATE 100 ROWS;
```

**Output:**
```
file_path                  | num_rows_parsed | num_errors | error_details
---------------------------+-----------------+------------+---------------
s3://bucket/file1.json     | 1000            | 0          | NULL
s3://bucket/file2.json     | 500             | 2          | Invalid JSON on line 45, 67
```

**Use VALIDATE to check:**
- Schema compatibility
- Data format correctness
- File accessibility
- Permissions

### Idempotent Ingestion Pattern

COPY INTO tracks loaded files in the Delta transaction log:

```sql
-- First run: Loads file1.parquet, file2.parquet
COPY INTO orders
FROM 's3://bucket/orders/'
FILEFORMAT = PARQUET;
-- Loaded: 2 files, 10,000 rows

-- New file arrives: file3.parquet

-- Second run: Only loads file3.parquet (files 1-2 skipped)
COPY INTO orders
FROM 's3://bucket/orders/'
FILEFORMAT = PARQUET;
-- Loaded: 1 file, 5,000 rows
```

**How it works:**
1. COPY INTO reads source path
2. Checks Delta log for previously loaded file paths
3. Filters out already-processed files
4. Loads only new files
5. Records new file paths in transaction log

**File Tracking Storage:**
```sql
-- View loaded files in Delta log
DESCRIBE HISTORY orders;

-- Check transaction details
SELECT operationParameters.path
FROM (DESCRIBE HISTORY orders)
WHERE operation = 'COPY INTO';
```

### Partitioned Source Paths

Improve performance with partitioned cloud storage:

```sql
-- Partition-aware loading
COPY INTO sales
FROM 's3://bucket/sales/year=2026/month=09/'
FILEFORMAT = PARQUET;

-- Pattern matching (loads all partitions)
COPY INTO sales
FROM 's3://bucket/sales/'
PATTERN = 'year=202[5-6]/month=*/data-*.parquet'
FILEFORMAT = PARQUET;
```

### Why COPY INTO Might Fail (README Q12)

**Answer:**

1. **Idempotent loading only** - Doesn't work if you need to reprocess same files (use `force = 'true'`)
2. **File format issues** - Incorrect FORMAT_OPTIONS (e.g., wrong delimiter, missing header)
3. **Schema mismatch** - Target schema incompatible with source (use `mergeSchema = 'true'`)
4. **Permissions** - No READ access to cloud storage path
5. **Path not accessible** - Cloud storage credentials missing or incorrect
6. **File corruption** - Malformed files in source path
7. **Target table doesn't exist** - Must CREATE TABLE first
8. **Missing mergeSchema in COPY_OPTIONS** - Schema evolution fails if only in FORMAT_OPTIONS

### Best Practices

```sql
-- ✅ Production pattern
COPY INTO bronze.orders
FROM 'abfss://raw@storage.dfs.core.windows.net/orders/'
FILEFORMAT = PARQUET
FORMAT_OPTIONS ('mergeSchema' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true');

-- ✅ Validate before loading
COPY INTO bronze.orders
FROM 'abfss://raw@storage.dfs.core.windows.net/orders/'
FILEFORMAT = PARQUET
VALIDATE ALL;  -- Test first

-- Then run actual load
COPY INTO bronze.orders
FROM 'abfss://raw@storage.dfs.core.windows.net/orders/'
FILEFORMAT = PARQUET;
```

**Use COPY INTO when:**
- Incremental file ingestion from cloud storage
- Batch loading with idempotency guarantees
- Schema evolution required
- Files arrive periodically (hourly, daily)
- Need file-level tracking

**Don't use COPY INTO when:**
- Need to process same file multiple times (use Spark reads)
- Streaming semantics needed (use Auto Loader)
- Complex transformations required (use Spark DataFrame API)
- Sub-second latency required (use Structured Streaming)
- Billions of small files (use Auto Loader with file notification)

## INSERT OVERWRITE

**README Q10: Considerations**

### Syntax

```sql
INSERT OVERWRITE TABLE target_table
SELECT * FROM source_table;

-- Partition-level overwrite
INSERT OVERWRITE TABLE target_table
PARTITION (year = 2026, month = 9)
SELECT * FROM source_table
WHERE year = 2026 AND month = 9;
```

### Considerations

1. **Data deletion** - Existing data is completely removed
2. **Not atomic** - Old data deleted before new data written
3. **No recovery** - Can't undo without backup/time travel
4. **Partition awareness** - Static vs. dynamic partitioning
5. **Schema must match** - Or use schema evolution

**Risks:**
- Accidental data loss
- Concurrent read failures
- Incomplete writes leave table empty

**Alternatives:**
```sql
-- Safer: Use MERGE
MERGE INTO target USING source
ON target.id = source.id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;

-- Or: TRUNCATE then INSERT
TRUNCATE TABLE target_table;
INSERT INTO target_table SELECT * FROM source_table;
```

**Cross-Reference:** See [Delta Lake](delta-lake.md) for MERGE operations

## MERGE Operations

### Upsert Pattern

```sql
MERGE INTO customers t
USING updates s
ON t.customer_id = s.customer_id
WHEN MATCHED THEN
  UPDATE SET *
WHEN NOT MATCHED THEN
  INSERT *;
```

### Conditional Updates

```sql
MERGE INTO inventory t
USING changes s
ON t.product_id = s.product_id
WHEN MATCHED AND s.action = 'update' THEN
  UPDATE SET quantity = s.quantity
WHEN MATCHED AND s.action = 'delete' THEN
  DELETE
WHEN NOT MATCHED THEN
  INSERT *;
```

### CDC Pattern

```sql
MERGE INTO target t
USING cdc_source s
ON t.id = s.id
WHEN MATCHED AND s.op = 'D' THEN
  DELETE
WHEN MATCHED AND s.op = 'U' THEN
  UPDATE SET *
WHEN NOT MATCHED AND s.op = 'I' THEN
  INSERT *;
```

**Cross-Reference:** See [CDC & SCD](cdc-scd.md)

## Batch vs. Streaming

**From [Databricks_Data_Engineering_Concepts.md:78](../Databricks_Data_Engineering_Concepts.md:78)**

### Batch Semantics

**Advantages:**
- Simple logic
- Always accurate
- All data visible

**Disadvantages:**
- Reprocesses data
- Higher latency (hours to minutes)
- Inefficient for large datasets

**Tools:**
- Materialized view flows
- Apache Spark batch APIs

### When to Use Batch

**From [Databricks_Data_Engineering_Concepts.md:114](../Databricks_Data_Engineering_Concepts.md:114)**

**Bronze Layer:**
- Batch acceptable for scheduled ingestion
- Streaming preferred for continuous ingestion

**Silver Layer:**
- **Batch with incremental refresh** (recommended)
- Streaming only when latency > accuracy

**Gold Layer:**
- **Batch processing** for aggregations
- Materialized views for precomputation

## Incremental Processing

Incremental processing loads only new or changed data since the last run, avoiding full table scans and reprocessing.

### JDBC Cursor-Based Pattern

Load only new rows from relational databases using a cursor column (timestamp or auto-incrementing ID):

```python
# Get last loaded value from checkpoint table
last_load_ts = spark.read.format("delta") \
  .load("/mnt/bronze/customers") \
  .agg({"updated_at": "max"}) \
  .collect()[0][0]

# Or from checkpoint metadata
# last_load_ts = spark.sql("SELECT MAX(checkpoint_value) FROM checkpoints WHERE table_name = 'customers'").first()[0]

# JDBC incremental read with WHERE clause in dbtable subquery
df = spark.read \
  .format("jdbc") \
  .option("url", "jdbc:postgresql://db.example.com:5432/mydb") \
  .option("user", dbutils.secrets.get("db-scope", "db-user")) \
  .option("password", dbutils.secrets.get("db-scope", "db-password")) \
  .option("dbtable", f"(SELECT * FROM customers WHERE updated_at > '{last_load_ts}') AS incremental") \
  .option("driver", "org.postgresql.Driver") \
  .load()

# Append new data to Delta table
df.write \
  .format("delta") \
  .mode("append") \
  .save("/mnt/bronze/customers")
```

**Key Points:**
- Cursor column must be indexed in source database for performance
- Use `dbtable` with subquery to push down WHERE filter
- Store last loaded value in checkpoint table or metadata
- Common cursor columns: `updated_at`, `created_at`, `row_id`, `version`

**JDBC Options:**
```python
{
  "url": "jdbc:postgresql://host:port/database",
  "dbtable": "(SELECT * FROM table WHERE id > 1000) AS q",
  "user": "username",
  "password": "password",
  "driver": "org.postgresql.Driver",
  "fetchsize": "10000",            # Rows per fetch (default 10)
  "numPartitions": "8",            # Parallel JDBC connections
  "partitionColumn": "id",         # Column for partitioning
  "lowerBound": "1",               # Min value for partitioning
  "upperBound": "1000000"          # Max value for partitioning
}
```

### Timestamp-Based Incremental Loading

Load data based on event timestamps with checkpoint tracking:

```python
from pyspark.sql.functions import col, max as spark_max

# Read checkpoint from control table
checkpoint = spark.sql("""
  SELECT MAX(checkpoint_timestamp) AS last_ts
  FROM control.checkpoints
  WHERE pipeline_name = 'sales_ingestion'
""").first()

last_ts = checkpoint['last_ts'] if checkpoint['last_ts'] else '1970-01-01 00:00:00'

# Read only new data from source
df = spark.read.format("delta").load("/mnt/raw/sales") \
  .filter(col("event_timestamp") > last_ts)

# Process and write to target
df.write \
  .format("delta") \
  .mode("append") \
  .save("/mnt/bronze/sales")

# Update checkpoint with max timestamp processed
new_checkpoint = df.agg(spark_max("event_timestamp")).first()[0]
spark.sql(f"""
  INSERT INTO control.checkpoints (pipeline_name, checkpoint_timestamp, processed_at)
  VALUES ('sales_ingestion', '{new_checkpoint}', current_timestamp())
""")
```

**Checkpoint Table Schema:**
```sql
CREATE TABLE IF NOT EXISTS control.checkpoints (
  pipeline_name STRING,
  checkpoint_timestamp TIMESTAMP,
  processed_at TIMESTAMP,
  rows_processed BIGINT,
  status STRING
)
USING DELTA
PARTITIONED BY (pipeline_name);
```

### Delta Table Time Travel (Version-Based)

Use Delta table versions for incremental processing:

```python
# Get last processed version from metadata
last_version = spark.sql("""
  SELECT MAX(processed_version)
  FROM control.delta_checkpoints
  WHERE table_name = 'source_table'
""").first()[0]

# Read only changes since last version
df = spark.read.format("delta") \
  .option("versionAsOf", last_version + 1) \
  .load("/mnt/source_table")

# Process incremental data
processed_df = df.transform(apply_transformations)

# Write to target
processed_df.write.format("delta").mode("append").save("/mnt/target_table")

# Update checkpoint
current_version = spark.sql("DESCRIBE HISTORY delta.`/mnt/source_table`").first()['version']
spark.sql(f"""
  INSERT INTO control.delta_checkpoints
  VALUES ('source_table', {current_version}, current_timestamp())
""")
```

### File-Based Incremental with Modification Time

Track processed files by modification timestamp:

```python
import datetime
from pyspark.sql.functions import input_file_name

# Get last processed file timestamp
last_file_time = spark.sql("""
  SELECT MAX(file_timestamp)
  FROM control.file_checkpoints
  WHERE source_path = '/mnt/raw/events/'
""").first()[0] or datetime.datetime(1970, 1, 1)

# Read files modified after last checkpoint
df = spark.read.format("json").load("/mnt/raw/events/") \
  .withColumn("source_file", input_file_name())

# Filter to only new files (would need to check file mod time via dbutils)
# In production, use Auto Loader for automatic file tracking

# Process and track
df.write.format("delta").mode("append").save("/mnt/bronze/events")

# Update checkpoint with current run time
spark.sql(f"""
  INSERT INTO control.file_checkpoints
  VALUES ('/mnt/raw/events/', current_timestamp())
""")
```

**Better Alternative: Use COPY INTO for file-based incremental:**
```sql
-- COPY INTO automatically tracks processed files
COPY INTO bronze.events
FROM '/mnt/raw/events/'
FILEFORMAT = JSON;
-- Only loads new files, no checkpoint tracking needed
```

### Watermark-Based Pattern (Streaming-like Batch)

Use watermarking for late-arriving data handling:

```python
from pyspark.sql.functions import window, col

# Define watermark tolerance (e.g., 1 hour late data accepted)
watermark_delay = "1 hour"

# Read source with event timestamp
df = spark.read.format("delta").load("/mnt/source") \
  .filter(col("event_timestamp") > last_checkpoint_ts)

# Apply watermark logic manually in batch
# (Actual watermarks are for streaming, this simulates the pattern)
max_event_ts = df.agg({"event_timestamp": "max"}).first()[0]
watermark_ts = max_event_ts - datetime.timedelta(hours=1)

# Process data up to watermark (ignoring very late data)
processed_df = df.filter(col("event_timestamp") <= watermark_ts)

# Write processed data
processed_df.write.format("delta").mode("append").save("/mnt/target")

# Checkpoint at watermark timestamp (not max timestamp)
update_checkpoint(watermark_ts)
```

### Incremental Merge Pattern (Upsert)

Combine incremental read with MERGE for upsert semantics:

```python
# Read incremental changes from source
last_ts = get_checkpoint("customers_sync")

incremental_df = spark.read \
  .format("jdbc") \
  .option("url", jdbc_url) \
  .option("dbtable", f"(SELECT * FROM customers WHERE updated_at > '{last_ts}') AS q") \
  .load()

# Create temp view for MERGE
incremental_df.createOrReplaceTempView("incremental_customers")

# MERGE into target Delta table
spark.sql("""
  MERGE INTO bronze.customers target
  USING incremental_customers source
  ON target.customer_id = source.customer_id
  WHEN MATCHED THEN UPDATE SET *
  WHEN NOT MATCHED THEN INSERT *
""")

# Update checkpoint
new_checkpoint = incremental_df.agg({"updated_at": "max"}).first()[0]
update_checkpoint("customers_sync", new_checkpoint)
```

### Best Practices for Incremental Processing

**Checkpoint Management:**
1. Store checkpoints in reliable storage (Delta table, not local files)
2. Include metadata: timestamp, rows processed, status
3. Atomic checkpoint updates (use transactions)
4. Track both timestamp and version/row count for validation

**Error Handling:**
```python
try:
    # Read incremental data
    df = read_incremental(last_checkpoint)

    # Process
    processed_df = transform(df)

    # Write
    processed_df.write.format("delta").mode("append").save(target_path)

    # Commit checkpoint only after successful write
    update_checkpoint(new_checkpoint_value)

except Exception as e:
    # Do NOT update checkpoint on failure
    log_error(f"Incremental load failed: {e}")
    raise
```

**Idempotency:**
```python
# Ensure reruns produce same results
# Option 1: MERGE with deduplication
MERGE INTO target USING (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY id ORDER BY updated_at DESC) AS rn
  FROM incremental_source
) source
ON target.id = source.id AND source.rn = 1
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *

# Option 2: Overwrite partition (for partitioned tables)
df.write \
  .format("delta") \
  .mode("overwrite") \
  .option("replaceWhere", "date = '2026-09-09'") \
  .save("/mnt/target")
```

**Comparison: Incremental Approaches**

| Approach | Best For | Pros | Cons |
|----------|----------|------|------|
| **COPY INTO** | Cloud object storage files | Automatic file tracking, idempotent, simple | File-level only, no transformations |
| **JDBC Cursor** | Relational databases | Efficient, uses DB indexes | Requires cursor column, network overhead |
| **Timestamp-based** | Any source with timestamps | Flexible, widely applicable | Clock skew issues, late data challenges |
| **Delta Time Travel** | Delta tables | Version history, easy rollback | Storage overhead for versions |
| **Auto Loader** | Cloud storage, millions of files | Scalable, file notification, schema evolution | Streaming semantics (covered separately) |

**Cross-Reference:** See [Streaming](streaming.md) for Auto Loader and continuous incremental processing

## JDBC/ODBC/REST Integration

External data source connectivity for batch ingestion from databases and APIs.

### JDBC (Java Database Connectivity)

JDBC allows Spark to directly read from relational databases as DataFrames, enabling integration with traditional data sources.

#### Supported Databases

- **PostgreSQL** - `org.postgresql.Driver`
- **MySQL/MariaDB** - `com.mysql.jdbc.Driver`
- **SQL Server** - `com.microsoft.sqlserver.jdbc.SQLServerDriver`
- **Oracle** - `oracle.jdbc.driver.OracleDriver`
- **DB2** - `com.ibm.db2.jcc.DB2Driver`
- **Snowflake** - `net.snowflake.spark.snowflake`
- **Redshift** - `com.amazon.redshift.jdbc.Driver`

#### Basic JDBC Connection Pattern

**Full table load:**

```python
# Read entire table from PostgreSQL
df = spark.read \
  .format("jdbc") \
  .option("url", "jdbc:postgresql://db.example.com:5432/mydb") \
  .option("dbtable", "public.customers") \
  .option("user", dbutils.secrets.get(scope="db-credentials", key="db_user")) \
  .option("password", dbutils.secrets.get(scope="db-credentials", key="db_pass")) \
  .option("driver", "org.postgresql.Driver") \
  .load()

# Write to Delta Lake bronze table
df.write \
  .format("delta") \
  .mode("overwrite") \
  .option("mergeSchema", "true") \
  .save("/mnt/bronze/customers")
```

**SQL Server example:**

```python
df = spark.read \
  .format("jdbc") \
  .option("url", "jdbc:sqlserver://server.database.windows.net:1433;database=mydb") \
  .option("dbtable", "dbo.orders") \
  .option("user", dbutils.secrets.get("sqlserver", "username")) \
  .option("password", dbutils.secrets.get("sqlserver", "password")) \
  .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
  .option("encrypt", "true") \
  .option("trustServerCertificate", "false") \
  .load()

df.write.format("delta").mode("append").save("/mnt/bronze/orders")
```

**MySQL example:**

```python
df = spark.read \
  .format("jdbc") \
  .option("url", "jdbc:mysql://mysql.example.com:3306/production") \
  .option("dbtable", "transactions") \
  .option("user", dbutils.secrets.get("mysql", "user")) \
  .option("password", dbutils.secrets.get("mysql", "password")) \
  .option("driver", "com.mysql.jdbc.Driver") \
  .load()
```

#### JDBC Performance Optimization

**Parallel reads with partitioning:**

```python
df = spark.read \
  .format("jdbc") \
  .option("url", jdbc_url) \
  .option("dbtable", "large_table") \
  .option("user", username) \
  .option("password", password) \
  .option("numPartitions", "8") \
  .option("partitionColumn", "id") \
  .option("lowerBound", "1") \
  .option("upperBound", "1000000") \
  .option("fetchsize", "10000") \
  .load()
```

**How partitioning works:**
- Spark creates 8 parallel JDBC connections
- Each partition reads a range: `WHERE id BETWEEN lower AND upper`
- Example: Partition 1 reads `id BETWEEN 1 AND 125000`, Partition 2 reads `id BETWEEN 125001 AND 250000`, etc.
- Significantly faster than single-threaded read

**Best practices:**
- Use numeric `partitionColumn` (int, bigint, long)
- Column should be indexed in source database
- Set `numPartitions` = number of executor cores
- `fetchsize` = 10000 to 100000 for large tables

#### Incremental JDBC with Cursor Columns (Enhanced)

**Pattern 1: Timestamp-based incremental load**

```python
from pyspark.sql.functions import col, max as spark_max

# Get last loaded timestamp from Delta table
last_load_ts = spark.read.format("delta") \
  .load("/mnt/bronze/customers") \
  .agg(spark_max("updated_at")) \
  .collect()[0][0]

# Fallback for first run
if last_load_ts is None:
    last_load_ts = "1970-01-01 00:00:00"

# Read only new/updated rows using subquery
df = spark.read \
  .format("jdbc") \
  .option("url", "jdbc:postgresql://db.example.com:5432/mydb") \
  .option("user", dbutils.secrets.get("db-credentials", "db_user")) \
  .option("password", dbutils.secrets.get("db-credentials", "db_pass")) \
  .option("dbtable", f"(SELECT * FROM customers WHERE updated_at > '{last_load_ts}') AS incremental") \
  .option("driver", "org.postgresql.Driver") \
  .load()

# Append only new rows to Delta table
df.write \
  .format("delta") \
  .mode("append") \
  .save("/mnt/bronze/customers")
```

**Pattern 2: ID-based incremental load (for append-only tables)**

```python
# Get max ID from Delta table
last_id = spark.read.format("delta") \
  .load("/mnt/bronze/transactions") \
  .agg({"transaction_id": "max"}) \
  .collect()[0][0] or 0

# Load only rows with ID > last_id
df = spark.read \
  .format("jdbc") \
  .option("url", jdbc_url) \
  .option("dbtable", f"(SELECT * FROM transactions WHERE transaction_id > {last_id} ORDER BY transaction_id) AS q") \
  .option("user", username) \
  .option("password", password) \
  .load()

df.write.format("delta").mode("append").save("/mnt/bronze/transactions")
```

**Pattern 3: Combined timestamp + ID for reliability**

```python
# Use both timestamp and ID to handle clock skew
checkpoint = spark.sql("""
    SELECT MAX(updated_at) AS last_ts, MAX(id) AS last_id
    FROM delta.`/mnt/bronze/orders`
""").first()

last_ts = checkpoint['last_ts'] or '1970-01-01'
last_id = checkpoint['last_id'] or 0

df = spark.read \
  .format("jdbc") \
  .option("dbtable", f"""
      (SELECT * FROM orders
       WHERE updated_at >= '{last_ts}'
       AND id > {last_id}
       ORDER BY updated_at, id) AS q
  """) \
  .option("url", jdbc_url) \
  .load()
```

**Cursor column requirements:**
- **Indexed** in source database for performance
- **Monotonically increasing** (timestamp, sequence number, auto-increment ID)
- **Never updated** (must be immutable for reliable incremental loading)
- **Not nullable** (NULL values can cause missed records)

**Common cursor column choices:**
- `updated_at TIMESTAMP` - Best for CDC-like scenarios
- `created_at TIMESTAMP` - Good for append-only tables
- `id BIGINT AUTO_INCREMENT` - Reliable for sequential inserts
- `version INT` - For versioned records
- `sequence_number BIGINT` - For event sourcing

#### JDBC Security Best Practices

**Always use Databricks Secrets:**

```python
# ✅ CORRECT: Use dbutils.secrets
username = dbutils.secrets.get(scope="database-creds", key="username")
password = dbutils.secrets.get(scope="database-creds", key="password")

# ❌ WRONG: Never hardcode credentials
username = "admin"  # DO NOT DO THIS
password = "secretpass123"  # DO NOT DO THIS
```

**Create secrets via Databricks CLI:**

```bash
# Create secret scope
databricks secrets create-scope --scope database-creds

# Add secrets
databricks secrets put --scope database-creds --key username
databricks secrets put --scope database-creds --key password
```

**Use SSL/TLS for database connections:**

```python
df = spark.read \
  .format("jdbc") \
  .option("url", "jdbc:postgresql://db.example.com:5432/mydb?ssl=true&sslmode=require") \
  .option("user", dbutils.secrets.get("db", "user")) \
  .option("password", dbutils.secrets.get("db", "pass")) \
  .load()
```

#### JDBC Write Operations

**Write DataFrame to database table:**

```python
# Write to database (use sparingly, Delta is preferred)
df.write \
  .format("jdbc") \
  .option("url", jdbc_url) \
  .option("dbtable", "reporting.summary_table") \
  .option("user", username) \
  .option("password", password) \
  .mode("overwrite") \
  .save()
```

**Note:** Writing to external databases from Databricks is uncommon. Preferred pattern is:
1. Read from database → Delta Lake (bronze)
2. Transform in Databricks (silver/gold)
3. Query results from Delta Lake or SQL Warehouse

### ODBC (Open Database Connectivity)

ODBC is similar to JDBC but supports additional database drivers and platforms.

**ODBC vs JDBC:**
- **JDBC**: Java-based, more common in Spark
- **ODBC**: Broader driver support, C-based
- **In Databricks**: JDBC is preferred for Spark connectivity

**ODBC use cases:**
- Legacy databases without JDBC drivers
- Proprietary systems (Teradata, Vertica, SAP HANA)
- Compatibility with specific enterprise systems

**Configuration (if required):**

```python
# ODBC connection string format
odbc_connection = "Driver={PostgreSQL};Server=db.example.com;Port=5432;Database=mydb;Uid=user;Pwd=pass;"

# Typically accessed via pyodbc or SQL Gateway
import pyodbc
conn = pyodbc.connect(odbc_connection)
```

**Recommendation:** Use JDBC for Spark integration whenever possible. ODBC is available but less common in Databricks workflows.

### REST API Ingestion

Ingest data from RESTful APIs using Python `requests` library and convert to DataFrames.

#### Basic REST API Pattern

```python
import requests
import json
from pyspark.sql import Row

# Fetch data from REST API
url = "https://api.example.com/v1/events"
headers = {
    "Authorization": f"Bearer {dbutils.secrets.get(scope='api-keys', key='events-api-token')}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
response.raise_for_status()  # Raise exception for 4xx/5xx errors

# Parse JSON response
data = response.json()["results"]  # Assuming response format: {"results": [...]}

# Convert to Spark DataFrame
df = spark.createDataFrame([Row(**row) for row in data])

# Write to Delta Lake
df.write \
  .format("delta") \
  .mode("append") \
  .save("/mnt/bronze/api_events")
```

#### Paginated API Pattern

**Handle APIs with pagination:**

```python
import requests
from pyspark.sql import Row

all_data = []
url = "https://api.example.com/v1/customers"
headers = {"Authorization": f"Bearer {dbutils.secrets.get('api', 'token')}"}

# Paginate through all pages
while url:
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    page_data = response.json()
    all_data.extend(page_data["results"])

    # Get next page URL (API-dependent)
    url = page_data.get("next_page_url")  # or page_data.get("links", {}).get("next")

    # Rate limiting
    import time
    time.sleep(0.1)  # 100ms delay between requests

# Convert all data to DataFrame
df = spark.createDataFrame([Row(**row) for row in all_data])
df.write.format("delta").mode("overwrite").save("/mnt/bronze/customers")
```

#### REST API with Query Parameters

**Filter API results:**

```python
import requests
from datetime import datetime, timedelta

# Get data from last 24 hours
since_timestamp = (datetime.now() - timedelta(days=1)).isoformat()

params = {
    "since": since_timestamp,
    "limit": 1000,
    "status": "active"
}

response = requests.get(
    "https://api.example.com/v1/orders",
    headers={"Authorization": f"Bearer {dbutils.secrets.get('api', 'token')}"},
    params=params
)

data = response.json()["orders"]
df = spark.createDataFrame([Row(**row) for row in data])
df.write.format("delta").mode("append").save("/mnt/bronze/orders")
```

#### REST API Error Handling

**Production-ready pattern with retries:**

```python
import requests
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def create_session_with_retries():
    """Create requests session with automatic retries"""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,  # Wait 1, 2, 4 seconds between retries
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

# Use session with retries
session = create_session_with_retries()

try:
    response = session.get(
        "https://api.example.com/v1/data",
        headers={"Authorization": f"Bearer {dbutils.secrets.get('api', 'token')}"},
        timeout=30
    )
    response.raise_for_status()

    data = response.json()
    df = spark.createDataFrame([Row(**row) for row in data])
    df.write.format("delta").mode("append").save("/mnt/bronze/api_data")

except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
    raise
except requests.exceptions.Timeout:
    print("Request timed out")
    raise
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
    raise
```

#### REST API Best Practices

**Security:**
```python
# ✅ Store API keys in Databricks Secrets
api_key = dbutils.secrets.get(scope="api-credentials", key="production-api-key")

# ❌ Never hardcode API keys
api_key = "sk-1234567890abcdef"  # DO NOT DO THIS
```

**Rate Limiting:**
```python
import time

# Respect API rate limits
for page in range(total_pages):
    response = requests.get(url, headers=headers)
    data = response.json()

    # Sleep to avoid rate limits (e.g., 10 requests per second)
    time.sleep(0.1)
```

**Schema Inference:**
```python
# Explicit schema for production (better than inference)
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType

schema = StructType([
    StructField("id", IntegerType(), False),
    StructField("name", StringType(), True),
    StructField("created_at", TimestampType(), True),
    StructField("status", StringType(), True)
])

df = spark.createDataFrame([Row(**row) for row in data], schema=schema)
```

### Lakeflow Connect (Managed Connectors)

**Recommended for enterprise SaaS and database systems.**

Lakeflow Connect provides **managed, production-ready connectors** for popular enterprise systems, eliminating the need for custom JDBC/REST code.

#### Supported Systems

**Enterprise SaaS:**
- Salesforce
- ServiceNow
- Workday
- NetSuite
- SAP
- Google Analytics
- Adobe Analytics

**Databases:**
- Oracle
- SQL Server
- PostgreSQL
- MySQL
- MongoDB
- Cassandra

**Cloud Platforms:**
- AWS RDS
- Azure SQL Database
- Google Cloud SQL

#### Why Use Lakeflow Connect

**Built-in capabilities:**
- **Change Data Capture (CDC)** - Automatic incremental loading
- **Schema evolution** - Handles source schema changes
- **Credential management** - Secure authentication
- **Error handling** - Automatic retries and logging
- **Monitoring** - Built-in metrics and alerts
- **Performance** - Optimized for each source system

**Configuration example (conceptual):**

```python
# Lakeflow Connect configuration (via UI or API)
{
  "connector_type": "salesforce",
  "source": {
    "instance_url": "https://company.salesforce.com",
    "username": dbutils.secrets.get("salesforce", "username"),
    "password": dbutils.secrets.get("salesforce", "password"),
    "security_token": dbutils.secrets.get("salesforce", "token")
  },
  "destination": {
    "catalog": "main",
    "schema": "bronze",
    "table": "salesforce_accounts"
  },
  "mode": "incremental",  # Automatic CDC
  "schedule": "0 * * * *"  # Hourly
}
```

#### When to Use Lakeflow Connect vs Custom Code

| Use Lakeflow Connect | Use Custom JDBC/REST |
|---------------------|---------------------|
| Enterprise SaaS systems (Salesforce, ServiceNow) | Proprietary internal APIs |
| Production workloads requiring reliability | One-time data migrations |
| Systems with frequent schema changes | Simple, static database tables |
| Need CDC without custom logic | Custom transformation during ingestion |
| Want managed monitoring/alerting | Specific query optimization requirements |

**Exam Tip:** For questions about ingesting from **Salesforce, ServiceNow, Oracle**, or other enterprise systems, **Lakeflow Connect** is the recommended answer over custom JDBC/REST code.

**Cross-Reference:** See [Workflows](workflows.md) for scheduling connector jobs, [Unity Catalog](unity-catalog.md) for credential management

### JDBC/ODBC/REST Comparison

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| **JDBC** | Relational databases (PostgreSQL, MySQL, SQL Server, Oracle) | Direct database access, incremental loading with cursor columns, parallel reads | Network latency, database load, requires driver |
| **ODBC** | Legacy databases, proprietary systems | Broader driver support | Less common in Spark, performance overhead |
| **REST API** | SaaS platforms, web services | Universal (HTTP), flexible | Pagination complexity, rate limits, manual schema handling |
| **Lakeflow Connect** | Enterprise SaaS/databases | Managed CDC, schema evolution, no code | Limited to supported systems, may have additional cost |

### Integration Patterns Summary

**Pattern 1: Full Load (Initial Sync)**
```python
# JDBC full table load
df = spark.read.format("jdbc").option("dbtable", "table").load()
df.write.format("delta").mode("overwrite").save("/bronze/table")
```

**Pattern 2: Incremental Load (Ongoing Sync)**
```python
# JDBC with cursor column
df = spark.read.format("jdbc") \
  .option("dbtable", f"(SELECT * FROM table WHERE updated_at > '{last_ts}') AS q") \
  .load()
df.write.format("delta").mode("append").save("/bronze/table")
```

**Pattern 3: API Ingestion (Event Data)**
```python
# REST API with pagination
data = fetch_paginated_api(url, headers)
df = spark.createDataFrame([Row(**r) for r in data])
df.write.format("delta").mode("append").save("/bronze/events")
```

**Pattern 4: Enterprise Connector (Managed)**
```
# Lakeflow Connect (configured via UI)
Source: Salesforce → Destination: Delta Table
Mode: Incremental (CDC), Schedule: Hourly
```

**Exam Tips:**
- **JDBC** = direct database connectivity with cursor-based incremental loading
- **Cursor column** must be monotonically increasing (timestamp, ID, sequence)
- **dbutils.secrets.get()** for secure credential management
- **Lakeflow Connect** preferred for Salesforce, ServiceNow, Oracle
- **REST API** requires manual pagination and schema handling
- **Incremental loading** > full table scans for performance

## Practice Questions

### Week 3 Study Guide Questions

**Q1: COPY INTO Idempotency**

Your data pipeline runs COPY INTO three times to load files from `s3://bucket/data/`. The bucket contains one Parquet file with 10,000 rows. How many total rows are in the target Delta table after three runs?

**Answer:** B) 10,000 rows (1 copy) ✓

**Explanation:**

COPY INTO is **idempotent** and automatically tracks loaded files in the Delta transaction log:

**How it works:**
- **First run:** Loads the file, writes 10,000 rows, records file path in Delta log
- **Second run:** Checks Delta log, sees file already loaded, skips it (0 rows written)
- **Third run:** Checks Delta log, sees file already loaded, skips it (0 rows written)
- **Total:** 10,000 rows (only loaded once)

**File Tracking Mechanism:**
```sql
-- First run
COPY INTO bronze.orders
FROM 's3://bucket/data/'
FILEFORMAT = PARQUET;
-- Result: Loaded 1 file, 10,000 rows

-- Second run (same command)
COPY INTO bronze.orders
FROM 's3://bucket/data/'
FILEFORMAT = PARQUET;
-- Result: Loaded 0 files, 0 rows (file already tracked)

-- Verify total
SELECT COUNT(*) FROM bronze.orders;
-- Result: 10,000 rows
```

**Delta transaction log tracking:**
```sql
-- View loaded file history
DESCRIBE HISTORY bronze.orders;

-- Check which files were processed
SELECT operationParameters.path
FROM (DESCRIBE HISTORY bronze.orders)
WHERE operation = 'COPY INTO';
```

**Why idempotency matters:**
- Safe to retry on failure
- No duplicate data from reruns
- Automatic file tracking (no manual checkpoint needed)
- Works at file level, not row level

**When file IS loaded again:**
- New files added to source path
- Using `COPY_OPTIONS ('force' = 'true')` to reprocess

**Cross-Reference:** See COPY INTO Command section above for idempotent ingestion pattern details

---

**Q2: Force Option to Reprocess Files**

How do you configure COPY INTO to reload already-processed files?

**Answer:** C) COPY_OPTIONS ('force' = 'true') ✓

**Explanation:**

The `force` option bypasses file tracking and reloads all files:

```sql
-- Reload all files (even if already processed)
COPY INTO bronze.orders
FROM 's3://bucket/orders/'
FILEFORMAT = PARQUET
COPY_OPTIONS ('force' = 'true');
```

**When to use force:**
1. **Source data corrected** - Upstream system fixed bad data
2. **Schema changed** - Need to reload with new schema
3. **Initial load failed midway** - Partial data loaded
4. **Testing/development** - Experimenting with transformations

**Risks:**
- **Duplicate data** if no unique constraints or MERGE logic
- **Performance impact** for large datasets
- **Increased cost** from reprocessing

**Safe pattern with force (avoid duplicates):**
```sql
-- Step 1: Reload into staging table with force
CREATE OR REPLACE TABLE staging.orders_reload AS
SELECT * FROM bronze.orders WHERE 1=0;  -- Empty table with same schema

COPY INTO staging.orders_reload
FROM 's3://bucket/orders/'
FILEFORMAT = PARQUET
COPY_OPTIONS ('force' = 'true');

-- Step 2: Deduplicate and merge into production
MERGE INTO bronze.orders t
USING (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY updated_at DESC) AS rn
  FROM staging.orders_reload
) s
ON t.order_id = s.order_id AND s.rn = 1
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;

-- Step 3: Cleanup staging
DROP TABLE staging.orders_reload;
```

**Alternative: Overwrite entire table (simpler but destructive):**
```sql
-- Truncate and reload (loses existing data)
TRUNCATE TABLE bronze.orders;

COPY INTO bronze.orders
FROM 's3://bucket/orders/'
FILEFORMAT = PARQUET;
```

**Best Practice:**
- Use `force` sparingly and with caution
- Document why force is needed
- Consider MERGE for deduplication
- Test on staging table first

**Cross-Reference:** See Force Option section above for detailed safe patterns

---

**Q5: COPY INTO Failure and Retry Behavior**

If COPY INTO fails while processing 100 files after successfully loading 60 files, what happens on retry?

**Answer:** C) Loads only the remaining 40 files (file-level state tracking) ✓

**Explanation:**

COPY INTO tracks file-level state in the Delta transaction log, enabling safe retries:

**Failure scenario:**
```sql
-- Attempting to load 100 files
COPY INTO bronze.events
FROM 's3://bucket/events/'
FILEFORMAT = JSON;

-- Progress:
-- Files 1-60: ✅ Loaded successfully, tracked in Delta log
-- File 61: ❌ Fails (corrupted JSON, permission error, etc.)
-- Files 62-100: ⏸️ Not processed
```

**On retry (same command):**
```sql
COPY INTO bronze.events
FROM 's3://bucket/events/'
FILEFORMAT = JSON;

-- COPY INTO behavior:
-- Files 1-60: ⏭️ Skipped (already in Delta log)
-- File 61: ❌ Fails again (still corrupted)
-- Files 62-100: ⏸️ Not processed (stops at first failure)
```

**To skip failed file and continue:**
```sql
-- Option 1: Fix corrupted file, then retry
-- (Recommended: fix data quality at source)

-- Option 2: Load remaining files by excluding failed file
COPY INTO bronze.events
FROM 's3://bucket/events/'
PATTERN = '*.json'
FILEFORMAT = JSON;
-- Note: Cannot exclude specific files, must fix or remove

-- Option 3: Use VALIDATE to identify bad files first
COPY INTO bronze.events
FROM 's3://bucket/events/'
FILEFORMAT = JSON
VALIDATE ALL;

-- Review validation output to find corrupted files
-- Remove or fix corrupted files
-- Retry COPY INTO
```

**File-level atomicity:**
- Each file is a separate transaction
- Successfully loaded files are committed immediately
- Failed files don't affect successfully loaded files
- Retry loads only new/unprocessed files

**Example with validation:**
```sql
-- Step 1: Validate all files before loading
COPY INTO bronze.events
FROM 's3://bucket/events/'
FILEFORMAT = JSON
VALIDATE ALL;

-- Output shows file-level status:
-- s3://bucket/events/file001.json | 5000 rows | 0 errors | NULL
-- s3://bucket/events/file061.json | 0 rows    | 1 error  | "Invalid JSON at line 45"
-- s3://bucket/events/file100.json | 3000 rows | 0 errors | NULL

-- Step 2: Fix or remove file061.json

-- Step 3: Retry COPY INTO
COPY INTO bronze.events
FROM 's3://bucket/events/'
FILEFORMAT = JSON;
-- Now loads all files successfully
```

**Cross-Reference:** See VALIDATE Mode section above for testing before load

---

**Q6: VALIDATE Mode for Dry Run**

What does VALIDATE mode do in COPY INTO?

**Answer:** B) Performs dry run without writing data, shows validation results ✓

**Explanation:**

VALIDATE mode tests COPY INTO without loading data, reporting file-level parsing results:

**Syntax:**
```sql
-- Validate all files
COPY INTO bronze.orders
FROM 's3://bucket/orders/'
FILEFORMAT = JSON
FORMAT_OPTIONS ('multiLine' = 'false')
VALIDATE ALL;

-- Validate first 100 rows of each file
COPY INTO bronze.orders
FROM 's3://bucket/orders/'
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true', 'delimiter' = ',')
VALIDATE 100 ROWS;
```

**Output format:**
```
file_path                              | num_rows_parsed | num_errors | error_details
---------------------------------------+-----------------+------------+----------------------------------
s3://bucket/orders/2026-09-01.json     | 15000           | 0          | NULL
s3://bucket/orders/2026-09-02.json     | 18000           | 0          | NULL
s3://bucket/orders/2026-09-03.json     | 500             | 3          | Invalid JSON at lines 45, 67, 89
s3://bucket/orders/2026-09-04.json     | 0               | 1          | File not accessible: permission denied
```

**What VALIDATE checks:**
1. **Schema compatibility** - Do file columns match table schema?
2. **Data format correctness** - Valid JSON, CSV, Parquet structure?
3. **File accessibility** - Can read files with current permissions?
4. **Parsing errors** - Malformed data, wrong delimiters, encoding issues?

**Use cases:**
```sql
-- Before production load: test new data source
COPY INTO bronze.new_dataset
FROM 's3://new-source/data/'
FILEFORMAT = PARQUET
VALIDATE ALL;
-- Review results before actual load

-- After schema change: verify compatibility
ALTER TABLE bronze.orders ADD COLUMN discount DECIMAL(10,2);

COPY INTO bronze.orders
FROM 's3://bucket/orders/'
FILEFORMAT = JSON
FORMAT_OPTIONS ('mergeSchema' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true')
VALIDATE ALL;
-- Confirms schema evolution will work

-- Troubleshooting failures: identify bad files
COPY INTO bronze.events
FROM 's3://bucket/events/'
FILEFORMAT = JSON
VALIDATE ALL;
-- Find which files have errors before loading
```

**VALIDATE ALL vs VALIDATE n ROWS:**
```sql
-- VALIDATE ALL: Check every row in every file
-- Pros: Complete validation, finds all errors
-- Cons: Slow for large datasets
VALIDATE ALL;

-- VALIDATE n ROWS: Check first n rows per file
-- Pros: Fast, catches common issues
-- Cons: May miss errors later in files
VALIDATE 1000 ROWS;
```

**Best practice workflow:**
```sql
-- 1. Validate first
COPY INTO bronze.orders
FROM 's3://bucket/orders/'
FILEFORMAT = JSON
VALIDATE ALL;

-- 2. Fix any errors identified

-- 3. Run actual load
COPY INTO bronze.orders
FROM 's3://bucket/orders/'
FILEFORMAT = JSON;
```

**Important: VALIDATE does NOT write data**
- Table remains unchanged
- No Delta log entries created
- Read-only operation
- Safe to run in production

**Cross-Reference:** See VALIDATE Mode section above for complete syntax and examples

---

**Q11: Incremental PostgreSQL Ingestion Without CDC**

You need to incrementally load new rows from a PostgreSQL table without CDC. The table has an `updated_at` timestamp column. What's the best approach?

**Answer:** B) JDBC with cursor column (timestamp-based incremental loading) ✓

**Explanation:**

Use JDBC with a **cursor column** (timestamp or ID) to track which rows have been loaded:

**Pattern: Timestamp-based incremental load**
```python
from pyspark.sql.functions import col, max as spark_max

# Step 1: Get last loaded timestamp from Delta table
last_load_ts = spark.read.format("delta") \
  .load("/mnt/bronze/customers") \
  .agg(spark_max("updated_at")) \
  .collect()[0][0]

# Fallback for first run
if last_load_ts is None:
    last_load_ts = "1970-01-01 00:00:00"

# Step 2: Read only new/updated rows using WHERE clause
df = spark.read \
  .format("jdbc") \
  .option("url", "jdbc:postgresql://db.example.com:5432/mydb") \
  .option("user", dbutils.secrets.get("db-credentials", "db_user")) \
  .option("password", dbutils.secrets.get("db-credentials", "db_pass")) \
  .option("dbtable", f"(SELECT * FROM customers WHERE updated_at > '{last_load_ts}') AS incremental") \
  .option("driver", "org.postgresql.Driver") \
  .load()

# Step 3: Append new rows to Delta table
df.write \
  .format("delta") \
  .mode("append") \
  .save("/mnt/bronze/customers")
```

**Why this works without CDC:**
- **Cursor column** (`updated_at`) tracks which rows are new/changed
- **Incremental reads** use `WHERE updated_at > last_timestamp`
- **Efficient** - database uses index on `updated_at`
- **No CDC infrastructure** needed in source database

**Cursor column requirements:**
1. **Indexed** in PostgreSQL for performance:
   ```sql
   CREATE INDEX idx_customers_updated_at ON customers(updated_at);
   ```
2. **Monotonically increasing** (timestamp or sequence)
3. **Never updated** (immutable for reliable tracking)
4. **Not nullable** (NULL values cause missed records)

**Alternative cursor columns:**
```python
# ID-based (for append-only tables)
last_id = spark.read.format("delta").load("/mnt/bronze/transactions") \
  .agg({"transaction_id": "max"}).collect()[0][0] or 0

df = spark.read.format("jdbc") \
  .option("dbtable", f"(SELECT * FROM transactions WHERE transaction_id > {last_id}) AS q") \
  .load()

# Combined timestamp + ID (most reliable)
checkpoint = spark.sql("""
    SELECT MAX(updated_at) AS last_ts, MAX(id) AS last_id
    FROM delta.`/mnt/bronze/orders`
""").first()

df = spark.read.format("jdbc") \
  .option("dbtable", f"""
      (SELECT * FROM orders
       WHERE updated_at >= '{checkpoint['last_ts']}'
       AND id > {checkpoint['last_id']}
       ORDER BY updated_at, id) AS q
  """) \
  .load()
```

**Why other options don't work:**

| Option | Why Not Suitable |
|--------|------------------|
| **COPY INTO** | Only for cloud object storage files, not databases |
| **Structured Streaming** | Requires streaming source (Kafka, Event Hubs), not batch JDBC |
| **Full table reload** | Inefficient, reprocesses all data every run |
| **Auto Loader** | Only for cloud storage files, not databases |

**Production pattern with checkpoint table:**
```python
# Store checkpoint in control table
spark.sql("""
  CREATE TABLE IF NOT EXISTS control.checkpoints (
    pipeline_name STRING,
    checkpoint_timestamp TIMESTAMP,
    checkpoint_id BIGINT,
    rows_processed BIGINT,
    processed_at TIMESTAMP
  ) USING DELTA
""")

# Read checkpoint
checkpoint = spark.sql("""
  SELECT checkpoint_timestamp, checkpoint_id
  FROM control.checkpoints
  WHERE pipeline_name = 'postgres_customers'
  ORDER BY processed_at DESC
  LIMIT 1
""").first()

last_ts = checkpoint['checkpoint_timestamp'] if checkpoint else '1970-01-01'
last_id = checkpoint['checkpoint_id'] if checkpoint else 0

# Load incremental data
df = spark.read.format("jdbc") \
  .option("dbtable", f"""
      (SELECT * FROM customers
       WHERE updated_at > '{last_ts}'
       OR (updated_at = '{last_ts}' AND id > {last_id})
       ORDER BY updated_at, id) AS q
  """) \
  .load()

# Write to Delta
df.write.format("delta").mode("append").save("/mnt/bronze/customers")

# Update checkpoint
if df.count() > 0:
    new_checkpoint = df.agg({"updated_at": "max", "id": "max"}).first()
    spark.sql(f"""
      INSERT INTO control.checkpoints
      VALUES ('postgres_customers',
              '{new_checkpoint[0]}',
              {new_checkpoint[1]},
              {df.count()},
              current_timestamp())
    """)
```

**Cross-Reference:** See JDBC Cursor-Based Pattern section above for detailed incremental loading patterns

---

**Q13: REST API Ingestion for 10K Events**

You need to ingest 10,000 event records from a REST API into a Delta table. What's the recommended approach?

**Answer:** B) Python requests library → DataFrame → Delta Lake ✓

**Explanation:**

Use Python `requests` to fetch API data, convert to Spark DataFrame, and write to Delta:

**Basic REST API ingestion pattern:**
```python
import requests
from pyspark.sql import Row

# Step 1: Fetch data from REST API
url = "https://api.example.com/v1/events"
headers = {
    "Authorization": f"Bearer {dbutils.secrets.get(scope='api-keys', key='events-api-token')}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
response.raise_for_status()  # Raise exception for 4xx/5xx errors

# Step 2: Parse JSON response
data = response.json()["results"]  # Assuming response: {"results": [...]}

# Step 3: Convert to Spark DataFrame
df = spark.createDataFrame([Row(**row) for row in data])

# Step 4: Write to Delta Lake
df.write \
  .format("delta") \
  .mode("append") \
  .save("/mnt/bronze/api_events")
```

**For large datasets with pagination (10K+ records):**
```python
import requests
from pyspark.sql import Row

all_data = []
url = "https://api.example.com/v1/events"
headers = {"Authorization": f"Bearer {dbutils.secrets.get('api', 'token')}"}

# Paginate through all pages
while url:
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    page_data = response.json()
    all_data.extend(page_data["results"])

    # Get next page URL (API-dependent)
    url = page_data.get("next_page_url")  # or ["links"]["next"]

    # Rate limiting (avoid throttling)
    import time
    time.sleep(0.1)  # 100ms delay between requests

# Convert all data to DataFrame
df = spark.createDataFrame([Row(**row) for row in all_data])
df.write.format("delta").mode("append").save("/mnt/bronze/events")

print(f"Loaded {len(all_data)} records")  # e.g., "Loaded 10,000 records"
```

**Production pattern with error handling:**
```python
import requests
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from pyspark.sql import Row

def create_session_with_retries():
    """Create requests session with automatic retries"""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,  # Wait 1, 2, 4 seconds
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    return session

# Use session with retries
session = create_session_with_retries()

try:
    response = session.get(
        "https://api.example.com/v1/events",
        headers={"Authorization": f"Bearer {dbutils.secrets.get('api', 'token')}"},
        params={"limit": 10000},
        timeout=30
    )
    response.raise_for_status()

    data = response.json()["events"]
    df = spark.createDataFrame([Row(**row) for row in data])
    df.write.format("delta").mode("append").save("/mnt/bronze/api_events")

    print(f"Successfully loaded {df.count()} events")

except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
    raise
except requests.exceptions.Timeout:
    print("Request timed out")
    raise
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
    raise
```

**Why this approach:**
1. **Flexible** - Works with any REST API
2. **Simple** - Native Python `requests` library
3. **Databricks-native** - Converts to Spark DataFrame seamlessly
4. **Delta Lake integration** - Direct write to Delta tables

**Why other options don't work:**

| Option | Why Not Suitable |
|--------|------------------|
| **COPY INTO** | Only for cloud storage files, not REST APIs |
| **JDBC** | For databases, not REST APIs |
| **Auto Loader** | For cloud storage files, not APIs |
| **Lakeflow Connect** | May not support your specific API (unless it's Salesforce, ServiceNow, etc.) |

**Best practices:**
```python
# ✅ Store API keys in secrets
api_key = dbutils.secrets.get(scope="api-credentials", key="production-api-key")

# ✅ Handle pagination for large datasets
# ✅ Add rate limiting (time.sleep) to avoid throttling
# ✅ Use retry logic for network failures
# ✅ Validate response status codes
# ✅ Define explicit schema for production (optional but recommended)

from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType

schema = StructType([
    StructField("event_id", IntegerType(), False),
    StructField("event_type", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("user_id", IntegerType(), True)
])

df = spark.createDataFrame([Row(**row) for row in data], schema=schema)
```

**Cross-Reference:** See REST API Ingestion section above for complete patterns and examples

---

**Q14: When to Use force='true'**

When should you use `COPY_OPTIONS ('force' = 'true')` in COPY INTO?

**Answer:** B) After schema changes or data corrections in source files; use with caution to avoid duplicates ✓

**Explanation:**

The `force` option reprocesses already-loaded files and should be used sparingly:

**Valid use cases:**

**1. Source data corrected:**
```sql
-- Scenario: Upstream system fixed incorrect revenue values in historical files
-- Need to reload corrected data

COPY INTO bronze.sales
FROM 's3://bucket/sales/'
FILEFORMAT = PARQUET
COPY_OPTIONS ('force' = 'true');

-- ⚠️ Risk: Duplicates if no deduplication logic
```

**2. Schema changed in source files:**
```sql
-- Scenario: Source files now include new column (e.g., 'discount')
-- Need to reload files with new schema

ALTER TABLE bronze.orders ADD COLUMN discount DECIMAL(10,2);

COPY INTO bronze.orders
FROM 's3://bucket/orders/'
FILEFORMAT = JSON
FORMAT_OPTIONS ('mergeSchema' = 'true')
COPY_OPTIONS ('force' = 'true', 'mergeSchema' = 'true');

-- Reloads all files with new schema
```

**3. Initial load failed midway:**
```sql
-- Scenario: First COPY INTO loaded 60 of 100 files, then failed
-- Delta table has partial data, but source files are complete
-- Need to reload all files to ensure consistency

TRUNCATE TABLE bronze.events;  -- Clear partial data

COPY INTO bronze.events
FROM 's3://bucket/events/'
FILEFORMAT = PARQUET
COPY_OPTIONS ('force' = 'true');

-- Reloads all 100 files from scratch
```

**Safe pattern to avoid duplicates:**
```sql
-- Step 1: Reload into staging table
CREATE OR REPLACE TABLE staging.orders_reload AS
SELECT * FROM bronze.orders WHERE 1=0;  -- Empty table, same schema

COPY INTO staging.orders_reload
FROM 's3://bucket/orders/'
FILEFORMAT = PARQUET
COPY_OPTIONS ('force' = 'true');

-- Step 2: Deduplicate and merge
MERGE INTO bronze.orders t
USING (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY updated_at DESC) AS rn
  FROM staging.orders_reload
) s
ON t.order_id = s.order_id AND s.rn = 1
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;

-- Step 3: Cleanup
DROP TABLE staging.orders_reload;
```

**When NOT to use force:**

| Scenario | Why Not Use force |
|----------|-------------------|
| **Regular incremental loads** | Use idempotent loading (default behavior) |
| **New files arrived** | Default COPY INTO loads only new files automatically |
| **Scheduled ETL** | Idempotency prevents duplicates on retries |
| **Testing in production** | Use VALIDATE mode instead |

**Risks of force='true':**
1. **Duplicate data** if no unique key constraints or MERGE logic
2. **Performance impact** - Reprocesses all files (expensive for large datasets)
3. **Increased cost** - Reprocessing consumes DBUs
4. **Data quality issues** - Old bad data may be reloaded

**Example: force causing duplicates (bad pattern):**
```sql
-- First run: Load 10,000 rows
COPY INTO bronze.orders
FROM 's3://bucket/orders/'
FILEFORMAT = PARQUET;

SELECT COUNT(*) FROM bronze.orders;
-- Result: 10,000 rows

-- Second run: Reload with force (WRONG - creates duplicates)
COPY INTO bronze.orders
FROM 's3://bucket/orders/'
FILEFORMAT = PARQUET
COPY_OPTIONS ('force' = 'true');

SELECT COUNT(*) FROM bronze.orders;
-- Result: 20,000 rows (duplicates!)
```

**Best practices:**
1. **Document why force is needed** - Leave code comments explaining the reason
2. **Use staging table** - Reload into temp table, then MERGE
3. **Test first** - Run on dev environment before production
4. **Consider alternatives** - Can you just load new files instead?
5. **Monitor duplicates** - Check row counts before/after

**Alternative: Reload without force (preferred when possible):**
```sql
-- Instead of force, delete and reload specific partition
DELETE FROM bronze.sales WHERE date = '2026-09-01';

COPY INTO bronze.sales
FROM 's3://bucket/sales/date=2026-09-01/'
FILEFORMAT = PARQUET;

-- Only reloads one partition, no force needed
```

**Cross-Reference:** See Force Option section above for safe patterns and complete examples

## Common Pitfalls

1. **COPY INTO with duplicates** - Fails or skips
2. **INSERT OVERWRITE without partition** - Entire table lost
3. **MERGE without conditions** - All rows updated
4. **No checkpoint tracking** - Reprocessing data
5. **Batch when streaming needed** - High latency

## Exam Tips

- COPY INTO = incremental file loading (Q12)
- INSERT OVERWRITE = destructive, not atomic (Q10)
- MERGE = upsert, prevents duplicates
- Batch for Silver/Gold layers (medallion pattern)
- Incremental > full reprocessing

## Cross-References

- [Delta Lake](delta-lake.md) - MERGE, OPTIMIZE
- [Streaming](streaming.md) - When to use streaming
- [Medallion Architecture](medallion-architecture.md) - Layer recommendations
- [CDC & SCD](cdc-scd.md) - Change tracking

## Sources

- [Databricks_Data_Engineering_Concepts.md](../Databricks_Data_Engineering_Concepts.md)
- https://docs.databricks.com/sql/language-manual/delta-copy-into.html
- Practice exam Q10, Q12
