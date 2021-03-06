
# 作用：主要用于所有接口的公共功能，使用一个基类（父类）。

# 功能1：处理URL
# 功能2：重新封装get方法和post方法
# 功能3：处理头信息（token）
# 功能4：登录

from setting import BASE_URL
from setting import LOGIN_INFO #导入setting里的BASE_URL
import  requests
from loguru import logger
from cacheout import Cache
cache = Cache() #实例化cache对象

class Base():

    #实现url的拼接
    def get_url(self,path,params=None):

    # 返回一个完整的URl
    #     path：接口路径，如 /admin/auth/login
    #     params：查询参数部分，如?page=1&limit=20&sort=add_time&order=desc
    #     return: full_url: http://121.196.13.152:8080/admin/auth/login
        if params:
            full_url = BASE_URL + path + params
            return full_url

        return BASE_URL + path



    #重写get方法
    def get(self,url):
        result=None
        response = requests.get(url,headers=self.get_headers())
        try:

            result=response.json()
            logger.success("请求URL：{}\n请求结果{}:\n".format(url,result))
            return result
        except Exception as e:
            logger.error("请求get方法异常，返回数据为：{}".format(result))


    #重写post方法
    def post(self,url,data):
        # 在原来post方法的基础上，新增日志以及直接返回json格式
        result = None
        response = requests.post(url,json=data,headers=self.get_headers())
        try:
            result = response.json() #获取响应体中的json数据
            logger.success("请求URL：{}\n请求参数:{}\n请求结果{}:\n".format(url,data,result))
            return result
        except Exception as e:
            logger.error("请求post方法异常，返回数据为：{}".format(result))


    #实现所有头信息的处理
    def get_headers(self):
        """
        处理请求头
        :return: 返回的是字典格式的请求头，多是包括了Content-Type，X-Litemall-Admin-Token
        """
        headers = {"Content-Type":"application/json"}
        token = cache.get("token")  #从缓存中获取token
        if token: #r如果token存在，将token放入headers里，否则直接返回headers默认值json
            headers.update({"X-Litemall-Admin-Token":token})
            return headers
        return headers


    #实现登录功能
    def login(self):
        """
        通过调用登录接口获取token的值，将其进行缓存，其他接口使用时直接从缓存中取数
        若没有取到数，再调用登录，再将token的值放在缓存里
        :return:
        """
        login_path="/admin/auth/login"
        login_url=self.get_url(login_path) #拼接登录接口
        result=self.post(login_url,LOGIN_INFO) #请求登录接口，返回了json数据
        try:
            if 0==result.get("errno"):# 设置一个判断条件，如果登录成功，即errno=0，则返回数据里有token
                logger.info("请求登录接口成功")
                token=result.get("data").get("token") #将token从返回结果result里取出来，因为token位于data对应的字典中的字典里所以用两次get
                cache.set("token",token)  #将token的值设置成cache里的缓存值
            else:
                logger.error("登录失败：{}".format(result))
                return None
        except Exception as e:
            logger.error("请求登录接口返回异常，异常数据{}".format(result))
            logger.error("报错信息{}".format(e))

if __name__ == '__main__':
    base=Base()
    # print(base.get_url("/admin/auth/login"))
    # print(base.get_url("/admin/admin/list","page=1&limit=20&sort=add_time&order=desc"))
    login_url=base.get_url("/admin/auth/login")
    login_data={"username":"admin123","password":"admin123"}
    print(base.post(login_url,login_data))
    # url1="http://www.baidu.com"
    #
    # print(base.get(url1))


