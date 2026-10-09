# Databricks Certified Data Engineer Associate
## Week 1–2 Study Guide: Official Documentation References

**Updated:** August 2026  
**Guide Version:** May 2026 Exam Guide  
**Audit Status:** All links verified as of August 30, 2026

---

## Domain 1: Databricks Intelligence Platform (6%)

### Lakehouse Architecture & Delta Lake

| Topic | URL | Version |
|-------|-----|---------|
| **What is Delta Lake?** | https://docs.databricks.com/en/delta/index.html | Latest |
| **Delta Lake ACID Properties** | https://docs.databricks.com/en/delta/index.html | Latest |
| **Delta Lake Transaction Log** | https://docs.databricks.com/en/delta/delta-log.html | Latest |
| **Time Travel (Version History)** | https://docs.databricks.com/en/delta/time-travel.html | Latest |
| **DESCRIBE HISTORY** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-aux-describe-history.html | Latest |
| **RESTORE TABLE** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-auxiliary-restore.html | Latest |
| **VACUUM** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-utility-vacuum.html | Latest |
| **OPTIMIZE & Z-ORDER** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-utility-optimize.html | Latest |

### Delta Lake DML & Schema

| Topic | URL | Version |
|-------|-----|---------|
| **INSERT, UPDATE, DELETE** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-dml.html | Latest |
| **MERGE INTO** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-dml-merge.html | Latest |
| **Schema Enforcement** | https://docs.databricks.com/en/delta/schema.html | Latest |
| **Schema Evolution** | https://docs.databricks.com/en/data-engineering/schema-evolution.html | Latest |
| **mergeSchema Option** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/schema.html | Latest |

### Liquid Clustering (NEW 2025)

| Topic | URL | Version |
|-------|-----|---------|
| **Liquid Clustering Overview** | https://docs.databricks.com/en/tables/clustering.html | Latest |
| **CLUSTER BY Clause** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-ddl-cluster-by.html | Latest |
| **Automatic Liquid Clustering (June 2025)** | https://docs.databricks.com/en/tables/clustering.html#automatic-liquid-clustering | Latest (GA June 2025) |
| **When to Partition Tables** | https://docs.databricks.com/en/tables/partitions.html | Latest |

### Databricks Workspace & Runtime

| Topic | URL | Version |
|-------|-----|---------|
| **Workspace Overview** | https://docs.databricks.com/en/workspace/index.html | Latest |
| **Notebooks** | https://docs.databricks.com/en/notebooks/index.html | Latest |
| **Databricks Runtime (DBR)** | https://docs.databricks.com/en/runtime/index.html | Latest |
| **DBR ML & Genomics** | https://docs.databricks.com/en/runtime/index.html | Latest |
| **Photon Runtime** | https://docs.databricks.com/en/runtime/photon.html | Latest |

### DBFS vs Unity Catalog Volumes

| Topic | URL | Version |
|-------|-----|---------|
| **DBFS (Legacy)** | https://docs.databricks.com/en/dbfs/index.html | Latest |
| **Unity Catalog Volumes** | https://docs.databricks.com/en/unity-catalog/volumes.html | Latest |
| **What Happened to Databricks Repos?** | https://docs.databricks.com/en/repos/what-happened-repos.html | Latest |

---

## Domain 1 (cont.): Unity Catalog & Access Control

### Unity Catalog Architecture

| Topic | URL | Version |
|-------|-----|---------|
| **Unity Catalog Overview** | https://docs.databricks.com/en/unity-catalog/index.html | Latest |
| **3-Level Namespace** | https://docs.databricks.com/en/unity-catalog/index.html | Latest |
| **Metastore, Catalog, Schema** | https://docs.databricks.com/en/unity-catalog/create-catalogs.html | Latest |
| **Privilege Hierarchy** | https://docs.databricks.com/en/unity-catalog/manage-privileges/privileges.html | Latest |

### Managed vs External Tables

| Topic | URL | Version |
|-------|-----|---------|
| **Managed Tables** | https://docs.databricks.com/en/unity-catalog/create-tables.html#managed-table | Latest |
| **External Tables** | https://docs.databricks.com/en/unity-catalog/create-tables.html#external-table | Latest |
| **Managed vs External** | https://docs.databricks.com/en/unity-catalog/create-tables.html | Latest |

### Access Control (GRANT/REVOKE/DENY)

