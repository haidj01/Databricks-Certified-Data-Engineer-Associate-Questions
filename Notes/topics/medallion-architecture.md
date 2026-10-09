# Medallion Architecture

**Category:** Architecture & Patterns
**Last Updated:** 2026-09-09

## Overview

The medallion architecture is a data design pattern organizing data into layers: Bronze (raw), Silver (cleaned), and Gold (aggregated). Each layer progressively refines data quality and business value.

**Source:** [Databricks_Data_Engineering_Concepts.md](../Databricks_Data_Engineering_Concepts.md#2-batch-vs-streaming-data-processing)

## Three Layers

### Bronze Layer (Raw)

**Purpose:** Land raw data exactly as received from source

**Characteristics:**
- Minimal transformation
- Original format preserved
- Schema-on-read
- Audit trail of all data

**Processing Recommendation:**
- **Use streaming** for ingestion workloads with stateless processing
- Append-only operations
- Fast, simple ingestion

**Example:**
```python
# Streaming ingestion to Bronze
@dlt.table
def bronze_events():
    return (
        spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load("/source/events/")
    )
```

**Cross-Reference:** See [Streaming](streaming.md) for streaming semantics

### Silver Layer (Cleaned & Conformed)

**Purpose:** Clean, validate, and conform data for analysis

**Characteristics:**
- Data quality rules applied
- Schema enforcement
- Standardized formats
- Deduplicated records
- Enriched with lookups

**Processing Recommendation:**
- **Use batch with incremental refresh** (preferred)
- Streaming only when latency requirements outweigh accuracy concerns
- Stateful transformations acceptable

**Example:**
```sql
CREATE OR REFRESH MATERIALIZED VIEW silver_orders AS
SELECT
  order_id,
  customer_id,
  CAST(order_date AS DATE) as order_date,
  CAST(amount AS DECIMAL(10,2)) as amount,
  status
FROM STREAM(bronze_orders)
WHERE order_id IS NOT NULL
  AND amount > 0;
```

**README Q26: How to identify silver or bronze?**

**Indicators:**
- **Bronze:** Raw schema, all columns, minimal transformation, high volume
- **Silver:** Clean schema, validated data, business-ready types, filtered records

**Source:** [Databricks_Data_Engineering_Concepts.md:115](../Databricks_Data_Engineering_Concepts.md:115)

### Gold Layer (Business-Level Aggregates)

**Purpose:** Serve business-ready, aggregated data for analytics and BI

**Characteristics:**
- Pre-aggregated metrics
- Business logic applied
- Optimized for queries
- Subject-area focused
- Dimension/fact tables

**Processing Recommendation:**
- **Use batch processing** for final aggregations
- Materialized views for frequently accessed aggregates
- Highest data quality

**Example:**
```sql
CREATE OR REFRESH MATERIALIZED VIEW gold_daily_revenue AS
SELECT
  order_date,
  customer_segment,
  COUNT(DISTINCT customer_id) as customers,
  COUNT(*) as orders,
  SUM(amount) as total_revenue,
  AVG(amount) as avg_order_value
FROM silver_orders
GROUP BY order_date, customer_segment;
```

**README Q24: Advantage of gold over silver?**

**Advantages:**
1. **Pre-aggregated** - Faster query performance
2. **Business logic applied** - Consistent calculations
3. **Optimized storage** - Smaller data size
4. **Ready for BI** - No transformation needed
5. **Single source of truth** - Governed metrics

**Cross-Reference:** See [Delta Lake](delta-lake.md) for OPTIMIZE and Z-ordering

## Bronze vs. Raw Table

**README Q25: Difference between bronze and raw?**

### Raw Table
- **Not part of medallion architecture**
- Exact copy of source system
- May include system columns
- Often external table pointing to source

### Bronze Table
- **First medallion layer**
- May include ingestion metadata (timestamp, source file)
- Delta format (ACID guarantees)
- Managed by Databricks
- Foundation for downstream processing

**Key Difference:**
- Raw = source system replica
- Bronze = lakehouse-ready ingestion layer

## Implementation Patterns

### Full Medallion Pipeline

```python
# Bronze: Raw ingestion
@dlt.table
def bronze_transactions():
    return spark.readStream.table("raw.transactions")

# Silver: Cleaning and validation
@dlt.table
@dlt.expect("valid_amount", "amount > 0")
def silver_transactions():
    return (
        dlt.read_stream("bronze_transactions")
        .select("transaction_id", "customer_id", "amount", "transaction_date")
        .filter("transaction_id IS NOT NULL")
    )

# Gold: Business metrics
@dlt.table
def gold_customer_lifetime_value():
    return (
        dlt.read("silver_transactions")
        .groupBy("customer_id")
        .agg(
            F.sum("amount").alias("lifetime_value"),
            F.count("*").alias("transaction_count")
        )
    )
```

### Incremental Processing

**Silver layer with incremental materialized view:**
```sql
CREATE OR REFRESH MATERIALIZED VIEW silver_customers
AS SELECT
  customer_id,
  UPPER(name) as name,
  LOWER(email) as email,
  CURRENT_TIMESTAMP() as processed_at
FROM bronze_customers;
```

## Best Practices

### Bronze Layer
- ✓ Preserve all source data
- ✓ Add ingestion metadata
- ✓ Use streaming for real-time sources
- ✓ Minimal transformation
- ✓ Append-only pattern

### Silver Layer
- ✓ Apply data quality rules
- ✓ Standardize schemas
- ✓ Deduplicate data
- ✓ Use incremental refresh
- ✓ Document transformations

### Gold Layer
- ✓ Pre-aggregate for performance
- ✓ Apply business logic
- ✓ Optimize for query patterns
- ✓ Create dimension/fact tables
- ✓ Z-order key columns

## Common Pitfalls

1. **Too many transformations in Bronze** - Violates raw data principle
2. **Streaming for Gold aggregates** - Adds unnecessary complexity
3. **No quality checks in Silver** - Poor data downstream
4. **Skipping layers** - Loses traceability
5. **Wrong processing mode** - Batch vs. streaming mismatch

## Exam Tips

- Bronze = streaming ingestion (stateless)
- Silver = batch with incremental refresh (preferred)
- Gold = batch for aggregations
- Gold advantages: pre-aggregated, business-ready (Q24)
- Bronze vs. Raw: managed vs. source replica (Q25)
- Identify by schema complexity and transformations (Q26)

## Cross-References

- [Lakeflow Spark Declarative Pipeline (DLT)](delta-live-tables.md) - Pipeline implementation
- [Streaming](streaming.md) - Bronze layer streaming
- [Batch Processing](batch-processing.md) - Silver/Gold batch operations
- [CDC & SCD](cdc-scd.md) - Bronze to Silver patterns

## Sources

- [Databricks_Data_Engineering_Concepts.md](../Databricks_Data_Engineering_Concepts.md#2-batch-vs-streaming-data-processing)
- Practice exam Q24, Q25, Q26, Q31
- Databricks medallion architecture documentation (pending ingestion)
