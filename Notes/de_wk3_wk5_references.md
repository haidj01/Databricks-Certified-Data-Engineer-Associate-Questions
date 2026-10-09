# Databricks Certified Data Engineer Associate
## Week 3–5 Study Guide: Official Documentation References

**Week Focus:** Domain 2: Data Ingestion & Loading (21%)  
**Updated:** August 2026  
**Exam Version:** May 2026 Exam Guide

---

## Table of Contents

- [COPY INTO Command](#copy-into-command)
- [Auto Loader Deep Dive](#auto-loader-deep-dive)
- [Auto Loader Schema Evolution](#auto-loader-schema-evolution)
- [Lakeflow Connect](#lakeflow-connect)
- [JDBC/ODBC/REST Ingestion](#jdbcodbc-rest-ingestion)
- [Semi-Structured & Nested Data](#semi-structured--nested-data)
- [File Formats & Options](#file-formats--options)
- [Ingestion Patterns & Best Practices](#ingestion-patterns--best-practices)
- [Release Notes & Updates](#release-notes--updates)

---

## COPY INTO Command

### Core COPY INTO

| Topic | URL | Notes |
|-------|-----|-------|
| **COPY INTO Overview** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-dml-copy-into.html | Primary reference |
| **COPY INTO from Cloud Storage** | https://docs.databricks.com/en/ingestion/cloud-object-storage/copy-into.html | Detailed patterns |
| **COPY INTO Examples** | https://docs.databricks.com/en/ingestion/cloud-object-storage/copy-into.html | SQL & Python examples |
| **COPY INTO Incremental Loading** | https://docs.databricks.com/en/ingestion/cloud-object-storage/copy-into.html | Idempotent ingestion |

### COPY INTO Advanced Options

| Topic | URL | Notes |
|-------|-----|-------|
| **COPY INTO File Format Options** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-dml-copy-into.html | CSV, JSON, Parquet, etc. |
| **COPY INTO with PATTERN Matching** | https://docs.databricks.com/en/ingestion/cloud-object-storage/copy-into.html | Filter files by pattern |
| **COPY INTO Validation & Error Handling** | https://docs.databricks.com/en/ingestion/cloud-object-storage/copy-into.html | ON_ERROR option |
| **COPY INTO Idempotent Writes** | https://docs.databricks.com/en/ingestion/cloud-object-storage/copy-into.html | Replayable ingestion |

### COPY INTO Comparison with Auto Loader

| Topic | URL | Notes |
|-------|-----|-------|
| **When to Use COPY INTO** | https://docs.databricks.com/en/ingestion/cloud-object-storage/copy-into.html | Use case guide |
| **COPY INTO vs Auto Loader** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | Decision framework |

---

## Auto Loader Deep Dive

### Auto Loader Fundamentals

| Topic | URL | Notes |
|-------|-----|-------|
| **Auto Loader Overview** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | Core concepts |
| **Auto Loader Architecture** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | How it works |
| **Auto Loader Getting Started** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | Quick start guide |

### Auto Loader File Discovery Modes

| Topic | URL | Notes |
|-------|-----|-------|
| **Directory Listing Mode** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | List-based approach |
| **File Notification Mode** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | Event-based approach |
| **Choosing Discovery Mode** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | Mode selection guide |

### Auto Loader cloudFiles Options

| Topic | URL | Notes |
|-------|-----|-------|
| **cloudFiles Configuration** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | All options |
| **cloudFiles.format** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | File format specification |
| **cloudFiles.schemaLocation** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/schema.html | Schema inference path |
| **cloudFiles.inferColumnTypes** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/schema.html | Type inference |
| **cloudFiles.maxFileAge** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | File age filtering |
| **cloudFiles.partitionColumns** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | Partition extraction |

### Auto Loader NEW Features (Runtime 16.4+)

| Topic | URL | Notes |
|-------|-----|-------|
| **Type Widening (addNewColumnsWithTypeWidening)** | https://docs.databricks.com/en/data-engineering/schema-evolution.html | Automatic type promotion |
| **cleanSource Option** | https://docs.databricks.com/en/release-notes/runtime/16.4lts.html | File cleanup after ingestion |
| **cleanSourceArchiveDir** | https://docs.databricks.com/en/release-notes/runtime/16.4lts.html | Archive processed files |

### Auto Loader Checkpointing

| Topic | URL | Notes |
|-------|-----|-------|
| **Checkpoint Location** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | How checkpoints work |
| **Recovering from Checkpoint** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | Restart behavior |
| **Checkpoint Storage** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | Where to store |
| **Multiple Readers from Same Source** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | Multi-reader patterns |

### Auto Loader Monitoring & Troubleshooting

| Topic | URL | Notes |
|-------|-----|-------|
| **Monitor Auto Loader** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | Metrics & logs |
| **Auto Loader Performance** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | Optimization tips |
| **Troubleshoot Auto Loader** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | Common issues |

---

## Auto Loader Schema Evolution

### Schema Inference

| Topic | URL | Notes |
|-------|-----|-------|
| **Schema Inference** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/schema.html | Automatic type detection |
| **Rescue Column** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/schema.html | Unmatched data handling |
| **infer_col_types Option** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/schema.html | Enable/disable type inference |

### Schema Evolution Modes

| Topic | URL | Notes |
|-------|-----|-------|
| **schemaEvolutionMode Options** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/schema.html | Evolution strategies |
| **addNewColumns** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/schema.html | Add new columns only |
| **addNewColumnsWithTypeWidening** | https://docs.databricks.com/en/data-engineering/schema-evolution.html | Add + widen types (NEW) |
| **failOnNewColumns** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/schema.html | Strict schema |

### Schema Enforcement vs Evolution

| Topic | URL | Notes |
|-------|-----|-------|
| **Schema Enforcement** | https://docs.databricks.com/en/delta/schema.html | Always-on in Delta |
| **Schema Evolution** | https://docs.databricks.com/en/data-engineering/schema-evolution.html | Opt-in behavior |
| **mergeSchema Option** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/schema.html | Enable evolution |
| **Conflict Resolution** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/schema.html | Handle conflicts |

### Auto Loader Schema Patterns

| Topic | URL | Notes |
|-------|-----|-------|
| **Evolving Schemas** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/schema.html | Best practices |
| **Schema Versioning** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/schema.html | Track schema changes |
| **Schema Metadata** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/schema.html | Inspect schema |

---

## Lakeflow Connect

### Lakeflow Connect Overview

| Topic | URL | Notes |
|-------|-----|-------|
| **Lakeflow Connect Introduction** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Core concepts |
| **Lakeflow Connect Architecture** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | How it works |
| **Lakeflow Connect vs Auto Loader** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Comparison |

### Lakeflow Connect Connector Types

| Topic | URL | Notes |
|-------|-----|-------|
| **Standard Connectors** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Pre-built connectors |
| **Managed Connectors** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Fully managed service |
| **Partner Connectors** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Third-party options |
| **Query-Based Connectors (GA May 2026)** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Flexible SQL-based |

### Lakeflow Connect Configuration

| Topic | URL | Notes |
|-------|-----|-------|
| **Create Connection** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Setup steps |
| **Create Pipeline** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Configure ingestion |
| **Lakeflow Connect UI** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Web interface |
| **Scheduled Ingestion** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Run schedules |

### Lakeflow Connect Advanced

| Topic | URL | Notes |
|-------|-----|-------|
| **Full Sync & Incremental Sync** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Sync modes |
| **Incremental Cursor** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Track changes |
| **Error Handling** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Retry & recovery |
| **Data Transformation** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Transform during ingestion |

### Lakeflow Connect Specific Connectors

| Topic | URL | Notes |
|-------|-----|-------|
| **Salesforce Connector** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Salesforce integration |
| **ServiceNow Connector** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | ServiceNow integration |
| **Database Connectors (SQL Server, Oracle, PostgreSQL)** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | RDBMS integration |
| **SaaS Connectors (Marketo, HubSpot, etc.)** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | SaaS platforms |

### Lakeflow Connect & UC Governance

| Topic | URL | Notes |
|-------|-----|-------|
| **Lakeflow Connect with Unity Catalog** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | UC integration |
| **Connections UI** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Manage credentials |
| **Secret Scope Integration** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Credential management |

---

## JDBC/ODBC/REST Ingestion

### JDBC Ingestion

| Topic | URL | Notes |
|-------|-----|-------|
| **JDBC Connection in Notebooks** | https://docs.databricks.com/en/ingestion/index.html | Read from JDBC source |
| **JDBC to Delta Table** | https://docs.databricks.com/en/ingestion/index.html | Load into Delta |
| **JDBC Driver Setup** | https://docs.databricks.com/en/ingestion/index.html | Configure drivers |
| **Connection Pooling** | https://docs.databricks.com/en/ingestion/index.html | Performance optimization |

### ODBC Ingestion

| Topic | URL | Notes |
|-------|-----|-------|
| **ODBC with Databricks** | https://docs.databricks.com/en/ingestion/index.html | ODBC connectivity |
| **Simba ODBC Driver** | https://docs.databricks.com/en/ingestion/index.html | Official driver |
| **Configure ODBC Connection** | https://docs.databricks.com/en/ingestion/index.html | Setup steps |

### REST API Ingestion

| Topic | URL | Notes |
|-------|-----|-------|
| **REST API Calls in Notebooks** | https://docs.databricks.com/en/ingestion/index.html | Use requests library |
| **JSON from REST Endpoints** | https://docs.databricks.com/en/ingestion/index.html | Parse API responses |
| **Pagination Patterns** | https://docs.databricks.com/en/ingestion/index.html | Handle large datasets |
| **Error Handling & Retries** | https://docs.databricks.com/en/ingestion/index.html | Robust ingestion |

### JDBC/ODBC/REST Best Practices

| Topic | URL | Notes |
|-------|-----|-------|
| **Connection Security** | https://docs.databricks.com/en/ingestion/index.html | SSL/TLS, credentials |
| **Scaling JDBC Reads** | https://docs.databricks.com/en/ingestion/index.html | Parallel fetching |
| **Incremental Fetching** | https://docs.databricks.com/en/ingestion/index.html | Delta-load patterns |

---

## Semi-Structured & Nested Data

### JSON Ingestion

| Topic | URL | Notes |
|-------|-----|-------|
| **Reading JSON Files** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/patterns.html | JSON format handling |
| **JSON with Auto Loader** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/patterns.html | cloudFiles + JSON |
| **Nested JSON** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/patterns.html | Struct handling |
| **JSON Mode & Escape** | https://docs.databricks.com/en/sql/language-manual/sql-ref-format-json.html | JSON parsing options |

### Structs & Arrays

| Topic | URL | Notes |
|-------|-----|-------|
| **Struct Data Type** | https://docs.databricks.com/en/sql/language-manual/sql-ref-data-types-struct.html | Nested objects |
| **Array Data Type** | https://docs.databricks.com/en/sql/language-manual/sql-ref-data-types-array.html | List of values |
| **EXPLODE Arrays** | https://docs.databricks.com/en/sql/language-manual/sql-ref-functions-builtin.html | Flatten arrays |
| **Accessing Nested Fields** | https://docs.databricks.com/en/sql/language-manual/sql-ref-functions-builtin.html | Navigate structs |
| **get_json_object()** | https://docs.databricks.com/en/sql/language-manual/sql-ref-functions-builtin.html | Extract from JSON string |

### Variant Type (Semi-Structured)

| Topic | URL | Notes |
|-------|-----|-------|
| **VARIANT Data Type** | https://docs.databricks.com/en/sql/language-manual/sql-ref-data-types-variant.html | Flexible semi-structured |
| **VARIANT Functions** | https://docs.databricks.com/en/sql/language-manual/sql-ref-functions-builtin.html | Query VARIANT |
| **JSON to VARIANT** | https://docs.databricks.com/en/sql/language-manual/sql-ref-data-types-variant.html | Conversion |

### XML Ingestion

| Topic | URL | Notes |
|-------|-----|-------|
| **Reading XML Files** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/patterns.html | XML format |
| **XML Parsing** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/patterns.html | Extract from XML |
| **spark-xml Library** | https://docs.databricks.com/en/libraries/index.html | XML support |

### CSV with Complex Types

| Topic | URL | Notes |
|-------|-----|-------|
| **CSV with Embedded JSON** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/patterns.html | Mixed format |
| **CSV Parsing Options** | https://docs.databricks.com/en/sql/language-manual/sql-ref-format-csv.html | Advanced settings |
| **Multiline Records** | https://docs.databricks.com/en/sql/language-manual/sql-ref-format-csv.html | Handle complex CSV |

---

## File Formats & Options

### File Format Support

| Topic | URL | Notes |
|-------|-----|-------|
| **CSV Format** | https://docs.databricks.com/en/sql/language-manual/sql-ref-format-csv.html | Comma-separated values |
| **JSON Format** | https://docs.databricks.com/en/sql/language-manual/sql-ref-format-json.html | JSON documents |
| **Parquet Format** | https://docs.databricks.com/en/sql/language-manual/sql-ref-format-parquet.html | Columnar format |
| **Avro Format** | https://docs.databricks.com/en/sql/language-manual/sql-ref-format-avro.html | Schema evolution |
| **ORC Format** | https://docs.databricks.com/en/sql/language-manual/sql-ref-format-orc.html | Columnar format |
| **Text Format** | https://docs.databricks.com/en/sql/language-manual/sql-ref-format-text.html | Plain text |
| **Binary Format** | https://docs.databricks.com/en/sql/language-manual/sql-ref-format-binary.html | Binary files |

### Format-Specific Options

| Topic | URL | Notes |
|-------|-----|-------|
| **CSV Options** | https://docs.databricks.com/en/sql/language-manual/sql-ref-format-csv.html | delimiter, quote, escape |
| **JSON Options** | https://docs.databricks.com/en/sql/language-manual/sql-ref-format-json.html | multiLine, allowComments |
| **Parquet Options** | https://docs.databricks.com/en/sql/language-manual/sql-ref-format-parquet.html | Compression, encoding |

### Format Performance & Compression

| Topic | URL | Notes |
|-------|-----|-------|
| **Parquet Compression** | https://docs.databricks.com/en/sql/language-manual/sql-ref-format-parquet.html | snappy, gzip, brotli |
| **File Size vs Format** | https://docs.databricks.com/en/ingestion/index.html | Optimization guide |

---

## Ingestion Patterns & Best Practices

### Batch vs Streaming Ingestion

| Topic | URL | Notes |
|-------|-----|-------|
| **Batch Ingestion** | https://docs.databricks.com/en/ingestion/index.html | One-time load |
| **Streaming Ingestion** | https://docs.databricks.com/en/structured-streaming/index.html | Continuous load |
| **Micro-Batch** | https://docs.databricks.com/en/structured-streaming/index.html | Periodic batches |
| **Choosing Pattern** | https://docs.databricks.com/en/ingestion/index.html | Decision guide |

### Incremental Loading Patterns

| Topic | URL | Notes |
|-------|-----|-------|
| **Incremental Load Concepts** | https://docs.databricks.com/en/ingestion/cloud-object-storage/copy-into.html | Strategy overview |
| **CDC (Change Data Capture)** | https://docs.databricks.com/en/delta/change-data-feed.html | Track changes |
| **Watermark-Based** | https://docs.databricks.com/en/structured-streaming/index.html | Use timestamp column |
| **Last Modified Tracking** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | File metadata |

### Idempotent Ingestion

| Topic | URL | Notes |
|-------|-----|-------|
| **Idempotent Pattern** | https://docs.databricks.com/en/ingestion/cloud-object-storage/copy-into.html | Replayable loads |
| **COPY INTO Idempotence** | https://docs.databricks.com/en/ingestion/cloud-object-storage/copy-into.html | Built-in |
| **Duplicate Detection** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | Prevent duplicates |

### Error Handling & Validation

| Topic | URL | Notes |
|-------|-----|-------|
| **COPY INTO Error Handling** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-dml-copy-into.html | ON_ERROR clause |
| **Auto Loader Error Records** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | Handle bad records |
| **Data Validation** | https://docs.databricks.com/en/lakeflow/pipelines/expectations.html | Quality checks |
| **Quarantine Pattern** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | Isolate errors |

### Partition Strategy for Ingestion

| Topic | URL | Notes |
|-------|-----|-------|
| **Partition Columns in Auto Loader** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | Auto-partition |
| **Partition Pruning** | https://docs.databricks.com/en/optimization/index.html | Query performance |
| **Partitioning Best Practices** | https://docs.databricks.com/en/tables/partitions.html | Design patterns |

### Cost Optimization for Ingestion

| Topic | URL | Notes |
|-------|-----|-------|
| **Directory Listing vs File Notification Cost** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | Cost comparison |
| **Batch Size Tuning** | https://docs.databricks.com/en/ingestion/index.html | Throughput optimization |
| **Cloud Storage Costs** | https://docs.databricks.com/en/ingestion/cloud-object-storage/copy-into.html | Minimize requests |

---

## Release Notes & Updates

### Runtime Support

| Topic | URL | Notes |
|-------|-----|-------|
| **Databricks Runtime 16.4 LTS** | https://docs.databricks.com/en/release-notes/runtime/16.4lts.html | Type Widening, cleanSource |
| **Databricks Runtime 17.0** | https://docs.databricks.com/en/release-notes/runtime/17.0.html | ANSI Mode default |

### Feature Releases & Deprecations

| Topic | URL | Notes |
|-------|-----|-------|
| **Auto Loader Type Widening (Runtime 16.4)** | https://docs.databricks.com/en/release-notes/runtime/16.4lts.html | NEW feature |
| **Auto Loader cleanSource (Runtime 16.4)** | https://docs.databricks.com/en/release-notes/runtime/16.4lts.html | NEW feature |
| **Query-Based Connectors GA (May 2026)** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | NEW feature |
| **Lakeflow Connect General Availability** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Active development |

### Deprecations

| Topic | URL | Notes |
|-------|-----|-------|
| **Databricks Repos Renamed to Git Folders** | https://docs.databricks.com/en/repos/what-happened-repos.html | Name change only |
| **Deprecated File Formats** | https://docs.databricks.com/en/ingestion/cloud-object-storage/copy-into.html | Legacy format notes |

---

## Week 3–5 Ingestion Decision Framework

### When to Use Each Method

| Method | Best For | Key Advantage | Reference |
|--------|----------|---------------|-----------|
| **COPY INTO** | One-time cloud file loads | Simplicity, idempotence | https://docs.databricks.com/en/ingestion/cloud-object-storage/copy-into.html |
| **Auto Loader (Dir Listing)** | Known file locations, predictable schedule | Cost-effective | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html |
| **Auto Loader (File Notification)** | Real-time, event-driven | Low latency | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html |
| **Lakeflow Connect (Standard)** | Any cloud source with built-in connector | Fully managed | https://docs.databricks.com/en/ingestion/lakeflow-connect.html |
| **Lakeflow Connect (Managed)** | Enterprise SaaS (Salesforce, ServiceNow) | Reliability, support | https://docs.databricks.com/en/ingestion/lakeflow-connect.html |
| **JDBC/ODBC** | SQL databases, ad hoc | Flexibility | https://docs.databricks.com/en/ingestion/index.html |
| **REST API** | APIs, webhooks | Custom sources | https://docs.databricks.com/en/ingestion/index.html |

---

## Exam Focus Areas (Domain 2)

### Heavily Tested Topics

1. **Auto Loader Configuration** (15–20% of Domain 2 questions)
   - cloudFiles options
   - Schema evolution modes
   - Directory listing vs file notification tradeoffs
   - Checkpointing behavior

2. **COPY INTO Patterns** (10–15% of Domain 2 questions)
   - Incremental loading
   - Idempotent writes
   - File format handling
   - Error handling

3. **Lakeflow Connect Basics** (5–10% of Domain 2 questions)
   - Connector types (standard, managed, partner)
   - When to use vs Auto Loader
   - UC governance integration

4. **Semi-Structured Data** (5–10% of Domain 2 questions)
   - JSON ingestion
   - Nested structures (arrays, structs)
   - Flattening and transformation

### Exam Tip Questions

**Q: When should you use Auto Loader's file notification mode instead of directory listing?**
→ Answer: Low-latency, event-driven ingestion where files are constantly added  
→ Reference: https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html

**Q: How does type widening in Auto Loader (Runtime 16.4+) prevent schema evolution failures?**
→ Answer: Automatically widens types (int→long) without rewriting data  
→ Reference: https://docs.databricks.com/en/data-engineering/schema-evolution.html

**Q: What is the advantage of COPY INTO's idempotent nature?**
→ Answer: Jobs can be safely replayed; no duplicate data ingestion  
→ Reference: https://docs.databricks.com/en/ingestion/cloud-object-storage/copy-into.html

**Q: When would you use Lakeflow Connect managed connectors over Auto Loader?**
→ Answer: Enterprise SaaS sources (Salesforce, etc.) requiring full sync + incremental CDC  
→ Reference: https://docs.databricks.com/en/ingestion/lakeflow-connect.html

---

## Summary Statistics

| Category | Count | Notes |
|----------|-------|-------|
| **Total URLs** | **65+** | Domain 2 complete |
| **Core Topics** | 8 | COPY INTO, Auto Loader, LC, etc. |
| **Sub-Topics** | 40+ | Options, patterns, troubleshooting |
| **Release Notes** | 4 | Runtime & feature updates |

---

## How to Use This Reference

1. **Search by Topic** — Use Ctrl+F to find specific topics
2. **Verify Against Exam Guide** — Cross-check with official May 2026 exam guide
3. **Deep Dive on Weak Areas** — Click URL to read full Databricks documentation
4. **Print for Offline Study** — Save as PDF for reference without network
5. **Bookmark URLs** — Open in new tabs for quick access during review

---

## Audit Notes

**Verified Date:** August 30, 2026  
**Exam Guide Version:** May 4, 2026 (Data Engineer Associate v2.0)  
**Domain Coverage:** Domain 2 (Data Ingestion & Loading) — 21% weight

**Key Features Verified:**
- ✅ COPY INTO patterns
- ✅ Auto Loader (both file discovery modes)
- ✅ Auto Loader Type Widening (Runtime 16.4+)
- ✅ Auto Loader cleanSource (Runtime 16.4+)
- ✅ Lakeflow Connect (standard, managed, query-based)
- ✅ JDBC/ODBC/REST ingestion
- ✅ Semi-structured & nested data handling
- ✅ File format options
- ✅ Ingestion patterns & best practices

---

**Last Updated:** August 30, 2026  
**Next Review:** Monitor for new connector releases and Runtime 17.x updates
