import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os, json

st.set_page_config(page_title="ShopperIQ", page_icon="🛒", layout="wide")

st.markdown("""<style>
.main{background:#F7F8FC;}
.kpi{background:white;border-radius:10px;padding:20px;margin-bottom:8px;border-left:4px solid;}
.kv{font-size:28px;font-weight:800;line-height:1;}
.kl{font-size:11px;color:#8A93A6;margin-top:6px;text-transform:uppercase;}
.cc{border-radius:12px;padding:20px;margin-bottom:10px;}
.cn{font-size:17px;font-weight:800;color:white;margin-bottom:2px;}
.cs{font-size:10px;opacity:0.75;color:white;text-transform:uppercase;margin-bottom:12px;}
.sp{display:inline-block;background:rgba(255,255,255,0.2);border-radius:20px;padding:3px 10px;font-size:11px;color:white;margin:2px 2px 2px 0;}
.wb{background:#FFF3F3;border:1px solid #F5BFBF;border-left:4px solid #E8394A;border-radius:8px;padding:16px 20px;margin-bottom:20px;}
.wt{font-weight:700;color:#C02030;font-size:13px;margin-bottom:6px;}
.wx{color:#7A3040;font-size:13px;line-height:1.7;}
.ib{background:#F0F4FF;border:1px solid #C5D3F0;border-left:4px solid #1B3A6B;border-radius:8px;padding:14px 18px;margin-bottom:16px;}
.cu{background:#1B3A6B;color:white;border-radius:12px 12px 4px 12px;padding:12px 16px;margin:6px 0 6px 20%;font-size:13px;line-height:1.6;}
.ca{background:white;color:#2C3550;border-radius:12px 12px 12px 4px;padding:12px 16px;margin:6px 20% 6px 0;font-size:13px;line-height:1.6;box-shadow:0 2px 8px rgba(27,58,107,0.1);}
.cl{font-size:10px;color:rgba(255,255,255,0.6);margin-bottom:4px;text-transform:uppercase;}
.cl2{font-size:10px;color:#8A93A6;margin-bottom:4px;text-transform:uppercase;}
.mc{border-radius:10px;padding:18px 20px;margin:10px 0;border-left:4px solid;background:white;}
.mt{display:inline-block;border-radius:4px;padding:3px 10px;font-size:10px;font-weight:700;text-transform:uppercase;margin-bottom:10px;}
.mm{font-size:15px;line-height:1.65;color:#1B3A6B;font-weight:600;margin-bottom:8px;}
.mw{font-size:11px;color:#8A93A6;border-top:1px solid #EEF0F6;padding-top:8px;line-height:1.6;}
.mr{display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid #F0F2F8;font-size:12px;}
.ml{color:#8A93A6;} .mv{color:#1B3A6B;font-weight:600;}
#MainMenu{visibility:hidden;}footer{visibility:hidden;}
</style>""", unsafe_allow_html=True)

NAVY = "#1B3A6B"
CORAL = "#E8394A"
GREEN = "#2E7D5E"

FP = pd.DataFrame({
    "recency":              [15.82, 40.39,  8.63],
    "frequency":            [10.59,  1.76, 11.12],
    "monetary":             [644.83, 53.24,563.07],
    "avg_basket":           [66.30,  35.63, 66.48],
    "loyalty_tenure_days":  [2571,   1550,  2109],
    "channel_spend_ECOMMERCE":[18.40, 0.53, 13.85],
    "promo_conversion_rate":[0.49,   0.00,  0.00],
    "avg_face_value":       [5.12,   0.37,  0.23],
    "n_promo_channels":     [1.17,   0.27,  0.23],
}, index=[0,1,2])
FS = pd.Series({0:46162, 1:156124, 2:157244})
FR = pd.Series({0:8273492, 1:88648768, 2:29695188})
FT = 359530

