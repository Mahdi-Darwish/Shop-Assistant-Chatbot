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

const AttachIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M20 11.5l-7.6 7.6a5 5 0 0 1-7.1-7.1l8-8a3.4 3.4 0 0 1 4.8 4.8l-8 8a1.8 1.8 0 0 1-2.5-2.5l7.3-7.3" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round"/>
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
      <div className="par" style={{ "--k": 1 }}>
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
      </div>
      <div className="par par-card" style={{ "--k": 2.2 }}>
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
    </div>
  );
}

/* ---------------------------------------------------------
   Nav
   --------------------------------------------------------- */
function Nav({ isAuthed, isAdmin, onLogin, onSignup, onLogout, onDashboard }) {
  const [scrolled, setScrolled] = useState(false);
  useEffect(() => {
    const on = () => setScrolled(window.scrollY > 24);
    on();
    window.addEventListener("scroll", on, { passive: true });
    return () => window.removeEventListener("scroll", on);
  }, []);
  return (
    <div className={`nav${scrolled ? " scrolled" : ""}`}>
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
              {isAdmin && onDashboard && (
                <button className="btn btn-solid" onClick={onDashboard}>Dashboard</button>
              )}
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
   Opening animation — the logo comes forward out of the dark,
   glowing, then zooms past the camera and the page opens.
   Plays once per browser tab; tap/click skips it; skipped entirely
   for people who asked their device for reduced motion.
   --------------------------------------------------------- */
const INTRO_KEY = "lamma_intro_seen";

function prefersReducedMotion() {
  return !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
}

function shouldPlayIntro() {
  if (prefersReducedMotion()) return false;
  try {
    return !sessionStorage.getItem(INTRO_KEY);
  } catch {
    return true;
  }
}

function Intro() {
  const [phase, setPhase] = useState(() => (shouldPlayIntro() ? "play" : "done"));

  function finish() {
    try { sessionStorage.setItem(INTRO_KEY, "1"); } catch { /* private mode: it just plays again */ }
    setPhase("done");
  }

  // timeline: logo comes forward (0–1.5s) → zooms through + overlay fades (1.9–2.6s)
  useEffect(() => {
    if (!shouldPlayIntro()) return undefined;
    const leave = setTimeout(() => setPhase((p) => (p === "play" ? "leave" : p)), 1900);
    const done = setTimeout(finish, 2650);
    return () => { clearTimeout(leave); clearTimeout(done); };
  }, []);

  // page state: lock scrolling while it plays; the hero drinks start flying in as the overlay fades
  useEffect(() => {
    const body = document.body;
    const html = document.documentElement;
    if (phase === "done") {
      body.classList.remove("intro-lock");
      html.classList.remove("intro-pending");
    } else {
      body.classList.add("intro-lock");
    }
    if (phase !== "play") html.classList.add("intro-done");
  }, [phase]);

  // if the page switches away mid-intro (e.g. an admin account opening the dashboard), never leave it locked
  useEffect(() => () => {
    document.body.classList.remove("intro-lock");
    document.documentElement.classList.remove("intro-pending");
  }, []);

  if (phase === "done") return null;
  return (
    <div className={`intro intro-${phase}`} aria-hidden="true" onClick={finish}>
      <div className="intro-glow"></div>
      <div className="intro-logo">
        <MarkIcon className="intro-mark" />
        <span className="intro-ar" lang="ar" dir="rtl">لمّة</span>
        <span className="intro-en">Lamma</span>
      </div>
    </div>
  );
}

/* ---------------------------------------------------------
   Scroll reveal — fades/rises into view once, when first seen
   --------------------------------------------------------- */
function Reveal({ className = "", delay = 0, children }) {
  const ref = useRef(null);
  const [shown, setShown] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el) return undefined;
    if (prefersReducedMotion() || !("IntersectionObserver" in window)) { setShown(true); return undefined; }
    const io = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) { setShown(true); io.disconnect(); }
    }, { threshold: 0.15 });
    io.observe(el);
    return () => io.disconnect();
  }, []);
  return (
    <div ref={ref} className={`reveal${shown ? " in" : ""} ${className}`} style={{ transitionDelay: `${delay}ms` }}>
      {children}
    </div>
  );
}

const BagIcon = () => (
  <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
    <path d="M5.5 8.5h13l-1 11h-11l-1-11z" stroke="currentColor" strokeWidth="1.6" strokeLinejoin="round" />
    <path d="M9 8.5V7a3 3 0 0 1 6 0v1.5" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
  </svg>
);

/* ---------------------------------------------------------
   Gold tongs pick the item up from the cart and drop it in the bag
   in the chat header (WAAPI, ~1.5s). Pure decoration: the cart
   itself is already updated by the server.
   --------------------------------------------------------- */
