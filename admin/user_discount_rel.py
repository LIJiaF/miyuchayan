import json
from datetime import datetime

from tornado.web import RequestHandler

from common.wrapper_func import is_login_func
from common.log_print import logger
from common.postgresql_conn import Postgres


class AdminUserDiscountRelHandler(RequestHandler):
    @is_login_func
    def get(self):
        cur_page = self.get_argument('cur_page', '1')
        search_val = self.get_argument('search_val', '')
        user_id = self.get_argument('user_id', '')

        if user_id:
            sql = """
                select 
                    wudr.id,
                    wu.id as user_id,
                    wdt.name as type,
                    wd.discount,
                    wd.rule, 
                    wudr.end_time,
                    wudr.use_time,
                    wudr.state
                from wx_user_discount_rel as wudr
                left join wx_user as wu on wu.openid = wudr.openid
                left join wx_discount as wd on wd.id = wudr.discount_id
                left join wx_discount_type as wdt on wdt.id = wd.type_id
                where wu.id = %d
                order by wudr.id desc
            """ % int(user_id)
            conn = Postgres()
            data = conn.fetchall(sql)
            return self.finish(json.dumps(data))

        where = ''
        if search_val:
            where += "where username like '%{}%'".format(search_val)

        page_size = 5

        sql = """
            select (
                    select count(*) 
                    from wx_user
                    """ + where + """
                ) as total, 
                wu.id, username, image_url, count(wudr.id) as discount_count
            from wx_user as wu
            right join wx_user_discount_rel as wudr on wudr.openid =  wu.openid
            """ + where + """
            group by wu.id, username, image_url
            having count(wudr.id) > 0
            order by discount_count desc, wu.id desc
            limit %d offset %d
        """ % (page_size, (int(cur_page) - 1) * page_size)
        conn = Postgres()
        data = conn.fetchall(sql)

        for d in data:
            d['discount_id'] = []

        table_data = {
            'data': data,
            'page_size': page_size,
            'total': data[0]['total'] if data else 0
        }

        return self.finish(table_data)

    @is_login_func
    def put(self):
        id = self.get_argument('id', '0')
        state = self.get_argument('state', 'false')

        use_time = datetime.strftime(datetime.now(), '%Y-%m-%d')

        sql = """
            update wx_user_discount_rel
            set state = %s, use_time = '%s'
            where id = %d
        """ % (state, use_time, int(id))

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
            delete from wx_user_discount_rel
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
