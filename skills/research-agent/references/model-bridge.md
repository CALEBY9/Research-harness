# 外部模型调用与写作交接

在已选择的分工确实需要外部模型时使用；普通写作可直接由当前宿主完成。
调用脚本为本技能下的 `scripts/model_bridge.py`，不新增公开技能或运行时守护进程。
默认配置位于 `~/.config/research-agent/models.json`；也可显式传 `--config`。

## 配置与连接

从 [配置示例](model-bridge.example.json) 建立自己的本地配置。模型名留空时不执行，
先用 `models --provider gateway` 查询实际 ID，再填写所需角色。不要依据偏好标签
假定接口提供 Gemini 4、Astra 或任何指定型号。服务列出模型不等于生成已成功。

默认用 `api_key_env` 引用环境变量，不把密钥写入配置、命令行或交接材料。
本机已有 CPA YAML 时，可将该字段替换为 `cpa_config_file`，值为现有配置的绝对路径；
脚本只读取已有 `api-keys` 的首个客户端密钥，不复制或修改它。该可选读取方式需
当前 Python 已有 PyYAML；环境变量方式仅用标准库。CPA 凭据只发送到端口匹配的
回环地址。安装技能不会启动 CPA、配置登录或获得订阅额度。

```powershell
python <skill-dir>/scripts/model_bridge.py models --provider gateway
python <skill-dir>/scripts/model_bridge.py call --role writer --instruction-file task.md --evidence evidence.md --evidence outline.md --output writing_runs/paragraph_01
```

在真实 shell 中把 `<skill-dir>` 换成已安装技能目录；路径有空格时加引号。
指令和证据文件应为 UTF-8 文本。PDF、Word、表格先用原有读取工具取得相关原文、
数值和定位，再组成该次需要的材料；API 收到实际文件内容，不能只给本机路径。
`--output` 选择项目内新的两级目录，已有目录会在发请求前被拒绝，保护原稿。

## Research Agent 的自动接续

1. 从当前任务和已有授权确定角色与范围。`writer` 用于 Gemini 拟投稿写作，
   `idea_peer` 用于开放讨论；`story` / `plan_peer` 仅在有高价值问题时显式调用，
   不默认消耗 Claude。Astra/Codex 若为当前宿主，直接承担自己的工作，不再调用自身 API。
2. 准备一次必要的作者请求和证据，执行一次 `call`。返回 `AWAITING_HOST_REVIEW`
   代表已有候选文本，当前 Research Agent 必须继续读取 `response.md` 并核对输入，
   不向用户把这个中间状态当成最终交付，也不要求用户手工搬运模型返回稿。
3. Codex/当前协调者核对数字、引用支持、范围、因果、确定程度和重要遗漏。
   请求/返回型号不一致时说明实际记录，不能冒充指定型号。模型自报身份与核验均非
   独立证明。保留自然表达，不做第二轮全篇防御性重写。
4. 无实质问题时，在原任务授权内用相应文档工具保存干净正文；如需 Word/PDF，
   沿用既有文档生成和版面检查。核对理由和调用记录留在该次目录，正文不混入过程。
   实质事实问题需广泛重写时，最多再做一次明确修正的 writer 调用，使用新的输出目录；
   仍有关键科学分歧则报告分歧，由作者决定，不进入无限审稿循环。

每次 `call` 只发一次生成 HTTP 请求，无隐式 Claude、重试、备用模型或投票。
配置中的输出 token 上限可被 `--max-output-tokens` 覆盖；这是单次生成上限，
不是价格或账户剩余额度。CPA 自身可能有重试，不能把桥接次数称为上游实际调用次数。
429、连接超时、空文本、无效响应和截断均显式失败；截断文本保留为
`partial_response.md`，不能作为完成稿。失败后不自动重复消耗额度。

## 来源与采用范围

参考实现已检查，以下仅借鉴设计，未复制上游代码或安装整套工作流：

- [Trivium](https://github.com/MetaQiu/Trivium/tree/2c89d260b70fb5654ad3c1294c8642b132d11005)：
  `scripts/paper_workflow.py` 的协调者与外部调用分离、文件化材料交接。
  未采用三模型逐段起草、Claude 合稿、投票达成共识及多轮去 AI 味链。
  该固定版本根目录 LICENSE 路径返回 404，不据此假定其代码可再分发。
- [ARIS llm-chat](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/8f493923f28c3f991dcca1287db97aa780d0969b/mcp-servers/llm-chat/server.py)：
  OpenAI-compatible 调用、请求与返回型号分开记录、审查调用不自动重试及空返回检查。
  上游 MIT；本地桥接器独立实现，未采用 MCP 服务、审查投票门槛、自动模型切换或日志框架。
- [CCG-Scholar](https://github.com/xlx777/ccg-scholar)：仅参考其配置化角色分配说明。
  未安装其 wrapper、MCP 集合，也未采用 Claude 正文主笔的默认分工。

借鉴来源和测试通过均不证明本地写作质量优于单模型；用实际任务的证据保真和
作者修改负担判断效果，不以多个模型赞同作为科学可靠性的保证。
