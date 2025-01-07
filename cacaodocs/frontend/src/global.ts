export interface TypeArgument {
    bg_color: string;
    color: string;
    description: string;
    function_name: string;
    emoji: string;
    type: string;
    args: Record<string, FieldDefinition>;
    note?: string;
}

export interface FieldDefinition {
  bg_color: string;
  color: string;
  description: string;
  emoji: string;
  type: string;
  note: string;
}

export interface ERNodeData {
  label: string;
  description?: string;
  fields: Record<string, FieldDefinition>;
}

export interface TypeItem {
    args: Record<string, TypeArgument>;
    description: string;
    function_name: string;
    function_source?: string;
    inputs?: string[];
    last_updated: string;
    outputs?: string | null;
    tag: string;
    type: string;
}

export interface ApiEndpoint {
    description: string;
    endpoint: string;
    function_name: string;
    function_source: string;
    inputs: any[];
    args?: Record<string, TypeArgument>;
    method: string;
    outputs: any;
    last_updated: string;
    responses: {
        [key: string]: {
            description: string;
            example: string;
        };
    };
    status: string;
    tag: string;
    type: string;
    version: string;
}

export interface DocItem {
    args: Record<string, TypeArgument>;
    description: string;
    function_name: string;
    function_source: string;
    inputs: string[];
    method: string;
    last_updated: string;
    outputs: any;
    returns: {
        description: string;
        full_type: string;
        is_list: boolean;
        is_type_ref: boolean;
        type_name: string;
    };
    status: string;
    tag: string;
    type: string;
    version: string;
}

interface Config {
    description: string;
    exclude_inputs: string[];
    logo_url: string;
    tag_mappings: Record<string, string>;
    theme: {
        primary_color: string;
        secondary_color: string;
        bg_color: string;
        text_color: string;
        highlight_code_bg_color: string;
        highlight_code_border_color: string;
        sidebar_bg_color: string;
        sidebar_text_color: string;
        sidebar_highlight_bg_color: string;
        sidebar_highlight_text_color: string;
        secondary_sidebar_bg_color: string;
        secondary_sidebar_text_color: string;
        secondary_sidebar_highlight_bg_color: string;
        secondary_sidebar_highlight_text_color: string;
        home_page_welcome_bg_1: string;
        home_page_welcome_bg_2: string;
        home_page_welcome_text_color: string;
        home_page_card_bg_color: string;
        home_page_card_text_color: string;
        code_bg_color: string;
        type_bg_color_1: string;
        type_bg_color_2: string;
        type_text_color: string;
    };
    title: string;
    type_mappings: Record<string, string>;
    verbose: boolean;
    version: string;
}

export interface AppData {
    api: ApiEndpoint[];
    docs: DocItem[];
    types: TypeItem[];
    config: Config;
}

declare global {
    interface Window {
        globalData?: AppData;
    }
}

export interface TypeDefinition extends TypeItem {
}