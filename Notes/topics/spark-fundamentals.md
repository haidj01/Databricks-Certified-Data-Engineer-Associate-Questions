# Spark & PySpark Fundamentals

**Category:** Data Processing
**Last Updated:** 2026-09-09

## Overview

Apache Spark APIs for distributed data processing in Databricks.

## Accessing Tables

**README Q38: spark.table() vs. spark.delta.table() vs. spark.sql()**

### spark.table()

**Recommended method:**

```python
df = spark.table("catalog.schema.table_name")
df = spark.table("mytable")  # Uses current catalog/schema
```

**Advantages:**
- Returns DataFrame
- Unity Catalog aware
- Simplest syntax
- Type-safe

### spark.sql()

```python
df = spark.sql("SELECT * FROM mytable")
```

**Use when:**
- Complex SQL queries
- Mixing SQL and DataFrame operations
- Legacy code compatibility

**Note:** `spark.sql("mytable")` is INCORRECT - requires SELECT statement

### spark.delta.table()

**Legacy/specific use:**

```python
from delta.tables import DeltaTable

dt = DeltaTable.forName(spark, "mytable")
```

**Use when:**
- Delta-specific operations (MERGE, UPDATE, DELETE)
- Table metadata access
- Advanced Delta features

**Best practice:** Use `spark.table()` for reads, `DeltaTable` for writes

## Array Functions

**README Q16: Advantages of array functions**

### Common Array Functions

```python
from pyspark.sql import functions as F

# Explode array into rows
df.select(F.explode("array_column"))

# Array contains
df.filter(F.array_contains("tags", "important"))

# Array size
df.select(F.size("array_column"))

# Array distinct
df.select(F.array_distinct("array_column"))

# Array intersection
df.select(F.array_intersect("arr1", "arr2"))
```

### Advantages

1. **Process nested data efficiently** without UDFs
2. **Avoid expensive joins** on array elements
3. **Native optimization** by Spark engine
4. **Type-safe operations** with compile-time checks
5. **Better performance** than custom Python functions

**Example:**
```python
# Instead of explode + join
df.select(F.array_contains("categories", "electronics"))

# Better than:
df.select(F.explode("categories")) \
  .filter(col("col") == "electronics")
```

## JDBC Connections

**README Q39: JDBC driver for SQLite**

```python
df = spark.read \
  .format("jdbc") \
  .option("url", "jdbc:sqlite:/path/to/database.db") \
  .option("driver", "org.sqlite.JDBC") \
  .option("dbtable", "table_name") \
  .load()
```

**Driver name:** `org.sqlite.JDBC`

**Common JDBC drivers:**
- MySQL: `com.mysql.jdbc.Driver`
- PostgreSQL: `org.postgresql.Driver`
- SQL Server: `com.microsoft.sqlserver.jdbc.SQLServerDriver`
- Oracle: `oracle.jdbc.driver.OracleDriver`
- SQLite: `org.sqlite.JDBC`

## Deduplication Strategies

**README Q40: Combine march_transaction and april_transaction without duplicates**

### Method 1: UNION with DISTINCT (recommended)

```python
march_df = spark.table("march_transaction")
april_df = spark.table("april_transaction")

all_transactions = march_df.union(april_df).distinct()
```

```sql
CREATE TABLE all_transaction AS
SELECT DISTINCT * FROM (
  SELECT * FROM march_transaction
  UNION ALL
  SELECT * FROM april_transaction
);
```

### Method 2: UNION with GROUP BY

```python
all_transactions = march_df.union(april_df) \
  .groupBy("transaction_id") \
  .agg(F.first("amount"))
```

### Method 3: Join and COALESCE

```python
all_transactions = march_df.join(
  april_df,
  on=["transaction_id"],
  how="full_outer"
).select(
  F.coalesce(march_df.transaction_id, april_df.transaction_id),
  # ... other columns
).distinct()
```

**Best practice:** UNION + DISTINCT for simplicity

## DataFrame Transformations

### Common Patterns

```python
# Select columns
df.select("col1", "col2")

# Filter rows
df.filter(col("amount") > 100)
df.where(col("status") == "active")

# Add columns
df.withColumn("new_col", col("old_col") * 2)

# Rename columns
df.withColumnRenamed("old_name", "new_name")

# Drop columns
df.drop("col1", "col2")

# Group and aggregate
df.groupBy("category").agg(
  F.sum("amount").alias("total"),
  F.count("*").alias("count")
)
```

## Performance Optimization

### Caching

```python
# Cache in memory
df.cache()

# Persist with storage level
from pyspark import StorageLevel
df.persist(StorageLevel.MEMORY_AND_DISK)

# Unpersist when done
df.unpersist()
```

**README Q28, Q45: Speed up query execution**

**Methods:**
1. **Cache frequently accessed data**
2. **Use cluster pools** (see [Cost Optimization](cost-optimization.md))
3. **Partition data appropriately**
4. **Use Z-ordering** (see [Delta Lake](delta-lake.md))
5. **Enable adaptive query execution**
6. **Broadcast small tables**

```python
# Broadcast join
from pyspark.sql.functions import broadcast

large_df.join(broadcast(small_df), "key")
```

### Adaptive Query Execution

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
```

## Troubleshooting Data Skew

**Sample Exam Question (From Official Exam Guide):**

**Scenario:** A scheduled job's duration has doubled. Spark UI shows most tasks finish in <30 seconds, but one task takes 10+ minutes. Shuffle read metrics show Min/Median 400MB, Max 5GB.

**Question:** What should you do?

**Answer:** Confirm adaptive query execution with skew join handling is active ✓

### Identifying Data Skew

**Symptoms:**
- One or few tasks take much longer than others
- Large difference between min/median and max shuffle read sizes
- Stage duration dominated by single task
- Uneven executor utilization

**Solutions:**

1. **Enable Adaptive Query Execution (recommended):**
```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "256MB")
```

**How AQE handles skew:**
- Detects skewed partitions automatically
- Splits large partitions into smaller sub-partitions
- Optimizes join strategy dynamically

2. **Manual Salting (if AQE insufficient):**
```python
from pyspark.sql.functions import concat, lit, rand

# Add salt to skewed key
df_salted = df.withColumn("salted_key",
    concat(col("key"), lit("_"), (rand() * 10).cast("int")))

# Join with exploded dimension
result = df_salted.join(dim_exploded, "salted_key")
```

3. **Repartition by skewed column:**
```python
df.repartition(200, "skewed_column")
```

**Cross-Reference:** See [exam-prep.md](exam-prep.md) for full sample question details

## Common Pitfalls

1. **Using spark.sql("tablename")** - Missing SELECT
2. **Not caching reused DataFrames** - Redundant computation
3. **Too many small files** - Slow reads
4. **UDFs instead of native functions** - Performance loss
5. **Collect() on large data** - OOM errors

## Exam Tips

- spark.table() = recommended for table access (Q38)
- Array functions = efficient nested data processing (Q16)
- SQLite driver = org.sqlite.JDBC (Q39)
- UNION + DISTINCT = remove duplicates (Q40)
- Cache + cluster pools = speed up queries (Q28, Q45)

## Cross-References

- [Delta Lake](delta-lake.md) - OPTIMIZE, Z-ordering
- [Cost Optimization](cost-optimization.md) - Cluster pools
- [Streaming](streaming.md) - Structured Streaming APIs

## Sources

- [References/pyspark-notes.md](../References/pyspark-notes.md)
- Practice exam questions
- Spark documentation (pending ingestion)
