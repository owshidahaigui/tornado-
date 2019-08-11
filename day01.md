# tornado

## 基础流程

### 第一个实例

```Python
#server01.py
#tornado 的基础web模块,
import tornado.web
#tornado的核心io循环模块,封装了linux的epoll，是tornado高效的基础
import tornado.ioloop
#类比Django中的视图
#一个业务处理类
class IndexHandler(tornado.web.RequestHandler):
    #处理get请求，不能处理POST请求
    def get(self,*args,**kwargs):
        #对应http1请求的方法
        #给浏览器响应信息
        self.write('sunck is a good man ')
if __name__=='__main__':
    #实例化一个app对象
    #application ：是tornado web框架的核心应用类,s是与服务器对应的接口
    #里面保存了路由映射表，有一个linsten方法，用了创建一个http服务器的实例并绑定了端口
    app=tornado.web.Application([
            (r'/',IndexHandler)
    ])
    #绑定监听端口
    #注意：此时服务器并没有开启监听
    app.listen(8000)
    '''
    IOLoop.current():返回当前线程的IOLoop实例
    IOLoop.start():启动IOlOOP实例的I/O循环，同时开启监听
    '''
    tornado.ioloop.IOLoop.current().start()
```

## 单进程与多进程

tornado默认启动单进程

- httpServer=tornado.httpserver.HTTPServer(app)
- httpServer.bind(port) 绑定端口
- httpServer.start(num) 启动num个进程，缺省默认为1，值为None,或者小于0，开启对应硬件机器的cpu核心数的进程
- app.listen() 只能在单进程模式中使用
- 多进程 虽然tornado 给我们提供了一次性启动多进程的方式，但是由于一些问题，不建议使用多进程实例的方式启动多进程，而是==手动启动多进程==，还能绑定多个端口
- 为什么不那样启动多进程：
  	1. 每个子进程都会从父进程中辅助一份IOloop的实例，如果在创建子进程前修改了IOloop，会影响所有的子进程
   2. 所有的进程都是由一个命令，无法做到在不停止服务的情况下修改代码
   3. 所有进程共享一个端口，想要分别监控很困难

### 多进程实例

```python
#server03.py
import tornado.web
import tornado.ioloop
import tornado.httpserver
class IndexHandler(tornado.web.RequestHandler):
    def get(self,*args,**kwargs):
        self.write('sunck is a good man ')
if __name__=='__main__':
    app=tornado.web.Application([
            (r'/',IndexHandler)
    ])
    #app.listen(8000) #这个就是默认监听8000借口并且开启服务器1个进程
    httpServer=tornado.httpserver.HTTPServer(app)
    #将服务器绑定到8000端口
    #httpServer.listen(8000)
    httpServer.bind(8000)
    #启动5个进程，缺省默认为1，值为None,或者小于0，开启对应硬件机器的cpu核心数的进程
    httpServer.start(5)
    tornado.ioloop.IOLoop.current().start()
```

## option模块

tornado为我们提供了一个tornado.options 模块
作用：全局参数的定义，存储，转换

#### 基础方法与属性：

  		1. **tornado.options.define()**
       功能：定义option选项变量的方法
       参数：
       
       - name 选项变量名，必须保证其唯一性，否则会报错"Option xxx alredy define in ..."
       - default 设置选项变量的默认值，默认为None
       - type 设置选项的类型,从命令行或者配置文件导入参数时，tornado会根据类型进行转换输入的值，转换不成会报错，可以是str,float，datetime，timedelta，如果没有设置type会根据default的值进行转换，如果没有设置default,就不会进行转换
       - multiple 设置选项变量是否可以为多个值，默认为False
       - help 选项变量的帮助提示信息
       - 实例：
       
       ```python
       #server04.py
       tornado.options.define('port',default=8000,type=int,help="this is a port",metavar=None,multiple=False,group=None,callback=None)
       #常用参数,设置变量为list ，传入列表，列表元素为字符串类型
       tornado.options.define('list',default=[],type=str)
       ```
  
         		2. **tornado.options.options**
功能：全局的options对象，所有定义的选项变量都会作为给对象的属性
       

实例：
       
       ```python
       #server04.py 上面定义的变量 
       httpServer.bind(tornado.options.options.port)
       ```

#### 获取参数的方法