const TONG_ARM = "M40 6 C37 6 35.5 9 36.5 13 C37 32 29 52 21.5 76 C20.5 80 22 84 26 85 C30 86 32.5 83 33.6 79.5 C40 58 44.5 34 44 13 C44 9 43 6 40 6 Z";
const TONGS_SVG = `<svg viewBox="0 0 80 110" aria-hidden="true"><defs><linearGradient id="tgd" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8a6a2f"/><stop offset=".45" stop-color="#f1d896"/><stop offset=".7" stop-color="#c9a45c"/><stop offset="1" stop-color="#7d5f28"/></linearGradient><filter id="tgs" x="-30%" y="-10%" width="160%" height="130%"><feDropShadow dx="0" dy="3" stdDeviation="2.2" flood-color="#1d140d" flood-opacity=".35"/></filter></defs><g filter="url(#tgs)"><g class="ta-l" style="transform-origin:40px 14px"><path fill="url(#tgd)" d="${TONG_ARM}"/></g><g class="ta-r" style="transform-origin:40px 14px"><path fill="url(#tgd)" transform="translate(80 0) scale(-1 1)" d="${TONG_ARM}"/></g><path d="M33 10 C33 2 47 2 47 10" fill="none" stroke="url(#tgd)" stroke-width="3.2" stroke-linecap="round"/><circle cx="40" cy="14" r="3.6" fill="#f6e3b0" stroke="#8a6a2f" stroke-width="1.2"/></g></svg>`;

function bumpBag(bag) {
  if (bag && bag.animate) {
    bag.animate(
      [{ transform: "scale(1)" }, { transform: "scale(1.24)" }, { transform: "scale(.94)" }, { transform: "scale(1)" }],
      { duration: 480, easing: "ease-out" }
    );
  }
}

function flyTongs(imgEl, bagEl, onArrive) {
  const a = imgEl.getBoundingClientRect();
  const b = bagEl.getBoundingClientRect();
  const s = 84 / 80;                                   // graphic is 84px wide for an 80-unit viewBox
  const cx = a.left + a.width / 2, cy = a.top + a.height / 2;
  const dx = b.left + b.width / 2 - cx, dy = b.top + b.height / 2 - 2 - cy;

  const wrap = document.createElement("div");
  wrap.className = "tong-fly";
  wrap.style.left = `${cx - 40 * s}px`;
  wrap.style.top = `${cy - 76 * s}px`;
  const item = document.createElement("img");
  item.className = "tong-item";
  item.alt = "";
  item.src = imgEl.currentSrc || imgEl.src;
  wrap.appendChild(item);
  wrap.insertAdjacentHTML("beforeend", TONGS_SVG);
  document.body.appendChild(wrap);
  const prevOpacity = imgEl.style.opacity;
  imgEl.style.transition = "opacity .3s";
  imgEl.style.opacity = "0.12";                        // "picked up" from the cart row

  const T = 1500, ease = "cubic-bezier(.4,0,.2,1)";
  if (wrap.animate) {
    const at = (o, tf, extra = {}) => ({ offset: o, transform: tf, ...extra });
    wrap.animate([
      at(0, "translate(0,0) scale(.85)", { opacity: 0 }),
      at(0.13, "translate(0,0) scale(1)", { opacity: 1, easing: ease }),
      at(0.45, `translate(${dx * 0.55}px,${dy * 0.35 - 10}px) rotate(-10deg) scale(1.06)`, { opacity: 1, easing: ease }),
      at(0.73, `translate(${dx}px,${dy}px) rotate(5deg) scale(.82)`, { opacity: 1 }),
      at(0.86, `translate(${dx}px,${dy}px) rotate(5deg) scale(.82)`, { opacity: 1, easing: ease }),
      at(1, `translate(${dx}px,${dy - 24}px) rotate(5deg) scale(.7)`, { opacity: 0 }),
    ], { duration: T, fill: "forwards" });
    const arm = (sg) => [
      at(0, `rotate(${sg * 22}deg)`), at(0.13, `rotate(${sg * 8.5}deg)`, { easing: ease }),
      at(0.73, `rotate(${sg * 8.5}deg)`), at(0.83, `rotate(${sg * 22}deg)`, { easing: ease }), at(1, `rotate(${sg * 22}deg)`),
    ];
    wrap.querySelector(".ta-l").animate(arm(1), { duration: T, fill: "forwards" });   // open → grip → release
    wrap.querySelector(".ta-r").animate(arm(-1), { duration: T, fill: "forwards" });
    item.animate([
      { offset: 0, opacity: 1, transform: "none" }, { offset: 0.73, opacity: 1, transform: "none" },
      { offset: 0.86, opacity: 0, transform: "translateY(16px) scale(.35)", easing: ease },
      { offset: 1, opacity: 0, transform: "translateY(16px) scale(.35)" },
    ], { duration: T, fill: "forwards" });
  }
  setTimeout(() => { if (onArrive) onArrive(); }, T * 0.78);                           // it lands in the bag
  setTimeout(() => { imgEl.style.opacity = prevOpacity || ""; }, T * 0.8);
  setTimeout(() => wrap.remove(), T + 80);
}

