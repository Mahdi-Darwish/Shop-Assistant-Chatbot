const { useState, useEffect, useRef } = React;

const API_BASE = "http://localhost:8000";

const CupIcon = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M4 8h13v6a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5V8Z" stroke="currentColor" strokeWidth="1.6" strokeLinejoin="round"/>
    <path d="M17 9.5h1.5a2.5 2.5 0 0 1 0 5H17" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M8 4c-.6.7-.6 1.3 0 2M11.5 4c-.6.7-.6 1.3 0 2" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"/>
  </svg>
);

const PlusIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 5v14M5 12h14" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
  </svg>
);

const BeanPattern = () => {
  const beans = [];
  for (let i = 0; i < 40; i++) {
    const x = (i * 97) % 800;
    const y = (i * 149) % 600;
    const r = 14 + (i % 3) * 4;
    beans.push(
      <ellipse key={i} cx={x} cy={y} rx={r} ry={r * 1.5} fill="#FBF3E7"
        transform={`rotate(${(x * 7) % 360} ${x} ${y})`} />
    );
  }
  return (
    <svg className="bean-pattern" viewBox="0 0 800 600" preserveAspectRatio="xMidYMid slice">
      {beans}
    </svg>
  );
};

function AuthScreen({ onAuthenticated }) {
  const [mode, setMode] = useState("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [phone, setPhone] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);

    const endpoint = mode === "login" ? "/login" : "/signup";
    const body =
      mode === "login"
        ? { username, password }
        : { username, password, confirm_password: confirmPassword, phone };

    try {
      const response = await fetch(`${API_BASE}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await response.json();

      if (!response.ok) {
        const message = Array.isArray(data.detail)
          ? data.detail.map((d) => d.msg).join(", ")
          : data.detail || "Something went wrong. Please try again.";
        throw new Error(message);
      }

      onAuthenticated(data.access_token);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-screen">
      <BeanPattern />
      <div className="auth-card">
        <CupIcon className="cup-mark" />
        <h1 className="brand">The Daily Grind</h1>
        <p className="tagline">Coffee, dessert, and a little help deciding.</p>

        {error && <div className="error-banner">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="field">
            <label htmlFor="username">Username</label>
            <input id="username" value={username} onChange={(e) => setUsername(e.target.value)} required />
          </div>

          <div className="field">
            <label htmlFor="password">Password</label>
            <input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>

          {mode === "signup" && (
            <>
              <div className="field">
                <label htmlFor="confirmPassword">Confirm password</label>
                <input id="confirmPassword" type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
              </div>
              <div className="field">
                <label htmlFor="phone">Phone number</label>
                <input id="phone" value={phone} onChange={(e) => setPhone(e.target.value)} required />
              </div>
            </>
          )}

          <button className="btn-primary" type="submit" disabled={loading}>
            {loading ? "Please wait…" : mode === "login" ? "Log in" : "Sign up"}
          </button>
        </form>

        <div className="switch-mode">
          {mode === "login" ? (
            <>New here? <button onClick={() => { setMode("signup"); setError(""); }}>Create an account</button></>
          ) : (
            <>Already have an account? <button onClick={() => { setMode("login"); setError(""); }}>Log in</button></>
          )}
        </div>
      </div>
    </div>
  );
}

function relativeTime(isoString) {
  const diff = Date.now() - new Date(isoString).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

function Sidebar({ conversations, activeId, onSelect, onNewChat }) {
  return (
    <div className="sidebar">
      <button className="new-chat-btn" onClick={onNewChat}>
        <PlusIcon />
        New chat
      </button>
      <div className="conversation-list">
        {conversations.map((c) => (
          <button
            key={c.id}
            className={`conversation-item ${c.id === activeId ? "active" : ""}`}
            onClick={() => onSelect(c.id)}
          >
            <div className="conversation-title">{c.title || "New conversation"}</div>
            <div className="conversation-time">{relativeTime(c.created_at)}</div>
          </button>
        ))}
        {conversations.length === 0 && (
          <p className="sidebar-empty">No past conversations yet.</p>
        )}
      </div>
    </div>
  );
}

function ChatScreen({ token, onLogout, basePath, isAdmin }) {
  const [conversations, setConversations] = useState([]);
  const [activeId, setActiveId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [loading, setLoading] = useState(true);
  const scrollRef = useRef(null);

  const authedFetch = (path, options = {}) =>
    fetch(`${API_BASE}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        ...(options.headers || {}),
      },
    });

  async function loadConversations(selectId) {
    const response = await authedFetch(`${basePath}/conversations`);
    if (response.status === 401) return onLogout();
    const data = await response.json();
    setConversations(data);

    if (selectId) {
      setActiveId(selectId);
    } else if (data.length > 0) {
      setActiveId(data[0].id); // most recent
    } else {
      await handleNewChat(data);
    }
  }

  async function loadMessages(conversationId) {
    const response = await authedFetch(`${basePath}/conversations/${conversationId}/messages`);
    if (response.status === 401) return onLogout();
    const data = await response.json();
    setMessages(response.ok ? data : []);
  }

  async function handleNewChat() {
    const response = await authedFetch(`${basePath}/conversations`, { method: "POST" });
    if (response.status === 401) return onLogout();
    const conversation = await response.json();
    setConversations((prev) => [conversation, ...prev]);
    setActiveId(conversation.id);
    setMessages([]);
  }

  useEffect(() => {
    (async () => {
      setLoading(true);
      await loadConversations();
      setLoading(false);
    })();
  }, []);

  useEffect(() => {
    if (activeId) loadMessages(activeId);
  }, [activeId]);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, sending]);

  async function handleSend(e) {
    e.preventDefault();
    const text = input.trim();
    if (!text || sending || !activeId) return;

    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setInput("");
    setSending(true);

    try {
      const response = await authedFetch(`${basePath}/chat`, {
        method: "POST",
        body: JSON.stringify({ message: text, conversation_id: activeId }),
      });

      if (response.status === 401) return onLogout();

      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Something went wrong.");

      setMessages((prev) => [...prev, { role: "assistant", content: data.reply }]);

      // First message in a fresh thread gets it a real title — refresh
      // the sidebar list so it shows up instead of "New conversation".
      loadConversations(activeId);
    } catch (err) {
      setMessages((prev) => [...prev, { role: "assistant", content: `Sorry — ${err.message}` }]);
    } finally {
      setSending(false);
    }
  }

  return (
    <div className="app-layout">
      <Sidebar
        conversations={conversations}
        activeId={activeId}
        onSelect={setActiveId}
        onNewChat={handleNewChat}
      />

      <div className="chat-screen">
        <div className="chat-header">
          <div className="brand-mark">
            <CupIcon />
            <h1 className="brand">The Daily Grind</h1>
            {isAdmin && <span className="admin-badge">Admin</span>}
          </div>
          <button className="logout-btn" onClick={onLogout}>Log out</button>
        </div>

        <div className="messages">
          {loading && (
            <div className="empty-state">
              <CupIcon className="cup-mark" />
              <span className="brand">Loading…</span>
            </div>
          )}

          {!loading && messages.length === 0 && (
            <div className="empty-state">
              <CupIcon className="cup-mark" />
              <span className="brand">
                {isAdmin ? "What would you like to manage?" : "What can I get started for you?"}
              </span>
              {isAdmin
                ? "Add or update products, manage user accounts — just ask."
                : "Ask about the menu, add something to your cart, or check an order."}
            </div>
          )}

          {messages.map((m, i) => (
            <div key={i} className={`message-row ${m.role}`}>
              {m.role === "assistant" && <div className="avatar"><CupIcon /></div>}
              <div className="message-bubble">{m.content}</div>
            </div>
          ))}

          {sending && (
            <div className="message-row assistant">
              <div className="avatar"><CupIcon /></div>
              <div className="message-bubble loading">Thinking…</div>
            </div>
          )}

          <div ref={scrollRef} />
        </div>

        <form className="input-bar" onSubmit={handleSend}>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={
              isAdmin
                ? "Add a product, deactivate a user, update a price…"
                : "Ask about the menu, or say what you'd like to order…"
            }
            disabled={sending}
          />
          <button type="submit" disabled={sending || !input.trim()}>Send</button>
        </form>
      </div>
    </div>
  );
}

