import json

from tornado.web import RequestHandler

from common.postgresql_conn import Postgres
from common.wrapper_func import is_login_func


class AdminReportHandler(RequestHandler):
    @is_login_func
    def post(self):
        conn = Postgres()
        fans_sql = """
            select 
                (select count(*) from wx_user) as total,
                (select count(*) from wx_user where sex = 1) as man,
                (select count(*) from wx_user where sex = 2) as woman,
                (select count(*) from wx_user where sex = 0) as other
        """
        fans_data = conn.fetchone(fans_sql)
        discount_sql = """
            select
                (select count(*) from wx_user_discount_rel) as total,
                (select count(*) from wx_user_discount_rel where state = true) as use,
                (select count(*) from wx_user_discount_rel where state = false) as un_use;
        """
        discount_data = conn.fetchone(discount_sql)
        experience_sql = """
            select username, experience
            from wx_user
            order by experience desc, id desc
            limit 10;
        """
        experience_data = conn.fetchall(experience_sql)
        score_sql = """
            select username, score
            from wx_user
            order by score desc, id desc
            limit 10;
        """
        score_data = conn.fetchall(score_sql)

        data = {
            'fans': fans_data,
            'discount': discount_data,
            'experience': experience_data,
            'score': score_data
        }

        return self.finish(json.dumps(data))
