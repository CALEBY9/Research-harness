# Research Harness · Research Agent

[中文](README.md) · [Installation guide (Chinese)](docs/installation.md) · [Example](examples/research_brief.md)

A researcher-led collection of skills for environmental and Earth sciences: water, soil, atmosphere and ecology. Research Agent coordinates literature, question development, methods, analysis, figures, writing and revision around the task at hand. Start with an idea, existing data, a paper or a manuscript.

Researchers retain control of scientific direction and central claims. The agent carries out authorized work while keeping source locations, uncertainties and contrary evidence visible.

Use Research Agent as the single coordinating entry. ARS, writing, polishing and
other skills are internal capabilities selected for the task; users need not
operate them separately. The selected workflow moves from reading and reflection
through broad exploration, focused evidence checks, pilots and plan refinement,
then experiments, writing and figures; start wherever existing work permits.
Model roles, connection requirements and validation limits are described in the
[architecture guide](docs/architecture.md).

The maintainer's multi-model allocation is opt-in: a fresh installation can use
the current host without Gemini, Claude or CPA. To adopt that allocation, state
it in your project instructions or request and supply your own configured access.
An optional [model bridge](skills/research-agent/references/model-bridge.md) sends
actual evidence, saves the response and returns control to Research Agent for
factual review and delivery. It requires your configured model endpoint and access;
installation does not supply accounts or quota.

## Quick start

You need Python 3.10+ and a Codex environment that supports local Agent Skills. The installer uses only the Python standard library. Model access comes from your own host environment.

```sh
git clone https://github.com/CALEBY9/Research-harness.git
cd Research-harness
python -X utf8 -B scripts/harness.py validate
python -X utf8 -B scripts/harness.py install --target ~/.agents/skills --dry-run
python -X utf8 -B scripts/harness.py install --target ~/.agents/skills
python -X utf8 -B scripts/harness.py check --target ~/.agents/skills
```

These Python commands work in PowerShell, Bash and zsh; Python expands `~`. Existing destination entries cause the entire installation to stop before copying. Your existing skills and settings are not overwritten.

Open Codex in your research project and confirm that `research-agent` appears in the skill list. Restart the session if needed. See [OpenAI Docs](https://learn.chatgpt.com/docs/build-skills) for host discovery rules.

Example request:

> Use $research-agent. Based on the materials I provide, identify the research task and complete the work supported by the available evidence. Preserve my agreed question and claims. Explain the evidence and options before proposing a change in scientific direction.

Try the [self-contained example](examples/research_brief.md), which includes English instructions and requires no private knowledge base.

## Capabilities

| Deliverable | Main skills |
|---|---|
| Topic development, literature landscapes and initial frameworks | academic-research-suite: selected ARS planning modes |
| Scientific value, novelty and claim selection | nature-scientific-insight |
| Process hypotheses from environmental observations | nature-research-discovery |
| Methods and experiment plans | nature-method-design |
| Search, citation checks, lawful full text and close reading | nature-academic-search, nature-downloader, nature-reader |
| Analysis, statistical reporting, evidence audit and data availability | nature-data-analysis, nature-statistics, nature-evidence-audit, nature-data |
| Scientific figures and presentations | nature-figure, nature-paper2ppt, nature-image2ppt |
| Manuscripts, language editing and formatting | nature-writing, nature-polishing, nature-paper-format |
| Proposals, referee-style review and response letters | nature-proposal-writer, nature-reviewer, nature-response |
| Optional corpus integration and literature monitoring | nature-literature-kb, nature-literature-pipeline |
| Requested skeptical critique and sourced decision support | ai-skeptic, nature-decision, nature-scholar-distiller |

The collection also includes Chinese general editing and shared references. The [catalog](skills/catalog.json) declares 29 active skill entry points. The redundant ARS writing adapter was removed from the source tree; its history and attribution remain in Git. Its retired name still prevents installation and identifies stale installations. Skills are selected by deliverable; there is no mandatory end-to-end autonomous pipeline.

## Optional dependencies

The core instructions work with your supplied materials. A private literature corpus is not required. When no corpus is configured, use supplied originals or accessible literature and report the evidence actually examined.

- Local corpus integration needs your own compatible backend, source documents and indexes. The author's private corpus and `research_library.py` backend are not included. Set `RESEARCH_AGENT_KB_ROOT` only when you have that backend; `doctor` checks its location, not retrieval quality.
- Search and full-text services need the relevant network access, accounts or institutional permissions.
- Document, PDF, presentation and specialist chart operations need suitable tools and their module dependencies. Office, Origin, EditaPlot and Tabbit are not bundled.
- Monitoring requires an explicitly configured scheduler and notification service. Installation creates no background jobs.

Install optional dependencies when a task actually requires them. The installer does not alter runtime settings, configure accounts or download models.

## Project-local or selective installation

```sh
python -X utf8 -B scripts/harness.py install --target ../my-research/.agents/skills
python -X utf8 -B scripts/harness.py check --target ../my-research/.agents/skills
```

Use `--skill nature-reader --skill nature-polishing` on both commands to select individual capabilities. Shared resources and notices are always included. Installing only the router does not install all specialist owners. Avoid duplicate user- and project-level installations.

For updates, stage into a fresh directory outside skill discovery, compare with your installation, preserve local edits and update only the reviewed files:

```sh
python -X utf8 -B scripts/harness.py stage --target ./local_state/review_candidate
```

The installer intentionally has no overwrite option. `git pull` does not change installed skills.

## Verification

```sh
python -X utf8 -B scripts/harness.py validate
python -m pip install -r scripts/pdf_download/requirements.txt
python -X utf8 -B -m unittest discover -s tests -v
python -X utf8 -B scripts/harness.py doctor
```

`validate` checks source structure, syntax, distribution selection and known credential patterns. `check` verifies installed files and shared resources. Neither executes models or establishes scientific quality. Optional tool tests report skips explicitly.

The pip command supplies the existing downloader's test dependencies; use a separate Python environment. Installing the skill collection itself does not require these packages.

[CI](.github/workflows/validate.yml) is configured for Windows, Linux and macOS with Python 3.10 and 3.13. Consult the Actions run for the exact commit; a configured matrix is not a claim that every platform has passed. Host skill discovery and real research behavior require separate checks.

## Licensing and contributions

Original contributions use [Apache-2.0](LICENSE). Third-party terms remain separate: ARS content uses CC BY-NC 4.0; Humanizer components retain MIT; Nature components retain Apache-2.0 and applicable embedded notices. The entire bundle must not be treated as unrestricted Apache-2.0 content. Read [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Unlicensed `figures4papers` reference material is excluded from the current distribution. Older Git history has not been rewritten. No private research inputs or credentials are included.

Contributions should address a reproducible problem, preserve provenance and include relevant checks. See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md). Do not upload private papers, credentials or complete research datasets to issues.
