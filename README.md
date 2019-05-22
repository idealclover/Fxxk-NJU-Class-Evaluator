# 南哪大学课程评估自动化脚本

> 📢教务处NB！

本脚本用来自动进行南哪大学的学期末课程评估

默认选项为全部“优秀”，老师表现“较好”，可在源码中进行更改

本工具仅用来针对**需要默认好评的课程**

请**确保**您其他需要评价的课程已评价完毕

**上课不易，请不要轻易放弃您的权利**

## 使用方法

没啥使用方法，自己去 [这里](https://fuck.idealclover.cn/) 瞅

我们以南大同学的身份保证不会存储你的学号与密码 源码在这自己看

## 部署相关

### Docker

项目已经上传至 DockerHub 可直接通过 Docker 部署

```
docker create --name=fuck --restart=unless-stopped \
-e KEY="项目密钥"  \
-p 对外端口:7577 \
idealclover/fxxk
```

之后访问 ```ip:对外端口``` 进入网站

### Python

项目所用版本为 Python 3

```
git clone https://github.com/idealclover/Fxxk-NJU-Class-Evaluator.git
cd Fxxk-NJU-Class-Evaluator
pip3 install --no-cache-dir -r requirements.txt
touch config.py && echo "secret_key = '项目密钥'" >> config.py
gunicorn app:app -c ./gunicorn.conf.py
```


## 反馈&贡献

欢迎在[issues](https://github.com/idealclover/Fxxk-NJU-Class-Evaluator/issues)区提交bug与反馈

欢迎各种形式的pr >v<

顺便求一波 stars 蟹蟹ww
