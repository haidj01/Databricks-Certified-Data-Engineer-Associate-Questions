# Cost Optimization

**Category:** Operations
**Last Updated:** 2026-09-09

## Overview

Strategies to reduce Databricks costs while maintaining performance and reliability.

## Compute Types and DBU Pricing

### Compute Options

| Compute Type | DBU Rate | Best For | Key Features |
|-------------|----------|----------|--------------|
| **All-Purpose Cluster** | High (2x job cluster) | Interactive development, notebooks | Multi-user, persistent, high availability |
| **Job Cluster** | Low (baseline) | Scheduled ETL, production workloads | Auto-terminate, optimized for task |
| **Serverless Compute** | Variable (pay-per-query) | Ad hoc SQL queries, unpredictable workload | Instant startup, auto-scaling |
| **Instance Pool** | Reduced infrastructure cost | Frequent cluster starts | Pre-warmed instances, faster startup |
| **SQL Warehouse (Classic)** | Medium | BI dashboards, SQL analytics | Dedicated SQL engine, caching |
| **SQL Warehouse (Pro)** | Higher | Advanced SQL workloads | Serverless, auto-scaling, photon |
| **SQL Warehouse (Serverless)** | Pay-per-query | Sporadic SQL queries | No cluster management, instant |

### DBU Consumption Patterns

**High DBU Usage Scenarios:**
- All-purpose clusters running 24/7
- Over-provisioned clusters (unused capacity)
- No auto-stop configured
- Large clusters for small workloads
- Inefficient queries (full table scans)

**Low DBU Usage Scenarios:**
- Job clusters with auto-terminate
- Right-sized clusters (autoscaling)
- Auto-stop after 10-30 minutes
- Serverless SQL for ad hoc queries
- Optimized queries with partitioning/Z-ORDER

**Cost Comparison Example:**
```
Scenario: Running 8-hour daily ETL job

Option 1: All-purpose cluster (always on)
- Cluster: 4 workers × 24 hours = 96 worker-hours/day
- DBU rate: 0.75 DBU/worker-hour
- Daily cost: 96 × 0.75 = 72 DBUs/day

Option 2: Job cluster (auto-terminate)
- Cluster: 4 workers × 8 hours = 32 worker-hours/day
- DBU rate: 0.40 DBU/worker-hour
- Daily cost: 32 × 0.40 = 12.8 DBUs/day

Savings: 82% reduction (72 - 12.8 = 59.2 DBUs/day)
```

### Cluster Sizing Guidelines

**Small Workloads (< 100 GB data):**
- Driver: 1x Standard_DS3_v2 (4 cores, 14 GB RAM)
- Workers: 2-4x Standard_DS3_v2
- Autoscale: Min 2, Max 4

**Medium Workloads (100 GB - 1 TB data):**
- Driver: 1x Standard_DS4_v2 (8 cores, 28 GB RAM)
- Workers: 4-8x Standard_DS4_v2
- Autoscale: Min 4, Max 8

**Large Workloads (> 1 TB data):**
- Driver: 1x Standard_DS5_v2 (16 cores, 56 GB RAM)
- Workers: 8-16x Standard_DS5_v2
- Autoscale: Min 8, Max 16

**Memory-Intensive Workloads:**
- Use memory-optimized instances (r5, r6i on AWS)
- Increase executor memory: `spark.executor.memory = 16g`
- Enable off-heap memory: `spark.memory.offHeap.enabled = true`

## Cluster Cost Reduction

### Auto-Stop Configuration

**README Q34, Q77:**

```python
# Cluster configuration
{
  "autotermination_minutes": 30,
  "autoscale": {
    "min_workers": 1,
    "max_workers": 8
  }
}
```

**Benefits:**
- Stops idle clusters automatically
- Reduces DBU consumption
- Pay only for active usage

**Best practice:** Set 10-30 minutes for interactive, 5-10 for jobs

### Cluster Pools

**README Q45: Speed up and reduce costs**

```python
{
  "instance_pool_id": "pool-123",
  "min_idle_instances": 2,
  "max_capacity": 10
}
```

