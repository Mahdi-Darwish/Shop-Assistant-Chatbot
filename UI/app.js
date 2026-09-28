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
/* Two overlapping squares — the classic eight-point khatam star
   used across the page as Lamma's brand mark. */
const MarkIcon = ({ className }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="4.2" y="4.2" width="15.6" height="15.6" stroke="currentColor" strokeWidth="1.3"/>
    <rect x="4.2" y="4.2" width="15.6" height="15.6" stroke="currentColor" strokeWidth="1.3" transform="rotate(45 12 12)"/>
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

const CartIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M3 4h2l2.4 12.2a2 2 0 0 0 2 1.6h7.7a2 2 0 0 0 2-1.6L21 8H6" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round"/>
    <circle cx="10" cy="21" r="1.4" fill="currentColor"/>
    <circle cx="17" cy="21" r="1.4" fill="currentColor"/>
  </svg>
);

/* ---------------------------------------------------------
   Typing indicator — three dots animating up and down.
   Replaces the old "Thinking…" text bubble.
   --------------------------------------------------------- */
function TypingIndicator() {
  return (
    <div className="typing-indicator" aria-label="Assistant is typing">
      <span></span>
      <span></span>
      <span></span>
    </div>
  );
}

/* ---------------------------------------------------------
   Detects a "added X to your cart" style confirmation in an
   assistant reply so we can surface quick-action buttons
   (Checkout / Add another item) right inside the message.
   --------------------------------------------------------- */
function parseCartConfirmation(text) {
  if (!text) return null;
  const plain = text.replace(/\*\*/g, "");
  const match = plain.match(/added\s+(.+?)\s+to\s+(?:your|the)\s+cart/i);
  return match ? match[1].trim() : null;
}

/* ---------------------------------------------------------
   Lightweight formatter for assistant replies. The LLM often
   writes back **bold** labels and "- " bulleted lists — this
   turns that raw markdown into real emphasis and a cleanly
   spaced list instead of showing the asterisks/dashes as-is.
   --------------------------------------------------------- */
function renderInline(text, keyPrefix) {
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return parts.map((part, i) =>
    part.startsWith("**") && part.endsWith("**") ? (
      <strong key={`${keyPrefix}-b-${i}`}>{part.slice(2, -2)}</strong>
    ) : (
      <React.Fragment key={`${keyPrefix}-t-${i}`}>{part}</React.Fragment>
    )
  );
}

function MessageContent({ text }) {
  const blocks = text.trim().split(/\n\s*\n/);

  return blocks.map((block, bi) => {
    const lines = block.split("\n").map((l) => l.trim()).filter(Boolean);
    const isList = lines.length > 0 && lines.every((l) => /^[-*•]\s+/.test(l));

    if (isList) {
      return (
        <ul className="msg-list" key={`b-${bi}`}>
          {lines.map((line, li) => (
            <li key={`b-${bi}-${li}`}>
              {renderInline(line.replace(/^[-*•]\s+/, ""), `b-${bi}-${li}`)}
            </li>
          ))}
        </ul>
      );
    }

    return (
      <p className="msg-paragraph" key={`b-${bi}`}>
        {lines.map((line, li) => (
          <React.Fragment key={`b-${bi}-${li}`}>
            {li > 0 && <br />}
            {renderInline(line, `b-${bi}-${li}`)}
          </React.Fragment>
        ))}
      </p>
    );
  });
}

/* ---------------------------------------------------------
   Hero photography — real cup + real pastry, gently animated
   --------------------------------------------------------- */
