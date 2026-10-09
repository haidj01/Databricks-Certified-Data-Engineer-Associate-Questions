# Delta Lake

**Category:** Core Technologies
**Last Updated:** 2026-09-09

## Overview

Delta Lake is an open-source storage framework that brings ACID transaction guarantees to data lakes. It acts as the single source of truth for data platforms.

## Key Concepts

### ACID Compliance

Delta Lake provides full ACID transaction guarantees:

- **Atomicity:** Operations complete fully or not at all
  - If a write fails mid-operation, no partial data is committed
  - All-or-nothing guarantee for multi-file operations
  - Transaction rollback on failure

- **Consistency:** Data remains in valid state
  - Schema enforcement prevents invalid data
  - Constraints validated before commit
  - Referential integrity maintained

- **Isolation:** Concurrent operations don't interfere
  - Optimistic concurrency control
  - Readers see consistent snapshots
  - Writers don't block readers
  - Serializable isolation level (default)

- **Durability:** Committed changes are permanent
  - Transaction log ensures durability
  - Writes persisted to cloud storage
  - Fault-tolerant recovery

**How ACID Works:**
1. All changes written to temporary files
2. Transaction log entry created atomically
3. Readers see only committed versions
4. Failed writes leave no partial data

**Exam Tip:** Delta Lake IS ACID compliant (README Q8). This is a key differentiator from Parquet/CSV.

### Table Structure

Delta tables contain:
- **Multiple data files** (not single file)
  - Parquet format data files
  - Stored in cloud object storage
  - Distributed across partitions

- **Transaction log** (_delta_log directory)
  - JSON files tracking all changes
  - Numbered sequentially: 00000000000000000000.json, 00000000000000000001.json, ...
  - Every 10 commits: Parquet checkpoint created for faster reads
  - Immutable, append-only log

- **Metadata** (schema, partitioning, statistics)
  - Schema definition and evolution history
  - Partition specifications
  - Min/max statistics for data skipping
  - File-level metrics

- **Version history** (for time travel)
  - Each transaction creates new version
  - Versions retained based on VACUUM retention
  - Enables rollback and auditing

**Transaction Log Example:**
```
/delta-table/
├── part-00000.parquet
├── part-00001.parquet
└── _delta_log/
    ├── 00000000000000000000.json  # Version 0
    ├── 00000000000000000001.json  # Version 1
    ├── 00000000000000000010.json  # Version 10
    └── 00000000000000000010.checkpoint.parquet  # Checkpoint
```

**Exam Tip:** Delta tables are NOT single files - they consist of multiple Parquet files + transaction log (README Q3)

**Cross-Reference:** See [Tables and Views](tables-views.md) for managed vs. external tables

## File Formats for Data Lakes

### Overview

Data lakes support multiple file formats, each with different characteristics optimized for specific use cases. Understanding format trade-offs is critical for exam and real-world implementations.

**Key Considerations:**
- **Compression:** Storage efficiency vs. CPU overhead
- **Schema evolution:** Ability to add/modify columns
- **Query performance:** Columnar (analytics) vs. row-based (transactional)
- **Splittability:** Can Spark parallelize reads across partitions?
- **Human readability:** Debugging and manual inspection

### File Format Comparison

| Format | Type | Compression | Schema Evolution | Splittable | Query Performance | Use Cases |
|--------|------|-------------|------------------|------------|-------------------|-----------|
| **Parquet** ✓ | Columnar | Excellent (Snappy, Gzip) | Yes (add columns) | Yes | **Excellent** for analytics | **Recommended for Delta Lake**, data warehousing, BI queries |
| **Avro** | Row-based | Good (Snappy, Deflate) | Yes (full evolution) | Yes | Good for row-level reads | Streaming, schema-heavy workloads, CDC |
| **ORC** | Columnar | Excellent (Zlib, Snappy) | Yes (limited) | Yes | Excellent for analytics | Hive compatibility, legacy Hadoop workloads |
| **JSON** | Text | Poor (Gzip only) | Flexible (schema-on-read) | Yes (if newline-delimited) | **Poor** | Semi-structured data, APIs, exploration |
| **CSV** | Text | Poor (Gzip only) | No | Yes | **Very poor** | Simple exports, human-readable, legacy integrations |

### Format Details

#### Parquet (Recommended for Delta Lake)

**Why Parquet:**
- **Columnar storage:** Optimized for analytics queries (SELECT specific columns)
- **Predicate pushdown:** Skip entire row groups based on min/max statistics
- **Excellent compression:** 10x smaller than CSV (Snappy compression)
- **Schema evolution:** Add new columns without rewriting data
- **Nested data support:** Arrays, structs, maps
- **Delta Lake native format:** All Delta tables use Parquet internally