| Topic | URL | Version |
|-------|-----|---------|
| **GRANT Privileges** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-dcl-grant.html | Latest |
| **REVOKE Privileges** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-dcl-revoke.html | Latest |
| **DENY Statement** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-dcl-deny.html | Latest |
| **Privilege Levels** | https://docs.databricks.com/en/unity-catalog/manage-privileges/privileges.html | Latest |

### Data Lineage & Governance

| Topic | URL | Version |
|-------|-----|---------|
| **Column-Level Lineage** | https://docs.databricks.com/en/unity-catalog/data-lineage.html | Latest |
| **Table Lineage** | https://docs.databricks.com/en/unity-catalog/data-lineage.html | Latest |
| **Data Lineage in UC** | https://docs.databricks.com/en/unity-catalog/data-lineage.html | Latest |

### Advanced UC Security

| Topic | URL | Version |
|-------|-----|---------|
| **Column Masking** | https://docs.databricks.com/en/security/column-masking.html | Latest |
| **Row-Level Security (Row Filters)** | https://docs.databricks.com/en/security/row-filter.html | Latest |
| **ABAC (Attribute-Based Access Control)** | https://docs.databricks.com/en/unity-catalog/attribute-controls.html | Latest |

---

## Domain 1 (cont.): Compute Services

### Cluster Types

| Topic | URL | Version |
|-------|-----|---------|
| **All-Purpose Clusters** | https://docs.databricks.com/en/compute/configure.html | Latest |
| **Job Clusters** | https://docs.databricks.com/en/compute/job-clusters.html | Latest |
| **Single-Node Clusters** | https://docs.databricks.com/en/compute/single-node.html | Latest |
| **Instance Pools** | https://docs.databricks.com/en/compute/instance-pools/index.html | Latest |
| **Autoscaling** | https://docs.databricks.com/en/compute/autoscaling.html | Latest |

### SQL Warehouses

| Topic | URL | Version |
|-------|-----|---------|
| **SQL Warehouse Types** | https://docs.databricks.com/en/compute/sql-warehouse/warehouse-types.html | Latest |
| **Classic SQL Warehouse** | https://docs.databricks.com/en/compute/sql-warehouse/warehouse-types.html#classic-sql-warehouse | Latest |
| **Pro SQL Warehouse** | https://docs.databricks.com/en/compute/sql-warehouse/warehouse-types.html#pro-sql-warehouse | Latest |
| **Serverless SQL Warehouse** | https://docs.databricks.com/en/compute/sql-warehouse/warehouse-types.html#serverless-sql-warehouse | Latest |
| **Warehouse Configuration** | https://docs.databricks.com/en/sql/admin/create-sql-warehouse.html | Latest |

### Serverless Compute (NEW 2025–2026)

| Topic | URL | Version |
|-------|-----|---------|
| **Serverless Compute** | https://docs.databricks.com/en/compute/serverless.html | Latest |
| **Serverless SQL Warehouse** | https://docs.databricks.com/en/compute/sql-warehouse/warehouse-types.html#serverless-sql-warehouse | Latest |
| **Serverless Jobs** | https://docs.databricks.com/en/jobs/run-serverless-jobs.html | Latest (2026) |
| **Serverless Notebooks** | https://docs.databricks.com/en/compute/serverless.html | Latest |

### DBU & Cost Models

| Topic | URL | Version |
|-------|-----|---------|
| **Databricks Units (DBU) Pricing** | https://databricks.com/product/pricing | Latest |
| **Cost Optimization** | https://docs.databricks.com/en/admin/index.html | Latest |

---

## Domain 1 (cont.): Advanced Features

### Predictive Optimization

| Topic | URL | Version |
|-------|-----|---------|
| **Predictive Optimization** | https://docs.databricks.com/en/optimizations/predictive-optimization.html | Latest |
| **Auto-Optimization** | https://docs.databricks.com/en/delta/table-properties.html | Latest |

### Data Skipping & Statistics

| Topic | URL | Version |
|-------|-----|---------|
| **Data Skipping** | https://docs.databricks.com/en/optimizations/data-skipping.html | Latest |
| **ANALYZE TABLE STATISTICS** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-aux-analyze-table.html | Latest |

### CLONE & Change Data Feed

