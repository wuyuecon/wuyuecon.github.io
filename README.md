# Yu Wu 个人网站：本地修改与上传说明

公开网址：https://wuyuecon.github.io/

本地项目：`E:\Resume\Website\yu-wu-site`。网站有 Home、Working Papers、Publications 三页。

## 最常用的操作

1. 用 VS Code 或记事本打开 `site-data.json`，修改并保存（UTF-8）。
2. 双击 **`Open Website.cmd`**：重新生成网页，并在浏览器打开本地预览。这一步不会上传。
3. 确认内容后，双击 **`Upload Website.cmd`**：重新生成网页、提交并推送至 GitHub。
4. 到仓库的 **Actions → pages build and deployment** 查看结果；任务成功后刷新公开网址。

两个入口需要本机已有的 Python 3.12 或更新版本；上传还需要 Git 和有效的 GitHub 登录。首次登录或登录过期时，按 Git Credential Manager 的提示操作。生成网页不需要安装 Python 第三方包。

**平时修改 `site-data.json`，不要直接修改生成的 HTML**，因为下次生成时会覆盖 HTML。

## 选择显示哪些字段

文件中的这段控制两类论文列表的显示方式：

```json
"paperDisplay": {
  "coauthors": true,
  "dates": false,
  "status": true,
  "abstracts": false
}
```

| 选项 | 控制的内容 | 当前设置 |
|---|---|---|
| `coauthors` | 合作者 | 显示 |
| `dates` | 日期 | 隐藏 |
| `status` | Working Paper、发表期刊或其他状态 | 显示 |
| `abstracts` | 摘要 | 隐藏 |

`true` 表示显示，`false` 表示隐藏。使用小写，**不要加引号**。这些开关同时控制 Working Papers 和 Publications。标题始终显示；字段内容为空时也不显示。

例如，想显示日期，需要把 `dates` 改成 `true`，同时给相应论文填写 `"date": "October 2026"`。不想公开某个字段，也可以将该论文的字段内容设为 `""`。

目前两篇论文都设为 **Working Paper**，日期留空且开关关闭；Home 不展示论文列表或独立 Education 板块。

## 选择展示哪些论文

Working Papers 的条目保存在 `papers` 数组中。每篇都有：

```json
"visible": true
```

改成 `false` 就会隐藏该篇论文，保留原有资料，方便以后恢复。改回 `true` 就重新显示。

论文按照数组中的顺序排列。调换两个完整条目可以改变顺序。

## 增加或修改一篇论文

找到 `papers` 中对应的条目，修改 `title`、`coauthors`、`date`、`status` 和 `abstract`。也可以在数组内添加一个新条目，结构如下（示例内容需替换为自己的信息）：

```json
{
  "id": "a-unique-paper-id",
  "visible": true,
  "title": "Your paper title",
  "coauthors": "Coauthor A and Coauthor B",
  "date": "",
  "status": "Working Paper",
  "abstract": ""
}
```

- `id` 用小写英文、数字和连字符，且不能与别篇重复。
- `coauthors` 只填写合作者姓名，不含自己，不必写 `with`；没有合作者时留空。
- `status` 可以填写确认过的投稿状态、期刊或发表信息；不用显示时留空，避免填入未经确认的状态。
- 不填日期就保留 `"date": ""`，不要填写占位日期。
- 当前没有上传论文全文，也没有为标题设置下载链接。

## 添加 Publications

目前文件中是：

```json
"publications": []
```

把正式发表论文的条目放进这个数组，使用上面相同的条目结构。`status` 可以填写实际期刊与发表信息。若某篇论文从 Working Papers 转为 Publications，将它从 `papers` 移到 `publications`；或隐藏原 working-paper 条目，避免重复展示。

数组为空，或里面所有论文的 `visible` 都是 `false` 时，Publications 会显示暂无条目。

## 修改 Home 与 CV

- 修改 `bio`：每个字符串显示为一段简介。本科与博士经历已放在简介里，不再单列 Education。
- 修改 `interests`：更新研究方向。
- 替换 `docs/assets/yu-wu-cv.pdf`：更新 View CV 下载的 PDF，保持文件名不变。
- 姓名、头衔、单位、邮箱等固定页眉或侧栏文字仍在 `build.py` 中；需要调整这些内容时同步修改相应位置。
- `education`、`talks`、`teaching`、`awards` 保留原资料，目前没有单独在 Home 展示；仅修改这些数组不会在 Home 增加板块。

## 保存时的注意事项

JSON 中多个条目之间用英文逗号隔开，最后一个条目后不加逗号。文字用英文双引号包围；不要写注释。正文中若包含英文双引号，用 `\"` 转义。

如果预览窗口提示 JSON 错误，按错误行号检查逗号和引号。修正后再预览；上传脚本在生成失败时会停止，不会上传半成品。

## 发布设置与故障排查

GitHub 仓库：https://github.com/wuyuecon/wuyuecon.github.io

发布来源是 **Settings → Pages → Deploy from a branch → main → /docs**。仓库保持 Public，`docs/.nojekyll` 让 GitHub 直接发布静态文件。网页在本机生成，不依赖自定义 Actions 构建。

上传只包含网站文件，不包含原始研究目录、股票项目、Firebase 配置或本机验证记录。上传脚本不会强推或自动合并冲突；如果提示远程有新提交，先停止并核对，或请 Codex 帮你处理。

本仓库 Git 目前使用本机已有代理 `127.0.0.1:7897`。如果代理停用或端口改变，上传可能失败，需要同步本仓库的代理配置；不要为此关闭 HTTPS 校验。