**Code Examples:**
```python
# Read Parquet
df = spark.read.format("parquet").load("/mnt/data/sales.parquet")

# Write Parquet with compression
df.write \
  .format("parquet") \
  .option("compression", "snappy") \
  .mode("overwrite") \
  .save("/mnt/output/sales.parquet")

# Write with partitioning
df.write \
  .format("parquet") \
  .partitionBy("year", "month") \
  .save("/mnt/output/sales_partitioned.parquet")
```

**Compression Codecs:**
- **Snappy** (default): Fast compression/decompression, moderate ratio
- **Gzip**: Higher compression ratio, slower
- **LZ4**: Very fast, moderate ratio
- **Zstandard (zstd)**: Best balance of speed and compression

**Performance:**
```sql
-- Query scans only "amount" column (not all columns)
SELECT SUM(amount) FROM parquet_table WHERE date = '2026-09-01';
-- Parquet: ~2 seconds for 1TB table
-- CSV: ~45 seconds for same data (must read entire file)
```

#### Avro (Best for Streaming)

**Why Avro:**
- **Row-based storage:** Efficient for writing records one-at-a-time
- **Full schema evolution:** Add, remove, rename fields with compatibility rules
- **Self-describing:** Schema embedded in file header
- **Compact binary format:** Smaller than JSON, larger than Parquet
- **Excellent for streaming:** Kafka, event sourcing, CDC pipelines

**Code Examples:**
```python
# Read Avro
df = spark.read.format("avro").load("/mnt/data/events.avro")

# Write Avro
df.write \
  .format("avro") \
  .mode("overwrite") \
  .save("/mnt/output/events.avro")

# Schema evolution: add new column
# Old schema: {id, name}
# New schema: {id, name, email}
# Avro handles this automatically with default values
```

**Schema Evolution Example:**
```python
# Forward compatibility: new reader, old data
# Backward compatibility: old reader, new data
# Full compatibility: both directions

# Avro supports all three with schema registry
```

**Use Cases:**
- Kafka message serialization
- CDC streams from databases
- Event sourcing architectures
- Schema-heavy data pipelines

#### ORC (Optimized Row Columnar)

**Why ORC:**
- **Hive native format:** Best for Hive compatibility
- **Columnar storage:** Similar to Parquet for analytics
- **Built-in indexes:** Bloom filters, min/max statistics
- **ACID support:** Native transactional support in Hive

**Code Examples:**
```python
# Read ORC
df = spark.read.format("orc").load("/mnt/data/legacy.orc")

# Write ORC
df.write \
  .format("orc") \
  .option("compression", "zlib") \
  .save("/mnt/output/data.orc")
```

**Parquet vs ORC:**
- **Parquet:** Better Spark integration, wider ecosystem support
- **ORC:** Better Hive integration, slightly better compression
- **Recommendation:** Use Parquet for new projects unless Hive legacy required

#### JSON (Semi-Structured Data)

**Why JSON:**
- **Schema-on-read:** No upfront schema definition
- **Nested structures:** Arrays, objects naturally represented
- **Human-readable:** Easy debugging and manual inspection
- **API integration:** Direct REST API responses

**Code Examples:**
```python
# Read JSON
df = spark.read.format("json").load("/mnt/data/api_responses.json")

# Write JSON (newline-delimited for Spark)
df.write \
  .format("json") \
  .mode("overwrite") \
  .save("/mnt/output/data.json")

# Infer schema from JSON
df = spark.read \
  .option("inferSchema", "true") \
  .json("/mnt/data/events.json")

# Provide schema explicitly (faster)
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
  StructField("id", IntegerType(), True),
  StructField("name", StringType(), True),
  StructField("metadata", StringType(), True)  # Nested JSON as string
])

df = spark.read.schema(schema).json("/mnt/data/events.json")
```

**Performance Issues:**
- **No columnar pruning:** Must read entire file
- **Poor compression:** Text format is verbose
- **Schema inference overhead:** Scans entire dataset
- **No predicate pushdown:** Cannot skip data efficiently

**When to Use:**
- API responses and logs
- Exploratory data analysis
- Semi-structured IoT data
- **Avoid for production analytics workloads**

#### CSV (Legacy Compatibility)

**Why CSV:**
- **Universal compatibility:** Readable by any tool
- **Human-readable:** Open in Excel, text editors
- **Simple structure:** Easy for non-technical users