| Topic | URL | Version |
|-------|-----|---------|
| **CLONE (Deep & Shallow)** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-dml-clone.html | Latest |
| **Change Data Feed (CDF)** | https://docs.databricks.com/en/delta/change-data-feed.html | Latest |

---

## Domain 2: Data Ingestion & Loading (21%)

### COPY INTO

| Topic | URL | Version |
|-------|-----|---------|
| **COPY INTO** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-dml-copy-into.html | Latest |
| **COPY INTO from Cloud Storage** | https://docs.databricks.com/en/ingestion/cloud-object-storage/copy-into.html | Latest |
| **Incremental Loading** | https://docs.databricks.com/en/ingestion/cloud-object-storage/copy-into.html | Latest |

### Auto Loader

| Topic | URL | Version |
|-------|-----|---------|
| **Auto Loader Overview** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | Latest |
| **Auto Loader Configuration** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | Latest |
| **Directory Listing vs File Notification** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | Latest |
| **Checkpointing** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/index.html | Latest |

### Auto Loader Schema Evolution

| Topic | URL | Version |
|-------|-----|---------|
| **Schema Inference & Evolution** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/schema.html | Latest |
| **cloudFiles.schemaEvolutionMode** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/schema.html | Latest |
| **Schema Evolution Modes** | https://docs.databricks.com/en/data-engineering/schema-evolution.html | Latest |
| **Rescued Data Column** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/schema.html | Latest |

### Auto Loader NEW Features (Runtime 16.4+)

| Topic | URL | Version |
|-------|-----|---------|
| **Type Widening (addNewColumnsWithTypeWidening)** | https://docs.databricks.com/en/release-notes/runtime/16.4lts.html | Runtime 16.4 LTS |
| **cloudFiles.cleanSource** | https://docs.databricks.com/en/release-notes/runtime/16.4lts.html | Runtime 16.4 LTS |
| **Schema Evolution in Databricks** | https://docs.databricks.com/en/data-engineering/schema-evolution.html | Latest |

### Lakeflow Connect

| Topic | URL | Version |
|-------|-----|---------|
| **Lakeflow Connect Overview** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Latest |
| **Standard Connectors** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Latest |
| **Managed Connectors** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Latest |
| **Query-Based Connectors (GA May 2026)** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Latest (GA May 2026) |
| **Connector Types & Selection** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Latest |

### Semi-Structured & Nested Data

| Topic | URL | Version |
|-------|-----|---------|
| **JSON Ingestion** | https://docs.databricks.com/en/ingestion/cloud-object-storage/auto-loader/patterns.html | Latest |
| **Nested Data (Structs, Arrays)** | https://docs.databricks.com/en/sql/language-manual/sql-ref-functions-builtin.html | Latest |
| **Variant Type (Semi-Structured)** | https://docs.databricks.com/en/sql/language-manual/sql-ref-data-types-variant.html | Latest |

### JDBC/ODBC & REST

| Topic | URL | Version |
|-------|-----|---------|
| **JDBC/ODBC Ingestion** | https://docs.databricks.com/en/ingestion/index.html | Latest |
| **REST API Ingestion** | https://docs.databricks.com/en/ingestion/index.html | Latest |

---

## Domain 3: Data Transformation & Modeling (22%)

### Bronze–Silver–Gold Pattern

| Topic | URL | Version |
|-------|-----|---------|
| **Medallion Architecture** | https://docs.databricks.com/en/lakehouse/index.html | Latest |
| **Bronze Layer (Raw Data)** | https://docs.databricks.com/en/lakehouse/index.html | Latest |
| **Silver Layer (Cleaned)** | https://docs.databricks.com/en/lakehouse/index.html | Latest |
| **Gold Layer (Analytics)** | https://docs.databricks.com/en/lakehouse/index.html | Latest |

### PySpark & SQL ETL

| Topic | URL | Version |
|-------|-----|---------|
| **DataFrame API** | https://docs.databricks.com/en/pyspark/index.html | Latest |
| **Spark SQL** | https://docs.databricks.com/en/sql/index.html | Latest |

### Join Operations

| Topic | URL | Version |
|-------|-----|---------|
| **INNER JOIN** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-dml-select-join.html | Latest |
| **LEFT JOIN** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-dml-select-join.html | Latest |
| **BROADCAST JOIN** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-dml-select-join.html | Latest |
| **CROSS JOIN** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-dml-select-join.html | Latest |
| **UNION / UNION ALL** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-dml-select-set-ops.html | Latest |