1. **tornado.options.parse_command_line()**

    作用：可以转换命令行参数，

    ```shell
    #server04.py
    import tornado.web
    import tornado.ioloop
    import tornado.httpserver
    import tornado.options
    from tornado.options import options
    #函数的原型
    #定义2个参数
    tornado.options.define('port',default=8000,type=int,help="this is a port",metavar=None,multiple=False,group=None,callback=None)
    #常用参数,设置变量为list ，传入列表，列表元素为字符串类型
    tornado.options.define('list',default=[],type=str,multiple=True)
    class IndexHandler(tornado.web.RequestHandler):
        def get(self,*args,**kwargs):
            self.write('sunck is a good man ')
    if __name__=='__main__':
        #转换命令行参数，并保存到tornado.options.options
        tornado.options.parse_command_line()
        print('list',tornado.options.options.list)
        app=tornado.web.Application([
                (r'/',IndexHandler)
        ])
        httpServer=tornado.httpserver.HTTPServer(app)
        #使用变量的值
        httpServer.bind(tornado.options.options.port)
        httpServer.start(1)
        tornado.ioloop.IOLoop.current().start()
    ```

    命令行启动实例

    ```shell
    (venv) tarena@tarena:~/桌面/tornado/code$ python3 server04.py --port=9000 --list=good,nice,handsome,cool
    ```

2. **tornado.options.parse_config_file(path)**
    功能：从配置文件导入参数
    创建一个名为config的普通文件

    ```python
    '''
    config文件
    port = 7000
    list = ['good','nice','handsome']
    '''
    if __name__=='__main__':
        #转换命令行参数，并保存到tornado.options.options
        tornado.options.parse_config_file('config')
        print('list',tornado.options.options.list)
    ```

    说明：书写格式仍要需要安装python的语法要。

## 导入参数

**最终版，创建config.py的普通文件,直接导入到主文件，不使用option模块**

```python
#config.py
#参数
options={
    'port':8080,
    'list':['good','nice','handsome']
}
```

```python
#sever06.py
import tornado.web
import tornado.ioloop
import tornado.httpserver
import config
class IndexHandler(tornado.web.RequestHandler):
    def get(self,*args,**kwargs):
        self.write('sunck is a good man ')
if __name__=='__main__':
    print('list',config.options['list'])
    app=tornado.web.Application([
            (r'/',IndexHandler)
    ])
    httpServer=tornado.httpserver.HTTPServer(app)
    httpServer.bind(config.options['port'])
    httpServer.start(1)
    tornado.ioloop.IOLoop.current().start()
```

## 日志

当我们在代码中使用parse_command_line()或者parse_config_file(path)方法时，tornado会默认开启logging模块功能，会向我们的终端输出一些打印信息
**关闭日志：**

1. 在主函数的第一行里加入代码

```python
#server05.py
if __name__=='__main__':
   #关闭日志
	tornado.options.options.logging=None
    #转换命令行参数，并保存到tornado.options.options
    tornado.options.parse_config_file('config')
    print('list',tornado.options.options.list)
```

2. 命令行输入

```python
if __name__=='__main__':
    #转换命令行参数，并保存到tornado.options.options
    tornado.options.parse_command_line()
'''
命令行输入(venv) tarena@tarena:~/桌面/tornado/code$ python3 server04.py --port=9000 --list=good,nice,handsome,cool --logging=none
'''
```

# 请求与响应

## tornado 工程模板

![基础工程模块分类](./images/基础工程模块分类.png)

## application文件

作用：URL映射文件
![appliciton文件](./images/appliciton文件.png)

### settings变量

#### **debug**

作用：设置tornado是否工作在调试模式下，默认为False即工作在生产模式下
True特性：

  		1. 自动重启:
       - tornado应用会监控源代码文件，当有保存改动时就重新启动服务器，减少手动启动的次数，提高开发效率.
       - 如果保存后代码有错误，会导致重启失败，修改错误后，需要手动重启
       - 可以通过设置autoreload为True设置

2. 取消缓存编译的模板
    - 通过complied_template_cahe=False单独设置
3. 取消缓存静态文件的hash值
    - 清除css 缓存等静态文件后面的hash值
    - 可以通过static_hash_cahe=False单独设置
4. 提供追踪信息(不用太注意)
    - 可以通过serve_traceback=True设置

#### **static_path**

作用：设置静态文件目录

#### **template_path**

作用：设置模板文件的目录

### 路由

1. 普通路由

```Python
 (r'/',index.IndexHandler)
```

2. 带参数的路由（非客户端传输）
    **重写initialize方法接收传递的参数**

```Python
#application.py 路由参数
(r'/sunck',index.SunckHandler,{'word1':"good",'word2':'nice'})

#index.py ,视图函数重写
class SunckHandler(RequestHandler):
    #该方法会在HTTP方法(get,post)之前调用
    def initialize(self,word1,word2):
        self.word1=word1
        self.word2=word2
    def get(self,*args,**kwargs):
        # print(self.word1,self.word2)
        self.write('sunck is a nice man')
```

