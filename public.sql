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

 Date: 04/07/2019 12:03:17
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
-- Records of admin_user
-- ----------------------------
INSERT INTO "public"."admin_user" VALUES (1, 'root', 'e1639d697b8879db11fbe29e829d4af8');

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
INSERT INTO "public"."wx_discount" VALUES (2, 3, '薯条', 50, 5, '任意消费，可免费兑换一份薯条', 'f');
INSERT INTO "public"."wx_discount" VALUES (1, 3, '奶茶', 50, 3, '任意消费，可免费兑换一杯中杯奶茶', 't');
INSERT INTO "public"."wx_discount" VALUES (3, 1, '5', 35, 5, '满15可用', 't');
INSERT INTO "public"."wx_discount" VALUES (4, 1, '3', 20, 20, '满15可用', 't');
INSERT INTO "public"."wx_discount" VALUES (5, 1, '5', 20, 19, '满20可用', 't');
INSERT INTO "public"."wx_discount" VALUES (6, 2, '9', 0, 77, '任意消费可用', 't');

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
  "sex" int2 DEFAULT 0,
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
-- Records of wx_user
-- ----------------------------
INSERT INTO "public"."wx_user" VALUES (17, 'oBNuy5xfL7gH6ktrwbk4hbg92HX4', '小醉', 0, 'http://thirdwx.qlogo.cn/mmopen/vi_32/2iagtqw7iaHzWF9gOlialESnrQnC3neQiaATuTOku1AXCoEOayibIfUdtmNbCvgZuTpJ38ejGMvqFl9A6uWLkFWWLmQ/132', '陕西', '西安', 0, 0, 'f', '0');
INSERT INTO "public"."wx_user" VALUES (16, 'oBNuy5x7qwUtjCWSYeP-wOW2ubas', '灵子', 2, 'http://thirdwx.qlogo.cn/mmopen/vi_32/At3BwicBsARwaO4dwGicJIsoiaVqYKDBoicRYm2oRuCPTKeW41vV6KvQxrWO9fxZN60TFL51dbDZP5Tibo6gUcO6Swg/132', '广东', '佛山', 45, 45, 't', '2019-06-30');
INSERT INTO "public"."wx_user" VALUES (14, 'oBNuy58i4Pu0ytCrgbDSvP8wK-_0', '离镜的路口总会有选择', 2, 'http://thirdwx.qlogo.cn/mmopen/vi_32/Gnq3dlXliaXe8MaVearbvGmZoTzTEbHWcWIbeFSv8XnfNtzsxhhkEb36gBY0oBWnvLia1VKWibBN04LwEHj5icqPFw/132', '广东', '清远', 0, 0, 'f', '0');
INSERT INTO "public"."wx_user" VALUES (15, 'oBNuy56j9YeMH2EirWPiAd65xUgs', '光', 1, 'http://thirdwx.qlogo.cn/mmopen/vi_32/6Nw457Rs4959kGFys5tgXIVG3lVvJXrnibpRpZQZI2cYIhUsVHmpNcShHRXgEibibhuiadPxz5bhVRaaw29qd24vvA/132', '', '', 35, 55, 'f', '2019-07-02');
INSERT INTO "public"."wx_user" VALUES (20, 'oBNuy5wkOa7OzSDBo6SzCX7wRhZY', 'A 全能的小强', 1, 'http://thirdwx.qlogo.cn/mmopen/vi_32/YtTZqQtNltKz5HyWfPtDZmfBF7cGC8GonqsgozwkohnsibMHGia3OtTHaOC59c1qcJsicOgFMaPqpjzx61n03A51w/132', '广西', '北海', 0, 0, 'f', '0');
INSERT INTO "public"."wx_user" VALUES (13, 'oBNuy542nMcB6HHmvbiRIKDfAM-0', '全', 1, 'http://thirdwx.qlogo.cn/mmopen/vi_32/7cfv6BtbktVnTq9A8Fb7LHtRFwVT5F5h3IxHobPJNPVxc9fLqjlwo6rkbueOZiae5cl4ZJvd3Mnpp5w5qUrZLhg/132', '广东', '清远', 25, 25, 't', '2019-07-03');
INSERT INTO "public"."wx_user" VALUES (18, 'oBNuy59HGQOAPhJwSUU4ojO8EvZ8', '心上人', 0, 'http://thirdwx.qlogo.cn/mmopen/vi_32/BfBAZ7icllg2oe3MB1o4gYjApEfH9Py3xlIbIpIoVqE0F7ztdg06PD0iau7nD19qA09lxDFYricInyyfrSULKvgLw/132', '', '', 5, 5, 'f', '2019-06-30');
INSERT INTO "public"."wx_user" VALUES (19, 'oBNuy5xlfVImm9FCx8pb7Hq4Bw78', '庄子', 0, 'http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLwnntSWmk75FGJyPSCHvFwRjNEpUBgg91jZxlic74dv8oGknRNmfzONc7cibkf28Sh6PmeicuhFTkcA/132', '广东', '珠海', 5, 5, 'f', '2019-07-01');
INSERT INTO "public"."wx_user" VALUES (12, 'oBNuy57qwhveTXWFIrn1n2B5W-k0', '李家富', 1, 'http://thirdwx.qlogo.cn/mmopen/vi_32/YDpmvs7WfVFjHpuOtysoFBxjQib3Gw0Btneh9UDicXVl9CVCqPNuNhfBZedQ0JYaNVlgmVaqYwpfxOYgBQquRP2w/132', '广东', '广州', 300, 80, 't', '2019-07-03');

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
-- Records of wx_user_discount_rel
-- ----------------------------
INSERT INTO "public"."wx_user_discount_rel" VALUES (24, 'oBNuy57qwhveTXWFIrn1n2B5W-k0', 4, '2019-07-06', 't', '2019-06-29');
INSERT INTO "public"."wx_user_discount_rel" VALUES (23, 'oBNuy57qwhveTXWFIrn1n2B5W-k0', 3, '2019-07-06', 't', '2019-06-29');
INSERT INTO "public"."wx_user_discount_rel" VALUES (25, 'oBNuy542nMcB6HHmvbiRIKDfAM-0', 1, '2019-07-06', 'f', NULL);
INSERT INTO "public"."wx_user_discount_rel" VALUES (26, 'oBNuy58i4Pu0ytCrgbDSvP8wK-_0', 1, '2019-07-06', 'f', NULL);
INSERT INTO "public"."wx_user_discount_rel" VALUES (27, 'oBNuy542nMcB6HHmvbiRIKDfAM-0', 6, '2019-07-06', 'f', NULL);
INSERT INTO "public"."wx_user_discount_rel" VALUES (28, 'oBNuy56j9YeMH2EirWPiAd65xUgs', 1, '2019-07-06', 't', '2019-06-29');
INSERT INTO "public"."wx_user_discount_rel" VALUES (30, 'oBNuy5x7qwUtjCWSYeP-wOW2ubas', 1, '2019-07-07', 't', '2019-06-30');
INSERT INTO "public"."wx_user_discount_rel" VALUES (31, 'oBNuy5x7qwUtjCWSYeP-wOW2ubas', 6, '2019-07-07', 't', '2019-06-30');
INSERT INTO "public"."wx_user_discount_rel" VALUES (22, 'oBNuy57qwhveTXWFIrn1n2B5W-k0', 6, '2019-07-05', 't', '2019-06-30');
INSERT INTO "public"."wx_user_discount_rel" VALUES (32, 'oBNuy5xfL7gH6ktrwbk4hbg92HX4', 1, '2019-07-07', 'f', NULL);
INSERT INTO "public"."wx_user_discount_rel" VALUES (33, 'oBNuy59HGQOAPhJwSUU4ojO8EvZ8', 1, '2019-07-07', 'f', NULL);
INSERT INTO "public"."wx_user_discount_rel" VALUES (21, 'oBNuy57qwhveTXWFIrn1n2B5W-k0', 1, '2019-07-05', 't', '2019-07-01');
INSERT INTO "public"."wx_user_discount_rel" VALUES (34, 'oBNuy57qwhveTXWFIrn1n2B5W-k0', 6, '2019-07-08', 'f', NULL);
INSERT INTO "public"."wx_user_discount_rel" VALUES (35, 'oBNuy5xlfVImm9FCx8pb7Hq4Bw78', 1, '2019-07-08', 'f', NULL);
INSERT INTO "public"."wx_user_discount_rel" VALUES (29, 'oBNuy56j9YeMH2EirWPiAd65xUgs', 5, '2019-07-07', 't', '2019-07-02');
INSERT INTO "public"."wx_user_discount_rel" VALUES (36, 'oBNuy5wkOa7OzSDBo6SzCX7wRhZY', 1, '2019-07-10', 'f', NULL);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
SELECT setval('"public"."admin_user_id_seq"', 2, false);
SELECT setval('"public"."wx_discount_id_seq"', 9, true);
SELECT setval('"public"."wx_discount_type_id_seq"', 7, true);
SELECT setval('"public"."wx_user_discount_rel_id_seq"', 38, true);
SELECT setval('"public"."wx_user_id_seq"', 22, true);

-- ----------------------------
-- Primary Key structure for table wx_discount
-- ----------------------------
ALTER TABLE "public"."wx_discount" ADD CONSTRAINT "wx_discount_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table wx_user
-- ----------------------------
ALTER TABLE "public"."wx_user" ADD CONSTRAINT "wx_user_pkey" PRIMARY KEY ("id");
