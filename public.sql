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

 Date: 20/06/2019 23:31:41
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
INSERT INTO "public"."wx_discount" VALUES (1, 1, '5', 88, 89, '满20可用', 't');
INSERT INTO "public"."wx_discount" VALUES (2, 2, '6', 8, 89, '任意消费可用', 't');
INSERT INTO "public"."wx_discount" VALUES (4, 3, '鸡排', 0, 10, '任意消费，可免费兑换鸡排一份', 't');
INSERT INTO "public"."wx_discount" VALUES (3, 3, '奶茶', 0, 10, '任意消费，可免费兑换一杯中杯奶茶', 't');

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
  "date" varchar(20) COLLATE "pg_catalog"."default" DEFAULT 0
)
;

-- ----------------------------
-- Records of wx_user
-- ----------------------------
INSERT INTO "public"."wx_user" VALUES (4, 'oBGCb1GE38DXO03ebeY0MtnfJKmc', '李家富', 'http://thirdwx.qlogo.cn/mmopen/vi_32/Q0EBmjmic8Is2ezTGhysF7JcUjSjnNVOYrCVoOJ6hIBNziaQiaFN76OSIpa7OpdibS3Zp7yzwUUHibdqgVxRpIic6KPA/132', '广东', '广州', 31, '2019-06-20');

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
SELECT setval('"public"."wx_discount_id_seq"', 5, true);
SELECT setval('"public"."wx_discount_type_id_seq"', 4, true);
SELECT setval('"public"."wx_user_discount_rel_id_seq"', 2, true);
SELECT setval('"public"."wx_user_id_seq"', 5, true);

-- ----------------------------
-- Primary Key structure for table wx_discount
-- ----------------------------
ALTER TABLE "public"."wx_discount" ADD CONSTRAINT "wx_discount_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table wx_user
-- ----------------------------
ALTER TABLE "public"."wx_user" ADD CONSTRAINT "wx_user_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table wx_user_discount_rel
-- ----------------------------
ALTER TABLE "public"."wx_user_discount_rel" ADD CONSTRAINT "wx_user_discount_rel_pkey" PRIMARY KEY ("id");
