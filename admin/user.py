from tornado.web import RequestHandler

from common.wrapper_func import is_login_func
from common.log_print import logger
from common.postgresql_conn import Postgres


class AdminUserHandler(RequestHandler):
    @is_login_func
    def get(self):
        cur_page = self.get_argument('cur_page', '1')
        search_val = self.get_argument('search_val', '')
        filter = self.get_argument('filter', None)

        where = 'where true'
        if search_val:
            where += " and username like '%{}%'".format(search_val)

        if filter and int(filter) == 1:
            where += " and is_admin = true"
        elif filter and int(filter) == 2:
            where += " and is_admin = false"

        page_size = 5

        sql = """
            select (
                select count(*) 
                from wx_user 
                """ + where + """
              ) as total, 
              id, openid, username, sex, image_url, city, score, experience, is_admin
            from wx_user
            """ + where + """
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
    def put(self):
        id = self.get_argument('id', '0')
        score = self.get_argument('score', '0')
        experience = self.get_argument('experience', '0')
        is_admin = self.get_argument('is_admin', 'false')

        sql = """
            update wx_user
            set score = %d, experience = %d, is_admin = %s
            where id = %d
        """ % (int(score), int(experience), is_admin, int(id))

        res = {
            'code': 0
        }

        try:
            conn = Postgres()
            conn.execute(sql)
            res['msg'] = '保存成功！'
        except Exception as e:
            logger.error('用户管理保存失败：%s' % e)
            res['code'] = -1
            res['msg'] = '保存失败！'
        finally:
            return self.finish(res)

    @is_login_func
    def delete(self):
        id = self.get_argument('id', '0')

        sql = """
            delete from wx_user
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
            logger.error('用户管理删除失败：%s' % e)
            res['code'] = -1
            res['msg'] = '删除失败！'
        finally:
            self.finish(res)