/* ---------------------------------------------------------
   Hero
   --------------------------------------------------------- */
const HERO_WORDS = ["Coffee", "is", "better", "shared."];

function Hero({ onOpenChat, onSignup }) {
  const sectionRef = useRef(null);

  /* gentle mouse + scroll parallax on the photos (set as CSS variables on the hero) */
  useEffect(() => {
    const hero = sectionRef.current;
    if (!hero || prefersReducedMotion()) return undefined;
    let raf = 0;
    let mx = 0, my = 0, sp = 0;
    function apply() {
      raf = 0;
      hero.style.setProperty("--mx", mx.toFixed(3));
      hero.style.setProperty("--my", my.toFixed(3));
      hero.style.setProperty("--sp", sp.toFixed(3));
    }
    const schedule = () => { if (!raf) raf = requestAnimationFrame(apply); };
    function onScroll() {
      const r = hero.getBoundingClientRect();
      sp = Math.min(1, Math.max(0, -r.top / Math.max(r.height, 1)));
      schedule();
    }
    function onMove(e) {
      const r = hero.getBoundingClientRect();
      if (r.bottom < 0 || r.height === 0) return;
      mx = Math.max(-1, Math.min(1, ((e.clientX - r.left) / r.width) * 2 - 1));
      my = Math.max(-1, Math.min(1, ((e.clientY - r.top) / r.height) * 2 - 1));
      schedule();
    }
    const hasMouse = !!(window.matchMedia && window.matchMedia("(hover: hover) and (pointer: fine)").matches);
    if (hasMouse) window.addEventListener("mousemove", onMove, { passive: true });
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
    return () => {
      window.removeEventListener("mousemove", onMove);
      window.removeEventListener("scroll", onScroll);
      if (raf) cancelAnimationFrame(raf);
    };
  }, []);

  return (
    <div className="hero-section lattice" ref={sectionRef}>
      <div className="site hero" id="top">
        <div className="hero-copy">
          <span className="hero-mark" lang="ar" dir="rtl">لمّة</span>
          <h1 aria-label="Coffee is better shared.">
            {HERO_WORDS.map((w, i) => (
              <React.Fragment key={w}>
                <span className="wd" aria-hidden="true"><span style={{ transitionDelay: `${0.15 + i * 0.1}s` }}>{w}</span></span>{" "}
              </React.Fragment>
            ))}
          </h1>
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

/* Product photos uploaded by the admin are stored as "/uploads/products/x.jpg"
   (served by the API); full http(s) links are used as-is. */
function resolveImg(url) {
  if (!url) return null;
  return url.startsWith("/") ? `${API_BASE}${url}` : url;
}

/* The product's own photo if it has one — otherwise the keyword-based
   fallback photo, so products added before image_url existed still look good. */
function productImageSrc(product, width = 400) {
  return resolveImg(product.image_url) || menuImageUrl(getMenuImageId(product), width);
}

const money = (n) => `$${Number(n || 0).toFixed(2)}`;

/* Product photos shown under an assistant reply. */
function ProductCards({ products }) {
  return (
    <div className="chat-products">
      {products.map((p) => (
        <div className="chat-product" key={p.id}>
          <img src={productImageSrc(p, 320)} alt={p.name} loading="lazy" decoding="async" />
          <div className="chat-product-info">
            <span className="chat-product-name">{p.name}</span>
            {typeof p.price === "number" && <span className="chat-product-price">{money(p.price)}</span>}
          </div>
        </div>
      ))}
    </div>
  );
}

/* Cart / order receipt with a photo per line — shown for "view cart" and checkout. */
function CartCard({ cart }) {
  return (
    <div className="chat-cart">
      <div className="chat-cart-title">
        {cart.kind === "order" && (
          <svg className="order-check" viewBox="0 0 24 24" aria-hidden="true">
            <circle cx="12" cy="12" r="10" />
            <path d="M7 12.5l3.2 3.2L17 9" />
          </svg>
        )}
        {cart.kind === "order" ? `Order #${cart.order_id}` : "Your cart"}
      </div>
      {cart.items.map((it, i) => (
        <div className="chat-cart-row" key={i} data-cart-name={it.name} style={{ "--i": i }}>
          <img src={productImageSrc({ name: it.name, image_url: it.image_url }, 160)} alt={it.name} loading="lazy" decoding="async" />
          <div className="chat-cart-info">
            <span className="chat-cart-name">{it.name}</span>
            <span className="chat-cart-qty">{it.quantity} × {money(it.unit_price)}</span>
          </div>
          <span className="chat-cart-sub">{money(it.subtotal)}</span>
        </div>
      ))}
      <div className="chat-cart-total">
        <span>Total</span>
        <span>{money(cart.total)}</span>
      </div>
    </div>
  );
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
      <Reveal className="section-head">
        <h2>On the counter today</h2>
        <p>Made fresh, served warm, and made for sharing. Welcome to لمّة.</p>
      </Reveal>
      <div ref={gridRef} className={`menu-grid ${inView ? "in-view" : ""}`}>
        {error && <div className="menu-error">Couldn't load the menu right now — try asking the assistant instead.</div>}
        {!error && products === null && <div className="menu-empty">Menu's brewing — one moment.</div>}
        {!error && products && products.length === 0 && (
          <div className="menu-empty">Nothing on the counter yet — check back soon.</div>
        )}
        {!error && products && products.slice(0, 8).map((p) => {
          const imgId = getMenuImageId(p);
          const ownImage = resolveImg(p.image_url);
          return (
            <div className="menu-card" key={p.id}>
              <div className="menu-card-photo">
                {ownImage ? (
                  <img src={ownImage} alt={p.name} loading="lazy" decoding="async" />
                ) : (
                  <img
                    src={menuImageUrl(imgId, 800)}
                    srcSet={`${menuImageUrl(imgId, 400)} 400w, ${menuImageUrl(imgId, 800)} 800w`}
                    sizes="(max-width: 560px) 90vw, (max-width: 1024px) 45vw, 320px"
                    alt={p.name}
                    loading="lazy"
                    decoding="async"
                  />
                )}
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
/* "Fingerprint" of the newest message. The history endpoint only returns the
   last 20 messages, so counting them would miss updates in long chats. */
const lastMessageSig = (list) =>
  list && list.length ? `${list[list.length - 1].role}|${list[list.length - 1].content}` : "";

function ChatWidget({ token, isAdmin, onRequireAuth, openSignal, embedded = false }) {
  const [open, setOpen] = useState(embedded);
  const [guestMessages, setGuestMessages] = useState([]);
  const [conversations, setConversations] = useState([]);
  const [activeId, setActiveId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [pendingImage, setPendingImage] = useState(null); // admin: { url, preview }
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState("");
  const [unread, setUnread] = useState(false); // new assistant message arrived while the chat was closed
  const fileInputRef = useRef(null);
  const scrollRef = useRef(null);
  const serverSig = useRef("");   // newest message as the server last told us
  const openRef = useRef(open);
  const sendingRef = useRef(false);
  openRef.current = open;
  sendingRef.current = sending;

  /* the bag in the header counts what's in the customer's cart (from the latest cart card) */
  let cartCount = 0;
  for (let i = messages.length - 1; i >= 0; i--) {
    const c = messages[i].cards && messages[i].cards.cart;
    if (c) { cartCount = c.kind === "cart" ? c.items.reduce((n, it) => n + (it.quantity || 0), 0) : 0; break; }
  }
  const [held, setHeld] = useState(null);           // while the tongs carry an item, the bag keeps showing the OLD count
  const shownCount = held !== null ? held : cartCount;
  const [fly, setFly] = useState(null);
  const bagRef = useRef(null);
  const cartSnap = useRef({});                       // name → quantity, to know what was just added
  const cartCountRef = useRef(0);
  cartCountRef.current = cartCount;

  useEffect(() => {
    if (openSignal > 0) setOpen(true);
  }, [openSignal]);

  useEffect(() => {
    if (open) setUnread(false);
  }, [open]);

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
    serverSig.current = response.ok ? lastMessageSig(data) : "";
    cartSnap.current = {};
    if (response.ok) {
      for (let i = data.length - 1; i >= 0; i--) {
        const c = data[i].cards && data[i].cards.cart;
        if (c) { if (c.kind === "cart") c.items.forEach((it) => { cartSnap.current[it.name] = it.quantity; }); break; }
      }
    }
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
    if (!fly) return undefined;
    const bag = bagRef.current;
    if (prefersReducedMotion() || !bag) { setHeld(null); return undefined; }
    const timers = [];
    timers.push(setTimeout(() => {                    // give the new message a moment to scroll into view
      const rows = [...document.querySelectorAll(".chat-messages .chat-cart-row")];
      let launched = 0;
      fly.names.slice(0, 3).forEach((name) => {
        const row = rows.filter((r) => r.dataset.cartName === name).pop();
        const img = row && row.querySelector("img");
        if (!img) return;
        timers.push(setTimeout(() => flyTongs(img, bag, () => { setHeld(null); bumpBag(bag); }), launched * 450));
        launched++;
      });
      if (!launched) { setHeld(null); return; }
      timers.push(setTimeout(() => setHeld(null), 1300 + launched * 450));   // safety: never leave the old number stuck
    }, 450));
    return () => timers.forEach(clearTimeout);
  }, [fly]);

  /* Customers: find their latest conversation on page load (without creating
     one) so order updates can be picked up even before the chat is opened. */
  useEffect(() => {
    if (!token || isAdmin) return undefined;
    let cancelled = false;
    (async () => {
      try {
        const response = await authedFetch("/conversations");
        if (!response.ok || cancelled) return;
        const data = await response.json();
        if (!cancelled && data.length > 0) {
          setConversations(data);
          setActiveId((current) => current ?? data[0].id);
        }
      } catch { /* the chat still works normally when opened */ }
    })();
    return () => { cancelled = true; };
  }, [token, isAdmin]);

  /* Live updates: every 8s (and the moment the tab becomes visible) check the
     conversation for new messages — e.g. "your order is being prepared" sent
     by the admin — so the customer never has to refresh. Never runs while a
     message is being sent, so it can't overwrite what's on screen. */
  useEffect(() => {
    if (!token || isAdmin || !activeId) return undefined;
    let cancelled = false;
    async function poll() {
      if (document.hidden || sendingRef.current) return;
      try {
        const response = await authedFetch(`/conversations/${activeId}/messages`);
        if (!response.ok || cancelled || sendingRef.current) return;
        const data = await response.json();
        const sig = lastMessageSig(data);
        if (cancelled || sig === serverSig.current) return;
        serverSig.current = sig;
        setMessages(data);
        if (!openRef.current && data.length > 0 && data[data.length - 1].role === "assistant") {
          setUnread(true);
        }
      } catch { /* try again on the next tick */ }
    }
    const timer = setInterval(poll, 8000);
    const onVisible = () => { if (!document.hidden) poll(); };
    document.addEventListener("visibilitychange", onVisible);
    return () => {
      cancelled = true;
      clearInterval(timer);
      document.removeEventListener("visibilitychange", onVisible);
    };
  }, [token, isAdmin, activeId]);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, guestMessages, sending]);

  /* Admin: upload the picked image right away; the returned path is then
     sent along with the next chat message (add/update product). */
  async function handleFilePick(e) {
    const file = e.target.files && e.target.files[0];
    e.target.value = "";
    if (!file) return;
    setUploadError("");
    if (file.size > 5 * 1024 * 1024) {
      setUploadError("Image is too large (max 5 MB).");
      return;
    }
    setUploading(true);
    try {
      const form = new FormData();
      form.append("file", file);
      const response = await fetch(`${API_BASE}/admin/uploads/product-image`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` }, // no Content-Type: the browser sets the multipart boundary
        body: form,
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(typeof data.detail === "string" ? data.detail : "Upload failed.");
      }
      setPendingImage({ url: data.image_url, preview: URL.createObjectURL(file) });
    } catch (err) {
      setUploadError(err.message || "Upload failed.");
    } finally {
      setUploading(false);
    }
  }

  async function sendMessage(text) {
    if (!text || sending) return;
    setInput("");
    setSending(true);

    if (!token) {
      const history = guestMessages.map(({ role, content }) => ({ role, content }));
      setGuestMessages((prev) => [...prev, { role: "user", content: text }]);
      try {
        const response = await fetch(`${API_BASE}/chat/guest`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: text, history }),
        });
        const data = await response.json();
        setGuestMessages((prev) => [...prev, { role: "assistant", content: data.reply || "Sorry, something went wrong.", cards: data.cards }]);
      } catch {
        setGuestMessages((prev) => [...prev, { role: "assistant", content: "Sorry — I couldn't reach the menu right now." }]);
      } finally {
        setSending(false);
      }
      return;
    }

    if (!activeId) { setSending(false); return; }
    const attached = isAdmin ? pendingImage : null;
    setMessages((prev) => [...prev, { role: "user", content: text, localImage: attached?.preview }]);
    try {
      const response = await authedFetch(`${basePath}/chat`, {
        method: "POST",
        body: JSON.stringify({
          message: text,
          conversation_id: activeId,
          ...(attached ? { image_url: attached.url } : {}),
        }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(typeof data.detail === "string" ? data.detail : "Something went wrong.");
      noteCart(data.cards);   // first: the bag must know the tongs are coming before the message re-renders it
      setMessages((prev) => [...prev, { role: "assistant", content: data.reply, cards: data.cards }]);
      serverSig.current = `assistant|${data.reply}`;
      // Keep the attachment until a product was actually saved with it, so the
      // admin can answer a follow-up question ("what's the price?") without re-attaching.
      if (attached && data.image_used) setPendingImage(null);
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

  /* Which items did this reply just add? → the tongs carry them to the bag. */
  function noteCart(cards) {
    const cart = cards && cards.cart;
    if (!cart) return;
    if (cart.kind === "order") { cartSnap.current = {}; return; }
    const prevTotal = Object.values(cartSnap.current).reduce((n, q) => n + q, 0);
    const next = {};
    const added = [];
    cart.items.forEach((it) => {
      next[it.name] = it.quantity;
      if (it.quantity > (cartSnap.current[it.name] || 0)) added.push(it.name);
    });
    cartSnap.current = next;
    if (added.length) { setHeld(prevTotal); setFly({ id: Date.now(), names: added }); }
  }

  /* Checkout button inside a cart message: the server places the order
     directly, then the receipt (with photos) lands in the chat. */
  async function handleCheckout() {
    if (sending || !activeId) return;
    setSending(true);
    setMessages((prev) => [...prev, { role: "user", content: "Checkout" }]);
    try {
      const response = await authedFetch("/chat/checkout", {
        method: "POST",
        body: JSON.stringify({ conversation_id: activeId }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(typeof data.detail === "string" ? data.detail : "Something went wrong.");
      noteCart(data.cards);   // first: the bag must know the tongs are coming before the message re-renders it
      setMessages((prev) => [...prev, { role: "assistant", content: data.reply, cards: data.cards }]);
      serverSig.current = `assistant|${data.reply}`;
    } catch (err) {
      setMessages((prev) => [...prev, { role: "assistant", content: `Sorry — ${err.message}` }]);
    } finally {
      setSending(false);
    }
  }

  const activeMessages = token ? messages : guestMessages;

  return (
    <>
      {!open && !embedded && (
        <button
          className="chat-launcher"
          onClick={() => setOpen(true)}
          aria-label={unread ? "Open chat — new message" : "Open chat"}
        >
          <ChatBubbleIcon />
          {unread && <span className="chat-unread-dot" aria-hidden="true"></span>}
        </button>
      )}

      {open && (
        <div className={`chat-panel${embedded ? " embedded" : ""}`}>
          <div className="chat-panel-header">
            <div className="who">
              <MarkIcon />
              <div className="who-text">
                <span className="who-name">{isAdmin ? "Admin assistant" : "Ask Lamma"}</span>
                <span className="who-status">
                  <span className="status-dot" aria-hidden="true"></span>
                  Responds within a second
                </span>
              </div>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              {token && !isAdmin && (
                <button
                  type="button"
                  className="chat-bag"
                  ref={bagRef}
                  onClick={() => sendMessage("Show my cart")}
                  disabled={sending}
                  aria-label={`Your cart, ${shownCount} item${shownCount === 1 ? "" : "s"}`}
                  title="Your cart"
                >
                  <BagIcon />
                  {shownCount > 0 && <span key={shownCount} className="chat-bag-count">{shownCount}</span>}
                </button>
              )}
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
              {!embedded && (
                <button className="chat-panel-close" onClick={() => setOpen(false)} aria-label="Close chat"><CloseIcon /></button>
              )}
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
                {token
                  ? isAdmin
                    ? "Add, edit or delete products and users — just tell me what to do. Use the paperclip to attach a product photo."
                    : "Ask about your order, or what's good today."
                  : "Ask what's on the menu, what's fresh, or for a recommendation."}
              </div>
            )}
            {activeMessages.map((m, i) => {
              const showCartActions =
                !!token && !isAdmin && m.role === "assistant" &&
                m.cards?.cart?.kind === "cart" && i === activeMessages.length - 1;
              return (
                <div key={i} className={`msg-row ${m.role}`}>
                  <div className="msg-bubble" dir="auto">
                    {m.role === "user" && m.localImage && (
                      <img className="msg-attached-img" src={m.localImage} alt="Attached" />
                    )}
                    {m.role === "assistant" ? <MessageContent text={m.content} /> : m.content}
                    {m.role === "assistant" && m.cards?.cart && <CartCard cart={m.cards.cart} />}
                    {m.role === "assistant" && m.cards?.products?.length > 0 && (
                      <ProductCards products={m.cards.products} />
                    )}
                    {showCartActions && (
                      <div className="msg-actions">
                        <button
                          type="button"
                          className="msg-action-btn primary"
                          onClick={handleCheckout}
                          disabled={sending}
                        >
                          <CartIcon />
                          Checkout
                        </button>
                        <button
                          type="button"
                          className="msg-action-btn"
                          onClick={() => sendMessage("I'd like to add more items. What's on the menu?")}
                          disabled={sending}
                        >
                          Add more items
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

          {isAdmin && (pendingImage || uploading || uploadError) && (
            <div className={`chat-attachment ${uploadError ? "error" : ""}`}>
              {pendingImage && <img src={pendingImage.preview} alt="Attached product" />}
              <span>
                {uploadError
                  ? uploadError
                  : uploading
                  ? "Uploading image…"
                  : "Image attached — it will be saved with the product you add or update."}
              </span>
              <button type="button" onClick={() => { setPendingImage(null); setUploadError(""); }} aria-label="Remove image">×</button>
            </div>
          )}

          <form className="chat-input-bar" onSubmit={handleSend}>
            {isAdmin && (
              <>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/jpeg,image/png,image/webp,image/gif"
                  style={{ display: "none" }}
                  onChange={handleFilePick}
                />
                <button
                  type="button"
                  className="chat-attach-btn"
                  onClick={() => fileInputRef.current?.click()}
                  disabled={sending || uploading}
                  aria-label="Attach product image"
                  title="Attach a product image from your device"
                >
                  <AttachIcon />
                </button>
              </>
            )}
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              dir="auto"
              placeholder={token ? (isAdmin ? "e.g. Add Cheesecake for $4 with this photo…" : "Ask about your order…") : "Ask about the menu…"}
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
   Admin dashboard — sidebar + live incoming orders
   --------------------------------------------------------- */
const STATUS_LABEL = {
  pending: "New",
  preparing: "Preparing",
  ready: "Ready",
  out_for_delivery: "Out for delivery",
  delivered: "Delivered",
  cancelled: "Cancelled",
};
const ACTIVE_STATUSES = ["pending", "preparing", "ready", "out_for_delivery"];
/* What the admin can do next from each status: [newStatus, button label, primary?] */
const ORDER_ACTIONS = {
  pending: [["preparing", "Start preparing", true]],
  preparing: [["ready", "Mark ready", true]],
  ready: [["out_for_delivery", "Out for delivery", false], ["delivered", "Delivered", true]],
  out_for_delivery: [["delivered", "Mark delivered", true]],
};

function timeAgo(iso) {
  if (!iso) return "";
  const secs = Math.max(0, Math.round((Date.now() - new Date(iso).getTime()) / 1000));
  if (secs < 60) return "just now";
  const mins = Math.floor(secs / 60);
  if (mins < 60) return `${mins} min ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours} h ago`;
  return new Date(iso).toLocaleDateString();
}

function OrderCard({ order, onStatus }) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const actions = ORDER_ACTIONS[order.status] || [];
  const canCancel = ACTIVE_STATUSES.includes(order.status);

  async function change(status) {
    if (status === "cancelled" && !window.confirm(`Cancel order #${order.id}? The customer will be notified.`)) return;
    setBusy(true);
    setError("");
    try {
      await onStatus(order.id, status);
    } catch (err) {
      setError(err.message || "Could not update the order.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className={`order-card status-${order.status}`}>
      <div className="order-head">
        <div className="order-head-main">
          <span className="order-id">Order #{order.id}</span>
          <span className={`order-pill ${order.status}`}>{STATUS_LABEL[order.status] || order.status}</span>
        </div>
        <span className="order-time" title={order.created_at ? new Date(order.created_at).toLocaleString() : ""}>
          {timeAgo(order.created_at)}
        </span>
      </div>
      <div className="order-customer">
        <strong>{order.username}</strong>
        {order.phone && <a href={`tel:${order.phone}`}>{order.phone}</a>}
      </div>
      <div className="order-items">
        {order.items.map((it, i) => (
          <div className="order-item" key={i}>
            <img
              src={productImageSrc({ name: it.product_name, image_url: it.image_url }, 120)}
              alt={it.product_name}
              loading="lazy"
              decoding="async"
            />
            <div className="order-item-info">
              <span className="order-item-name">{it.product_name}</span>
              <span className="order-item-qty">{it.quantity} × {money(it.unit_price)}</span>
            </div>
            <span className="order-item-sub">{money(it.subtotal)}</span>
          </div>
        ))}
      </div>
      <div className="order-foot">
        <span className="order-total">Total {money(order.total_price)}</span>
        <div className="order-actions">
          {actions.map(([status, label, primary]) => (
            <button
              key={status}
              type="button"
              className={`msg-action-btn${primary ? " primary" : ""}`}
              disabled={busy}
              onClick={() => change(status)}
            >
              {label}
            </button>
          ))}
          {canCancel && (
            <button type="button" className="msg-action-btn danger" disabled={busy} onClick={() => change("cancelled")}>
              Cancel
            </button>
          )}
        </div>
      </div>
      {error && <div className="order-error">{error}</div>}
    </div>
  );
}

function OrdersBoard({ orders, connError, onStatus }) {
  const [filter, setFilter] = useState("active");

  if (orders === null) {
    return <div className="orders-empty">{connError ? "Couldn't load orders — retrying…" : "Loading orders…"}</div>;
  }
  const active = orders.filter((o) => ACTIVE_STATUSES.includes(o.status));
  const done = orders.filter((o) => !ACTIVE_STATUSES.includes(o.status));
  const shown = filter === "active" ? active : filter === "done" ? done : orders;

  return (
    <>
      <div className="orders-tabs">
        {[["active", "Active", active.length], ["done", "Completed", done.length], ["all", "All", orders.length]].map(
          ([key, label, count]) => (
            <button
              key={key}
              type="button"
              className={`orders-tab${filter === key ? " active" : ""}`}
              onClick={() => setFilter(key)}
            >
              {label} <span>{count}</span>
            </button>
          )
        )}
        <span className={`orders-live${connError ? " offline" : ""}`}>
          <span className="orders-live-dot" aria-hidden="true"></span>
          {connError ? "Reconnecting…" : "Live"}
        </span>
      </div>
      {shown.length === 0 ? (
        <div className="orders-empty">
          {filter === "active" ? "No active orders right now. New orders will appear here automatically." : "Nothing here yet."}
        </div>
      ) : (
        <div className="orders-list">
          {shown.map((o) => <OrderCard key={o.id} order={o} onStatus={onStatus} />)}
        </div>
      )}
    </>
  );
}

function AdminDashboard({ token, onLogout, onViewSite }) {
  const [section, setSection] = useState("orders");
  const [orders, setOrders] = useState(null); // null until the first load
  const [connError, setConnError] = useState(false);
  const [toast, setToast] = useState(null);
  const knownIds = useRef(null);

  /* Poll for orders every 8s so new ones appear without asking the chatbot.
     Paused while the tab is hidden, refreshed the moment it's visible again. */
  useEffect(() => {
    let cancelled = false;
    async function load() {
      if (document.hidden) return;
      try {
        const response = await fetch(`${API_BASE}/admin/orders`, { headers: { Authorization: `Bearer ${token}` } });
        if (response.status === 401) { onLogout(); return; }
        if (!response.ok) throw new Error("bad status");
        const data = await response.json();
        if (cancelled) return;
        if (knownIds.current) {
          const fresh = data.filter((o) => !knownIds.current.has(o.id));
          if (fresh.length) {
            setToast(fresh.length === 1 ? `New order #${fresh[0].id} from ${fresh[0].username}` : `${fresh.length} new orders`);
          }
        }
        knownIds.current = new Set(data.map((o) => o.id));
        setOrders(data);
        setConnError(false);
      } catch {
        if (!cancelled) setConnError(true);
      }
    }
    load();
    const timer = setInterval(load, 8000);
    const onVisible = () => { if (!document.hidden) load(); };
    document.addEventListener("visibilitychange", onVisible);
    return () => {
      cancelled = true;
      clearInterval(timer);
      document.removeEventListener("visibilitychange", onVisible);
    };
  }, [token]);

  useEffect(() => {
    if (!toast) return undefined;
    const t = setTimeout(() => setToast(null), 7000);
    return () => clearTimeout(t);
  }, [toast]);

  const pending = orders ? orders.filter((o) => o.status === "pending").length : 0;

  useEffect(() => {
    const original = document.title;
    document.title = pending > 0 ? `(${pending}) New orders · Lamma` : original;
    return () => { document.title = original; };
  }, [pending]);

  async function changeStatus(orderId, status) {
    const response = await fetch(`${API_BASE}/admin/orders/${orderId}/status`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ status }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(typeof data.detail === "string" ? data.detail : "Could not update the order.");
    setOrders((prev) => (prev ? prev.map((o) => (o.id === data.id ? data : o)) : prev));
  }

  return (
    <div className="dash">
      <aside className="dash-sidebar">
        <div className="dash-brand">
          <MarkIcon />
          <span className="dash-brand-name">Lamma</span>
          <span className="admin-tag">Admin</span>
        </div>
        <nav className="dash-nav">
          <button
            type="button"
            className={`dash-nav-item${section === "orders" ? " active" : ""}`}
            onClick={() => setSection("orders")}
          >
            <span className="dash-nav-title">
              Incoming orders
              {pending > 0 && <span className="dash-badge">{pending}</span>}
            </span>
            <span className="dash-nav-sub">Updates automatically</span>
          </button>
          <button
            type="button"
            className={`dash-nav-item${section === "assistant" ? " active" : ""}`}
            onClick={() => setSection("assistant")}
          >
            <span className="dash-nav-title">Menu &amp; users</span>
            <span className="dash-nav-sub">Add, edit or delete with the assistant</span>
          </button>
        </nav>
        <div className="dash-foot">
          <button type="button" className="dash-foot-btn" onClick={onViewSite}>View website</button>
          <button type="button" className="dash-foot-btn" onClick={onLogout}>Log out</button>
        </div>
      </aside>

      <main className="dash-main">
        {toast && (
          <button type="button" className="dash-toast" onClick={() => { setSection("orders"); setToast(null); }}>
            🔔 {toast}
          </button>
        )}
        <section className="dash-section" style={{ display: section === "orders" ? "block" : "none" }}>
          <h1 className="dash-title">Incoming orders</h1>
          <OrdersBoard orders={orders} connError={connError} onStatus={changeStatus} />
        </section>
        <section className="dash-section chat" style={{ display: section === "assistant" ? "block" : "none" }}>
          <ChatWidget token={token} isAdmin={true} embedded={true} onRequireAuth={() => {}} openSignal={0} />
        </section>
      </main>
    </div>
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
  const [adminView, setAdminView] = useState("dashboard"); // admins land on the dashboard

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
    setAdminView("dashboard");
  }

  if (token && role === "admin" && adminView === "dashboard") {
    return (
      <AdminDashboard
        token={token}
        onLogout={handleLogout}
        onViewSite={() => setAdminView("site")}
      />
    );
  }

  return (
    <>
      <Intro />
      <Nav
        isAuthed={!!token}
        isAdmin={role === "admin"}
        onLogin={() => setAuthModal("login")}
        onSignup={() => setAuthModal("signup")}
        onLogout={handleLogout}
        onDashboard={() => setAdminView("dashboard")}
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