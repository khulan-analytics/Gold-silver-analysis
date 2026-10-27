import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from pathlib import Path

# Precious Metals Outlook | English / Italiano
st.set_page_config(page_title="Gold & Silver Outlook | Oro e Argento", page_icon="🥇", layout="wide")

DATA_DIR = Path("data_cache")
DATA_DIR.mkdir(exist_ok=True)

TEXT = {
    "English": {
        "title": "Gold & Silver Outlook",
        "subtitle": "5–10 year scenario analysis linked to current US interest rates",
        "language": "Language / Lingua",
        "about": "This dashboard combines recent futures prices, the 10-year real Treasury yield, and user-adjustable scenarios. It is a scenario tool, not a guaranteed prediction.",
        "market": "Market data",
        "gold": "Gold futures (USD/oz)",
        "silver": "Silver futures (USD/oz)",
        "real_yield": "10-year real Treasury yield",
        "fed_rate": "Effective federal funds rate",
        "settings": "Forecast assumptions",
        "horizon": "Forecast horizon (years)",
        "gold_growth": "Gold annual growth assumption (%)",
        "silver_growth": "Silver annual growth assumption (%)",
        "rate_sensitivity": "Annual growth adjustment per 1 percentage-point change in real yield (%)",
        "real_yield_help": "A higher real yield usually increases the opportunity cost of holding non-yielding metals. The relationship is not mechanical.",
        "forecast": "Forecast scenarios",
        "bear": "Bear case",
        "base": "Base case",
        "bull": "Bull case",
        "year": "Year",
        "price": "Illustrative price (USD/oz)",
        "history": "Historical prices",
        "forecast_chart": "Historical prices and scenario paths",
        "table": "Forecast table",
        "buy_sell": "When might buying or selling make sense?",
        "buy": "Potential buying conditions",
        "buy_text": "Consider staged purchases rather than trying to pick one exact bottom. More favorable conditions may include falling real yields, a weakening US dollar, easing inflation pressure, price stabilization after a correction, or a long-term allocation need. Confirm the thesis with your own risk tolerance.",
        "sell": "Potential selling / rebalancing conditions",
        "sell_text": "Consider trimming or rebalancing when your target allocation is exceeded, prices rise far above your planned valuation range, real yields and the dollar rise persistently, or your investment thesis changes. Predefine a target allocation and review rules rather than relying on a single price target.",
        "caution": "Important limitations",
        "caution_text": "Long-term metal prices are affected by real yields, the US dollar, inflation expectations, central-bank purchases, geopolitical risk, ETF flows, mining supply, and industrial demand. Silver is generally more volatile because it also has substantial industrial use. Forecasts are nominal USD per troy ounce, before fees, taxes, storage costs, or ETF tracking differences. Futures prices are not identical to spot prices.",
        "sources": "Data sources",
        "refresh": "Refresh market data",
        "refresh_help": "Attempts a fresh download; if it fails, the app uses cached CSV data when available.",
        "last_update": "Latest available observation",
        "source_note": "Prices use Yahoo Finance futures tickers GC=F and SI=F. Interest rates use FRED series DFII10 (10-year real Treasury yield) and DFF (effective federal funds rate).",
        "download": "Download forecast CSV",
        "no_data": "Could not retrieve live or cached data for",
        "data_warning": "Live data may be delayed, incomplete, or unavailable. Check the source before making decisions.",
        "method": "Methodology",
        "method_text": "The base path compounds the selected annual nominal growth assumption from the latest available futures price. Bear and bull paths use a 5 percentage-point annual growth adjustment around the base case. The real-yield sensitivity control adjusts the base growth assumption relative to the latest real yield versus a 2% reference yield. This is transparent scenario arithmetic—not a statistically validated 5–10 year forecast.",
        "growth_effect": "Rate-adjusted annual growth",
        "source_links": "Sources: Federal Reserve policy rate, FRED interest-rate data, Yahoo Finance historical futures data.",
    },
    "Italiano": {
        "title": "Prospettive per Oro e Argento",
        "subtitle": "Analisi di scenario a 5–10 anni collegata ai tassi d’interesse statunitensi attuali",
        "language": "Lingua / Language",
        "about": "Questa dashboard combina prezzi recenti dei futures, rendimento reale dei Treasury a 10 anni e scenari modificabili dall’utente. È uno strumento di scenario, non una previsione garantita.",
        "market": "Dati di mercato",
        "gold": "Futures sull’oro (USD/oncia)",
        "silver": "Futures sull’argento (USD/oncia)",
        "real_yield": "Rendimento reale Treasury a 10 anni",
        "fed_rate": "Tasso effettivo dei federal funds",
        "settings": "Ipotesi di previsione",
        "horizon": "Orizzonte di previsione (anni)",
        "gold_growth": "Ipotesi di crescita annua dell’oro (%)",
        "silver_growth": "Ipotesi di crescita annua dell’argento (%)",
        "rate_sensitivity": "Variazione della crescita annua per ogni punto percentuale di variazione del rendimento reale (%)",
        "real_yield_help": "Un rendimento reale più elevato di solito aumenta il costo opportunità di detenere metalli che non producono interessi. La relazione non è automatica.",
        "forecast": "Scenari di previsione",
        "bear": "Scenario ribassista",
        "base": "Scenario base",
        "bull": "Scenario rialzista",
        "year": "Anno",
        "price": "Prezzo indicativo (USD/oncia)",
        "history": "Prezzi storici",
        "forecast_chart": "Prezzi storici e percorsi di scenario",
        "table": "Tabella delle previsioni",
        "buy_sell": "Quando potrebbe avere senso comprare o vendere?",
        "buy": "Possibili condizioni favorevoli all’acquisto",
        "buy_text": "Valuta acquisti graduali invece di cercare di individuare un unico minimo. Condizioni potenzialmente favorevoli includono rendimenti reali in calo, dollaro più debole, minori pressioni inflazionistiche, stabilizzazione dei prezzi dopo una correzione o una necessità di allocazione a lungo termine. Verifica sempre la coerenza con la tua tolleranza al rischio.",
        "sell": "Possibili condizioni per vendere o riequilibrare",
        "sell_text": "Valuta una riduzione o un riequilibrio quando il peso dell’investimento supera il tuo obiettivo, i prezzi superano ampiamente la fascia di valutazione prevista, i rendimenti reali e il dollaro aumentano in modo persistente oppure cambia la tesi d’investimento. Definisci in anticipo allocazione obiettivo e regole di revisione, invece di affidarti a un solo prezzo obiettivo.",
        "caution": "Limiti importanti",
        "caution_text": "I prezzi dei metalli nel lungo periodo dipendono da rendimenti reali, dollaro USA, aspettative d’inflazione, acquisti delle banche centrali, rischi geopolitici, flussi degli ETF, offerta mineraria e domanda industriale. L’argento è generalmente più volatile perché ha anche un importante utilizzo industriale. Le previsioni sono espresse in USD nominali per oncia troy, al lordo di commissioni, imposte, costi di custodia e differenze di replica degli ETF. I futures non sono identici ai prezzi spot.",
        "sources": "Fonti dei dati",
        "refresh": "Aggiorna i dati di mercato",
        "refresh_help": "Tenta un nuovo download; in caso di errore utilizza i file CSV memorizzati, se disponibili.",
        "last_update": "Ultima osservazione disponibile",
        "source_note": "I prezzi provengono dai futures Yahoo Finance GC=F e SI=F. I tassi provengono da FRED: DFII10 (rendimento reale Treasury a 10 anni) e DFF (tasso effettivo federal funds).",
        "download": "Scarica la previsione CSV",
        "no_data": "Impossibile recuperare dati live o memorizzati per",
        "data_warning": "I dati live possono essere ritardati, incompleti o non disponibili. Verifica le fonti prima di prendere decisioni.",
        "method": "Metodologia",
        "method_text": "Il percorso base applica l’ipotesi di crescita nominale annua selezionata all’ultimo prezzo disponibile dei futures. Gli scenari ribassista e rialzista modificano la crescita annua di 5 punti percentuali rispetto allo scenario base. Il controllo di sensibilità ai rendimenti reali modifica la crescita base rispetto all’ultimo rendimento reale e a un riferimento del 2%. È un calcolo trasparente di scenario, non una previsione a 5–10 anni convalidata statisticamente.",
        "growth_effect": "Crescita annua corretta per il tasso",
        "source_links": "Fonti: Federal Reserve, dati sui tassi FRED e prezzi storici futures Yahoo Finance.",
    },
}

