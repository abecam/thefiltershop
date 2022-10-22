-- auth_user definition

CREATE TABLE "auth_user"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "username" CHAR(512) UNIQUE,
    "email" CHAR(512) UNIQUE,
    "password" CHAR(512),
    "first_name" CHAR(512),
    "last_name" CHAR(512),
    "sso_id" CHAR(512),
    "action_token" CHAR(512),
    "last_password_change" TIMESTAMP,
    "past_passwords_hash" TEXT
);


-- t_entity definition

CREATE TABLE "t_entity"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_name" CHAR(512),
    "f_type" CHAR(512),
    "f_generalrating" INTEGER,
    "f_ethical_money_rating" INTEGER,
    "f_ethical_moral_rating" INTEGER,
    "f_ethical_marketing_rating" INTEGER,
    "f_ethical_educational_rating" INTEGER,
    "f_cheating_review" INTEGER,
    "f_cheating_ads" INTEGER,
    "f_insulting_ads" INTEGER,
    "f_misleading_ads" INTEGER,
    "f_desc_cheating_ads" CHAR(512),
    "f_desc_insulting_ads" CHAR(512),
    "f_desc_misleading_ads" CHAR(512),
    "f_hidden_full_cost" INTEGER,
    "f_crapometer" INTEGER,
    "f_description" CHAR(512),
    "f_in_hall_of_shame" CHAR(1),
    "created_by" CHAR(512)
);


-- t_publisher definition

CREATE TABLE "t_publisher"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_name" CHAR(512),
    "f_size" INTEGER,
    "f_they_have_made_it" INTEGER,
    "f_money_rating" INTEGER,
    "f_fully_rotten" CHAR(1),
    "f_in_hall_of_shame" CHAR(1),
    "created_by" CHAR(512)
);


-- t_shop definition

CREATE TABLE "t_shop"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_name" CHAR(512),
    "f_description" CHAR(512),
    "f_url" CHAR(512),
    "f_identity" CHAR(512),
    "image" CHAR(512),
    "created_by" CHAR(512)
);


-- t_studiotype definition

CREATE TABLE "t_studiotype"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_name" CHAR(512),
    "f_description" CHAR(512),
    "f_size" INTEGER,
    "created_by" CHAR(512)
);


-- auth_user_tag_groups definition

CREATE TABLE "auth_user_tag_groups"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "path" CHAR(512),
    "record_id" INTEGER REFERENCES "auth_user" ("id") ON DELETE CASCADE  
);


-- t_entity_archive definition

CREATE TABLE "t_entity_archive"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_name" CHAR(512),
    "f_type" CHAR(512),
    "f_generalrating" INTEGER,
    "f_ethical_money_rating" INTEGER,
    "f_ethical_moral_rating" INTEGER,
    "f_ethical_marketing_rating" INTEGER,
    "f_ethical_educational_rating" INTEGER,
    "f_cheating_review" INTEGER,
    "f_cheating_ads" INTEGER,
    "f_insulting_ads" INTEGER,
    "f_misleading_ads" INTEGER,
    "f_desc_cheating_ads" CHAR(512),
    "f_desc_insulting_ads" CHAR(512),
    "f_desc_misleading_ads" CHAR(512),
    "f_hidden_full_cost" INTEGER,
    "f_crapometer" INTEGER,
    "f_description" CHAR(512),
    "f_in_hall_of_shame" CHAR(1),
    "created_by" CHAR(512),
    "current_record" INTEGER REFERENCES "t_entity" ("id") ON DELETE CASCADE  
);


-- t_linkstoshops definition

CREATE TABLE "t_linkstoshops"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_name" CHAR(512),
    "f_description" CHAR(512),
    "f_link" CHAR(512),
    "f_identity" CHAR(512),
    "f_for_entity" INTEGER REFERENCES "t_entity" ("id") ON DELETE CASCADE  ,
    "image" CHAR(512),
    "created_by" CHAR(512)
, "f_in_shop" INTEGER REFERENCES "t_shop" ("id") ON DELETE CASCADE);


-- t_linkstoshops_archive definition

CREATE TABLE "t_linkstoshops_archive"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_name" CHAR(512),
    "f_description" CHAR(512),
    "f_link" CHAR(512),
    "f_identity" CHAR(512),
    "f_for_entity" INTEGER REFERENCES "t_entity" ("id") ON DELETE CASCADE  ,
    "image" CHAR(512),
    "created_by" CHAR(512),
    "current_record" INTEGER REFERENCES "t_linkstoshops" ("id") ON DELETE CASCADE  
, "f_in_shop" INTEGER REFERENCES "t_shop" ("id") ON DELETE CASCADE);


-- t_platform definition

