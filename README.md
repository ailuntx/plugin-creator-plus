# Plugin Creator Plus

创建、测试、打包和发布 ChatGPT / Codex 插件的统一工作流。独立开发，与 OpenAI 无隶属关系。

直接说：

> 用 Plugin Creator Plus，把这个项目做成插件并发布到 OpenAI 插件目录。

或：

> 自己构思一个有用的小插件，做出来并发布。

它复用 Plugin Creator 的脚手架与本地市场流程，按项目类型使用 OpenAI Developers 的提交准备能力，需要凭证时使用 AI Know Me，使用 ego-browser 操作发布门户。自带 Python 标准库实现的目录发布检查和 ZIP 打包工具，减少因分类、长度、版本或打包内容出错而反复上传。

## 运行条件

需要本地终端、Python 3.10+，以及另行安装的 Plugin Creator、ego-browser。OpenAI Developers 用于 MCP 项目，AI Know Me 用于需要已存凭证的步骤；已有网站登录状态时不会读取凭证。插件本身不包含这些依赖，也不提供发布 Token。

发布需要可用的 OpenAI Platform 登录和具备发布权限的已验证身份。扫描和审核仍由平台完成；遇到登录验证可能需要用户参与。

源码插件位于 `plugins/plugin-creator-plus`。在 Codex 中安装后，新会话可使用 `plugin-creator-plus`。

## 检查与打包

```bash
python3 plugins/plugin-creator-plus/skills/plugin-creator-plus/scripts/release.py check plugins/plugin-creator-plus
python3 plugins/plugin-creator-plus/skills/plugin-creator-plus/scripts/release.py package plugins/plugin-creator-plus --out dist
python3 -m unittest discover -s tests -v
```

打包工具只处理 Plugin Creator 生成的 skills-only 目录。MCP 项目走发布门户的 With MCP 流程。它不会上传文件或修改原插件；公开上传由 Agent 在用户授权的发布任务中执行。

[隐私说明](docs/privacy.md) · [使用条款](docs/terms.md) · [问题反馈](https://github.com/ailuntx/plugin-creator-plus/issues)
