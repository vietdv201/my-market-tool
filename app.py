import streamlit as st
import streamlit.components.v1 as components

# --- CẤU HÌNH TRANG ---
st.set_page_config(layout="wide", page_title="Market Monitor Pro")

# --- DANH SÁCH MÃ (Đã phân loại & Sắp xếp theo Vốn hóa/Volume) ---

# 1. METALS (Nguồn: ICE Data Services)
metals = [
    "FX_IDC:XAUUSD", # Gold
    "FX_IDC:XAGUSD"  # Silver
]

# 2. INDICES (Nguồn: Global/Forexcom - Để tối ưu dữ liệu miễn phí)
# Sắp xếp theo độ lớn thị trường: Mỹ -> Âu -> Á
indices = [
    "FOREXCOM:SPX500",  # S&P 500 (Mỹ)
    "FOREXCOM:NSXUSD",  # Nasdaq 100 (Mỹ)
    "FOREXCOM:DJI",     # Dow Jones 30 (Mỹ)
    "FOREXCOM:RUSS2000",# Russell 2000 (Mỹ)
    "BLACKBULL:JP225",  # Nikkei 225 (Nhật)
    "FOREXCOM:GRXEUR",  # DAX 40 (Đức)
    "FOREXCOM:UKXGBP",  # FTSE 100 (Anh)
    "FOREXCOM:FRXEUR",  # CAC 40 (Pháp)
    "FOREXCOM:EUXEUR",  # STOXX 50 (Châu Âu)
    "FOREXCOM:AUXAUD",  # ASX 200 (Úc)
    "FOREXCOM:ESXEUR",  # IBEX 35 (Tây Ban Nha)
    "FOREXCOM:NEXEUR",  # AEX 25 (Hà Lan)
    "FOREXCOM:SMXCHF",  # SMI 20 (Thụy Sĩ)
]

# 3. CRYPTO (Nguồn: BITFINEX)
# Sắp xếp theo Vốn hóa thị trường (Market Cap)
crypto = [
    "BITFINEX:BTCUSD",  # Bitcoin
    "BITFINEX:ETHUSD",  # Ethereum
    "BITFINEX:BNBUSD",  # Binance Coin
    "BITFINEX:SOLUSD",  # Solana
    "BITFINEX:XRPUSD",  # Ripple
    "BITFINEX:ADAUSD",  # Cardano
    "BITFINEX:DOGEUSD", # Dogecoin
    "BITFINEX:DOTUSD",  # Polkadot
    "BITFINEX:LTCUSD",  # Litecoin
    "BITFINEX:BCHUSD",  # Bitcoin Cash
    "BITFINEX:LINKUSD", # Chainlink (LNK)
    "BITFINEX:XLMUSD",  # Stellar
    "BITFINEX:XTZUSD",  # Tezos
    "BITFINEX:MKRUSD",  # Maker
    # "BITFINEX:NERUSD" # (Lưu ý: Near Protocol trên Bitfinex mã thường là NEAR hoặc coin khác, đã ẩn tạm nếu không tìm thấy dữ liệu chuẩn)
]

# 4. FOREX (Nguồn: ICE Data Services - FX_IDC)
# Nhóm 1: Các cặp tiền chính (Majors) & USD
fx_majors = [
    "FX_IDC:EURUSD", "FX_IDC:USDJPY", "FX_IDC:GBPUSD", 
    "FX_IDC:AUDUSD", "FX_IDC:USDCAD", "FX_IDC:USDCHF", "FX_IDC:NZDUSD"
]

