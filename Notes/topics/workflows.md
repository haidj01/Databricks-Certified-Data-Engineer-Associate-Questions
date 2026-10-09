# Lakeflow Jobs (Databricks Workflows)

**Category:** Operations
**Last Updated:** 2026-09-09
**Terminology:** Formerly "Databricks Jobs/Workflows". Renamed to "Lakeflow Jobs" as of May 2026. Both names may appear on the exam.

## Overview

Lakeflow Jobs orchestrates data engineering tasks, ML pipelines, and analytics workloads with dependencies, scheduling, and monitoring using DAG-based task graphs.

## Key Concepts

### Job Components

**Job:** Top-level orchestration unit
**Tasks:** Individual units of work
**Clusters:** Compute resources

### Task Dependencies

Tasks can depend on other tasks:

```json
{
  "tasks": [
    {
      "task_key": "bronze_ingestion",
      "notebook_task": {...}
    },
    {
      "task_key": "silver_transformation",
      "depends_on": [{"task_key": "bronze_ingestion"}],
      "notebook_task": {...}
    }
  ]
}
```

**Cross-Reference:** See [Delta Live Tables](delta-live-tables.md) for automatic dependency inference

### Scheduling

#### Cron-based Scheduling

```python
# Every day at 2 AM
schedule = "0 2 * * *"

# Every Monday at 9 AM
schedule = "0 9 * * 1"

# Every hour
schedule = "0 * * * *"
```

#### Preventing Execution on Specific Days

**README Q29: Prevent code from running on Sundays**

**Method 1: Schedule-based (preferred)**
```python
# Cron: Run Monday-Saturday at 2 AM (skip Sunday)
schedule = "0 2 * * 1-6"
```

**Method 2: Conditional logic in code**
```python
from datetime import datetime

if datetime.now().weekday() != 6:  # 6 = Sunday
    # Execute workload
    process_data()
else:
    print("Skipping Sunday execution")
```

**Method 3: Job-level condition**
```python
# In job configuration
if datetime.now().strftime("%A") != "Sunday":
    dbutils.notebook.run("process_notebook")
```

### Alerts and Notifications

#### Email Alerts

```json
{
  "email_notifications": {
    "on_start": ["team@example.com"],
    "on_success": ["team@example.com"],
    "on_failure": ["oncall@example.com"]
  }
}
```

#### Webhooks

```json
{
  "webhook_notifications": {
    "on_failure": [{
      "id": "webhook-123"
    }]
  }
}
```

**README Q44: Webhook vs. Email for alerts?**

**Use webhooks when:**
- Integration with incident management (PagerDuty, Slack)
- Automated remediation needed
- Custom notification logic required
- Programmable responses needed

**Use email when:**
- Simple notifications sufficient
- Human review required
- No integration systems
- Less urgent alerts

### Retry Configuration

```json
{
  "max_retries": 3,
  "retry_on_timeout": true,
  "timeout_seconds": 3600
}
```

## Checking Task Status

**README Q43: Check failed task status in DLT**

**Method 1: UI**
- Navigate to Pipeline
- View Event Log
- Filter by "error" or "failed"

**Method 2: API**
```python
GET /api/2.0/pipelines/{pipeline_id}/events?filter=level='ERROR'
```

**Method 3: System Tables**
```sql
SELECT * FROM system.lakeflow.pipeline_events
WHERE level = 'ERROR'
AND pipeline_id = '<pipeline-id>';
```

## Job Types

### Notebook Tasks
```json
{
  "notebook_task": {
    "notebook_path": "/path/to/notebook",
    "base_parameters": {"param1": "value1"}
  }
}
```

### DLT Pipeline Tasks
```json
{
  "pipeline_task": {
    "pipeline_id": "abc-123"
  }
}
```

### Python Wheel Tasks
```json
{
  "python_wheel_task": {
    "package_name": "my_package",
    "entry_point": "main"
  }
}
```

## Declarative Automation Bundles (DABs)

**Terminology:** Formerly "Databricks Asset Bundles". Renamed to "Declarative Automation Bundles" (DABs) as of May 2026.

**Sample Exam Question (From Official Exam Guide):**

**Scenario:** Need modular deployment, versioning, orchestration of ETL pipelines with CI/CD repeatability across dev/test/prod environments.

