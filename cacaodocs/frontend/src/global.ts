export interface TypeArgument {
    bg_color: string;
    color: string;
    description: string;
    emoji: string;
    type: string;
}

export interface TypeItem {
    args: Record<string, TypeArgument>;
    description: string;
    function_name: string;
    function_source?: string;
    inputs?: string[];
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

export interface AppData {
    api: ApiEndpoint[];
    docs: DocItem[];
    types: TypeItem[];
}

declare global {
    interface Window {
        globalData?: AppData;
    }
}

export interface TypeDefinition extends TypeItem {
  // TypeItem already has all the fields we need
}