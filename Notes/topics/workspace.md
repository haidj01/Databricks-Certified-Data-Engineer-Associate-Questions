# Databricks Workspace

**Category:** Development & Tools
**Last Updated:** 2026-09-09
**Terminology:** "Databricks Repos" renamed to "Databricks Git Folders" as of May 2026. Both names may appear on the exam.

## Overview

The Databricks workspace provides a collaborative environment for data engineering, data science, and analytics.

## Architecture Components

### Control Plane vs. Data Plane

**README Q5: Which component is web application part of?**

#### Control Plane
The web application, user interface, and management services.

**Components:**
- **Web application** ✓ (Answer to Q5)
- Workspace UI
- Notebook interface
- Job scheduler
- Cluster manager (configuration)
- User management
- Metadata services

**Hosted by:** Databricks (managed service)

**Access:** HTTPS through browser

#### Data Plane
Where actual data processing and storage occurs.

**Components:**
- Compute clusters (VMs)
- Data storage (S3, ADLS, GCS)
- Network infrastructure
- Processing engines (Spark, ML runtimes)

**Hosted by:** Customer's cloud account (AWS, Azure, GCP)

**Security:** VNet/VPC peering, private links

**Key Distinction:**
- **Control Plane** = management, UI, orchestration
- **Data Plane** = compute, storage, processing

**Exam Tip:** Web application is part of the **Control Plane**

## Git Folders and Version Control

### Databricks Git Folders (formerly Repos)

Git integration for notebooks and code.

**Terminology Note:** Previously called "Databricks Repos", renamed to "Databricks Git Folders" in May 2026.

**README Q6: What operations done outside of Databricks repo?**

#### Inside Databricks Repos (UI)
- ✓ Create branch
- ✓ Switch branch
- ✓ Commit changes
- ✓ Pull from remote
- ✓ View diff
- ✓ Resolve conflicts

#### Outside Databricks Repos
**These require external git client:**
- ✗ **Push to remote** (requires git push from terminal/client)
- ✗ **Clone repository** (initial clone done externally)
- ✗ Force push
- ✗ Rebase operations
- ✗ Complex merge strategies

**Note:** As of 2026, Databricks Repos supports most git operations in UI. Check current documentation for latest features.

**Answer to Q6:** Clone and push operations traditionally done outside repos (though UI capabilities have expanded)

### Repos vs. Notebook Versioning

**README Q7: Advantage of repo over notebook versioning?**

#### Notebook Versioning (Legacy)

**Features:**
- Revision history per notebook
- Restore previous versions
- Compare changes
- Auto-saved versions

**Limitations:**
- ✗ No branching
- ✗ No collaborative workflows
- ✗ No external git integration
- ✗ Single notebook scope
- ✗ No CI/CD integration

#### Databricks Repos (Recommended)

**Advantages:**
1. **Branching support** ✓ (Key advantage for Q7)
   - Feature branches
   - Parallel development
   - Isolated experimentation

2. **Collaborative workflows**
   - Pull requests
   - Code review
   - Team collaboration

3. **External git integration**
   - GitHub, GitLab, Bitbucket
   - Standard git workflows
   - Industry-standard VCS

4. **Multi-file scope**
   - Entire project versioning
   - Dependencies tracked
   - Configuration files

5. **CI/CD integration**
   - Automated testing
   - Deployment pipelines
   - Environment promotion

**Exam Tip:** Main advantage is **branching** capability (Q7)

## Workspace Objects

### Notebooks

**Types:**
- Python notebooks (.py)
- SQL notebooks (.sql)
- Scala notebooks (.scala)
- R notebooks (.r)

**Features:**
- Interactive execution
- Real-time collaboration
- Visualization
- Magic commands
- Widget parameters
- Revision history

**Magic Commands:**
```python
%python  # Switch cell to Python
%sql     # Switch cell to SQL
%scala   # Switch cell to Scala
%r       # Switch cell to R
%sh      # Run shell command
%md      # Markdown text cell
%run /path/to/notebook  # Run another notebook inline
%fs ls /path/  # Browse DBFS
```

**Widget Parameters:**
```python
# Create widgets for parameterization
dbutils.widgets.text('param_name', 'default_value')
dbutils.widgets.dropdown('env', 'dev', ['dev', 'prod'])
dbutils.widgets.multiselect('regions', 'us-east', ['us-east', 'us-west'])

# Get widget values
param = dbutils.widgets.get('param_name')
```