**Code Examples:**
```python
# Read CSV with header
df = spark.read \
  .format("csv") \
  .option("header", "true") \
  .option("inferSchema", "true") \
  .load("/mnt/data/sales.csv")

# Write CSV
df.write \
  .format("csv") \
  .option("header", "true") \
  .mode("overwrite") \
  .save("/mnt/output/export.csv")

# CSV with custom delimiter
df = spark.read \
  .format("csv") \
  .option("header", "true") \
  .option("delimiter", "|") \
  .option("quote", "\"") \
  .option("escape", "\\") \
  .load("/mnt/data/pipe_delimited.csv")

# Provide schema explicitly (recommended)
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

schema = StructType([
  StructField("product_id", StringType(), True),
  StructField("sales_amount", DoubleType(), True),
  StructField("region", StringType(), True)
])

df = spark.read \
  .format("csv") \
  .option("header", "true") \
  .schema(schema) \
  .load("/mnt/data/sales.csv")
```

**Common CSV Issues:**
- **Quote/escape handling:** Embedded commas, newlines break parsing
- **Schema inference errors:** All columns read as strings
- **No data types:** "123" vs 123 ambiguity
- **No compression:** Large file sizes
- **Poor performance:** 10-50x slower than Parquet

**CSV Options:**
```python
{
  "header": "true",           # First row is column names
  "inferSchema": "true",      # Auto-detect data types (slow)
  "delimiter": ",",           # Field separator
  "quote": "\"",              # Quote character
  "escape": "\\",             # Escape character
  "nullValue": "NULL",        # How nulls are represented
  "dateFormat": "yyyy-MM-dd", # Date parsing format
  "timestampFormat": "yyyy-MM-dd HH:mm:ss",
  "multiLine": "true"         # Allow quoted newlines
}
```

**When to Use:**
- Data export for Excel/BI tools
- Simple data exchanges with external systems
- Human-readable debugging output
- **Avoid for production data pipelines**

### Format Selection Best Practices

#### For Production Data Lakes (Recommended)

**Use Parquet (wrapped in Delta Lake):**
```python
# Create Delta table (Parquet under the hood)
df.write \
  .format("delta") \
  .mode("overwrite") \
  .option("overwriteSchema", "true") \
  .partitionBy("date") \
  .save("/mnt/gold/sales")

# Delta provides: ACID, time travel, schema evolution, upserts
# Built on Parquet: columnar performance, compression, predicate pushdown
```

**Why Delta + Parquet:**
- Best query performance (columnar)
- ACID transactions (Delta)
- Schema evolution (both)
- Time travel (Delta)
- MERGE/UPDATE/DELETE (Delta)
- Excellent compression (Parquet)

#### For Streaming Pipelines

**Use Avro (with schema registry):**
```python
# Write streaming data as Avro
stream_df.writeStream \
  .format("avro") \
  .option("checkpointLocation", "/mnt/checkpoints/kafka") \
  .start("/mnt/bronze/events")

# Then batch convert to Delta for analytics
spark.read.format("avro").load("/mnt/bronze/events") \
  .write.format("delta").mode("append").save("/mnt/silver/events")
```

**Avro Advantages:**
- Schema evolution for event streams
- Compact binary serialization
- Kafka compatibility
- Fast writes

#### For API/Log Ingestion

**Use JSON initially, convert to Delta:**
```python
# Ingest JSON from API
api_df = spark.read.json("/mnt/landing/api_responses/")

# Convert to Delta with schema
api_df.write \
  .format("delta") \
  .mode("overwrite") \
  .save("/mnt/bronze/api_data")

# Query as Delta (Parquet performance)
spark.read.format("delta").load("/mnt/bronze/api_data")
```

#### For External Integrations

**Use CSV for exports only:**
```python
# Export Delta table to CSV for BI tool
spark.read.format("delta").load("/mnt/gold/sales") \
  .write \
  .format("csv") \
  .option("header", "true") \
  .mode("overwrite") \
  .save("/mnt/exports/sales_for_excel.csv")
```

**Never store production data as CSV** - only for final exports.

### COPY INTO Format Support

**Format-Specific Options:**

