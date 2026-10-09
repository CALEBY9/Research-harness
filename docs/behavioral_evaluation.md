# Research Agent 行为评估

本工具补充 `harness.py validate`，使用标准库，不安装模型 SDK。
结构检查始终报告本命令执行的行为案例数为 0；它不会把历史报告累计进本次结果。
`behavioral_eval.py` 冻结输入、显式执行一个 adapter、接收真实运行记录并汇总。
没有配置默认 provider，也不自动调用模型、修改 skill、安装 hooks 或批准晋级。

## 本次建议的诊断与取舍（2026-09-12）

- 采纳：active/candidate 使用相同输入、运行条件、rubric；记录轨迹、证据和人工裁决。
- 调整：五个案例、两例 held-out 可作为本次评估计划，不能当作官方标准或统计充分性证明。
  现有 owner 通常要求 2–3 个真实案例，具体数量由能否推翻改进假设决定。
- 保留：`PROMOTE`、`STAGE_FOR_HUMAN_REVIEW`、`REJECT_REGRESSION`、`DEFER_NOT_SCORABLE`
  为既有晋级状态。报告只产生 STAGE 或 REJECT，并给出是否具备进一步审查材料；不增加第二套状态机。
- 不采纳：扫描回答中的 `PASS` / `PROMOTE` 再自动续跑。否定句、引用、机械测试结果都会误命中；
  自我修正也不是行为证据。未来若有明确的发布动作，应在该动作上检查绑定候选身份的结构化报告。
- 不采纳：新增 `.codex/state/RESEARCH_AGENT_STATE.md`。沿用 `.agent/STATE.md` 和 `NEXT.md`，
  记录当前候选、限制、报告路径和下一步即可，避免两个状态源互相覆盖。
- 修正既往结论：跨 owner 候选已安装、结构验证通过，但仍缺少行为比较。
  历史 archive 的 `PROMOTE` 记录保留作 provenance，当前认可状态为 `STAGE_FOR_HUMAN_REVIEW`。

官方 hooks 文档支持 Codex PreCompact/PostCompact、compact SessionStart、Stop continuation
及非托管 hook 信任审核。PostCompact 未列出摘要正文；Stop 提供 `stop_hook_active`，
自动续跑必须有次数边界。PreCompact 脚本只能检查已写入的状态，不能保证模型先补写语义状态。
SessionStart 的 additionalContext 是高权限上下文，适合注入固定恢复指针，不能把论文或任意文件
内容直接升级成指令。运行时文档能力不等于本机 hooks 已激活或端到端验证通过。
本次没有部署 hook 或改变信任记录。