**dbutils - Databricks Utilities:**
```python
# File operations
dbutils.fs.ls('/delta/')
dbutils.fs.cp('/src/', '/dst/')
dbutils.fs.rm('/path/', recurse=True)

# Secrets
dbutils.secrets.get('scope', 'key')

# Notebook orchestration
dbutils.notebook.run('/path/child', timeout_seconds=300,
                     arguments={'param': 'value'})
dbutils.notebook.exit('return_value')
```

### Jobs

Scheduled or triggered workloads.

**Components:**
- Tasks (notebooks, JARs, Python wheels, DLT)
- Clusters (job or all-purpose)
- Schedules (cron-based)
- Dependencies (task ordering)

**Cross-Reference:** See [Workflows](workflows.md)

### Clusters

**Types:**
- **All-purpose clusters:** Interactive use, higher DBU cost
- **Job clusters:** Automated workloads, lower DBU cost

**Cross-Reference:** See [Cost Optimization](cost-optimization.md)

### Databricks Runtime (DBR)

Pre-configured Apache Spark environments with additional optimizations.

**Runtime Types:**

| Runtime Type | Includes | Best For |
|-------------|----------|----------|
| **Standard DBR** | Apache Spark, Delta Lake, Python, R, Scala | General data engineering, ETL pipelines |
| **DBR ML** | Standard DBR + MLflow, TensorFlow, PyTorch, scikit-learn | Machine learning model training, feature engineering |
| **Photon Runtime** | Standard DBR + native vectorized query engine | SQL workloads, BI queries, 3-5x faster analytics |
| **DBR LTS** | Long-Term Support versions | Production workloads requiring stability |
| **DBR Genomics** | Standard DBR + genomics libraries (Hail, GATK) | Bioinformatics, genomic data analysis |

**Version Selection:**
```python
# Cluster configuration
{
  "spark_version": "13.3.x-scala2.12",  # Standard DBR
  "spark_version": "13.3.x-cpu-ml-scala2.12",  # ML Runtime
  "spark_version": "13.3.x-photon-scala2.12"  # Photon Runtime
}
```

**Exam Tip:** Photon provides significant performance improvements for SQL workloads without code changes.

### Dashboards

SQL-based analytics dashboards.

**Features:**
- Query visualizations
- Scheduled refreshes
- Sharing and permissions
- Parameterized queries

## File Storage: DBFS vs Unity Catalog Volumes

### Comparison Table

| Aspect | DBFS | Unity Catalog Volumes |
|--------|------|----------------------|
| **Governance** | Limited, no fine-grained access control | Full Unity Catalog governance with ACLs |
| **Path Format** | `dbfs:/path/to/file` or `/dbfs/path/to/file` | `/Volumes/catalog/schema/volume/path` |
| **Access Control** | Workspace-level only | Catalog, schema, and volume-level GRANT/REVOKE |
| **Use Cases** | Legacy data, temp files, DBFS root | Governed file storage, ML artifacts, unstructured data |
| **Auditability** | Limited audit trail | Full Unity Catalog audit logs and lineage |
| **Portability** | Workspace-specific | Cross-workspace with Unity Catalog metastore |
| **Recommendation** | Migrate away from DBFS | **Preferred for new projects** |

### When to Use Unity Catalog Volumes

**Recommended:**
- Storing ML models and artifacts
- Unstructured data (images, PDFs, audio files)
- Files requiring access control
- Multi-workspace environments
- Compliance and audit requirements

**Example:**
```python
# DBFS (legacy)
df = spark.read.parquet("dbfs:/mnt/data/files/")

# Unity Catalog Volumes (recommended)
df = spark.read.parquet("/Volumes/main/bronze/raw_files/data.parquet")

# Create volume
spark.sql("""
  CREATE VOLUME IF NOT EXISTS main.bronze.raw_files
  COMMENT 'Raw file ingestion storage'
""")

# Grant access
spark.sql("GRANT READ VOLUMES ON VOLUME main.bronze.raw_files TO `analysts`")
```

**Migration Path:**
1. Create Unity Catalog volumes
2. Copy data from DBFS to volumes
3. Update code references
4. Deprecate DBFS mounts

