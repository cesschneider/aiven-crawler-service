-- Table: public.crawler_results

-- DROP TABLE public.crawler_results;

CREATE TABLE public.crawler_results
(
    id integer NOT NULL DEFAULT nextval('crawler_results_id_seq'::regclass),
    url character varying(100) COLLATE pg_catalog."default" NOT NULL,
    state character varying(20) COLLATE pg_catalog."default" NOT NULL,
    status_code integer,
    response_time integer,
    regex character varying(100) COLLATE pg_catalog."default",
    content text COLLATE pg_catalog."default",
    "timestamp" bigint NOT NULL,
    CONSTRAINT result_id_pk PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public.crawler_results
    OWNER to avnadmin;
-- Index: status_code_idx

-- DROP INDEX public.status_code_idx;

CREATE INDEX status_code_idx
    ON public.crawler_results USING btree
    (status_code ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: timestamp_idx

-- DROP INDEX public.timestamp_idx;

CREATE INDEX timestamp_idx
    ON public.crawler_results USING btree
    ("timestamp" ASC NULLS LAST)
    TABLESPACE pg_default;