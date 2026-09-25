"""
End-to-End Test Suite for OMC Agent Tools Ecosystem.
Validates:
1. Tool Registry integrity and Schema generation.
2. Social content creation tools (Hooks, Formatting, Visual Prompts).
3. Research and Market Spy tools.
4. CSKH and CRM automation tools (Pricing lookup, Objections, Lead capture).
5. Brand Safety & Compliance tools (Banned claims, Price verification).
"""

import sys
import os
import unittest
from pathlib import Path

# Ensure root directory is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from engines.tools.registry import (
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


class TestAgentToolsEcosystem(unittest.TestCase):

    def test_01_registry_loaded(self):
        """Test that all 13 tools are properly registered."""
        all_tools = list_all_tools()
        self.assertGreaterEqual(len(all_tools), 13)
        tool_names = [t["name"] for t in all_tools]
        expected_tools = [
            "generate_video_script",
            "generate_viral_hooks",
            "format_social_post",
            "generate_visual_prompt",
            "search_market_trends",
            "inspect_competitor_content",
            "extract_customer_painpoints",
            "lookup_pricing",
            "resolve_objection",
            "capture_lead_crm",
            "notify_owner_telegram",
            "audit_brand_safety",
            "verify_price_accuracy"
        ]
        for exp in expected_tools:
            self.assertIn(exp, tool_names)

    def test_02_openai_schemas(self):
        """Test that OpenAI function calling schemas are valid."""
        schemas = get_openai_tools("social-creator")
        self.assertGreaterEqual(len(schemas), 4)
        for s in schemas:
            self.assertEqual(s["type"], "function")
            self.assertIn("name", s["function"])
            self.assertIn("description", s["function"])
            self.assertIn("parameters", s["function"])

    def test_03_generate_viral_hooks(self):
        """Test social viral hook generation tool."""
        res = execute_tool("generate_viral_hooks", topic="Trị nám da", audience="phụ nữ 30+")
        self.assertTrue(res["success"])
        data = res["data"]
        self.assertEqual(data["total_hooks"], 5)
        self.assertTrue(any("Trị nám da" in h["hook_text"] for h in data["hooks"]))

    def test_04_format_social_post(self):
        """Test formatting social post for TikTok and Zalo."""
        res_tt = execute_tool("format_social_post", platform="tiktok", content="Review kem dưỡng ẩm siêu đỉnh")
        self.assertTrue(res_tt["success"])
        self.assertIn("tiktok", res_tt["data"]["platform"])

        res_zl = execute_tool("format_social_post", platform="zalo", content="Báo giá dịch vụ")
        self.assertTrue(res_zl["success"])
        self.assertIn("Kính gửi Quý khách", res_zl["data"]["formatted_post"])

    def test_05_research_market_trends(self):
        """Test market research tool."""
        res = execute_tool("search_market_trends", keyword="Spa làm đẹp")
        self.assertTrue(res["success"])
        self.assertGreaterEqual(len(res["data"]["trending_content_angles"]), 3)

    def test_06_lookup_pricing(self):
        """Test product pricing lookup."""
        res = execute_tool("lookup_pricing", product_keyword="Starter")
        self.assertTrue(res["success"])
        self.assertGreaterEqual(len(res["data"]["matched_products"]), 1)
        self.assertEqual(res["data"]["matched_products"][0]["promo_price"], 1990000)

    def test_07_resolve_objection(self):
        """Test objection resolution scripts."""
        res = execute_tool("resolve_objection", objection_type="price_too_high")
        self.assertTrue(res["success"])
        self.assertIn("Chê giá cao", res["data"]["title"])
        self.assertIn("step_1_empathy", res["data"]["breakdown"])

    def test_08_capture_lead_crm(self):
        """Test lead capture with VN phone validation."""
        # Valid phone
        res_valid = execute_tool("capture_lead_crm", name="Nguyen Van Test", phone="0912345678", platform="Zalo")
        self.assertTrue(res_valid["success"])
        self.assertTrue(res_valid["data"]["success"])
        self.assertEqual(res_valid["data"]["lead"]["phone"], "0912345678")

        # Invalid phone
        res_invalid = execute_tool("capture_lead_crm", name="Bad Phone", phone="123456")
        self.assertTrue(res_invalid["success"])
        self.assertFalse(res_invalid["data"]["success"])
        self.assertIn("không hợp lệ", res_invalid["data"]["error"])

    def test_09_audit_brand_safety(self):
        """Test brand safety auditing for banned claims."""
        # Unsafe content
        res_bad = execute_tool("audit_brand_safety", content="Thuốc nam cam kết 100% trị dứt điểm")
        self.assertTrue(res_bad["success"])
        self.assertFalse(res_bad["data"]["is_safe"])
        self.assertGreaterEqual(res_bad["data"]["total_violations"], 2)

        # Safe content
        res_good = execute_tool("audit_brand_safety", content="Dịch vụ hỗ trợ chăm sóc da chuyên sâu theo phác đồ cá nhân")
        self.assertTrue(res_good["success"])
        self.assertTrue(res_good["data"]["is_safe"])

    def test_10_verify_price_accuracy(self):
        """Test pricing accuracy gatekeeper."""
        # Approved price
        res_ok = execute_tool("verify_price_accuracy", quoted_price=1990000, product_code_or_name="P-01")
        self.assertTrue(res_ok["success"])
        self.assertEqual(res_ok["data"]["status"], "APPROVED")

        # Unauthorized price
        res_bad = execute_tool("verify_price_accuracy", quoted_price=500000, product_code_or_name="P-01")
        self.assertTrue(res_bad["success"])
        self.assertEqual(res_bad["data"]["status"], "REJECTED")


if __name__ == "__main__":
    unittest.main()
