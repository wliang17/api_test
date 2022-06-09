from loguru import logger
from api.base import Base

#定义一个用户管理的类，实现添加用户，编辑用户，查询用户列表，删除用户的功能,同时该类要继承Base基类，方便调用函数
class UserManager(Base):

    #初始化接口路径
    def __init__(self):
        self.add_user_url=self.get_url("/admin/admin/create")
        self.edit_user_url = self.get_url("/admin/admin/update")
        self.search_user_url = self.get_url("/admin/admin/list?page=1&limit=20&sort=add_time&order=desc")
        self.delete_user_url = self.get_url("/admin/admin/delete")


    #添加用户
    def add_user(self,username,password,**kwargs): #**kwargs任意参数，可以添加任意个参数
        """
        请求的是添加管理员的接口
        :return:添加管理员接口返回的json数据
        """
        user_data={"username":username,"password":password}
        if kwargs:
            logger.info("添加管理员可选参数:",**kwargs)
            user_data.update(**kwargs)
        return self.post(self.add_user_url,user_data)


    #查询用户
    def search_user(self):
        """
                请求的是查询管理员接口
                :return: 返回的是查询管理接口的json数据
                """
        return self.get(self.search_user_url)



    #编辑用户
    def edit_user(self,id,username,password,**kwargs):
        """
                请求的是编辑管理员接口
                :return: 返回的是编辑管理接口的json数据
                """
        user_data = {"id": id, "username": username,"password":password}
        if kwargs:
            logger.info("编辑管理员可选参数", kwargs)
            user_data.update(**kwargs)
        return self.post(self.edit_user_url, user_data)


    #删除用户
    def delete_user(self,id,username,**kwargs):
        """
        请求的是删除管理员接口
        :return: 返回的是删除管理接口的json数据
        """
        user_data={"id":id,"username":username}
        if kwargs:
            logger.info("删除管理员可选参数",kwargs)
            user_data.update(**kwargs)
        return self.post(self.delete_user_url,user_data)
