-- Table: public.encryptionKeys
-- It is used for storing the fileNames along with the encryption keys.


-- DROP TABLE IF EXISTS public."encryptionKeys";

CREATE TABLE IF NOT EXISTS public."encryptionKeys"
(
    "fileName" text COLLATE pg_catalog."default",
    encrypt_key text COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."encryptionKeys"
    OWNER to postgres;
	
-- Table: public.filePermission
-- It is used for storing the fileName , userName and the access level of file/directory.
-- DROP TABLE IF EXISTS public."filePermission";

CREATE TABLE IF NOT EXISTS public."filePermission"
(
    "fileName" text COLLATE pg_catalog."default",
    "userName" text COLLATE pg_catalog."default",
    "Access" text COLLATE pg_catalog."default",
    type text COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."filePermissi	on"
    OWNER to postgres;
	
-- Table: public.loginaddress
-- It is used to store the login information of the users so that we can prevent password jacking attack.

-- DROP TABLE IF EXISTS public.loginaddress;

CREATE TABLE IF NOT EXISTS public.loginaddress
(
    username text COLLATE pg_catalog."default",
    "ipAddress" text COLLATE pg_catalog."default",
    "loginTime" text COLLATE pg_catalog."default",
    "loginInfo" text COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.loginaddress
    OWNER to postgres;
	
-- Table: public.msgTable

-- DROP TABLE IF EXISTS public."msgTable";
-- Was used for storing messages for SQL Injection. However, not used now.

CREATE TABLE IF NOT EXISTS public."msgTable"
(
    message text COLLATE pg_catalog."default",
    message_key text COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."msgTable"
    OWNER to postgres;
	
CREATE TABLE uploadHistory(
   upload_id SERIAL PRIMARY KEY,
   file_ACTION VARCHAR NOT NULL,
   USERNAME VARCHAR NOT NULL,
   FILENAME VARCHAR NOT NULL,
   TIMESTAMP VARCHAR NOT NULL   
);
