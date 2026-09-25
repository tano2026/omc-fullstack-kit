---
name: fetch-url-tool
description: Provides a utility to fetch content from a URL via an OpenClaw extension on the VPS.
category: utilities
---

## 🚀 Overview

This skill enables Hermes Agent to fetch content from URLs. Due to limitations in directly integrating custom `fetch` tools within the Hermes Python environment, this implementation leverages an OpenClaw extension running on your VPS (100.64.173.75) to provide the URL fetching capability as an HTTP API endpoint.

## 🛠️ OpenClaw Extension Setup (VPS: 100.64.173.75)

To enable the `fetch_url` functionality, you need to deploy a custom Node.js extension within your OpenClaw installation on the VPS.

**1. Create the Extension Directory:**

```bash
sudo mkdir -p /usr/lib/node_modules/openclaw/dist/extensions/hermes-fetch-url
```

**2. Create `package.json` for the Extension:**

```bash
sudo tee /usr/lib/node_modules/openclaw/dist/extensions/hermes-fetch-url/package.json > /dev/null <<'EOF'
{
  "name": "@openclaw/hermes-fetch-url",
  "version": "1.0.0",
  "private": true,
  "description": "Hermes fetch_url tool via OpenClaw",
  "type": "module",
  "openclaw": {
    "extensions": [
      "./index.js"
    ]
  }
}
EOF
```

**3. Create `index.js` for the Extension:**

This file defines the HTTP endpoint (`/api/v1/hermes-fetch`) that Hermes will call. It uses Node.js `fetch` (via `undici`) to retrieve content from the specified URL.

```bash
sudo tee /usr/lib/node_modules/openclaw/dist/extensions/hermes-fetch-url/index.js > /dev/null <<'EOF'
import { t as definePluginEntry } from '../../plugin-entry-BZpzqykQ.js';
import { fetch } from 'undici'; // Requires undici or native fetch in Node.js (v18+)

var hermes_fetch_url_default = definePluginEntry({
  id: "hermes-fetch-url",
  name: "Hermes Fetch URL Tool",
  description: "Provides a basic URL fetching utility for Hermes Agent",
  register(api) {
    api.registerHttpRoute({
      path: "/api/v1/hermes-fetch",
      auth: "none", // For simplified initial testing, consider adding authentication later
      match: "exact",
      handler: async (req, res) => {
        if ((req.method ?? "GET").toUpperCase() !== "POST") {
          res.statusCode = 405;
          res.setHeader("Allow", "POST");
          res.end(JSON.stringify({ error: "Method Not Allowed" }));
          return;
        }

        let body = '';
        for await (const chunk of req) {
          body += chunk.toString();
        }

        let requestData;
        try {
          requestData = JSON.parse(body);
        } catch (e) {
          res.statusCode = 400;
          res.setHeader("Content-Type", "application/json");
          res.end(JSON.stringify({ error: "Invalid JSON body" }));
          return;
        }

        const { url } = requestData;

        if (!url) {
          res.statusCode = 400;
          res.setHeader("Content-Type", "application/json");
          res.end(JSON.stringify({ error: 'URL is required' }));
          return;
        }

        try {
          const response = await fetch(url);
          const content = await response.text();
          res.statusCode = 200;
          res.setHeader("Content-Type", "application/json");
          res.end(JSON.stringify({ content: content, status: response.status, url: url }));
        } catch (error) {
          console.error('Fetch error:', error);
          res.statusCode = 500;
          res.setHeader("Content-Type", "application/json");
          res.end(JSON.stringify({ error: error.message }));
        }
      }
    });
  }
});

export { hermes_fetch_url_default as default };
EOF
```

**4. Restart OpenClaw on VPS:**

After creating the files, you need to restart the `openclaw` process for the new extension to be loaded.

```bash
ssh ubuntu@100.64.173.75 "pm2 restart openclaw"
```

## 🤖 Agent Integration (Hermes Python - Local)

Once the OpenClaw extension is running on your VPS, you can update your local Hermes `fetch-url-tool` plugin (or create a new Python tool) to call this endpoint.

**Example Python tool implementation (e.g., in `~/.hermes/plugins/fetch-url-tool/tools.py`):**

```python
import requests
import json

def fetch_url(url: str, max_length: int = 5000) -> dict:
    openclaw_endpoint = "http://100.64.173.75:20128/api/v1/hermes-fetch" # Use the OmniRoute external port and new API path
    headers = {"Content-Type": "application/json"}
    payload = {"url": url}

    try:
        response = requests.post(openclaw_endpoint, headers=headers, data=json.dumps(payload), timeout=15)
        response.raise_for_status() # Raise an exception for HTTP errors
        data = response.json()
        content = data.get("content", "")
        status = data.get("status", 200)
        fetched_url = data.get("url", url)
        return {"content": content[:max_length], "status": status, "url": fetched_url}
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch URL via OpenClaw: {e}", "status": 500}
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse JSON response from OpenClaw: {e}", "status": 500}

# No _register_tool() needed if this is part of a Hermes plugin's tools.py
```

**5. Restart Hermes Local:**

Restart your local Hermes Agent to load the updated `fetch-url-tool` plugin.
