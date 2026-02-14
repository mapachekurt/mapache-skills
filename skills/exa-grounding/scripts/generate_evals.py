import os
import argparse
import sys
# Requires exa_py, python-dotenv, openai (or other LLM client)

try:
    from exa_py import Exa
    from dotenv import load_dotenv
    # In a real scenario, import your LLM client here
except ImportError:
    print("Missing dependencies: uv pip install exa-py python-dotenv")
    sys.exit(1)

load_dotenv()

def generate_evals(topic: str, exa_key: str):
    """
    1. Searches Exa for "difficult interview questions" or "scenarios" for the topic.
    2. Synthesizes them into a Markdown test plan.
    """
    print(f"🕵️‍♀️ Searching for 'Tough Scenarios' regarding: {topic}...")
    exa = Exa(exa_key)
    
    # Search for "exams", "interview questions", "edge cases"
    query = f"difficult interview questions and edge case scenarios for {topic} experts"
    result = exa.search_and_contents(
        query,
        type="neural",
        use_autoprompt=True,
        num_results=5,
        text=True
    )
    
    # Synthesis (Simulated here, would be LLM call in production)
    print("🧠 Synthesizing Verification Suite...")
    
    output = f"# Verification Suite: {topic}\n\n"
    output += "## Goal\nFail the agent if it relies on generic knowledge. Pass only if it cites specific, expert-level constraints found in these sources.\n\n"
    
    for res in result.results:
        output += f"### Scenario Source: {res.title}\n"
        output += f"**URL**: {res.url}\n"
        output += f"> Context: {res.text[:300]}...\n\n"
        output += "**Test Case**:\n- [ ] Ask Agent: <Insert Question Based on Context>\n"
        output += "- [ ] Expected: <Specific Constraint/Fact>\n"
        output += "- [ ] Anti-Pattern: <Generic Answer>\n\n"
        
    filename = f"verification_suite_{topic.replace(' ', '_').lower()}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(output)
        
    print(f"✅ Generated {filename}. Review this BEFORE creating the agent.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    args = parser.parse_args()
    
    key = os.getenv("EXA_API_KEY")
    if not key:
        print("❌ EXA_API_KEY required for eval generation.")
        sys.exit(1)
        
    generate_evals(args.topic, key)

if __name__ == "__main__":
    main()
