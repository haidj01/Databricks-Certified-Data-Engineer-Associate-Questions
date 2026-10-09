# Unity Catalog

**Category:** Core Technologies
**Last Updated:** 2026-09-09

## Overview

Unity Catalog is Databricks' unified governance solution for data and AI assets, providing centralized access control, auditing, lineage, and data discovery across all workspaces.

## Architecture

### Metastore

Central repository of metadata spanning multiple workspaces.

**Key Features:**
- **One metastore per region** (or per organization)
- **Multi-workspace governance:** Share catalogs across workspaces
- **Cloud storage:** Backed by cloud object storage (S3, ADLS, GCS)
- **Access control:** Centralized permission management
- **Lineage tracking:** Automatic data lineage capture

**Architecture:**
```
Metastore
  ├── Workspace 1
  ├── Workspace 2
  └── Workspace 3
       ↓
  Catalog (main)
    ├── Schema (sales)
    │   ├── Table (orders)
    │   ├── Table (customers)
    │   └── View (revenue_summary)
    └── Schema (marketing)
        └── Table (campaigns)
```

**Cross-Reference:** See [Workspace](workspace.md) for workspace components

## Key Concepts

### Three-Level Namespace

Unity Catalog uses a hierarchical 3-level namespace for organizing data objects:

```
catalog.schema.table
```

**Hierarchy:**

| Level | Description | Example |
|-------|-------------|---------|
| **Metastore** | Top-level container (regional) | `metastore_prod` |
| **Catalog** | Top namespace level | `main`, `dev`, `analytics` |
| **Schema** | Collection of tables/views | `sales`, `marketing`, `hr` |
| **Object** | Data assets | `orders`, `customers`, `revenue_view` |

**Examples:**
```sql
-- Fully qualified table name
SELECT * FROM main.sales.orders;

-- Use catalog/schema
USE CATALOG main;
USE SCHEMA sales;
SELECT * FROM orders;

-- Create catalog hierarchy
CREATE CATALOG IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS analytics.marketing;
CREATE TABLE analytics.marketing.campaigns (...);
```

**Benefits:**
- **Multi-tenancy:** Isolate dev/test/prod environments
- **Organization:** Logical grouping by domain or team
- **Access control:** Fine-grained permissions at each level
- **Discovery:** Clear namespace hierarchy

### Permission Types

#### GRANT USAGE

**When to use (README Q15):**
- Allow users to **see** and **navigate** objects
- Does NOT grant read/write permissions
- Required for accessing child objects

```sql
GRANT USAGE ON CATALOG catalog_name TO user@example.com;
GRANT USAGE ON SCHEMA catalog_name.schema_name TO user@example.com;
```

**Use case:** Let users browse the catalog structure without accessing data.

#### GRANT ALL PRIVILEGES

**When to use (README Q14):**
- Full control over objects
- Includes SELECT, MODIFY, CREATE, DROP
- Typically for administrators or object owners

```sql
GRANT ALL PRIVILEGES ON CATALOG catalog_name TO user@example.com;
GRANT ALL PRIVILEGES ON SCHEMA schema_name TO user@example.com;
```

**Caution:** Very permissive - use sparingly.

#### Privilege Hierarchy

Unity Catalog supports granular permissions at each level:

| Privilege | Allows | Applies To |
|-----------|--------|------------|
| **SELECT** | Read data from tables/views | Tables, Views |
| **MODIFY** | Insert, update, delete data | Tables |
| **CREATE** | Create new objects | Catalogs, Schemas |
| **USAGE** | Access and traverse objects | Catalogs, Schemas |
| **EXECUTE** | Run functions and procedures | Functions |
| **READ_METADATA** | View object metadata | All objects |
| **ALL PRIVILEGES** | All permissions on object | All objects |

**Privilege Inheritance:**
- USAGE on catalog required to access any schema/table within
- USAGE on schema required to access any table within
- Permissions are additive (multiple grants combine)
- DENY always wins (see DENY-wins rule below)

#### DENY-Wins Rule

**Key Concept:** DENY permissions always override GRANT permissions.

```sql
-- Grant read access
GRANT SELECT ON TABLE sensitive_data TO data_scientists;

-- But deny specific user
DENY SELECT ON TABLE sensitive_data TO user@contractor.com;

-- Result: user@contractor.com CANNOT read, even though data_scientists group can
```

