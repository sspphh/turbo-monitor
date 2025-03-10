from dao import base_bao
from entity import user
import time
import threading


class UserDao(base_bao.BaseDao):
    # 单例模式
    __instance = None

    # 初始化锁
    __init_lock = threading.Lock()

    def get_instance(self):
        with UserDao.__init_lock:
            if not self.__instance:
                self.__instance = UserDao()
            return self.__instance

    def add_user(self, _account, _password, _name):
        new_user = user.User(account=_account, password=_password, name=_name,
                             last_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        self.session.add(new_user)
        self.session.commit()

    def query_user(self, _account):
        the_user = self.session.query(user.User).filter(user.User.account == _account).first()
        return the_user

    def update_user_last_time(self, _account):
        the_user = self.query_user(_account)
        the_user.last_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.session.commit()

    def update_user_name(self, _account, _name):
        the_user = self.query_user(_account)
        the_user.name = _name
        self.session.commit()

    def update_user_password(self, _account, _password):
        the_user = self.query_user(_account)
        the_user.password = _password
        self.session.commit()

    def delete_user(self, _account):
        the_user = self.query_user(_account)
        self.session.delete(the_user)
        self.session.commit()


user_dao = UserDao.get_instance()