function App() {
  const [token, setToken] = useState(() => localStorage.getItem("shop_token"));
  const [role, setRole] = useState(null);
  const [checkingRole, setCheckingRole] = useState(true);

  useEffect(() => {
    if (!token) {
      setCheckingRole(false);
      return;
    }
    (async () => {
      try {
        const response = await fetch(`${API_BASE}/me`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!response.ok) {
          handleLogout();
          return;
        }
        const data = await response.json();
        setRole(data.role);
      } finally {
        setCheckingRole(false);
      }
    })();
  }, [token]);

  function handleAuthenticated(newToken) {
    localStorage.setItem("shop_token", newToken);
    setCheckingRole(true);
    setToken(newToken);
  }

  function handleLogout() {
    localStorage.removeItem("shop_token");
    setToken(null);
    setRole(null);
  }

  if (!token) {
    return <AuthScreen onAuthenticated={handleAuthenticated} />;
  }

  if (checkingRole) {
    return (
      <div className="auth-screen">
        <BeanPattern />
        <div className="empty-state" style={{ color: "#F3EDE2" }}>
          <CupIcon className="cup-mark" />
        </div>
      </div>
    );
  }

  const isAdmin = role === "admin";
  return (
    <ChatScreen
      token={token}
      onLogout={handleLogout}
      basePath={isAdmin ? "/admin" : ""}
      isAdmin={isAdmin}
    />
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);