lang = st.sidebar.selectbox("Language / Lingua", ["English", "Italiano"])
T = TEXT[lang]

st.title(T["title"])
st.caption(T["subtitle"])
st.info(T["about"])

with st.sidebar:
    st.header(T["settings"])
    years = st.select_slider(T["horizon"], options=[5, 10], value=10)
    gold_growth_input = st.slider(T["gold_growth"], min_value=-10.0, max_value=20.0, value=4.0, step=0.5)
    silver_growth_input = st.slider(T["silver_growth"], min_value=-15.0, max_value=25.0, value=5.0, step=0.5)
    rate_sensitivity = st.slider(T["rate_sensitivity"], min_value=-5.0, max_value=5.0, value=-1.0, step=0.25, help=T["real_yield_help"])
    refresh = st.button(T["refresh"], help=T["refresh_help"])

def download_yahoo(ticker, filename, period="10y"):
    path = DATA_DIR / filename
    if not refresh and path.exists():
        try:
            cached = pd.read_csv(path, index_col=0, parse_dates=True)
            if not cached.empty and "Close" in cached.columns:
                return cached, "cache"
        except Exception:
            pass
    try:
        data = yf.download(ticker, period=period, auto_adjust=False, progress=False, threads=False)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        if not data.empty and "Close" in data.columns:
            data = data[["Close"]].dropna()
            data.to_csv(path)
            return data, "live"
    except Exception:
        pass
    if path.exists():
        try:
            cached = pd.read_csv(path, index_col=0, parse_dates=True)
            if not cached.empty and "Close" in cached.columns:
                return cached, "cache"
        except Exception:
            pass
    return pd.DataFrame(), "unavailable"