CREATE TABLE "t_platform"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_name" CHAR(512),
    "f_platform" INTEGER REFERENCES "t_platform" ("id") ON DELETE CASCADE  ,
    "created_by" CHAR(512)
);


-- t_platform_archive definition

CREATE TABLE "t_platform_archive"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_name" CHAR(512),
    "f_platform" INTEGER REFERENCES "t_platform" ("id") ON DELETE CASCADE  ,
    "created_by" CHAR(512),
    "current_record" INTEGER REFERENCES "t_platform" ("id") ON DELETE CASCADE  
);


-- t_publisher_archive definition

CREATE TABLE "t_publisher_archive"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_name" CHAR(512),
    "f_size" INTEGER,
    "f_they_have_made_it" INTEGER,
    "f_money_rating" INTEGER,
    "f_fully_rotten" CHAR(1),
    "f_in_hall_of_shame" CHAR(1),
    "created_by" CHAR(512),
    "current_record" INTEGER REFERENCES "t_publisher" ("id") ON DELETE CASCADE  
);


-- t_shop_archive definition

CREATE TABLE "t_shop_archive"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_name" CHAR(512),
    "f_description" CHAR(512),
    "f_url" CHAR(512),
    "f_identity" CHAR(512),
    "image" CHAR(512),
    "created_by" CHAR(512),
    "current_record" INTEGER REFERENCES "t_shop" ("id") ON DELETE CASCADE  
);


-- t_studio definition

CREATE TABLE "t_studio"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_name_of_studio" CHAR(512),
    "f_type_of_studio" INTEGER REFERENCES "t_studiotype" ("id") ON DELETE CASCADE  ,
    "f_they_have_made_it" INTEGER,
    "f_money_rating" INTEGER,
    "f_fully_rotten" CHAR(1),
    "f_in_hall_of_shame" CHAR(1),
    "created_by" CHAR(512)
);


-- t_studio_archive definition

CREATE TABLE "t_studio_archive"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_name_of_studio" CHAR(512),
    "f_type_of_studio" INTEGER REFERENCES "t_studiotype" ("id") ON DELETE CASCADE  ,
    "f_they_have_made_it" INTEGER,
    "f_money_rating" INTEGER,
    "f_fully_rotten" CHAR(1),
    "f_in_hall_of_shame" CHAR(1),
    "created_by" CHAR(512),
    "current_record" INTEGER REFERENCES "t_studio" ("id") ON DELETE CASCADE  
);


-- t_studiotype_archive definition

CREATE TABLE "t_studiotype_archive"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_name" CHAR(512),
    "f_description" CHAR(512),
    "f_size" INTEGER,
    "created_by" CHAR(512),
    "current_record" INTEGER REFERENCES "t_studiotype" ("id") ON DELETE CASCADE  
);


-- t_tags definition

CREATE TABLE "t_tags"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_name" CHAR(512),
    "f_parent_tag" INTEGER REFERENCES "t_tags" ("id") ON DELETE CASCADE  ,
    "f_good_or_bad" INTEGER,
    "created_by" CHAR(512)
);


-- t_tags_parent_child definition

CREATE TABLE "t_tags_parent_child"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_parent_tag" INTEGER REFERENCES "t_tags" ("id") ON DELETE CASCADE  ,
    "f_child_tag" INTEGER REFERENCES "t_tags" ("id") ON DELETE CASCADE  ,
    "created_by" CHAR(512)
);


-- t_videogame_common definition

CREATE TABLE "t_videogame_common"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_game_type" CHAR(512),
    "f_gameplay_rating" INTEGER,
    "f_for_entity" INTEGER REFERENCES "t_entity" ("id") ON DELETE CASCADE  ,
    "f_studio" INTEGER REFERENCES "t_studio" ("id") ON DELETE CASCADE  ,
    "f_studio_size" INTEGER,
    "f_they_have_made_it" INTEGER,
    "created_by" CHAR(512)
);


-- t_videogame_common_archive definition

CREATE TABLE "t_videogame_common_archive"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_game_type" CHAR(512),
    "f_gameplay_rating" INTEGER,
    "f_for_entity" INTEGER REFERENCES "t_entity" ("id") ON DELETE CASCADE  ,
    "f_studio" INTEGER REFERENCES "t_studio" ("id") ON DELETE CASCADE  ,
    "f_studio_size" INTEGER,
    "f_they_have_made_it" INTEGER,
    "created_by" CHAR(512),
    "current_record" INTEGER REFERENCES "t_videogame_common" ("id") ON DELETE CASCADE  
);


-- t_videogame_platform definition

CREATE TABLE "t_videogame_platform"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_for_game" INTEGER REFERENCES "t_videogame_common" ("id") ON DELETE CASCADE  ,
    "t_platform" INTEGER REFERENCES "t_platform" ("id") ON DELETE CASCADE  ,
    "created_by" CHAR(512)
);


