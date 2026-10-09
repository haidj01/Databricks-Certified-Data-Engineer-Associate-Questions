# Exam Preparation Guide

**Category:** Exam Strategy
**Last Updated:** 2026-09-09

## Exam Overview

**Official Name:** Databricks Certified Data Engineer Associate

**Format:**
- **Questions:** 45 scored multiple-choice questions
- **Time:** 90 minutes (~2 minutes per question)
- **Fee:** USD $200 (plus taxes)
- **Delivery:** Online or test center
- **Test Aids:** None allowed
- **Validity:** 2 years
- **Recertification:** Required every 2 years

**Prerequisites:**
- None required (recommended: 6 months hands-on experience)
- Course attendance highly recommended

**Important:** Exams may include unscored items for statistical purposes. These don't impact your score but extra time is factored in.

## Exam Sections & Weights

Understanding the weight of each section helps prioritize study time:

### Section 1: Databricks Intelligence Platform (6%)
**~3 questions**

**Topics:**
- Platform architecture (Control Plane vs Data Plane)
- Delta Lake fundamentals
- Unity Catalog basics
- Compute services (characteristics, limitations, cost models)
- Selecting appropriate compute for workloads

**Study Priority:** Low (only 6% of exam)

**Cross-Reference:** [Workspace](workspace.md), [Delta Lake](delta-lake.md)

---

### Section 2: Data Ingestion and Loading (21%)
**~9-10 questions** ⭐ **HIGH PRIORITY**

**Topics:**
- Batch, streaming, and incremental loading patterns
- **COPY INTO** command for cloud object storage
- **Auto Loader** with schema enforcement and evolution
- **Lakeflow Connect** (standard and managed connectors)
- JDBC/ODBC and REST clients for data ingestion
- Prioritizing ingestion methods based on requirements
- Ingesting semi-structured data (JSON, nested data)

**Study Priority:** ⭐ **HIGHEST** (21% of exam)

**Cross-Reference:** [Batch Processing](batch-processing.md), [Streaming](streaming.md)

---

### Section 3: Data Transformation and Modeling (22%)
**~10 questions** ⭐ **HIGH PRIORITY**

**Topics:**
- Data cleaning (nulls, standardizing types, Bronze→Silver)
- DataFrame operations (joins, unions, filters)
- Column/row manipulation (add, drop, rename, explode arrays)
- Data deduplication and aggregations
- **Spark tuning parameters:**
  - `spark.sql.shuffle.partitions`
  - `spark.default.parallelism`
  - `spark.executor.memory` / `spark.driver.memory`
  - `spark.sql.autoBroadcastJoinThreshold`
- Gold layer objects (materialized views, views, streaming tables)
- Data quality checks and validation

**Study Priority:** ⭐ **HIGHEST** (22% of exam)

**Cross-Reference:** [Spark Fundamentals](spark-fundamentals.md), [Medallion Architecture](medallion-architecture.md)

---

### Section 4: Working with Lakeflow Jobs (16%)
**~7 questions**

**Topics:**
- Control flows (retries, conditional tasks, branching, looping)
- Configuring tasks (notebook, SQL query, dashboard, pipeline tasks)
- Task dependencies using DAG-based task graph
- Job schedules and trigger types:
  - Scheduled (cron)
  - File arrival
  - Table update
- Time-based vs data-driven triggers

**Study Priority:** Medium-High (16% of exam)

**Cross-Reference:** [Workflows](workflows.md)

---

### Section 5: Implementing CI/CD (10%)
**~4-5 questions**

**Topics:**
- Code development workflow in Databricks UI
- **Databricks Git Folders** (formerly Repos):
  - Creating and switching branches
  - Committing and pushing changes
  - Creating pull requests
- **Declarative Automation Bundles (DABs):**
  - Environment-specific configuration (dev/test/prod)
  - Variables and overrides
  - Packaging and promoting Jobs and Pipelines
- **Databricks CLI** for automated workflows

**Study Priority:** Medium (10% of exam)

**Cross-Reference:** [Workspace](workspace.md)

---

### Section 6: Troubleshooting, Monitoring, and Optimization (10%)
**~4-5 questions**

**Topics:**
- Job performance trends using run history
- Monitoring pipeline health (job statuses, DAG graphs, run times)
- **Performance bottlenecks:**
  - Data skew
  - Shuffling
  - Disk spilling
  - Interpreting Spark UI stage-level metrics
- **Liquid Clustering** features
- **Predictive Optimization** features
- Cluster issues (startup failures, library conflicts, OOM)

**Study Priority:** Medium (10% of exam)

**Cross-Reference:** [Cost Optimization](cost-optimization.md), [Spark Fundamentals](spark-fundamentals.md)

---

### Section 7: Governance and Security (15%)
**~7 questions**

**Topics:**
- Managed vs External tables (create, modify, delete, convert)
- Access controls using UI and SQL:
  - `GRANT`, `REVOKE`, `DENY` privileges
  - Principals (users, groups, service principals)
  - Security hierarchy levels
