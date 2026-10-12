# Work package

## Source and scope

- Objective and selected owner: 按作者本轮最终修改授权，补足科学叙述、分析设计与实际绘图的交付衔接；保留 ARS 写作 owner。
- Author-confirmed source paths and sections: 现有 research-agent、ars-academic-writing、res_method、res_plan、res_analyze、data_analyze；作者本轮要求及前轮实际稿件诊断。既有未提交叙事增强必须保留。
- Authorized actions and editable surface: 上述源码及对应 Codex 安装、维护评估文档、本地独立示例和恢复状态。允许必要本地计算、渲染、核验；无第三方模型调用、公开推送或正式科研稿图修改。
- Existing implementation/tests to reuse: harness validate、现有 unittest、真实历史写作产物和已冻结的输入副本。旧 A/B 试验保持原样，本次不是其执行或重跑。
- Scientific invariants, protected artifacts and non-goals: 不改变研究定义、样本、权重、协议或主线；版本化汇总仅作本地开发演示；未知状态不并入阴性，不虚构推断或专家验证。技能安装验收不等于科研质量提升。
- Unresolved author decisions: 无阻塞本次工程修改的决定；独立作者质量评价保持未决。
- Recovery: 修改前备份实际源码与安装；恢复时只还原本轮涉及文件，保留此前未提交修改。

## 1. Tasks

- [x] 1.1 核对实际方法与报告，消除方法规划的固定主张数量及重复加载；源码/安装先比较再同步。
- [x] 1.2 将问题、辨别性比较、可回答的推断与正文交付衔接；不再复制 CARS/CER 等既有规则。
- [x] 1.3 按需加载统计设计与图件执行参考，将可选模型/搜索细节移出普通分析上下文；保留原有保护条款。
- [x] 1.4 在隔离目录完成真实汇总数据的派生量复核、可编辑图及实际图像检查；另交完整引言候选和证据说明。
- [x] 1.5 运行相关维护检查、数据数值核对和错误输入测试；安装匹配后更新已有恢复状态，准确标注独立质量验证缺口。

## 2. Cross-project delivery validation

- [x] 2.1 按作者“继续完善”授权，在已查开发案例之外选择可获得底层记录的本地项目，先核对范围与来源；私有材料仅存 ignored local_state。
- [x] 2.2 完成可复算的描述性比较、完整结果与讨论候选及真实 SVG/PNG，发现输入/配置错误时保留失败并收窄受影响结论。
- [x] 2.3 执行九项数据检查及实际图像检查；记录来源资格仍不完整，不据同会话实作宣称因果质量增益。入口见本地 `.agent/NEXT.md`。
- [ ] 2.4 取得作者实际修订记录及独立读者图件理解结果；模型不得代填修改成本或作者接受。

## 3. Focused continuation (2026-10-11)

- [x] 3.1 按作者“继续优化”授权，补足 Results/Discussion 从已有结果形成认识的局部方法；明确文献推理迁移与学者框架蒸馏的不同路由，修正残留 Nature owner 指针。
- [x] 3.2 针对已有表格错汇总、总体比率误读风险和未执行的联合方案建议，补充条件分析指导；用同一水—碳开发案例交付完整修订正文及真实比较图，不新增正式分析或冒充未见项目验证。
- [x] 3.3 对上述三技能六文件完成相关检查、备份与本地同步；保留旧 A/B、作者待审状态及来源资格限制，报告实际证据。

## Acceptance evidence

| Requirement/source | Implementation/artifact | Check and expected observation | Actual result/evidence locator | Status |
|---|---|---|---|---|
| 作者要求、既有所有权 | 六个现有 owner 与参考 | ARS 保留，普通润色无需全流程 | 源码规则保留；13份安装对应源码。本轮未另测新会话 | IMPLEMENTED; BEHAVIOR_UNTESTED |
| 科学问题与证据匹配 | 方法/论证/结果解释参考 | 问题组不缩减，描述、关联、机制分开，缺证给出最小辨别工作 | 完整正文与伴随说明已完成，保留作者范围；独立质量评价待做 | LOCAL_DEMONSTRATION_COMPLETE |
| 数据分析与作图交付 | 独立开发示例 | 固定范围分母复核；未知显示；SVG/PDF/PNG 真实产生并检查 | 六项数值/错误输入测试通过；打开最终PNG与PDF预览，修复间距；矢量文字保留 | VERIFIED_FOR_THIS_CASE |
| 作品与维护证据分开 | 完整候选正文和维护报告 | 不用自评分或结构测试宣布顶刊质量 | 本地报告区分工程通过、作品完成与独立增益未测；路径见已有.agent恢复指针 | COMPLETE |
| 回归与安装 | 原生检查及安装比较 | 相关检查通过，旧试验保持，正式科研文件不写入 | harness、25 tests、diff检查通过；89冻结文件一致；未写入正式科研项目 | PASS_WITH_STATED_SCOPE |
| 2026-10-11 局部延续 | 三技能六文件、完整 Results/Discussion 与真实两栏图 | 方法落实到已有结果解释、准确分母和渲染产物 | 25 仓库/9 数据测试通过；安装匹配；通用 validator 对既有下划线名称的失败已记录。私有实作及来源限制由 `.agent/NEXT.md` 指向 | ENGINEERING_COMPLETE; HUMAN_REVIEW_PENDING |

## Review and handoff

- Missing / partial / contradictory / unrequested changes: 独立作者评价、复杂推断与本轮新会话行为未测。补充方法文件发现相同固定主张限制和评分循环，一并局部修复；项目OpenSpec旧owner上下文改为当前ARS，历史归档不变。
- Actual verification commands and limitations: `python -B scripts/harness.py validate`；`python -B -m unittest discover -s tests -v`；`git diff --check`；本地数据测试及绘图命令由恢复指针进入报告。没有额外模型调用或质量因果结论。
- Next step: 已有 `.agent/NEXT.md`、`.agent/STATE.md` 记录安装身份、回滚位置及作品待审状态；不自动扩大试验或公开推送。
