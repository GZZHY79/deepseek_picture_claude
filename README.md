# read-image — Claude Code 视觉识别 Skill

让 Claude Code 读取并描述本地图片文件。兼容任意 OpenAI 格式的视觉 API。默认使用智谱 GLM-4V-Flash（免费），也支持 OpenAI、OpenRouter、vLLM 等。

- ⚡ **轻量** —— 一个 Python 脚本，一个依赖（`httpx`），再无其他
- 🔌 **易装** —— marketplace 两行命令，或手动复制一次

## 为什么需要这个？

Claude Code 内置的 `Read` 工具不会把图片发送给非 Anthropic 的 API。如果你用 DeepSeek 或其他第三方模型，读图功能直接挂掉——只返回 `[Unsupported Image]`。

这个 skill 绕过这个限制：直接读取图片文件，调用视觉模型 API，把文字描述返回给 Claude。

## 工作原理

```
用户："这张图里有什么？"  →  Skill 触发  →  Python 脚本读取图片
                                                 ↓
用户看到文字描述          ←  Claude 转发   ←  视觉 API 返回结果
```

## 安装与配置

配置是**必须的**——没有 API key 无法使用。

### 第一步：安装

**Marketplace 安装（推荐）：**
```bash
claude plugin marketplace add https://github.com/GZZHY79/deepseek_picture_claude
claude plugin install read-image
```

**手动安装：**
```bash
mkdir -p ~/.claude/skills/
cp -r read-image ~/.claude/skills/
pip install httpx
```

### 第二步：配置 API key ⚠️ 必做

在 `~/.claude/settings.json`（或项目级 `.claude/settings.json`）中添加：

```json
{
  "env": {
    "VISION_API_KEY": "换成你的真实key",
    "VISION_BASE_URL": "https://open.bigmodel.cn/api/paas/v4",
    "VISION_MODEL": "GLM-4V-Flash"
  }
} 
```

添加时注意外侧"{}"的位置
免费 key 可在 [open.bigmodel.cn/apikey/platform](https://open.bigmodel.cn/apikey/platform) 获取。

### 其他模型提供商

<details>
<summary>OpenRouter（免费）</summary>

在 [openrouter.ai/keys](https://openrouter.ai/keys) 获取 key：
```json
{
  "env": {
    "VISION_API_KEY": "sk-or-v1-...",
    "VISION_BASE_URL": "https://openrouter.ai/api/v1",
    "VISION_MODEL": "nvidia/nemotron-nano-12b-v2-vl:free"
  }
}
```
</details>

<details>
<summary>OpenAI</summary>

```json
{
  "env": {
    "VISION_API_KEY": "sk-...",
    "VISION_BASE_URL": "https://api.openai.com/v1",
    "VISION_MODEL": "gpt-4o-mini"
  }
}
```
</details>


## 使用

安装配置完成后，直接对 Claude 说：

> "读一下这张图：/path/to/screenshot.png"
>
> "这张图表显示了什么？ ~/Downloads/results.png"
>
> "分析这个架构图：/tmp/architecture.jpg"

## 配置参考

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `VISION_API_KEY` | *(必填)* | 视觉模型提供商的 API key |
| `VISION_BASE_URL` | `https://open.bigmodel.cn/api/paas/v4` | OpenAI 兼容的 API 地址 |
| `VISION_MODEL` | `GLM-4V-Flash` | 视觉模型名称 |

## 支持的图片格式

PNG、JPG/JPEG、GIF、WebP、BMP、TIFF。

## 常见问题

**`claude plugin marketplace add` 卡住或超时：**
```bash
CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS=600000 claude plugin marketplace add https://github.com/GZZHY79/deepseek_picture_claude
```

**提示 `VISION_API_KEY environment variable is required`：**
确认已完成 [第二步](#第二步配置-api-key-️-必做)——在 `settings.json` 中正确添加了 `env` 块。

## License

MIT

---
 欢迎大家使用和在[Issue](https://github.com/GZZHY79/deepseek_picture_claude/issues)提出建议，我会及时查看。