META = {
    0: {
        "name": "Power Shoppers", "persona": "The Deal Hunter", "emoji": "Power",
        "bg": "linear-gradient(135deg,#1B3A6B,#24508F)", "color": NAVY, "light": "#EEF3FF",
        "channel": "Coupon Network / iGraal / App Push",
        "offer": "High face-value coupons EUR5-EUR10",
        "timing": "Monday-Tuesday",
        "coupons": "YES - invest here (49% conversion)",
        "coupon_cost": 18748, "coupon_pct": 3.8, "roi": 441,
        "cpg": "Drive trial with proven 49% conversion",
        "retail": "Basket fill-rate uplift on promoted items",
        "consumer": "Maximum savings on items they already buy",
        "verdict": "UNDER-FUNDED",
    },
    1: {
        "name": "Passive Mass", "persona": "The Sleeping Giant", "emoji": "Sleep",
        "bg": "linear-gradient(135deg,#E8394A,#F06070)", "color": CORAL, "light": "#FFF0F2",
        "channel": "Marmiton / 750g / Retargeting",
        "offer": "Win-back bundle / Habit rewards",
        "timing": "Weekend only",
        "coupons": "NO - 0% conversion, use re-engagement",
        "coupon_cost": 11842, "coupon_pct": 2.4, "roi": 7486,
        "cpg": "Re-activate lapsed buyers at scale",
        "retail": "Frequency uplift - +1 trip = millions in revenue",
        "consumer": "Rediscover products at low risk",
        "verdict": "WRONG TOOL",
    },
    2: {
        "name": "Active Regulars", "persona": "The Loyal Regular", "emoji": "Trophy",
        "bg": "linear-gradient(135deg,#2E7D5E,#3A9B74)", "color": GREEN, "light": "#EDFAF4",
        "channel": "Cashier Print / Loyalty App / DOOH",
        "offer": "Loyalty reward / Premium bundle / Cart upsell",
        "timing": "Wednesday-Thursday",
        "coupons": "NO - redirect budget to Cluster 0",
        "coupon_cost": 465583, "coupon_pct": 93.8, "roi": 64,
        "cpg": "Upsell to premium SKUs via loyalty mechanics",
        "retail": "Protect retention and maximise basket value",
        "consumer": "Recognised and rewarded for consistency",
        "verdict": "OVER-FUNDED",
    },
}

PRODUCTS = [
    "Danone Activia Yogurt", "President Butter", "Orangina 1.5L",
    "Fleury Michon Ham", "Evian Still Water 6-pack", "Bonne Maman Jam",
    "Knorr Chicken Stock", "Milka Chocolate Bar", "Panzani Pasta 500g",
    "Herta Frankfurt Sausages", "LU Petit Ecolier", "Amora Dijon Mustard",
    "Lipton Ice Tea Peach", "Yoplait Fromage Frais", "Badoit Sparkling Water",
]

SUGS = [
    "Which cluster should I target for a premium yogurt launch?",
    "Where is our coupon budget being wasted?",
    "Best omnichannel strategy combining in-store and e-commerce?",
    "How do I reactivate dormant Cluster 1 shoppers?",
    "Explain the ROI difference between the three clusters.",
    "How does ShopperIQ benefit CPG brands, retailers AND consumers?",
]


@st.cache_data(show_spinner=False)
def load_data(drive_path):
    if drive_path and os.path.exists(drive_path):
        try:
            mc = pd.read_parquet(drive_path) if drive_path.endswith(".parquet") else pd.read_csv(drive_path)
            if "cluster" in mc.columns:
                feats = [f for f in ["recency","frequency","monetary","avg_basket",
                    "loyalty_tenure_days","channel_spend_ECOMMERCE",
                    "promo_conversion_rate","avg_face_value","n_promo_channels"] if f in mc.columns]
                p = mc.groupby("cluster")[feats].mean().round(2)
                s = mc["cluster"].value_counts().sort_index()
                r = mc.groupby("cluster")["monetary"].sum()
                return p, s, r, len(mc), "Live data from Drive"
        except Exception:
            pass
    try:
        import __main__
        mc = getattr(__main__, "master_clean", None)
        if mc is not None and "cluster" in mc.columns:
            feats = [f for f in ["recency","frequency","monetary","avg_basket",
                "loyalty_tenure_days","channel_spend_ECOMMERCE",
                "promo_conversion_rate","avg_face_value","n_promo_channels"] if f in mc.columns]
            p = mc.groupby("cluster")[feats].mean().round(2)
            s = mc["cluster"].value_counts().sort_index()
            r = mc.groupby("cluster")["monetary"].sum()
            return p, s, r, len(mc), "Live data from Colab session"
    except Exception:
        pass
    return FP, FS, FR, FT, "Pre-computed values (Cell 32)"


