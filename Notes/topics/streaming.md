# Streaming Processing

**Category:** Data Processing
**Last Updated:** 2026-09-09

## Overview

Structured Streaming in Databricks enables real-time data processing with exactly-once semantics, built on Apache Spark.

**Cross-Reference:** See [Databricks_Data_Engineering_Concepts.md](../Databricks_Data_Engineering_Concepts.md#2-batch-vs-streaming-data-processing) for batch vs. streaming comparison

## Key Concepts

### Batch vs. Streaming Semantics

**Batch:**
- Processes all available data
- Reprocesses on each run
- No state tracking
- Simple logic, always accurate

**Streaming:**
- Processes only new data
- Tracks what's been processed
- Maintains state for joins/aggregations
- Efficient but complex

### Trigger Configuration

#### processingTime Trigger

**README Q17: Set processingTime to 5 seconds**

```python
df.writeStream \
  .trigger(processingTime='5 seconds') \
  .format("delta") \
  .outputMode("append") \
  .start("/path/to/output")
```

**Behavior:**
- Micro-batch every 5 seconds
- Waits for previous batch to complete
- Good for near-real-time (seconds latency)

#### Continuous Processing

**README Q18: Configure for production continuous processing**

```python
df.writeStream \
  .trigger(continuous='1 second') \
  .format("delta") \
  .outputMode("append") \
  .start("/path/to/output")
```

**Note:** As of 2026, continuous mode has limitations:
- Experimental feature
- Limited operation support
- Not recommended for production (Q36)

**Production recommendation:**
```python
# Use availableNow for production
df.writeStream \
  .trigger(availableNow=True) \
  .format("delta") \
  .outputMode("append") \
  .start("/path/to/output")
```

**availableNow:**
- Processes all available data in single batch
- Stops after completion
- Good for scheduled streaming jobs
- Production-ready

#### Once Trigger

```python
df.writeStream \
  .trigger(once=True) \
  .format("delta") \
  .start("/path/to/output")
```

- Processes available data once
- Legacy option (availableNow preferred)

### Output Modes

```python
# Append - only new rows (default)
.outputMode("append")

# Complete - entire result table
.outputMode("complete")

# Update - only updated rows
.outputMode("update")
```

### Watermarks

Handle late-arriving data:

```python
df.withWatermark("timestamp", "10 minutes") \
  .groupBy("category") \
  .count()
```

**Important:** Required for stateful operations to prevent unbounded state growth.

**Cross-Reference:** See [Databricks_Data_Engineering_Concepts.md](../Databricks_Data_Engineering_Concepts.md#6-data-aggregation) for stateful aggregates

### Checkpointing

```python
df.writeStream \
  .option("checkpointLocation", "/path/to/checkpoint") \
  .start()
```

**Purpose:**
- Fault tolerance
- Exactly-once processing
- Tracks processed data
- Required for streaming queries

## Common Patterns

### Stream-Static Join

```python
# Stream from Delta table
streaming_df = spark.readStream.table("bookings")

# Static table
users_df = spark.read.table("users")

# Join
result = streaming_df.join(users_df, "user_id")

result.writeStream \
  .trigger(availableNow=True) \
  .start()
```

**Source:** [Databricks_Data_Engineering_Concepts.md:229](../Databricks_Data_Engineering_Concepts.md:229)

### Streaming Aggregation

```python
df.withWatermark("event_time", "1 hour") \
  .groupBy(
    window("event_time", "1 hour"),
    "user_id"
  ) \
  .count() \
  .writeStream \
  .outputMode("update") \
  .start()
```

### Auto Loader for File Ingestion

**Sample Exam Question (From Official Exam Guide):**

**Scenario:** Building pipelines to consume Databricks audit logs from S3. Need to understand format, latency, and overwrite behavior.

**Question:** What is the audit log format, delivery latency, and can files be overwritten?

**Answer:** JSON format, <15 minute latency, files can be overwritten ✓

**Auto Loader Pattern:**
```python
# Ingest audit logs with Auto Loader
df = spark.readStream \
  .format("cloudFiles") \
  .option("cloudFiles.format", "json") \
  .option("cloudFiles.schemaLocation", "/checkpoint/schema") \
  .load("s3://bucket/audit-logs/")

df.writeStream \
  .option("checkpointLocation", "/checkpoint/audit-logs") \
  .trigger(availableNow=True) \
  .table("audit_logs")
```

**Key Characteristics of Audit Logs:**

1. **Format:** JSON (not Parquet or CSV)
   - Each log entry is a JSON object
   - Schema can evolve over time

2. **Delivery Latency:** <15 minutes
   - Near real-time delivery from Databricks
   - Some delay expected, not instant

3. **Idempotency Required:**
   - Files can be overwritten by Databricks
   - Auto Loader handles this with checkpointing
   - Prevents duplicate processing

**Why Auto Loader:**
- Automatically discovers new files
- Handles schema evolution
- Efficient incremental processing
- Built-in checkpointing for exactly-once semantics
- Scales to millions of files

**Alternatives (not recommended):**
```python
# ❌ Spark readStream without cloudFiles
# - No automatic schema inference
# - Manual file tracking required
spark.readStream.format("json").load("path")

# ❌ Batch processing with glob patterns
# - Reprocesses all files
# - No incremental tracking
spark.read.json("path/*.json")
```

**Cross-Reference:** See [exam-prep.md](exam-prep.md) for full sample question details

## Auto Loader vs COPY INTO Comparison

**Week 3 Study Guide Topic:** Choosing between Auto Loader and COPY INTO for file ingestion

### Overview

Both Auto Loader and COPY INTO are used for incremental file ingestion, but they use different mechanisms and are suited for different scenarios.

**Auto Loader:**
- Streaming-based incremental file ingestion
- Uses file notification or directory listing for tracking
- Part of Structured Streaming API

**COPY INTO:**
- Batch-based incremental file ingestion
- Uses file listing for tracking
- SQL-based operation

### Detailed Comparison

| Feature | Auto Loader | COPY INTO | Winner |
|---------|------------|-----------|--------|
| **API** | Streaming (readStream) | Batch (SQL) | Depends on use case |
| **File Tracking** | File notification (SQS, Event Grid) or directory listing | Directory listing only | **Auto Loader** (more efficient) |
| **Scalability** | Millions of files (file notification) | Thousands of files (listing overhead) | **Auto Loader** |
| **Schema Inference** | Automatic with evolution | Manual schema required | **Auto Loader** |
| **Schema Evolution** | Built-in support with `cloudFiles.schemaEvolutionMode` | Requires `mergeSchema` option | **Auto Loader** |
| **Latency** | Near real-time (continuous) | Scheduled batch (minutes to hours) | **Auto Loader** |
| **Idempotency** | Built-in with checkpointing | Built-in with file tracking | Tie |
| **Cost** | Streaming cluster cost + file notification | Batch cluster cost | **COPY INTO** (lower compute) |
| **Syntax** | Python/Scala (programmatic) | SQL (declarative) | **COPY INTO** (simpler) |
| **File Formats** | All formats (JSON, CSV, Parquet, Avro, ORC) | All formats | Tie |
| **Error Handling** | Stream error handling | SQL error modes | Tie |
| **Cloud Integration** | Native cloud events (S3/ADLS/GCS) | Standard file listing | **Auto Loader** |
| **Learning Curve** | Higher (streaming concepts) | Lower (SQL syntax) | **COPY INTO** |

### File Tracking Mechanisms

#### Auto Loader - File Notification (Recommended)

**How it works:**
- Cloud storage sends notifications to queue (SQS, Event Grid, Pub/Sub)
- Auto Loader listens to queue for new file events
- Processes only notified files
- Scales to millions of files with constant overhead

**Configuration:**
```python
df = spark.readStream \
  .format("cloudFiles") \
  .option("cloudFiles.format", "json") \
  .option("cloudFiles.useNotifications", "true") \
  .option("cloudFiles.schemaLocation", "/checkpoint/schema") \
  .load("s3://bucket/landing/")
```

**Requirements:**
- AWS: S3 bucket configured with SQS/SNS notifications
- Azure: ADLS Gen2 with Event Grid subscriptions
- GCP: GCS with Pub/Sub notifications

**Benefits:**
- ✓ O(1) complexity for file discovery
- ✓ Instant notification of new files
- ✓ No periodic directory listing overhead
- ✓ Scales to millions of files

#### Auto Loader - Directory Listing (Fallback)

**How it works:**
- Periodically lists directory for new files
- Compares with previous list to find new files
- Processes delta between lists

**Configuration:**
```python
df = spark.readStream \
  .format("cloudFiles") \
  .option("cloudFiles.format", "json") \
  .option("cloudFiles.useNotifications", "false") \
  .option("cloudFiles.schemaLocation", "/checkpoint/schema") \
  .load("s3://bucket/landing/")
```

**When to use:**
- Cloud notifications not available
- Simpler setup (no cloud event configuration)
- Smaller file volumes (< 10,000 files)

**Limitations:**
- O(n) complexity for file listing
- Periodic polling overhead
- Delayed file discovery

#### COPY INTO - File Listing

**How it works:**
- Maintains internal metadata of processed files
- Lists directory on each execution
- Compares with metadata to find new files
- Processes only new files

**Configuration:**
```sql
COPY INTO bronze.sales
FROM '/mnt/landing/sales/'
FILEFORMAT = PARQUET
FORMAT_OPTIONS ('mergeSchema' = 'true')
COPY_OPTIONS ('force' = 'false');
```

**Characteristics:**
- File tracking stored in table metadata
- Idempotent (reruns skip already processed files)
- Efficient for thousands of files
- Performance degrades with 10,000+ files (listing overhead)

### Schema Inference and Evolution

#### Auto Loader - Automatic Schema Inference

**Powerful schema management:**
```python
df = spark.readStream \
  .format("cloudFiles") \
  .option("cloudFiles.format", "json") \
  .option("cloudFiles.schemaLocation", "/checkpoint/schema") \
  .option("cloudFiles.inferColumnTypes", "true") \
  .option("cloudFiles.schemaEvolutionMode", "addNewColumns") \
  .load("s3://bucket/data/")
```

**Schema Evolution Modes:**

| Mode | Behavior | Use Case |
|------|----------|----------|
| `addNewColumns` | Automatically add new columns | **Recommended** - handles evolving schemas |
| `rescue` | Put unmatched data in `_rescued_data` column | Schema validation, data quality |
| `failOnNewColumns` | Fail stream if new columns detected | Strict schema enforcement |
| `none` | No evolution, use initial schema | Static schema (default) |

**Example:**
```python
# Day 1: Files have columns [id, name, amount]
# Day 2: Files have columns [id, name, amount, category]
# Result: Auto Loader adds "category" column automatically
#         Old records have NULL for category

df = spark.readStream \
  .format("cloudFiles") \
  .option("cloudFiles.format", "json") \
  .option("cloudFiles.schemaLocation", "/mnt/checkpoint/sales_schema") \
  .option("cloudFiles.schemaEvolutionMode", "addNewColumns") \
  .load("/mnt/landing/sales/")

df.writeStream \
  .option("checkpointLocation", "/mnt/checkpoint/sales") \
  .option("mergeSchema", "true") \
  .table("bronze.sales")
```

**Benefits:**
- Zero-configuration schema handling
- Automatic type inference
- Built-in schema evolution
- Rescued data column for debugging

#### COPY INTO - Manual Schema Management

**Requires explicit schema or mergeSchema:**
```sql
-- Option 1: Explicit schema (recommended)
COPY INTO bronze.sales
FROM (
  SELECT id::INT,
         name::STRING,
         amount::DOUBLE,
         category::STRING
  FROM '/mnt/landing/sales/'
)
FILEFORMAT = JSON
COPY_OPTIONS ('force' = 'false');

-- Option 2: Schema evolution with mergeSchema
COPY INTO bronze.sales
FROM '/mnt/landing/sales/'
FILEFORMAT = JSON
FORMAT_OPTIONS ('mergeSchema' = 'true');
```

**Limitations:**
- Manual schema definition required
- `mergeSchema` adds columns but doesn't infer types
- No automatic type detection
- Must update schema manually for new columns

### Scalability Comparison

#### Auto Loader - Millions of Files

**File Notification Mode:**
```
File Count: 10,000,000 files
File Discovery: O(1) - event-driven
Processing Time: ~5 seconds to start
Memory Overhead: Constant (queue-based)
```

**Example scenario:**
```python
# IoT sensor data - millions of small JSON files
# Auto Loader with file notification

df = spark.readStream \
  .format("cloudFiles") \
  .option("cloudFiles.format", "json") \
  .option("cloudFiles.useNotifications", "true") \
  .option("cloudFiles.schemaLocation", "/checkpoint/iot_schema") \
  .load("s3://iot-data/sensors/")

# Efficiently processes 10M+ files with constant overhead
```

#### COPY INTO - Thousands of Files

**Directory Listing Mode:**
```
File Count: 10,000 files
File Discovery: O(n) - full directory scan
Processing Time: ~30-60 seconds to start
Memory Overhead: Linear with file count
```

**Performance degradation:**
```sql
-- Works well for < 10,000 files
COPY INTO bronze.sales
FROM '/mnt/landing/sales/'
FILEFORMAT = PARQUET;

-- Performance issues with 100,000+ files:
-- - Slow directory listing (minutes)
-- - High memory usage for file tracking
-- - Better to partition data or use Auto Loader
```

### Performance Characteristics

#### Auto Loader

**Strengths:**
- Constant-time file discovery with notifications
- Low latency (near real-time)
- Efficient for continuous ingestion
- Handles backfill efficiently

**Overhead:**
- Streaming cluster must stay running (higher cost)
- File notification setup (cloud configuration)
- Checkpoint storage overhead

**Best performance:**
```python
# Optimized Auto Loader configuration
df = spark.readStream \
  .format("cloudFiles") \
  .option("cloudFiles.format", "parquet") \
  .option("cloudFiles.useNotifications", "true") \
  .option("cloudFiles.maxFilesPerTrigger", "1000") \
  .option("cloudFiles.schemaLocation", "/checkpoint/schema") \
  .load("/mnt/landing/")

df.writeStream \
  .option("checkpointLocation", "/checkpoint/data") \
  .trigger(availableNow=True) \
  .table("bronze.data")
```

#### COPY INTO

**Strengths:**
- Lower compute cost (batch execution)
- Simple SQL syntax
- No checkpoint management
- Good for scheduled batch ingestion

**Overhead:**
- Directory listing time (grows with file count)
- Cold start for each execution
- Manual orchestration required

**Best performance:**
```sql
-- Optimized COPY INTO with partitioning
COPY INTO bronze.sales
FROM '/mnt/landing/sales/year=2026/month=09/'
FILEFORMAT = PARQUET
PATTERN = '*.parquet'
COPY_OPTIONS ('force' = 'false');
```

### Code Examples - Same Use Case

**Scenario:** Ingest daily CSV files from S3 landing zone into bronze layer

#### Auto Loader Approach

```python
# Auto Loader - Streaming ingestion
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

# Define schema (optional, but recommended for performance)
schema = StructType([
  StructField("order_id", StringType(), True),
  StructField("customer_id", StringType(), True),
  StructField("amount", DoubleType(), True),
  StructField("order_date", TimestampType(), True)
])

# Auto Loader with schema hint
df = spark.readStream \
  .format("cloudFiles") \
  .option("cloudFiles.format", "csv") \
  .option("cloudFiles.useNotifications", "true") \
  .option("cloudFiles.schemaLocation", "/mnt/checkpoint/orders_schema") \
  .option("cloudFiles.inferColumnTypes", "true") \
  .option("cloudFiles.schemaEvolutionMode", "addNewColumns") \
  .schema(schema) \
  .load("s3://landing-zone/orders/")

# Write to bronze with checkpointing
df.writeStream \
  .format("delta") \
  .option("checkpointLocation", "/mnt/checkpoint/orders") \
  .option("mergeSchema", "true") \
  .trigger(availableNow=True) \
  .table("bronze.orders")

# Result: Processes all existing files + automatically ingests new files
```

**Advantages:**
- Automatic schema inference
- Handles schema changes (new columns)
- Scales to millions of files
- Near real-time ingestion
- No manual orchestration

**Disadvantages:**
- Higher cost (streaming cluster)
- More complex setup (cloud notifications)

#### COPY INTO Approach

```sql
-- COPY INTO - Batch ingestion (schedule in Lakeflow Jobs)

-- Create target table with explicit schema
CREATE TABLE IF NOT EXISTS bronze.orders (
  order_id STRING,
  customer_id STRING,
  amount DOUBLE,
  order_date TIMESTAMP
) USING DELTA;

-- COPY INTO with idempotent execution
COPY INTO bronze.orders
FROM 's3://landing-zone/orders/'
FILEFORMAT = CSV
FORMAT_OPTIONS (
  'header' = 'true',
  'inferSchema' = 'false',
  'timestampFormat' = 'yyyy-MM-dd HH:mm:ss'
)
COPY_OPTIONS ('force' = 'false');

-- Schedule this SQL in Lakeflow Jobs (e.g., every hour)
```

**Advantages:**
- Lower cost (batch execution)
- Simple SQL syntax
- Easy to understand and maintain
- Good for scheduled hourly/daily ingestion

**Disadvantages:**
- Manual schema management
- Higher latency (batch intervals)
- Performance issues with 10,000+ files
- Requires job orchestration

### When to Use Each

#### Use Auto Loader When:

1. **High file volume** (10,000+ files)
   - File notification scales to millions
   - Directory listing becomes bottleneck with COPY INTO

2. **Near real-time latency required**
   - Streaming provides continuous ingestion
   - COPY INTO limited to batch intervals

3. **Schema evolution expected**
   - Automatic schema inference and evolution
   - Rescued data column for debugging

4. **Complex file formats** (nested JSON, Avro)
   - Better schema inference for complex types
   - Handles schema changes gracefully

5. **IoT/Event streaming** use cases
   - Continuous file generation
   - Low-latency requirements

**Example scenarios:**
- IoT sensor data (millions of small JSON files)
- Application logs (continuous stream)
- CDC files from Kafka Connect
- Real-time analytics pipelines

#### Use COPY INTO When:

1. **Low to moderate file volume** (< 10,000 files)
   - Efficient with smaller file counts
   - Simpler setup than Auto Loader

2. **Scheduled batch ingestion** (hourly, daily)
   - Cost-effective for periodic loads
   - No need for always-on streaming cluster

3. **Simple, stable schemas**
   - Schema rarely changes
   - Explicit control over schema preferred

4. **SQL-first teams**
   - Familiar SQL syntax
   - No Python/Scala required

5. **Regulatory/compliance** requirements
   - Explicit batch boundaries
   - Scheduled processing windows

**Example scenarios:**
- Daily sales reports from external vendor
- Weekly data exports from SaaS applications
- Monthly financial data loads
- Hourly aggregated reports

### Best Practices

#### Auto Loader Best Practices

```python
# 1. Use file notification for scalability
spark.readStream \
  .format("cloudFiles") \
  .option("cloudFiles.useNotifications", "true") \
  .option("cloudFiles.region", "us-east-1") \
  .option("cloudFiles.resourceGroup", "databricks-rg")

# 2. Provide schema hint for performance
.schema(schema)

# 3. Enable schema evolution for flexibility
.option("cloudFiles.schemaEvolutionMode", "addNewColumns")

# 4. Set maxFilesPerTrigger for backfill control
.option("cloudFiles.maxFilesPerTrigger", "1000")

# 5. Use availableNow trigger for scheduled streaming
.trigger(availableNow=True)

# 6. Store checkpoint in separate location
.option("checkpointLocation", "/mnt/checkpoints/my_stream")

# 7. Partition output for query performance
.partitionBy("year", "month") \
.table("bronze.my_table")
```

#### COPY INTO Best Practices

```sql
-- 1. Partition landing zone for efficiency
COPY INTO bronze.sales
FROM '/mnt/landing/sales/year=2026/month=09/'
FILEFORMAT = PARQUET;

-- 2. Use explicit schema (avoid inferSchema)
COPY INTO bronze.customers
FROM (
  SELECT customer_id::STRING,
         name::STRING,
         email::STRING,
         created_at::TIMESTAMP
  FROM '/mnt/landing/customers/'
)
FILEFORMAT = CSV;

-- 3. Use PATTERN to filter files
COPY INTO bronze.logs
FROM '/mnt/landing/logs/'
FILEFORMAT = JSON
PATTERN = 'log_2026-09-*.json';

-- 4. Set force=false for idempotency (default)
COPY_OPTIONS ('force' = 'false');

-- 5. Monitor copy history
SELECT * FROM bronze.sales
WHERE _metadata.file_path LIKE '%landing%'
ORDER BY _metadata.file_modification_time DESC;

-- 6. Handle schema evolution explicitly
FORMAT_OPTIONS ('mergeSchema' = 'true');
```

### Migration Path: COPY INTO → Auto Loader

**When to migrate:**
- File count exceeds 10,000
- Latency requirements become more stringent
- Schema evolution becomes frequent

**Migration steps:**

```python
# Step 1: Analyze current COPY INTO pattern
# SQL: COPY INTO bronze.sales FROM '/mnt/landing/sales/' FILEFORMAT = PARQUET

# Step 2: Create Auto Loader equivalent
df = spark.readStream \
  .format("cloudFiles") \
  .option("cloudFiles.format", "parquet") \
  .option("cloudFiles.useNotifications", "true") \
  .option("cloudFiles.schemaLocation", "/checkpoint/sales_schema") \
  .load("/mnt/landing/sales/")

# Step 3: Backfill existing files
df.writeStream \
  .option("checkpointLocation", "/checkpoint/sales") \
  .trigger(availableNow=True) \
  .table("bronze.sales")

# Step 4: Switch to continuous mode after backfill
# Change trigger to processingTime for near real-time
```

### Cost Comparison Example

**Scenario:** Ingest 1,000 files per day (100 MB each)

#### Auto Loader Cost

```
Streaming cluster: 4 workers × 24 hours = 96 worker-hours/day
DBU rate: 0.40 DBU/worker-hour
Daily DBU cost: 96 × 0.40 = 38.4 DBUs/day

File notification cost:
- S3 events: $0.05 per 1,000 events = $0.05/day
- SQS messages: $0.40 per 1M requests = negligible

Total: ~38.4 DBUs/day + $0.05 cloud events
```

#### COPY INTO Cost

```
Job cluster: 4 workers × 0.5 hours (30 min batch) = 2 worker-hours/day
DBU rate: 0.40 DBU/worker-hour
Daily DBU cost: 2 × 0.40 = 0.8 DBUs/day

No cloud event costs

Total: ~0.8 DBUs/day
```

**Cost difference:** COPY INTO is ~48x cheaper for scheduled batch use case

**Cost breakeven:**
- Auto Loader becomes cost-effective when latency SLA < 1 hour
- Or when file count > 10,000 (COPY INTO performance degrades)

### Exam Tips

**Common exam question patterns:**

1. **"Millions of files"** → **Auto Loader** (scalability)
2. **"Near real-time"** → **Auto Loader** (streaming)
3. **"Scheduled hourly"** → **COPY INTO** (batch, cost-effective)
4. **"Schema changes frequently"** → **Auto Loader** (schema evolution)
5. **"Simple SQL syntax"** → **COPY INTO** (SQL-first)
6. **"Low latency required"** → **Auto Loader** (continuous)
7. **"Cost-conscious manager"** → **COPY INTO** (batch)
8. **"10,000+ files"** → **Auto Loader** (notification-based)

**Key differentiators:**
- Auto Loader = streaming, scalable, schema evolution
- COPY INTO = batch, simple SQL, cost-effective

**Cross-Reference:** See [Batch Processing](batch-processing.md) for COPY INTO details, [Cost Optimization](cost-optimization.md) for cluster cost comparison

## Medallion Architecture Recommendations

From [Databricks_Data_Engineering_Concepts.md:115](../Databricks_Data_Engineering_Concepts.md:115):

- **Bronze:** Streaming for ingestion (stateless)
- **Silver:** Batch with incremental refresh (streaming only if latency critical)
- **Gold:** Batch processing for aggregations

**Cross-Reference:** See [Medallion Architecture](medallion-architecture.md)

## Common Pitfalls

1. **No watermark for stateful ops** - Unbounded state growth
2. **Continuous mode in production** - Not production-ready (Q36)
3. **Wrong output mode** - Data duplication or loss
4. **Missing checkpoint location** - No fault tolerance
5. **Streaming for everything** - Added complexity when batch suffices

## Exam Tips

- processingTime = micro-batch interval (Q17)
- availableNow = production batch streaming (Q18, Q36)
- Continuous = experimental, not for production (Q36)
- Watermarks required for stateful operations
- Bronze = streaming, Silver/Gold = batch (best practice)

## Cross-References

- [Lakeflow Spark Declarative Pipeline (DLT)](delta-live-tables.md) - Declarative streaming
- [Batch Processing](batch-processing.md) - When to use batch
- [Medallion Architecture](medallion-architecture.md) - Layer-specific patterns

## Sources

- [Databricks_Data_Engineering_Concepts.md](../Databricks_Data_Engineering_Concepts.md)
- Practice exam Q17, Q18, Q36
- Structured Streaming documentation (pending ingestion)
