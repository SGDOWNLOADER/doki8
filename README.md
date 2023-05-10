# doki8

Docker：https://hub.docker.com/repository/docker/jxxghp/nas-tools

## **功能：**

主要用于心动日剧(http://www.doki8.net/)签到和评论，每日6+3心动豆

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