def call_ai(messages, system, gemini_key, groq_key):
    if gemini_key and len(gemini_key) > 10:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system)
            history = []
            for msg in messages[:-1]:
                role = "user" if msg["role"] == "user" else "model"
                history.append({"role": role, "parts": [msg["content"]]})
            chat = model.start_chat(history=history)
            resp = chat.send_message(messages[-1]["content"])
            return resp.text, "Gemini"
        except Exception:
            pass
    if groq_key and len(groq_key) > 10:
        try:
            from groq import Groq
            all_msgs = [{"role": "system", "content": system}] + messages
            resp = Groq(api_key=groq_key).chat.completions.create(
                model="llama-3.3-70b-versatile", messages=all_msgs, max_tokens=800)
            return resp.choices[0].message.content, "Groq"
        except Exception:
            pass
    return None, None


def build_system(profiles, sizes, revenue, total):
    lines = [
        "You are ShopperIQ, expert AI marketing strategist for Catalina FMCG shopper activation.",
        "You analyse real French grocery shopper data and give sharp data-backed recommendations.",
        "",
    ]
    for i in range(3):
        m = META[i]
        p = profiles.loc[i]
        conv = p["promo_conversion_rate"] * 100
        lines.append("CLUSTER " + str(i) + " - " + m["name"] + " (" + m["persona"] + "):")
        lines.append("  Size: " + str(sizes[i]) + " shoppers (" + str(round(sizes[i]/total*100,1)) + "% of base)")
        lines.append("  Recency: " + str(round(p["recency"],1)) + "d | Freq: " + str(round(p["frequency"],1)) + " | Basket: EUR" + str(round(p["avg_basket"],2)))
        lines.append("  Conv: " + str(round(conv,0)) + "% | Budget: EUR" + str(m["coupon_cost"]) + " (" + str(m["coupon_pct"]) + "%) | ROI: " + str(m["roi"]) + "x")
        lines.append("  Channel: " + m["channel"])
        lines.append("")
    lines += [
        "KEY INSIGHT: 93.8% of coupon budget goes to Cluster 2 with 0% conversion.",
        "Cluster 0 converts at 49% but gets only 3.8% of budget.",
        "Answer in 2-4 paragraphs. Cite specific numbers. Be sharp and impressive.",
        "Explain value for CPG brands, retailers, AND consumers when relevant.",
    ]
    return "\n".join(lines)


