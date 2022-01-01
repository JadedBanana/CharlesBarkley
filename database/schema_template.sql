--
-- PostgreSQL database dump
--

-- Dumped from database version 11.14 (Raspbian 11.14-0+deb10u1)
-- Dumped by pg_dump version 13.5 (Ubuntu 13.5-0ubuntu0.21.10.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

--
-- Name: reminder; Type: TABLE; Schema: public; Owner: Jadi3Pi
--

CREATE TABLE public.reminder (
    id integer NOT NULL,
    user_id bigint NOT NULL,
    reminder_str character varying NOT NULL,
    reminder_date timestamp without time zone NOT NULL
);


ALTER TABLE public.reminder OWNER TO "Jadi3Pi";

--
-- Name: reminder_id_seq; Type: SEQUENCE; Schema: public; Owner: Jadi3Pi
--

ALTER TABLE public.reminder ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.reminder_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: reminder reminder_pkey; Type: CONSTRAINT; Schema: public; Owner: Jadi3Pi
--

ALTER TABLE ONLY public.reminder
    ADD CONSTRAINT reminder_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

