"""
Central Tool Registry for OMC Agents.
Allows registering, inspecting, generating OpenAI function schemas, and executing agent tools.
"""

import inspect
import json
import logging
from typing import Callable, Dict, Any, List, Optional

logger = logging.getLogger("OMC-ToolRegistry")

_TOOL_REGISTRY: Dict[str, Dict[str, Any]] = {}


def register_tool(
    name: str,
    description: str,
    agent_ids: List[str],
    category: str = "general",
    parameters: Optional[Dict[str, Any]] = None,
):
    """
    Decorator to register an executable tool.
    
    :param name: Unique name of the tool (e.g. 'generate_viral_hooks')
    :param description: What the tool does and when to use it
    :param agent_ids: List of agent IDs allowed to invoke this tool (or ['*'] for all)
    :param category: Functional category ('social', 'research', 'cskh', 'safety', 'ops')
    :param parameters: Optional JSON-Schema for parameters. If None, auto-generated from signature.
    """
    def decorator(func: Callable):
        param_schema = parameters or _generate_schema_from_signature(func)
        _TOOL_REGISTRY[name] = {
            "name": name,
            "description": description.strip(),
            "category": category,
            "agent_ids": agent_ids,
            "function": func,
            "parameters": param_schema,
        }
        return func
    return decorator


def _generate_schema_from_signature(func: Callable) -> Dict[str, Any]:
    """Generates basic JSON Schema from Python function signature & type hints."""
    sig = inspect.signature(func)
    properties = {}
    required = []

    type_mapping = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
    }

    for param_name, param in sig.parameters.items():
        if param_name in ("self", "cls"):
            continue

        param_type = "string"
        if param.annotation != inspect.Parameter.empty:
            param_type = type_mapping.get(param.annotation, "string")

        prop_def: Dict[str, Any] = {"type": param_type}

        if param.default is inspect.Parameter.empty:
            required.append(param_name)
        else:
            prop_def["default"] = param.default

        properties[param_name] = prop_def

    return {
        "type": "object",
        "properties": properties,
        "required": required,
    }


def get_tool(name: str) -> Optional[Dict[str, Any]]:
    """Retrieves tool definition by name."""
    return _TOOL_REGISTRY.get(name)


def list_all_tools() -> List[Dict[str, Any]]:
    """Returns a list of all registered tool metadata."""
    return [
        {
            "name": t["name"],
            "description": t["description"],
            "category": t["category"],
            "agent_ids": t["agent_ids"],
            "parameters": t["parameters"],
        }
        for t in _TOOL_REGISTRY.values()
    ]


def get_agent_tools(agent_id: str) -> List[Dict[str, Any]]:
    """Retrieves all tools accessible by a specific agent ID."""
    return [
        t for t in _TOOL_REGISTRY.values()
        if "*" in t["agent_ids"] or agent_id in t["agent_ids"]
    ]


def get_openai_tools(agent_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns OpenAI/Hermes/OpenClaw compatible function calling schemas.
    """
    tools = get_agent_tools(agent_id) if agent_id else _TOOL_REGISTRY.values()
    return [
        {
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t["description"],
                "parameters": t["parameters"],
            }
        }
        for t in tools
    ]


def execute_tool(_tool_name: str, **kwargs) -> Dict[str, Any]:
    """
    Executes a registered tool with keyword arguments safely.
    Returns standard dictionary: { "success": bool, "data": Any, "error": Optional[str] }
    """
    if _tool_name not in _TOOL_REGISTRY:
        return {
            "success": False,
            "data": None,
            "error": f"Tool '{_tool_name}' is not registered. Available tools: {list(_TOOL_REGISTRY.keys())}",
        }

    tool_entry = _TOOL_REGISTRY[_tool_name]
    func = tool_entry["function"]

    try:
        result = func(**kwargs)
        return {
            "success": True,
            "tool": _tool_name,
            "data": result,
            "error": None,
        }
    except Exception as e:
        logger.error(f"Error executing tool '{_tool_name}': {e}", exc_info=True)
        return {
            "success": False,
            "tool": _tool_name,
            "data": None,
            "error": str(e),
        }
