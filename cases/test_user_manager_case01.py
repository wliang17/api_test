
#主要实现的是用户管理中心的测试用例

import unittest
from api.user_manager import UserManager,Base
from loguru import logger
from data.user_manager_data import UserManagerData
class TestUserManager(unittest.TestCase):

    user_id = 0


    @classmethod
    def setUpClass(cls) -> None:
        cls.user=UserManager()
        # base = Base()  使用添加编辑，查询删除用户等功能时，需要先登录，这里注释掉因为在run case中已经登录了，这里不需要再登录
        # base.login()

        cls.username=UserManagerData.add_user_data.get("username")
        cls.password=UserManagerData.add_user_data.get("password")
        cls.new_username=UserManagerData.add_user_data.get("new_username")
        cls.errno=UserManagerData.add_user_data.get("errno")


    #case1：添加管理员，只输入用户名和密码的情况。测试用例的设计一般先编写一个实际值，然后用断言，让实际值和期望值进行比较
    def test01_add_user(self): #数字编号是为了运行时，按照顺序依次运行，从而符合逻辑

        # 1.初始化添加管理员的数据
        # self.username='wliang01'
        # self.password='123456'
        # slef.user_id=None # 定义一个实例变量id，用于删除模块使用

        #2.调用添加管理员的接口
        actual_result=self.user.add_user(self.username,self.password)
        data = actual_result.get("data") #获取返回的数据中的data字典内容,赋给变量data
        if data: #如果data存在，则更新全局变量user_id，调用时前面需要加类名TestUserManager.user_id
            TestUserManager.user_id=data.get("id")
            # TestUserManager.user_id=self.user_id #全局变量
            logger.info("获取的添加管理员用户id：{}".format(TestUserManager.user_id))

        #3.进行断言
        self.assertEqual(self.errno,actual_result.get('errno')) #断言返回的结果中errno是否为0，为0则成功
        self.assertEqual(self.username,actual_result.get('data').get('username')) #断言添加的用户名与返回的结果中的用户名是否一致

    # case2：编辑管理员，修改的是用户名称
    def test02_edit_username(self):
        # 1.初始化编辑数据
        # 2.请求编辑接口
        actual_result=self.user.edit_user(TestUserManager.user_id,self.new_username,password=123456) #new_username是更改后的用户名
        # 3.断言返回结果
        self.assertEqual(self.errno,actual_result.get("errno"))
        self.assertEqual(self.new_username,actual_result.get("data").get("username"))

    # case3：查询用户列表
    def test03_search_user(self):
        # 1.初始化查询数据
        # 2.请求查询接口
        actual_result=self.user.search_user()
        # 3.断言返回结果
        self.assertEqual(self.errno,actual_result.get("errno"))


    # case4：删除管理员，删除指定id的用户名
    def test04_delete_user(self):
        #1.初始化删除数据
        #2.请求删除接口
        logger.info("这里获取到的user_id是:{}".format(TestUserManager.user_id))
        actual_result=self.user.delete_user(TestUserManager.user_id,self.new_username)
        #3.断言返回结果
        self.assertEqual(self.errno,actual_result.get("errno"))


if __name__ == '__main__':
    unittest.main()