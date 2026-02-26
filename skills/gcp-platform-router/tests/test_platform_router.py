import os
import json
import pytest
import sys

# Add scripts directory to path to import route_agent
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))
from route_agent import route_agent

def get_test_cases():
    cases_path = os.path.join(os.path.dirname(__file__), "platform_router_cases.json")
    with open(cases_path, "r") as f:
        return json.load(f)

@pytest.mark.parametrize("case", get_test_cases())
def test_routing_logic(case):
    description = case["description"]
    expected_target = case["expected_target"]
    
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        pytest.skip("GOOGLE_API_KEY not found in environment")
    
    result = route_agent(description, api_key)
    
    assert "deployment_target" in result
    assert result["deployment_target"].lower() == expected_target.lower()
    assert "confidence" in result
    assert "reasons" in result and len(result["reasons"]) > 0
