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
# 前端

借助[此处](https://github.com/shimh-develop/blog-vue-springboot)写好的`Vue`页面。
[预览地址](http://shiminghui.top:8000/)

# 后端
## bugs:
- [x] 首页摘要信息获取错误
- [ ] 点击页内锚点，跳转到文章分类页面，应该在本页面内跳转。
- [ ] 更新文章，对原有标签删除时，不成功，但新加正常。
- [ ] token超时时弹出很多message,应该使用更友好的方式！！！或者说精准提示，一次只提示一条即可

## TODO:

- [x] 概览页（index）显示
- [x] 文章阅读计数
- [x] 添加获取用户信息API
- [x] 博客自己修改  
  view页面需要summary,因为在编辑时，摘要不能消失  
  编辑时需要对新的和旧的标签对比，正常不走add逻辑  
  编辑时应该是post请求，将用户提交的全量更新，没有的置空
- [ ] 博客作者自己删除
- [ ] 标签管理员手动添加
- [ ] 分类管理员手动添加
- [ ] 标签云
---
优先级中等
- [ ] 管理员账户
- [ ] i18n（en&zh）

---
优先级低

- [ ] 移动端，这个之后再做
