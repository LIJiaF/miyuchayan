import json

from tornado.web import RequestHandler

from common.wrapper_func import is_login_func
from common.log_print import logger
from common.postgresql_conn import Postgres


class AdminDiscountTypeHandler(RequestHandler):
    @is_login_func
    def get(self):
        cur_page = self.get_argument('cur_page', '1')

        if cur_page == '0':
            sql = """
                select id, name
                from wx_discount_type
                order by id
            """
            conn = Postgres()
            data = conn.fetchall(sql)
            return self.finish(json.dumps(data))
        else:
            page_size = 5

            sql = """
                select (
                    select count(*) 
                    from wx_discount_type
                  ) as total, 
                  id, type, name
                from wx_discount_type
                order by id desc
                limit %d offset %d
            """ % (page_size, (int(cur_page) - 1) * page_size)
            conn = Postgres()
            data = conn.fetchall(sql)

            table_data = {
                'data': data,
                'page_size': page_size,
                'total': data[0]['total'] if data else 0
            }

            return self.finish(table_data)

    @is_login_func
    def post(self):
        type = self.get_argument('type', None)
        name = self.get_argument('name', None)

        res = {
            'code': 0
        }

        if not type:
            res['code'] = -1
            res['msg'] = '类型不能为空！'
            return self.finish(res)

        if not name:
            res['code'] = -1
            res['msg'] = '名称不能为空！'
            return self.finish(res)

        sql = """
            insert into wx_discount_type (type, name)
            values ('%s', '%s')
        """ % (type, name)

        try:
            conn = Postgres()
            conn.execute(sql)
            res['msg'] = '添加成功'
        except Exception as e:
            logger.error('优惠券类型添加失败：%s' % e)
            res['code'] = -1
            res['msg'] = '添加失败！'
        finally:
            return self.finish(res)

    @is_login_func
    def put(self):
        id = self.get_argument('id', '0')
        type = self.get_argument('type', '')
        name = self.get_argument('name', '')

        sql = """
            update wx_discount_type
            set type = '%s', name = '%s'
            where id = %d
        """ % (type, name, int(id))

        res = {
            'code': 0
        }

        try:
            conn = Postgres()
            conn.execute(sql)
            res['msg'] = '保存成功！'
        except Exception as e:
            logger.error('优惠券类型保存失败：%s' % e)
            res['code'] = -1
            res['msg'] = '保存失败！'
        finally:
            return self.finish(res)

    @is_login_func
    def delete(self):
        id = self.get_argument('id', '0')

        sql = """
            delete from wx_discount_type
            where id = %d
        """ % int(id)

        res = {
            'code': 0
        }

        try:
            conn = Postgres()
            conn.execute(sql)
            res['msg'] = '删除成功！'
        except Exception as e:
            logger.error('优惠券类型删除失败：%s' % e)
            res['code'] = -1
            res['msg'] = '删除失败！'
        finally:
            self.finish(res)