**Question:** What approach should you use for deployment?

**Answer:** Use DABs (Declarative Automation Bundles) with Git + CI/CD ✓

**Why DABs:**

1. **Modular Deployment:**
   - Bundle jobs, pipelines, notebooks, libraries together
   - Single deployment unit
   - Consistent environment configuration

2. **Versioning:**
   - Infrastructure as code in Git
   - Track changes over time
   - Rollback to previous versions

3. **Orchestration:**
   - Define task dependencies declaratively
   - Multi-stage workflows
   - Automated execution order

4. **CI/CD Repeatability:**
   - Automated deployment pipelines
   - Environment promotion (dev → test → prod)
   - Consistent deployments across environments

**DAB Structure:**
```yaml
# databricks.yml
bundle:
  name: data_pipeline

variables:
  catalog:
    description: Target catalog
    default: dev

environments:
  dev:
    variables:
      catalog: dev_catalog

  prod:
    variables:
      catalog: prod_catalog

resources:
  jobs:
    daily_etl:
      name: "Daily ETL - ${var.catalog}"
      tasks:
        - task_key: bronze_ingestion
          notebook_task:
            notebook_path: ./notebooks/bronze.py

        - task_key: silver_transform
          depends_on:
            - task_key: bronze_ingestion
          notebook_task:
            notebook_path: ./notebooks/silver.py

  pipelines:
    dlt_pipeline:
      name: "DLT Pipeline - ${var.catalog}"
      catalog: ${var.catalog}
      target: pipeline_schema
```

**Deployment Workflow:**
```bash
# Deploy to dev
databricks bundle deploy -t dev

# Validate in dev
databricks bundle run daily_etl -t dev

# Deploy to prod (via CI/CD)
databricks bundle deploy -t prod
```

**CI/CD Integration (GitHub Actions Example):**
```yaml
name: Deploy to Production
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy DAB
        run: |
          databricks bundle validate -t prod
          databricks bundle deploy -t prod
```

**Benefits:**
- **Version Control:** All config in Git
- **Environment Parity:** Same code, different variables
- **Automated Testing:** Validate before deploy
- **Audit Trail:** Git history tracks changes
- **Team Collaboration:** Pull request workflow

**Alternatives (not recommended):**

| Approach | Limitation |
|----------|------------|
| **Manual UI deployment** | Not repeatable, no version control |
| **Custom scripts** | Hard to maintain, error-prone |
| **Notebook-based deployment** | Limited orchestration, no env separation |
| **Terraform only** | More complex than DABs for Databricks |

**Best Practices:**
- Store DABs in Git repository
- Use environment variables for config
- Validate bundles before deployment
- Separate dev/test/prod environments
- Automate deployments via CI/CD
- Version bundle configurations
- Test in dev before prod promotion

**Cross-Reference:** See [exam-prep.md](exam-prep.md) for full sample question details, [Workspace](workspace.md) for Git Folders integration

## Common Patterns

### Multi-stage Pipeline

```
Bronze Ingestion
    ↓
Silver Transformation (depends on Bronze)
    ↓
Gold Aggregation (depends on Silver)
    ↓
Data Quality Checks (depends on Gold)
```

### Parallel Processing

```
Source A → Process A ↘
                      → Merge → Output
Source B → Process B ↗
```

Both Process A and Process B run in parallel, then Merge waits for both.

## Common Pitfalls

1. **No task dependencies** - Race conditions
2. **Circular dependencies** - Job won't start
3. **Missing retries** - Transient failures cause issues
4. **No timeout** - Jobs hang indefinitely
5. **Wrong alert channel** - Missed critical failures

## Exam Tips

- Schedule with cron to prevent specific days (Q29)
- Webhook = integration, Email = simple notification (Q44)
- Check failed tasks in event log or system tables (Q43)
- Task dependencies defined via depends_on

## Cross-References

- [Delta Live Tables](delta-live-tables.md) - Pipeline execution
- [Cost Optimization](cost-optimization.md) - Job cluster configuration
- [Monitoring](monitoring.md) - Job metrics

## Sources

- References/de-mod-5-deploy-workloads-with-databricks-workflows.pdf (pending ingestion)
- Practice exam questions