3. 反向解析,传参(非客户端传输)

    **同样重写initialize方法接收传递的参数**
    **url= self.reverse_url(name)反向解析获取真实URL**，

```python
#application.py,路由映射
tornado.web.url(r'/kaige',index.KaigeHandler,{'word3':"handsome",'word4':'cool'},name='kaige')

#index.py
#首页返回一个超链接，href使用反向解析名，
class IndexHandler(RequestHandler):
    def get(self,*args,**kwargs):
        #获取name为‘kaige’的路由的正则匹配
        url=self.reverse_url('kaige')
        self.write('<a href="%s">去另一个界面</a>'%url)
```

- 注意：如果使用name反向，不能使用原来的（）路由，需要使用tornado.web.url定义路由

### RequestHandeler(视图函数基类)

#### 1. 利用http协议向服务器传递参数（正则分组取值）

- **提取url的特定部分**

```Python
URL=http://127.0.0.1:8000/liuyifei/sunck/good/nice/
从中提取参数，sunck,good,nice
#application.py
(r'/liuyifei/(\w+)/(\w+)/(\w+)',index.LiuyifeiHandler)

#index.py handler类（视图）
class LiuyifeiHandler(RequestHandler):
    def get(self,h1,h2,h3,*args,**kwargs):
        print(h1,h2,h3,sep='-')
        self.write('liuyifei is a nice women')
```

​	正则分组命名为捕获组,handler类关键字传参

```Python
URL=http://127.0.0.1:8000/liuyifei/sunck/good/nice/
从中提取参数，sunck,good,nice
#application.py
(r'/liuyifei/(？P<p1>\w+)/(？P<p2>\w+)/(？P<p3>\w+)',index.LiuyifeiHandler),

#index.py handler类（视图）
class LiuyifeiHandler(RequestHandler):
    def get(self,p1,p2,p3,*args,**kwargs):
        print(p1,p2,p3,sep='-')
        self.write('liuyifei is a nice women')
```

#### 2. 查询字符串（get方式传递参数）

- **使用函数：name=self.get_query_argument(name,default=ARG_DEFAULT,strip=True)**
  **参数**：

1. **name** 从get请求参数字符串中返回指定参数的值
    - 如果出现多个同名参数，返回最后一个值
2. **default** 设置未传name参数的值，使用default的值
    - 如果default没有设置，那么就会抛出一个tornado.web.MissingArgumentError异常
3. **strip** 表示是否过滤掉两边空白字符，默认为True过滤

实例

```Python
#url:127.0.0.1:9000/?a=1&b=1&c=  1
#application.py
(r'/zhangmanyu',index.ZhangmanyuHandler)
 
#index.py
class ZhangmanyuHandler(RequestHandler):
    def get(self,*args,**kwargs):
        a=self.get_query_argument('a')
        b = self.get_query_argument('b')
        c = self.get_query_argument('c')
        print(a,b,'*'+c+'*')
        self.write('zhangmanyu is good women')
#结果： a b *c*
```

**取一个变量2个值的情况url（172.0.0.1:8000?a=1&a=2）**

- 使用函数：name_list=self.get_query_arguments(name,strip=True)
- 得到一个列表，没有默认值

#### 3. 请求体携带参数(post方式传递参数)

- **在http报文头中增加字段**

- **使用函数：name=self.get_body_argument(name,default=ARG_DEFAULT,strip=True)参数同上**
- **多选(复选框)使用：name_list=self.get_body_arguments(name,strip=True)**
  实例

```html
//postfile.html
<form action="/postfile" method="post">
        姓名：<input type="text" name="username"/>
        <hr/>
        密码：<input type="password" name="passwd"/>
        <hr/>
        爱好：
        <input type="checkbox" value="power" name="hobby">权利
        <input type="checkbox" value="money" name="hobby">金钱
        <input type="checkbox" value="book" name="hobby">书
        <input type="submit" value="登录"/>
    </form>
```

```python
#application.py
(r'/postfile',index.PostFileHandler)

#index.py
class PostFileHandler(RequestHandler):
    def get(self,*args,**kwargs):
        self.render('postfile.html')
    def post(self,*args,**kwargs):
        name=self.get_body_argument('username')
        passwd=self.get_body_argument('passwd')
        hobbyList=self.get_body_arguments('hobby') #取复选框多个
        print(name,passwd,hobbyList)
        self.write('sunck is a handsome man')
#结果：dahaigu jibuzhu555 ['power', 'money']
```

