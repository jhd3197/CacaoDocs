import re

class DocstringParser:
    @staticmethod
    def parse_returns(returns_section):
        """Parse the returns section to extract type information."""
        if not returns_section:
            return None

        # Enhance the regex to handle multiple lines and optional spaces
        type_pattern = r'@type\{(\w+)\}:\s*(.*)'
        match = re.search(type_pattern, returns_section, re.DOTALL)

        if match:
            type_name = match.group(1)
            description = match.group(2).strip()
            return {
                'is_type_ref': True,
                'type_name': type_name,
                'description': description
            }
        
        # If no match, return the raw returns_section
        return {
            'is_type_ref': False,
            'content': returns_section
        }

    @staticmethod
    def parse_docstring(docstring):
        """Parse the entire docstring."""
        sections = {}
        current_section = None
        current_content = []

        for line in docstring.split('\n'):
            line = line.strip()
            
            # Check for section headers
            if line and line.endswith(':'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = line[:-1].strip()
                current_content = []
            elif current_section and line:
                current_content.append(line)

        # Add the last section
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()

        # Process the Returns section specially
        if 'Returns' in sections:
            sections['Returns'] = DocstringParser.parse_returns(sections['Returns'])

        return sections
