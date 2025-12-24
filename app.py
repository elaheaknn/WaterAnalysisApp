import pandas as pd
import matplotlib.pyplot as plt
import ternary
import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_title="Water Analysis Ternary Diamond")

# ===== خواندن داده‌ها =====
file_path = r"F:\عرب\پایپر.xlsx"
df = pd.read_excel(file_path)

# ===== اسلایسرها =====
mahal = st.sidebar.selectbox("Select Station", df['mahal'].unique())
name_sh = st.sidebar.selectbox("Select City", df['Name_Sh'].unique())
year_month = st.sidebar.selectbox("Select Date", df['Year_month'].unique())

# ===== فیلتر کردن داده‌ها =====
df_filtered = df[(df['mahal'] == mahal) &
                 (df['Name_Sh'] == name_sh) &
                 (df['Year_month'] == year_month)].copy()

sample_name = f"{mahal} | {name_sh} | {year_month}"

# ===== محاسبات درصد =====
cations = ['ca', 'mg', 'na', 'k']
anions  = ['cl', 'so4', 'hco3', 'co3']

df_filtered['Parameter'] = df_filtered['Parameter'].str.lower().str.strip()

df_c = df_filtered[df_filtered['Parameter'].isin(cations)].copy()
df_a = df_filtered[df_filtered['Parameter'].isin(anions)].copy()

total_cations = df_c['Value'].sum()
total_anions  = df_a['Value'].sum()

if total_cations == 0:
    ca = mg = na_k = 0
else:
    df_c['pct'] = df_c['Value'] / total_cations * 100
    ca   = round(df_c[df_c['Parameter'] == 'ca']['pct'].sum(), 1) if not df_c[df_c['Parameter'] == 'ca'].empty else 0
    mg   = round(df_c[df_c['Parameter'] == 'mg']['pct'].sum(), 1) if not df_c[df_c['Parameter'] == 'mg'].empty else 0
    na_k = round(100 - ca - mg, 1)

if total_anions == 0:
    cl = so4 = hco3_co3 = 0
else:
    df_a['pct'] = df_a['Value'] / total_anions * 100
    cl       = round(df_a[df_a['Parameter'] == 'cl']['pct'].sum(), 1) if not df_a[df_a['Parameter'] == 'cl'].empty else 0
    so4      = round(df_a[df_a['Parameter'] == 'so4']['pct'].sum(), 1) if not df_a[df_a['Parameter'] == 'so4'].empty else 0
    hco3_co3 = round(100 - cl - so4, 1)

# ===== تابع offset =====
def smart_offset(x, y, maxshift=12):
    dx = 0
    dy = 8 if y < 50 else -8
    return dx, dy

# ===== رسم نمودار =====
fig = plt.figure(figsize=(16, 12), facecolor='none')

# مثلث کاتیون
ax_cat = fig.add_axes([0.05, 0.05, 0.38, 0.65])
tax1 = ternary.TernaryAxesSubplot(ax=ax_cat, scale=100)
tax1.gridlines(color="black", multiple=10, linewidth=0.7)

ax_cat.text(0.5, 1.05, "Cation", ha='center', va='bottom', fontsize=16, fontweight='bold', color='#004C99', transform=ax_cat.transAxes)

tax1.left_axis_label("Ca²⁺ (%)", fontsize=13, offset=0.14, fontweight='bold')
tax1.right_axis_label("Mg²⁺ (%)", fontsize=13, offset=0.14, fontweight='bold')
tax1.bottom_axis_label("Na⁺ + K⁺ (%)", fontsize=13, offset=0.12, fontweight='bold')

tax1.scatter([[ca, mg, na_k]], marker='o', color='#004C99', s=300, edgecolor='black', linewidth=2.5, zorder=5)