# SIDEBAR
with st.sidebar:
    st.markdown("<div style='text-align:center;padding:16px 0 20px;'><div style='font-size:22px;font-weight:800;color:#1B3A6B;'>ShopperIQ</div><div style='font-size:10px;color:#AAB0C0;text-transform:uppercase;letter-spacing:0.1em;margin-top:3px;'>Catalina x ESCP 2026</div></div>", unsafe_allow_html=True)
    page = st.radio("Nav", ["Dashboard", "AI Strategist", "Message Lab"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**Google Drive Path**")
    drive_path = st.text_input("Drive path", value="/content/drive/MyDrive/master_clean.csv", label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**Free AI Keys**")
    st.caption("Option 1: Gemini - free at aistudio.google.com")
    gemini_key = st.text_input("Gemini key", type="password", placeholder="AIza...", label_visibility="collapsed")
    st.caption("Option 2: Groq - free at console.groq.com")
    groq_key = "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"
    has_ai = (gemini_key and len(gemini_key) > 10) or (groq_key and len(groq_key) > 10)
    st.caption("AI ready" if has_ai else "Paste a key above to enable AI")
    st.markdown("---")
    st.caption("359,530 shoppers | K-Means K=3 | Silhouette 0.228")

profiles, sizes, revenue, total, data_status = load_data(drive_path)

# HEADER
header_html = (
    "<div style='background:linear-gradient(135deg,#1B3A6B,#24508F);padding:22px 28px;"
    "border-radius:12px;margin-bottom:22px;display:flex;align-items:center;justify-content:space-between;'>"
    "<div><div style='font-size:26px;font-weight:800;color:white;'>Shopper"
    "<span style=\"color:#F5A0A8;\">IQ</span></div>"
    "<div style='color:rgba(255,255,255,0.7);font-size:12px;margin-top:3px;'>"
    "Omnichannel Shopper Activation &middot; " + data_status + "</div></div>"
    "<div style='background:rgba(255,255,255,0.15);border-radius:20px;padding:5px 14px;"
    "color:white;font-size:11px;font-weight:600;'>ESCP x Catalina Hackathon 2026</div></div>"
)
st.markdown(header_html, unsafe_allow_html=True)


# ─── DASHBOARD ────────────────────────────────────────────────────────────────
if page == "Dashboard":
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown("<div class='kpi' style='border-color:#1B3A6B'><div class='kv' style='color:#1B3A6B'>" + str(total) + "</div><div class='kl'>Shoppers Analysed</div></div>", unsafe_allow_html=True)
    with k2:
        st.markdown("<div class='kpi' style='border-color:#E8394A'><div class='kv' style='color:#E8394A'>EUR" + str(round(revenue.sum()/1e6,1)) + "M</div><div class='kl'>Total Revenue</div></div>", unsafe_allow_html=True)
    with k3:
        st.markdown("<div class='kpi' style='border-color:#2E7D5E'><div class='kv' style='color:#2E7D5E'>EUR" + str(round(profiles["avg_basket"].mean(),2)) + "</div><div class='kl'>Avg Basket Size</div></div>", unsafe_allow_html=True)
    with k4:
        st.markdown("<div class='kpi' style='border-color:#C0392B'><div class='kv' style='color:#C0392B'>93.8%</div><div class='kl'>Coupon Budget Misallocated</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div class='wb'><div class='wt'>Warning: Critical Budget Misallocation Detected</div><div class='wx'><strong>EUR465,583 (93.8%)</strong> of all coupon spend goes to Cluster 2 which has a <strong>0% conversion rate</strong>. Cluster 0 converts at <strong>49%</strong> but receives only <strong>EUR18,748 (3.8%)</strong>. Redirecting just 20% would fund approximately 18,000 additional high-converting activations.</div></div>", unsafe_allow_html=True)

    st.markdown("<strong>Shopper Segments</strong><hr style='margin:6px 0 14px;border-color:#E8394A;border-width:2px;'>", unsafe_allow_html=True)
    c0, c1, c2 = st.columns(3)
    for col, cid in [(c0, 0), (c1, 1), (c2, 2)]:
        with col:
            m = META[cid]
            p = profiles.loc[cid]
            conv = round(p["promo_conversion_rate"] * 100, 0)
            pct = round(sizes[cid] / total * 100, 1)
            card_html = (
                "<div class='cc' style='background:" + m["bg"] + ";'>"
                "<div style='font-size:13px;font-weight:700;color:white;margin-bottom:4px;'>[" + m["emoji"] + "]</div>"
                "<div class='cn'>Cluster " + str(cid) + " - " + m["name"] + "</div>"
                "<div class='cs'>" + m["persona"] + "</div>"
                "<div style='margin-bottom:8px;'>"
                "<span class='sp'>" + str(sizes[cid]) + " shoppers</span>"
                "<span class='sp'>" + str(pct) + "%</span></div>"
                "<div>"
                "<span class='sp'>" + str(round(p["frequency"],1)) + " trips</span>"
                "<span class='sp'>EUR" + str(round(p["avg_basket"],0)) + " basket</span>"
                "<span class='sp'>" + str(int(conv)) + "% promo</span></div>"
                "<div style='margin-top:12px;padding:5px 10px;background:rgba(255,255,255,0.2);"
                "border-radius:20px;font-size:10px;color:white;font-weight:700;display:inline-block;'>"
                + m["verdict"] + "</div></div>"
            )
            st.markdown(card_html, unsafe_allow_html=True)

    st.markdown("<br><strong>Cluster Deep-Dives</strong><hr style='margin:6px 0 14px;border-color:#E8394A;border-width:2px;'>", unsafe_allow_html=True)
    for cid in [0, 1, 2]:
        m = META[cid]
        p = profiles.loc[cid]
        conv = round(p["promo_conversion_rate"] * 100, 0)
        with st.expander("Cluster " + str(cid) + " - " + m["name"] + "  |  " + m["persona"], expanded=(cid == 0)):
            dl, dr = st.columns(2)
            with dl:
                st.markdown("**Behavioural Metrics**")
                rows = [
                    ("Shoppers", str(sizes[cid]) + " (" + str(round(sizes[cid]/total*100,1)) + "%)"),
                    ("Recency", str(round(p["recency"],1)) + " days ago"),
                    ("Frequency", str(round(p["frequency"],1)) + " trips"),
                    ("Avg Basket", "EUR" + str(round(p["avg_basket"],2))),
                    ("Spend/Shopper", "EUR" + str(round(p["monetary"],2))),
                    ("Tenure", str(round(p["loyalty_tenure_days"]/365,1)) + " yrs"),
                    ("E-commerce", "EUR" + str(round(p["channel_spend_ECOMMERCE"],2))),
                    ("Promo Conv.", str(int(conv)) + "%"),
                    ("Coupon Budget", "EUR" + str(m["coupon_cost"]) + " (" + str(m["coupon_pct"]) + "%)"),
                ]
                for lbl, val in rows:
                    st.markdown("<div class='mr'><span class='ml'>" + lbl + "</span><span class='mv'>" + val + "</span></div>", unsafe_allow_html=True)
            with dr:
                st.markdown("**Activation Strategy**")
                strat = [
                    ("Channel", m["channel"]),
                    ("Offer", m["offer"]),
                    ("Timing", m["timing"]),
                    ("Use Coupons?", m["coupons"]),
                ]
                for lbl, val in strat:
                    st.markdown("<div class='mr'><span class='ml'>" + lbl + "</span><span class='mv'>" + val + "</span></div>", unsafe_allow_html=True)
                st.markdown("<br>**Stakeholder Value**", unsafe_allow_html=True)
                st.markdown("CPG: " + m["cpg"])
                st.markdown("Retail: " + m["retail"])
                st.markdown("Consumer: " + m["consumer"])

    st.markdown("<br><strong>Visual Analytics</strong><hr style='margin:6px 0 14px;border-color:#E8394A;border-width:2px;'>", unsafe_allow_html=True)
    ch1, ch2 = st.columns(2)
    with ch1:
        fig = go.Figure(go.Pie(
            labels=["C0 " + META[0]["name"], "C1 " + META[1]["name"], "C2 " + META[2]["name"]],
            values=[sizes[0], sizes[1], sizes[2]],
            hole=0.55, marker_colors=[NAVY, CORAL, GREEN], textinfo="percent+label"))
        fig.update_layout(title="Shopper Base Composition", showlegend=False, height=300,
            margin=dict(t=40, b=10, l=10, r=10), paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)
    with ch2:
        fig2 = go.Figure()
        for cid in range(3):
            fig2.add_trace(go.Scatter(
                x=[META[cid]["coupon_cost"]],
                y=[profiles.loc[cid, "promo_conversion_rate"] * 100],
                mode="markers+text", text=["C" + str(cid)], textposition="top center",
                marker=dict(size=max(sizes[cid]//4000, 20),
                            color=[NAVY, CORAL, GREEN][cid], opacity=0.85)))
        fig2.update_layout(title="Budget vs Conversion", xaxis_title="Coupon Budget (EUR)",
            yaxis_title="Conversion (%)", height=300, showlegend=False,
            margin=dict(t=40, b=40, l=40, r=10), paper_bgcolor="white", plot_bgcolor="#F7F8FC")
        st.plotly_chart(fig2, use_container_width=True)
    ch3, ch4 = st.columns(2)
    with ch3:
        fig3 = go.Figure(go.Bar(
            x=["C0 " + META[0]["name"], "C1 " + META[1]["name"], "C2 " + META[2]["name"]],
            y=[revenue[0]/1e6, revenue[1]/1e6, revenue[2]/1e6],
            marker_color=[NAVY, CORAL, GREEN],
            text=["EUR" + str(round(revenue[i]/1e6,1)) + "M" for i in range(3)],
            textposition="outside"))
        fig3.update_layout(title="Revenue by Cluster", yaxis_title="Revenue (EUR M)", height=300,
            margin=dict(t=40, b=40, l=40, r=10), paper_bgcolor="white", plot_bgcolor="#F7F8FC")
        st.plotly_chart(fig3, use_container_width=True)
    with ch4:
        cats = ["Frequency", "Basket", "Promo", "Tenure", "E-comm"]
        keys = ["frequency", "avg_basket", "promo_conversion_rate", "loyalty_tenure_days", "channel_spend_ECOMMERCE"]
        maxes = [11.12, 66.48, 0.49, 2571, 18.40]
        fig4 = go.Figure()
        for cid in range(3):
            p = profiles.loc[cid]
            vals = [p[k] / mx for k, mx in zip(keys, maxes)]
            fig4.add_trace(go.Scatterpolar(
                r=vals + [vals[0]], theta=cats + [cats[0]], fill="toself",
                name=META[cid]["name"], line_color=[NAVY, CORAL, GREEN][cid],
                fillcolor=[NAVY, CORAL, GREEN][cid], opacity=0.2))
        fig4.update_layout(title="Behaviour Radar", showlegend=True, height=300,
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            margin=dict(t=40, b=10, l=10, r=10), paper_bgcolor="white")
        st.plotly_chart(fig4, use_container_width=True)


# ─── AI STRATEGIST ────────────────────────────────────────────────────────────
elif page == "AI Strategist":
    system = build_system(profiles, sizes, revenue, total)
    if not has_ai:
        st.markdown("<div class='ib'><b>AI features need a free API key</b><br><br><b>Option 1 - Google Gemini:</b> Go to aistudio.google.com, click Get API Key, copy the key starting with AIza and paste in sidebar.<br><br><b>Option 2 - Groq:</b> Go to console.groq.com, sign up free, go to API Keys, create and copy key starting with gsk_ and paste in sidebar.</div>", unsafe_allow_html=True)

    st.markdown("**Try asking:**")
    cols = st.columns(3)
    for i, sug in enumerate(SUGS):
        if cols[i % 3].button(sug, key="sug_" + str(i), use_container_width=True):
            st.session_state.setdefault("chat", [])
            st.session_state["chat"].append({"role": "user", "content": sug})

    st.markdown("---")
    if "chat" not in st.session_state:
        st.session_state["chat"] = []

    if not st.session_state["chat"]:
        st.markdown("<div class='ca'><div class='cl2'>ShopperIQ AI</div>Hi! I have full context on your 3 shopper clusters from the Catalina dataset. Ask me anything about campaign strategy, channel selection, ROI, or how to pitch these segments to a CPG client. Use the buttons above or type below.</div>", unsafe_allow_html=True)

    for msg in st.session_state["chat"]:
        if msg["role"] == "user":
            st.markdown("<div class='cu'><div class='cl'>You</div>" + msg["content"] + "</div>", unsafe_allow_html=True)
        else:
            content = msg["content"].replace("\n", "<br>")
            st.markdown("<div class='ca'><div class='cl2'>ShopperIQ AI</div>" + content + "</div>", unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        ci, cb = st.columns([5, 1])
        user_input = ci.text_input("Message", placeholder="Ask about clusters, channels, ROI...", label_visibility="collapsed")
        submitted = cb.form_submit_button("Send", use_container_width=True)

    if submitted and user_input:
        st.session_state["chat"].append({"role": "user", "content": user_input})
        if has_ai:
            with st.spinner("Thinking..."):
                reply, source = call_ai(st.session_state["chat"], system, gemini_key, groq_key)
            if reply:
                st.session_state["chat"].append({"role": "assistant", "content": reply})
            else:
                st.session_state["chat"].append({"role": "assistant", "content": "API call failed. Check your key and internet connection."})
        else:
            st.session_state["chat"].append({"role": "assistant", "content": "No AI key found. Please add a Gemini or Groq key in the sidebar."})
        st.rerun()

    if st.button("Clear conversation"):
        st.session_state["chat"] = []
        st.rerun()


# ─── MESSAGE LAB ──────────────────────────────────────────────────────────────
elif page == "Message Lab":
    st.markdown("Generate 3 personalised marketing messages for any product and cluster.")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        product_sel = st.selectbox("Product", ["-- Select --"] + PRODUCTS)
        product_custom = st.text_input("Or type custom product", placeholder="e.g. Bio Pasta 500g")
        product = product_custom if product_custom else ("" if product_sel == "-- Select --" else product_sel)
    with col_b:
        cluster_sel = st.selectbox("Target Cluster",
            ["-- Select --", "Cluster 0 - Power Shoppers", "Cluster 1 - Passive Mass", "Cluster 2 - Active Regulars"])
        cluster_id = None
        if "0" in cluster_sel:
            cluster_id = 0
        elif "1" in cluster_sel:
            cluster_id = 1
        elif "2" in cluster_sel:
            cluster_id = 2
    with col_c:
        channel_sel = st.selectbox("Channel", [
            "Auto (from cluster)", "Cashier coupon", "App push",
            "Email", "DOOH screen", "Coupon Network", "Marmiton", "E-commerce cart"])

    if cluster_id is not None:
        m = META[cluster_id]
        p = profiles.loc[cluster_id]
        conv = round(p["promo_conversion_rate"] * 100, 0)
        clr = [NAVY, CORAL, GREEN][cluster_id]
        st.markdown(
            "<div style='background:" + m["light"] + ";border:1px solid " + clr + "33;border-radius:8px;padding:14px 18px;margin:10px 0;'>"
            "<strong style='color:" + clr + ";'>Cluster " + str(cluster_id) + " - " + m["name"] + "</strong>"
            "<span style='color:" + clr + ";font-size:12px;margin-left:8px;'>" + m["persona"] + "</span><br><br>"
            "<span style='background:" + clr + ";color:white;border-radius:12px;padding:3px 10px;font-size:11px;margin-right:6px;'>" + str(int(conv)) + "% conversion</span>"
            "<span style='background:" + clr + ";color:white;border-radius:12px;padding:3px 10px;font-size:11px;'>" + m["timing"] + "</span>"
            "<p style='margin:10px 0 0;font-size:12px;color:#556;'>" + m["offer"] + "</p></div>",
            unsafe_allow_html=True)

    can_gen = bool(product) and cluster_id is not None and has_ai
    generate = st.button("Generate Personalised Messages", type="primary", disabled=not can_gen, use_container_width=True)
    if not has_ai:
        st.info("Add a free Gemini or Groq key in the sidebar to generate messages.")

    if generate and can_gen:
        m = META[cluster_id]
        p = profiles.loc[cluster_id]
        conv = round(p["promo_conversion_rate"] * 100, 0)
        channel = m["channel"] if "Auto" in channel_sel else channel_sel

        prompt_parts = [
            "Generate exactly 3 personalised marketing messages for:",
            "Product: " + product,
            "Target: Cluster " + str(cluster_id) + " - " + m["name"] + " (" + m["persona"] + ")",
            "Profile: " + str(int(conv)) + "% promo conversion | EUR" + str(round(p["avg_basket"],2)) + " basket | " + m["timing"] + " | Channel: " + channel,
            "Offer type: " + m["offer"],
            "",
            "Rules:",
            "- 2-3 sentences each",
            "- Match the cluster psychology exactly",
            "- Cluster 0: lead with EUR5+ saving amount (they NEED a big discount to act)",
            "- Cluster 1: lead with rediscovery (they need a reason to come back)",
            "- Cluster 2: lead with recognition or loyalty (they already shop, reward them)",
            "- Human and personal, not generic marketing speak",
            "",
            "Return ONLY a JSON array with no markdown:",
            '[{"tone":"Direct & Savings-led","message":"...","why":"one sentence why this works"},',
            '{"tone":"Relational & Loyalty","message":"...","why":"one sentence why this works"},',
            '{"tone":"Urgency & Scarcity","message":"...","why":"one sentence why this works"}]',
        ]
        prompt = "\n".join(prompt_parts)

        with st.spinner("Generating messages..."):
            reply, source = call_ai([{"role": "user", "content": prompt}], "", gemini_key, groq_key)

        if reply:
            try:
                clean = reply.replace("```json", "").replace("```", "").strip()
                msgs = json.loads(clean)
                TC = [
                    (NAVY, "#EEF3FF"),
                    (CORAL, "#FFF0F2"),
                    (GREEN, "#EDFAF4"),
                ]
                for i, msg in enumerate(msgs):
                    tc, bg = TC[i]
                    tone = msg.get("tone", "")
                    message = msg.get("message", "")
                    why = msg.get("why", "")
                    st.markdown(
                        "<div class='mc' style='border-color:" + tc + ";background:" + bg + ";'>"
                        "<div class='mt' style='background:" + tc + ";color:white;'>" + tone + "</div>"
                        "<div class='mm'>" + message + "</div>"
                        "<div class='mw'>Insight: " + why + "</div></div>",
                        unsafe_allow_html=True)
                st.markdown(
                    "<div style='background:white;border:1px solid #E0E4EF;border-radius:8px;padding:12px 16px;margin-top:12px;font-size:12px;'>"
                    "Send via: <strong>" + channel + "</strong> &nbsp;/&nbsp; "
                    "Best time: <strong>" + m["timing"] + "</strong> &nbsp;/&nbsp; "
                    "Generated by " + source + "</div>",
                    unsafe_allow_html=True)
            except Exception as e:
                st.error("Could not parse response. Raw output: " + str(reply)[:300])
        else:
            st.error("AI call failed. Check your key in the sidebar.")
