# Change Data Capture (CDC) & Slowly Changing Dimensions (SCD)

**Category:** Architecture & Patterns
**Last Updated:** 2026-09-09

## Overview

CDC and SCD patterns enable efficient synchronization of data from source systems while maintaining historical context.

**Source:** [Databricks_Data_Engineering_Concepts.md](../Databricks_Data_Engineering_Concepts.md#4-change-data-capture-and-snapshots)

## Change Data Capture (CDC)

### Core Concept

CDC tracks **changes** (inserts, updates, deletes) instead of reprocessing entire datasets.

**Benefits:**
- Reduced data volume (only changes transferred)
- Historical reconstruction capability
- Stable surrogate key maintenance

### CDC Feeds vs. Snapshots

#### CDC Feeds
- Record-level operations with metadata
- Operation type (INSERT, UPDATE, DELETE)
- Sequence numbers for ordering
- Native from transactional databases

**Example structure:**
```
| id | name  | op_type | seq_num | timestamp |
|----|-------|---------|---------|-----------|
| 1  | Alice | INSERT  | 1       | 10:00     |
| 1  | Alice | UPDATE  | 2       | 11:00     |
| 2  | Bob   | INSERT  | 3       | 12:00     |
```

#### Snapshots
- Complete table state at specific time
- No operation metadata
- Used when CDC unavailable
- Full table dump per period

**When to use snapshots:**
- CDC not available from source
- Cost/performance constraints
- Legacy systems
- Organizational limitations

## Slowly Changing Dimensions (SCD)

### SCD Type 1: Current State Only

**Approach:** Overwrite old data with new data

```sql
MERGE INTO target t
USING source s ON t.id = s.id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

**Characteristics:**
- Only latest version kept
- No history
- Simple implementation
- Less storage

**Use when:**
- History not required
- Incremental materialized views
- Current state sufficient

**Source:** [Databricks_Data_Engineering_Concepts.md:162](../Databricks_Data_Engineering_Concepts.md:162)

### SCD Type 2: Historical Tracking

**Approach:** Create multiple versions with validity timestamps

```sql
-- Table structure
CREATE TABLE customers (
  id INT,
  name STRING,
  email STRING,
  __START_AT TIMESTAMP,
  __END_AT TIMESTAMP
);

-- Active records
SELECT * FROM customers WHERE __END_AT IS NULL;

-- Historical records
SELECT * FROM customers WHERE __END_AT IS NOT NULL;
```

**Characteristics:**
- Complete history preserved
- Multiple versions per entity
- Validity period tracking
- More storage required

**Use when:**
- Regulatory compliance needed
- Trend analysis required
- Auditing essential
- Understanding entity evolution

**Source:** [Databricks_Data_Engineering_Concepts.md:165](../Databricks_Data_Engineering_Concepts.md:165)

## Automated Processing

### AUTO CDC API

Processes CDC feeds automatically:

```python
import dlt
from pyspark.sql.functions import col

@dlt.table
def target_table():
    return dlt.read_stream("cdc_source") \
        .apply_changes(
            target="target_table",
            source="cdc_source",
            keys=["id"],
            sequence_by="sequence_num",
            apply_as_deletes=col("op_type") == "DELETE",
            except_column_list=["op_type", "sequence_num"]
        )
```

**Features:**
- Automatic out-of-order record handling
- INSERT, UPDATE, DELETE operations
- Change Data Feed emission

**Source:** [Databricks_Data_Engineering_Concepts.md:176](../Databricks_Data_Engineering_Concepts.md:176)

### AUTO CDC FROM SNAPSHOT API

Generates synthetic CDC from snapshots:

```python
import dlt

@dlt.table
def target_from_snapshots():
    return (
        dlt.apply_changes_from_snapshot(
            source="snapshot_table",
            keys=["id"],
            snapshot_version=col("snapshot_date"),
            row_version=col("updated_at")
        )
    )
```

**Features:**
- Compares consecutive snapshots
- Derives SCD logic automatically
- Requires ascending version order
- Python-only feature

**Source:** [Databricks_Data_Engineering_Concepts.md:177](../Databricks_Data_Engineering_Concepts.md:177)

## Version Determination

### Pipeline Ingestion Time
```python
@dlt.table
def bronze():
    return spark.read.format("delta") \
        .option("versionAsOf", execution_timestamp) \
        .load("/path/to/snapshots")
```

### Version Functions
```python
def get_snapshot_version():
    df = spark.read.load("/path")
    version = df.select("snapshot_id").first()[0]
    return (df, version)
```

**Source:** [Databricks_Data_Engineering_Concepts.md:180](../Databricks_Data_Engineering_Concepts.md:180)

## Additional Capabilities

**Metrics tracked:**
- `num_upserted_rows`
- `num_deleted_rows`

**Column-subset tracking:**
- Track only critical attributes for SCD Type 2
- Reduces storage while preserving key history

**Source:** [Databricks_Data_Engineering_Concepts.md:190](../Databricks_Data_Engineering_Concepts.md:190)

## Decision Matrix

| Scenario | Approach |
|----------|----------|
| Need change-only processing | CDC |
| Full dumps only available | Snapshots |
| Current state sufficient | SCD Type 1 |
| History required | SCD Type 2 |
| Native CDC available | AUTO CDC |
| Only snapshots available | AUTO CDC FROM SNAPSHOT |

**Source:** [Databricks_Data_Engineering_Concepts.md:195](../Databricks_Data_Engineering_Concepts.md:195)

## Common Pitfalls

1. **SCD Type 2 without cleanup** - Unbounded growth
2. **Missing sequence numbers** - Out-of-order problems
3. **No validity tracking** - Can't query point-in-time
4. **Wrong SCD type** - Either too much or too little history

## Exam Tips

- SCD Type 1 = overwrite, no history
- SCD Type 2 = multiple versions with timestamps
- CDC = change-only processing
- Snapshots = full state at intervals
- AUTO CDC = for native feeds
- AUTO CDC FROM SNAPSHOT = synthetic CDC from dumps

## Cross-References

- [Delta Lake](delta-lake.md) - MERGE operations
- [Lakeflow Spark Declarative Pipeline (DLT)](delta-live-tables.md) - apply_changes API
- [Medallion Architecture](medallion-architecture.md) - Bronze layer ingestion

## Sources

- [CDC_SCD_REVIEW.md](../CDC_SCD_REVIEW.md)
- [Databricks_Data_Engineering_Concepts.md](../Databricks_Data_Engineering_Concepts.md#4-change-data-capture-and-snapshots)
