// CacaoDocs v2 Type Definitions

export interface ArgDoc {
    name: string;
    type: string;
    description: string;
    default: string | null;
}

export interface ReturnDoc {
    type: string;
    description: string;
}

export interface RaiseDoc {
    type: string;
    description: string;
}

export interface ParsedDocstring {
    summary: string;
    description: string;
    args: ArgDoc[];
    returns: ReturnDoc | null;
    raises: RaiseDoc[];
    examples: string[];
    attributes: ArgDoc[];
    notes: string[];
}

export interface MethodDoc {
    name: string;
    module: string;
    signature: string;
    docstring: ParsedDocstring;
    is_async: boolean;
    is_classmethod: boolean;
    is_staticmethod: boolean;
    is_property: boolean;
    source: string;
    line_number: number;
    decorators: string[];
}

export interface FunctionDoc {
    name: string;
    module: string;
    full_path: string;
    signature: string;
    docstring: ParsedDocstring;
    is_async: boolean;
    source: string;
    line_number: number;
    decorators: string[];
}

export interface ClassDoc {
    name: string;
    module: string;
    full_path: string;
    docstring: ParsedDocstring;
    bases: string[];
    methods: MethodDoc[];
    source: string;
    line_number: number;
    decorators: string[];
}

export interface ModuleDoc {
    name: string;
    full_path: string;
    file_path: string;
    docstring: string;
    classes: ClassDoc[];
    functions: FunctionDoc[];
}

export interface PageDoc {
    title: string;
    slug: string;
    content: string;
    file_path: string;
    order: number;
}

export interface Config {
    title: string;
    description: string;
    version: string;
    logo_url: string;
    github_url: string;
    footer_text: string;
    google_analytics_id: string;
    clarity_id: string;
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
    };
}

export interface AppData {
    modules: ModuleDoc[];
    classes: ClassDoc[];
    functions: FunctionDoc[];
    pages: PageDoc[];
    config: Config;
}

declare global {
    interface Window {
        globalData?: AppData;
    }
}

// Helper type for counting items
export interface DocumentationStats {
    moduleCount: number;
    classCount: number;
    functionCount: number;
    methodCount: number;
    pageCount: number;
}

export function getStats(data: AppData): DocumentationStats {
    const methodCount = data.classes.reduce(
        (sum, cls) => sum + cls.methods.length,
        0
    );

    return {
        moduleCount: data.modules.length,
        classCount: data.classes.length,
        functionCount: data.functions.length,
        methodCount,
        pageCount: data.pages.length,
    };
}