**Use Cases:**
- Temporary access revocation without removing from groups
- Contractor restrictions within team
- Compliance requirements for specific users
- Emergency access lockdowns

**Important:** DENY is more restrictive than not granting - explicitly blocks access.

#### Common Permission Patterns

```sql
-- Read-only access (minimum required grants)
GRANT USAGE ON CATALOG catalog_name TO analyst_group;
GRANT USAGE ON SCHEMA catalog_name.schema_name TO analyst_group;
GRANT SELECT ON SCHEMA catalog_name.schema_name TO analyst_group;

-- Full schema access
GRANT USAGE ON CATALOG catalog_name TO engineer_group;
GRANT ALL PRIVILEGES ON SCHEMA catalog_name.schema_name TO engineer_group;

-- Table-level access (more granular)
GRANT USAGE ON CATALOG catalog_name TO marketing_team;
GRANT USAGE ON SCHEMA catalog_name.analytics TO marketing_team;
GRANT SELECT ON TABLE catalog_name.analytics.campaigns TO marketing_team;

-- Deny specific user within group
GRANT SELECT ON SCHEMA catalog_name.finance TO finance_team;
DENY SELECT ON TABLE catalog_name.finance.salaries TO contractor@example.com;
```

### Creating Physical Objects for Team Sharing

**README Q19: Which physical object for 10 tables?**

Create a **SCHEMA** (database):

```sql
CREATE SCHEMA shared_analytics;

-- Then grant access
GRANT USAGE ON CATALOG main TO other_team;
GRANT SELECT ON SCHEMA shared_analytics TO other_team;
```

**Why SCHEMA:**
- Groups related tables logically
- Single permission grant covers all tables
- Easy to discover and navigate
- Better governance than individual table grants

### Marking PII Data

**README Q22:**

Use **COMMENT** during table creation:

```sql
CREATE TABLE customers (
  customer_id INT,
  email STRING,
  ssn STRING
)
COMMENT 'Contains PII: email, SSN';

-- Or add tags
ALTER TABLE customers SET TBLPROPERTIES (
  'contains_pii' = 'true',
  'pii_columns' = 'email,ssn'
);
```

### Getting Database Path

**README Q23:**

```sql
DESCRIBE DATABASE EXTENDED customer360;
```

Returns:
- Database name
- Description
- Location (HDFS/cloud path)
- Owner
- Properties

### Security Features

#### Column Masking

Dynamically mask sensitive data based on user privileges.

```sql
-- Create masking function
CREATE FUNCTION mask_ssn(ssn STRING)
RETURN CASE
  WHEN is_account_group_member('finance_team') THEN ssn
  ELSE 'XXX-XX-XXXX'
END;

-- Apply mask to column
ALTER TABLE customers ALTER COLUMN ssn SET MASK mask_ssn;

-- Result:
-- finance_team sees: 123-45-6789
-- other users see: XXX-XX-XXXX
```

**Use Cases:**
- PII protection (SSN, credit cards)
- Salary data masking
- Healthcare information (HIPAA compliance)
- Financial data redaction

**Built-in Masking Functions:**
```sql
-- Redact entire value
ALTER TABLE users ALTER COLUMN email SET MASK redact;

-- Hash the value
ALTER TABLE users ALTER COLUMN phone SET MASK hash;

-- Show partial data
CREATE FUNCTION mask_email(email STRING)
RETURN CONCAT(LEFT(email, 3), '***@***.com');
```

#### Row-Level Filters

Restrict which rows users can see based on predicates.

```sql
-- Create row filter function
CREATE FUNCTION filter_region(region STRING)
RETURN CASE
  WHEN is_account_group_member('global_managers') THEN TRUE
  WHEN is_account_group_member('us_team') AND region = 'US' THEN TRUE
  WHEN is_account_group_member('eu_team') AND region = 'EU' THEN TRUE
  ELSE FALSE
END;

-- Apply filter to table
ALTER TABLE sales SET ROW FILTER filter_region ON (region);

-- Result:
-- global_managers see all rows
-- us_team sees only US rows
-- eu_team sees only EU rows
```

**Use Cases:**
- Multi-tenant data isolation
- Regional data access control
- Department-specific data views
- Customer data segregation