# Nhóm 2: Các cặp chéo (Crosses - EUR, GBP, AUD, JPY)
fx_crosses = [
    "FX_IDC:EURGBP", "FX_IDC:EURJPY", "FX_IDC:EURCHF", "FX_IDC:EURAUD", "FX_IDC:EURCAD", "FX_IDC:EURNZD",
    "FX_IDC:GBPJPY", "FX_IDC:GBPCHF", "FX_IDC:GBPAUD", "FX_IDC:GBPCAD", "FX_IDC:GBPNZD",
    "FX_IDC:AUDJPY", "FX_IDC:AUDCAD", "FX_IDC:AUDCHF", "FX_IDC:AUDNZD",
    "FX_IDC:CADJPY", "FX_IDC:CADCHF", 
    "FX_IDC:CHFJPY",
    "FX_IDC:NZDJPY", "FX_IDC:NZDCAD", "FX_IDC:NZDCHF"
]

# Nhóm 3: Tiền tệ Châu Á & Mới nổi (Exotics)
fx_exotics = [
    "FX_IDC:USDCNH", # Yuan Trung Quốc
    "FX_IDC:USDSGD", # Singapore Dollar
    "FX_IDC:EURHKD", # Euro vs Hong Kong
    "FX_IDC:EURSGD", # Euro vs Singapore
    "FX_IDC:GBPSGD", # Bảng Anh vs Singapore
    "FX_IDC:USDMXN", # Peso Mexico
    "FX_IDC:USDZAR", # Rand Nam Phi
    "FX_IDC:USDSEK", # Thụy Điển
    "FX_IDC:USDNOK", # Na Uy
]

# Gộp tất cả lại thành một danh sách tổng để hiển thị
all_symbols = {
    "--- KIM LOẠI QUÝ (METALS) ---": metals,
    "--- CHỈ SỐ (INDICES) ---": indices,
    "--- TIỀN ĐIỆN TỬ (CRYPTO) ---": crypto,
    "--- FOREX (CHÍNH) ---": fx_majors,
    "--- FOREX (CHÉO) ---": fx_crosses,
    "--- FOREX (KHÁC) ---": fx_exotics
}

# --- SIDEBAR (THANH BÊN) ---
st.sidebar.title("🔍 Bộ Lọc")

# Tạo Menu chọn nhóm
selected_group = st.sidebar.radio("Chọn Nhóm:", list(all_symbols.keys()))

# Lấy danh sách mã tương ứng với nhóm đã chọn
current_list = all_symbols[selected_group]

st.sidebar.markdown("---")
# Dropdown chọn mã cụ thể
selected_symbol = st.sidebar.selectbox(f"Chọn Mã ({len(current_list)} mã):", current_list)

# --- PHẦN HIỂN THỊ CHÍNH ---
col1, col2 = st.columns([8, 2]) 

with col1:
    # Hiển thị tên mã to đẹp
    st.title(f"{selected_symbol.split(':')[1]}") 
    st.caption(f"Nguồn dữ liệu: {selected_symbol.split(':')[0]}")

with col2:
    st.write("") 
    st.write("") 
    # Link mở sang TradingView để lưu phân tích
    tv_url = f"https://www.tradingview.com/chart/?symbol={selected_symbol}"
    st.link_button("👉 Mở TradingView (Lưu vẽ)", tv_url)

# --- WIDGET TRADINGVIEW ---
tv_widget_code = f"""
<div class="tradingview-widget-container" style="height:100%;width:100%">
  <div id="tradingview_chart" style="height:850px;width:100%"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget(
  {{
  "autosize": true,
  "symbol": "{selected_symbol}",
  "interval": "D",
  "timezone": "Asia/Ho_Chi_Minh",
  "theme": "dark",
  "style": "1",
  "locale": "vi_VN",
  "toolbar_bg": "#f1f3f6",
  "enable_publishing": false,
  "hide_top_toolbar": false,
  "hide_legend": false,
  "save_image": true,
  "container_id": "tradingview_chart",
  "studies": [
    "RSI@tv-basicstudies",
    "MASimple@tv-basicstudies" 
  ],
  "show_popup_button": true,
  "popup_width": "1000",
  "popup_height": "650"
  }}
  );
  </script>
</div>
"""

components.html(tv_widget_code, height=850)