#### 4. 即可以获取get请求，也可以获取post请求

- **使用函数:name=self.get_argument(name,default=ARG_DEFAULT,strip=True)**
- **多选使用:name_list=self.get_arguments(name,strip=True)**
- **注意：一般不会这么使用，无法区分请求方式**

### request对象

**属性参数**：

1. method	http请求的方式
2. host	被请求的主机
3. uri   请求的完整资料地址，包括路径和get查询参数部分
4. path    请求的路径部分
5. query   请求参数部分
6. version   使用的htttp版本
7. headers   请求的协议头，是一个字典类型
8. body    请求体数据，post请求才有
9. remote_ip   客户端的ip
10. files    用户上传的文件，字典类型

- 实例

```Python
#url:	http://127.0.0.1:9000/zhuyin?a=1&b=2
class ZhuyingHandler(RequestHandler):
    def get(self,*args,**kwargs):
        print('method',self.request.method)
        print('host',self.request.host)
        print('url',self.request.uri)
        print('path',self.request.path)
        print('query',self.request.query)
        print('version',self.request.version)
        print('headers',self.request.headers)
        print('body',self.request.body)
        print('remote_ip',self.request.remote_ip)
        print('files',self.request.files)
        self.write('zhuyin is a good women')
```

- 输出结果

```txt
method GET
host 127.0.0.1:9000
url /zhuyin?a=1&b=2
path /zhuyin
query a=1&b=2
version HTTP/1.1
headers Host: 127.0.0.1:9000
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9

body b''	#没有post请求
remote_ip 127.0.0.1
files {}	#没有文件上传，具体看下面
	{name1:[tornado.httputil.HTTPfile对象,tornado.httputil.HTTPfile对象],name2:[ tornado.httputil.HTTPfile对象,..]}
	name为前端input表情的name属性名
```

### tornado.httputil.HTTPfile对象(文件上传)

- **作用：是接受到的文件对象**
- **属性：**

1. filename  上传文件的实际名，用于创建本地文件名
2. body  文件的数据实体,将body属性写入文件中保存到本地
3. content_type   文件类型,多用于判断上传文件类型是否正确

实例

```html
//前端输入 upfile.html
<form method="post" action="/upfile" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="file" name="file">
        <input type="file" name='img'>
        <input type="submit" value="上传">
    </form>
```

```python
#application.py	
(r'/upfile',index.UpFileHandler)
```

```python
#index.py
class UpFileHandler(RequestHandler):
    def get(self,*args,**kwargs):
        self.render('upfile.html')
    def post(self,*args,**kwargs):
        filesDict=self.request.files
		print(filesDict)	#打印request.files属性
'''
{
	'file': [	#键值file为input的name值，
		{	#字典value值为一个列表，里面是每个文件的 tornado.httputil.HTTPfile对象
			#每个对象都是有3个属性，'filename','body','content_type'
			'filename': '1.txt', 			
			'body': b'hhahhaa\n', 
			'content_type': 'text/plain'
		}, {
			'filename': '1 2.txt', 'body': b'', 
			'content_type': 'text/plain'
		}	], 
	'img': [
		{
			'filename': '1 3.png', 
			'body': b'', 
			'content_type': 'image/png'
		}
	]
}
'''        #遍历request.file键值
        for inputname in filesDict:
        	#取出相应的文件（tornado.httputil.HTTPfile对象）列表
            fileArr=filesDict[inputname]
            for fileObject in fileArr:
                import os
                import config
                #创建存储路径,可以通过'对象名.属性'的方式取出属性值
                filePath=os.path.join(config.BASE_DIRS,'upfile/'+fileObject.filename)
                #存储到本地
                with open(filePath,'wb') as f:
                    #通过存储body里的数据来把数据存储到本地文件
                    f.write(fileObject.body)
        self.write('ok')
```

## 响应

### write

- **原型：self.write(chunk)**
- **作用：将chunk数据写到输出缓冲区**

**1. cookie：多次连续发送self.write(data)，先存放在客户端缓存中，服务器响应结束，客户端是一次接受全部**

- self.finish()
  1. 刷新缓存区，关闭当次请求通道
  2. 在finish()下面不要再写write，报错：RuntimeError: Cannot write() after finish()

```python
#write
class WriteHandler(RequestHandler):
    def get(self,*args,**kwargs):
        self.write('good')
        self.write('nice')
        self.write('handsome')
        self.write('man')
        self.finish()
        #下面写了报错
        self.write('right')
```

