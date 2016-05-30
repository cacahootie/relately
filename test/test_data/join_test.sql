
--
-- Name: join_test; Type: SCHEMA; Schema: -;
-- this is the postgresql example for joins
-- https://www.postgresql.org/docs/current/static/queries-table-expressions.html
--

CREATE SCHEMA join_test;

--
-- Name: t1; Type: TABLE; Schema: join_test; Tablespace: 
--

CREATE TABLE t1 (
    num integer,
    name text
);

--
-- Name: t2; Type: TABLE; Schema: join_test; Tablespace: 
--

CREATE TABLE t2 (
    num integer,
    value text
);

--
-- Data for Name: t1; Type: TABLE DATA; Schema: join_test;
--

COPY t1 (num, name) FROM stdin;
1	a
2	b
3	c
\.


--
-- Data for Name: t2; Type: TABLE DATA; Schema: join_test;
--

COPY t2 (num, value) FROM stdin;
1	xxx
3	yyy
5	zzz
\.


--
-- PostgreSQL database dump complete
--