- **Column-level masking**
- **Row-level security**
- **Unity Catalog ABAC policies** (row filtering, column masking)

**Study Priority:** Medium-High (15% of exam)

**Cross-Reference:** [Unity Catalog](unity-catalog.md)

---

## Key Terminology Updates (May 2026)

⚠️ **CRITICAL:** Databricks has renamed several products. Know both old and new names for the exam.

| Old Name | New Name (May 2026) | Alias |
|----------|---------------------|-------|
| Delta Live Tables | **Lakeflow Spark Declarative Pipeline** | DLT still used |
| Databricks Jobs | **Lakeflow Jobs** | Jobs still used |
| Databricks Repos | **Databricks Git Folders** | Repos deprecated |
| Databricks Asset Bundles | **Declarative Automation Bundles** | DABs |
| Auto Loader | Auto Loader | No change |
| - | **Lakeflow Connect** | New ingestion system |

**Exam Tip:** Questions may use either old or new terminology. Be familiar with both!

## Sample Exam Questions

The exam guide provides 5 retired sample questions. Here are the key patterns:

### Question 1: Data Skew Diagnosis
**Objective:** Identify performance bottlenecks (data skew, shuffling, disk spilling)

**Scenario:** Job duration doubled. Spark UI shows most tasks finish in <30s, but one task takes 10+ minutes. Shuffle read: Min/Median 400MB, Max 5GB.

**Answer:** Confirm adaptive query execution with skew join handling is active ✓

**Key Concepts:**
- Data skew = one partition much larger than others
- Adaptive Query Execution (AQE) handles skew automatically
- Alternative: manual salting/repartitioning

**Cross-Reference:** [Spark Fundamentals](spark-fundamentals.md)

---

### Question 2: Platform Selection
**Objective:** Select suitable compute/platform for workload

**Scenario:** Need rapid iteration, reliable rollbacks, audit trails, consistent access for AI and BI.

**Answer:** Delta Lake ACID transactions + time travel, governed by Unity Catalog ✓

**Key Concepts:**
- Delta Lake provides ACID + time travel
- Unity Catalog provides governance + lineage
- Single source of truth pattern

**Cross-Reference:** [Delta Lake](delta-lake.md), [Unity Catalog](unity-catalog.md)

---

### Question 3: Audit Log Ingestion
**Objective:** Data ingestion patterns

**Scenario:** Building pipelines to consume Databricks audit logs from S3. Need to understand format, latency, and overwrite behavior.

**Answer:** JSON format, <15 minute latency, files can be overwritten ✓

**Key Concepts:**
- Audit logs are JSON (not Parquet/CSV)
- Near real-time delivery (<15 min)
- Idempotency required (files may be overwritten)
- Use Auto Loader with checkpointing

**Cross-Reference:** [Streaming](streaming.md), [Batch Processing](batch-processing.md)

---

### Question 4: Cluster Configuration
**Objective:** Diagnose cluster configuration issues

**Scenario:** Support ad hoc SQL queries for business analysts. Need fast startup, multiple simultaneous users, cost-effective scaling.

**Answer:** High-concurrency cluster with autoscaling ✓

**Key Concepts:**
- High-concurrency cluster = shared for multiple users
- Autoscaling = cost-effective (scales down when idle)
- Job cluster = for scheduled ETL (not ad hoc)
- All-purpose fixed = no auto-scaling

**Cross-Reference:** [Cost Optimization](cost-optimization.md), [Workspace](workspace.md)

---

### Question 5: CI/CD Deployment
**Objective:** Code development workflow and CI/CD

**Scenario:** Need modular deployment, versioning, orchestration of ETL pipelines with CI/CD repeatability.

**Answer:** Use DABs (Declarative Automation Bundles) with Git + CI/CD ✓

**Key Concepts:**
- DABs = infrastructure as code for Databricks
- Version in Git (standard workflow)
- Promote across environments (dev→test→prod)
- Automated CI/CD actions

**Cross-Reference:** [Workflows](workflows.md)

---

## Study Strategy

### Time Allocation by Section

Based on exam weights and complexity:

| Section | Weight | Study Time | Priority |
|---------|--------|------------|----------|
| Data Transformation (§3) | 22% | 25% | ⭐⭐⭐ |
| Data Ingestion (§2) | 21% | 25% | ⭐⭐⭐ |
| Lakeflow Jobs (§4) | 16% | 15% | ⭐⭐ |
| Governance & Security (§7) | 15% | 15% | ⭐⭐ |
| CI/CD (§5) | 10% | 10% | ⭐ |
| Troubleshooting (§6) | 10% | 10% | ⭐ |
| Platform Overview (§1) | 6% | 5% | ⭐ |

### Recommended Study Plan

**Week 1-2: Core Foundations (50% of exam)**
- Data Ingestion patterns (COPY INTO, Auto Loader, Lakeflow Connect)
- Data Transformation (PySpark, SQL, medallion architecture)
- Spark fundamentals (joins, aggregations, tuning)
- Delta Lake (ACID, MERGE, OPTIMIZE, time travel)

