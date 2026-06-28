# GATES.md — 验收闸门（Niche Scanner MVP）

状态：`已配置`
最后更新：2026-06-27

## 1. 总规则

只有同时满足以下条件，才可以声称完成：

1. `bash check.sh` 通过。
2. 满足 `PRD.md` 的相关验收标准。
3. 没有引入未经确认的新依赖、架构变化或密钥硬编码。

## 2. 自动检查

| 闸门 | 命令 | 是否必须 | 通过条件 |
|---|---|---|---|
| 环境 / 安装 | `python -c "import fastapi, httpx, sqlalchemy, weasyprint"` | 是 | 退出码 0 |
| 代码风格 (backend) | `ruff check backend/app/` | 是 | 无 error |
| 类型检查 (backend) | `mypy backend/app/` | 是 | 无类型错误 |
| 测试 | `pytest backend/tests/ -v --tb=short -q` | 是 | 全部通过 |
| 构建 (frontend) | `cd frontend && npm run build` | 是 | 退出码 0 |
| 冒烟测试 | `curl -f http://localhost:8000/health` | 是 | HTTP 200 |
| 安全审计 | `grep -r "sk-.*" backend/app/ frontend/src/` | 是 | 无结果（无硬编码密钥） |

## 3. 人工验收

- [ ] P0 主流程：输入 3 想法 → 60s 内看到排名 → 下载 PDF
- [ ] 空、加载、错误、成功状态都可见且合理
- [ ] 某个 scraper 失败时仍显示部分评分 + 缺失标注
- [ ] 移动端布局正常，无溢出
- [ ] 当前版本已写入 `STATUS.md`
- [ ] 历史版本已写入 `CHANGELOG.md`
- [ ] 新报错或踩坑已写入 `ERRORS.md`
- [ ] 没有 Polsia 遗留代码混入 Niche Scanner 核心页面

## 4. 最近运行

- 运行时间：
- 运行命令：`bash check.sh`
- 结果：
- 未通过项：
