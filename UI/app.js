const { useState, useEffect, useRef } = React;

const API_BASE =
  window.location.hostname === "localhost" ||
  window.location.hostname === "127.0.0.1" ||
  window.location.protocol === "file:"
    ? "http://localhost:8000"
    : "https://shop-assistant-chatbot.onrender.com";

/* ---------------------------------------------------------
   Icons
   --------------------------------------------------------- */
const CupIcon = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M4 8h13v6a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5V8Z" stroke="currentColor" strokeWidth="1.6" strokeLinejoin="round"/>
    <path d="M17 9.5h1.5a2.5 2.5 0 0 1 0 5H17" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const CloseIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M6 6l12 12M18 6L6 18" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
  </svg>
);

const ChatBubbleIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M4 6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H9l-4 4v-4H6a2 2 0 0 1-2-2V6Z" stroke="currentColor" strokeWidth="1.7" strokeLinejoin="round"/>
  </svg>
);

/* ---------------------------------------------------------
   Hero photography — real cup + real pastry, gently animated
   --------------------------------------------------------- */
function HeroArt() {
  return (
    <div className="hero-art">
      <div className="hero-photo hero-photo-main">
        <img
          src="https://images.unsplash.com/photo-1512568400610-62da28bc8a13?auto=format&fit=crop&w=1000&q=80"
          alt="Cappuccino with latte art resting in a bed of fresh roasted coffee beans"
          loading="eager"
          decoding="async"
        />
        <div className="hero-steam" aria-hidden="true">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
      <div className="hero-photo hero-photo-card">
        <img
          src="https://images.unsplash.com/photo-1678303054606-9247ec5ca401?auto=format&fit=crop&w=600&q=80"
          alt="A beautifully plated dessert"
          loading="lazy"
          decoding="async"
        />
      </div>
    </div>
  );
}

/* ---------------------------------------------------------
   Nav
   --------------------------------------------------------- */