### Aggregations & Deduplication

| Topic | URL | Version |
|-------|-----|---------|
| **COUNT, SUM, AVG, MIN, MAX** | https://docs.databricks.com/en/sql/language-manual/sql-ref-functions-builtin.html | Latest |
| **APPROX_COUNT_DISTINCT** | https://docs.databricks.com/en/sql/language-manual/sql-ref-functions-builtin.html | Latest |
| **GROUP BY / HAVING** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-dml-select.html | Latest |
| **ROW_NUMBER / RANK / DENSE_RANK** | https://docs.databricks.com/en/sql/language-manual/sql-ref-functions-builtin.html | Latest |
| **Deduplication Patterns** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-dml-select.html | Latest |

### Array Operations

| Topic | URL | Version |
|-------|-----|---------|
| **EXPLODE** | https://docs.databricks.com/en/sql/language-manual/sql-ref-functions-builtin.html | Latest |
| **FLATTEN** | https://docs.databricks.com/en/sql/language-manual/sql-ref-functions-builtin.html | Latest |
| **Array Operations** | https://docs.databricks.com/en/sql/language-manual/sql-ref-functions-builtin.html | Latest |

### Spark Tuning Parameters

| Topic | URL | Version |
|-------|-----|---------|
| **spark.sql.shuffle.partitions** | https://docs.databricks.com/en/sql/conf.html | Latest |
| **spark.default.parallelism** | https://docs.databricks.com/en/sql/conf.html | Latest |
| **spark.sql.autoBroadcastJoinThreshold** | https://docs.databricks.com/en/sql/conf.html | Latest |
| **Executor & Driver Memory** | https://docs.databricks.com/en/compute/configure.html | Latest |

### Gold Layer Objects

| Topic | URL | Version |
|-------|-----|---------|
| **Views** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-ddl-create-view.html | Latest |
| **Materialized Views** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-ddl-create-materialized-view.html | Latest |
| **Streaming Tables** | https://docs.databricks.com/en/lakeflow/pipelines/streaming-tables.html | Latest |
| **Tables vs Views** | https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-ddl-create-view.html | Latest |

### Data Quality & Validation

| Topic | URL | Version |
|-------|-----|---------|
| **Expectations in DLT** | https://docs.databricks.com/en/lakeflow/pipelines/expectations.html | Latest |
| **Data Quality Checks** | https://docs.databricks.com/en/lakeflow/pipelines/expectations.html | Latest |

---

## Domain 4: Working with Lakeflow Jobs (16%)

### Lakeflow Jobs Overview

| Topic | URL | Version |
|-------|-----|---------|
| **Lakeflow Jobs** | https://docs.databricks.com/en/jobs/index.html | Latest |
| **Lakeflow Jobs (formerly Workflows)** | https://docs.databricks.com/en/jobs/index.html | Latest |
| **Job Creation** | https://docs.databricks.com/en/jobs/jobs-quickstart.html | Latest |
| **Jobs UI** | https://docs.databricks.com/en/jobs/index.html | Latest |

### Task Types

| Topic | URL | Version |
|-------|-----|---------|
| **Notebook Task** | https://docs.databricks.com/en/jobs/task-types.html | Latest |
| **SQL Task** | https://docs.databricks.com/en/jobs/task-types.html | Latest |
| **Python Task** | https://docs.databricks.com/en/jobs/task-types.html | Latest |
| **JAR Task** | https://docs.databricks.com/en/jobs/task-types.html | Latest |
| **Python Wheel Task** | https://docs.databricks.com/en/jobs/task-types.html | Latest |
| **Pipeline Task (Lakeflow Spark Declarative Pipelines)** | https://docs.databricks.com/en/jobs/task-types.html | Latest |
| **Dashboard Task** | https://docs.databricks.com/en/jobs/task-types.html | Latest |
| **dbt Task** | https://docs.databricks.com/en/jobs/task-types.html | Latest |
| **AI Runtime Task (NEW)** | https://docs.databricks.com/en/jobs/task-types.html | Latest |
| **SQL Alert Task (NEW)** | https://docs.databricks.com/en/release-notes/dev-tools/bundles.html | Latest |

### DAG & Dependencies

