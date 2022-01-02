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

--
-- Name: hg_action_wrapper_type; Type: TYPE; Schema: public; Owner: pi
--

CREATE TYPE public.hg_action_wrapper_type AS ENUM (
    'trigger',
    'normal'
);


ALTER TYPE public.hg_action_wrapper_type OWNER TO pi;

--
-- Name: hg_phase_category; Type: TYPE; Schema: public; Owner: pi
--

CREATE TYPE public.hg_phase_category AS ENUM (
    'bloodbath',
    'day',
    'night',
    'event',
    'status',
    'placement',
    'kills',
    'win',
    'tie'
);


ALTER TYPE public.hg_phase_category OWNER TO pi;

--
-- Name: hg_phase_type; Type: TYPE; Schema: public; Owner: pi
--

CREATE TYPE public.hg_phase_type AS ENUM (
    'action',
    'status',
    'win',
    'place',
    'kills',
    'tie'
);


ALTER TYPE public.hg_phase_type OWNER TO pi;

SET default_tablespace = '';

--
-- Name: hg_action_wrappers; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public.hg_action_wrappers (
    action_wrapper_id integer NOT NULL,
    type public.hg_action_wrapper_type NOT NULL,
    parent_phase_id integer NOT NULL,
    single_action_id integer,
    success_action_ids integer[],
    failure_action_ids integer[],
    trigger_chance real,
    trigger_item smallint,
    trigger_hurt boolean
);


ALTER TABLE public.hg_action_wrappers OWNER TO pi;

--
-- Name: hg_action_wrappers_action_wrapper_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

ALTER TABLE public.hg_action_wrappers ALTER COLUMN action_wrapper_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.hg_action_wrappers_action_wrapper_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: hg_actions; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public.hg_actions (
    action_id integer NOT NULL,
    text character varying(256),
    extra_players smallint NOT NULL,
    kill smallint[],
    credit smallint[],
    give smallint[],
    hurt smallint[],
    heal smallint[]
);


ALTER TABLE public.hg_actions OWNER TO pi;

--
-- Name: hg_actions_action_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

ALTER TABLE public.hg_actions ALTER COLUMN action_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.hg_actions_action_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: hg_current_game_actions; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public.hg_current_game_actions (
    game_action_id integer NOT NULL,
    action_id integer NOT NULL,
    players smallint[] NOT NULL
);


ALTER TABLE public.hg_current_game_actions OWNER TO pi;

--
-- Name: hg_current_game_actions_game_action_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

ALTER TABLE public.hg_current_game_actions ALTER COLUMN game_action_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.hg_current_game_actions_game_action_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: hg_current_game_phases; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public.hg_current_game_phases (
    game_phase_id integer NOT NULL,
    type public.hg_phase_type NOT NULL,
    title character varying NOT NULL,
    description character varying,
    game_action_ids integer[],
    player_statuses smallint[],
    complete boolean DEFAULT false NOT NULL
);


ALTER TABLE public.hg_current_game_phases OWNER TO pi;

--
-- Name: hg_current_game_phases_game_phase_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

ALTER TABLE public.hg_current_game_phases ALTER COLUMN game_phase_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.hg_current_game_phases_game_phase_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: hg_phases; Type: TABLE; Schema: public; Owner: pi
--

CREATE TABLE public.hg_phases (
    phase_id integer NOT NULL,
    type public.hg_phase_type NOT NULL,
    title character varying NOT NULL,
    description character varying,
    category public.hg_phase_category
);


ALTER TABLE public.hg_phases OWNER TO pi;

--
-- Name: hg_phases_phase_id_seq; Type: SEQUENCE; Schema: public; Owner: pi
--

ALTER TABLE public.hg_phases ALTER COLUMN phase_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.hg_phases_phase_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: reminders; Type: TABLE; Schema: public; Owner: Jadi3Pi
--

CREATE TABLE public.reminders (
    id integer NOT NULL,
    user_id bigint NOT NULL,
    reminder_str character varying NOT NULL,
    reminder_date timestamp without time zone NOT NULL
);


ALTER TABLE public.reminders OWNER TO "Jadi3Pi";

--
-- Name: reminder_id_seq; Type: SEQUENCE; Schema: public; Owner: Jadi3Pi
--

ALTER TABLE public.reminders ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.reminder_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: hg_action_wrappers hg_action_wrappers_pkey; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public.hg_action_wrappers
    ADD CONSTRAINT hg_action_wrappers_pkey PRIMARY KEY (action_wrapper_id);


--
-- Name: hg_actions hg_actions_pkey; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public.hg_actions
    ADD CONSTRAINT hg_actions_pkey PRIMARY KEY (action_id);


--
-- Name: hg_current_game_actions hg_current_game_actions_pkey; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public.hg_current_game_actions
    ADD CONSTRAINT hg_current_game_actions_pkey PRIMARY KEY (game_action_id);


--
-- Name: hg_current_game_phases hg_current_game_phases_pkey; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public.hg_current_game_phases
    ADD CONSTRAINT hg_current_game_phases_pkey PRIMARY KEY (game_phase_id);


--
-- Name: hg_phases hg_phases_pkey; Type: CONSTRAINT; Schema: public; Owner: pi
--

ALTER TABLE ONLY public.hg_phases
    ADD CONSTRAINT hg_phases_pkey PRIMARY KEY (phase_id);


--
-- Name: reminders reminder_pkey; Type: CONSTRAINT; Schema: public; Owner: Jadi3Pi
--

ALTER TABLE ONLY public.reminders
    ADD CONSTRAINT reminder_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

