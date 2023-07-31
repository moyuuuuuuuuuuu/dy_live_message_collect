## 抖音直播弹幕抓取助手

##### 本程序分为三种模式

> 三种模式都有一个不可或缺的参数直播间id，文件末尾会讲解如何获取直播间id



###### 采集模式

- collect[c]

此模式下将会采集当前直播间弹幕并将弹幕数据写入redis中存储



###### 导出模式

- export[e]

此模式将会把redis中属于当前直播间的弹幕导出到excel文件中（excel文件与本程序在同目录）

在程序运行前会询问是否同步删除redis中数据 若输入<font color="red">yes</font>则删除redis中属于当前直播间的弹幕数据

否则不会删除

###### 删除模式

- delete [d]

此模式仅用于删除reids中属于当前直播间弹幕数据



### 如何运行

##### python命令运行

```textile
python main.py
```

如图：

- 导出模式

![b1e86a84-9570-43e4-87bc-a6010418c65f](file:///C:/Users/janma/Pictures/Typedown/b1e86a84-9570-43e4-87bc-a6010418c65f.png)

<font color="red">注意：yes为删除远端redis中当前直播间弹幕数据</font>

- 采集模式

![1690812277058.png](http://images.moyuu.top/i/2023/07/31/64c7bf7825367.png)

- 删除模式

![1690812421006.png](http://images.moyuu.top/i/2023/07/31/64c7c007e6ead.png)



##### 打包成exe文件

命令如下：

```shell
pyinstaller -F main.py
```

执行结束后会在本目录下生成<font color="red">build</font>和<font color="red">dist</font>两个目录，dist目录下的<font color="red">main.exe</font>即为本程序 把.env复制到跟main.exe文件同级后打开exe文件即可

命令参考以上



#### 如何获取直播间id

直播间链接如下：

live.douyin.com/<font color="red">123456</font>?xxx=aaa

其中的标红的数字部分即为直播间id
