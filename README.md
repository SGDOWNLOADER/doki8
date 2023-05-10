# doki8

Docker：https://hub.docker.com/repository/docker/jxxghp/nas-tools

## **功能：**

主要用于[心动日剧](http://www.doki8.net/)签到和评论，每日6+3心动豆

## 安装

### 1、Docker

```bash
docker pull miraclemie/doki8:latest
# 输入自己的用户名和密码
docker run -itd --name=doki8 -e USER_NAME='XXX' -e PASSWD='XXX' miraclemie/doki8:latest
```



### 2、本地运行

python3.8版本以上，主要需要用到ddddocr的库，需要本机环境有opencv支持，如发现缺少依赖包需额外安装,建议设置定时任务：

```
git clone -b master https://github.com/SGDOWNLOADER/doki8.git --recurse-submodule 
python3 -m pip install -r requirements.txt
export USER_NAME="XXXX"
export PASSWD="XXXX"
nohup python3 doki8.py & 
```

## 免责声明

1. 本软件仅供学习交流使用，软件本身不提供任何内容，仅作为辅助工具简化用户手工操作，对用户的行为及内容毫不知情，使用本软件产生的任何责任需由使用者本人承担。
2. 本软件代码开源，基于开源代码进行修改，人为去除相关限制导致软件被分发、传播并造成责任事件的，需由代码修改发布者承担全部责任。同时按MIT License开源协议要求，基于此软件代码的所有修改必须开源。
3. 本项目没有在任何地方发布捐赠信息页面，也不会接受任何捐赠，请仔细辨别避免误导。