**Advantages:**
- Faster cluster start times (pre-warmed instances)
- Reduced cloud infrastructure costs
- Better resource utilization
- Lower total cost of ownership

**Use when:**
- Frequent cluster creation
- Predictable workload patterns
- Need fast start times

### Autoscaling

**Sample Exam Question (From Official Exam Guide):**

**Scenario:** Need to support ad hoc SQL queries for business analysts. Requirements: fast startup, multiple simultaneous users, cost-effective scaling.

**Question:** What cluster configuration should you use?

**Answer:** High-concurrency cluster with autoscaling ✓

**Why High-Concurrency + Autoscaling:**

1. **Multiple Simultaneous Users:**
   - High-concurrency mode shares resources efficiently
   - Supports 10+ concurrent users on same cluster
   - Fair scheduling prevents resource monopolization

2. **Fast Startup:**
   - Cluster remains warm between queries
   - No cold start delays
   - Can combine with cluster pools for even faster startup

3. **Cost-Effective Scaling:**
   - Autoscaling adds workers during peak demand
   - Scales down during idle periods
   - Pay only for utilized capacity

**Configuration:**
```python
{
  "cluster_type": "all-purpose",
  "spark_version": "13.3.x-scala2.12",
  "node_type_id": "i3.xlarge",
  "autoscale": {
    "min_workers": 2,
    "max_workers": 10
  },
  "autotermination_minutes": 30,
  "spark_conf": {
    "spark.databricks.cluster.profile": "serverless"
  }
}
```

**Alternatives (not suitable):**

| Option | Why Not Suitable |
|--------|------------------|
| **Job cluster** | For scheduled ETL only, not ad hoc queries |
| **All-purpose fixed size** | No cost-effective scaling, wastes resources |
| **Single-user cluster** | Cannot support multiple simultaneous users |
| **No autoscaling** | Expensive during low usage periods |

**Best Practices:**
- Set min_workers to handle baseline load
- Set max_workers based on peak demand
- Enable auto-stop (10-30 min) to save costs
- Use cluster pools for faster startup

**Benefits:**
- Scale based on workload
- Avoid over-provisioning
- Optimize DBU spend
- Support concurrent users efficiently

**Cross-Reference:** See [exam-prep.md](exam-prep.md) for full sample question details

## SQL Warehouse Optimization

### Serverless SQL Warehouses

**README Q32, Q33, Q75:**

**Advantages:**
- Instant startup (no cluster provisioning)
- Automatic scaling
- Pay per query (not per hour)
- No infrastructure management

**Cost comparison:**
```
Classic warehouse: Pay for entire runtime
Serverless: Pay only for query execution
```

**Use when:**
- Sporadic query patterns
- Unpredictable workload
- BI/analytics queries
- Manager concerned about costs (Q33)

### Warehouse Auto-Stop

```sql
-- Set in SQL warehouse configuration
auto_stop_mins = 10
```

**README Q77:** Add auto-stop to SQL endpoint

Reduces costs by:
- Stopping idle warehouses
- Avoiding continuous billing
- Automatic restart on query

## DBU Usage Monitoring

**README Q32: Control DBU usage**

### Budget Alerts

```python
# Set budget thresholds
{
  "budget_name": "monthly_budget",
  "amount": 10000,
  "alert_threshold": 80  # Alert at 80%
}
```

### Usage Dashboard

Monitor:
- DBU consumption per workspace
- Cost per job/cluster
- Most expensive queries
- Idle resource time

### Cost Allocation Tags

Tag resources for granular cost tracking:

```python
# Cluster tags
{
  "cluster_name": "production-etl",
  "custom_tags": {
    "team": "data-engineering",
    "project": "customer-analytics",
    "environment": "production",
    "cost-center": "CC-1234",
    "owner": "team-lead@company.com"
  }
}
```

**Tag-Based Reporting:**
```sql
-- Query usage by tag
SELECT tag.team,
       SUM(usage.dbu_count) AS total_dbus,
       SUM(usage.cost_usd) AS total_cost
FROM system.billing.usage usage
JOIN system.compute.clusters clusters ON usage.cluster_id = clusters.cluster_id
GROUP BY tag.team
ORDER BY total_cost DESC;
```

