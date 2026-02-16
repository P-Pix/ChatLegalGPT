import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function prettySource(s) {
  const title = s?.source?.title || s?.source?.id || "Source";
  const url = s?.source?.url || "";
  const date = s?.source?.date || "";
  return { title, url, date };
}

export default function App() {
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Bonjour, je suis ChatLegalGPT. Posez votre question sur le droit français." }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function send() {
    const q = input.trim();
    if (!q) return;

    setMessages((m) => [...m, { role: "user", content: q }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data?.detail || "Erreur");

      setMessages((m) => [
        ...m,
        { role: "assistant", content: data.answer, sources: data.retrieved }
      ]);
    } catch (e) {
      setMessages((m) => [...m, { role: "assistant", content: `Erreur API: ${String(e.message || e)}` }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 980, margin: "0 auto", padding: 16, fontFamily: "system-ui" }}>
      <header style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between" }}>
        <h1 style={{ margin: 0 }}>ChatLegalGPT</h1>
        <span style={{ fontSize: 12, opacity: 0.75 }}>RAG + citations (prototype)</span>
      </header>

      <div style={{ border: "1px solid #ddd", borderRadius: 12, padding: 12, minHeight: 420, marginTop: 12 }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ marginBottom: 16 }}>
            <div style={{ fontWeight: 700 }}>{msg.role === "user" ? "Vous" : "ChatLegalGPT"}</div>
            <div style={{ whiteSpace: "pre-wrap" }}>{msg.content}</div>

            {msg.sources && (
              <details style={{ marginTop: 8 }}>
                <summary>Sources récupérées</summary>
                <ul style={{ marginTop: 8 }}>
                  {msg.sources.map((s) => {
                    const ps = prettySource(s);
                    return (
                      <li key={s.rank} style={{ marginBottom: 8 }}>
                        <div><b>[SOURCE {s.rank}]</b> score={Number(s.score).toFixed(3)}</div>
                        <div style={{ fontSize: 13, opacity: 0.85 }}>
                          {ps.title}{ps.date ? ` — ${ps.date}` : ""}{ps.url ? ` — ${ps.url}` : ""}
                        </div>
                      </li>
                    );
                  })}
                </ul>
              </details>
            )}
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => (e.key === "Enter" ? send() : null)}
          placeholder="Ex: Quels sont mes droits en cas de rupture de période d’essai ?"
          style={{ flex: 1, padding: 12, borderRadius: 10, border: "1px solid #ddd" }}
        />
        <button onClick={send} disabled={loading} style={{ padding: "12px 16px", borderRadius: 10 }}>
          {loading ? "…" : "Envoyer"}
        </button>
      </div>

      <p style={{ marginTop: 12, fontSize: 12, opacity: 0.8 }}>
        Information générale uniquement. Pour un cas concret, vérifiez les textes applicables et/ou consultez un professionnel.
      </p>
    </div>
  );
}