function HeroArt() {
  return (
    <div className="hero-art">
      <div className="hero-photo hero-photo-main">
        <img
          src="https://images.unsplash.com/photo-1506778020041-0ea35027d019?auto=format&fit=crop&w=3840&q=90"
          srcSet="
            https://images.unsplash.com/photo-1506778020041-0ea35027d019?auto=format&fit=crop&w=1000&q=85 1000w,
            https://images.unsplash.com/photo-1506778020041-0ea35027d019?auto=format&fit=crop&w=2000&q=88 2000w,
            https://images.unsplash.com/photo-1506778020041-0ea35027d019?auto=format&fit=crop&w=3840&q=90 3840w
          "
          sizes="(max-width: 560px) 260px, (max-width: 880px) 300px, 420px"
          alt="Traditional Arabic coffee poured into a small patterned cup"
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
          src="https://images.unsplash.com/photo-1651507265947-06cbb2283901?auto=format&fit=crop&w=2400&q=90"
          srcSet="
            https://images.unsplash.com/photo-1651507265947-06cbb2283901?auto=format&fit=crop&w=600&q=85 600w,
            https://images.unsplash.com/photo-1651507265947-06cbb2283901?auto=format&fit=crop&w=1200&q=88 1200w,
            https://images.unsplash.com/photo-1651507265947-06cbb2283901?auto=format&fit=crop&w=2400&q=90 2400w
          "
          sizes="(max-width: 560px) 110px, (max-width: 880px) 130px, 180px"
          alt="A stack of golden baklava"
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
          <MarkIcon />
          <span className="wordmark-text">
            <span className="wordmark-ar" lang="ar" dir="rtl">لمّة</span>
            <span className="wordmark-en">Lamma</span>
          </span>
        </a>
        <div className="nav-links">
          <a href="#menu">Menu</a>
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
    <div className="hero-section lattice">
      <div className="site hero" id="top">
        <div className="hero-copy">
          <span className="hero-mark" lang="ar" dir="rtl">لمّة</span>
          <h1>Coffee is better shared.</h1>
          <p>
            لمّة (lamma) means gathering. Slow-poured qahwa, warm cardamom
            pastries, and a seat that's yours for as long as you want it.
          </p>
          <div className="hero-actions">
            <button className="btn btn-solid" onClick={onOpenChat}>Ask what's brewing</button>
            <button className="hero-login-hint" onClick={onSignup}>Create an account to order</button>
          </div>
        </div>
        <HeroArt />
      </div>
    </div>
  );
}

/* ---------------------------------------------------------
   Menu preview — live from GET /products
   --------------------------------------------------------- */
/* ---------------------------------------------------------
   Menu item photos — picked automatically from the product's
   name/description, so a new item added in the admin panel gets
   a fitting photo immediately, with no image field in the DB.
   --------------------------------------------------------- */
const MENU_IMAGE_RULES = [
  { keywords: ["cheesecake", "cheese-cake", "cheese cake"], id: "1588411781312-5a863186a260" },
  { keywords: ["tiramisu"], id: "1707528903686-91cbbe2f2985" },
  { keywords: ["croissant"], id: "1702090888946-d330cd452f5e" },
  { keywords: ["crepe", "crêpe", "pancake", "waffle"], id: "1569077218751-3e3de7800c00" },
  { keywords: ["baklava", "kunafa", "knafeh", "künefe", "maamoul", "assabeh", "mabroumeh"], id: "1651507265947-06cbb2283901" },
  { keywords: ["ice cream", "icecream", "gelato", "sundae", "sorbet"], id: "1588195539297-f0b4efdb5472" },
  { keywords: ["sandwich", "panini", "club sandwich", "toastie", "toasted"], id: "1533920606431-81cd9c3bce0f" },
  { keywords: ["tea", "chai", "karak"], id: "1541696490-8744a5dc0228" },
  { keywords: ["juice", "lemonade", "smoothie", "milkshake", "shake", "soda", "mocktail"], id: "1618046364546-81e9d03d39a6" },
  { keywords: ["ice", "iced", "cold", "mocha", "frappe", "frappuccino"], id: "1517701604599-bb29b565090c" },
  { keywords: ["espresso", "americano", "coffee", "latte", "cappuccino", "macchiato", "qahwa", "arabica"], id: "1428550443830-190057dc8098" },
  { keywords: ["donut", "doughnut", "muffin", "danish", "scone", "cinnamon roll", "cookie", "pastry", "pastries"], id: "1710077717714-976db5604dd7" },
];
const MENU_IMAGE_FALLBACK_ID = "1506778020041-0ea35027d019";