dx, dy = smart_offset(ca, mg)
tax1.ax.text(ca, mg + dy,
             f"Ca: {ca}%\nMg: {mg}%\nNa+K: {na_k}%",
             ha='center', va='bottom', fontsize=11.5, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.55", facecolor="#d0e8ff", alpha=0.97, edgecolor="#004C99", linewidth=2.3), zorder=10)

tax1.clear_matplotlib_ticks()
ax_cat.axis('off')

# مثلث آنیون
ax_an = fig.add_axes([0.57, 0.05, 0.38, 0.65])
tax2 = ternary.TernaryAxesSubplot(ax=ax_an, scale=100)
tax2.gridlines(color="black", multiple=10, linewidth=0.7)

ax_an.text(0.5, 1.05, "Anion", ha='center', va='bottom', fontsize=16, fontweight='bold', color='#990000', transform=ax_an.transAxes)

tax2.left_axis_label("Cl⁻ (%)", fontsize=13, offset=0.14, fontweight='bold')
tax2.right_axis_label("SO₄²⁻ (%)", fontsize=13, offset=0.14, fontweight='bold')
tax2.bottom_axis_label("HCO₃⁻ + CO₃²⁻ (%)", fontsize=13, offset=0.12, fontweight='bold')

tax2.scatter([[cl, so4, hco3_co3]], marker='o', color='#990000', s=300, edgecolor='black', linewidth=2.5, zorder=5)

dx, dy = smart_offset(cl, so4)
tax2.ax.text(cl, so4 + dy,
             f"Cl: {cl}%\nSO4: {so4}%\nHCO3+CO3: {hco3_co3}%",
             ha='center', va='bottom', fontsize=11.5, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.55", facecolor="#ffecb3", alpha=0.97, edgecolor="#990000", linewidth=2.3), zorder=10)

tax2.clear_matplotlib_ticks()
ax_an.axis('off')

# الماس وسط
ax_d = fig.add_axes([0.25, 0.32, 0.5, 0.55])
cx, cy = 0.5, 0.5
w, h = 3, 6

left   = (cx - w/2, cy)
top    = (cx, cy + h/2)
right  = (cx + w/2, cy)
bottom = (cx, cy - h/2)

ax_d.plot([left[0], top[0], right[0], bottom[0], left[0]],
          [left[1], top[1], right[1], bottom[1], left[1]], color='black', linewidth=2.8)

for i in range(1, 5):
    t = i / 5.0
    ax_d.plot([left[0] + t*(top[0]-left[0]), bottom[0] + t*(right[0]-bottom[0])],
              [left[1] + t*(top[1]-left[1]), bottom[1] + t*(right[1]-bottom[1])],
              color='lightgray', lw=0.9)
    ax_d.plot([bottom[0] + t*(left[0]-bottom[0]), right[0] + t*(top[0]-right[0])],
              [bottom[1] + t*(left[1]-bottom[1]), right[1] + t*(top[1]-right[1])],
              color='lightgray', lw=0.9)

ax_d.text(cx, cy + h/2 + 0.08, "Mg²⁺ + SO4²⁻", ha='center', va='bottom', fontsize=13, fontweight='bold')
ax_d.text(cx + w/2 + 0.14, cy, "Ca²⁺ + Cl⁻", ha='left', va='center', fontsize=13, fontweight='bold', rotation=-90)
ax_d.text(cx, cy - h/2 - 0.08, "Na⁺ + K⁺ + HCO3⁻ + CO3²⁻", ha='center', va='top', fontsize=13, fontweight='bold')
ax_d.text(cx - w/2 - 0.14, cy, "Ca²⁺ + HCO3⁻ + CO3²⁻", ha='right', va='center', fontsize=13, fontweight='bold', rotation=90)

ax_d.scatter(ca + 0.5*na_k / 100, mg + 0.5*na_k / 100, color='#2ca02c', s=450, edgecolor='black', linewidth=3.5, zorder=10)

ax_d.text(cx, cy + 0.15,
          f"{sample_name}\nCa: {ca}% | Mg: {mg}% | Na+K: {na_k}%\nCl: {cl}% | SO4: {so4}% | HCO3+CO3: {hco3_co3}%",
          ha='center', va='bottom', fontsize=12, fontweight='bold',
          bbox=dict(boxstyle="round,pad=0.9", facecolor="#ccffcc", alpha=0.96, edgecolor="darkgreen", linewidth=2.8))

ax_d.set_xlim(cx - w/2 - 0.25, cx + w/2 + 0.25)
ax_d.set_ylim(cy - h/2 - 0.25, cy + h/2 + 0.25)
ax_d.set_aspect('equal')
ax_d.axis('off')

plt.tight_layout()
fig.patch.set_alpha(0)
for ax in fig.get_axes():
    ax.set_facecolor("none")

# ===== نمایش در Streamlit =====
st.pyplot(fig)