| Topic | URL | Version |
|-------|-----|---------|
| **DAG (Directed Acyclic Graph)** | https://docs.databricks.com/en/jobs/index.html | Latest |
| **Task Dependencies** | https://docs.databricks.com/en/jobs/task-dependencies.html | Latest |
| **Serial vs Parallel Execution** | https://docs.databricks.com/en/jobs/task-dependencies.html | Latest |

### Control Flow

| Topic | URL | Version |
|-------|-----|---------|
| **Retries** | https://docs.databricks.com/en/jobs/control-flow.html | Latest |
| **Conditional Tasks (if/else)** | https://docs.databricks.com/en/jobs/control-flow.html | Latest |
| **Branching & Looping** | https://docs.databricks.com/en/jobs/control-flow.html | Latest |
| **For Each Task** | https://docs.databricks.com/en/jobs/control-flow.html | Latest |
| **Run If Conditions** | https://docs.databricks.com/en/jobs/control-flow.html | Latest |

### Triggers & Scheduling

| Topic | URL | Version |
|-------|-----|---------|
| **Scheduled Triggers** | https://docs.databricks.com/en/jobs/schedule-jobs.html | Latest |
| **File Arrival Trigger** | https://docs.databricks.com/en/jobs/schedule-jobs.html | Latest |
| **Table Update Trigger** | https://docs.databricks.com/en/jobs/schedule-jobs.html | Latest |
| **Cron Syntax** | https://docs.databricks.com/en/jobs/schedule-jobs.html | Latest |
| **Time-Based vs Data-Driven Triggers** | https://docs.databricks.com/en/jobs/schedule-jobs.html | Latest |

### Job Monitoring & Runs

| Topic | URL | Version |
|-------|-----|---------|
| **Monitor Lakeflow Jobs** | https://docs.databricks.com/en/jobs/monitor.html | Latest |
| **Job Run History** | https://docs.databricks.com/en/jobs/monitor.html | Latest |
| **Spark UI for Jobs** | https://docs.databricks.com/en/jobs/monitor.html | Latest |
| **Jobs System Tables** | https://docs.databricks.com/en/admin/system-tables/jobs.html | Latest |

### Serverless Jobs (NEW 2026)

| Topic | URL | Version |
|-------|-----|---------|
| **Serverless Jobs** | https://docs.databricks.com/en/jobs/run-serverless-jobs.html | Latest (2026) |
| **Serverless Compute for Jobs** | https://docs.databricks.com/en/jobs/run-serverless-jobs.html | Latest (2026) |

---

## Domain 5: Implementing CI/CD (10%)

### Databricks Git Folders

| Topic | URL | Version |
|-------|-----|---------|
| **Git Folders** | https://docs.databricks.com/en/repos/index.html | Latest |
| **Git Folders (formerly Repos)** | https://docs.databricks.com/en/repos/what-happened-repos.html | Latest |
| **Create Git Folder** | https://docs.databricks.com/en/repos/create-repo.html | Latest |
| **Collaborate with Git Folders** | https://docs.databricks.com/en/repos/git-operations.html | Latest |
| **Branches, Commits, Push/Pull** | https://docs.databricks.com/en/repos/git-operations.html | Latest |
| **Pull Requests** | https://docs.databricks.com/en/repos/git-operations.html | Latest |

### CI/CD with Git Folders

| Topic | URL | Version |
|-------|-----|---------|
| **CI/CD with Git Folders** | https://docs.databricks.com/en/repos/ci-cd.html | Latest |
| **Production Git Folder** | https://docs.databricks.com/en/repos/ci-cd.html | Latest |
| **Environment Promotion** | https://docs.databricks.com/en/repos/ci-cd.html | Latest |

### Declarative Automation Bundles (DABs)

| Topic | URL | Version |
|-------|-----|---------|
| **Declarative Automation Bundles** | https://docs.databricks.com/en/dev-tools/bundles/index.html | Latest |
| **Formerly Databricks Asset Bundles** | https://docs.databricks.com/en/dev-tools/bundles/index.html | Latest (renamed March 2026) |
| **Bundle Configuration** | https://docs.databricks.com/en/dev-tools/bundles/config.html | Latest |
| **Bundle Resources** | https://docs.databricks.com/en/dev-tools/bundles/resources.html | Latest |
| **Deploy Bundles** | https://docs.databricks.com/en/dev-tools/bundles/deploy.html | Latest |

### Bundle Environment & Variables

