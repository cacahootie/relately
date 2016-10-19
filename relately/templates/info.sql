
SELECT to_json(t) FROM
    (
        SELECT *
        FROM information_schema.columns
        WHERE table_schema = %(schema)s
          AND table_name   = %(view)s
    ) t