- 浏览器打印结果

```
goodnicehandsomeman
//全部记在一起，self.finish()下面的没有打印，其实服务器已经报错
```

#### 利用write方式写json数据

- 正常写法json

```Python
#application.py
class Json1Handler(RequestHandler):
    def get(self,*args,**kwargs):
        per={
            'name':'sunck',
            'age':18,
            'height':175,
            'weight':70
        }
        import json
        jsonStr=json.dumps(per)
        self.write(jsonStr)
```

- write直接发送json数据

```Python
#application.py
class Json2Handler(RequestHandler):
    def get(self,*args,**kwargs):
        per={
            'name':'sunck',
            'age':18,
            'height':175,
            'weight':70
        }
        self.write(per)
```

- 注意：自己手动序列化json方式Content-Type属性值为text/html.而采用write自动序列化方式，Content-Type属性值为application/json，**推荐使用第二种方法**

### set_header(name,value)

- 作用：手动设置一个名为name，值为value的响应头字段
- 参数：
  1. name:字段名称
  2. value:字段值
- 可以修改一些原来的响应头数据（抓包看不到？？），也可以自定义新的

- 实例

```python
#application.py 用上面write第一个例子
class Json1Handler(RequestHandler):
    def get(self,*args,**kwargs):
        per={
           'name':'sunck','age':18,'height':175,'weight':70
        }
        import json
        jsonStr=json.dumps(per)
        #修改原有属性
        self.set_header('Content-Type','application/json;charset=utf-8')
        #自定义响应头属性
        self.set_header('sunck','hhgood')
        self.write(jsonStr)
```

### set_default_headers()

- 作用：在进入http响应处理（get,post...）方法之前被调用,可以重写改方法来预先设置默认的headers
- 注意：在Http处理方法中使用set_header设置的字段会覆盖set_default_headers()里面的默认字段的值
- 实例

```Python
#application.py
class HeaderHandler(RequestHandler):
    #重写，里面设置在默认响应头适用于整个类，每个http处理方法
    def set_default_headers(self):
        #同样在里面使用self.set_header()方法设置
        self.set_header('Content-Type','text/html;charset=utf-8')
         self.set_header('kaige','nice')
    def get(self,*args,**kwargs):
        #因为http处理方法是后执行，所以这里的设置会覆盖上面的
        self.set_header('kaige','handsome')
        self.write('good nice')
    def post(self,*args,**kwargs):
        pass
```

### self.set_status(status_code,reason=None)

- 作用：为响应设置状态码,可以自定义状态码,或者修改原有状态码的描述
- 参数：
  1. status_code:状态码值：为intl类型，
     - 如果reason的值为None，则状态码必须为正常值(非自定义)，正常值自带reason值，比如404，not found,，不然就报错
  2. reason:描述状态码的词组，string类型

- 实例

```Python
#application.py 	状态码
class StatusCodeHandler(RequestHandler):
    def get(self,*args,**kwargs):
        self.set_status(200,'我是谁，我在哪里')
        self.write('88888888888888888888888888')
```

### 重定向 self.redirect(url)

- 作用：重定向到url
- 实例

```python
#application.py 	重定向
class RedirectHandler(RequestHandler):
    def get(self,*args,**kwargs):
        self.redirect('/')
```

### 响应错误

#### self.send_error(status_code=500,**kwargs)

- 作用：抛出http错误状态码，默认为500，抛出错误后tornado会调用write_error()方法进行处理，并返回给浏览器错误界面,
- 对应django 404 界面，这个方法就是定义错误也没
- 注意：在send_error之后就不要有响应输出了(self.write())
- 实例在下面

#### wirte_error(status_code,**kwargs)

- 作用：用来处理send_error抛出的错误信息（状态码），根据错误状态码，返回相对的响应给浏览器错误界面

```python
#application.py		错误处理
class ErrorHandler(RequestHandler):
    #根据错误
    def write_error(self, status_code, **kwargs):
        if status_code==500:
            code=500
            #返回500界面（自定义）
            self.write('服务器内部错误')
        elif status_code==404:
            code=404
            #返回404界面(自定义)
            self.write('资料不存在')
        self.set_header(status_code)#定义状态码，告知浏览器发生错误
    def get(self,*args,**kwargs):
        #通过flag码来调试错误页面
        flag=self.get_query_argument('flag')
        if flag== '0':
            #执行self.send_error()就跳到self.write_error方法
            self.send_error(500)#50
            0这个参数是自己定义的
            self.write('error')#这段代码永远无法执行
        self.write('you are right')
```