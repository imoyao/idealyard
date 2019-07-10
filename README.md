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

## TODO:

- [x] 概览页（index）显示
- [x] 文章阅读计数
- [x] 添加获取用户信息API
- [ ] 博客自己修改  
  view页面需要summary,因为在编辑时，摘要不能消失  
  编辑时需要对新的和旧的标签对比，正常不走add逻辑  
  编辑时应该是patch请求，现在没有这个，只有post,所以可能后端逻辑和命名都需要改！
- [ ] 博客作者自己删除
- [ ] 标签管理员手动添加
- [ ] 分类管理员手动添加
- [ ] 首页摘要信息获取错误
- [ ] 标签云
---
优先级中等
- [ ] 管理员账户
- [ ] i18n（en&zh）

---
优先级低

- [ ] 移动端，这个之后再做