**Complex Filter Example:**
```sql
CREATE FUNCTION filter_customer_data(customer_id STRING, region STRING)
RETURN
  is_account_group_member('admins') OR
  (is_account_group_member('sales_us') AND region = 'US') OR
  (current_user() = CONCAT(customer_id, '@company.com'));

ALTER TABLE orders SET ROW FILTER filter_customer_data ON (customer_id, region);
```

#### Data Lineage

Automatic tracking of data flow across tables, views, and notebooks.

```sql
-- View lineage via system tables
SELECT * FROM system.access.table_lineage
WHERE table_name = 'customer_analytics';

-- View column lineage
SELECT * FROM system.access.column_lineage
WHERE table_name = 'customer_analytics'
AND column_name = 'email';
```

**Lineage Captures:**
- Source → Target relationships
- Notebook/job that created data
- Timestamp of transformation
- User who executed operation
- Column-level dependencies

**Benefits:**
- Impact analysis (what breaks if I change this table?)
- Compliance auditing
- Data quality troubleshooting
- Understanding data provenance

#### Audit Logs

Track all access and modifications.

```sql
-- Query audit logs
SELECT * FROM system.access.audit
WHERE action_name = 'SELECT'
AND table_name = 'sensitive_customer_data'
AND event_date >= '2026-09-01';

-- Monitor privilege changes
SELECT * FROM system.access.audit
WHERE action_name IN ('GRANT', 'REVOKE', 'DENY')
ORDER BY event_time DESC;
```

**Logged Events:**
- Table reads/writes
- Permission changes
- Schema modifications
- Failed access attempts
- Data exports

### Table Types

#### Managed Tables

Default in Unity Catalog:

```sql
CREATE TABLE table_name (col1 INT, col2 STRING);
```

**Characteristics:**
- Data and metadata managed by Databricks
- DROP TABLE deletes both data and metadata
- Data stored in Unity Catalog storage location
- Recommended for most use cases

**Storage Location:**
```sql
-- Default managed location
CREATE TABLE managed_table (id INT, name STRING);
-- Stored in: /mnt/unity-catalog/<catalog>/<schema>/managed_table/

-- View storage location
DESCRIBE DETAIL managed_table;
```

#### External Tables

```sql
CREATE EXTERNAL TABLE table_name (col1 INT, col2 STRING)
LOCATION 's3://bucket/path/';
```

**README Q20: Delete metadata but keep data:**

External tables allow this:
```sql
DROP TABLE external_table_name;
-- Metadata deleted, data files remain at location
```

**Characteristics:**
- Data owned by external systems
- DROP TABLE removes only metadata
- Data files remain at external location
- Requires cloud storage permissions

**Use Cases:**
- Data owned by external systems
- Shared data across platforms
- Preserve data when dropping table
- Legacy data migration

**Comparison:**

| Feature | Managed Tables | External Tables |
|---------|---------------|-----------------|
| **Data Location** | Unity Catalog storage | User-specified location |
| **DROP TABLE** | Deletes data + metadata | Deletes metadata only |
| **Governance** | Full Unity Catalog control | Requires external permissions |
| **Recommended For** | New tables, full governance | Existing data, shared storage |
| **Performance** | Optimized by Databricks | Depends on external storage |

### Unity Catalog Volumes

Governed storage for unstructured data (files, ML models, images, PDFs).

**README Q7 covered in practice questions section below.**

**Path Format:**
```
/Volumes/catalog/schema/volume_name/path/to/file
```

**Create Volume:**
```sql
CREATE VOLUME IF NOT EXISTS main.ml_artifacts.models
COMMENT 'Trained ML models and artifacts';

-- External volume (data in cloud storage)
CREATE EXTERNAL VOLUME main.data.raw_files
LOCATION 's3://my-bucket/raw-data/'
COMMENT 'External raw file storage';
```

**Access Volumes:**
```python
# Read file from volume
df = spark.read.parquet("/Volumes/main/bronze/raw_files/data.parquet")

# List files in volume
dbutils.fs.ls("/Volumes/main/bronze/raw_files/")

# Copy file to volume
dbutils.fs.cp("local_file.csv", "/Volumes/main/bronze/raw_files/uploaded.csv")
```