```sql
-- COPY INTO with Parquet
COPY INTO bronze.sales
FROM '/mnt/landing/sales/'
FILEFORMAT = PARQUET
FORMAT_OPTIONS ('mergeSchema' = 'true');

-- COPY INTO with JSON
COPY INTO bronze.logs
FROM '/mnt/landing/logs/'
FILEFORMAT = JSON
FORMAT_OPTIONS ('inferSchema' = 'true');

-- COPY INTO with CSV
COPY INTO bronze.customers
FROM '/mnt/landing/customers/'
FILEFORMAT = CSV
FORMAT_OPTIONS (
  'header' = 'true',
  'delimiter' = ',',
  'quote' = '"',
  'inferSchema' = 'false'
);

-- COPY INTO with Avro
COPY INTO bronze.events
FROM '/mnt/landing/events/'
FILEFORMAT = AVRO;
```

**Cross-Reference:** See [Batch Processing](batch-processing.md) for comprehensive COPY INTO patterns

### Exam Tips

**Format Questions:**
- **"Best format for analytics workloads?"** → Parquet (columnar, compression)
- **"Best format for streaming with schema evolution?"** → Avro
- **"Best format for human readability?"** → JSON or CSV
- **"What format does Delta Lake use internally?"** → Parquet
- **"Best compression for Parquet?"** → Snappy (default, good balance)
- **"Can CSV be splittable?"** → Yes (if uncompressed or with splittable compression)

**Performance Comparisons:**
- Parquet: 10-50x faster than CSV for analytics
- Columnar (Parquet, ORC): Best for SELECT specific columns
- Row-based (Avro, CSV, JSON): Better for row-level reads/writes

**Schema Evolution:**
- Parquet: Can add columns (additive)
- Avro: Full schema evolution (add, remove, rename with compatibility)
- JSON: Flexible schema-on-read
- CSV: No schema evolution

### Cross-References

- [Batch Processing](batch-processing.md) - COPY INTO format options
- [Streaming](streaming.md) - Auto Loader format inference
- [Cost Optimization](cost-optimization.md) - Storage costs by format

### Time Travel & Versioning

Query and restore historical table versions.

```sql
-- Query historical version by number
SELECT * FROM table_name VERSION AS OF 10;

-- Query by timestamp
SELECT * FROM table_name TIMESTAMP AS OF '2026-09-01 10:30:00';

-- Using @ syntax
SELECT * FROM table_name@v10;

-- Restore to previous version
RESTORE TABLE table_name TO VERSION AS OF 10;

-- View version history
DESCRIBE HISTORY table_name;
```

**Use Cases:**
- Audit and compliance queries
- Rollback bad writes
- Compare data across time
- Reproduce ML training datasets
- Debug data quality issues

**Limitations:**
- Versions only available within VACUUM retention
- Performance degrades with many versions
- Metadata overhead for large histories

### VACUUM Command

Removes old data files no longer referenced by the transaction log.

```sql
-- Default 7-day retention
VACUUM table_name;

-- Custom retention (168 hours = 7 days)
VACUUM table_name RETAIN 168 HOURS;

-- Aggressive cleanup (24 hours minimum)
VACUUM table_name RETAIN 24 HOURS;

-- Dry run to see what would be deleted
VACUUM table_name DRY RUN;
```

**⚠️ Critical Warning:** Data becomes unavailable after VACUUM if:
- Files are deleted beyond retention period
- Time travel queries reference deleted versions
- Running concurrent jobs reading old versions
- Default retention: 7 days (168 hours)

**Safety Considerations:**
- Never VACUUM below 7 days for production tables
- Ensure no long-running queries accessing historical data
- VACUUM can break running streaming jobs if they reference old files
- Consider increasing retention for audit/compliance tables

**Best Practices:**
```sql
-- Safe for most workloads
VACUUM table_name RETAIN 168 HOURS;  -- 7 days

-- For audit tables
VACUUM audit_logs RETAIN 720 HOURS;  -- 30 days

-- Check table size before VACUUM
DESCRIBE DETAIL table_name;
```

**Exam Tip:** README Q1 - Data unavailability after VACUUM is a common exam trap!

### MERGE Operations

Prevents duplicates when upserting data (INSERT + UPDATE in single transaction).

```sql
-- Basic MERGE (upsert)
MERGE INTO target t
USING source s
ON t.id = s.id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;

-- MERGE with DELETE
MERGE INTO target t
USING source s
ON t.id = s.id
WHEN MATCHED AND s.is_deleted = true THEN DELETE
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;

-- Conditional MERGE
MERGE INTO target t
USING source s
ON t.id = s.id
WHEN MATCHED AND s.last_updated > t.last_updated THEN
  UPDATE SET t.value = s.value, t.last_updated = s.last_updated
WHEN NOT MATCHED THEN
  INSERT (id, value, last_updated) VALUES (s.id, s.value, s.last_updated);
```

