TYPE_DEFINITIONS = [
    {
        "type": "id",
        "emoji": "🔑",
        "color": "#0EA5E9",  # sky
        "bg_color": "#E0F2FE",
        "arg_matches": {
            "name": ["id", "identifier", "uuid", "_id"],
            "type": []
        }
    },
    {
        "type": "email",
        "emoji": "📧",
        "color": "#02a6ed",  # red
        "bg_color": "#FEE2E2",
        "arg_matches": {
            "name": ["email", "mail", "sender", "recipient"],
            "type": ["email"]
        }
    },
    {
        "type": "url",
        "emoji": "🔗",
        "color": "#06B6D4",  # cyan
        "bg_color": "#CFFAFE",
        "arg_matches": {
            "name": ["url", "uri", "link", "website", "endpoint"],
            "type": ["url"]
        }
    },
    {
        "type": "password",
        "emoji": "🔒",
        "color": "#475569",  # slate
        "bg_color": "#F1F5F9",
        "arg_matches": {
            "name": ["password", "secret", "key", "token"],
            "type": ["password"]
        }
    },
    {
        "type": "str",
        "emoji": "📝",
        "color": "#22C55E",  # green
        "bg_color": "#DCFCE7",
        "arg_matches": {
            "name": ["name", "title", "description", "text", "label"],
            "type": ["str", "string"]
        }
    },
    {
        "type": "int",
        "emoji": "🔢",
        "color": "#3B82F6",  # blue
        "bg_color": "#DBEAFE",
        "arg_matches": {
            "name": ["count", "quantity", "amount", "number", "age"],
            "type": ["int", "integer", "number"]
        }
    },
    {
        "type": "float",
        "emoji": "🔢",
        "color": "#6366F1",  # indigo
        "bg_color": "#E0E7FF",
        "arg_matches": {
            "name": ["price", "rate", "amount", "balance"],
            "type": ["float", "decimal", "double"]
        }
    },
    {
        "type": "bool",
        "emoji": "✓",
        "color": "#EAB308",  # yellow
        "bg_color": "#FEF9C3",
        "arg_matches": {
            "name": ["is_", "has_", "can_", "should_", "active", "enabled", "visible"],
            "type": ["bool", "boolean"]
        }
    },
    {
        "type": "list",
        "emoji": "📋",
        "color": "#A855F7",  # purple
        "bg_color": "#F3E8FF",
        "arg_matches": {
            "name": ["items", "list", "array", "collection"],
            "type": ["list", "array", "[]"]
        }
    },
    {
        "type": "dict",
        "emoji": "🗂",
        "color": "#EC4899",  # pink
        "bg_color": "#FCE7F3",
        "arg_matches": {
            "name": ["data", "config", "options", "settings", "params"],
            "type": ["dict", "dictionary", "object", "map"]
        }
    },
    {
        "type": "datetime",
        "emoji": "📅",
        "color": "#d97d37",  # slate
        "bg_color": "#F1F5F9",
        "arg_matches": {
            "name": ["date", "time", "created_at", "updated_at", "timestamp"],
            "type": ["datetime", "date", "time"]
        }
    },
    {
        "type": "file",
        "emoji": "📄",
        "color": "#F97316",  # orange
        "bg_color": "#FFEDD5",
        "arg_matches": {
            "name": ["file", "document", "attachment", "upload"],
            "type": ["file", "binary", "blob", "bytes"]
        }
    }
]