| Topic | URL | Version |
|-------|-----|---------|
| **Environment-Specific Configuration** | https://docs.databricks.com/en/dev-tools/bundles/config.html | Latest |
| **Variables & Overrides** | https://docs.databricks.com/en/dev-tools/bundles/config.html | Latest |
| **Environment Promotion (dev/test/prod)** | https://docs.databricks.com/en/dev-tools/bundles/deploy.html | Latest |

### Databricks CLI

| Topic | URL | Version |
|-------|-----|---------|
| **Databricks CLI** | https://docs.databricks.com/en/dev-tools/cli/index.html | Latest |
| **CLI Setup** | https://docs.databricks.com/en/dev-tools/cli/index.html | Latest |
| **Bundle Validate** | https://docs.databricks.com/en/dev-tools/cli/index.html | Latest |
| **Bundle Deploy** | https://docs.databricks.com/en/dev-tools/cli/index.html | Latest |
| **Databricks CLI Reference** | https://docs.databricks.com/en/dev-tools/cli/index.html | Latest |

### Bundle Tutorials

| Topic | URL | Version |
|-------|-----|---------|
| **Develop a Job with DABs** | https://docs.databricks.com/en/dev-tools/bundles/tutorials.html | Latest |
| **Develop Pipelines with DABs** | https://docs.databricks.com/en/dev-tools/bundles/tutorials.html | Latest |
| **Bundle Examples** | https://docs.databricks.com/en/dev-tools/bundles/tutorials.html | Latest |

---

## Domain 6: Troubleshooting, Monitoring & Optimization (10%)

### Lakeflow Jobs Monitoring

| Topic | URL | Version |
|-------|-----|---------|
| **Monitor Lakeflow Jobs** | https://docs.databricks.com/en/jobs/monitor.html | Latest |
| **Run History & Metrics** | https://docs.databricks.com/en/jobs/monitor.html | Latest |
| **Compare Execution Times** | https://docs.databricks.com/en/jobs/monitor.html | Latest |
| **Pipeline Health** | https://docs.databricks.com/en/jobs/monitor.html | Latest |
| **DAG Visualization** | https://docs.databricks.com/en/jobs/monitor.html | Latest |

### Spark UI & Performance

| Topic | URL | Version |
|-------|-----|---------|
| **Spark UI** | https://docs.databricks.com/en/clusters/monitor/spark-ui.html | Latest |
| **Stage Metrics** | https://docs.databricks.com/en/clusters/monitor/spark-ui.html | Latest |
| **Task Metrics** | https://docs.databricks.com/en/clusters/monitor/spark-ui.html | Latest |
| **Shuffle Read/Write** | https://docs.databricks.com/en/clusters/monitor/spark-ui.html | Latest |

### Performance Bottlenecks

| Topic | URL | Version |
|-------|-----|---------|
| **Data Skew** | https://docs.databricks.com/en/optimizations/adaptive-query-execution.html | Latest |
| **Shuffling** | https://docs.databricks.com/en/sql/conf.html | Latest |
| **Disk Spilling** | https://docs.databricks.com/en/clusters/monitor/spark-ui.html | Latest |
| **Out-of-Memory (OOM) Errors** | https://docs.databricks.com/en/compute/troubleshoot.html | Latest |

### Cluster Startup Issues

| Topic | URL | Version |
|-------|-----|---------|
| **Cluster Startup Troubleshooting** | https://docs.databricks.com/en/compute/troubleshoot.html | Latest |
| **Library Conflicts** | https://docs.databricks.com/en/libraries/index.html | Latest |
| **Init Scripts** | https://docs.databricks.com/en/compute/configure.html | Latest |

### Liquid Clustering & Predictive Optimization

| Topic | URL | Version |
|-------|-----|---------|
| **Liquid Clustering** | https://docs.databricks.com/en/tables/clustering.html | Latest |
| **Predictive Optimization** | https://docs.databricks.com/en/optimizations/predictive-optimization.html | Latest |
| **Auto-Optimization** | https://docs.databricks.com/en/delta/table-properties.html | Latest |

---

## Domain 7: Governance & Security (15%)

### Unity Catalog Fundamentals (Reviewed)

| Topic | URL | Version |
|-------|-----|---------|
| **Unity Catalog Overview** | https://docs.databricks.com/en/unity-catalog/index.html | Latest |
| **Managed vs External Tables** | https://docs.databricks.com/en/unity-catalog/create-tables.html | Latest |

