1. CREATE DELTA SINK
```commandline
from pyspark import pipelines as pd

dp.create_sink(
name   = 'delta_sink',
format = 'delta'
options ={'tableName'='catalog_name.schema_name.my_sink'}
)
@dp.append_flow(name='my_sink_flow' target='delta_sink')
def delta_flow()
    return spark.readStream.table("any_streaming_table")
```

2. CHANGE PROPERTIES

```commandline
--1. Disable Deletion Vector
ALTER TABLE my_sink
SET TBLPROPERTIES(
    'delta.enableDeletionVector'='false'
);

--2. Enable Iceburg Competibility
ALTER TABLE my_sink
SET TBLPROPERTIES(
    'delta.columnMapping.mode' ='name',
    'delta.enableIceburgCompatV2'='true',
    'delta.universalFormat.enabledFormats'='iceburg'
);

```