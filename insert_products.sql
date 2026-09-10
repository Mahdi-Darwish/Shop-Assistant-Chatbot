--
-- PostgreSQL database dump
--

\restrict 3gXqmVlWYat1cxkcKty7d3mH9RbJNbzXVked5dMn1WG3NHwn8whywfJNZt5chov

-- Dumped from database version 18.2
-- Dumped by pg_dump version 18.2 (Postgres.app)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: admin
--

INSERT INTO public.products (id, name, description, price) VALUES (8, 'ice-coffee-latte', 'iced coffee with foam on top', 3.5);
INSERT INTO public.products (id, name, description, price) VALUES (9, 'american-espresso', 'fresh coffee beans', 2.5);
INSERT INTO public.products (id, name, description, price) VALUES (10, 'white-ice-mocha', 'white ice mocha', 4.5);
INSERT INTO public.products (id, name, description, price) VALUES (11, 'cheese-cake', 'fresh strawberry cheesecake', 4.5);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.products_id_seq', 11, true);


--
-- PostgreSQL database dump complete
--

\unrestrict 3gXqmVlWYat1cxkcKty7d3mH9RbJNbzXVked5dMn1WG3NHwn8whywfJNZt5chov