**Use Cases:**
- Prevent duplicate records during ingestion
- Implement SCD Type 1 (overwrite)
- Handle CDC (Change Data Capture) streams
- Synchronize data from source systems

**Performance Tips:**
- Add WHERE clause to USING to reduce data scanned
- Partition target table on merge key when possible
- Use Z-ORDER on merge key columns

**Example: Preventing Duplicates (README Q9)**
```sql
-- Instead of INSERT (creates duplicates)
INSERT INTO users SELECT * FROM new_users;

-- Use MERGE (upserts safely)
MERGE INTO users t
USING new_users s ON t.user_id = s.user_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

**Exam Tip:** README Q9 - MERGE is the recommended way to avoid duplicates in Delta tables

**Cross-Reference:** See [CDC & SCD](cdc-scd.md) for detailed merge patterns

### Schema Evolution

Delta Lake supports automatic and manual schema evolution.

```sql
-- Enable automatic schema evolution
SET spark.databricks.delta.schema.autoMerge.enabled = true;

-- Insert with new columns (auto-adds columns)
INSERT INTO table_name SELECT col1, col2, new_col3 FROM source;

-- Add column explicitly
ALTER TABLE table_name ADD COLUMN new_column STRING;

-- Change column type (limited - must be compatible)
ALTER TABLE table_name ALTER COLUMN age TYPE BIGINT;

-- Change column comment
ALTER TABLE table_name ALTER COLUMN status COMMENT 'Order status code';

-- Rename column
ALTER TABLE table_name RENAME COLUMN old_name TO new_name;

-- Drop column
ALTER TABLE table_name DROP COLUMN deprecated_column;
```

**Schema Evolution Modes:**

| Mode | Behavior | Use Case |
|------|----------|----------|
| **No evolution** | Reject schema changes | Strict schema enforcement |
| **Auto-merge** | Add new columns automatically | Evolving data sources |
| **Overwrite schema** | Replace entire schema | Schema corrections |

**Important Rules:**
- Cannot change column type to incompatible type (e.g., STRING → INT)
- Can widen types (INT → BIGINT, FLOAT → DOUBLE)
- New columns added with NULL values for existing rows
- Dropping columns doesn't delete data (VACUUM needed)

**Example:**
```sql
-- Initial schema
CREATE TABLE events (id INT, name STRING);

-- Enable auto-merge
SET spark.databricks.delta.schema.autoMerge.enabled = true;

-- Insert with new column (automatically adds 'timestamp')
INSERT INTO events SELECT 1 AS id, 'login' AS name, current_timestamp() AS timestamp;

-- Result: Table now has (id, name, timestamp) with NULL timestamp for old rows
```

**Exam Tip:** Schema evolution is automatic when autoMerge is enabled, but type compatibility rules still apply

### Optimization

#### OPTIMIZE Command

Compacts small files into larger ones for better read performance.

```sql
-- Basic compaction
OPTIMIZE table_name;

-- Optimize specific partition
OPTIMIZE table_name WHERE date >= '2026-09-01';

-- Combine with Z-ORDER
OPTIMIZE table_name ZORDER BY (column1, column2);

-- Check table details before/after
DESCRIBE DETAIL table_name;
```

**Benefits:**
- Reduces number of small files
- Improves read performance
- Reduces metadata overhead
- Better parallelism during queries

**When to Run:**
- After many small writes
- Streaming ingestion (daily/weekly)
- Before critical analytics queries
- When `DESCRIBE DETAIL` shows many small files

**Performance Impact:**
- Reads: 2-10x faster
- Small file threshold: < 128 MB
- Target file size: 1 GB (configurable)

#### Z-Ordering

Colocates related information in the same set of files for faster queries.

```sql
-- Z-ORDER by single column
OPTIMIZE table_name ZORDER BY (customer_id);

-- Z-ORDER by multiple columns (up to 4 recommended)
OPTIMIZE table_name ZORDER BY (region, product_category);
```

**How it Works:**
- Multi-dimensional clustering
- Co-locates related values in same files
- Enables data skipping (min/max statistics)
- Reduces files scanned during queries

**Best Practices:**
- Use on high-cardinality columns (customer_id, user_id)
- Limit to 3-4 columns maximum
- Choose columns used in WHERE clauses
- Don't Z-ORDER on partition columns (already clustered)

**Example:**
```sql
-- Query before Z-ORDER: scans 100 files
SELECT * FROM orders WHERE customer_id = 'C12345';

-- Run Z-ORDER
OPTIMIZE orders ZORDER BY (customer_id);

