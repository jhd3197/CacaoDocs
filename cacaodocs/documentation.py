# cacaodocs/documentation.py

import re
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import markdown  # Add import for markdown processing
import base64  # Add this import at the top

class CacaoDocs:
    """A class to handle documentation processes for Python code."""

    # Default configuration
    _config = {
        "title": "Documentation",
        "description": "Welcome to the documentation.",
        "version": "1.0.0",
        "theme": {
            "primary_color": "#4CAF50",
            "secondary_color": "#45a049"
        },
        "type_mappings": {
            "api": "API",
            "types": "Types",
            "docs": "Documentation"
        },
        "tag_mappings": {},
        "logo_url": "cacaodocs/templates/assets/img/logo.png"  # Add default logo path
    }

    # Type definitions for badges
    _type_definitions = [
        {
            "type": "str",
            "emoji": "📝",
            "color": "#22C55E",  # green
            "bg_color": "#DCFCE7",
            "contains": ["str", "string"]
        },
        {
            "type": "int",
            "emoji": "🔢",
            "color": "#3B82F6",  # blue
            "bg_color": "#DBEAFE",
            "contains": ["int", "integer", "number"]
        },
        {
            "type": "float",
            "emoji": "🔢",
            "color": "#6366F1",  # indigo
            "bg_color": "#E0E7FF",
            "contains": ["float", "decimal", "double"]
        },
        {
            "type": "bool",
            "emoji": "✓",
            "color": "#EAB308",  # yellow
            "bg_color": "#FEF9C3",
            "contains": ["bool", "boolean"]
        },
        {
            "type": "list",
            "emoji": "📋",
            "color": "#A855F7",  # purple
            "bg_color": "#F3E8FF",
            "contains": ["list", "array"]
        },
        {
            "type": "dict",
            "emoji": "🗂",
            "color": "#EC4899",  # pink
            "bg_color": "#FCE7F3",
            "contains": ["dict", "dictionary", "object"]
        },
        {
            "type": "datetime",
            "emoji": "📅",
            "color": "#64748B",  # slate
            "bg_color": "#F1F5F9",
            "contains": ["datetime", "date", "time"]
        },
        {
            "type": "file",
            "emoji": "📄",
            "color": "#F97316",  # orange
            "bg_color": "#FFEDD5",
            "contains": ["file", "binary", "blob"]
        },
        {
            "type": "email",
            "emoji": "📧",
            "color": "#EF4444",  # red
            "bg_color": "#FEE2E2",
            "contains": ["email", "mail"]
        },
        {
            "type": "url",
            "emoji": "🔗",
            "color": "#06B6D4",  # cyan
            "bg_color": "#CFFAFE",
            "contains": ["url", "uri", "link"]
        },
        {
            "type": "password",
            "emoji": "🔒",
            "color": "#475569",  # slate
            "bg_color": "#F1F5F9",
            "contains": ["password", "secret"]
        },
        {
            "type": "id",
            "emoji": "🔒",
            "color": "#0EA5E9",  # sky
            "bg_color": "#E0F2FE",
            "contains": ["id", "identifier", "uuid"]
        }
    ]

    # Class-level registry
    _registry = {
        'api': [],
        'types': [],
        'docs': []
    }

    # Add custom Jinja2 filters
    @staticmethod
    def _regex_search(value, pattern):
        """Custom filter for regex search."""
        if not value:
            return None
        match = re.search(pattern, str(value))
        return match.groups() if match else None

    @staticmethod
    def _regex_replace(value, pattern, repl=''):
        """Custom filter for regex replace."""
        if not value:
            return value
        return re.sub(pattern, repl, str(value))

    # Update the _jinja_env initialization
    _jinja_env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
        autoescape=select_autoescape(['html', 'xml'])
    )
    _jinja_env.filters['regex_search'] = _regex_search
    _jinja_env.filters['regex_replace'] = _regex_replace

    @classmethod
    def load_config(cls, config_path: Optional[str] = None) -> None:
        """
        Load configuration from a YAML file.

        Args:
            config_path (str, optional): Path to the configuration file.
                Defaults to looking for 'cacao.yaml' in the current directory.
        """
        if config_path is None:
            # Change to load 'cacao.yaml'
            config_path = Path.cwd() / 'cacao.yaml'
        
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                cls._config.update(config)
                print(f"Loaded configuration: {cls._config}")  # Debug line to verify config loading
        except FileNotFoundError:
            print(f"Warning: No configuration file found at {config_path}")
        except yaml.YAMLError as e:
            print(f"Error parsing configuration file: {e}")

    @classmethod
    def get_display_name(cls, doc_type: str) -> str:
        """Get the display name for a documentation type."""
        return cls._config['type_mappings'].get(doc_type, doc_type.title())

    @classmethod
    def get_tag_display(cls, tag: str) -> str:
        """Get the display name for a tag."""
        return cls._config['tag_mappings'].get(tag, tag.title())

    @classmethod
    def configure(cls, **kwargs):
        """
        Configure the documentation settings.

        Args:
            **kwargs: Configuration options including:
                - title (str): Documentation title
                - description (str): Documentation description
                - version (str): API version
                - theme (dict): Theme configuration
        """
        cls._config.update(kwargs)

    @staticmethod
    def parse_docstring(docstring: str, doc_type: str) -> dict:
        """Parse complete docstring information including metadata and sections."""
        if not docstring:
            return {}

        # Basic metadata patterns
        patterns = {
            "endpoint": r"Endpoint:\s*(.*)",
            "method": r"Method:\s*(.*)",
            "version": r"Version:\s*(.*)",
            "status": r"Status:\s*(.*)",
            "last_updated": r"Last Updated:\s*(.*)"
        }

        metadata = {}

        # Extract basic metadata
        for key, pattern in patterns.items():
            match = re.search(pattern, docstring)
            if match:
                metadata[key] = match.group(1).strip()

        # Extract sections with improved Returns handling
        sections = {
            "description": r"Description:\s*(.*?)(?=\n\s*(?:Args|JSON Body|Returns|Raises|$))",
            "args": r"Args:\s*(.*?)(?=\n\s*(?:JSON Body|Returns|Raises|$))",
            "json_body": r"JSON Body:\s*(.*?)(?=\n\s*(?:Returns|Raises|$))",
            "returns": r"Returns:\s*(.*?)(?=\n\s*(?:Raises|$))",
            "raises": r"Raises:\s*(.*?)(?=\n\s*(?:$))"
        }

        # Modified section for handling Args with type extraction
        for section, pattern in sections.items():
            match = re.search(pattern, docstring, re.DOTALL)
            if match:
                content = match.group(1).strip()
                
                # Skip if content is "None"
                if content.lower() == "none":
                    continue
                
                # Special handling for Args section
                if section == "args":
                    args_dict = {}
                    args_lines = content.split('\n')
                    
                    for line in args_lines:
                        line = line.strip()
                        if not line:
                            continue
                            
                        # Check if this is a new argument
                        parts = re.match(r'(\w+)\s*\(([^)]+)\)\s*(?:@|\s)\s*(.*)', line)
                        if parts:
                            arg_name = parts.group(1).strip()
                            arg_type = parts.group(2).strip()
                            arg_desc = parts.group(3).strip()
                            args_dict[arg_name] = {
                                'type': arg_type,
                                'description': arg_desc
                            }
                        else:
                            # Fallback if pattern doesn't match
                            parts = re.match(r'(\w+)\s*\(([^)]+)\)', line)
                            if parts:
                                arg_name = parts.group(1).strip()
                                arg_type = parts.group(2).strip()
                                args_dict[arg_name] = {
                                    'type': arg_type,
                                    'description': ''
                                }
                            else:
                                # If type is missing
                                parts = line.split(':', 1)
                                if len(parts) > 1:
                                    arg_name = parts[0].strip()
                                    arg_desc = parts[1].strip()
                                    args_dict[arg_name] = {
                                        'type': 'Unknown',
                                        'description': arg_desc
                                    }
                                else:
                                    args_dict[line] = {
                                        'type': 'Unknown',
                                        'description': ''
                                    }
                    
                    metadata[section] = args_dict
                    continue

                # Special handling for Returns section
                elif section == "returns":
                    type_pattern = r'@type\{((?:list\[)?(\w+)(?:\])?)\}:\s*(.*)'  # Updated pattern to capture list types
                    type_match = re.search(type_pattern, content, re.IGNORECASE)  # Added case-insensitive flag
                    if type_match:
                        full_type = type_match.group(1)  # e.g., "list[User]" or "User"
                        base_type = type_match.group(2)  # e.g., "User"
                        is_list = full_type.lower().startswith('list[')
                        
                        metadata[section] = {
                            'is_type_ref': True,
                            'type_name': base_type,
                            'is_list': is_list,
                            'full_type': full_type,
                            'description': type_match.group(3).strip()
                        }
                        continue

                # Handle other sections normally
                metadata[section] = content

        return metadata

    @classmethod
    def doc_api(cls, doc_type: str = "api", tag: str = "general"):
        """
        A decorator to capture and store documentation metadata.

        Args:
            doc_type (str): Type of documentation ('api', 'types', 'docs')
            tag (str): Tag for grouping related items
        """
        def decorator(func):
            # Parse the docstring for metadata
            docstring_metadata = cls.parse_docstring(func.__doc__, doc_type)  # Pass doc_type here

            # Merge the decorator arguments and docstring metadata
            metadata = {
                "function_name": func.__name__,
                "tag": tag,
                "type": doc_type
            }
            metadata.update(docstring_metadata)

            # Register this item in the appropriate registry
            if (doc_type in cls._registry):
                cls._registry[doc_type].append(metadata)
            else:
                cls._registry['docs'].append(metadata)  # fallback

            return func
        return decorator

    @classmethod
    def get_json(cls) -> dict:
        """Retrieve the current documentation registry as JSON."""
        return cls._registry

    @classmethod
    def _build_type_nav(cls) -> str:
        """Build the type navigation HTML."""
        nav_items = []
        first_type = None
        for doc_type, items in cls._registry.items():
            if items:
                if first_type is None:
                    first_type = doc_type
                display_name = cls.get_display_name(doc_type)
                style = f'style="border-color: {cls._config["theme"]["primary_color"]}; color: {cls._config["theme"]["primary_color"]};"' if doc_type == first_type else 'style="border-color: transparent; color: #6B7280;"'
                nav_items.append(
                    f'<button data-nav-item="{doc_type}" '
                    f'class="border-b-2 px-4 py-4 text-sm font-medium hover:border-gray-300 hover:text-gray-700" '
                    f'{style} onclick="switchType(\'{doc_type}\')">{display_name}</button>'
                )
        return "\n".join(nav_items)

    @classmethod
    def _build_home_content(cls) -> str:
        """Build the home page content from custom sections in config."""
        sections = []
        
        # Load markdown content for the welcome page
        introduction_md_path = Path.cwd() / 'welcome.md'
        if (introduction_md_path.exists()):
            with open(introduction_md_path, 'r', encoding='utf-8') as f:
                introduction_md = f.read()
                introduction_html = markdown.markdown(introduction_md)
                sections.append(f"""
                <div class="bg-white rounded-lg shadow-md p-6 mb-6">
                    <h2 class="text-2xl font-bold mb-4" style="color: {cls._config['theme']['primary_color']}">Welcome</h2>
                    <div class="prose max-w-none">
                        {introduction_html}
                    </div>
                </div>
                """)
        
        # Add version info
        sections.append(f"""
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 class="text-2xl font-bold mb-4" style="color: {cls._config['theme']['primary_color']}">System Information</h2>
            <dl class="grid grid-cols-2 gap-4">
                <dt class="font-medium">Version</dt>
                <dd>{cls._config.get('version', '1.0.0')}</dd>
            </dl>
        </div>
        """)

        return "\n".join(sections)

    @classmethod
    def _build_content_sections(cls) -> str:
        """Build all content sections with type-based visibility."""
        sections = []
        for doc_type, items in cls._registry.items():
            if items and doc_type != 'api':  # Only handle non-API content here
                sections.append(f'<div data-content="{doc_type}" class="hidden">')
                cards_html = cls._build_card_view(items)  # Just use card view for non-API types
                sections.append(cards_html)
                sections.append('</div>')
        
        # Add API content section
        if cls._registry.get('api'):
            sections.append('<div data-content="api" class="hidden">')
            # API content is handled through API_CARD_CONTENT and API_TABLE_CONTENT placeholders
            sections.append('</div>')
        
        return "\n".join(sections)

    @classmethod
    def _build_sidebar(cls) -> str:
        """Return the HTML for the sidebar menu organized by doc type and tags."""
        nav_items = {}
        for doc_type, items in cls._registry.items():
            if items:
                nav_items[doc_type] = {}
                for item in items:
                    tag = item.get('tag', 'general')
                    nav_items[doc_type].setdefault(tag, []).append(item)

        sidebar_parts = []
        for doc_type, tags in nav_items.items():
            sidebar_parts.append(f'<div data-sidebar="{doc_type}" class="hidden">')  # Ensure data-sidebar attribute is set
            for tag, items in tags.items():
                sidebar_parts.append(f'<div class="mb-4"><h3 class="text-gray-400 text-sm uppercase mt-4">{cls.get_tag_display(tag)}</h3>')
                sidebar_parts.append('<ul class="space-y-2 mt-2">')
                for item in items:
                    if doc_type == 'api':
                        display_name = item.get('endpoint', 'N/A')
                    elif doc_type == 'types':
                        display_name = item.get('function_name', 'N/A')
                    else:
                        display_name = item.get('endpoint') or item.get('function_name') or 'N/A'
                    
                    anchor_id = f"{doc_type}-{item['function_name']}".lower().replace(" ", "-")
                    method = item.get('method', 'N/A').upper() if doc_type == 'api' else ''
                    
                    sidebar_parts.append(f'''
<li>
  <a href="#{anchor_id}" class="block py-1 px-2 hover:bg-gray-700 rounded text-sm flex items-center">
    <span>{display_name}</span>
    {f'<span class="ml-2 px-2 py-0.5 text-xs rounded-full" style="background-color: {cls._config["theme"]["primary_color"]}; color: #FFFFFF;">{method}</span>' if method else ''}
  </a>
</li>
''')
                sidebar_parts.append('</ul></div>')
            sidebar_parts.append('</div>')
        return "\n".join(sidebar_parts)

    @classmethod
    def _build_endpoints_for_type(cls, doc_type: str) -> str:
        """Generate the HTML for documented items of a specific type."""
        return cls._build_endpoints(filter_type=doc_type)

    @classmethod
    def _get_unique_statuses(cls) -> list:
        """Collect all unique statuses from the API documentation."""
        statuses = set()
        for items in cls._registry.values():
            for item in items:
                if status := item.get('status'):
                    statuses.add(status.strip())
        return sorted(list(statuses))

    @classmethod
    def _get_unique_tags(cls) -> list:
        """Collect all unique tags from the API documentation."""
        tags = set()
        for items in cls._registry.values():
            for item in items:
                if tag := item.get('tag'):
                    tags.add(tag.strip())
        return sorted(list(tags))
    
    @classmethod
    def _get_unique_versions(cls) -> list:
        """Collect all unique versions from the API documentation."""
        versions = set()
        for items in cls._registry.values():
            for item in items:
                if version := item.get('version'):
                    versions.add(version.strip())
        return sorted(list(versions))
    
    @classmethod
    def _get_relative_logo_path(cls) -> str:
        """Get the relative path for the logo file."""
        # Get the logo path from config
        logo_path = cls._config.get('logo_url', 'templates/assets/img/logo.png')
        
        # Convert to relative path
        if logo_path.startswith(('/', 'C:', 'D:')):
            # If it's an absolute path, try to make it relative to the project root
            try:
                project_root = Path.cwd()
                logo_path = str(Path(logo_path).relative_to(project_root))
            except ValueError:
                # Fallback to default if we can't make it relative
                logo_path = 'templates/assets/img/logo.png'
        
        # Ensure forward slashes for web compatibility
        return logo_path.replace('\\', '/')

    @classmethod
    def _get_base64_logo(cls) -> str:
        """Get the logo as a base64 encoded string."""
        try:
            # Get the logo path from config
            logo_path = cls._config.get('logo_url', 'templates/assets/img/logo.png')
            
            # Try different base paths to find the logo
            possible_paths = [
                Path.cwd() / logo_path,  # From current working directory
                Path(__file__).parent / logo_path,  # From module directory
                Path(__file__).parent.parent / logo_path,  # From project root
                Path(logo_path)  # Direct path
            ]
            
            # Try each path until we find the logo
            for path in possible_paths:
                if path.exists():
                    with open(path, 'rb') as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode()
                        # Detect image type from file extension
                        image_type = path.suffix.lstrip('.').lower()
                        if image_type not in ['png', 'jpg', 'jpeg', 'gif']:
                            image_type = 'png'  # Default to PNG
                        return f"data:image/{image_type};base64,{encoded_string}"
            
            print(f"Warning: Logo not found in any of these locations: {[str(p) for p in possible_paths]}")
            return ""
            
        except Exception as e:
            print(f"Error loading logo: {e}")
            return ""

    @classmethod
    def get_html(cls) -> str:
        """Generate HTML documentation."""
        template_path = Path.cwd() / 'cacaodocs' / 'templates' / 'cacao_template.html'
        if not template_path.exists():
            return "<h1>Template file not found.</h1>"

        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()

        # Get unique statuses, tags, and versions for the filters
        statuses = cls._get_unique_statuses()
        status_options = '\n'.join([
            '<option value="all">All Statuses</option>'
        ] + [
            f'<option value="{status.lower()}">{status}</option>'
            for status in statuses
        ])
        
        tags = cls._get_unique_tags()
        tag_options = '\n'.join([
            '<option value="all">All Tags</option>'
        ] + [
            f'<option value="{tag.lower()}">{cls.get_tag_display(tag)}</option>'
            for tag in tags
        ])
        
        versions = cls._get_unique_versions()
        version_options = '\n'.join([
            '<option value="all">All Versions</option>'
        ] + [
            f'<option value="{version.lower()}">{version}</option>'
            for version in versions
        ])

        # Build API views
        api_items = cls._registry.get('api', [])
        cards_html = cls._build_card_view(api_items) if api_items else ''
        table_html = cls._build_table_view(api_items) if api_items else ''

        # Get base64 encoded logo
        base64_logo = cls._get_base64_logo()
        print(f"Logo encoded successfully: {bool(base64_logo)}")  # Debug line

        # Replace placeholders
        template = template.replace("{{ TITLE }}", cls._config['title'])
        template = template.replace("{{ DESCRIPTION }}", cls._config['description'])
        template = template.replace("{{ TYPE_NAV }}", cls._build_type_nav())
        template = template.replace("{{ SIDEBAR }}", cls._build_sidebar())
        template = template.replace("{{ HOME_CONTENT }}", cls._build_home_content())
        template = template.replace("{{ STATUS_OPTIONS }}", status_options)
        template = template.replace("{{ TAG_OPTIONS }}", tag_options)
        template = template.replace("{{ VERSION_OPTIONS }}", version_options)
        template = template.replace("{{ API_CARD_CONTENT }}", cards_html)
        template = template.replace("{{ API_TABLE_CONTENT }}", table_html)
        template = template.replace("{{ CONTENT_SECTIONS }}", cls._build_content_sections())
        template = template.replace("{{ PRIMARY_COLOR }}", cls._config['theme']['primary_color'])
        template = template.replace("{{ logo_url }}", base64_logo)

        return template

    @classmethod
    def _build_endpoints(cls, filter_type: str = None) -> tuple[str, str]:
        """Generate both card and table views for documented items."""
        items = cls._registry.get(filter_type, []) if filter_type else [
            item for items in cls._registry.values() for item in items
        ]
        
        # Build card view
        cards_html = cls._build_card_view(items)
        # Build table view
        table_html = cls._build_table_view(items)
        
        return cards_html, table_html

    @classmethod
    def _build_card_view(cls, items: list) -> str:
        """Generate the card view HTML for documented items using Jinja template."""
        template = cls._jinja_env.get_template('components/api_card.html')
        html = []
        
        for item in items:
            # Ensure args is always a dictionary
            args = item.get('args', {})
            if isinstance(args, str):
                args = {'args': args}  # Convert string to simple dictionary
            
            # Ensure json_body is a dictionary if it's a valid JSON string
            json_body = item.get('json_body')
            if isinstance(json_body, str):
                try:
                    json_body = json.loads(json_body)
                except json.JSONDecodeError:
                    json_body = {"content": json_body}  # Fallback to a simple dictionary
            
            # Prepare context for the template
            returns_data = item.get('returns', {})
            if isinstance(returns_data, str):
                returns_data = {'is_type_ref': False, 'content': returns_data}
            
            context = {
                'anchor_id': f"types-{item['function_name']}".lower().replace(" ", "-"),  # Ensure prefix is 'types-'
                'method': item.get('method', '').lower(),
                'status': item.get('status', '').lower(),
                'endpoint': item.get('endpoint', '').lower(),
                'version': item.get('version', '').lower(),
                'tag': item.get('tag', 'general'),
                'description': item.get('description', ''),
                'is_api_type': item.get('type', '').lower() == 'api',
                'has_metadata': any(item.get(key) for key in ['endpoint', 'method', 'last_updated']),
                'function_name': item['function_name'],
                'metadata': [
                    ('Endpoint', item.get('endpoint')),
                    ('Method', item.get('method')),
                    ('Last Updated', item.get('last_updated'))
                ],
                'args': args,  # Now guaranteed to be a dictionary
                'json_body': json_body,
                'returns': returns_data,
                'raises': item.get('raises'),
                'registry': cls._registry,  # Add the registry to the context
                'PRIMARY_COLOR': cls._config['theme']['primary_color'],
                'type_definitions': cls._type_definitions  # Add type definitions to context
            }
            
            html.append(template.render(**context))
        
        return "\n".join(html)

    @classmethod
    def _build_table_view(cls, items: list) -> str:
        """Generate the table view HTML for documented items using Jinja template."""
        template = cls._jinja_env.get_template('components/api_table.html')
        return template.render(
            items=items,
            PRIMARY_COLOR=cls._config['theme']['primary_color']  # Add this line
        )

