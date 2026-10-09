# Lakeflow Spark Declarative Pipeline (DLT)

**Category:** Core Technologies
**Last Updated:** 2026-09-09
**Terminology:** Formerly "Delta Live Tables" (DLT). Renamed to "Lakeflow Spark Declarative Pipeline" as of May 2026. Both names may appear on the exam.

## Overview

Lakeflow Spark Declarative Pipeline (DLT) is a declarative framework for building reliable, maintainable, and testable data pipelines on Delta Lake. It uses declarative syntax where you specify WHAT you want, not HOW to do it.

**Cross-Reference:** See [Databricks_Data_Engineering_Concepts.md](../Databricks_Data_Engineering_Concepts.md#1-procedural-vs-declarative-data-processing) for procedural vs. declarative comparison

## Key Concepts

### Pipeline Components

#### Streaming Tables
```sql
CREATE OR REFRESH STREAMING TABLE table_name
AS SELECT * FROM STREAM(source_table);
```

- Process data incrementally using streaming semantics
- Track processed records
- Handle only new data on refresh

**Cross-Reference:** See [Streaming](streaming.md) for detailed streaming concepts

#### Materialized Views
```sql
CREATE OR REFRESH MATERIALIZED VIEW view_name
AS SELECT * FROM source_table;
```

- Process all data using batch semantics
- Recompute results on refresh
- Better for aggregations and joins

**Note:** Materialized views use batch, streaming tables use streaming (README Q21)

### Data Quality Expectations

Documentation: https://docs.databricks.com/workflows/delta-live-tables/delta-live-tables-expectations.html

#### EXPECT
Logs violations but allows data to pass through.

```sql
CREATE STREAMING TABLE orders (
  CONSTRAINT valid_date EXPECT (order_date IS NOT NULL)
)
```

**Behavior (README Q13):**
- Records quality metrics
- Does NOT drop invalid records
- Pipeline continues processing

#### EXPECT OR DROP
Drops rows that violate the constraint.

```sql
CREATE STREAMING TABLE orders (
  CONSTRAINT valid_date EXPECT (order_date IS NOT NULL) ON VIOLATION DROP ROW
)
```

**Behavior (README Q13):**
- Invalid rows are dropped
- Violations logged in metrics
- Only valid data proceeds

#### EXPECT OR FAIL
Fails the pipeline on any violation.

```sql
CREATE STREAMING TABLE orders (
  CONSTRAINT valid_date EXPECT (order_date IS NOT NULL) ON VIOLATION FAIL UPDATE
)
```

**Behavior:**
- Pipeline stops on first violation
- No data written
- Manual intervention required

### Creating Dependent Tasks

**README Q27:**

Tasks become dependent through table references:

```sql
-- Bronze layer
CREATE STREAMING TABLE bronze_orders
AS SELECT * FROM cloud_files('/data/orders', 'json');

-- Silver layer (depends on bronze)
CREATE STREAMING TABLE silver_orders
AS SELECT * FROM STREAM(bronze_orders)
WHERE order_date IS NOT NULL;

-- Gold layer (depends on silver)
CREATE MATERIALIZED VIEW gold_daily_revenue
AS SELECT date, SUM(amount) as revenue
FROM silver_orders
GROUP BY date;
```

Dependencies are inferred automatically from table references.

### Data Quality Monitoring

**Where to see metrics (README Q30):**
- DLT pipeline event logs
- Pipeline details UI
- Metrics dashboard
- System tables

Metrics tracked:
- `num_rows_passing_expectations`
- `num_rows_dropped`
- `num_rows_failing_expectations`
- Pipeline run statistics

### Pipeline Execution

**How to execute (README Q31):**

1. **UI:** Pipeline > Start/Refresh button
2. **API:**
```python
POST /api/2.0/pipelines/{pipeline_id}/updates
```
3. **Jobs:** Schedule as Databricks workflow task
4. **CLI:**
```bash
databricks pipelines run --pipeline-id <id>
```

### Streaming Live Status

**README Q21:**

When a table is marked as "Streaming Live":
- Pipeline is actively processing
- Incremental data ingestion is happening
- New records are continuously arriving
- Source is being monitored for changes

## Common Pitfalls

1. **Using streaming for aggregations** - Use materialized views instead
2. **Not setting expectations** - Missing data quality validation
3. **Wrong expectation type** - DROP vs. EXPECT vs. FAIL
4. **Forgetting dependencies** - Manual task ordering instead of declarative

## Exam Tips

- EXPECT = log violations (Q13)
- EXPECT OR DROP = remove invalid rows (Q13)
- Streaming vs. Materialized views = incremental vs. batch (Q21)
- Dependencies created through table references (Q27)
- Metrics available in event logs and UI (Q30)
- Multiple execution methods available (Q31)

## Cross-References

- [Delta Lake](delta-lake.md) - Underlying storage layer
- [Streaming](streaming.md) - Streaming semantics
- [Data Quality](data-quality.md) - Expectations and constraints
- [Workflows](workflows.md) - Pipeline scheduling

## Sources

- [Databricks_Data_Engineering_Concepts.md](../Databricks_Data_Engineering_Concepts.md)
- References/de-mod-4-build-data-pipelines-with-delta-live-tables.pdf (pending ingestion)
- https://docs.databricks.com/workflows/delta-live-tables/delta-live-tables-expectations.html
