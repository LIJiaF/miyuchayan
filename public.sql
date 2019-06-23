/*
 Navicat Premium Data Transfer

 Source Server         : wx
 Source Server Type    : PostgreSQL
 Source Server Version : 100008
 Source Host           : 120.76.56.231:5432
 Source Catalog        : wx
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 100008
 File Encoding         : 65001

 Date: 23/06/2019 12:57:33
*/


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
-- Records of wx_discount
-- ----------------------------
INSERT INTO "public"."wx_discount" VALUES (1, 3, '奶茶', 88, 100, '任意消费，可免费兑换一杯中杯奶茶', 'f');
INSERT INTO "public"."wx_discount" VALUES (3, 2, '6', 15, 98, '任意消费可用', 't');
INSERT INTO "public"."wx_discount" VALUES (2, 1, '5', 15, 98, '满15可用', 't');

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
-- Records of wx_discount_type
-- ----------------------------
INSERT INTO "public"."wx_discount_type" VALUES (1, '满减券', 'money');
INSERT INTO "public"."wx_discount_type" VALUES (2, '折扣券', 'discount');
INSERT INTO "public"."wx_discount_type" VALUES (3, '兑换券', 'exchange');

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
  "state" bool DEFAULT false
)
;

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
SELECT setval('"public"."wx_discount_id_seq"', 6, true);
SELECT setval('"public"."wx_discount_type_id_seq"', 5, true);
SELECT setval('"public"."wx_user_discount_rel_id_seq"', 18, true);
SELECT setval('"public"."wx_user_id_seq"', 10, true);

-- ----------------------------
-- Primary Key structure for table wx_discount
-- ----------------------------
ALTER TABLE "public"."wx_discount" ADD CONSTRAINT "wx_discount_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table wx_user
-- ----------------------------
ALTER TABLE "public"."wx_user" ADD CONSTRAINT "wx_user_pkey" PRIMARY KEY ("id");
