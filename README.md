# IdealYard

使用 `Vue` 和 `Flask` 搭建个人博客
## 前置条件
### Python

3.6+

### MySQL

```bash
mysql  Ver 14.14 Distrib 5.7.26, for linux-glibc2.12 (x86_64) using  EditLine wrapper
```
username：root

password：111111

数据库：`iyblog_dev`
```sql
CREATE DATABASE iyblog_dev CHARSET=UTF8;
```

也可以通过修改配置之后自行定义。

1. 进入当前目录之后，先通过pip安装pipenv管理包
```bash
pip install pipenv [--user]
```
2. 安装Python依赖
```bash
pipenv install 
```
3. 配置环境变量
```bash
cd back
vi .flaskenv
```
4. 配置个人敏感信息
如百度翻译API秘钥，密码等
```bash
vi .env
```



# 前端

借助[此处](https://github.com/shimh-develop/blog-vue-springboot)写好的`Vue`页面。
[预览地址](http://shiminghui.top:8000/)

# 后端
## BUGS:
- [x] 首页摘要信息获取错误
- [x] 概览页（index）显示
- [x] 更新文章，对原有标签删除时，不成功，但新加正常
- [x] 首页点击查看全部进入空白页
- [ ] 编辑文章报错
- [ ] 新建文章报错
- [ ] 首页无限滚动时：Duplicate keys detected: 'xxxx'. This may cause an update error.
- [ ] 点击页内锚点，跳转到文章分类页面，应该在本页面内跳转
- [ ] 访问已删除文章时，不会跳转到首页！
- [ ] token超时时弹出很多message,应该使用更友好的方式！！！或者精准提示，一次只提示一条即可

## TODO:

- [x] 文章阅读计数
- [x] 添加获取用户信息API
- [x] 博客自己修改  
  view页面需要summary,因为在编辑时，摘要不能消失  
  编辑时需要对新的和旧的标签对比，正常不走add逻辑  
  编辑时应该是post请求，将用户提交的全量更新，没有的置空
- [x] 博客作者自己删除
- [ ] slug选项在更新文章时应该是不可见的（url确定之后不可修改！）
- [ ] 链接由id变成数字和slug的组合
- [x] 标签云
~~参考[这里](https://github.com/MikeCoder/hexo-tag-cloud)~~
~~参考[这里](https://juejin.im/post/5c99a0f7e51d454e9b3c3343)~~
~~参考[这里](https://github.com/nobalmohan/vue-tag-cloud)~~
- [x] 本次/上次提交中header样式需要调整！！！
- [ ] 标签管理员手动添加
- [ ] 分类管理员手动添加
---
优先级中等
- [ ] 管理员账户
- [ ] i18n（en&zh）

---
优先级低

- [ ] 移动端自适应，之后再做