-- Query after Z-ORDER: scans 5 files (20x improvement)
SELECT * FROM orders WHERE customer_id = 'C12345';
```

**Purpose:** Query performance optimization through data skipping (README Q11)

#### Liquid Clustering (Recommended for New Tables)

Next-generation clustering that replaces Z-ORDER and partitioning.

```sql
-- Create table with liquid clustering
CREATE TABLE events (
  timestamp TIMESTAMP,
  user_id STRING,
  event_type STRING
)
CLUSTER BY (user_id, event_type);

-- OPTIMIZE automatically re-clusters
OPTIMIZE events;
```

**Advantages over Z-ORDER:**
- Incremental clustering (faster)
- Automatic clustering key selection
- No manual OPTIMIZE needed
- Better for high write volumes
- Supports more columns efficiently

**When to Use:**
| Technique | Best For |
|-----------|----------|
| **Partitioning** | Low cardinality (date, region), few partitions |
| **Z-ORDER** | Medium cardinality, ad hoc queries, existing tables |
| **Liquid Clustering** | High cardinality, high write volume, new tables |

**Migration:**
```sql
-- Convert from partitioned + Z-ORDER to liquid clustering
ALTER TABLE old_table
CLUSTER BY (user_id, timestamp);
```

**Cross-Reference:** See [Cost Optimization](cost-optimization.md) for cluster tuning

### INSERT OVERWRITE

Replaces all data in a table or partition.

```sql
-- Overwrite entire table
INSERT OVERWRITE TABLE table_name
SELECT * FROM source_table;

-- Overwrite specific partition
INSERT OVERWRITE TABLE table_name
PARTITION (date='2026-09-01')
SELECT * FROM source_table WHERE date='2026-09-01';
```

**Considerations (README Q10):**
- Deletes existing data before writing
- Not atomic at partition level (old files deleted, then new files written)
- Can't recover overwritten data after VACUUM
- Consider using MERGE instead for upserts
- Use with caution in production

**Safer Alternative:**
```sql
-- Instead of INSERT OVERWRITE
-- Use DELETE + INSERT (within transaction)
DELETE FROM table_name WHERE condition;
INSERT INTO table_name SELECT * FROM source_table;

-- Or use MERGE for upserts
MERGE INTO table_name ...
```

### Change Data Feed (CDF)

Track row-level changes (inserts, updates, deletes) for incremental processing.

```sql
-- Enable CDF on table creation
CREATE TABLE users (id INT, name STRING, email STRING)
TBLPROPERTIES (delta.enableChangeDataFeed = true);

-- Enable CDF on existing table
ALTER TABLE users
SET TBLPROPERTIES (delta.enableChangeDataFeed = true);

-- Read changes since version
SELECT * FROM table_changes('users', 10);

-- Read changes between timestamps
SELECT * FROM table_changes('users', '2026-09-01', '2026-09-02');

-- CDF columns
SELECT _change_type, _commit_version, _commit_timestamp, *
FROM table_changes('users', 0);
```

**Change Types:**
- `insert`: New row added
- `update_preimage`: Row before update
- `update_postimage`: Row after update
- `delete`: Row deleted

**Use Cases:**
- Incremental ETL pipelines
- CDC replication to downstream systems
- Audit trail of changes
- Incremental ML feature engineering

**Example: Incremental Pipeline**
```python
# Read only changes since last checkpoint
changes_df = spark.read.format("delta") \
  .option("readChangeData", "true") \
  .option("startingVersion", last_processed_version) \
  .table("users")

# Process only changed rows
changes_df.filter(col("_change_type").isin("insert", "update_postimage")) \
  .write.mode("append").table("users_silver")
```

**Cross-Reference:** See [CDC & SCD](cdc-scd.md) for detailed change tracking patterns

### CLONE Operations

Create copies of Delta tables efficiently.

```sql
-- SHALLOW CLONE (metadata only, shares data files)
CREATE TABLE users_dev
SHALLOW CLONE users;

-- DEEP CLONE (full copy of data files)
CREATE TABLE users_backup
DEEP CLONE users;

-- Clone specific version
CREATE TABLE users_snapshot
DEEP CLONE users VERSION AS OF 100;
```

**Comparison:**

| Feature | SHALLOW CLONE | DEEP CLONE |
|---------|--------------|------------|
| **Speed** | Instant (metadata only) | Slow (copies all data) |
| **Storage** | Minimal (shares files) | Full (duplicate files) |
| **Independence** | Affected by source VACUUM | Fully independent |
| **Use Case** | Dev/test environments | Backups, isolation |

**Use Cases:**

**SHALLOW CLONE:**
- Quick dev/test environment creation
- Experimentation without data duplication
- Cost-effective for temporary tables
- **Warning:** Source VACUUM will affect clone

**DEEP CLONE:**
- Production backups before risky operations
- Data archival for compliance
- Isolated environments (complete independence)
- Cross-region replication

**Example Workflow:**
```sql
-- Create dev environment (instant)
CREATE TABLE customers_dev SHALLOW CLONE customers;