function getMenuImageId(product) {
  const haystack = `${product.name || ""} ${product.description || ""}`.toLowerCase();
  for (const rule of MENU_IMAGE_RULES) {
    if (rule.keywords.some((k) => haystack.includes(k))) return rule.id;
  }
  return MENU_IMAGE_FALLBACK_ID;
}

function menuImageUrl(id, width) {
  return `https://images.unsplash.com/photo-${id}?auto=format&fit=crop&w=${width}&q=85`;
}

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
        <h2>On the counter today</h2>
        <p>Made fresh, served warm, and made for sharing. Welcome to لمّة.</p>
      </div>
      <div ref={gridRef} className={`menu-grid ${inView ? "in-view" : ""}`}>
        {error && <div className="menu-error">Couldn't load the menu right now — try asking the assistant instead.</div>}
        {!error && products === null && <div className="menu-empty">Menu's brewing — one moment.</div>}
        {!error && products && products.length === 0 && (
          <div className="menu-empty">Nothing on the counter yet — check back soon.</div>
        )}
        {!error && products && products.slice(0, 8).map((p) => {
          const imgId = getMenuImageId(p);
          return (
            <div className="menu-card" key={p.id}>
              <div className="menu-card-photo">
                <img
                  src={menuImageUrl(imgId, 800)}
                  srcSet={`${menuImageUrl(imgId, 400)} 400w, ${menuImageUrl(imgId, 800)} 800w`}
                  sizes="(max-width: 560px) 90vw, (max-width: 1024px) 45vw, 320px"
                  alt={p.name}
                  loading="lazy"
                  decoding="async"
                />
              </div>
              <div className="menu-card-body">
                <h3>{p.name}</h3>
                <p className="desc">{p.description}</p>
                <div className="menu-card-divider"><span></span></div>
                <div className="price">${p.price.toFixed(2)}</div>
              </div>
            </div>
          );
        })}
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
    <div className="story lattice" id="story">
      <div ref={innerRef} className={`site story-inner ${inView ? "in-view" : ""}`}>
        <div>
          <h2>Coffee was always an invitation.</h2>
          <p>
            Across the Gulf and the Levant, coffee is the first thing
            offered to a guest — poured from a dallah, into a small cup,
            again and again until you've had enough. That's the idea
            behind Lamma: pull up a seat, and someone will bring you a
            cup before you've finished asking.
          </p>
        </div>
        <div className="story-stat">
          <span className="num">6am – 11pm</span>
          <span className="label">Open every day, made for lingering.</span>
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
      <div className="footer-brand">
        <span className="footer-name-ar" lang="ar" dir="rtl">لمّة</span>
        <span className="footer-name-en">Lamma</span>
      </div>
      <span>14 Miller Street, open daily 6am–11pm</span>
      <span>Menu, orders, and your account are all in the chat, bottom right.</span>
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

  async function sendMessage(text) {
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

  function handleSend(e) {
    e.preventDefault();
    const text = input.trim();
    if (!text) return;
    sendMessage(text);
  }

  // Used by the in-message quick-action buttons (Checkout / Add another item)
  function quickSend(text) {
    sendMessage(text);
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
            <div className="who">
              <MarkIcon />
              <div className="who-text">
                <span className="who-name">Ask Lamma</span>
                <span className="who-status">
                  <span className="status-dot" aria-hidden="true"></span>
                  Responds within a second
                </span>
              </div>
            </div>
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
            {activeMessages.map((m, i) => {
              const cartItem = m.role === "assistant" ? parseCartConfirmation(m.content) : null;
              return (
                <div key={i} className={`msg-row ${m.role}`}>
                  <div className="msg-bubble" dir="auto">
                    {m.role === "assistant" ? <MessageContent text={m.content} /> : m.content}
                    {cartItem && (
                      <div className="msg-actions">
                        <button
                          type="button"
                          className="msg-action-btn primary"
                          onClick={() => quickSend("Checkout")}
                        >
                          <CartIcon />
                          Checkout
                        </button>
                        <button
                          type="button"
                          className="msg-action-btn"
                          onClick={() => quickSend("I'd like to add another item")}
                        >
                          Add another item
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
            {sending && (
              <div className="msg-row assistant">
                <div className="msg-bubble thinking"><TypingIndicator /></div>
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