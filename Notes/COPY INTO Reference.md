1. SQL command that used to various format files to delta table
2. Idempotent means that only process only one time per file.
3. good for scheduled data loading in dataflow job.
```python
table_name = '<catalog>.<schema>.booking_updates_schemaless'
source_data = '/Volumes/<catalog>/<schema>/<volume>/wanderbricks/booking_updates'
source_format = 'JSON'

spark.sql("CREATE TABLE IF NOT EXISTS " + table_name)

spark.sql("COPY INTO " + table_name + \
  " FROM '" + source_data + "'" + \
  " FILEFORMAT = " + source_format + \
  " FORMAT_OPTIONS ('mergeSchema' = 'true', 'multiLine' = 'true')" + \
  " COPY_OPTIONS ('mergeSchema' = 'true')"
)
```
