# Observability Extension for WarehousePG

The following views are provided by the extension in the `observability` schema.

## Segment Configuration

The `observability.gp_segment_configuration` view shows the `gp_toolkit.gp_segment_configuration` data, sorted by database id.

The `observability.segments_not_in_preferred_role` view shows all segments and mirrors which are not in the preferred order. Ideally this view returns no rows when the database cluster is healthy.

The `observability.gp_segment_configuration_status` view shows the current coordinator and segment configuration. It also shows if segments or mirrors are down or not in sync.

## Logfiles

The `observability.gp_log_system` view returns the `gp_toolkit.gp_log_system`view.

The `observability.gp_log_all_sql_queries` view returns all SQL queries executed in the database.

The following views extract certain parts of the logs:

- `observability.gp_log_severity_debug`: Shows all log messages with severity debug (this view includes all debug levels)
- `observability.gp_log_severity_info`: Shows all log messages with severity info
- `observability.gp_log_severity_notice`: Shows all log messages with severity notice
- `observability.gp_log_severity_warning`: Shows all log messages with severity warning
- `observability.gp_log_severity_error`: Shows all log messages with severity error
- `observability.gp_log_severity_log`: Shows all log messages with severity log
- `observability.gp_log_severity_fatal`: Shows all log messages with severity fatal
- `observability.gp_log_severity_panic`: Shows all log messages with severity panic
- `observability.gp_log_severity_info_higher`: Shows all log messages with severity info and higher
- `observability.gp_log_severity_notice_higher`: Shows all log messages with severity notice and higher
- `observability.gp_log_severity_warning_higher`: Shows all log messages with severity warning and higher
- `observability.gp_log_severity_error_higher`: Shows all log messages with severity error and higher
- `observability.gp_log_severity_log_higher`: Shows all log messages with severity log and higher
- `observability.gp_log_severity_fatal_higher`: Shows all log messages with severity fatal and higher
- `observability.gp_log_last_10_min`: Shows all log messages of the last 10 minutes
- `observability.gp_log_last_30_min`: Shows all log messages of the last 30 minutes
- `observability.gp_log_last_1_hour`: Shows all log messages of the last 1 hour
- `observability.gp_log_last_6_hours`: Shows all log messages of the last 6 hour
- `observability.gp_log_last_12_hours`: Shows all log messages of the last 12 hour
- `observability.gp_log_last_1_day`: Shows all log messages of the last 1 day
- `observability.gp_log_last_1_week`: Shows all log messages of the last 1 week
- `observability.gp_log_last_1_month`: Shows all log messages of the last 1 month

Note: scanning logfiles might take a long time, depending on the amount of logs. Even when limiting to, for example, 10 minutes, the view has to scan all available logs.

## Memory Usage

The `observability.memory_usage` view shows the memory usage for the coordinator and all segments.

Note: the name of the coordinator host is hardcoded as `coordinator`, for both WHPG 6.x and 7.x.

## Ongoing Queries

The `observability.user_queries` view shows all currently ongoing queries in the database.

This view only shows user queries, and excludes the current connection (the one currently executing this view).

The `observability.user_queries_count` view shows the number of ongoing user queries. This view excludes the current connection, and all backend connections.

Note: This is not the number of open connections, which might be higher.

## Load Average

The `observability.loadavg` view shows the average (1 minute, 5 minutes, 15 minutes) load on the coordinator and all segment hosts.

## Disk Space Usage

The `observability.disk_space_usage` view shows the disk usage for all partitions on the coordinator and all segments.

Note: This view excludes logical (like `sys` or `proc`) and temporary (like `tmp`) partitions.

## Database size

The `observability.gp_database_size` view shows the size of all databases in the cluster.
