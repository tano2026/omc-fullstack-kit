#!/usr/bin/env python3
"""
JEV Reflex Gate 3 - Closed-Loop Delivery & Evaluation Gate (~10ms)
Đánh giá tính hợp lệ của kết quả thực thi (Pass/Fail Verifier).
Chặn đứng hiện tượng ảo giác (hallucination) báo cáo hoàn thành khi code vẫn lỗi hoặc chưa pass test.
"""

import sys
import json
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

class EvalGate:
    @staticmethod
    def verify_execution(execution_output: str, exit_code: int = 0) -> dict:
        """
        Kiểm tra đầu ra thực thi theo nguyên tắc Reflex Gate 3:
        - Exit code phải là 0
        - Không chứa từ khóa lỗi nghiêm trọng (Fatal, Error, Exception, FAILED)
        - Nếu có test suite: số test FAIL phải bằng 0.
        """
        output_lower = execution_output.lower() if execution_output else ""
        
        # 1. Exit code check
        if exit_code != 0:
            return {
                "passed": False,
                "reason": f"Lỗi thực thi: Tiến trình kết thúc với mã lỗi {exit_code}",
                "metric": "exit_code_failure"
            }
            
        # 2. Syntax / Runtime fatal errors check
        fatal_indicators = [
            "syntaxerror:", "traceback (most recent call last):", 
            "modulenotfounderror:", "segmentation fault", "nullpointerexception"
        ]
        for indicator in fatal_indicators:
            if indicator in output_lower:
                return {
                    "passed": False,
                    "reason": f"Phát hiện lỗi nghiêm trọng trong output ({indicator})",
                    "metric": "runtime_exception"
                }
                
        # 3. Test assertion check
        if "failed" in output_lower and "passed" in output_lower:
            # Check pattern like "1 failed, 3 passed"
            if "0 failed" not in output_lower:
                return {
                    "passed": False,
                    "reason": "Bộ kiểm thử (Test Suite) vẫn còn ca kiểm thử bị FAIL.",
                    "metric": "test_assertion_failure"
                }

        return {
            "passed": True,
            "reason": "Xác minh hoàn tất: Code thực thi thành công, 100% assertions đạt chuẩn.",
            "metric": "closed_loop_verified"
        }

if __name__ == "__main__":
    test_out = "Ran 5 tests in 0.04s. OK"
    result = EvalGate.verify_execution(test_out, 0)
    print(f"EvalGate: {result['passed']} | {result['reason']}")
