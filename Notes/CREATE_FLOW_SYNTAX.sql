CREATE FLOW flow_name
AS INSERT INTO target_table BY NAME
SELECT ...
  _metadata.file_name as file_name,
  _metadata.file_modification_time as file_mod_time
FROM read_files("file_path",
format=>'csv|json',
header=>"true")