function Nav({ isAuthed, isAdmin, onLogin, onSignup, onLogout }) {
  return (
    <div className="nav">
      <div className="nav-inner">
        <a className="wordmark" href="#top">
          <CupIcon />
          The Daily Grind
        </a>
        <div className="nav-links">
          <a href="#story">Our story</a>
        </div>
        <div className="nav-auth">
          {isAuthed ? (
            <div className="account-pill">
              {isAdmin && <span className="admin-tag">Admin</span>}
              <button className="btn btn-ghost" onClick={onLogout}>Log out</button>
            </div>
          ) : (
            <>
              <button className="btn btn-ghost" onClick={onLogin}>Log in</button>
              <button className="btn btn-solid" onClick={onSignup}>Sign up</button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

/* ---------------------------------------------------------
   Hero
   --------------------------------------------------------- */
function Hero({ onOpenChat, onSignup }) {
  return (
    <div className="site hero" id="top">
      <div className="hero-copy">
        <h1>Coffee that's actually worth the walk.</h1>
        <p>
          Small-batch roasts, a pastry case that empties out by noon, and a
          menu assistant sitting in the corner of this page if you'd rather
          just ask what's good today.
        </p>
        <div className="hero-actions">
          <button className="btn btn-solid" onClick={onOpenChat}>Ask about the menu</button>
          <button className="hero-login-hint" onClick={onSignup}>Create an account to order</button>
        </div>
      </div>
      <HeroArt />
    </div>
  );
}

/* ---------------------------------------------------------
   Menu preview — live from GET /products
   --------------------------------------------------------- */
function MenuPreview() {
  const [products, setProducts] = useState(null);
  const [error, setError] = useState(false);
  const [inView, setInView] = useState(false);
  const gridRef = useRef(null);

  useEffect(() => {
    fetch(`${API_BASE}/products`)
      .then((r) => {
        if (!r.ok) throw new Error();
        return r.json();
      })
      .then(setProducts)
      .catch(() => setError(true));
  }, []);

  useEffect(() => {
    const el = gridRef.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setInView(true);
          observer.disconnect();
        }
      },
      { threshold: 0.15 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, [products, error]);

  return (
    <div className="site menu-section" id="menu">
      <div className="section-head">
        <h2>What's fresh today</h2>
        <p>Pulled straight from the counter — ask the assistant if you want the full list or something specific.</p>
      </div>
      <div ref={gridRef} className={`menu-grid ${inView ? "in-view" : ""}`}>
        {error && <div className="menu-error">Couldn't load the menu right now — try asking the assistant instead.</div>}
        {!error && products === null && <div className="menu-empty">Menu's brewing — one moment.</div>}
        {!error && products && products.length === 0 && (
          <div className="menu-empty">Nothing on the counter yet — check back soon.</div>
        )}
        {!error && products && products.slice(0, 8).map((p) => (
          <div className="menu-card" key={p.id}>
            <h3>{p.name}</h3>
            <p className="desc">{p.description}</p>
            <div className="price">${p.price.toFixed(2)}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ---------------------------------------------------------
   Story
   --------------------------------------------------------- */
function Story() {
  const [inView, setInView] = useState(false);
  const innerRef = useRef(null);

  useEffect(() => {
    const el = innerRef.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setInView(true);
          observer.disconnect();
        }
      },
      { threshold: 0.2 }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return (
    <div className="story" id="story">
      <div ref={innerRef} className={`site story-inner ${inView ? "in-view" : ""}`}>
        <div>
          <h2>Roasted here, not shipped in.</h2>
          <p>
            We roast in small batches twice a week, pull every shot to
            order, and bake the pastry case fresh each morning — nothing
            sits under glass longer than a day. If you're not sure what
            to get, the assistant in the corner knows the counter better
            than most of our regulars.
          </p>
        </div>
        <div className="story-stat">
          <span className="num">6am – 7pm</span>
          <span className="label">Open every day of the week</span>
        </div>
      </div>
    </div>
  );
}

/* ---------------------------------------------------------
   Footer
   --------------------------------------------------------- */
function Footer() {
  return (
    <div className="site footer">
      <span>The Daily Grind — 14 Miller Street</span>
      <span>Menu, orders, and account all live in the chat, bottom right.</span>
    </div>
  );
}

/* ---------------------------------------------------------
   Auth modal
   --------------------------------------------------------- */
function AuthModal({ mode, onClose, onAuthenticated, onSwitchMode }) {
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
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}><CloseIcon /></button>

        <div className="modal-tabs">
          <button
            className={`modal-tab ${mode === "login" ? "active" : ""}`}
            onClick={() => onSwitchMode("login")}
          >
            Log in
          </button>
          <button
            className={`modal-tab ${mode === "signup" ? "active" : ""}`}
            onClick={() => onSwitchMode("signup")}
          >
            Sign up
          </button>
        </div>

        <h2>{mode === "login" ? "Welcome back" : "Create your account"}</h2>
        <p className="modal-sub">
          {mode === "login"
            ? "Log in to order, track it, and pick up where you left off."
            : "Takes a few seconds — you'll be ordering right after."}
        </p>

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

          <button className="btn btn-solid" type="submit" disabled={loading}>
            {loading ? "Please wait…" : mode === "login" ? "Log in" : "Sign up"}
          </button>
        </form>
      </div>
    </div>
  );
}

/* ---------------------------------------------------------
   Chat widget — guest (read-only) or authenticated (full)
   --------------------------------------------------------- */
function ChatWidget({ token, isAdmin, onRequireAuth, openSignal }) {
  const [open, setOpen] = useState(false);
  const [guestMessages, setGuestMessages] = useState([]);
  const [conversations, setConversations] = useState([]);
  const [activeId, setActiveId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (openSignal > 0) setOpen(true);
  }, [openSignal]);

  const basePath = isAdmin ? "/admin" : "";

  const authedFetch = (path, options = {}) =>
    fetch(`${API_BASE}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        ...(options.headers || {}),
      },
    });

  async function loadConversations() {
    const response = await authedFetch(`${basePath}/conversations`);
    if (!response.ok) return;
    const data = await response.json();
    setConversations(data);
    if (data.length > 0) {
      setActiveId(data[0].id);
    } else {
      await handleNewChat();
    }
  }

  async function loadMessages(conversationId) {
    const response = await authedFetch(`${basePath}/conversations/${conversationId}/messages`);
    const data = await response.json();
    setMessages(response.ok ? data : []);
  }

  async function handleNewChat() {
    const response = await authedFetch(`${basePath}/conversations`, { method: "POST" });
    const conversation = await response.json();
    setConversations((prev) => [conversation, ...prev]);
    setActiveId(conversation.id);
    setMessages([]);
  }

  useEffect(() => {
    if (open && token) loadConversations();
    if (open && !token) setGuestMessages((m) => m);
  }, [open, token]);

  useEffect(() => {
    if (token && activeId) loadMessages(activeId);
  }, [activeId, token]);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, guestMessages, sending]);

  async function handleSend(e) {
    e.preventDefault();
    const text = input.trim();
    if (!text || sending) return;
    setInput("");
    setSending(true);

    if (!token) {
      const history = guestMessages;
      setGuestMessages((prev) => [...prev, { role: "user", content: text }]);
      try {
        const response = await fetch(`${API_BASE}/chat/guest`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: text, history }),
        });
        const data = await response.json();
        setGuestMessages((prev) => [...prev, { role: "assistant", content: data.reply || "Sorry, something went wrong." }]);
      } catch {
        setGuestMessages((prev) => [...prev, { role: "assistant", content: "Sorry — I couldn't reach the menu right now." }]);
      } finally {
        setSending(false);
      }
      return;
    }

    if (!activeId) { setSending(false); return; }
    setMessages((prev) => [...prev, { role: "user", content: text }]);
    try {
      const response = await authedFetch(`${basePath}/chat`, {
        method: "POST",
        body: JSON.stringify({ message: text, conversation_id: activeId }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Something went wrong.");
      setMessages((prev) => [...prev, { role: "assistant", content: data.reply }]);
      loadConversations();
    } catch (err) {
      setMessages((prev) => [...prev, { role: "assistant", content: `Sorry — ${err.message}` }]);
    } finally {
      setSending(false);
    }
  }

  const activeMessages = token ? messages : guestMessages;

  return (
    <>
      {!open && (
        <button className="chat-launcher" onClick={() => setOpen(true)} aria-label="Open chat">
          <ChatBubbleIcon />
        </button>
      )}

      {open && (
        <div className="chat-panel">
          <div className="chat-panel-header">
            <div className="who"><CupIcon />Ask The Daily Grind</div>
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              {token && conversations.length > 0 && (
                <select
                  className="chat-history-select"
                  value={activeId || ""}
                  onChange={(e) => setActiveId(Number(e.target.value))}
                >
                  {conversations.map((c) => (
                    <option key={c.id} value={c.id}>{c.title || "New chat"}</option>
                  ))}
                </select>
              )}
              {token && (
                <button className="chat-panel-close" onClick={handleNewChat} aria-label="New chat" title="New chat">+</button>
              )}
              <button className="chat-panel-close" onClick={() => setOpen(false)} aria-label="Close chat"><CloseIcon /></button>
            </div>
          </div>

          {!token && (
            <div className="guest-banner">
              <span>Browsing as guest — log in to order</span>
              <button onClick={onRequireAuth}>Log in</button>
            </div>
          )}

          <div className="chat-messages">
            {activeMessages.length === 0 && (
              <div className="chat-empty">
                {token ? "Ask about your order, or what's good today." : "Ask what's on the menu, what's fresh, or for a recommendation."}
              </div>
            )}
            {activeMessages.map((m, i) => (
              <div key={i} className={`msg-row ${m.role}`}>
                <div className="msg-bubble" dir="auto">{m.content}</div>
              </div>
            ))}
            {sending && (
              <div className="msg-row assistant">
                <div className="msg-bubble thinking">Thinking…</div>
              </div>
            )}
            <div ref={scrollRef} />
          </div>

          <form className="chat-input-bar" onSubmit={handleSend}>
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              dir="auto"
              placeholder={token ? "Ask about your order…" : "Ask about the menu…"}
              disabled={sending}
            />
            <button type="submit" disabled={sending || !input.trim()}>Send</button>
          </form>
        </div>
      )}
    </>
  );
}

/* ---------------------------------------------------------
   App
   --------------------------------------------------------- */
function App() {
  const [token, setToken] = useState(() => localStorage.getItem("shop_token"));
  const [role, setRole] = useState(null);
  const [authModal, setAuthModal] = useState(null); // null | "login" | "signup"
  const [chatOpenSignal, setChatOpenSignal] = useState(0);

  useEffect(() => {
    if (!token) { setRole(null); return; }
    fetch(`${API_BASE}/me`, { headers: { Authorization: `Bearer ${token}` } })
      .then((r) => (r.ok ? r.json() : Promise.reject()))
      .then((data) => setRole(data.role))
      .catch(() => handleLogout());
  }, [token]);

  function handleAuthenticated(newToken) {
    localStorage.setItem("shop_token", newToken);
    setToken(newToken);
    setAuthModal(null);
    setChatOpenSignal((n) => n + 1);
  }

  function handleLogout() {
    localStorage.removeItem("shop_token");
    setToken(null);
    setRole(null);
  }

  return (
    <>
      <Nav
        isAuthed={!!token}
        isAdmin={role === "admin"}
        onLogin={() => setAuthModal("login")}
        onSignup={() => setAuthModal("signup")}
        onLogout={handleLogout}
      />
      <Hero onOpenChat={() => setChatOpenSignal((n) => n + 1)} onSignup={() => setAuthModal("signup")} />
      <MenuPreview />
      <Story />
      <Footer />

      <ChatWidget
        token={token}
        isAdmin={role === "admin"}
        onRequireAuth={() => setAuthModal("login")}
        openSignal={chatOpenSignal}
      />

      {authModal && (
        <AuthModal
          mode={authModal}
          onClose={() => setAuthModal(null)}
          onSwitchMode={setAuthModal}
          onAuthenticated={handleAuthenticated}
        />
      )}
    </>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);