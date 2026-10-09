# Databricks Data Engineer Certification - Knowledge Index

**Last Updated:** 2026-09-30

## 📚 Core Concepts

### Databricks Fundamentals
- [Databricks Data Engineering Concepts](Databricks_Data_Engineering_Concepts.md)
  - Procedural vs. Declarative Processing
  - Batch vs. Streaming Data Processing
  - Tables and Views
  - Change Data Capture and Snapshots
  - Join Operations
  - Data Aggregation

## 🎯 Core Technologies

### Delta Lake
- [Delta Lake Fundamentals](topics/delta-lake.md)
  - ACID compliance
  - VACUUM and retention
  - MERGE operations
  - Z-ordering and optimization
  - Time travel and versioning
- [Delta Sink & Iceberg Compatibility](DELTA_SINK_ICEBURG_READ.md)
  - Creating Delta Sinks
  - Disabling Deletion Vectors
  - Enabling Iceberg Compatibility

### Delta Live Tables (DLT)
- [Delta Live Tables](topics/delta-live-tables.md)
  - Pipeline creation and syntax
  - Expectations (EXPECT, DROP)
  - Data quality monitoring
  - Dependent tasks
  - Streaming vs. materialized views

### Unity Catalog
- [Unity Catalog](topics/unity-catalog.md)
  - GRANT permissions
  - USAGE vs. ALL PRIVILEGES
  - Schemas and catalogs
  - PII data tagging
  - External vs. managed tables

## 🔄 Data Processing

### Spark & PySpark
- [Spark Fundamentals](topics/spark-fundamentals.md)
  - DataFrames and transformations
  - Array functions
  - spark.table() vs. spark.sql()
  - JDBC connections
  - Performance optimization

### Streaming
- [Streaming Processing](topics/streaming.md)
  - Trigger configuration
  - processingTime settings
  - Continuous processing
  - Stream vs. batch semantics
  - Watermarks and state management

### Batch Processing
- [Batch Operations](topics/batch-processing.md)
  - MERGE operations
  - Deduplication strategies
- [COPY INTO Reference](COPY%20INTO%20Reference.md)
  - Idempotent file ingestion
  - Format options and mergeSchema
  - Scheduled data loading

## 🏗️ Architecture & Patterns

### Medallion Architecture
- [Medallion Pattern](topics/medallion-architecture.md)
  - Bronze layer (raw ingestion)
  - Silver layer (cleaned, conformed)
  - Gold layer (business-level aggregates)
  - Layer transition best practices

### CDC & SCD
- [Change Data Capture](topics/cdc-scd.md)
  - CDC fundamentals
  - SCD Type 1 (overwrite)
  - SCD Type 2 (historical tracking)
  - AUTO CDC API
  - Snapshot processing
- [CDC & SCD Review](CDC_SCD_REVIEW.md)
  - AUTO CDC Flow Syntax
  - SCD Type 1 vs Type 2
  - SEQUENCE BY and KEYS

## ⚙️ Operations

### Workflows & Jobs
- [Databricks Workflows](topics/workflows.md)
  - Job creation and scheduling
  - Task dependencies
  - Webhooks vs. email alerts
  - Scheduling patterns
  - Preventing execution on specific days

### Cost Optimization
- [Cost Management](topics/cost-optimization.md)
  - Serverless SQL warehouses
  - Auto-stop configuration
  - Cluster pools
  - DBU usage monitoring
  - Spot instances

## 💻 Development & Tools

### Databricks Workspace
- [Workspace Concepts](topics/workspace.md)
  - Control plane vs. data plane
  - Repos vs. notebook versioning
  - Branching strategies
  - Operations outside repos (push, pull, clone)

### Learning Tools
- [Obsidian 사용법](Obsidian_사용법.md)
  - 기본 마크다운 문법
  - 노트 연결과 그래프 뷰
  - 검색 및 태그 활용
  - 학습 워크플로우

## 📖 SQL Syntax Reference

- [CREATE FLOW](CREATE_FLOW_SYNTAX.sql) - Flow creation syntax
- [SET CUSTOM TAG](SET_CUSTOM_TAG_SYNTAX.sql) - Custom tagging syntax
- [STREAMING TABLE](STREAMING_TABLE_SYNTAX.sql) - Streaming table syntax

## 📝 Weekly Study Guides

- [Week 1-2 References](de_wk1_wk2_references.md)
- [Week 3-5 References](de_wk3_wk5_references.md)
- [Week 6-8 References](de_wk6_wk8_references.md)
- [Week 9-10 References](de_wk9_wk10_references.md)

## 🎓 Exam Preparation

- [Exam Strategy](topics/exam-prep.md)
  - High-priority topics
  - Common question patterns
  - Time management
  - Practice exam insights
- [Question Mapping](question-mapping.md)
- [Schema Reference](schema.md)

## 📊 Progress Tracking

**Total README Questions:** 90
**Categorized:** 0
**Answered:** 0
**Pending:** 90

See [log.md](log.md) for detailed progress tracking.

---

## 🗂️ Quick Navigation

### By Topic
- **Data Ingestion**: [COPY INTO](COPY%20INTO%20Reference.md) | [Batch Processing](topics/batch-processing.md) | [Streaming](topics/streaming.md)
- **Data Transformation**: [Spark](topics/spark-fundamentals.md) | [DLT](topics/delta-live-tables.md)
- **Data Architecture**: [Medallion](topics/medallion-architecture.md) | [CDC/SCD](CDC_SCD_REVIEW.md)
- **Data Governance**: [Unity Catalog](topics/unity-catalog.md)
- **Operations**: [Workflows](topics/workflows.md) | [Cost Optimization](topics/cost-optimization.md)

### By Resource Type
- **Concepts**: [Core Concepts](Databricks_Data_Engineering_Concepts.md)
- **Syntax**: [SQL Files](CREATE_FLOW_SYNTAX.sql)
- **Weekly**: [Study Guides](#📝-weekly-study-guides)
- **Practice**: [Exam Prep](topics/exam-prep.md)