def download_fred(series_id, filename):
    path = DATA_DIR / filename
    try:
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
        df = pd.read_csv(url)
        if len(df.columns) >= 2:
            df.columns = ["DATE", series_id]
            df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")
            df[series_id] = pd.to_numeric(df[series_id], errors="coerce")
            df = df.set_index("DATE").dropna()
            if not df.empty:
                df.to_csv(path)
                return df, "live"
    except Exception:
        pass
    if path.exists():
        try:
            df = pd.read_csv(path, index_col=0, parse_dates=True)
            df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors="coerce")
            df = df.dropna()
            if not df.empty:
                return df, "cache"
        except Exception:
            pass
    return pd.DataFrame(), "unavailable"

gold, gold_source = download_yahoo("GC=F", "gold_futures.csv")
silver, silver_source = download_yahoo("SI=F", "silver_futures.csv")
real_yield_df, real_source = download_fred("DFII10", "real_yield_dfii10.csv")
fed_rate_df, fed_source = download_fred("DFF", "effective_fed_funds_dff.csv")

if gold.empty or silver.empty:
    st.error(f"{T['no_data']} gold or silver. " + T["data_warning"])
    st.stop()

gold_close = gold["Close"].dropna()
silver_close = silver["Close"].dropna()
gold_now = float(gold_close.iloc[-1])
silver_now = float(silver_close.iloc[-1])
real_yield = float(real_yield_df.iloc[:, 0].dropna().iloc[-1]) if not real_yield_df.empty else 2.0
fed_rate = float(fed_rate_df.iloc[:, 0].dropna().iloc[-1]) if not fed_rate_df.empty else np.nan
real_date = real_yield_df.index[-1].date().isoformat() if not real_yield_df.empty else "N/A"
fed_date = fed_rate_df.index[-1].date().isoformat() if not fed_rate_df.empty else "N/A"

# The rate adjustment is relative to a 2% real-yield reference. Higher real yields
# reduce assumed growth when the sensitivity is negative. It is a scenario input,
# not a causal estimate or a trained forecasting model.
rate_adjustment = rate_sensitivity * (real_yield - 2.0)
gold_growth = gold_growth_input + rate_adjustment
silver_growth = silver_growth_input + rate_adjustment

st.subheader(T["market"])
m1, m2, m3, m4 = st.columns(4)
m1.metric(T["gold"], f"${gold_now:,.2f}")
m2.metric(T["silver"], f"${silver_now:,.2f}")
m3.metric(T["real_yield"], f"{real_yield:.2f}%", help=f"Latest observation: {real_date}")
m4.metric(T["fed_rate"], f"{fed_rate:.2f}%" if np.isfinite(fed_rate) else "N/A", help=f"Latest observation: {fed_date}")
st.caption(T["source_note"])
st.warning(T["data_warning"])

