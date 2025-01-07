# cacaodocs/documentation.py
import re
import json
import yaml
import inspect
from pathlib import Path
from typing import Dict, List, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import markdown
import base64
from .type_definitions import TYPE_DEFINITIONS
from bs4 import BeautifulSoup
import textwrap
from datetime import datetime
import logging
import io
import zipfile
import shutil

class CacaoDocs:
    """A class to handle documentation processes for Python code."""

    _logger = logging.getLogger(__name__)  # Add this line

    # Default config includes 'verbose': False so logs are off by default
    _config = {
        "title": "Welcome to CacaoDocs Dashboard",
        "description": "Manage and explore your documentation with ease",
        "version": "1.0.0",
        "theme": {
            "primary_color": "#4CAF50",
            "secondary_color": "#8b5d3b",
            "background_color": "#f5f5f5",
            "text_color": "#331201",
            "sidebar_background_color": "#ffffff",
            "sidebar_text_color": "#331201",
            "sidebar_highlight_background_color": "#736d67",
            "sidebar_highlight_text_color": "#ffffff",
            "highlight_code_background_color": "#3a2f2a",
            "highlight_code_border_color": "#8b5d3b"
        },
        "type_mappings": {
            "api": "API",
            "types": "Types",
            "docs": "Documentation"
        },
        "tag_mappings": {},
        "logo_url": "cacaodocs/templates/assets/img/logo.png",
        "verbose": False,  # Turn on/off verbose logs here or via cacao.yaml
        "exclude_inputs": ["self"]
    }

    _type_definitions = TYPE_DEFINITIONS

    _registry = {
        'api': [],
        'types': [],
        'docs': []
    }

    @staticmethod
    def _regex_search(value, pattern):
        if not value:
            return None
        match = re.search(pattern, str(value))
        return match.groups() if match else None

    @staticmethod
    def _regex_replace(value, pattern, repl=''):
        if not value:
            return value
        return re.sub(pattern, repl, str(value))

    _jinja_env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
        autoescape=select_autoescape(['html', 'xml'])
    )
    _jinja_env.filters['regex_search'] = _regex_search
    _jinja_env.filters['regex_replace'] = _regex_replace

    @classmethod
    def load_config(cls, config_path: Optional[str] = None) -> None:
        """
        Loads a YAML configuration file (cacao.yaml by default) and updates _config.
        """
        if config_path is None:
            config_path = Path.cwd() / 'cacao.yaml'
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                cls._config.update(config)
                if cls._config.get("verbose"):
                    print(f"[CacaoDocs] Loaded configuration: {cls._config}")
        except FileNotFoundError:
            if cls._config.get("verbose"):
                print(f"[CacaoDocs] Warning: No configuration file found at {config_path}")
        except yaml.YAMLError as e:
            if cls._config.get("verbose"):
                print(f"[CacaoDocs] Error parsing configuration file: {e}")

    @classmethod
    def get_display_name(cls, doc_type: str) -> str:
        return cls._config['type_mappings'].get(doc_type, doc_type.title())

    @classmethod
    def get_tag_display(cls, tag: str) -> str:
        return cls._config['tag_mappings'].get(tag, tag.title())

    @classmethod
    def configure(cls, **kwargs):
        """
        Update the configuration in code. Example:
            CacaoDocs.configure(verbose=True)
        """
        cls._config.update(kwargs)
        if cls._config.get("verbose"):
            print("[CacaoDocs] Updated configuration:", cls._config)

    @classmethod
    def parse_docstring(cls, docstring: str, doc_type: str) -> dict:
        """
        Parse the complete docstring to extract custom metadata: Endpoint, Method,
        Description, Responses, and more.
        """
        if not docstring:
            if cls._config.get("verbose"):
                print("[CacaoDocs] No docstring provided.")
            return {}

        # Dedent to remove common leading whitespace
        docstring = textwrap.dedent(docstring)
        if cls._config.get("verbose"):
            print(f"[CacaoDocs] Parsing docstring for doc_type='{doc_type}':\n{docstring}")

        # Patterns to fetch standard metadata lines
        patterns = {
            "endpoint": r"Endpoint:\s*(.*)",
            "method": r"Method:\s*(.*)",
            "version": r"Version:\s*(.*)",
            "status": r"Status:\s*(.*)",
            "last_updated": r"Last Updated:\s*(.*)"
        }

        metadata = {}

        # Extract standard metadata from docstring
        for key, pattern in patterns.items():
            match = re.search(pattern, docstring)
            if match:
                metadata[key] = match.group(1).strip()

                if key == "last_updated":
                    date_str = metadata[key]
                    try:
                        # Attempt to parse ISO datetime with time
                        try:
                            dt = datetime.fromisoformat(date_str)
                        except ValueError:
                            # If parsing with time fails, try parsing date only
                            dt = datetime.strptime(date_str, "%Y-%m-%d")
                        # Convert to ISO 8601 format
                        metadata[key] = dt.isoformat()
                    except ValueError as e:
                        if cls._config.get("verbose"):
                            print(f"[CacaoDocs] Error parsing 'last_updated': {e}")
                        # Handle the error as needed, e.g., set to None or raise an exception
                        metadata[key] = None

                    
                if cls._config.get("verbose"):
                    print(f"[CacaoDocs] Found {key}: {metadata[key]}")

        # Extended sections
        sections = {
            "description": r"Description:\s*(.*?)(?=\n\s*(?:Args|Data|JSON Body|Returns|Raises|Responses|$))",
            "args": r"Args:\s*(.*?)(?=\n\s*(?:Data|JSON Body|Returns|Raises|Responses|$))",
            "json_body": r"(?:Data|JSON Body):\s*(.*?)(?=\n\s*(?:Returns|Raises|Responses|$))",
            "returns": r"Returns:\s*(.*?)(?=\n\s*(?:Raises|Responses|$))",
            "raises": r"Raises:\s*(.*?)(?=\n\s*(?:Responses|$))",
            "responses": r"Responses:\s*(.*?)(?=\n\s*$|$)"
        }

        # Use the above regex to find each section in docstring
        for section, pattern in sections.items():
            match = re.search(pattern, docstring, re.DOTALL)
            if match:
                content = match.group(1).strip()
                if not content or content.lower() == "none":
                    continue

                if section == "responses":
                    # Attempt YAML parse
                    metadata[section] = cls._parse_responses_section(content)
                    continue

                if section == "args":
                    # Parse each line for "arg_name (type): description"
                    args_dict = {}
                    for line in content.split('\n'):
                        line = line.strip()
                        if not line:
                            continue
                        parts = re.match(r'(\w+)\s*\(([^)]+)\)\s*:\s*(.+)?', line)
                        if parts:
                            arg_name = parts.group(1).strip()
                            arg_type = parts.group(2).strip()
                            arg_desc = parts.group(3).strip() if parts.group(3) else ""

                            # Try matching custom types if specified
                            type_def = None
                            for td in cls._type_definitions:
                                name_matches = any(
                                    p in arg_name.lower() for p in td['arg_matches']['name']
                                )
                                type_matches = any(
                                    p == arg_type.lower() for p in td['arg_matches']['type']
                                )
                                if name_matches or type_matches:
                                    type_def = td
                                    break

                            args_dict[arg_name] = {
                                'type': arg_type,
                                'description': arg_desc,
                                'emoji': type_def['emoji'] if type_def else '📎',
                                'color': type_def['color'] if type_def else '#c543ab',
                                'bg_color': type_def['bg_color'] if type_def else '#F3F4F6'
                            }
                    metadata[section] = args_dict
                    continue

                if section == "returns":
                    # Looking for a pattern like @type{list[User]}: Some description
                    type_pattern = r'@type\{((?:list\[)?(\w+)(?:\])?)\}:\s*(.*)'
                    type_match = re.search(type_pattern, content, re.IGNORECASE)
                    if type_match:
                        full_type = type_match.group(1)
                        base_type = type_match.group(2)
                        is_list = full_type.lower().startswith('list[')

                        metadata[section] = {
                            'is_type_ref': True,
                            'type_name': base_type,
                            'is_list': is_list,
                            'full_type': full_type,
                            'description': type_match.group(3).strip()
                        }
                    else:
                        metadata[section] = content
                    continue

                # For description, json_body, raises, store the raw content
                metadata[section] = content

        if cls._config.get("verbose"):
            print("[CacaoDocs] Finished parsing docstring metadata:", metadata)
        return metadata
    
    @staticmethod
    def _parse_responses_section(responses_section: str) -> dict:
        """
        A fully custom parser for a minimal, YAML-like 'Responses' section.
        It allows arbitrary keys under 'Responses:' like 'Data:', '201:', etc.
        Each block can have multiple fields, e.g.:

            Data:
                description: "Some text"
                example: "{\n"key": "value"\n}"
                notes: "Any other field"

        This parser:
        - Detects a top-level key line (e.g., 'Data:' or '201:') by regex
        ^\s*(\S+)\s*:\s*$ at the start of the line.
        - Gathers subsequent lines until the next top-level key or end of block.
        - Within each block, it looks for subfields like 'description:', 'example:', 'anythingElse:'.
        - For multiline content (like JSON under 'example:'), it accumulates lines until
        the next subfield or the block ends.

        Returns a dictionary where each top-level key has a dict of subfields.
        Example output:
        {
        "Data": {
            "example": "{\n    \"key\": \"value\"\n}",
            "notes": "Any other field"
        }
        }
        """

        # 1. Split the entire block into lines
        lines = responses_section.strip().splitlines()

        # The final structure: { "Data": {...}, "201": {...}, ... }
        final_responses = {}

        # We track the "current block key" (e.g. 'Data') and the lines belonging to it
        current_block_key = None
        block_lines = []

        # Regex to detect a top-level block key line, e.g. "Data:" or "201:" or "MyKey:"
        block_key_pattern = re.compile(r'^\s*(\S+)\s*:\s*$')

        def parse_fields(lines_block: list[str]) -> dict:
            """
            Parse a block of lines like:
                description: "Hello!"
                example:
                    {
                        "foo": "bar"
                    }
                notes: "anything"

            Return a dict of the form:
            {
            "description": "Hello!",
            "example": "{\n    \"foo\": \"bar\"\n}",
            "notes": "anything"
            }

            We look for lines matching 'key:' to start a field. Subsequent lines
            (indented or not) accumulate until the next field or end of block.
            """
            result = {}
            current_field = None
            buffer = []

            field_pattern = re.compile(r'^\s*([^:]+)\s*:\s*(.*)$')  
            # e.g. "description:" => group(1)="description", group(2)=maybe "Hello!" or empty

            for line in lines_block:
                stripped = line.rstrip()
                if not stripped:
                    # Blank line, keep as part of buffer or skip?
                    if current_field:
                        buffer.append("")
                    continue

                match = field_pattern.match(stripped)
                if match:
                    # We found a new field definition, so store the old field buffer first
                    if current_field:
                        # Store the previous field content
                        result[current_field] = "\n".join(buffer).strip()
                    # Reset for the new field
                    current_field = match.group(1).strip()
                    first_value = match.group(2).strip()  # Remainder on the same line
                    buffer = []
                    if first_value:
                        buffer.append(first_value)
                else:
                    # This line is a continuation of the current field's content
                    if current_field:
                        buffer.append(stripped)

            # At the end, store whatever was in the buffer
            if current_field:
                result[current_field] = "\n".join(buffer).strip()

            return result

        # 2. Iterate through lines to find top-level block keys
        for line in lines:
            # Check if line is a block key
            m = block_key_pattern.match(line)
            if m:
                # If we already have a current block, parse its lines
                if current_block_key is not None:
                    parsed_fields = parse_fields(block_lines)
                    final_responses[current_block_key] = parsed_fields

                # Start a new block
                current_block_key = m.group(1)
                block_lines = []
            else:
                # This line belongs to the current block
                block_lines.append(line)

        # 3. If there's a trailing block at the end, parse it
        if current_block_key is not None:
            parsed_fields = parse_fields(block_lines)
            final_responses[current_block_key] = parsed_fields

        return final_responses

    @classmethod
    def doc_api(cls, doc_type: str = "api", tag: str = "general"):
        """
        A decorator to capture and store documentation metadata.

        Args:
            doc_type (str): Type of documentation ('api', 'types', 'docs')
            tag (str): Tag for grouping related items
        """
        def decorator(func):
            # Grab the docstring
            docstring = func.__doc__ or ""
            # Parse out the metadata
            docstring_metadata = cls.parse_docstring(docstring, doc_type)

            # Start building the metadata dictionary
            metadata = {
                "function_name": func.__name__,
                "tag": tag,
                "type": doc_type
            }
            metadata.update(docstring_metadata)

            # Attempt to get source code
            try:
                source = inspect.getsource(func)
                metadata["function_source"] = source
            except OSError:
                metadata["function_source"] = None

            # Gather info on parameters (inputs) and return annotations
            signature = inspect.signature(func)
            exclude = cls._config.get("exclude_inputs", [])
            metadata["inputs"] = [p for p in signature.parameters.keys() if p not in exclude]
            return_annotation = signature.return_annotation
            metadata["outputs"] = (
                str(return_annotation) if return_annotation is not inspect.Signature.empty else None
            )

            # Auto-detect Flask route info from source
            route_pattern = re.compile(
                r'@app\.route\(\s*[\'"](.+?)[\'"]\s*(?:,\s*methods\s*=\s*\[([^\]]+)\])?\)'
            )
            route_match = route_pattern.search(source) if source else None
            if route_match:
                route = route_match.group(1).strip()
                methods_str = route_match.group(2)
                if methods_str:
                    raw_methods = re.findall(r"[A-Z]+", methods_str.upper())
                    flask_methods = [m for m in raw_methods]
                else:
                    flask_methods = ["GET"]  # default if not specified

                if not metadata.get("endpoint"):
                    metadata["endpoint"] = route

                if not metadata.get("method"):
                    metadata["method"] = ", ".join(flask_methods)

            if cls._config.get("verbose"):
                print(f"[CacaoDocs] Final metadata for {func.__name__}:", metadata)

            # Register in global registry
            if doc_type in cls._registry:
                cls._registry[doc_type].append(metadata)
            else:
                cls._registry['docs'].append(metadata)

            return func

        return decorator

    @classmethod
    def get_one_of_each(cls) -> dict:
        """Retrieve one configuration from each category."""
        one_of_each = {}
        for key, items in cls._registry.items():
            # if key is "types" then set all the items
            if key == "types":
                one_of_each[key] = items
            else:
                one_of_each[key] = items[0] if items else None
        return one_of_each

    @classmethod
    def get_two_of_each(cls) -> dict:
        """Retrieve two configurations from each category."""
        two_of_each = {}
        for key, items in cls._registry.items():
            if key == "types":
                two_of_each[key] = items
            else:
                two_of_each[key] = items[:2] if len(items) >= 2 else items
        return two_of_each

    @classmethod
    def get_four_of_each(cls) -> dict:
        """Retrieve four configurations from each category."""
        four_of_each = {}
        for key, items in cls._registry.items():
            four_of_each[key] = items[:4] if len(items) >= 4 else items
        return four_of_each

    @classmethod
    def get_json(cls) -> dict:
        """Retrieve the current documentation registry as JSON."""
        return {
            **cls._registry,
            "configs": cls._config
        }

    @classmethod
    def get_html(cls) -> str:
        # Retrieve JSON content
        json_content = cls.get_json()
    
        # Dynamically calculate the path to index.html based on the current file location
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"Current directory: {current_dir}")  # Replace print with logging
        index_html_path = os.path.join(current_dir, "frontend", "build", "index.html")
    
        # Read the HTML file
        try:
            with open(index_html_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
            cls._logger.debug(f"Successfully read {index_html_path}")  # Replace print with logging
        except FileNotFoundError:
            raise FileNotFoundError(f"index.html not found at path: {index_html_path}")
        except Exception as e:
            raise Exception(f"An error occurred while reading index.html: {e}")
        
        # Initialize BeautifulSoup for HTML parsing
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Inline CSS files
        for link_tag in soup.find_all('link', rel='stylesheet'):
            href = link_tag.get('href')
            if href and not href.startswith('http'):  # Skip external links
                css_path = os.path.join("cacaodocs", "frontend", "build", href.lstrip('/'))
                try:
                    with open(css_path, 'r', encoding='utf-8') as css_file:
                        css_content = css_file.read()
                    # Create a new <style> tag
                    style_tag = soup.new_tag('style')
                    style_tag.string = css_content
                    # Replace the <link> tag with the <style> tag
                    link_tag.replace_with(style_tag)
                    cls._logger.debug(f"Inlined CSS from {css_path}")  # Replace print with logging
                except FileNotFoundError:
                    cls._logger.debug(f"CSS file not found: {css_path}. Skipping inlining for this file.")  # Replace print with logging
                except Exception as e:
                    cls._logger.debug(f"Error inlining CSS file {css_path}: {e}. Skipping inlining for this file.")  # Replace print with logging
        
        # Inline JavaScript files
        for script_tag in soup.find_all('script', src=True):
            src = script_tag.get('src')
            if src and not src.startswith('http'):  # Skip external scripts
                js_path = os.path.join("cacaodocs", "frontend", "build", src.lstrip('/'))
                try:
                    with open(js_path, 'r', encoding='utf-8') as js_file:
                        js_content = js_file.read()
                    # Create a new <script> tag without the src attribute
                    new_script_tag = soup.new_tag('script')
                    new_script_tag.string = js_content
                    # Replace the old <script> tag with the new one
                    script_tag.replace_with(new_script_tag)
                    cls._logger.debug(f"Inlined JavaScript from {js_path}")  # Replace print with logging
                except FileNotFoundError:
                    cls._logger.debug(f"JavaScript file not found: {js_path}. Skipping inlining for this file.")  # Replace print with logging
                except Exception as e:
                    cls._logger.debug(f"Error inlining JavaScript file {js_path}: {e}. Skipping inlining for this file.")  # Replace print with logging
        
        # Find the existing script tag that defines window.globalData
        script_tags = soup.find_all('script')
        global_data_script_found = False
        for script in script_tags:
            if script.string and 'window.globalData' in script.string:
                cls._logger.debug("Found existing window.globalData script tag. Updating it.")  # Replace print with logging
                # Serialize the JSON content to a JavaScript object string
                json_js = json.dumps(json_content, ensure_ascii=False, indent=4)
                # Update the script content
                script.string = f"window.globalData = {json_js};"
                global_data_script_found = True
                break
        
        if not global_data_script_found:
            cls._logger.debug("No existing window.globalData script tag found. Creating a new one.")  # Replace print with logging
            # Serialize the JSON content to a JavaScript object string
            json_js = json.dumps(json_content, ensure_ascii=False, indent=4)
            new_script_tag = soup.new_tag('script')
            new_script_tag.string = f"window.globalData = {json_js};"
            # Insert the new script tag before the closing </body> tag
            if soup.body:
                soup.body.append(new_script_tag)
                cls._logger.debug("Appended new window.globalData script tag to <body>.")  # Replace print with logging
            else:
                # If <body> is not found, append the script at the end of the HTML
                soup.append(new_script_tag)
                cls._logger.debug("Appended new window.globalData script tag to the end of the HTML.")  # Replace print with logging
        
        # Convert the modified soup back to a string
        updated_html = str(soup)
        cls._logger.debug("HTML content successfully updated.")  # Replace print with logging
        
        return updated_html

    @classmethod
    def get_zip(cls, output_path: Optional[str] = None) -> bytes:
        """
        Generate a zip file containing the documentation with all assets.
        
        Args:
            output_path (Optional[str]): Path where to save the zip file. 
                                       If None, returns the bytes without saving.
        
        Returns:
            bytes: The zip file content as bytes
        """
        try:
            # Create an in-memory zip file
            zip_buffer = io.BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Get the build directory path
                current_dir = Path(__file__).parent
                build_dir = current_dir / "frontend" / "build"
                
                if not build_dir.exists():
                    raise FileNotFoundError(f"Build directory not found at {build_dir}")
                
                cls._logger.info(f"Creating documentation zip from {build_dir}")
                
                # Get JSON content for the documentation
                json_content = cls.get_json()
                
                # Read and modify index.html
                index_path = build_dir / "index.html"
                if not index_path.exists():
                    raise FileNotFoundError(f"index.html not found at {index_path}")
                
                # Add all files from build directory
                for path in build_dir.rglob('*'):
                    if path.is_file():
                        try:
                            archive_path = path.relative_to(build_dir)
                            cls._logger.debug(f"Adding {path} to zip as {archive_path}")
                            
                            # Special handling for index.html
                            if path.name == 'index.html':
                                with open(path, 'r', encoding='utf-8') as f:
                                    html_content = f.read()
                                
                                # Modify the HTML to include the JSON data
                                soup = BeautifulSoup(html_content, 'html.parser')
                                json_js = json.dumps(json_content, ensure_ascii=False, indent=4)
                                
                                # Update or add globalData script
                                script_found = False
                                for script in soup.find_all('script'):
                                    if script.string and 'window.globalData' in script.string:
                                        script.string = f"window.globalData = {json_js};"
                                        script_found = True
                                        break
                                
                                if not script_found:
                                    new_script = soup.new_tag('script')
                                    new_script.string = f"window.globalData = {json_js};"
                                    soup.body.append(new_script)
                                
                                zip_file.writestr(str(archive_path), str(soup))
                            else:
                                # For all other files, add them as-is
                                with open(path, 'rb') as f:
                                    zip_file.writestr(str(archive_path), f.read())
                        except Exception as e:
                            cls._logger.warning(f"Error adding file {path} to zip: {e}")
                            continue
            
            # Get the zip file content
            zip_content = zip_buffer.getvalue()
            
            # If output_path is provided, save the zip file
            if output_path:
                output_path = Path(output_path)
                # Create directory if it doesn't exist
                output_path.parent.mkdir(parents=True, exist_ok=True)
                # Write the zip file
                with open(output_path, 'wb') as f:
                    f.write(zip_content)
                cls._logger.info(f"Documentation zip saved to {output_path}")
            
            return zip_content
            
        except Exception as e:
            cls._logger.error(f"Error generating zip file: {e}")
            raise

    @classmethod
    def get_docs(cls, output_dir: str) -> None:
        """
        Generate documentation files in the specified directory.
        If the directory exists, it will be deleted and recreated.
        
        Args:
            output_dir (str): Path where to generate the documentation files
        """
        try:
            output_path = Path(output_dir)
            
            # Delete the directory if it exists
            if output_path.exists():
                cls._logger.info(f"Removing existing directory: {output_path}")
                shutil.rmtree(output_path)
            
            # Create the directory
            output_path.mkdir(parents=True, exist_ok=True)
            cls._logger.info(f"Created directory: {output_path}")
            
            # Get JSON content for the documentation
            json_content = cls.get_json()
            
            # Get the build directory path
            current_dir = Path(__file__).parent
            build_dir = current_dir / "frontend" / "build"
            
            if not build_dir.exists():
                raise FileNotFoundError(f"Build directory not found at {build_dir}")
            
            # Copy all files from build directory
            for path in build_dir.rglob('*'):
                if path.is_file():
                    try:
                        # Calculate relative path
                        relative_path = path.relative_to(build_dir)
                        # Calculate destination path
                        dest_path = output_path / relative_path
                        # Create parent directories if they don't exist
                        dest_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        # Special handling for index.html
                        if path.name == 'index.html':
                            with open(path, 'r', encoding='utf-8') as f:
                                html_content = f.read()
                            
                            # Modify the HTML to include the JSON data
                            soup = BeautifulSoup(html_content, 'html.parser')
                            json_js = json.dumps(json_content, ensure_ascii=False, indent=4)
                            
                            # Update or add globalData script
                            script_found = False
                            for script in soup.find_all('script'):
                                if script.string and 'window.globalData' in script.string:
                                    script.string = f"window.globalData = {json_js};"
                                    script_found = True
                                    break
                            
                            if not script_found:
                                new_script = soup.new_tag('script')
                                new_script.string = f"window.globalData = {json_js};"
                                soup.body.append(new_script)
                            
                            # Write modified index.html
                            with open(dest_path, 'w', encoding='utf-8') as f:
                                f.write(str(soup))
                        else:
                            # Copy file as-is
                            shutil.copy2(path, dest_path)
                        
                        cls._logger.debug(f"Copied {path} to {dest_path}")
                    
                    except Exception as e:
                        cls._logger.warning(f"Error copying file {path}: {e}")
                        continue
            
            cls._logger.info(f"Documentation generated successfully in {output_dir}")
        
        except Exception as e:
            cls._logger.error(f"Error generating documentation: {e}")
            raise
