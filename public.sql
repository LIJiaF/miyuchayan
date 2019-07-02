/*
 Navicat Premium Data Transfer

 Source Server         : wx
 Source Server Type    : PostgreSQL
 Source Server Version : 100008
 Source Host           : 120.76.56.231:5432
 Source Catalog        : postgres
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 100008
 File Encoding         : 65001

 Date: 02/07/2019 15:02:20
*/


-- ----------------------------
-- Sequence structure for admin_user_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."admin_user_id_seq";
CREATE SEQUENCE "public"."admin_user_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for wx_discount_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."wx_discount_id_seq";
CREATE SEQUENCE "public"."wx_discount_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for wx_discount_type_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."wx_discount_type_id_seq";
CREATE SEQUENCE "public"."wx_discount_type_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for wx_user_discount_rel_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."wx_user_discount_rel_id_seq";
CREATE SEQUENCE "public"."wx_user_discount_rel_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for wx_user_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."wx_user_id_seq";
CREATE SEQUENCE "public"."wx_user_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Table structure for admin_user
-- ----------------------------
DROP TABLE IF EXISTS "public"."admin_user";
CREATE TABLE "public"."admin_user" (
  "id" int4 NOT NULL DEFAULT nextval('admin_user_id_seq'::regclass),
  "username" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "password" varchar(255) COLLATE "pg_catalog"."default" NOT NULL
)
;

-- ----------------------------
-- Table structure for wx_discount
-- ----------------------------
DROP TABLE IF EXISTS "public"."wx_discount";
CREATE TABLE "public"."wx_discount" (
  "id" int4 NOT NULL DEFAULT nextval('wx_discount_id_seq'::regclass),
  "type_id" int2 NOT NULL,
  "discount" varchar(16) COLLATE "pg_catalog"."default" NOT NULL,
  "score" int2 DEFAULT 0,
  "count" int2 DEFAULT 0,
  "rule" varchar(255) COLLATE "pg_catalog"."default",
  "state" bool DEFAULT false
)
;

-- ----------------------------
-- Table structure for wx_discount_type
-- ----------------------------
DROP TABLE IF EXISTS "public"."wx_discount_type";
CREATE TABLE "public"."wx_discount_type" (
  "id" int4 NOT NULL DEFAULT nextval('wx_discount_type_id_seq'::regclass),
  "name" varchar(10) COLLATE "pg_catalog"."default" NOT NULL,
  "type" varchar(15) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Table structure for wx_user
-- ----------------------------
DROP TABLE IF EXISTS "public"."wx_user";
CREATE TABLE "public"."wx_user" (
  "id" int4 NOT NULL DEFAULT nextval('wx_user_id_seq'::regclass),
  "openid" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "username" varchar(80) COLLATE "pg_catalog"."default" NOT NULL,
  "image_url" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "province" varchar(10) COLLATE "pg_catalog"."default",
  "city" varchar(10) COLLATE "pg_catalog"."default",
  "score" int2 DEFAULT 0,
  "experience" int4 DEFAULT 0,
  "is_admin" bool DEFAULT false,
  "date" varchar(20) COLLATE "pg_catalog"."default" DEFAULT 0
)
;

-- ----------------------------
-- Table structure for wx_user_discount_rel
-- ----------------------------
DROP TABLE IF EXISTS "public"."wx_user_discount_rel";
CREATE TABLE "public"."wx_user_discount_rel" (
  "id" int4 NOT NULL DEFAULT nextval('wx_user_discount_rel_id_seq'::regclass),
  "openid" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "discount_id" int2 NOT NULL,
  "end_time" varchar(15) COLLATE "pg_catalog"."default" NOT NULL,
  "state" bool DEFAULT false,
  "use_time" varchar(30) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
SELECT setval('"public"."admin_user_id_seq"', 2, false);
SELECT setval('"public"."wx_discount_id_seq"', 9, true);
SELECT setval('"public"."wx_discount_type_id_seq"', 7, true);
SELECT setval('"public"."wx_user_discount_rel_id_seq"', 28, true);
SELECT setval('"public"."wx_user_id_seq"', 3, true);

-- ----------------------------
-- Primary Key structure for table wx_discount
-- ----------------------------
ALTER TABLE "public"."wx_discount" ADD CONSTRAINT "wx_discount_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table wx_user
-- ----------------------------
ALTER TABLE "public"."wx_user" ADD CONSTRAINT "wx_user_pkey" PRIMARY KEY ("id");
