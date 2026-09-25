"""
Unified Tool Runner & CLI Dispatcher for OMC Agents.
Provides execution harness and schema export for Hermes, DSH, and OpenClaw runtimes.
"""

import sys
import os
import json
import argparse
from typing import Dict, Any, Optional

# Ensure package path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Import registry and all tool modules to trigger decorators
from engines.tools.registry import (
    register_tool,
    list_all_tools,
    get_agent_tools,
    get_openai_tools,
    execute_tool,
    get_tool
)
import engines.tools.social_tools
import engines.tools.research_tools
import engines.tools.cskh_tools
import engines.tools.safety_tools


def list_tools_summary(agent_id: Optional[str] = None):
    """Prints a neat summary table of available tools."""
    tools = get_agent_tools(agent_id) if agent_id else list_all_tools()
    print(f"\n=================================================================")
    print(f"🛠️ OMC AGENT TOOLS ECOSYSTEM (Agent: {agent_id or 'ALL'})")
    print(f"Total Tools: {len(tools)}")
    print(f"=================================================================")
    for i, t in enumerate(tools, 1):
        print(f"\n{i}. [{t['category'].upper()}] {t['name']}")
        print(f"   📋 Mô tả: {t['description'][:100]}...")
        print(f"   🤖 Agents: {', '.join(t['agent_ids'])}")
        req_params = t['parameters'].get('required', [])
        props = list(t['parameters'].get('properties', {}).keys())
        print(f"   ⚙️ Tham số: {props} (Bắt buộc: {req_params})")
    print(f"=================================================================\n")


def run_tool_cli(tool_name: str, args_json: str):
    """Executes tool with JSON string argument and prints formatted result."""
    try:
        kwargs = json.loads(args_json) if args_json else {}
    except Exception as e:
        print(f"❌ Error parsing JSON args: {e}")
        return

    print(f"🚀 Executing tool: '{tool_name}' with args: {kwargs} ...\n")
    result = execute_tool(tool_name, **kwargs)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def export_agent_tool_schemas(dest_dir: str = "engines/tools/schemas"):
    """Exports OpenAI/Hermes compatible tool definition schemas per agent."""
    os.makedirs(dest_dir, exist_ok=True)
    agents = [
        "social-creator",
        "market-spy",
        "cskh-consultant",
        "brand-guard",
        "ceo-copilot",
        "media-producer",
        "research-intel",
        "jev-sentinel",
        "openclaw-executor"
    ]

    for ag in agents:
        schemas = get_openai_tools(ag)
        file_path = os.path.join(dest_dir, f"{ag}_tools.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(schemas, f, ensure_ascii=False, indent=2)
        print(f"✅ Exported {len(schemas)} tools for agent '{ag}' -> {file_path}")


def main():
    parser = argparse.ArgumentParser(description="OMC Agent Tool Runner")
    parser.add_argument("--list", action="store_true", help="List all registered tools")
    parser.add_argument("--agent", type=str, help="Filter tools by agent ID")
    parser.add_argument("--tool", type=str, help="Name of tool to execute")
    parser.add_argument("--args", nargs="*", help="JSON string or key=value pairs of arguments for the tool")
    parser.add_argument("--export-schemas", action="store_true", help="Export OpenAI function schemas for all agents")

    args = parser.parse_args()

    if args.export_schemas:
        export_agent_tool_schemas()
    elif args.tool:
        raw_args = " ".join(args.args) if args.args else "{}"
        if not raw_args.strip().startswith("{") and "=" in raw_args:
            # Handle key=value format like topic=TriMun count=3
            kv_dict = {}
            for item in args.args:
                if "=" in item:
                    k, v = item.split("=", 1)
                    kv_dict[k.strip()] = v.strip()
            raw_args = json.dumps(kv_dict)
        run_tool_cli(args.tool, raw_args)
    else:
        list_tools_summary(args.agent)


if __name__ == "__main__":
    main()
