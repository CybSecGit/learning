#!/usr/bin/env python3
import re

def clean_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    # Fix malformed patterns from previous runs
    content = re.sub(r'&#123;name&#125;#123;name&#123;name&#125;#125;', 'name', content)
    content = re.sub(r'#123;[^}]*#125;', '', content)
    
    # Clean up any other malformed patterns
    content = re.sub(r'&#123;([^}]+)&#125;#123;[^}]*#125;', r'&#123;\1&#125;', content)
    
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f'Cleaned {filename}')

clean_file('chapter-11-pattern-based-ai-automation.md')
clean_file('chapter-12-model-context-protocol-mcp-architecture.md')