**Week 3: Workflows & Orchestration (16% of exam)**
- Lakeflow Jobs (task dependencies, triggers, DAG)
- Scheduling patterns (cron, file arrival, table update)
- Control flows (retries, branching, looping)

**Week 4: Governance & Security (15% of exam)**
- Unity Catalog (managed vs external tables)
- Access controls (GRANT/REVOKE/DENY)
- Row-level security and column masking
- ABAC policies

**Week 5: Advanced Topics (20% of exam)**
- CI/CD with DABs and Git Folders
- Troubleshooting (Spark UI, data skew, OOM)
- Performance optimization (Liquid Clustering, AQE)
- Cost optimization strategies

**Week 6: Practice & Review**
- Take practice exams
- Review weak areas
- Memorize terminology updates
- Time yourself (2 minutes per question)

### During the Exam

**Time Management:**
- 90 minutes ÷ 45 questions = **2 minutes per question**
- Flag difficult questions and move on
- Reserve 10-15 minutes for review
- Don't spend >3 minutes on any single question

**Question Strategies:**
1. **Read carefully** - questions test nuances
2. **Eliminate wrong answers** first
3. **Look for keywords** - "most suitable", "best practice", "recommended"
4. **Watch for negatives** - "NOT", "EXCEPT", "avoid"
5. **Scenario-based** - match requirements to solution

**Common Traps:**
- Confusing old vs new terminology
- Batch vs Streaming recommendations (Silver = batch preferred!)
- GRANT USAGE vs ALL PRIVILEGES
- Job cluster vs All-purpose cluster costs
- COPY INTO vs Auto Loader use cases

## High-Yield Topics

Focus on these for maximum ROI:

### Must-Know Commands
```sql
-- COPY INTO (incremental file loading)
COPY INTO target FROM '/path' FILEFORMAT = PARQUET;

-- MERGE (upsert pattern)
MERGE INTO target USING source ON condition
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;

-- OPTIMIZE (file compaction)
OPTIMIZE table_name ZORDER BY (column);

-- VACUUM (file cleanup, default 7 days)
VACUUM table_name RETAIN 168 HOURS;

-- GRANT (permissions)
GRANT SELECT ON TABLE my_table TO user@example.com;
GRANT USAGE ON SCHEMA my_schema TO `analysts`;
```

### Must-Know PySpark
```python
# Auto Loader pattern
spark.readStream \
  .format("cloudFiles") \
  .option("cloudFiles.format", "json") \
  .option("cloudFiles.schemaLocation", "/schema") \
  .load("/data")

# Streaming trigger patterns
.trigger(processingTime="5 seconds")  # Micro-batch
.trigger(availableNow=True)           # Process all available, then stop
.trigger(once=True)                   # Process once (deprecated)

# DataFrame operations
df.join(other_df, "key", "inner")     # Join
df.groupBy("col").agg(F.sum("amt"))   # Aggregation
df.dropDuplicates(["id"])             # Deduplication
df.withColumn("new", F.expr("..."))   # Add column
```

### Must-Know Concepts

**Medallion Architecture:**
- Bronze = raw ingestion (streaming recommended)
- Silver = cleaned data (batch with incremental refresh)
- Gold = business aggregates (batch processing)

**Cluster Types:**
- All-purpose = interactive, 2x DBU cost
- Job cluster = automated, lower cost
- High-concurrency = shared, SQL analytics
- Single-node = development only

**Unity Catalog Hierarchy:**
- Metastore → Catalog → Schema → Table/View
- GRANT USAGE = access to container (navigate)
- GRANT SELECT = read data
- GRANT ALL PRIVILEGES = full control

**Spark Tuning:**
- `spark.sql.shuffle.partitions` = default 200 (tune for data size)
- `spark.sql.autoBroadcastJoinThreshold` = default 10MB
- Broadcast join = small table (<10MB) to all executors
- Shuffle = expensive, minimize when possible

## Cross-References

- [Delta Lake](delta-lake.md) - ACID, time travel, OPTIMIZE
- [Unity Catalog](unity-catalog.md) - Permissions, governance
- [Streaming](streaming.md) - Triggers, watermarks
- [Batch Processing](batch-processing.md) - COPY INTO, MERGE
- [Spark Fundamentals](spark-fundamentals.md) - Tuning, joins
- [Workflows](workflows.md) - Lakeflow Jobs, scheduling
- [Cost Optimization](cost-optimization.md) - Cluster types, auto-stop
- [Medallion Architecture](medallion-architecture.md) - Bronze/Silver/Gold

## Sources

- Official Exam Guide (May 2026)
- databricks-certified-data-engineer-associate-exam-guide-may-2026-000.pdf
- 5 sample questions with answers

## Next Steps

1. ✅ Review this exam prep guide
2. ⏳ Complete all topic pages in recommended order
3. ⏳ Take practice exams and track weak areas
4. ⏳ Review terminology updates (old vs new names)
5. ⏳ Memorize high-yield commands and patterns
6. ⏳ Practice Spark UI interpretation for data skew
7. ⏳ Understand DABs deployment workflow