**Grant Permissions:**
```sql
-- Grant read access
GRANT READ VOLUMES ON VOLUME main.bronze.raw_files TO analysts;

-- Grant write access
GRANT WRITE VOLUMES ON VOLUME main.bronze.raw_files TO data_engineers;

-- Grant all permissions
GRANT ALL PRIVILEGES ON VOLUME main.ml_artifacts.models TO ml_team;
```

**Use Cases:**
- ML model storage and versioning
- Unstructured file storage (PDFs, images, audio)
- Data lake file management with governance
- Cross-workspace file sharing
- Log file storage with access control

**Cross-Reference:** See [Workspace](workspace.md) for DBFS vs Volumes comparison

## External Locations and Storage Credentials

### Overview

External Locations enable Unity Catalog to securely access data in cloud object storage (S3, ADLS, GCS) for external tables and volumes.

**Architecture:**
```
Storage Credential (cloud authentication)
  ↓
External Location (path + credential)
  ↓
External Table / External Volume (data access)
```

**Key Concepts:**
- **Storage Credential:** Contains cloud IAM role/service principal for authentication
- **External Location:** Maps a cloud storage path to a storage credential
- **External Table/Volume:** References external location for data access

### Storage Credentials

Authenticate to cloud storage using IAM roles or service principals.

**AWS Example (IAM Role):**
```sql
CREATE STORAGE CREDENTIAL aws_s3_credential
WITH (AWS_IAM_ROLE = 'arn:aws:iam::123456789012:role/databricks-unity-catalog-role');
```

**Azure Example (Service Principal):**
```sql
CREATE STORAGE CREDENTIAL azure_adls_credential
WITH (
  AZURE_SERVICE_PRINCIPAL_CLIENT_ID = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
  AZURE_SERVICE_PRINCIPAL_CLIENT_SECRET = '<secret>',
  AZURE_TENANT_ID = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
);
```

**GCP Example (Service Account):**
```sql
CREATE STORAGE CREDENTIAL gcp_gcs_credential
WITH (GCP_SERVICE_ACCOUNT_EMAIL = 'databricks@project-id.iam.gserviceaccount.com');
```

**View Storage Credentials:**
```sql
SHOW STORAGE CREDENTIALS;

DESCRIBE STORAGE CREDENTIAL aws_s3_credential;
```

**Security Best Practices:**
- **Use IAM roles (AWS) or managed identities (Azure)** - avoid hardcoded secrets
- **Principle of least privilege** - grant only necessary bucket/container access
- **Rotate credentials regularly** - especially service principal secrets
- **Audit access** - monitor credential usage via audit logs

### External Locations

Map cloud storage paths to storage credentials.

**Create External Location (AWS S3):**
```sql
CREATE EXTERNAL LOCATION s3_raw_data
URL 's3://my-company-data/raw/'
WITH (STORAGE CREDENTIAL aws_s3_credential)
COMMENT 'Raw data landing zone';
```

**Create External Location (Azure ADLS Gen2):**
```sql
CREATE EXTERNAL LOCATION adls_bronze
URL 'abfss://bronze@mystorageaccount.dfs.core.windows.net/'
WITH (STORAGE CREDENTIAL azure_adls_credential)
COMMENT 'Bronze layer data';
```

**Create External Location (GCP GCS):**
```sql
CREATE EXTERNAL LOCATION gcs_landing
URL 'gs://my-company-bucket/landing/'
WITH (STORAGE CREDENTIAL gcp_gcs_credential)
COMMENT 'Landing zone for ingestion';
```

**View External Locations:**
```sql
SHOW EXTERNAL LOCATIONS;

DESCRIBE EXTERNAL LOCATION s3_raw_data;
```

**Grant Access to External Location:**
```sql
-- Allow users to create external tables at this location
GRANT CREATE EXTERNAL TABLE ON EXTERNAL LOCATION s3_raw_data TO data_engineers;

-- Allow users to create external volumes
GRANT CREATE EXTERNAL VOLUME ON EXTERNAL LOCATION s3_raw_data TO data_engineers;

-- Read-only access
GRANT READ FILES ON EXTERNAL LOCATION s3_raw_data TO analysts;

-- Full access
GRANT ALL PRIVILEGES ON EXTERNAL LOCATION s3_raw_data TO admins;
```

