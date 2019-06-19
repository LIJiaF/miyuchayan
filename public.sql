/*
 Navicat Premium Data Transfer

 Source Server         : wx
 Source Server Type    : PostgreSQL
 Source Server Version : 100008
 Source Host           : localhost:5432
 Source Catalog        : wx
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 100008
 File Encoding         : 65001

 Date: 17/06/2019 22:41:48
*/


-- ----------------------------
-- Table structure for wx_discount
-- ----------------------------
DROP TABLE IF EXISTS "public"."wx_discount";
CREATE TABLE "public"."wx_discount" (
  "id" int4 NOT NULL,
  "code" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "type" varchar(10) COLLATE "pg_catalog"."default" NOT NULL,
  "discount" int2 NOT NULL,
  "score" int2 DEFAULT 0,
  "end_time" varchar(15) COLLATE "pg_catalog"."default",
  "rule" varchar(255) COLLATE "pg_catalog"."default",
  "state" bool DEFAULT false
)
;

-- ----------------------------
-- Table structure for wx_user
-- ----------------------------
DROP TABLE IF EXISTS "public"."wx_user";
CREATE TABLE "public"."wx_user" (
  "id" int4 NOT NULL,
  "openid" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "username" varchar(80) COLLATE "pg_catalog"."default" NOT NULL,
  "image_url" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "province" varchar(10) COLLATE "pg_catalog"."default",
  "city" varchar(10) COLLATE "pg_catalog"."default",
  "score" int2 DEFAULT 0,
  "discount" int2 DEFAULT 0,
  "date" varchar(20) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Primary Key structure for table wx_discount
-- ----------------------------
ALTER TABLE "public"."wx_discount" ADD CONSTRAINT "wx_discount_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table wx_user
-- ----------------------------
ALTER TABLE "public"."wx_user" ADD CONSTRAINT "wx_user_pkey" PRIMARY KEY ("id");