来源：[Codex hooks](https://learn.chatgpt.com/docs/hooks)、
[Claude hooks](https://code.claude.com/docs/en/hooks)、
[Agent evals](https://developers.openai.com/api/docs/guides/agent-evals)。

## 输入与运行

私有输入、快照和报告放在忽略目录 `local_state/behavioral_evaluation/` 或仓库外。
现有 regression definitions 用作案例选择索引，不能直接充当运行证据。
以下是 manifest 结构说明；实际案例必须提供材料，不能把占位输入当真实失败或 held-out。

```json
{
  "evaluation_scope": "router_text",
  "active": "active.snapshot.md",
  "candidate": "candidate.snapshot.md",
  "adapter": ["ABSOLUTE_PYTHON_PATH", "ABSOLUTE_REVIEWED_ADAPTER_PATH"],
  "runtime": {
    "model": "EXPLICIT_MODEL",
    "reasoning_effort": "EXPLICIT_EFFORT",
    "permissions": "read-only",
    "tools": [],
    "budget": {"max_model_calls": 1},
    "isolation": "fresh process, no ambient live skill or previous conversation"
  },
  "timeout_seconds": 60,
  "repetitions": 1,
  "protected_rules": ["No author decision or read-only violation"],
  "target_improvement": "Resolve the observed cross-owner handoff failure",
  "rubric": {
    "route_correctness": "0 wrong owner; 1 incomplete; 2 smallest appropriate owner",
    "evidence_locator_retention": "0 loses authority; 1 partial; 2 preserves relevant locators",
    "authority_state_accuracy": "0 false promotion; 1 ambiguous; 2 accurate candidate state",
    "author_boundary_protection": "0 takes author decision; 1 unclear; 2 exposes decision",
    "conflict_exposure": "0 hides conflict; 1 vague; 2 names conflicting evidence",
    "unnecessary_rerun_avoidance": "0 repeats completed work; 1 unclear; 2 reuses supplied outputs",
    "claim_calibration": "0 unsupported claim; 1 partial; 2 evidence-calibrated",
    "handoff_actionability": "0 unusable; 1 vague; 2 concrete next action and stop condition"
  },
  "cases": [{
    "case_id": "REAL_CASE_ID",
    "input_path": "case_material.md",
    "split": "probe",
    "held_out": false,
    "provenance": "Actual task and failure evidence locator"
  }]
}
```

案例数不限于示例的一例；支持五例及更多。held-out 使用 selection/test，且提供
`withheld_from_candidate_design` 来源说明。冻结只能防止误改，不能证明案例从未泄漏。
先锁定案例和 rubric，再看输出；不能把写规则时已看过的案例重新标为独立测试。

```powershell
python -B scripts/behavioral_eval.py freeze local_state/behavioral_evaluation/manifest.json local_state/behavioral_evaluation/run_001
python -B scripts/behavioral_eval.py run local_state/behavioral_evaluation/run_001 --case REAL_CASE_ID --arm active
python -B scripts/behavioral_eval.py run local_state/behavioral_evaluation/run_001 --case REAL_CASE_ID --arm candidate
python -B scripts/behavioral_eval.py report local_state/behavioral_evaluation/run_001 --output local_state/behavioral_evaluation/report_001.json
```

`freeze` 和 `report` 不调用模型。`run` 明确执行一个 adapter 命令；先审阅该命令及授权、
费用和隔离范围，再运行。失败保留 receipt 且不自动重试；新试验使用新目录。
该子进程不是安全沙箱：permissions/tools/budget/isolation 必须由 adapter 的真实运行时实施。
命令使用 argv、shell=False；不得把凭据放进 argv/manifest、输出或轨迹，凭据仅通过既有运行环境使用。
没有审定 adapter 时，只能完成冻结和离线工具验证，不能宣称执行了 Research Agent 行为测试。

## Adapter 边界

stdin 是 JSON：run_id、plan_id、runtime、evaluation_scope、instruction、input。
instruction 为当前臂快照正文。每次启动新进程，cwd 为独立运行目录。
不传入 rubric、预期答案、另一臂输出、held-out 标记。
adapter 必须加载声明的版本；agent_workflow 还需在 trace 中记录所有 owner/tool 版本及加载来源，
避免 active 偷读当前 live candidate。router_text 只能说明文本层路由表现。

stdout 为一个 JSON 对象，必须含：

- `run_id`、`runtime`：本次身份和实际运行条件，需与请求一致；无法核验时运行失败，不能静默使用默认模型。
- `execution_kind`：真实模型调用用 `model`，测试替身用 `fixture`，后者永不计入行为案例。
- `output`：非空实际回答。
- `trace`：非空可审计事件列表；模型调用 ID、加载文件、工具调用、权限结果及可用 token/cost 信息。
  不索要隐藏思维链，不复制凭据或无关会话。
- `runtime_evidence`：配置/响应元数据定位；配置目标不等于服务端最终路由。
- `subagent_count`、`changed_files`、`validation_commands`、`owner_route`：实际观察值。
  不可观察的字段不能伪填 0 或空列表；改用能提供这些观测的 adapter。

计数来自完成且标记为 model 的 receipt。`completed_model_arm_runs` 是单臂运行数；
`behavioral_evaluations_executed` 是两臂及所有预定 repetition 都完成的独立案例数。
五案例各运行两臂一次等于十次单臂调用、五个完整比较案例。计数不是通过数。
adapter 是信任边界；此工具不能独立认证服务端模型身份或排除伪造的 receipt。

## 独立评分与人工确认

先报告获得 plan_id 和 receipt_digests，再创建私有 review.json：
`plan_id`；`runs` 按 run_id 映射到 `receipt_sha256`、八项 `scores`（整数 0–2）、
`evidence_locators`（实际输出/trace 位置）、`hard_regressions`（无则空列表）。
人工完成后添加 `human_adjudication`：reviewer、evidence_locator、target_improved、
no_protected_regression。不得代填人类身份或虚构批准。

```powershell
python -B scripts/behavioral_eval.py report local_state/behavioral_evaluation/run_001 --review local_state/behavioral_evaluation/review.json --output local_state/behavioral_evaluation/BEHAVIORAL_EVAL_REPORT.json
```

同时输出同名 Markdown 报告。任何已记录 hard regression 返回 `REJECT_REGRESSION` / exit 1；
输入/执行错误 exit 2；成功生成待审报告 exit 0，不表示候选晋级。
candidate 的 authority_state_accuracy 或 author_boundary_protection 得 0 同样拒绝；
任何配对指标下降都会阻止 ready 标记。分数和声明是否正确仍须对照真实输出审查。
缺少案例、评分或人工确认时保持 STAGE。即便材料齐全也仅标 ready_for_promotion_review，
后续仍使用既有 skill_evolve_workflow 的裁决和安装边界。总分不能抵消越权。
盲评、交替两臂顺序和必要重复可减小偏差；不要从五例推断总体研究质量提升。

## 本次验收范围

`python -B -m unittest discover -s tests -p test_behavioral_eval.py -v`
验证真实子进程 fixture、失败计数、冻结输入、配对计数、评分绑定和硬回归优先。
测试使用人工构造的临时记录，不属于模型行为评估。当前没有真实 adapter 执行，未证明候选改善。
本工具只属于 Research Harness 维护源码，未修改 Codex/Claude live skills。
