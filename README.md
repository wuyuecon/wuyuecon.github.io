# Yu Wu — Academic Website

Personal academic website of Yu Wu (吴裕), PhD Candidate in Economics at the National School of Development, Peking University. Research interests: **Macro Labor** and **China Economy**.

Website: https://wuyuecon.github.io/

网站导航为 **Home / Working Papers / Publications**。CV 下载保留在 Home。Publications 当前暂留空，待站主提供已发表论文后补充。

## 本地修改与预览

1. 编辑 `site-data.json`：个人简介、研究方向、论文、摘要、教育和教学经历。
2. 更新英文简历时，用新版 PDF 替换 `docs/assets/yu-wu-cv.pdf`。
3. 运行 `python build.py`，或双击 `Upload Website.cmd`，它会先重新生成网页。
4. 双击 `Open Website.cmd` 预览本地网站。

标题和页面结构在 `build.py`，样式在 `docs/assets/style.css`。生成网页需要 Python 3.12 或更新版本，无需额外 Python 包。

## 上传与自动发布

双击 **`Upload Website.cmd`**：重新生成网页、提交网站文件，再推送至 `main`。首次 GitHub 登录或登录过期时，按 Git Credential Manager 提示完成登录。

也可以使用：

```powershell
python build.py
git add -- build.py site-data.json docs README.md .gitignore "Open Website.cmd" "Upload Website.cmd"
git commit -m "Update academic website"
git push origin main
```

每次推送后，GitHub 内置 Pages 流程会将 **`main` 分支的 `docs/`** 发布为网站，不运行自定义构建工作流。网页在本机由 `python build.py` 生成。进入仓库 **Actions → pages build and deployment** 检查结果；上传完成与网页发布完成是两个阶段，内置发布任务成功后刷新网站。

仓库的 Settings → Pages 应使用 **Deploy from a branch → main → /docs** 作为发布来源。`docs/.nojekyll` 表示直接发布静态网页。仓库需保持 Public，才能使用当前账号支持的 GitHub Pages。

网站为纯静态 HTML/CSS，无数据库、前端依赖或 API 密钥。源码、数据文件和本地维护脚本留在仓库，只有 `docs/` 会被作为网页发布。

## 内容来源

个人履历、两篇 working papers 和摘要依据本人提供的英文简历。研究方向以站主最新指定为准。未提供的论文 PDF 和社交账号不设占位链接。
