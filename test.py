#!/usr/bin/env python3
# Test script for CFG2CNF

import subprocess
import sys

def test_grammar(grammar, description):
    print(f"\n===== Testing {description} =====")
    print("Input Grammar:")
    print("\n".join(grammar))
    print("\nOutput:")
    
    # Run the main.py script with the grammar as input
    process = subprocess.run(
        ["python3", "main.py"],
        input="\n".join(grammar) + "\n*\n",
        text=True,
        capture_output=True
    )
    
    # Print the output
    print(process.stdout)
    
    if process.returncode != 0:
        print(f"Error (return code {process.returncode}):")
        print(process.stderr)
        return False
    
    return True

def main():
    # Test cases
    test_cases = [
        (
            ["S -> SaB | aB", "B -> bB | $"],
            "Basic grammar from README"
        ),
        (
            ["S -> AB | BC", "A -> a | aA", "B -> b", "C -> cC | c"],
            "Grammar with multiple rules"
        ),
        (
            ["S -> aSb | $"],
            "Grammar with epsilon"
        ),
        (
            ["S -> A | B", "A -> a", "B -> b"],
            "Grammar with unit productions"
        ),
        (
            ["S -> aBc", "B -> bB | $"],
            "Grammar with mixed terminals and non-terminals"
        )
    ]
    
    # Run the tests
    success = 0
    for grammar, description in test_cases:
        if test_grammar(grammar, description):
            success += 1
    
    print(f"\nTests: {success}/{len(test_cases)} successful")

if __name__ == "__main__":
    main()
