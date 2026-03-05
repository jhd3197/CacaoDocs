import React, { useEffect, useState, useMemo } from "react";
import FlexSearch from "flexsearch";
import { Modal, Input, Card, Tag, Space, Radio } from "antd";
import { useHotkeys } from "react-hotkeys-hook";
import { useNavigate } from "react-router-dom";
import type { AppData } from "../../global";

type SearchItemType = "module" | "class" | "function" | "page";

interface SearchItem {
  type: SearchItemType;
  name: string;
  fullPath: string;
  description: string;
  path: string;
  source?: string;
  module?: string;
}

interface GlobalSearchProps {
  data: AppData;
}

const highlightText = (text: string, query: string) => {
  if (!query || !text) return text;
  const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, "gi");
  const parts = text.split(regex);

  return parts.map((part, i) =>
    part.toLowerCase() === query.toLowerCase() ? (
      <mark key={i}>{part}</mark>
    ) : (
      part
    )
  );
};

const getSnippet = (fullText: string, query: string, snippetLen = 60): string => {
  if (!fullText) return "";
  if (!query) {
    const snippet = fullText.slice(0, snippetLen);
    return snippet + (fullText.length > snippetLen ? "..." : "");
  }
  const lowerText = fullText.toLowerCase();
  const lowerQuery = query.toLowerCase();
  const index = lowerText.indexOf(lowerQuery);

  if (index < 0) {
    const snippet = fullText.slice(0, snippetLen);
    return snippet + (fullText.length > snippetLen ? "..." : "");
  }

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
  const [filterType, setFilterType] = useState<"all" | SearchItemType>("all");
  const [searchMode, setSearchMode] = useState<"description" | "code">("description");

  const navigate = useNavigate();

  const getTypeColor = (type: SearchItemType) => {
    switch (type) {
      case "module":
        return { color: "#1890ff", bg: "#4892b5" };
      case "class":
        return { color: "#722ed1", bg: "#9e7cb5" };
      case "function":
        return { color: "#52c41a", bg: "#85aa5f" };
      case "page":
        return { color: "#fa8c16", bg: "#d4a35c" };
      default:
        return { color: "#000000", bg: "#b66767" };
    }
  };

  const handleItemClick = (item: SearchItem) => {
    setVisible(false);
    navigate(item.path);
  };

  const indexDescription = useMemo(() => FlexSearch.create(), []);
  const indexCode = useMemo(() => FlexSearch.create(), []);

  const combinedItems = useMemo(() => {
    const items: SearchItem[] = [
      ...data.modules.map((m) => ({
        type: "module" as const,
        name: m.name,
        fullPath: m.full_path,
        description: m.docstring || "",
        path: `/modules/${encodeURIComponent(m.full_path)}`,
        source: "",
        module: m.full_path,
      })),
      ...data.classes.map((c) => ({
        type: "class" as const,
        name: c.name,
        fullPath: c.full_path,
        description: c.docstring.summary || c.docstring.description || "",
        path: `/classes/${encodeURIComponent(c.full_path)}`,
        source: c.source,
        module: c.module,
      })),
      ...data.functions.map((f) => ({
        type: "function" as const,
        name: f.name,
        fullPath: f.full_path,
        description: f.docstring.summary || f.docstring.description || "",
        path: `/functions#function-${f.name}`,
        source: f.source,
        module: f.module,
      })),
      ...data.pages.map((p) => ({
        type: "page" as const,
        name: p.title,
        fullPath: p.slug,
        description: p.content.replace(/<[^>]*>/g, '').slice(0, 200),
        path: `/pages/${encodeURIComponent(p.slug)}`,
        source: "",
        module: "",
      })),
    ];
    return items;
  }, [data]);

  useEffect(() => {
    indexDescription.clear();
    indexCode.clear();

    combinedItems.forEach((item, idx) => {
      const textDesc = `${item.type} ${item.name} ${item.fullPath} ${item.description}`;
      indexDescription.add(idx, textDesc);

      const textCode = `${item.type} ${item.name} ${item.source || ""}`;
      indexCode.add(idx, textCode);
    });
  }, [combinedItems, indexDescription, indexCode]);

  useHotkeys("ctrl+k", (event) => {
    event.preventDefault();
    setVisible(true);
  });

  useEffect(() => {
    if (!query) {
      setResults([]);
      return;
    }

    const performSearch = async () => {
      const activeIndex = searchMode === "description" ? indexDescription : indexCode;
      const foundIDs = await activeIndex.search(query);
      let matchedItems = foundIDs.map((idx) => combinedItems[idx as any]);

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
      title="Search Documentation"
      width={600}
      maskClosable
      styles={{
        body: {
          display: "flex",
          flexDirection: "column",
          maxHeight: "70vh",
          padding: 0,
        }
      }}
    >
      <div style={{ padding: 16, borderBottom: "1px solid #f0f0f0" }}>
        <Input
          placeholder="Search modules, classes, functions..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          autoFocus
          size="large"
          style={{ marginBottom: 16 }}
        />

        <Space wrap>
          <Radio.Group
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
          >
            <Radio value="all">All</Radio>
            <Radio value="module">Modules</Radio>
            <Radio value="class">Classes</Radio>
            <Radio value="function">Functions</Radio>
            <Radio value="page">Pages</Radio>
          </Radio.Group>

          <Radio.Group
            value={searchMode}
            onChange={(e) => setSearchMode(e.target.value)}
          >
            <Radio value="description">Description</Radio>
            <Radio value="code">Code</Radio>
          </Radio.Group>
        </Space>
      </div>

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
            const snippetText =
              searchMode === "code"
                ? getSnippet(item.source || "", query, 80)
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
                    {item.module && (
                      <Tag color="blue">{item.module}</Tag>
                    )}
                  </Space>

                  <div style={{ fontWeight: "bold" }}>
                    {highlightText(item.name, query)}
                  </div>

                  <div style={{ color: "#888", fontSize: "0.85em" }}>
                    {item.fullPath}
                  </div>

                  <div style={{ color: "#666", whiteSpace: "pre-wrap" }}>
                    {highlightText(snippetText, query)}
                  </div>
                </Space>
              </Card>
            );
          })}

          {query && results.length === 0 && (
            <div style={{ textAlign: "center", color: "#999", padding: 20 }}>
              No results found for "{query}"
            </div>
          )}
        </Space>
      </div>
    </Modal>
  );
};

export default GlobalSearch;