### Using External Locations with External Tables

**Create External Table Using External Location:**
```sql
-- Create external table pointing to existing data
CREATE EXTERNAL TABLE sales_external
USING DELTA
LOCATION 's3://my-company-data/raw/sales/'
COMMENT 'External sales data from legacy system';

-- Or use named external location
CREATE EXTERNAL TABLE IF NOT EXISTS customers_external (
  customer_id INT,
  name STRING,
  email STRING
)
LOCATION 's3://my-company-data/raw/customers/';
```

**DROP Behavior:**
```sql
-- Drop external table
DROP TABLE sales_external;
-- Result: Metadata deleted, data files at s3://.../ remain intact
```

**Use Cases for External Tables:**
- **Legacy data:** Existing data in S3/ADLS/GCS that can't be moved
- **Shared data:** Data accessed by multiple systems (Databricks + others)
- **Compliance:** Data must remain in specific storage location
- **Data ownership:** Data owned by external team/system

### Using External Locations with External Volumes

**Create External Volume:**
```sql
-- External volume for ML artifacts
CREATE EXTERNAL VOLUME ml_models
LOCATION 's3://my-company-data/ml-artifacts/'
COMMENT 'ML models shared across teams';
```

**Access External Volume:**
```python
# List files in external volume
dbutils.fs.ls("/Volumes/main/ml_artifacts/ml_models/")

# Read file from external volume
model = mlflow.pyfunc.load_model("/Volumes/main/ml_artifacts/ml_models/model_v1")

# Write file to external volume
dbutils.fs.cp("local_model.pkl", "/Volumes/main/ml_artifacts/ml_models/model_v2.pkl")
```

**External vs Managed Volumes:**

| Feature | Managed Volume | External Volume |
|---------|---------------|-----------------|
| **Storage** | Unity Catalog managed | User-specified cloud path |
| **DROP VOLUME** | Deletes data + metadata | Deletes metadata only |
| **Governance** | Full UC control | Requires external location permissions |
| **Use Case** | New data, full governance | Existing files, shared storage |

### Complete Workflow Example

**Step 1: Create Storage Credential**
```sql
-- Metastore admin creates credential
CREATE STORAGE CREDENTIAL company_s3_role
WITH (AWS_IAM_ROLE = 'arn:aws:iam::123456789012:role/unity-catalog-access');
```

**Step 2: Create External Location**
```sql
-- Map S3 path to credential
CREATE EXTERNAL LOCATION company_raw_data
URL 's3://company-data-lake/raw/'
WITH (STORAGE CREDENTIAL company_s3_role)
COMMENT 'Company raw data landing zone';
```

**Step 3: Grant Permissions**
```sql
-- Allow data engineers to create external tables/volumes
GRANT CREATE EXTERNAL TABLE ON EXTERNAL LOCATION company_raw_data TO data_engineers;
GRANT CREATE EXTERNAL VOLUME ON EXTERNAL LOCATION company_raw_data TO data_engineers;
```

**Step 4: Create External Table**
```sql
-- Data engineer creates external table
CREATE EXTERNAL TABLE raw_sales
LOCATION 's3://company-data-lake/raw/sales/'
COMMENT 'Sales data from legacy ERP system';

-- Verify table
DESCRIBE DETAIL raw_sales;
```

**Step 5: Access Control**
```sql
-- Grant read access to analysts
GRANT USAGE ON CATALOG main TO analysts;
GRANT USAGE ON SCHEMA main.raw TO analysts;
GRANT SELECT ON TABLE main.raw.raw_sales TO analysts;
```

### Cloud-Specific Examples

#### AWS S3 External Location Pattern

```sql
-- IAM role-based credential (recommended)
CREATE STORAGE CREDENTIAL s3_role_credential
WITH (AWS_IAM_ROLE = 'arn:aws:iam::123456789012:role/databricks-uc-s3-access');

-- Create external location for each environment
CREATE EXTERNAL LOCATION s3_dev_bronze
URL 's3://company-dev/bronze/'
WITH (STORAGE CREDENTIAL s3_role_credential);

CREATE EXTERNAL LOCATION s3_prod_bronze
URL 's3://company-prod/bronze/'
WITH (STORAGE CREDENTIAL s3_role_credential);

-- Create external table
CREATE EXTERNAL TABLE dev.bronze.events
LOCATION 's3://company-dev/bronze/events/';
```

