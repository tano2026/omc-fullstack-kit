"""
Test Suite for OMC Agency OS Multi-Brand & Metrics Engine.
"""

import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from engines.brand_manager import (
    list_brands,
    get_active_brand,
    set_active_brand,
    create_brand,
    init_default_brands
)
from engines.metrics_tracker import get_metrics, record_activity


class TestAgencyOS(unittest.TestCase):

    def setUp(self):
        init_default_brands()

    def test_01_default_brands_initialized(self):
        """Test default brands exist."""
        brands = list_brands()
        self.assertGreaterEqual(len(brands), 3)
        brand_ids = [b["id"] for b in brands]
        self.assertIn("tano-agency", brand_ids)
        self.assertIn("an-binh-travel", brand_ids)
        self.assertIn("spa-hoa-mai", brand_ids)

    def test_02_switch_active_brand(self):
        """Test brand switching."""
        set_active_brand("spa-hoa-mai")
        active = get_active_brand()
        self.assertEqual(active["id"], "spa-hoa-mai")

        set_active_brand("tano-agency")
        active_reset = get_active_brand()
        self.assertEqual(active_reset["id"], "tano-agency")

    def test_03_create_new_brand(self):
        """Test 1-click brand onboarding."""
        res = create_brand(
            name="Nha Khoa Smile Care",
            industry="Nha Khoa Thẩm Mỹ",
            hotline="0999.888.777",
            core_offer="Niềng răng trong suốt và Cấy ghép Implant",
            pricing_starter="2.000.000đ",
            pricing_pro="5.500.000đ",
            pricing_vip="15.000.000đ"
        )
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["brand"]["id"], "nha-khoa-smile-care")

        # Verify brand is now active
        active = get_active_brand()
        self.assertEqual(active["id"], "nha-khoa-smile-care")

    def test_04_metrics_and_roi_calculation(self):
        """Test real-time metrics tracking and cost savings calculation."""
        before = get_metrics()
        initial_conv = before["total_conversations"]
        initial_hours = before["total_hours_saved"]

        # Record activities
        record_activity("chat", 10)
        record_activity("video", 2)
        record_activity("lead", 1)

        after = get_metrics()
        self.assertEqual(after["total_conversations"], initial_conv + 10)
        # 10*0.05 + 2*1.5 + 1*0.5 = 0.5 + 3.0 + 0.5 = 4.0 hours added
        self.assertAlmostEqual(after["total_hours_saved"], initial_hours + 4.0, places=1)
        self.assertEqual(after["cost_savings_vnd"], int(after["total_hours_saved"] * after["hourly_rate_vnd"]))


if __name__ == "__main__":
    unittest.main()