**Cross-Reference:** See [Unity Catalog](unity-catalog.md) for detailed volume management

## Workspace Organization

### Folder Structure Best Practices

```
/Workspace/
├── /Users/
│   └── /user@example.com/
│       ├── /experiments/
│       └── /scratch/
├── /Shared/
│   ├── /production/
│   ├── /staging/
│   └── /development/
└── /Repos/
    └── /team-repo/
        ├── /notebooks/
        ├── /src/
        └── /tests/
```

## Practice Questions

### Week 1 Study Guide Questions

**Q6: Photon Runtime Performance Advantage**

Your team runs heavy SQL analytics workloads on large datasets. What is the primary performance advantage of using Photon Runtime over standard Databricks Runtime?

**Answer:** C++ vectorized query engine providing 2-3x faster SQL workloads without code changes ✓

**Explanation:**

Photon is a native vectorized query engine written in C++ that provides significant performance improvements for SQL workloads:

**Performance Benefits:**
- **2-3x faster queries** for SQL and DataFrame operations
- **Lower cost** due to faster execution (less compute time)
- **Zero code changes** required - drop-in replacement
- **Automatic optimization** of query execution

**How Photon Works:**
- Vectorized execution processes data in batches (SIMD instructions)
- Native C++ implementation (not JVM-based like standard Spark)
- Optimized for modern CPUs with advanced instruction sets
- Efficient memory management and data processing

**When to Use Photon:**
- SQL-heavy workloads (BI dashboards, analytics queries)
- Large table scans and aggregations
- Complex joins and window functions
- High-concurrency SQL warehouses
- Cost-sensitive environments (faster = cheaper)

**Configuration:**
```python
# Cluster configuration with Photon
{
  "spark_version": "13.3.x-photon-scala2.12",
  "node_type_id": "i3.xlarge",
  "autoscale": {
    "min_workers": 2,
    "max_workers": 8
  }
}
```

**Photon vs Standard Runtime:**

| Aspect | Standard DBR | Photon Runtime |
|--------|-------------|----------------|
| **Query Engine** | JVM-based Spark | C++ vectorized engine |
| **SQL Performance** | Baseline | 2-3x faster |
| **Code Changes** | N/A | None required |
| **Memory Efficiency** | Good | Excellent |
| **Cost** | Standard | Lower (faster execution) |
| **Use Case** | General workloads | SQL-heavy analytics |

**Built-in Features:**
- Serverless SQL Warehouses use Photon by default
- No additional configuration needed for serverless
- Compatible with all Delta Lake features
- Works with existing SQL queries and notebooks

**Example Performance:**
```sql
-- Same query on Standard DBR: 45 seconds
-- Same query on Photon: 15 seconds (3x faster)
SELECT region,
       product_category,
       SUM(sales_amount) AS total_sales,
       AVG(sales_amount) AS avg_sales
FROM sales_data
WHERE sale_date >= '2026-01-01'
GROUP BY region, product_category
HAVING total_sales > 100000
ORDER BY total_sales DESC;
```

**Cross-Reference:** See Databricks Runtime (DBR) section above for runtime type comparison, [Cost Optimization](cost-optimization.md) for Photon cost benefits

## Common Pitfalls

1. **Using notebook versioning for team projects** - No branching
2. **All-purpose clusters for jobs** - 2x cost
3. **Not using Repos** - Missing version control benefits
4. **Shared folders without permissions** - Security risk
5. **Confusing control and data plane** - Architecture misunderstanding

## Exam Tips

- Web application = Control Plane (Q5)
- Push/Clone = outside Databricks Repos (Q6)
- Repos advantage = Branching (Q7)
- Photon = 2-3x faster SQL with zero code changes (Week 1 Q6)
- Control Plane = UI, management
- Data Plane = compute, storage

## Cross-References

- [Workflows](workflows.md) - Job scheduling
- [Cost Optimization](cost-optimization.md) - Cluster types
- [Unity Catalog](unity-catalog.md) - Permissions

## Sources

- Databricks architecture documentation (pending ingestion)
- Practice exam questions Q5, Q6, Q7
- References/de-mod-1-get-started-with-databricks-data-science-and-engineering-workspace.pdf (pending ingestion)