**Benefits:**
- Chargeback to business units
- Cost attribution by project
- Environment-specific budgets
- Identify cost outliers

### Cost Monitoring Best Practices

1. **Set up budget alerts at multiple thresholds**
   - 50% warning
   - 80% critical
   - 100% auto-stop (optional)

2. **Review usage weekly**
   - Top 10 most expensive clusters
   - Idle cluster time
   - Unused resources

3. **Track DBU trends**
   - Month-over-month growth
   - Anomaly detection
   - Forecast future usage

4. **Audit cluster configurations**
   - Right-sizing opportunities
   - Auto-stop settings
   - Spot instance eligibility

**Example Monitoring Query:**
```sql
-- Find most expensive clusters in last 30 days
SELECT cluster_name,
       SUM(dbu_count) AS total_dbus,
       SUM(cost_usd) AS total_cost,
       AVG(cluster_size) AS avg_workers,
       SUM(idle_time_hours) AS wasted_hours
FROM system.billing.usage
WHERE usage_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY cluster_name
ORDER BY total_cost DESC
LIMIT 10;
```

### Query Optimization

```sql
-- Enable adaptive query execution
SET spark.sql.adaptive.enabled = true;

-- Cache frequently accessed data
CACHE TABLE frequent_table;

-- Optimize table layout
OPTIMIZE table_name ZORDER BY (filter_column);
```

**Cross-Reference:** See [Delta Lake](delta-lake.md) for OPTIMIZE and Z-ordering

## Job Optimization

### Job Clusters vs. All-Purpose Clusters

**Job clusters (recommended):**
- 50% cheaper DBU rate
- Terminate after job
- Optimized for workload

**All-purpose clusters:**
- Higher DBU rate
- Interactive use
- Multi-user access

### Spot Instances

```python
{
  "aws_attributes": {
    "first_on_demand": 1,
    "availability": "SPOT_WITH_FALLBACK",
    "spot_bid_price_percent": 100
  }
}
```

**Savings:** Up to 90% on compute costs

**Considerations:**
- Can be interrupted
- Not for SLA-critical jobs
- Good for fault-tolerant workloads

## Storage Optimization

### VACUUM Strategy

```sql
-- Default 7 days
VACUUM table_name RETAIN 168 HOURS;

-- For cost-sensitive scenarios
VACUUM table_name RETAIN 24 HOURS;
```

**Balance:**
- Shorter retention = less storage cost
- Longer retention = more time travel capability

### Table Optimization

```sql
-- Compact small files
OPTIMIZE table_name;

-- Remove deleted data
VACUUM table_name;
```

**Benefit:** Reduced storage costs and improved query performance

## Cost Reduction Checklist

**For managers concerned about costs (README Q33):**

1. ✓ Enable auto-stop on all clusters (10-30 min)
2. ✓ Use serverless SQL warehouses
3. ✓ Convert to job clusters from all-purpose
4. ✓ Enable cluster autoscaling
5. ✓ Use spot instances for non-critical jobs
6. ✓ Implement cluster pools for frequent jobs
7. ✓ Set up budget alerts
8. ✓ Regular VACUUM and OPTIMIZE
9. ✓ Review and delete unused resources
10. ✓ Right-size cluster configurations

## Practice Questions

### Week 2 Study Guide Questions

**Q5: Instance Pool for Startup Time**

Your team complains about long cluster startup times (5-7 minutes) for frequent ad hoc jobs. What feature can reduce startup time to ~30 seconds?

**Answer:** Instance Pool ✓

**Explanation:**
Instance Pools pre-warm idle instances for faster cluster creation:
- **Startup time:** Reduced from 5-7 minutes to ~30 seconds
- **How it works:** Keeps instances ready in idle state
- **Cost benefit:** Lower cloud infrastructure costs
- **Best for:** Frequent cluster creation/deletion patterns

**Configuration:**
```python
{
  "instance_pool_id": "pool-123",
  "min_idle_instances": 2,    # Keep 2 instances warm
  "max_capacity": 10,          # Scale up to 10 total
  "idle_instance_autotermination_minutes": 15
}
```