def build_scenarios(metal, current, growth, n_years):
    rows = []
    for year in range(1, n_years + 1):
        rows.append({
            T["year"]: datetime.now().year + year,
            "Metal": metal,
            T["bear"]: current * (1 + (growth - 5.0) / 100) ** year,
            T["base"]: current * (1 + growth / 100) ** year,
            T["bull"]: current * (1 + (growth + 5.0) / 100) ** year,
        })
    return pd.DataFrame(rows)

gold_forecast = build_scenarios("Gold", gold_now, gold_growth, years)
silver_forecast = build_scenarios("Silver", silver_now, silver_growth, years)

c1, c2 = st.columns(2)
with c1:
    st.subheader("Gold")
    st.metric(T["growth_effect"], f"{gold_growth:.2f}%")
    st.metric(f"{years}-year {T['base'].lower()}", f"${gold_forecast[T['base']].iloc[-1]:,.0f}/oz",
              delta=f"{(gold_forecast[T['base']].iloc[-1] / gold_now - 1) * 100:+.1f}%")
with c2:
    st.subheader("Silver")
    st.metric(T["growth_effect"], f"{silver_growth:.2f}%")
    st.metric(f"{years}-year {T['base'].lower()}", f"${silver_forecast[T['base']].iloc[-1]:,.0f}/oz",
              delta=f"{(silver_forecast[T['base']].iloc[-1] / silver_now - 1) * 100:+.1f}%")

st.subheader(T["forecast_chart"])
fig = make_subplots(rows=1, cols=2, subplot_titles=("Gold (USD/oz)", "Silver (USD/oz)"))
for df, history, col in [(gold_forecast, gold_close, 1), (silver_forecast, silver_close, 2)]:
    hist = history.tail(5 * 252)
    fig.add_trace(go.Scatter(x=hist.index, y=hist.values, name=f"{df['Metal'].iloc[0]} history", mode="lines"), row=1, col=col)
    last_date = hist.index[-1]
    future_dates = [last_date] + [pd.Timestamp(datetime.now().year + i, 12, 31) for i in range(1, years + 1)]
    start_value = float(hist.iloc[-1])
    for scenario in [T["bear"], T["base"], T["bull"]]:
        vals = [start_value] + df[scenario].tolist()
        fig.add_trace(go.Scatter(x=future_dates, y=vals, name=f"{df['Metal'].iloc[0]} - {scenario}",
                                 mode="lines", line=dict(dash="solid" if scenario == T["base"] else "dash"),
                                 showlegend=True), row=1, col=col)
fig.update_layout(height=520, hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
fig.update_yaxes(title_text="USD per troy ounce")
st.plotly_chart(fig, use_container_width=True)

st.subheader(T["table"])
rows = []
for metal, current, df in [("Gold", gold_now, gold_forecast), ("Silver", silver_now, silver_forecast)]:
    for _, r in df.iterrows():
        rows.append({
            "Metal": metal,
            T["year"]: int(r[T["year"]]),
            "Current price (USD/oz)": current,
            T["bear"]: r[T["bear"]],
            T["base"]: r[T["base"]],
            T["bull"]: r[T["bull"]],
        })
forecast_table = pd.DataFrame(rows)
st.dataframe(
    forecast_table.style.format({
        "Current price (USD/oz)": "${:,.2f}",
        T["bear"]: "${:,.2f}",
        T["base"]: "${:,.2f}",
        T["bull"]: "${:,.2f}",
    }),
    use_container_width=True,
    hide_index=True
)
st.download_button(T["download"], forecast_table.to_csv(index=False).encode("utf-8"),
                   file_name="gold_silver_forecast.csv", mime="text/csv")

with st.expander(T["method"]):
    st.write(T["method_text"])
    st.write(f"{T['real_yield']}: {real_yield:.2f}% (observation date: {real_date})")
    st.write(f"{T['fed_rate']}: {fed_rate:.2f}% (observation date: {fed_date})" if np.isfinite(fed_rate) else f"{T['fed_rate']}: N/A")
    st.write(T["source_links"])

st.subheader(T["buy_sell"])
b1, b2 = st.columns(2)
with b1:
    st.markdown(f"**{T['buy']}**")
    st.write(T["buy_text"])
with b2:
    st.markdown(f"**{T['sell']}**")
    st.write(T["sell_text"])

st.subheader(T["caution"])
st.write(T["caution_text"])
st.caption("Built for educational and analytical purposes. Not personalized financial advice.")
