import React, { useEffect, useState, useMemo } from "react";
import FlexSearch from "flexsearch";
import { Modal, Input, Card, Tag, Space, Radio } from "antd";
import { useHotkeys } from "react-hotkeys-hook";
import { useNavigate } from "react-router-dom";

interface SearchItem {
  type: "api" | "doc" | "type";
  name: string;
  content: string;
  description: string;
  tag?: string;
  path: string;
  function_source?: string;  // <--- new property for code
  method?: string;  // Add method field
}

interface GlobalSearchProps {
  data: {
    api: Array<{
      endpoint: string;
      function_name?: string;
      description: string;
      function_source?: string; // <--- code snippet
      method?: string; // Add method
    }>;
    docs: Array<{
      function_name: string;
      tag?: string;
      description: string;
      function_source?: string; // <--- code snippet
    }>;
    types: Array<{
      function_name: string;
      tag?: string;
      description: string;
      function_source?: string; // <--- code snippet
    }>;
  };
}

/**
 * highlightText: Simple substring highlight using <mark>.
 * For more robust highlighting, consider a library (e.g. react-highlight-words).
 */
const highlightText = (text: string, query: string) => {
  if (!query) return text;
  const regex = new RegExp(`(${query})`, "gi");
  const parts = text.split(regex);

  return parts.map((part, i) =>
    part.toLowerCase() === query.toLowerCase() ? (
      <mark key={i}>{part}</mark>
    ) : (
      part
    )
  );
};

/**
 * getSnippet: Return a snippet of `fullText` around the first match of `query`.
 * E.g.  if snippetLen=60, we show ~30 chars before and 30 after the match.
 */
const getSnippet = (
  fullText: string,
  query: string,
  snippetLen = 60
): string => {
  if (!fullText) return "";
  if (!query) {
    // If no query, just show the first snippetLen chars
    const snippet = fullText.slice(0, snippetLen);
    return snippet + (fullText.length > snippetLen ? "..." : "");
  }
  const lowerText = fullText.toLowerCase();
  const lowerQuery = query.toLowerCase();
  const index = lowerText.indexOf(lowerQuery);

  if (index < 0) {
    // If we can't find the query, just take the first snippetLen chars
    const snippet = fullText.slice(0, snippetLen);
    return snippet + (fullText.length > snippetLen ? "..." : "");
  }

  // Start ~half snippetLen before the match
  const half = Math.floor(snippetLen / 2);
  const start = Math.max(0, index - half);
  const end = Math.min(fullText.length, index + lowerQuery.length + half);

  let snippet = fullText.slice(start, end);

  if (start > 0) snippet = "..." + snippet;
  if (end < fullText.length) snippet = snippet + "...";

  return snippet;
};