**Use cases:**
- Job clusters that start/stop frequently
- Interactive development with short sessions
- CI/CD pipelines requiring fast feedback
- Scheduled jobs with tight SLAs

**Cross-Reference:** See cluster pools section earlier for detailed configuration

**Q6: Job Cluster vs All-Purpose Billing**

What is the primary cost difference between job clusters and all-purpose clusters?

**Answer:** Job clusters have ~50% lower DBU rates than all-purpose clusters ✓

**Explanation:**
DBU pricing comparison:
- **Job Cluster:** 0.40 DBU/worker-hour (baseline rate)
- **All-Purpose Cluster:** 0.75 DBU/worker-hour (~2x job cluster)
- **Savings:** Up to 50% on DBU costs for production workloads

**Additional cost benefits of job clusters:**
- Auto-terminate after job completion
- Optimized for specific workload
- No idle time billing
- Better resource utilization

**Example:**
```
Daily 8-hour ETL job with 4 workers:

All-Purpose (always on):
- Runtime: 24 hours × 4 workers = 96 worker-hours
- DBU rate: 0.75 DBU/worker-hour
- Daily cost: 96 × 0.75 = 72 DBUs

Job Cluster (auto-terminate):
- Runtime: 8 hours × 4 workers = 32 worker-hours
- DBU rate: 0.40 DBU/worker-hour
- Daily cost: 32 × 0.40 = 12.8 DBUs

Savings: 82% reduction (72 - 12.8 = 59.2 DBUs/day)
```

**When to use:**
- **Job clusters:** Scheduled ETL, production workflows, automated jobs
- **All-purpose clusters:** Interactive development, notebooks, ad hoc queries

**Q7: Serverless SQL Warehouse for Fast Startup**

Your BI team needs instant query execution without managing infrastructure. Which SQL warehouse type should you use?

**Answer:** Serverless SQL Warehouse ✓

**Explanation:**
Serverless SQL Warehouses provide:
- **Instant startup:** No cluster provisioning delay
- **Auto-scaling:** Automatic capacity adjustments
- **Pay-per-query:** Billed only for query execution time
- **No management:** Zero infrastructure overhead
- **Fast queries:** Optimized with Photon engine

**Cost model:**
```
Classic SQL Warehouse:
- Pay for entire runtime (even if idle)
- Manual start/stop management
- Fixed capacity provisioning

Serverless SQL Warehouse:
- Pay only for query execution
- Automatic instant startup
- Dynamic capacity scaling
```

**Use cases:**
- Sporadic query patterns
- BI dashboards with unpredictable usage
- Ad hoc analytics by business users
- Cost-conscious environments
- Fast startup requirements

**Configuration:**
```python
{
  "warehouse_type": "SERVERLESS",
  "auto_stop_mins": 10,
  "enable_photon": true  # Built-in for serverless
}
```

**Benefits:**
- 2-3x faster than classic warehouses (Photon)
- No idle capacity costs
- Scales to zero when not in use
- Instant availability for users

**Cross-Reference:** See Serverless SQL Warehouses section earlier for detailed comparison

## Common Pitfalls

1. **All-purpose for jobs** - 2x DBU cost
2. **No auto-stop** - Idle cluster costs
3. **Over-provisioned clusters** - Wasted capacity
4. **No spot instances** - Missing 90% savings
5. **Ignoring query optimization** - Inefficient DBU usage

## Exam Tips

- Serverless = cost savings + auto-scaling (Q32, Q33)
- Auto-stop = reduce cluster costs (Q34, Q77)
- Cluster pools = faster start + lower costs (Q45)
- Job clusters cheaper than all-purpose
- Spot instances = up to 90% savings

## Cross-References

- [Delta Lake](delta-lake.md) - OPTIMIZE and VACUUM
- [Workflows](workflows.md) - Job cluster configuration
- [Monitoring](monitoring.md) - Usage tracking

## Sources

- Practice exam Q32, Q33, Q34, Q40, Q75, Q77
- Databricks pricing documentation (pending ingestion)