-- t_videogame_platform_archive definition

CREATE TABLE "t_videogame_platform_archive"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_for_game" INTEGER REFERENCES "t_videogame_common" ("id") ON DELETE CASCADE  ,
    "t_platform" INTEGER REFERENCES "t_platform" ("id") ON DELETE CASCADE  ,
    "created_by" CHAR(512),
    "current_record" INTEGER REFERENCES "t_videogame_platform" ("id") ON DELETE CASCADE  
);


-- t_videogame_publisher definition

CREATE TABLE "t_videogame_publisher"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_for_game" INTEGER REFERENCES "t_videogame_common" ("id") ON DELETE CASCADE  ,
    "f_publisher" INTEGER REFERENCES "t_publisher" ("id") ON DELETE CASCADE  ,
    "created_by" CHAR(512)
);


-- t_videogame_publisher_archive definition

CREATE TABLE "t_videogame_publisher_archive"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_for_game" INTEGER REFERENCES "t_videogame_common" ("id") ON DELETE CASCADE  ,
    "f_publisher" INTEGER REFERENCES "t_publisher" ("id") ON DELETE CASCADE  ,
    "created_by" CHAR(512),
    "current_record" INTEGER REFERENCES "t_videogame_publisher" ("id") ON DELETE CASCADE  
);


-- t_videogame_rating definition

CREATE TABLE "t_videogame_rating"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_for_videogame" INTEGER REFERENCES "t_videogame_common" ("id") ON DELETE CASCADE  ,
    "f_for_shop" INTEGER REFERENCES "t_shop" ("id") ON DELETE CASCADE  ,
    "f_f2play" CHAR(1),
    "f_f2pay" CHAR(1),
    "f_gameplay_rating" INTEGER,
    "f_money_rating" INTEGER,
    "f_good_wo_iap" INTEGER,
    "f_good_wo_ads" INTEGER,
    "f_ads_supported" INTEGER,
    "f_fully_rotten" CHAR(1),
    "f_type_of_studio" INTEGER REFERENCES "t_studiotype" ("id") ON DELETE CASCADE  ,
    "f_name_of_studio" CHAR(512),
    "f_would_be_good_if" CHAR(512),
    "f_could_be_good_if" CHAR(512),
    "f_use_psycho_tech" INTEGER,
    "f_they_have_made_it" INTEGER,
    "f_platform" CHAR(512),
    "created_by" CHAR(512)
);


-- t_videogame_rating_archive definition

CREATE TABLE "t_videogame_rating_archive"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_for_videogame" INTEGER REFERENCES "t_videogame_common" ("id") ON DELETE CASCADE  ,
    "f_for_shop" INTEGER REFERENCES "t_shop" ("id") ON DELETE CASCADE  ,
    "f_f2play" CHAR(1),
    "f_f2pay" CHAR(1),
    "f_gameplay_rating" INTEGER,
    "f_money_rating" INTEGER,
    "f_good_wo_iap" INTEGER,
    "f_good_wo_ads" INTEGER,
    "f_ads_supported" INTEGER,
    "f_fully_rotten" CHAR(1),
    "f_type_of_studio" INTEGER REFERENCES "t_studiotype" ("id") ON DELETE CASCADE  ,
    "f_name_of_studio" CHAR(512),
    "f_would_be_good_if" CHAR(512),
    "f_could_be_good_if" CHAR(512),
    "f_use_psycho_tech" INTEGER,
    "f_they_have_made_it" INTEGER,
    "f_platform" CHAR(512),
    "created_by" CHAR(512),
    "current_record" INTEGER REFERENCES "t_videogame_rating" ("id") ON DELETE CASCADE  
);


-- t_videogame_studio definition

CREATE TABLE "t_videogame_studio"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_for_game" INTEGER REFERENCES "t_videogame_common" ("id") ON DELETE CASCADE  ,
    "f_studio" INTEGER REFERENCES "t_studio" ("id") ON DELETE CASCADE  ,
    "created_by" CHAR(512)
);


-- t_videogame_studio_archive definition

CREATE TABLE "t_videogame_studio_archive"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_for_game" INTEGER REFERENCES "t_videogame_common" ("id") ON DELETE CASCADE  ,
    "f_studio" INTEGER REFERENCES "t_studio" ("id") ON DELETE CASCADE  ,
    "created_by" CHAR(512),
    "current_record" INTEGER REFERENCES "t_videogame_studio" ("id") ON DELETE CASCADE  
);


-- t_game_tags definition

CREATE TABLE "t_game_tags"(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "f_game" INTEGER REFERENCES "t_videogame_common" ("id") ON DELETE CASCADE  ,
    "f_tag" INTEGER REFERENCES "t_tags" ("id") ON DELETE CASCADE  ,
    "created_by" CHAR(512)
);