const GlobalSearch: React.FC<GlobalSearchProps> = ({ data }) => {
  const [visible, setVisible] = useState(false);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchItem[]>([]);
  const [filterType, setFilterType] = useState<"all" | "api" | "doc" | "type">("all");
  const [searchMode, setSearchMode] = useState<"description" | "code">("description");

  const navigate = useNavigate();

  const getTypeColor = (type: string) => {
    switch (type) {
      case "api":
        return { color: "#1890ff", bg: "#4892b5" };
      case "doc":
        return { color: "#52c41a", bg: "#85aa5f" };
      case "type":
        return { color: "#722ed1", bg: "#9e7cb5" };
      default:
        return { color: "#000000", bg: "#b66767" };
    }
  };

  const handleItemClick = (item: SearchItem) => {
    setVisible(false);
    
    setTimeout(() => {
      // Extract the endpoint type from item.type
      const endpointType = item.type === 'api' ? 'api' : 
                          item.type === 'type' ? 'types' : 'docs';
      
      // Clean up any existing prefixes and add the correct one
      const targetHash = item.path.split('#').slice(1).join('#');
      const cleanHash = targetHash.replace(/^\/(?:api|types|docs)#/, '');
      const newPath = `/#/${endpointType}#${cleanHash}`;
      
      // Use replace instead of pushState for more reliable hash changes
      window.location.replace(newPath);
      
      // Dispatch custom event with cleaned hash and type
      const navigationEvent = new CustomEvent('navigationRequest', {
        detail: { hash: cleanHash, type: endpointType }
      });
      window.dispatchEvent(navigationEvent);
    }, 100);
  };

  // Prebuild 2 indexes: one for normal (description) and one for code
  const indexDescription = useMemo(() => FlexSearch.create(), []);
  const indexCode = useMemo(() => FlexSearch.create(), []);

  // Build the items array once
  const combinedItems = useMemo(() => {
    const items: SearchItem[] = [
      ...data.api.map((x) => ({
        type: "api" as const,
        name: x.endpoint,
        content: x.function_name || "",
        description: x.description,
        path: `/#/api#${x.endpoint}-${x.method}`, // Include method in path
        tag: "API",
        function_source: x.function_source,
        method: x.method // Add method
      })),
      ...data.docs.map((x) => ({
        type: "doc" as const,
        name: x.function_name,
        content: "",
        description: x.description,
        path: `/#/docs#${x.function_name}`,
        tag: x.tag,
        function_source: x.function_source
      })),
      ...data.types.map((x) => ({
        type: "type" as const,
        name: x.function_name,
        content: "",
        description: x.description,
        path: `/#/types#${x.function_name}`,
        tag: x.tag,
        function_source: x.function_source
      })),
    ];
    return items;
  }, [data]);

  // On mount (and whenever data changes), rebuild both indexes
  useEffect(() => {
    indexDescription.clear();
    indexCode.clear();

    combinedItems.forEach((item, idx) => {
      // Normal/description index
      const textDesc = `${item.type} ${item.name} ${item.description} ${item.content}`;
      indexDescription.add(idx, textDesc);

      // Code index (fallback to name if no code present)
      const textCode = `${item.type} ${item.name} ${item.function_source || ""}`;
      indexCode.add(idx, textCode);
    });
  }, [combinedItems, indexDescription, indexCode]);

  // Hotkey Ctrl+K to open
  useHotkeys("ctrl+k", (event) => {
    event.preventDefault();
    setVisible(true);
  });

  // Whenever query/filterType/searchMode changes, run search
  useEffect(() => {
    if (!query) {
      setResults([]);
      return;
    }

    const performSearch = async () => {
      // 1) pick which index to use
      const activeIndex =
        searchMode === "description" ? indexDescription : indexCode;

      // 2) do the search
      const foundIDs = await activeIndex.search(query);

      // 3) map IDs back to items
      let matchedItems = foundIDs.map((idx) => combinedItems[idx as any]);

      // 4) filter by type if needed
      if (filterType !== "all") {
        matchedItems = matchedItems.filter((item) => item.type === filterType);
      }

      setResults(matchedItems);
    };

    performSearch();
  }, [query, filterType, searchMode, combinedItems, indexDescription, indexCode]);

  return (
    <Modal
      open={visible}
      footer={null}
      onCancel={() => setVisible(false)}
      title="Global Search"
      width={600}
      maskClosable
      bodyStyle={{
        display: "flex",
        flexDirection: "column",
        maxHeight: "70vh",
        padding: 0,
      }}
    >
      {/* Header area: search + filters */}
      <div style={{ padding: 16, borderBottom: "1px solid #f0f0f0" }}>
        <Input
          placeholder="Type to search..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          autoFocus
          size="large"
          style={{ marginBottom: 16 }}
        />

        <Space wrap>
          {/* Type Filter */}
          <Radio.Group
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
          >
            <Radio value="all">All</Radio>
            <Radio value="api">API</Radio>
            <Radio value="doc">Doc</Radio>
            <Radio value="type">Type</Radio>
          </Radio.Group>

          {/* Search Mode (Description vs Code) */}
          <Radio.Group
            value={searchMode}
            onChange={(e) => setSearchMode(e.target.value)}
          >
            <Radio value="description">Description</Radio>
            <Radio value="code">Code</Radio>
          </Radio.Group>
        </Space>
      </div>

      {/* Scrollable results area */}
      <div
        style={{
          flex: 1,
          overflowY: "auto",
          padding: 16,
        }}
      >
        <Space direction="vertical" style={{ width: "100%" }}>
          {results.map((item, index) => {
            const typeColors = getTypeColor(item.type);

            // If we're in "code" mode, show snippet from function_source
            // Otherwise, show the item.description
            const snippetText =
              searchMode === "code"
                ? getSnippet(item.function_source || "", query, 80)
                : item.description;

            return (
              <Card
                key={index}
                size="small"
                style={{ cursor: "pointer" }}
                onClick={() => handleItemClick(item)}
              >
                <Space direction="vertical" size={2} style={{ width: "100%" }}>
                  <Space>
                    <Tag
                      color={typeColors.color}
                      style={{
                        backgroundColor: typeColors.bg,
                        border: "none",
                      }}
                    >
                      {item.type.toUpperCase()}
                    </Tag>
                    {item.method && (
                      <Tag color="#331201">{item.method}</Tag>
                    )}
                    {item.tag && <Tag color="blue">{item.tag}</Tag>}
                  </Space>

                  {/* Name */}
                  <div style={{ fontWeight: "bold" }}>
                    {highlightText(item.name, query)}
                  </div>

                  {/* Description or Code Snippet */}
                  <div style={{ color: "#666", whiteSpace: "pre-wrap" }}>
                    {highlightText(snippetText, query)}
                  </div>
                </Space>
              </Card>
            );
          })}
        </Space>
      </div>
    </Modal>
  );
};

export default GlobalSearch;
