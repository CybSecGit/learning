#!/usr/bin/env python3
import re

def fix_mdx_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    # Variables that commonly cause MDX issues
    variables = [
        'name', 'domain', 'objective', 'inputs', 'outputs', 'examples', 
        'context', 'language', 'analysis', 'system_description', 'error_message', 
        'incident_type', 'timeline', 'affected_systems', 'impact', 'evidence', 
        'response_actions', 'file_path', 'stack_trace', 'function_code', 
        'code_section', 'code'
    ]
    
    for var in variables:
        # Replace \{var\} with HTML entities
        content = content.replace(f'\\{{{var}\\}}', f'&#123;{var}&#125;')
        
        # Also handle cases where backslashes were not used
        # But be careful not to replace legitimate code
        pattern = rf'(?<!`)(?<!#123;)\{{{var}\}}(?!&#125;)(?!`)'
        replacement = f'&#123;{var}&#125;'
        content = re.sub(pattern, replacement, content)
    
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f'Fixed {filename}')

# Fix both files
fix_mdx_file('chapter-11-pattern-based-ai-automation.md')
fix_mdx_file('chapter-12-model-context-protocol-mcp-architecture.md')