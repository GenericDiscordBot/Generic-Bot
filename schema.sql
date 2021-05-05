CREATE TABLE guild_configs (
    guild_id bigint NOT NULL,
    prefix text DEFAULT '>>>'::text,
    CONSTRAINT guild_configs_pkey PRIMARY KEY (guild_id)
)
