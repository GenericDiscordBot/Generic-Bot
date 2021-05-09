CREATE TABLE prefixes (
    guild_id BIGINT NOT NULL,
    prefix TEXT NOT NULL,
    PRIMARY KEY (guild_id, prefix),

    CONSTRAINT guild_id_foreign FOREIGN KEY (guild_id)
        REFERENCES public.guild_configs (guild_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID
);

CREATE TABLE public.guild_configs
(
    guild_id bigint NOT NULL,
    mute_role bigint,
    CONSTRAINT guild_configs_pkey PRIMARY KEY (guild_id)
);
