from tornado.web import RequestHandler

from common.wrapper_func import is_login_func
from common.log_print import logger
from common.postgresql_conn import Postgres


class AdminDiscountHandler(RequestHandler):
    @is_login_func
    def get(self):
        cur_page = self.get_argument('cur_page', None)

        limit = ''
        page_size = 0
        if cur_page:
            page_size = 5
            limit += 'limit %d offset %d' % (page_size, (abs(int(cur_page)) - 1) * page_size)

        sql = """
            select (
                select count(*) 
                from wx_discount
              ) as total, 
              wd.id, name, type_id, discount, score, count, rule, state
            from wx_discount as wd
            left join wx_discount_type as wdt on wdt.id = wd.type_id
            order by score desc, id desc
            """ + limit + """
        """
        conn = Postgres()
        data = conn.fetchall(sql)

        optionSql = """
            select id, name
            from wx_discount_type
            order by id
        """
        optionData = conn.fetchall(optionSql)

        total = data[0]['total'] if data else 0
        table_data = {
            'data': data,
            'page_size': page_size or total,
            'total': total,
            'options': optionData
        }

        return self.finish(table_data)

    @is_login_func
    def post(self):
        type_id = self.get_argument('type_id', None)
        discount = self.get_argument('discount', None)
        score = self.get_argument('score', None)
        state = self.get_argument('state', None)
        rule = self.get_argument('rule', None)

        res = {
            'code': 0
        }

        if not type_id:
            res['code'] = -1
            res['msg'] = '优惠券类型不能为空！'
            return self.finish(res)

        sql = """
            insert into wx_discount (type_id, discount, score, state, rule)
            values (%d, '%s', %d, %s, '%s')
        """ % (int(type_id), discount, int(score), state, rule)

        try:
            conn = Postgres()
            conn.execute(sql)
            res['msg'] = '添加成功'
        except Exception as e:
            logger.error('优惠券添加失败：%s' % e)
            res['code'] = -1
            res['msg'] = '添加失败！'
        finally:
            return self.finish(res)

    @is_login_func
    def put(self):
        id = self.get_argument('id', '0')
        type_id = self.get_argument('type_id', '0')
        discount = self.get_argument('discount', '')
        score = self.get_argument('score', '0')
        count = self.get_argument('count', '0')
        rule = self.get_argument('rule', '')
        state = self.get_argument('state', 'false')

        sql = """
            update wx_discount
            set type_id = %d, discount = '%s', score = %d, count = %d, rule = '%s', state = %s
            where id = %d
        """ % (int(type_id), discount, int(score), int(count), rule, state, int(id))

        res = {
            'code': 0
        }

        try:
            conn = Postgres()
            conn.execute(sql)
            res['msg'] = '保存成功！'
        except Exception as e:
            logger.error('优惠券保存失败：%s' % e)
            res['code'] = -1
            res['msg'] = '保存失败！'
        finally:
            return self.finish(res)

    @is_login_func
    def delete(self):
        id = self.get_argument('id', '0')

        sql = """
            delete from wx_discount
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
            logger.error('优惠券删除失败：%s' % e)
            res['code'] = -1
            res['msg'] = '删除失败！'
        finally:
            self.finish(res)