-- Test changes
INSERT INTO customers_dev VALUES (999, 'Test User');

-- Create backup before production change
CREATE TABLE customers_backup_20260901
DEEP CLONE customers;

-- Restore if needed
CREATE OR REPLACE TABLE customers
SHALLOW CLONE customers_backup_20260901;
```

## Common Pitfalls

1. **VACUUM too aggressively** - Loses time travel capability
2. **Forgetting MERGE conditions** - Creates duplicates
3. **Z-ordering wrong columns** - No performance benefit
4. **INSERT OVERWRITE without backup** - Data loss risk

## Advantages Over Traditional Data Lakes

**Sample Exam Question (From Official Exam Guide):**

**Scenario:** Need rapid iteration, reliable rollbacks, audit trails, and consistent access for both AI and BI workloads.

**Question:** What platform capabilities should you choose?

**Answer:** Delta Lake ACID transactions + time travel, governed by Unity Catalog ✓

**Why Delta Lake + Unity Catalog:**

1. **Rapid Iteration:**
   - ACID guarantees enable safe concurrent writes
   - No data corruption from parallel operations
   - Immediate consistency for reads

2. **Reliable Rollbacks:**
   - Time travel to any previous version
   - `RESTORE TABLE` command for quick recovery
   - Version history retained per retention policy

3. **Audit Trails:**
   - Transaction log tracks all changes
   - Unity Catalog lineage shows data flow
   - Who accessed/modified what and when

4. **Consistent Access (AI + BI):**
   - Single source of truth for all workloads
   - Same data for ML training and dashboards
   - No ETL duplication needed

**Example:**
```sql
-- Rollback to previous version
RESTORE TABLE customer_data TO VERSION AS OF 42;

-- Audit history
DESCRIBE HISTORY customer_data;

-- Unity Catalog lineage
SELECT * FROM system.access.table_lineage
WHERE table_name = 'customer_data';
```

**Key Advantages (README Q4):**
- ACID transactions
- Schema enforcement and evolution
- Time travel and versioning
- Better performance with optimizations
- Unified batch and streaming

**Cross-Reference:** See [Unity Catalog](unity-catalog.md) for governance, [Streaming](streaming.md) for incremental processing, [exam-prep.md](exam-prep.md) for full sample question details

## Practice Questions

### Week 1 Study Guide Questions

**Q1: Schema Enforcement**

A team wants to ensure data quality by preventing incompatible data types from being written to their Delta table. Which Delta Lake feature should they rely on?

**Answer:** Schema Enforcement ✓

**Explanation:**
Delta Lake automatically enforces schema on write operations:
- Rejects writes with incompatible data types
- Validates column names and types match table schema
- Prevents data corruption from type mismatches
- Throws error if incoming data doesn't match existing schema

**Example:**
```python
# Table schema: id INT, name STRING, age INT
# This write will fail (age as STRING instead of INT)
invalid_df = spark.createDataFrame([(1, "John", "thirty")], ["id", "name", "age"])
invalid_df.write.mode("append").saveAsTable("users")  # Error: Schema mismatch
```

**Q2: Time Travel for Regulatory Audit**

Your organization needs to query data as it existed on a specific date for a regulatory audit. Which Delta Lake capability should you use?

**Answer:** Time Travel with TIMESTAMP AS OF ✓

**Explanation:**
Delta Lake's time travel feature allows querying historical table versions:
- Query data at specific timestamp or version number
- Audit trail for compliance requirements
- No need to maintain separate historical copies
- Data retained based on VACUUM retention period

**Example:**
```sql
-- Query data as it existed on audit date
SELECT * FROM customer_transactions
TIMESTAMP AS OF '2026-01-15 00:00:00';

-- Or by version number
SELECT * FROM customer_transactions VERSION AS OF 42;
```

**Q3: VACUUM RETAIN 0 HOURS Impact**

What happens if you run `VACUUM table_name RETAIN 0 HOURS` and then try to query `VERSION AS OF 10`?

**Answer:** Query will fail with error - historical data files have been deleted ✓

**Explanation:**
VACUUM with 0 hours retention immediately deletes old data files:
- All historical versions become unavailable
- Time travel queries fail if referencing deleted versions
- Cannot restore to previous versions
- Transaction log remains, but data files are gone
- **Minimum safe retention: 7 days (168 hours)**

**Warning:** Never use RETAIN 0 HOURS in production!

**Example:**
```sql
-- Dangerous operation
VACUUM customer_data RETAIN 0 HOURS;