### Privilege Management

| Topic | URL | Version |
|-------|-----|---------|
| **GRANT / REVOKE / DENY** | https://docs.databricks.com/en/unity-catalog/manage-privileges/privileges.html | Latest |
| **Privilege Reference** | https://docs.databricks.com/en/unity-catalog/manage-privileges/privileges.html | Latest |
| **Principals (Users, Groups, Service Principals)** | https://docs.databricks.com/en/unity-catalog/manage-privileges/privileges.html | Latest |

### Column & Row-Level Security

| Topic | URL | Version |
|-------|-----|---------|
| **Column-Level Masking** | https://docs.databricks.com/en/security/column-masking.html | Latest |
| **Row-Level Security (Row Filters)** | https://docs.databricks.com/en/security/row-filter.html | Latest |
| **ABAC (Attribute-Based Access Control)** | https://docs.databricks.com/en/unity-catalog/attribute-controls.html | Latest |

---

## Cross-Domain: Lakeflow Spark Declarative Pipelines (DLT)

| Topic | URL | Version |
|-------|-----|---------|
| **Lakeflow Spark Declarative Pipelines** | https://docs.databricks.com/en/lakeflow/pipelines/index.html | Latest |
| **Formerly Delta Live Tables (DLT)** | https://docs.databricks.com/en/lakeflow/pipelines/index.html | Latest |
| **LIVE TABLE** | https://docs.databricks.com/en/lakeflow/pipelines/live-tables.html | Latest |
| **STREAMING TABLE** | https://docs.databricks.com/en/lakeflow/pipelines/streaming-tables.html | Latest |
| **Expectations** | https://docs.databricks.com/en/lakeflow/pipelines/expectations.html | Latest |
| **Pipeline Monitoring** | https://docs.databricks.com/en/lakeflow/pipelines/monitor.html | Latest |

---

## Cross-Domain: Lakeflow Connect

| Topic | URL | Version |
|-------|-----|---------|
| **Lakeflow Connect** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Latest |
| **Standard Connectors** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Latest |
| **Managed Connectors** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | Latest |

---

## Release Notes & Updates

| Topic | URL | Version |
|-------|-----|---------|
| **Databricks Runtime 17.0 (ANSI Mode Default)** | https://docs.databricks.com/en/release-notes/runtime/17.0.html | Runtime 17.0 |
| **Databricks Runtime 16.4 LTS** | https://docs.databricks.com/en/release-notes/runtime/16.4lts.html | Runtime 16.4 LTS |
| **Declarative Automation Bundles Rename** | https://docs.databricks.com/en/release-notes/dev-tools/bundles.html | March 2026 |
| **Automatic Liquid Clustering GA** | https://docs.databricks.com/en/tables/clustering.html | June 2025 |
| **Serverless Jobs (2026)** | https://docs.databricks.com/en/jobs/run-serverless-jobs.html | 2026 |
| **Query-Based Connectors GA** | https://docs.databricks.com/en/ingestion/lakeflow-connect.html | May 2026 |
| **Unity Catalog Secrets GA** | https://docs.databricks.com/en/security/secrets/index.html | August 2026 |

---

## Audit Notes

**Verified Date:** August 30, 2026  
**Base Exam Guide:** Databricks Certified Data Engineer Associate (May 2026)  
**DBR Support:** Databricks Runtime 15.4 LTS – 17.0+

### Key Updates Verified:
- ✅ Automatic Liquid Clustering (CLUSTER BY AUTO) — June 2025 GA
- ✅ Auto Loader Type Widening (addNewColumnsWithTypeWidening) — Runtime 16.4+
- ✅ Auto Loader cleanSource Option — Runtime 16.4+
- ✅ Serverless Jobs as Default — 2026 Update
- ✅ Declarative Automation Bundles Renamed — March 2026
- ✅ Lakeflow Jobs (formerly Workflows) — Renamed
- ✅ Lakeflow Spark Declarative Pipelines (formerly DLT) — Renamed
- ✅ Lakeflow Connect (standard & managed) — Current taxonomy
- ✅ Query-Based Connectors GA — May 2026
- ✅ Unity Catalog Secrets GA — August 2026

---

**Last Updated:** August 30, 2026  
**Next Review:** Monitor for Runtime 17.0+ and Q4 2026 releases
