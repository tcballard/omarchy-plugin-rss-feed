// Data-only Perch v1 card; provider state and URL handling remain in RSS Feed.
function clean(value, limit) {
    return String(value || "").replace(/[\u0000-\u001f]/g, " ").slice(0, limit);
}
function articles(news) {
    return (news.itemsForSource("all") || []).slice(0, 8);
}
function revision(news) {
    // Stable snapshot identity including visible content, read state and URLs.
    var identity = articles(news).map(function(item) { return [item.id, item.url, clean(item.title, 180), clean(item.sourceName, 240)]; });
    return "r" + Qt.md5(JSON.stringify([identity, news.readIds, news.fetchedAt, news.refreshing, news.lastError, news.configurationError, news.stale, news.partial]));
}
function card(news) {
    var items = articles(news);
    var rev = revision(news);
    return {
        version: 1, revision: rev, title: "RSS Feed",
        status: news.refreshing ? "loading" : news.lastError || news.configurationError ? "error" : news.stale ? "offline" : items.length ? "ready" : "empty",
        summary: clean(news.configurationError || news.lastError || (news.refreshing ? "Refreshing feeds…" : news.unreadCount + " unread" + (news.stale ? " · cached headlines" : news.partial ? " · some feeds unavailable" : "")), 240),
        actions: news.refreshing ? [] : [{id: "refresh", label: "Refresh feeds"}],
        rows: items.map(function(item, i) {
            return {id: "article-" + i, title: clean(item.title, 180), detail: clean(item.sourceName || item.source || "", 240),
                    action: /^https?:\/\//.test(String(item.url || "")) ? {id: "open:" + i, label: "Read article"} : null};
        })
    };
}
function resolve(news, raw) {
    if (typeof raw !== "string" || raw.length > 1024) return null;
    try {
        var p = JSON.parse(raw);
        if (!p || p.version !== 1 || p.revision !== revision(news)) return null;
        if (p.action === "refresh" && !news.refreshing) return {kind: "refresh"};
        if (typeof p.action !== "string" || !/^open:[0-7]$/.test(p.action)) return null;
        var item = articles(news)[Number(p.action.slice(5))];
        if (!item || !/^https?:\/\//.test(String(item.url || ""))) return null;
        return {kind: "open", article: item};
    } catch (_) { return null; }
}