-- This will now fail
SELECT * FROM customer_data VERSION AS OF 10;
-- Error: The table or view 'customer_data' at version 10 is not available
```

**Q4: Schema Evolution**

You need to add new columns to incoming data without manually altering the table schema. What option should you use?

**Answer:** `.option('mergeSchema', 'true')` ✓

**Explanation:**
Schema evolution allows automatic addition of new columns:
- New columns added automatically on write
- Existing rows get NULL for new columns
- No manual ALTER TABLE needed
- Supports schema widening (not all type changes)

**Alternative:** Set `spark.databricks.delta.schema.autoMerge.enabled = true` globally

**Example:**
```python
# Original schema: id, name
# New data includes: id, name, email (new column)
new_df = spark.createDataFrame([
    (1, "Alice", "alice@example.com"),
    (2, "Bob", "bob@example.com")
], ["id", "name", "email"])

# Without mergeSchema - would fail
# With mergeSchema - adds email column automatically
new_df.write \
    .mode("append") \
    .option("mergeSchema", "true") \
    .saveAsTable("users")
```

**Q5: Liquid Clustering vs Z-ORDER**

What is the main advantage of Liquid Clustering compared to Z-ORDER?

**Answer:** Incremental and flexible clustering ✓

**Explanation:**
Liquid Clustering advantages:
- **Incremental:** Only clusters new/changed data, not entire table
- **Flexible:** Can change clustering columns without rewriting all data
- **Automatic:** OPTIMIZE automatically applies clustering
- **Performance:** Faster clustering operations for large tables
- **Scalable:** Better for high-write-volume tables

**Comparison:**
```sql
-- Z-ORDER (legacy approach)
OPTIMIZE table_name ZORDER BY (col1, col2);
-- Rewrites all files each time

-- Liquid Clustering (modern approach)
CREATE TABLE events (
  timestamp TIMESTAMP,
  user_id STRING
) CLUSTER BY (user_id);  -- Defined once

OPTIMIZE events;  -- Incrementally clusters only new data
```

**Q8: Lakehouse vs Data Lake**

What is a key architectural difference between a traditional data lake and a lakehouse?

**Answer:** Lakehouse adds ACID transaction guarantees and metadata layer on top of data lake storage ✓

**Explanation:**
Lakehouse architecture (Delta Lake) adds:
- **ACID Transactions:** Atomicity, consistency, isolation, durability
- **Metadata Layer:** Transaction log tracks all changes
- **Schema Enforcement:** Prevents data quality issues
- **Time Travel:** Version history and rollback capability
- **Unified Storage:** Single source of truth for AI and BI workloads
- **Performance Optimizations:** OPTIMIZE, Z-ORDER, data skipping

**Traditional Data Lake limitations:**
- No ACID guarantees (eventual consistency)
- No schema enforcement
- No version history
- Requires separate systems for different workloads
- Manual data quality checks

**Cross-Reference:** See [exam-prep.md](exam-prep.md) for full Lakehouse architecture explanation

## Exam Tips

- Delta Lake = single source of truth (Q2)
- Multiple files, not single file (Q3)
- ACID compliant (Q8)
- MERGE prevents duplicates (Q9)
- VACUUM affects time travel availability (Q1)
- Z-ordering improves query performance (Q11)
- Schema enforcement prevents type mismatches (Week 1 Q1)
- Time travel enables regulatory audits (Week 1 Q2)
- Never VACUUM with 0 hours retention (Week 1 Q3)
- Use mergeSchema for automatic schema evolution (Week 1 Q4)
- Liquid Clustering is incremental and flexible (Week 1 Q5)

## Cross-References

- [Lakeflow Spark Declarative Pipeline (DLT)](delta-live-tables.md) - Pipeline processing on Delta tables
- [CDC & SCD](cdc-scd.md) - Change tracking patterns
- [Tables and Views](tables-views.md) - Table types and metadata
- [Streaming](streaming.md) - Incremental processing

## Sources

- [Databricks_Data_Engineering_Concepts.md](../Databricks_Data_Engineering_Concepts.md)
- References/de_wk3_study_guide.pdf (pending ingestion)
- References/de-mod-3-manage-data-with-delta-lake.pdf (pending ingestion)
