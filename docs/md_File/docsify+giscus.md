
>  非常感谢项目[ruanqizhen/test ](https://github.com/ruanqizhen/test) and [mzlogin:giscus不显示在评论区](https://github.com/mzlogin/blog-comments/discussions/204)
# docsify  + giscus 

## 开启 Discussions

打开github上的相关项目---Setttings---向下滑---勾选Discussions---回到项目界面

![](https://mypic2016.oss-cn-beijing.aliyuncs.com/picGo/202212041627622.png)

## 安装giscus

进入https://github.com/apps/giscus  --- 点击Install --- 选择你的仓库---save

## 配置giscus

1. 进入[giscus.app](https://giscus.app/zh-CN)

2. 在仓库中输入：`xdd1997/docsify`

   ![](https://mypic2016.oss-cn-beijing.aliyuncs.com/picGo/202212041628699.png)

3. 勾选 `Discussion 的标题包含页面的<title>`
2. Discussion 分类选择：`General`
3. 特性中勾选：**将评论框放在评论上方** 与 **懒加载评论**
4. 主题选第一个
5. 获得如下脚本作为参考

```
<script src="https://giscus.app/client.js"
        data-repo="xdd1997/docsify"
        data-repo-id="R_kgDOIg7OMQ"
        data-category="General"
        data-category-id="DIC_kwDOIg7OMc4CSz3W"
        data-mapping="title"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="top"
        data-theme="light"
        data-lang="zh-CN"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>
```



## 嵌入docsify

在index.html中添加

```
plugins: [
      function(hook, vm) {
          hook.beforeEach(function (md) {
            const regex = new RegExp("\"images/", 'ig');
            md = md.replace(regex, "\"docs/images/");
            return md;
          });
          hook.doneEach(function() {     
            const path = vm.route.path === '/' ? '/README' : vm.route.path;
            const path_split = path.split('/');
            const last_item = path_split[path_split.length - 1];
            var dsq = document.createElement('script');
            dsq.type = 'text/javascript';
            dsq.async = true;
            dsq.setAttribute('src', 'https://giscus.app/client.js');
            dsq.setAttribute('data-repo', 'xdd1997/docsify');
            dsq.setAttribute('data-repo-id', 'R_kgDOIg7OMQ');
            dsq.setAttribute('data-category', 'General');
            dsq.setAttribute('data-category-id', 'DIC_kwDOIg7OMc4CSz3W');
            dsq.setAttribute('data-mapping', 'specific');
            dsq.setAttribute('data-term', last_item);
            dsq.setAttribute('data-reactions-enabled', '1');
            dsq.setAttribute('data-emit-metadata', '0');
            dsq.setAttribute('data-theme', 'light');
            dsq.setAttribute('data-lang', 'zh-CN');
            dsq.setAttribute('crossorigin', 'anonymous');
            document.getElementById('main').appendChild(dsq);
          });
        },
      ],
```



## 成功

https://xdd1997.github.io/docsify/#/