**IAM Policy Required:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::company-data-lake/*",
        "arn:aws:s3:::company-data-lake"
      ]
    }
  ]
}
```

#### Azure ADLS Gen2 External Location Pattern

```sql
-- Service principal credential
CREATE STORAGE CREDENTIAL adls_sp_credential
WITH (
  AZURE_SERVICE_PRINCIPAL_CLIENT_ID = '<client-id>',
  AZURE_SERVICE_PRINCIPAL_CLIENT_SECRET = '<secret>',
  AZURE_TENANT_ID = '<tenant-id>'
);

-- External location for ADLS container
CREATE EXTERNAL LOCATION adls_raw_zone
URL 'abfss://raw@companystorage.dfs.core.windows.net/'
WITH (STORAGE CREDENTIAL adls_sp_credential);

-- Create external table
CREATE EXTERNAL TABLE raw.transactions
LOCATION 'abfss://raw@companystorage.dfs.core.windows.net/transactions/';
```

#### GCP GCS External Location Pattern

```sql
-- Service account credential
CREATE STORAGE CREDENTIAL gcs_sa_credential
WITH (GCP_SERVICE_ACCOUNT_EMAIL = 'uc-access@company-project.iam.gserviceaccount.com');

-- External location for GCS bucket
CREATE EXTERNAL LOCATION gcs_data_lake
URL 'gs://company-data-lake/raw/'
WITH (STORAGE CREDENTIAL gcs_sa_credential);

-- Create external table
CREATE EXTERNAL TABLE raw.logs
LOCATION 'gs://company-data-lake/raw/logs/';
```

### External Locations vs Direct Paths

**Without External Location (Not Recommended):**
```sql
-- Direct path - no governance, must configure cluster-level credentials
CREATE EXTERNAL TABLE sales
LOCATION 's3://bucket/path/';
-- Issues: No audit trail, no fine-grained access, credential sprawl
```

**With External Location (Recommended):**
```sql
-- Uses registered external location - full governance
CREATE EXTERNAL TABLE sales
LOCATION 's3://company-data/sales/';
-- External location 's3://company-data/' must be registered first
-- Benefits: Audit logs, access control, credential centralization
```

### Exam Tips

**External Locations Questions:**
- **"How to access S3 data with Unity Catalog?"** → Create Storage Credential + External Location
- **"What's required for external tables?"** → External Location (which references Storage Credential)
- **"Managed vs External Location?"** → Managed for new data (UC storage), External for existing cloud data
- **"What happens when DROP EXTERNAL TABLE?"** → Metadata deleted, data files remain
- **"How to grant access to cloud storage?"** → GRANT on External Location

**Key Differences:**
- **Storage Credential** = authentication (IAM role, service principal)
- **External Location** = path + credential mapping
- **External Table** = metadata + data at external location
- **External Volume** = governed file storage at external location

**Common Patterns:**
- One storage credential per cloud provider/account
- Multiple external locations per environment (dev/test/prod)
- External tables for legacy/shared data
- Managed tables for new UC-governed data

### Security and Compliance

**Best Practices:**

1. **Use instance profiles/managed identities** (not access keys/secrets)
   ```sql
   -- Good: IAM role (no secrets)
   CREATE STORAGE CREDENTIAL s3_role
   WITH (AWS_IAM_ROLE = 'arn:aws:iam::123456789012:role/uc-access');

   -- Avoid: Access keys (hardcoded secrets)
   -- NOT RECOMMENDED: CREATE STORAGE CREDENTIAL ... WITH (AWS_ACCESS_KEY, AWS_SECRET_KEY)
   ```

2. **Principle of least privilege** - only necessary bucket/path access
   ```sql
   -- Separate locations for different data classifications
   CREATE EXTERNAL LOCATION sensitive_data
   URL 's3://company-secure/pii/'
   WITH (STORAGE CREDENTIAL restricted_role);

   GRANT CREATE EXTERNAL TABLE ON EXTERNAL LOCATION sensitive_data TO security_admins;
   -- No public access
   ```

3. **Audit external location access**
   ```sql
   -- Monitor who accesses external data
   SELECT user_identity.email,
          request_params.external_location_name,
          event_time
   FROM system.access.audit
   WHERE action_name = 'createExternalTable'
   ORDER BY event_time DESC;
   ```

4. **Use separate credentials per environment**
   ```sql
   CREATE STORAGE CREDENTIAL dev_s3_role WITH (AWS_IAM_ROLE = '...dev-role');
   CREATE STORAGE CREDENTIAL prod_s3_role WITH (AWS_IAM_ROLE = '...prod-role');
   ```

**Cross-Reference:** See [Security Best Practices](security.md) for credential management (if exists)

## Common Pitfalls

1. **GRANT ALL PRIVILEGES too broadly** - Security risk, violates least privilege principle
2. **Forgetting USAGE grants** - Users can't navigate catalog/schema hierarchy
3. **Wrong object type for sharing** - Use schemas, not individual tables (better governance)
4. **Not documenting PII** - Compliance issues, should use COMMENT or masking
5. **Managed table when need external** - Can't preserve data on DROP
6. **Not using DENY for exceptions** - Removing from groups affects multiple resources
7. **Missing column masking for PII** - Sensitive data exposed to unauthorized users
8. **No row-level filters for multi-tenant** - Data isolation violations
9. **Ignoring audit logs** - Missing compliance requirements
10. **Not checking lineage** - Breaking downstream dependencies

## Practice Questions

### Week 1 Study Guide Questions

**Q7: Unity Catalog Volumes**

You need to store unstructured data files (PDFs, images) with fine-grained access control. What Unity Catalog feature should you use?

**Answer:** Unity Catalog Volumes ✓

**Explanation:**
Unity Catalog Volumes provide governed file storage:
- **Fine-grained ACLs:** Catalog, schema, and volume-level permissions
- **Audit logs:** Track all file access and modifications
- **Cross-workspace:** Share files across workspaces via metastore
- **Unstructured data:** Store any file type (images, PDFs, audio, models)
- **Path format:** `/Volumes/catalog/schema/volume/path`

**Comparison with DBFS:**
```python
# DBFS (legacy - limited governance)
dbfs:/mnt/data/files/

# Unity Catalog Volumes (recommended - full governance)
/Volumes/main/bronze/raw_files/
```

**Example:**
```python
# Create volume
spark.sql("""
  CREATE VOLUME IF NOT EXISTS main.ml_artifacts.models
  COMMENT 'ML model storage'
""")

# Grant access
spark.sql("GRANT READ VOLUMES ON VOLUME main.ml_artifacts.models TO data_scientists")

# Store files
dbutils.fs.cp("local_file.pdf", "/Volumes/main/bronze/documents/file.pdf")
```

**Cross-Reference:** See [Workspace](workspace.md) for detailed DBFS vs Volumes comparison

### Week 2 Study Guide Questions

**Q1: Managed Table DROP Behavior**

What happens when you run `DROP TABLE` on a managed table in Unity Catalog?

**Answer:** Both metadata AND data files are deleted ✓

**Explanation:**
Managed tables in Unity Catalog:
- **Full lifecycle management** by Databricks
- **DROP TABLE** deletes both:
  - Metadata (table definition, schema)
  - Data files (all Parquet files in storage)
- **Storage location:** Unity Catalog managed storage
- **Cannot recover** data after DROP (unless backups exist)
- **Recommended for:** New tables with full governance

**Example:**
```sql
CREATE TABLE customers (id INT, name STRING);
-- Data stored in: /mnt/unity-catalog/main/sales/customers/

DROP TABLE customers;
-- Both metadata and data are deleted
-- Storage location is emptied
```

**Cross-Reference:** See managed vs external tables comparison earlier in this document

**Q2: External Table for Compliance**

Your team needs to drop a table's metadata for reorganization but must preserve the underlying data files for compliance reasons. What table type should you use?

**Answer:** External Table ✓

**Explanation:**
External tables separate metadata from data:
- **DROP TABLE** removes only metadata
- **Data files remain** at external location
- **Use cases:**
  - Compliance requirements (data retention)
  - Shared data across platforms
  - Legacy data migration
  - Data owned by external systems

**Example:**
```sql
-- Create external table
CREATE EXTERNAL TABLE audit_logs (
  timestamp TIMESTAMP,
  user_id STRING,
  action STRING
)
LOCATION 's3://compliance-bucket/audit-logs/';

-- Drop metadata only
DROP TABLE audit_logs;
-- Metadata deleted, but files in s3://compliance-bucket/audit-logs/ remain intact
-- Can recreate table pointing to same location later
```

**Q3: DENY vs GRANT Privilege**

A user is a member of the `data_engineers` group which has SELECT access to a table. You explicitly DENY SELECT to that specific user. What happens?

**Answer:** DENY always wins - the user CANNOT read the table ✓

**Explanation:**
DENY-wins rule in Unity Catalog:
- **DENY overrides all GRANT** permissions
- Applies even if user belongs to groups with access
- Cannot be bypassed by additional grants
- Explicit block of specific permissions

**Use Cases:**
- Temporary access revocation without removing from groups
- Contractor restrictions within team
- Emergency access lockdowns
- Compliance-required exceptions

**Example:**
```sql
-- Group has access
GRANT SELECT ON TABLE sensitive_data TO data_engineers;

-- But specific user is denied
DENY SELECT ON TABLE sensitive_data TO contractor@company.com;

-- Result: contractor@company.com CANNOT read, even though they're in data_engineers group
```

**Q4: Minimum Privileges for SELECT**

What is the minimum set of privileges needed for a user to query `SELECT * FROM main.sales.orders`?

**Answer:** USAGE on catalog `main` + USAGE on schema `sales` + SELECT on table `orders` ✓

**Explanation:**
Privilege hierarchy in Unity Catalog requires grants at each level:

**Required grants:**
```sql
-- 1. Catalog-level USAGE (to traverse)
GRANT USAGE ON CATALOG main TO user@example.com;

-- 2. Schema-level USAGE (to access schema)
GRANT USAGE ON SCHEMA main.sales TO user@example.com;

-- 3. Table-level SELECT (to read data)
GRANT SELECT ON TABLE main.sales.orders TO user@example.com;
```

**Why all three are needed:**
- **USAGE on catalog:** Navigate to catalog (like entering a building)
- **USAGE on schema:** Navigate to schema (like entering a floor)
- **SELECT on table:** Read data from table (like reading a file)

**Common mistake:** Granting only SELECT on table without USAGE on parent objects

**Q8: USE CATALOG and USE SCHEMA Privileges**

A user wants to run `USE CATALOG analytics; USE SCHEMA marketing;` to set their default namespace. What privileges are needed?

**Answer:** USAGE on catalog `analytics` AND USAGE on schema `marketing` ✓

**Explanation:**
USE statements require USAGE privileges:
- **USE CATALOG** requires USAGE on that catalog
- **USE SCHEMA** requires USAGE on that schema
- USAGE allows navigation/traversal but NOT data access
- Separate from SELECT/MODIFY privileges

**Example:**
```sql
-- Grant required privileges
GRANT USAGE ON CATALOG analytics TO analyst@company.com;
GRANT USAGE ON SCHEMA analytics.marketing TO analyst@company.com;

-- Now user can set default namespace
USE CATALOG analytics;
USE SCHEMA marketing;

-- But still need SELECT to query tables
SELECT * FROM campaigns;  -- Fails without SELECT privilege

-- To actually read data
GRANT SELECT ON SCHEMA analytics.marketing TO analyst@company.com;
```

**Privilege separation:**
- **USAGE:** Browse and navigate (see structure)
- **SELECT:** Read data (access content)
- Both needed for full access

## Exam Tips

- USAGE = navigation only (Q15)
- ALL PRIVILEGES = full control (Q14)
- SCHEMA = best for sharing multiple tables (Q19)
- COMMENT = mark PII data (Q22)
- DESCRIBE DATABASE EXTENDED = get path (Q23)
- External table = preserve data on DROP (Q20)
- DENY always wins over GRANT
- Column masking protects PII dynamically
- Row filters enable multi-tenant isolation
- Lineage tracks data flow automatically
- Metastore spans multiple workspaces
- 3-level namespace: catalog.schema.table

## Cross-References

- [Tables and Views](tables-views.md) - Table types details
- [Data Quality](data-quality.md) - PII handling
- [Workflows](workflows.md) - Job permissions

## Sources

- Databricks Unity Catalog documentation (pending ingestion)
- Practice exam questions
