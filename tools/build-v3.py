#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build-v3.py — dựng prototype-v3 từ mockup đã giải nén của khách hàng.

Nguyên tắc: KHÔNG chép tay một dòng markup nào. Script cắt nguyên xi từng khối
màn hình ra khỏi `_raw/template.html` (theo số dòng + khớp thẻ <sc-if>), giữ
nguyên runtime của KH, rồi chỉ làm 3 việc:

  1. Đổi GIÁ TRỊ màu (bảng COLORS bên dưới) — không đụng layout, font, spacing.
  2. Thay chữ "Homi365 ●" ở thanh trên bằng logo chính thức.
  3. Cắt thành mỗi màn một file .html, nối với nhau bằng link thật.

Chạy:
    cd D:\\BA\\ProjectBA\\Medigo
    python prototype-v3\\tools\\build-v3.py

Cần chạy `extract-bundle.py` trước. Không cần thư viện ngoài.
"""

import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # prototype-v3/tools
V3 = HERE.parent                                 # prototype-v3
RAW = HERE / "_raw"
SRC = RAW / "template.html"

# ============================================================================
# 1. BẢNG MÀU — chỗ duy nhất cần sửa khi KH đổi ý về màu
# ============================================================================
# Thứ tự QUAN TRỌNG: chuỗi cụ thể phải đứng trước chuỗi tổng quát.

COLORS = [
    # --- Thương hiệu: cyan #00ADEE -> navy #1E3A66 -----------------------
    ("#00ADEE", "#1E3A66"),
    ("#00adee", "#1E3A66"),
    ("#0099d1", "#1B3358"),                       # hover
    ("#0088ba", "#122544"),                       # active
    ("#00728f", "#0F7F96"),                       # chữ badge "Đã duyệt"
    ("rgba(0,173,238,.14)", "rgba(15,127,150,.14)"),   # nền badge -> teal
    ("rgba(0,173,238,", "rgba(30,58,102,"),            # còn lại -> navy
    # --- Nút "Thanh toán" trong mockup KH đang là đỏ #EE0000 nhưng hover
    #     lại là cyan — gần như chắc chắn là lỗi. Đưa về màu chính. -------
    ("#EE0000", "#1E3A66"),
    # --- Xanh lá: thành công --------------------------------------------
    ("#84BE52", "#2F7A48"),
    ("#4c7a2e", "#2F7A48"),
    ("#73aa45", "#2F7A48"),
    ("rgba(132,190,82,", "rgba(47,122,72,"),
    # --- Cam: cảnh báo ---------------------------------------------------
    ("#FFA500", "#965C0A"),
    ("#FBAE40", "#965C0A"),
    ("#FFBC40", "#E0B15F"),
    ("#a36400", "#965C0A"),
    ("rgba(255,165,0,", "rgba(150,92,10,"),
    # --- Đỏ: lỗi ---------------------------------------------------------
    ("#D9342B", "#C0392B"),
    ("#E20707", "#C0392B"),
    ("rgba(217,52,43,", "rgba(192,57,43,"),
    ("rgba(226,7,7,", "rgba(192,57,43,"),
    # --- Xám -------------------------------------------------------------
    ("#1F1F1F", "#2B303A"),
    ("#424242", "#5B6472"),
    ("#414445", "#5B6472"),
    ("#939393", "#8A93A3"),
    ("#AAAAAA", "#C9CED4"),
    ("#5c5c5c", "#5B6472"),
    ("rgba(31,31,31,", "rgba(43,48,58,"),
    ("rgba(170,170,170,", "rgba(154,163,176,"),
    ("rgba(204,204,204,.9)", "rgba(18,37,68,.16)"),     # đổ bóng
    # --- Navy sẵn có trong mockup (sidebar admin) ------------------------
    ("#344557", "#1B3358"),
    ("#2a3745", "#122544"),
    ("rgba(52,69,87,", "rgba(27,51,88,"),
]

# Màu KHÔNG được đổi — logo bên thứ ba trong màn thanh toán.
# Nền trang đổi sang warm-50 của HOMI365, thẻ/card giữ trắng -> section xen kẽ
# ấm / trắng như prototype-v2. Áp TRƯỚC bảng COLORS để giá trị var() không bị
# bảng màu đụng vào.
WARM = "#FAF8F3"
CHART = "#1BA3BE"     # teal-500 — màu cột biểu đồ, tách khỏi navy của nút/link

BG_PATCHES = [
    # (2 mục chèn màn B5/B6 được nối thêm ở cuối file, sau khi markup của
    #  chúng đã được khai báo — xem "BG_PATCHES += [...]" bên dưới.)
    # 7.5.2 — cây tuyến 3 cấp (mockup chỉ vẽ F0 → F1) + khối lịch sử hạng.
    ("      tree:[{name:'Lê Văn Cường', orders:4},{name:'Phạm Thị Dung', orders:1}] },",
     "      tree:[{name:'Lê Văn Cường', orders:4, children:[{name:'Ngô Thị Em', orders:2},"
     "{name:'Đỗ Anh Tuấn', orders:9}]},{name:'Phạm Thị Dung', orders:1, children:[]}] },"),
    ("      tree:[{name:'Ngô Thị Em', orders:2}] },",
     "      tree:[{name:'Ngô Thị Em', orders:2, children:[{name:'Vũ Minh Khang', orders:5}]}] },"),
    ("""              <div style="font-size:13px;padding:var(--s3) var(--s5);margin-left:var(--s8);border-left:2px solid rgba(170,170,170,.35);color:var(--c2)">{{t.name}} — F1 · {{t.orders}} đơn</div>""",
     """              <div style="font-size:13px;padding:var(--s3) var(--s5);margin-left:var(--s8);border-left:2px solid rgba(170,170,170,.35);color:var(--c2)">{{t.name}} — F1 · {{t.orders}} đơn</div>
              <sc-for list="{{t.children}}" as="g" hint-placeholder-count="2">
                <div style="font-size:13px;padding:var(--s3) var(--s5);margin-left:var(--s10);border-left:2px solid rgba(170,170,170,.25);color:var(--c5)">{{g.name}} — F2 · {{g.orders}} đơn</div>
              </sc-for>"""),
    ("""          <div style="font-size:12px;font-weight:700;color:var(--c5);text-transform:uppercase;letter-spacing:.03em;margin-bottom:var(--s5)">Lịch sử đơn hàng &amp; hoa hồng</div>""",
     """          <div style="font-size:12px;font-weight:700;color:var(--c5);text-transform:uppercase;letter-spacing:.03em;margin-bottom:var(--s5)">Lịch sử thăng/giáng hạng</div>
          <div style="display:flex;flex-direction:column;gap:var(--s3);font-size:13px;margin-bottom:var(--s7)">
            <sc-for list="{{selectedMember.rankHistory}}" as="rh" hint-placeholder-count="2">
              <div style="display:flex;justify-content:space-between;gap:var(--s5);color:var(--c2)"><span>{{rh.label}}</span><span style="color:var(--c5);flex:none">{{rh.time}}</span></div>
            </sc-for>
          </div>
          <div style="font-size:12px;font-weight:700;color:var(--c5);text-transform:uppercase;letter-spacing:.03em;margin-bottom:var(--s5)">Lịch sử đơn hàng &amp; hoa hồng</div>"""),

    # 7.1.3 — gợi ý cho khách đã mua hàng nhưng chưa là thành viên.
    ("""            <button sc-camel-on-click="{{agentLoginSubmit}}" style="height:46px;background:var(--c6);color:var(--c12);border:none;border-radius:var(--r-md);font-size:16px;font-weight:600;box-shadow:var(--sh)" style-hover="background:#0099d1">Đăng nhập</button>""",
     """            <button sc-camel-on-click="{{agentLoginSubmit}}" style="height:46px;background:var(--c6);color:var(--c12);border:none;border-radius:var(--r-md);font-size:16px;font-weight:600;box-shadow:var(--sh)" style-hover="background:#0099d1">Đăng nhập</button>
            <div style="font-size:12px;color:var(--c5);background:rgba(170,170,170,.08);border-radius:var(--r-sm);padding:var(--s4);line-height:1.6">Đã mua hàng nhưng chưa đăng ký thành viên? Nhập số điện thoại đã mua rồi bấm Đăng nhập — hệ thống sẽ đưa bạn sang màn đăng ký và điền sẵn thông tin từ đơn cũ.</div>"""),

    # A2 bước 5: mockup chỉ đưa link giới thiệu. Thêm link mua hàng cá nhân
    # ngay bên dưới để agent nhận đủ 2 link ngay lúc kích hoạt (8.1.C-4).
    ('<button sc-camel-on-click="{{copyLink}}" style="height:44px;background:var(--c6);'
     'color:var(--c12);border:none;border-radius:var(--r-md);font-size:15px;'
     'font-weight:600" style-hover="background:#0099d1">{{copyLabel}}</button>',
     '<button sc-camel-on-click="{{copyLink}}" style="height:44px;background:var(--c6);'
     'color:var(--c12);border:none;border-radius:var(--r-md);font-size:15px;'
     'font-weight:600" style-hover="background:#0099d1">{{copyLabel}}</button>\n'
     '            <div style="height:1px;background:rgba(170,170,170,.25)"></div>\n'
     '            <div style="font-size:12px;color:var(--c5);text-transform:uppercase;'
     'letter-spacing:.04em">Link mua hàng cá nhân</div>\n'
     '            <div style="font-size:13px;color:var(--c4);word-break:break-all;'
     'background:rgba(170,170,170,.08);border-radius:var(--r-sm);padding:var(--s4)">'
     '{{personalLink}}</div>\n'
     '            <button sc-camel-on-click="{{copyPersonalLink}}" style="height:44px;'
     'background:var(--c12);color:var(--c6);border:1px solid var(--c6);'
     'border-radius:var(--r-md);font-size:15px;font-weight:600" '
     'style-hover="background:rgba(0,173,238,.06)">{{copyPersonalLabel}}</button>'),
    # A3 thiếu hẳn link bán hàng — agent rời màn "kích hoạt thành công" là mất
    # đường lấy link. Chèn một thẻ link + nút copy ngay dưới phần chào.
    # copyLink / copyLabel đã có sẵn trong renderVals nên dùng lại được.
    ("""{{agentStageToggleLabel}}</button>
      </div>
""",
     """{{agentStageToggleLabel}}</button>
      </div>

      <div style="background:var(--c12);border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);padding:var(--s7);display:flex;flex-direction:column;gap:var(--s6)">
        <div style="font-size:12px;color:var(--c5);text-transform:uppercase;letter-spacing:.04em">Link bán hàng của bạn</div>

        <div style="display:flex;flex-direction:column;gap:var(--s3)">
          <div style="font-size:12px;font-weight:600;color:var(--c2)">Link giới thiệu · mã {{refCode}}</div>
          <div style="display:flex;gap:var(--s3);align-items:center">
            <div style="flex:1;min-width:0;font-size:13px;color:var(--c4);word-break:break-all;background:rgba(170,170,170,.08);border-radius:var(--r-sm);padding:var(--s4)">{{refLink}}</div>
            <button sc-camel-on-click="{{copyLink}}" style="flex:none;height:40px;padding:0 var(--s6);background:var(--c6);color:var(--c12);border:none;border-radius:var(--r-md);font-size:14px;font-weight:600" style-hover="background:#0099d1">{{copyLabel}}</button>
          </div>
        </div>

        <div style="display:flex;flex-direction:column;gap:var(--s3)">
          <div style="font-size:12px;font-weight:600;color:var(--c2)">Link mua hàng cá nhân</div>
          <div style="display:flex;gap:var(--s3);align-items:center">
            <div style="flex:1;min-width:0;font-size:13px;color:var(--c4);word-break:break-all;background:rgba(170,170,170,.08);border-radius:var(--r-sm);padding:var(--s4)">{{personalLink}}</div>
            <button sc-camel-on-click="{{copyPersonalLink}}" style="flex:none;height:40px;padding:0 var(--s6);background:var(--c12);color:var(--c6);border:1px solid var(--c6);border-radius:var(--r-md);font-size:14px;font-weight:600" style-hover="background:rgba(0,173,238,.06)">{{copyPersonalLabel}}</button>
          </div>
        </div>
      </div>

      <div style="display:flex;gap:var(--s2);flex-wrap:wrap;align-items:center">
        <span style="font-size:12px;color:var(--c5);margin-right:var(--s2)">Số đơn theo</span>
        <sc-for list="{{orderRanges}}" as="r" hint-placeholder-count="4">
          <button sc-camel-on-click="{{r.onClick}}" style="{{r.style}}">{{r.label}}</button>
        </sc-for>
      </div>
"""),
    # A3: tách hoa hồng thành 4 trạng thái (đã ghi nhận / chờ duyệt · tạm giữ /
    # đã rút / khả dụng) thay vì chỉ 2 con số, và nói rõ cơ chế hold.
    ("""        <div style="display:flex;justify-content:space-between;gap:var(--s5)">
          <div><div style="font-size:12px;color:var(--c6);font-weight:600">Số dư khả dụng</div><div style="font-size:26px;font-weight:900;color:var(--c6)">{{availableBalanceLabel}}</div></div>
          <div style="text-align:right"><div style="font-size:12px;color:var(--c5)">Đang chờ duyệt (đã khóa)</div><div style="font-size:15px;font-weight:700;color:var(--c2)">{{pendingBalanceLabel}}</div></div>
        </div>
        <div style="font-size:11px;color:var(--c5)">Đã ghi nhận: {{earnedBalanceLabel}} · số tiền đang chờ/đã duyệt sẽ tạm khóa khỏi số dư khả dụng.</div>""",
     """        <div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--s5)">
          <div><div style="font-size:12px;color:var(--c5)">Đã ghi nhận</div><div style="font-size:18px;font-weight:700;color:var(--c2)">{{earnedBalanceLabel}}</div></div>
          <div style="text-align:right"><div style="font-size:12px;color:var(--c5)">Đang chờ duyệt · tạm giữ</div><div style="font-size:18px;font-weight:700;color:var(--c9)">{{pendingBalanceLabel}}</div></div>
          <div><div style="font-size:12px;color:var(--c5)">Đã rút</div><div style="font-size:18px;font-weight:700;color:var(--c2)">{{metricWithdrawn}}</div></div>
          <div style="text-align:right"><div style="font-size:12px;color:var(--c6);font-weight:600">Số dư khả dụng</div><div style="font-size:26px;font-weight:900;color:var(--c6)">{{availableBalanceLabel}}</div></div>
        </div>
        <div style="font-size:11px;color:var(--c5);border-top:1px solid rgba(170,170,170,.35);padding-top:var(--s4);line-height:1.6">Yêu cầu rút tiền đang ở trạng thái <strong>chờ duyệt</strong> hoặc <strong>đã duyệt</strong> sẽ được tạm giữ và trừ khỏi số dư khả dụng, cho tới khi chi trả xong hoặc bị từ chối. Bị từ chối thì tiền hoàn lại số dư khả dụng.</div>"""),
    # Cột biểu đồ hoa hồng (A3): dùng teal thay màu chính.
    ("border-radius:var(--r-sm) var(--r-sm) 0 0;background:var(--c6)",
     "border-radius:var(--r-sm) var(--r-sm) 0 0;background:var(--c-chart)"),
    # A1 + C1: nền xám nhạt -> nền ấm
    ("background:rgba(170,170,170,.05)", "background:var(--warm-50)"),
    # Thẻ chỉ có viền, không khai báo nền: trên nền trắng của mockup thì không
    # thấy, nhưng trên nền ấm mới sẽ bị chìm -> cho về trắng để nổi khối.
    ('style="border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg)',
     'style="background:var(--c12);border:1px solid rgba(170,170,170,.35);'
     'border-radius:var(--r-lg)'),
    # A3: đang để trắng -> nền ấm cho các thẻ nổi lên
    ("padding:0 var(--s7) var(--s11);background:var(--c12)",
     "padding:0 var(--s7) var(--s11);background:var(--warm-50)"),
]

# ---------------------------------------------------------------------------
# Bổ sung ngoài mockup KH (yêu cầu 08/09): màn Quản lý sản phẩm và chức năng
# Thêm hàng vào kho. Viết bằng đúng style inline của mockup để không lệch tông.
# Dùng màu gốc (#00ADEE, rgba(170,...)) để bảng COLORS xử lý như mọi chỗ khác.
# ---------------------------------------------------------------------------

_INP = ('height:44px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);'
        'border-radius:var(--r-md);font-size:14px')
_FOCUS = 'border-color:#00ADEE;box-shadow:0 0 0 3px rgba(0,173,238,.25)'
_BTN_PRIMARY = ('height:38px;padding:0 var(--s6);background:var(--c6);border:none;'
                'border-radius:var(--r-md);font-size:13px;font-weight:600;color:var(--c12)')
_BTN_GHOST = ('height:38px;padding:0 var(--s6);background:var(--c12);'
              'border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);'
              'font-size:13px;font-weight:600;color:var(--c2)')

B5_PRODUCTS = """      <!-- B5 PRODUCTS (bổ sung, không có trong mockup KH) -->
      <sc-if value="{{isB5}}" hint-placeholder-val="{{false}}">
        <div style="display:flex;flex-direction:column;gap:var(--s7)">
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:var(--s5)">
            <div><div style="font-size:24px;font-weight:700">Quản lý sản phẩm</div><div style="font-size:12px;color:var(--c5);margin-top:var(--s1)">{{productCount}} sản phẩm đang bán</div></div>
            <button sc-camel-on-click="{{openProductForm}}" style="%(btn)s" style-hover="background:#0099d1">+ Thêm sản phẩm</button>
          </div>

          <div style="background:var(--c12);border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);overflow:hidden">
            <table style="width:100%%;border-collapse:collapse;font-size:13px">
              <thead>
                <tr style="background:rgba(170,170,170,.08);text-align:left">
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5);width:104px">Hình ảnh</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5);width:32%%">Tên sản phẩm</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Mô tả</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5);width:88px"></th>
                </tr>
              </thead>
              <tbody>
                <sc-for list="{{products}}" as="p" hint-placeholder-count="2">
                  <tr style="border-top:1px solid rgba(170,170,170,.2)">
                    <td style="padding:var(--s5);vertical-align:top"><div style="width:72px;height:72px;border-radius:var(--r-md);background:rgba(170,170,170,.15);display:flex;align-items:center;justify-content:center;font-size:10px;color:var(--c5);text-align:center;padding:var(--s2)">{{p.imageLabel}}</div></td>
                    <td style="padding:var(--s5);vertical-align:top"><div style="font-weight:600;color:var(--c1)">{{p.name}}</div><div style="font-size:12px;color:var(--c5);margin-top:var(--s1);font-family:monospace">{{p.sku}}</div></td>
                    <td style="padding:var(--s5);vertical-align:top;color:var(--c2);line-height:1.6">{{p.desc}}</td>
                    <td style="padding:var(--s5);vertical-align:top"><button sc-camel-on-click="{{p.onEdit}}" style="height:32px;padding:0 var(--s5);background:var(--c12);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:12px;font-weight:600;color:var(--c2)" style-hover="background:rgba(170,170,170,.08)">Sửa</button></td>
                  </tr>
                </sc-for>
              </tbody>
            </table>
          </div>
        </div>
      </sc-if>

      <sc-if value="{{showProductForm}}" hint-placeholder-val="{{false}}">
        <div style="position:fixed;inset:0;background:rgba(31,31,31,.5);display:flex;align-items:flex-start;justify-content:center;z-index:220;padding:var(--s7);overflow-y:auto">
          <div style="width:100%%;max-width:460px;background:var(--c12);border-radius:var(--r-lg);padding:var(--s8);display:flex;flex-direction:column;gap:var(--s6);box-shadow:0 8px 30px rgba(0,0,0,.25);margin:var(--s10) 0">
            <div style="display:flex;justify-content:space-between;align-items:flex-start">
              <div style="font-size:18px;font-weight:700;color:var(--c1)">{{productFormTitle}}</div>
              <button sc-camel-on-click="{{closeProductForm}}" style="background:none;border:none;font-size:18px;color:var(--c5)">&#10005;</button>
            </div>
            <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:14px;font-weight:600;color:var(--c2)">Tên sản phẩm (*)</label>
              <input type="text" value="{{productFormName}}" placeholder="Gói Bác sĩ 24/7 · License 12 tháng" style="%(inp)s" style-focus="%(focus)s">
            </div>
            <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:14px;font-weight:600;color:var(--c2)">Hình ảnh</label>
              <label style="border:1px dashed rgba(170,170,170,.6);border-radius:var(--r-md);padding:var(--s7);display:flex;flex-direction:column;align-items:center;gap:var(--s2);cursor:pointer;color:var(--c5)" style-hover="border-color:#00ADEE;color:#00ADEE">
                <span style="font-size:22px">&#11014;</span>
                <span style="font-size:13px;font-weight:600">Tải ảnh sản phẩm</span>
                <span style="font-size:11px">PNG hoặc JPG, tối đa 2MB</span>
              </label>
            </div>
            <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:14px;font-weight:600;color:var(--c2)">Mô tả</label>
              <textarea rows="4" placeholder="Mô tả ngắn hiển thị ở trang mua hàng…" style="padding:var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px;font-family:inherit;resize:vertical" style-focus="%(focus)s">{{productFormDesc}}</textarea>
            </div>
            <div style="display:flex;gap:var(--s5)">
              <button sc-camel-on-click="{{closeProductForm}}" style="flex:1;height:44px;background:var(--c12);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px;font-weight:600;color:var(--c2)">Huỷ</button>
              <button sc-camel-on-click="{{closeProductForm}}" style="flex:1;height:44px;background:var(--c6);border:none;border-radius:var(--r-md);font-size:14px;font-weight:600;color:var(--c12)" style-hover="background:#0099d1">Lưu sản phẩm</button>
            </div>
          </div>
        </div>
      </sc-if>

      <sc-if value="{{showAddStock}}" hint-placeholder-val="{{false}}">
        <div style="position:fixed;inset:0;background:rgba(31,31,31,.5);display:flex;align-items:center;justify-content:center;z-index:220;padding:var(--s7)">
          <div style="width:100%%;max-width:420px;background:var(--c12);border-radius:var(--r-lg);padding:var(--s8);display:flex;flex-direction:column;gap:var(--s6);box-shadow:0 8px 30px rgba(0,0,0,.25)">
            <div style="display:flex;justify-content:space-between;align-items:flex-start">
              <div><div style="font-size:18px;font-weight:700;color:var(--c1)">Thêm hàng vào kho</div><div style="font-size:12px;color:var(--c5);margin-top:var(--s1)">Mỗi mã kích hoạt gắn với đúng một sản phẩm</div></div>
              <button sc-camel-on-click="{{closeAddStock}}" style="background:none;border:none;font-size:18px;color:var(--c5)">&#10005;</button>
            </div>
            <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:14px;font-weight:600;color:var(--c2)">Mã sản phẩm (*)</label>
              <input type="text" value="{{addStockSku}}" sc-camel-on-change="{{setAddStockSku}}" placeholder="CN02-0025" style="%(inp)s;font-family:monospace" style-focus="%(focus)s">
            </div>
            <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:14px;font-weight:600;color:var(--c2)">Mã kích hoạt (*)</label>
              <input type="text" value="{{addStockCode}}" sc-camel-on-change="{{setAddStockCode}}" placeholder="ACT-100925" style="%(inp)s;font-family:monospace" style-focus="%(focus)s">
            </div>
            <sc-if value="{{addStockError}}" hint-placeholder-val="{{false}}">
              <div style="font-size:12px;color:#D9342B;background:rgba(217,52,43,.08);border-radius:var(--r-sm);padding:var(--s4);line-height:1.6">{{addStockError}}</div>
            </sc-if>
            <div style="font-size:11px;color:var(--c5);line-height:1.6">Hàng thêm vào sẽ ở trạng thái <strong>Sẵn hàng</strong> cho tới khi được gán vào đơn. Mã kích hoạt và mã sản phẩm không được trùng với mã đã có trong kho.</div>
            <div style="display:flex;gap:var(--s5)">
              <button sc-camel-on-click="{{closeAddStock}}" style="flex:1;height:44px;background:var(--c12);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px;font-weight:600;color:var(--c2)">Huỷ</button>
              <button sc-camel-on-click="{{submitAddStock}}" style="flex:1;height:44px;background:var(--c6);border:none;border-radius:var(--r-md);font-size:14px;font-weight:600;color:var(--c12)" style-hover="background:#0099d1">Thêm vào kho</button>
            </div>
          </div>
        </div>
      </sc-if>

      <sc-if value="{{showImportStock}}" hint-placeholder-val="{{false}}">
        <div style="position:fixed;inset:0;background:rgba(31,31,31,.5);display:flex;align-items:flex-start;justify-content:center;z-index:220;padding:var(--s7);overflow-y:auto">
          <div style="width:100%%;max-width:560px;background:var(--c12);border-radius:var(--r-lg);padding:var(--s8);display:flex;flex-direction:column;gap:var(--s6);box-shadow:0 8px 30px rgba(0,0,0,.25);margin:var(--s10) 0">
            <div style="display:flex;justify-content:space-between;align-items:flex-start">
              <div><div style="font-size:18px;font-weight:700;color:var(--c1)">Import hàng loạt</div><div style="font-size:12px;color:var(--c5);margin-top:var(--s1)">Mã nào hợp lệ thì nhận, mã trùng thì bỏ qua và báo lại</div></div>
              <button sc-camel-on-click="{{closeImportStock}}" style="background:none;border:none;font-size:18px;color:var(--c5)">&#10005;</button>
            </div>

            <label style="border:1px dashed rgba(170,170,170,.6);border-radius:var(--r-md);padding:var(--s6);display:flex;align-items:center;justify-content:center;gap:var(--s3);cursor:pointer;color:var(--c5);font-size:13px;font-weight:600" style-hover="border-color:#00ADEE;color:#00ADEE">
              <span style="font-size:18px">&#11014;</span> Chọn file Excel / CSV
            </label>

            <div style="display:flex;flex-direction:column;gap:var(--s2)">
              <label style="font-size:14px;font-weight:600;color:var(--c2)">Hoặc dán danh sách</label>
              <div style="font-size:11px;color:var(--c5);line-height:1.6">Mỗi dòng một thiết bị, theo thứ tự <strong>mã sản phẩm, mã kích hoạt</strong>. Ví dụ: <span style="font-family:monospace">CN02-1301, ACT-130145</span></div>
              <textarea rows="7" value="{{importText}}" sc-camel-on-change="{{setImportText}}" placeholder="CN02-1301, ACT-130145&#10;CN02-1302, ACT-130146&#10;CN02-1303, ACT-130147" style="padding:var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:13px;font-family:monospace;resize:vertical" style-focus="%(focus)s"></textarea>
            </div>

            <sc-if value="{{hasImportResult}}" hint-placeholder-val="{{false}}">
              <div style="display:flex;flex-direction:column;gap:var(--s4);border:1px solid rgba(170,170,170,.35);border-radius:var(--r-md);padding:var(--s6)">
                <div style="display:flex;gap:var(--s7);flex-wrap:wrap;font-size:13px">
                  <div><span style="color:var(--c5)">Tổng dòng: </span><strong>{{importResult.total}}</strong></div>
                  <div><span style="color:var(--c5)">Đã nhập: </span><strong style="color:#4c7a2e">{{importResult.ok}}</strong></div>
                  <div><span style="color:var(--c5)">Bỏ qua: </span><strong style="color:#D9342B">{{importResult.skip}}</strong></div>
                </div>
                <sc-if value="{{importResult.hasSkipped}}" hint-placeholder-val="{{false}}">
                  <div style="display:flex;flex-direction:column;gap:var(--s2);max-height:180px;overflow-y:auto">
                    <sc-for list="{{importResult.skipped}}" as="k" hint-placeholder-count="3">
                      <div style="font-size:12px;display:flex;gap:var(--s4);align-items:baseline">
                        <span style="font-family:monospace;color:var(--c2);flex:1;min-width:0;word-break:break-all">{{k.line}}</span>
                        <span style="flex:none;color:#D9342B">{{k.reason}}</span>
                      </div>
                    </sc-for>
                  </div>
                </sc-if>
              </div>
            </sc-if>

            <div style="display:flex;gap:var(--s5)">
              <button sc-camel-on-click="{{closeImportStock}}" style="flex:1;height:44px;background:var(--c12);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px;font-weight:600;color:var(--c2)">Đóng</button>
              <button sc-camel-on-click="{{runImportStock}}" style="flex:1;height:44px;background:var(--c6);border:none;border-radius:var(--r-md);font-size:14px;font-weight:600;color:var(--c12)" style-hover="background:#0099d1">Import</button>
            </div>
          </div>
        </div>
      </sc-if>

""" % {"btn": _BTN_PRIMARY, "inp": _INP, "focus": _FOCUS}

B6_ORDERS = """      <!-- B6 ORDERS (bổ sung, không có trong mockup KH) -->
      <sc-if value="{{isB6}}" hint-placeholder-val="{{false}}">
        <div style="display:flex;flex-direction:column;gap:var(--s7)">
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:var(--s5)">
            <div><div style="font-size:24px;font-weight:700">Quản lý đơn hàng</div><div style="font-size:12px;color:var(--c5);margin-top:var(--s1)">{{orderTotal}} đơn · đối soát chuyển khoản và cấp mã kích hoạt</div></div>
            <button style="%(ghost)s" style-hover="background:rgba(170,170,170,.08)">Xuất file Excel</button>
          </div>

          <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:var(--s5)">
            <div style="background:var(--c12);border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);padding:var(--s7);display:flex;flex-direction:column;gap:var(--s2)"><div style="font-size:12px;color:var(--c5)">Chờ đối soát</div><div style="font-size:26px;font-weight:700;color:var(--c1)">{{orderPendingCount}}</div></div>
            <div style="background:var(--c12);border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);padding:var(--s7);display:flex;flex-direction:column;gap:var(--s2)"><div style="font-size:12px;color:var(--c5)">Chờ Head Admin</div><div style="font-size:26px;font-weight:700;color:var(--c1)">{{orderConfirm1Count}}</div></div>
            <div style="background:var(--c12);border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);padding:var(--s7);display:flex;flex-direction:column;gap:var(--s2)"><div style="font-size:12px;color:var(--c5)">Đã thanh toán</div><div style="font-size:26px;font-weight:700;color:var(--c1)">{{orderPaidCount}}</div></div>
            <div style="background:var(--c12);border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);padding:var(--s7);display:flex;flex-direction:column;gap:var(--s2)"><div style="font-size:12px;color:var(--c5)">Doanh thu đã đối soát</div><div style="font-size:22px;font-weight:700;color:var(--c1)">{{orderRevenue}}</div></div>
          </div>

          <div style="display:flex;gap:var(--s5);flex-wrap:wrap;align-items:center">
            <div style="display:flex;gap:var(--s2);flex-wrap:wrap">
              <sc-for list="{{orderFilters}}" as="f" hint-placeholder-count="5">
                <button sc-camel-on-click="{{f.onClick}}" style="{{f.style}}">{{f.label}}</button>
              </sc-for>
            </div>
            <input type="text" value="{{orderSearch}}" sc-camel-on-change="{{setOrderSearch}}" placeholder="Tìm theo mã đơn, tên hoặc SĐT khách…" style="flex:1;min-width:220px;height:38px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px" style-focus="%(focus)s">
          </div>

          <div style="background:var(--c12);border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);overflow:hidden">
            <table style="width:100%%;border-collapse:collapse;font-size:13px">
              <thead>
                <tr style="background:rgba(170,170,170,.08);text-align:left">
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Mã đơn</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Khách hàng</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Gói</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Số tiền</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Người giới thiệu</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Ngày đặt</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Trạng thái</th>
                </tr>
              </thead>
              <tbody>
                <sc-for list="{{orders}}" as="o" hint-placeholder-count="5">
                  <tr sc-camel-on-click="{{o.onClick}}" style="border-top:1px solid rgba(170,170,170,.2);cursor:pointer" style-hover="background:rgba(0,173,238,.05)">
                    <td style="padding:var(--s5);font-family:monospace;font-weight:600;color:var(--c1)">{{o.id}}</td>
                    <td style="padding:var(--s5)"><div style="font-weight:600;color:var(--c1)">{{o.buyer}}</div><div style="font-size:12px;color:var(--c5)">{{o.phone}}</div></td>
                    <td style="padding:var(--s5);color:var(--c2)">{{o.pkg}}</td>
                    <td style="padding:var(--s5);font-weight:600;color:var(--c1)">{{o.amount}}</td>
                    <td style="padding:var(--s5);color:var(--c2)">{{o.referrer}}</td>
                    <td style="padding:var(--s5);color:var(--c5)">{{o.date}}</td>
                    <td style="padding:var(--s5)"><span style="display:inline-block;padding:4px 10px;border-radius:var(--r-xl);font-size:11px;font-weight:600;background:{{o.badgeBg}};color:{{o.badgeColor}}">{{o.statusLabel}}</span></td>
                  </tr>
                </sc-for>
              </tbody>
            </table>
            <sc-if value="{{ordersEmpty}}" hint-placeholder-val="{{false}}">
              <div style="padding:var(--s10);text-align:center;font-size:13px;color:var(--c5)">Không có đơn hàng nào khớp bộ lọc.</div>
            </sc-if>
          </div>
        </div>
      </sc-if>

      <sc-if value="{{hasSelectedOrder}}" hint-placeholder-val="{{false}}">
        <div style="position:fixed;inset:0;background:rgba(31,31,31,.4);display:flex;justify-content:flex-end;z-index:210">
          <div style="width:100%%;max-width:470px;background:var(--c12);height:100%%;overflow-y:auto;padding:var(--s8);display:flex;flex-direction:column;gap:var(--s6);box-shadow:-8px 0 30px rgba(0,0,0,.15)">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:var(--s5)">
              <div><div style="font-size:20px;font-weight:700;color:var(--c1);font-family:monospace">{{selectedOrder.id}}</div><div style="margin-top:var(--s2)"><span style="display:inline-block;padding:4px 10px;border-radius:var(--r-xl);font-size:11px;font-weight:600;background:{{selectedOrder.badgeBg}};color:{{selectedOrder.badgeColor}}">{{selectedOrder.statusLabel}}</span></div></div>
              <button sc-camel-on-click="{{closeOrder}}" style="background:none;border:none;font-size:18px;color:var(--c5)">&#10005;</button>
            </div>

            <sc-if value="{{selectedOrder.stageNote}}" hint-placeholder-val="{{false}}">
              <div style="font-size:12px;color:#a36400;background:rgba(255,165,0,.12);border-radius:var(--r-sm);padding:var(--s4);line-height:1.6">{{selectedOrder.stageNote}}</div>
            </sc-if>

            <div style="display:flex;flex-direction:column;gap:var(--s4);font-size:13px">
              <div style="font-size:12px;color:var(--c5);text-transform:uppercase;letter-spacing:.04em">Khách hàng</div>
              <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5)">Họ tên</span><span style="font-weight:600;color:var(--c1);text-align:right">{{selectedOrder.buyer}}</span></div>
              <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5)">Số điện thoại</span><span style="font-weight:600;color:var(--c1)">{{selectedOrder.phone}}</span></div>
              <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5)">Email</span><span style="color:var(--c2);text-align:right">{{selectedOrder.email}}</span></div>
              <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5)">Địa chỉ nhận hàng</span><span style="color:var(--c2);text-align:right;max-width:62%%">{{selectedOrder.address}}</span></div>
            </div>

            <div style="height:1px;background:rgba(170,170,170,.25)"></div>

            <div style="display:flex;flex-direction:column;gap:var(--s4);font-size:13px">
              <div style="font-size:12px;color:var(--c5);text-transform:uppercase;letter-spacing:.04em">Đơn hàng</div>
              <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5)">Gói</span><span style="font-weight:600;color:var(--c1);text-align:right">{{selectedOrder.pkg}}</span></div>
              <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5)">Số tiền</span><span style="font-weight:700;color:var(--c6);font-size:16px">{{selectedOrder.amount}}</span></div>
              <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5)">Người giới thiệu</span><span style="color:var(--c2)">{{selectedOrder.referrer}} · {{selectedOrder.refCode}}</span></div>
              <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5)">Ngày đặt</span><span style="color:var(--c2)">{{selectedOrder.date}}</span></div>
              <div style="display:flex;justify-content:space-between;gap:var(--s5)"><span style="color:var(--c5)">Mã kích hoạt</span><span style="font-family:monospace;font-weight:600;color:var(--c1)">{{selectedOrder.activationCodeLabel}}</span></div>
            </div>

            <div style="height:1px;background:rgba(170,170,170,.25)"></div>

            <div style="display:flex;flex-direction:column;gap:var(--s4)">
              <div style="font-size:12px;color:var(--c5);text-transform:uppercase;letter-spacing:.04em">Ảnh chuyển khoản</div>
              <div style="border:1px solid rgba(170,170,170,.35);border-radius:var(--r-md);padding:var(--s7);display:flex;flex-direction:column;align-items:center;gap:var(--s3);background:rgba(170,170,170,.05)">
                <span style="font-size:26px;color:var(--c5)">&#128196;</span>
                <span style="font-size:12px;color:var(--c2);font-family:monospace">{{selectedOrder.proof}}</span>
                <span style="font-size:11px;color:var(--c5)">Bấm để xem ảnh gốc</span>
              </div>
            </div>

            <div style="display:flex;flex-direction:column;gap:var(--s4)">
              <div style="font-size:12px;color:var(--c5);text-transform:uppercase;letter-spacing:.04em">Lịch sử xử lý</div>
              <sc-for list="{{selectedOrder.auditLog}}" as="a" hint-placeholder-count="3">
                <div style="display:flex;gap:var(--s4);font-size:12px">
                  <div style="flex:none;width:6px;height:6px;border-radius:var(--r-full);background:var(--c6);margin-top:6px"></div>
                  <div><div style="color:var(--c1);font-weight:600">{{a.label}}</div><div style="color:var(--c5)">{{a.actor}} · {{a.time}}</div></div>
                </div>
              </sc-for>
            </div>

            <sc-if value="{{selectedOrder.isRejected}}" hint-placeholder-val="{{false}}">
              <div style="font-size:12px;color:var(--c2);background:rgba(170,170,170,.08);border-radius:var(--r-sm);padding:var(--s5);line-height:1.6">Đơn đã bị từ chối. Phase 1 <strong>không mở lại đơn cũ</strong> — khách cần đặt đơn mới qua link giới thiệu.</div>
            </sc-if>

            <sc-if value="{{selectedOrder.canAct}}" hint-placeholder-val="{{true}}">
              <div style="display:flex;flex-direction:column;gap:var(--s4);border-top:1px solid rgba(170,170,170,.25);padding-top:var(--s6)">
                <sc-if value="{{selectedOrder.needsCodePick}}" hint-placeholder-val="{{true}}">
                  <div style="display:flex;flex-direction:column;gap:var(--s2)">
                    <label style="font-size:14px;font-weight:600;color:var(--c2)">Chọn mã kích hoạt từ kho (*)</label>
                    <sc-raw-select value="{{orderActivationCode}}" sc-camel-on-change="{{setOrderActivationCode}}" style="height:44px;padding:0 var(--s5);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px;font-family:monospace;color:var(--c2);background:var(--c12)">
                      <option value="">— Chọn mã Sẵn hàng —</option>
                      <sc-for list="{{availableStockCodes}}" as="c" hint-placeholder-count="5">
                        <option value="{{c.code}}">{{c.label}}</option>
                      </sc-for>
                    </sc-raw-select>
                    <div style="font-size:11px;color:var(--c5)">Còn {{availableStockCount}} mã Sẵn hàng trong kho. Mã đã chọn sẽ chuyển sang <strong>Đã gán đơn hàng</strong>.</div>
                  </div>
                  <sc-if value="{{orderCodeError}}" hint-placeholder-val="{{false}}">
                    <div style="font-size:12px;color:#D9342B;background:rgba(217,52,43,.08);border-radius:var(--r-sm);padding:var(--s4)">{{orderCodeError}}</div>
                  </sc-if>
                </sc-if>
                <sc-if value="{{selectedOrder.canConfirm}}" hint-placeholder-val="{{true}}">
                  <button sc-camel-on-click="{{confirmOrder}}" style="height:44px;background:var(--c6);border:none;border-radius:var(--r-md);font-size:14px;font-weight:600;color:var(--c12)" style-hover="background:#0099d1">{{selectedOrder.confirmLabel}}</button>
                </sc-if>
                <sc-if value="{{selectedOrder.canReject}}" hint-placeholder-val="{{true}}">
                  <button sc-camel-on-click="{{rejectOrder}}" style="height:42px;background:var(--c12);border:1px solid #D9342B;border-radius:var(--r-md);font-size:14px;font-weight:600;color:#D9342B" style-hover="background:rgba(217,52,43,.06)">Từ chối đơn</button>
                </sc-if>
                <div style="font-size:11px;color:var(--c5);line-height:1.6">{{selectedOrder.actHint}}</div>
              </div>
            </sc-if>
          </div>
        </div>
      </sc-if>

""" % {"ghost": _BTN_GHOST, "focus": _FOCUS}

# Nối 2 mục này SAU khi B5_PRODUCTS / B6_ORDERS đã khai báo ở trên.
BG_PATCHES += [
    # Chèn màn Đơn hàng (B6) và Quản lý sản phẩm (B5) ngay trước khối B4.
    ("      <!-- B4 WAREHOUSE -->",
     B6_ORDERS + B5_PRODUCTS + "      <!-- B4 WAREHOUSE -->"),
    # B4: thêm nút "Thêm hàng vào kho" cạnh nút xuất Excel.
    ('<button style="%s" style-hover="background:rgba(170,170,170,.08)">'
     'Xuất file Excel</button>' % _BTN_GHOST,
     '<div style="display:flex;gap:var(--s3);flex-wrap:wrap">'
     '<button style="%s" style-hover="background:rgba(170,170,170,.08)">'
     'Xuất file Excel</button>'
     '<button sc-camel-on-click="{{openImportStock}}" style="%s" '
     'style-hover="background:rgba(170,170,170,.08)">Import hàng loạt</button>'
     '<button sc-camel-on-click="{{openAddStock}}" style="%s" '
     'style-hover="background:#0099d1">+ Thêm hàng vào kho</button></div>'
     % (_BTN_GHOST, _BTN_GHOST, _BTN_PRIMARY)),
]

B7_ADMIN_USERS = """      <!-- B7 ADMIN USERS (bổ sung 7.9.1, không có trong mockup KH) -->
      <sc-if value="{{isB7}}" hint-placeholder-val="{{false}}">
        <div style="display:flex;flex-direction:column;gap:var(--s7)">
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:var(--s5)">
            <div><div style="font-size:24px;font-weight:700">Tài khoản admin</div><div style="font-size:12px;color:var(--c5);margin-top:var(--s1)">{{adminUserCount}} tài khoản · mỗi tài khoản gán đúng 1 vai trò</div></div>
            <button sc-camel-on-click="{{openAdminUserForm}}" style="%(btn)s" style-hover="background:#0099d1">+ Thêm tài khoản</button>
          </div>

          <div style="background:var(--c12);border:1px solid rgba(170,170,170,.35);border-radius:var(--r-lg);overflow:hidden">
            <table style="width:100%%;border-collapse:collapse;font-size:13px">
              <thead>
                <tr style="background:rgba(170,170,170,.08);text-align:left">
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Họ tên</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Email đăng nhập</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Vai trò</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5)">Trạng thái</th>
                  <th style="padding:var(--s5);font-weight:600;color:var(--c5);width:170px"></th>
                </tr>
              </thead>
              <tbody>
                <sc-for list="{{adminUsers}}" as="u" hint-placeholder-count="3">
                  <tr style="border-top:1px solid rgba(170,170,170,.2)">
                    <td style="padding:var(--s5);font-weight:600;color:var(--c1)">{{u.name}}</td>
                    <td style="padding:var(--s5);color:var(--c2);font-family:monospace">{{u.email}}</td>
                    <td style="padding:var(--s5)"><span style="display:inline-block;padding:4px 10px;border-radius:var(--r-xl);font-size:11px;font-weight:600;background:{{u.roleBg}};color:{{u.roleColor}}">{{u.roleLabel}}</span></td>
                    <td style="padding:var(--s5)"><span style="display:inline-block;padding:4px 10px;border-radius:var(--r-xl);font-size:11px;font-weight:600;background:{{u.badgeBg}};color:{{u.badgeColor}}">{{u.statusLabel}}</span></td>
                    <td style="padding:var(--s5)">
                      <div style="display:flex;gap:var(--s3)">
                        <button sc-camel-on-click="{{u.onEdit}}" style="height:32px;padding:0 var(--s5);background:var(--c12);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:12px;font-weight:600;color:var(--c2)" style-hover="background:rgba(170,170,170,.08)">Sửa</button>
                        <button sc-camel-on-click="{{u.onToggleLock}}" style="{{u.lockStyle}}">{{u.lockLabel}}</button>
                      </div>
                    </td>
                  </tr>
                </sc-for>
              </tbody>
            </table>
          </div>

          <div style="font-size:12px;color:var(--c5);line-height:1.7;background:rgba(170,170,170,.05);border-radius:var(--r-md);padding:var(--s6)">
            <strong style="color:var(--c2)">Admin Specialist</strong> làm bước 1 của mọi quy trình duyệt 2 lớp: xác nhận tiền về của đơn hàng, duyệt hồ sơ thành viên, duyệt yêu cầu rút tiền.<br>
            <strong style="color:var(--c2)">Head Admin</strong> làm bước 2 và là người duy nhất được kích hoạt tài khoản, cấp mã kích hoạt, đánh dấu đã chi trả, và quản lý chính màn này.
          </div>
        </div>
      </sc-if>

      <sc-if value="{{showAdminUserForm}}" hint-placeholder-val="{{false}}">
        <div style="position:fixed;inset:0;background:rgba(31,31,31,.5);display:flex;align-items:center;justify-content:center;z-index:220;padding:var(--s7)">
          <div style="width:100%%;max-width:430px;background:var(--c12);border-radius:var(--r-lg);padding:var(--s8);display:flex;flex-direction:column;gap:var(--s6);box-shadow:0 8px 30px rgba(0,0,0,.25)">
            <div style="display:flex;justify-content:space-between;align-items:flex-start">
              <div style="font-size:18px;font-weight:700;color:var(--c1)">{{adminUserFormTitle}}</div>
              <button sc-camel-on-click="{{closeAdminUserForm}}" style="background:none;border:none;font-size:18px;color:var(--c5)">&#10005;</button>
            </div>
            <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:14px;font-weight:600;color:var(--c2)">Họ tên (*)</label>
              <input type="text" value="{{adminUserFormName}}" placeholder="Nguyễn Thị Trinh" style="%(inp)s" style-focus="%(focus)s">
            </div>
            <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:14px;font-weight:600;color:var(--c2)">Email đăng nhập (*)</label>
              <input type="text" value="{{adminUserFormEmail}}" placeholder="trinh@homi365.com.vn" style="%(inp)s;font-family:monospace" style-focus="%(focus)s">
            </div>
            <div style="display:flex;flex-direction:column;gap:var(--s2)"><label style="font-size:14px;font-weight:600;color:var(--c2)">Vai trò (*)</label>
              <sc-raw-select style="%(inp)s;color:var(--c2);background:var(--c12)">
                <option>Admin Specialist</option>
                <option>Head Admin</option>
              </sc-raw-select>
              <div style="font-size:11px;color:var(--c5);line-height:1.6">Mỗi tài khoản chỉ được gán đúng một vai trò. Đổi vai trò có hiệu lực ở lần đăng nhập kế tiếp.</div>
            </div>
            <div style="display:flex;gap:var(--s5)">
              <button sc-camel-on-click="{{closeAdminUserForm}}" style="flex:1;height:44px;background:var(--c12);border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);font-size:14px;font-weight:600;color:var(--c2)">Huỷ</button>
              <button sc-camel-on-click="{{closeAdminUserForm}}" style="flex:1;height:44px;background:var(--c6);border:none;border-radius:var(--r-md);font-size:14px;font-weight:600;color:var(--c12)" style-hover="background:#0099d1">Lưu tài khoản</button>
            </div>
          </div>
        </div>
      </sc-if>

""" % {"btn": _BTN_PRIMARY, "inp": _INP, "focus": _FOCUS}

# B7 khai báo sau khối BG_PATCHES += ở trên nên phải nối riêng ở đây.
# Neo vẫn còn trong chuỗi thay thế của lần trước, nên lần này chèn tiếp được.
BG_PATCHES.append(("      <!-- B4 WAREHOUSE -->",
                   B7_ADMIN_USERS + "      <!-- B4 WAREHOUSE -->"))

KEEP = {
    "#ED1C24": "logo Techcombank",
    "#00A19A": "logo napas247",
    "#003DA5": "logo napas247",
}


def recolor(s):
    for old, new in COLORS:
        s = s.replace(old, new)
    return s


# ============================================================================
# 2. VỊ TRÍ CÁC KHỐI TRONG template.html (số dòng, 1-based)
# ============================================================================

L_FONTS = (12, 731)      # nội dung <style> chứa @font-face
L_BASE = (734, 738)      # nội dung <style> reset
L_ROOTDIV = 741          # <div style="--c1:…"> — nơi khai báo biến
L_TOPBAR_WRAP = 744      # thẻ <div> bọc thanh trên (giữ nguyên style)
L_SCRIPT = (1611, 2114)  # cả <script type="text/x-dc"> … </script>

# Khối bắt đầu tại dòng nào (nếu là dòng comment thì <sc-if> nằm ngay sau).
BLOCKS = {
    "A1": 754, "QR": 839, "PAYOK": 878, "LOOKUP": 893, "BLOCKED": 912,
    "A2": 922, "A3": 1040, "WDFORM": 1100, "WDOK": 1125,
    "C1": 1136, "B1": 1244, "ADMIN": 1259,
    "SLIDE_MEMBER": 1412, "SLIDE_STOCK": 1458, "SLIDE_WD": 1487,
    "MODALS": 1544,
}

# ============================================================================
# 3. DANH SÁCH MÀN HÌNH
# ============================================================================

FILES = {
    "A1": "a1-buy.html", "A2": "a2-register.html", "A3": "a3-dashboard.html",
    "C1": "c1-login.html", "B1": "b1-admin-login.html",
    "B2": "b2-members.html", "B3": "b3-withdrawals.html", "B4": "b4-warehouse.html",
    "B5": "b5-products.html", "B6": "b6-orders.html",
    "B7": "b7-admin-users.html",
}
ADMIN_CODES = ("B2", "B3", "B4", "B5", "B6", "B7")

ADMIN_BLOCKS = ["ADMIN", "SLIDE_MEMBER", "SLIDE_WD", "SLIDE_STOCK", "MODALS"]

SCREENS = [
    {
        "code": "A1", "title": "A1 · Thông tin nhận hàng", "group": "Người mua",
        "blocks": ["A1", "QR", "PAYOK", "LOOKUP", "BLOCKED"],
        "states": [
            ("", "Mặc định — form mua hàng", {}),
            ("qr", "Modal quét QR thanh toán", {"showQRPayment": True}),
            ("thanh-toan-ok", "Modal thanh toán thành công", {"showPaymentSuccess": True}),
            ("tra-cuu-don", "Modal tra cứu đơn hàng", {"showOrderLookup": True}),
            ("tuyen-tren-chan", "Modal tuyến trên bị chặn", {"showUplineBlockedModal": True}),
        ],
    },
    {
        "code": "A2", "title": "A2 · Đăng ký Agent", "group": "Người mua",
        "blocks": ["A2", "BLOCKED"],
        "states": [
            ("", "Bước 1 — thông tin", {"regStep": 1}),
            ("buoc-2", "Bước 2 — xác thực OTP", {"regStep": 2}),
            ("buoc-3", "Bước 3 — đặt mật khẩu", {"regStep": 3}),
            ("buoc-4", "Bước 4 — điều khoản", {"regStep": 4}),
            ("buoc-5", "Bước 5 — hoàn tất", {"regStep": 5}),
        ],
    },
    {
        "code": "A3", "title": "A3 · Dashboard thành viên", "group": "Thành viên",
        "blocks": ["A3", "WDFORM", "WDOK"],
        "states": [
            ("", "Agent mới — chưa có hoa hồng", {"agentStage": "new"}),
            ("da-tinh-hh", "Agent đang hoạt động", {"agentStage": "active"}),
            ("rut-tien", "Form yêu cầu rút tiền", {"agentStage": "active", "showWithdrawForm": True}),
            ("rut-tien-ok", "Rút tiền — gửi thành công", {"agentStage": "active", "showWithdrawSuccess": True}),
        ],
    },
    {
        "code": "C1", "title": "C1 · Đăng nhập thành viên", "group": "Thành viên",
        "blocks": ["C1", "LOOKUP"],
        "states": [
            ("", "Đăng nhập", {"agentLoginStep": "login"}),
            ("otp", "Xác thực OTP", {"agentLoginStep": "otp"}),
            ("quen-sdt", "Quên mật khẩu — nhập SĐT", {"agentLoginStep": "forgot_phone"}),
            ("quen-otp", "Quên mật khẩu — OTP", {"agentLoginStep": "forgot_otp"}),
            ("quen-dat-lai", "Quên mật khẩu — đặt lại", {"agentLoginStep": "forgot_reset"}),
            ("quen-ok", "Quên mật khẩu — thành công", {"agentLoginStep": "forgot_success"}),
        ],
    },
    {
        "code": "B1", "title": "B1 · Đăng nhập quản trị", "group": "Quản trị",
        "blocks": ["B1"],
        "states": [("", "Đăng nhập admin", {})],
    },
    {
        "code": "B2", "title": "B2 · Thành viên", "group": "Quản trị",
        "blocks": ADMIN_BLOCKS,
        "states": [
            ("", "Danh sách thành viên", {}),
            ("chi-tiet", "Ngăn chi tiết thành viên", {"selectedMemberId": 6}),
            ("duyet", "Modal duyệt hồ sơ", {"selectedMemberId": 6,
                                            "actionModal": {"type": "approve", "kind": "member", "id": 6}}),
            ("tu-choi", "Modal từ chối hồ sơ", {"selectedMemberId": 6,
                                                "actionModal": {"type": "reject", "kind": "member", "id": 6}}),
        ],
    },
    {
        "code": "B3", "title": "B3 · Yêu cầu rút tiền", "group": "Quản trị",
        "blocks": ADMIN_BLOCKS,
        "states": [
            ("", "Danh sách yêu cầu", {}),
            ("chi-tiet", "Ngăn chi tiết yêu cầu", {"selectedWithdrawalId": 1}),
            ("duyet", "Modal duyệt rút tiền", {"selectedWithdrawalId": 1,
                                               "actionModal": {"type": "approve", "kind": "withdrawal", "id": 1}}),
            ("tu-choi", "Modal từ chối rút tiền", {"selectedWithdrawalId": 1,
                                                   "actionModal": {"type": "reject", "kind": "withdrawal", "id": 1}}),
            ("da-chi-tra", "Modal đánh dấu đã chi trả", {"selectedWithdrawalId": 3,
                                                         "actionModal": {"type": "paid", "kind": "withdrawal", "id": 3}}),
        ],
    },
    {
        "code": "B4", "title": "B4 · Quản lý kho hàng", "group": "Quản trị",
        "blocks": ADMIN_BLOCKS,
        "states": [
            ("", "Danh sách kho", {}),
            ("chi-tiet", "Ngăn chi tiết thiết bị", {"selectedStockId": 3}),
            ("them-hang", "Modal thêm hàng vào kho", {"showAddStock": True}),
            ("import", "Modal import hàng loạt", {"showImportStock": True}),
        ],
    },
    {
        "code": "B6", "title": "B6 · Quản lý đơn hàng", "group": "Quản trị",
        "blocks": ADMIN_BLOCKS,
        "states": [
            ("", "Danh sách đơn hàng", {}),
            ("cho-doi-soat", "Chi tiết đơn chờ đối soát", {"selectedOrderId": "DH923983"}),
            ("cho-head", "Chi tiết đơn chờ Head Admin", {"selectedOrderId": "DH100511"}),
            ("da-thanh-toan", "Chi tiết đơn đã cấp mã", {"selectedOrderId": "DH100234"}),
            ("head", "Xem với vai Head Admin", {"adminRole": "head",
                                                "selectedOrderId": "DH100511"}),
        ],
    },
    {
        "code": "B7", "title": "B7 · Tài khoản admin", "group": "Quản trị",
        "blocks": ADMIN_BLOCKS,
        "states": [
            ("", "Danh sách tài khoản admin", {}),
            ("them", "Modal thêm tài khoản", {"showAdminUserForm": True}),
        ],
    },
    {
        "code": "B5", "title": "B5 · Quản lý sản phẩm", "group": "Quản trị",
        "blocks": ADMIN_BLOCKS,
        "states": [
            ("", "Danh sách sản phẩm", {}),
            ("them", "Modal thêm sản phẩm", {"showProductForm": True}),
            ("sua", "Modal sửa sản phẩm", {"showProductForm": True,
                                           "editingProductId": "CN02"}),
        ],
    },
]

# ============================================================================
# 4. SỬA JS: điều hướng giữa các file thay vì đổi state trong một trang
# ============================================================================

JS_PATCHES = [
    # Thêm helper GO() và cho nav dùng nó.
    ("    const set = (id) => () => this.setState({ screen: id });",
     "    const GO = (id, carry) => {\n"
     "      const f = (window.__FILES || {})[id];\n"
     "      if (!f) return;\n"
     "      try { sessionStorage.setItem('__homi_carry', JSON.stringify(carry || {})); } catch (e) {}\n"
     "      location.href = f;\n"
     "    };\n"
     "    const set = (id) => () => GO(id);"),

    # Mua xong -> chọn đăng ký seller
    ("this.setState({ showPaymentSuccess: false, screen: 'A2', regStep: 1 })",
     "GO('A2', { regStep: 1 })"),

    # Đăng ký xong -> dashboard
    ("goToA3: () => this.setState({ screen: 'A3' })",
     "goToA3: () => GO('A3')"),

    # Đăng nhập agent thành công -> dashboard
    ("{ this.setState({ screen: 'A3', agentLoginError: false }); }",
     "{ GO('A3'); }"),
    ("agentOtpConfirm: () => this.setState({ screen: 'A3', agentLoginStep: 'login', agentLoginError: false })",
     "agentOtpConfirm: () => GO('A3')"),

    # Đăng nhập admin -> màn Thành viên
    ("adminLoginSubmit: () => this.setState({ screen: 'B2' })",
     "adminLoginSubmit: () => GO('B2')"),

    # Tra cứu đơn thành công -> sang màn đăng ký, mang theo dữ liệu đơn
    ("""        this.setState({
          showOrderLookup: false, screen: 'A2', regStep: 1,
          orderId: order.orderId, uplineRank,
          buyerName: order.buyerName, buyerPhone: phone, buyerEmail: order.buyerEmail,
          buyerCccd: order.buyerCccd, buyerAddress: order.buyerAddress, buyerDob: order.buyerDob
        });""",
     """        GO('A2', {
          regStep: 1,
          orderId: order.orderId, uplineRank,
          buyerName: order.buyerName, buyerPhone: phone, buyerEmail: order.buyerEmail,
          buyerCccd: order.buyerCccd, buyerAddress: order.buyerAddress, buyerDob: order.buyerDob
        });"""),

    # 7.3.2 — số đơn đổi theo khoảng thời gian đang chọn.
    ("      metricOrders: s.agentStage === 'active' ? '10' : '1',",
     "      metricOrders: (s.agentStage === 'active' ? this.ORDER_RANGE_VALUES\n"
     "        : this.ORDER_RANGE_VALUES_NEW)[s.orderRange || 'month'],"),

    # 7.5.2 — lịch sử thăng/giáng hạng trong ngăn chi tiết thành viên.
    ("      selectedMember = {\n        ...selectedMemberRaw, status: effStatus,",
     "      selectedMember = {\n        ...selectedMemberRaw, status: effStatus,\n"
     "        rankHistory: this.RANK_HISTORY[selectedMemberRaw.id]\n"
     "          || [{ label: 'Tham gia · hạng ' + selectedMemberRaw.rank, time: selectedMemberRaw.joined }],"),

    # Cho phép trang bơm state ban đầu (chọn màn, chọn bước, mở modal)
    # + state cho màn Quản lý sản phẩm và modal Thêm hàng vào kho.
    ("    actionModal: null, rejectReason: '', paidNote: ''\n  };",
     "    actionModal: null, rejectReason: '', paidNote: '',\n"
     "    showProductForm: false, editingProductId: null,\n"
     "    showAddStock: false, addStockSku: '', addStockCode: '', addStockError: '',\n"
     "    showImportStock: false, importText: '', importResult: null,\n"
     "    orderActivationCode: '', orderCodeError: '',\n"
     "    copyPersonalLabel: 'Copy link',\n"
     "    showAdminUserForm: false, editingAdminUserId: null, adminUserLocks: {},\n"
     "    orderRange: 'month',\n"
     "    ordersData: null, orderSearch: '', orderStatusFilter: 'all',\n"
     "    selectedOrderId: null,\n"
     "    ...(window.__STATE__ || {})\n  };"),

    # Sidebar quản trị: thêm mục Quản lý sản phẩm.
    ("  ADMIN_NAV = [['B2','Thành viên'],['B3','Yêu cầu rút tiền'],"
     "['B4','Quản lý kho hàng']];",
     "  ADMIN_NAV = [['B2','Thành viên'],['B3','Yêu cầu rút tiền'],"
     "['B6','Đơn hàng'],['B4','Quản lý kho hàng'],['B5','Quản lý sản phẩm'],"
     "['B7','Tài khoản admin']];"),

    # B5 cũng nằm trong khung quản trị.
    ("const adminOn = ['B2','B3','B4'].includes(s.screen);",
     "const adminOn = ['B2','B3','B4','B5','B6','B7'].includes(s.screen);"),

    ("isB3: s.screen === 'B3', isB4: s.screen === 'B4',",
     "isB3: s.screen === 'B3', isB4: s.screen === 'B4', "
     "isB5: s.screen === 'B5', isB6: s.screen === 'B6', isB7: s.screen === 'B7',"),

    # 7.9.4 — nhãn trạng thái duyệt hiện rõ số lượt: 0/2 · 1/2 · 2/2.
    ("      pending: ['rgba(255,165,0,.15)', '#a36400', 'Chờ duyệt'],",
     "      pending: ['rgba(255,165,0,.15)', '#a36400', 'Chờ duyệt (0/2)'],"),
    ("      specialist_approved: ['rgba(255,165,0,.15)', '#a36400', 'Chờ Head Admin duyệt'],",
     "      specialist_approved: ['rgba(255,165,0,.15)', '#a36400', 'Chờ Head Admin (1/2)'],"),
    ("      approved: ['rgba(0,173,238,.14)', '#00728f', 'Đã duyệt'],",
     "      approved: ['rgba(0,173,238,.14)', '#00728f', 'Đã duyệt (2/2)'],"),

    # 7.1.3 — đã mua hàng nhưng chưa là agent thì đưa sang màn đăng ký,
    # mang theo dữ liệu đơn cũ để autofill (khớp luôn 7.2.8).
    ("""      agentLoginSubmit: () => {
        if (s.agentPhone.trim() && s.agentPassword === '123456') { GO('A3'); }
        else { this.setState({ agentLoginError: true, agentLoginStep: 'otp' }); }
      },""",
     """      agentLoginSubmit: () => {
        const ph = s.agentPhone.trim();
        const boughtOrder = this.ORDERS_BY_PHONE[ph];
        const isAgent = this.REGISTERED_PHONES.includes(ph);
        if (boughtOrder && !isAgent) {
          GO('A2', { regStep: 1, orderId: boughtOrder.orderId,
            buyerName: boughtOrder.buyerName, buyerPhone: ph, buyerEmail: boughtOrder.buyerEmail,
            buyerCccd: boughtOrder.buyerCccd, buyerAddress: boughtOrder.buyerAddress,
            buyerDob: boughtOrder.buyerDob });
          return;
        }
        if (ph && s.agentPassword === '123456') { GO('A3'); }
        else { this.setState({ agentLoginError: true, agentLoginStep: 'otp' }); }
      },"""),

    # Badge cho vòng đời đơn hàng (khác badge rút tiền: 'paid' đã dùng cho chi trả).
    ("      activated: ['rgba(0,173,238,.14)', '#00728f', 'Đã kích hoạt']",
     "      activated: ['rgba(0,173,238,.14)', '#00728f', 'Đã kích hoạt'],\n"
     "      order_pending: ['rgba(255,165,0,.15)', '#a36400', 'Chờ đối soát'],\n"
     "      order_confirmed1: ['rgba(255,165,0,.15)', '#a36400', 'Chờ Head Admin xác nhận'],\n"
     "      order_paid: ['rgba(132,190,82,.14)', '#4c7a2e', 'Đã thanh toán · đã cấp mã'],\n"
     "      order_rejected: ['rgba(217,52,43,.12)', '#D9342B', 'Từ chối']"),

    # Khởi tạo dữ liệu đơn hàng.
    ("    if (!this.state.stockData) this.setState({ stockData: this.makeStock() });",
     "    if (!this.state.stockData) this.setState({ stockData: this.makeStock() });\n"
     "    if (!this.state.ordersData) this.setState({ ordersData: this.makeOrders() });"),

    # Dữ liệu sản phẩm + đơn hàng (mockup KH không có 2 màn này).
    ("  componentDidMount() {",
     """  ORDER_FILTERS = [['all','Tất cả'],['order_pending','Chờ đối soát'],['order_confirmed1','Chờ Head Admin'],['order_paid','Đã thanh toán'],['order_rejected','Từ chối']];

  makeOrders() {
    const raw = [
      { id:'DH923983', buyer:'Nguyễn Văn A', phone:'0901111111', email:'nguyenvana@gmail.com',
        address:'12 Nguyễn Huệ, Phường Bến Nghé, TP. Hồ Chí Minh',
        pkg:'Gói 1 năm · CN02', amountNum:10000000, referrer:'Trần Thị Bích', refCode:'923983',
        date:'03/09/2026 09:12', status:'order_pending', proof:'bill-DH923983.jpg', activationCode:null,
        auditLog:[{label:'Khách tạo đơn', actor:'Hệ thống', time:'03/09/2026 09:12'},
                  {label:'Khách tải ảnh chuyển khoản', actor:'Nguyễn Văn A', time:'03/09/2026 09:20'}] },
      { id:'DH100511', buyer:'Lý Thị Hoa', phone:'0902222222', email:'lythihoa@gmail.com',
        address:'45 Lê Lợi, Phường Bến Thành, TP. Hồ Chí Minh',
        pkg:'Gói nửa năm · CN02-6M', amountNum:6000000, referrer:'Lê Văn Cường', refCode:'118820',
        date:'02/09/2026 15:40', status:'order_confirmed1', proof:'bill-DH100511.jpg', activationCode:null,
        auditLog:[{label:'Khách tạo đơn', actor:'Hệ thống', time:'02/09/2026 15:40'},
                  {label:'Khách tải ảnh chuyển khoản', actor:'Lý Thị Hoa', time:'02/09/2026 15:52'},
                  {label:'Admin Specialist xác nhận tiền về (chờ Head Admin)', actor:'Admin Specialist', time:'02/09/2026 16:30'}] },
      { id:'DH100234', buyer:'Đỗ Anh Tuấn', phone:'0903333333', email:'doanhtuan@gmail.com',
        address:'88 Trần Hưng Đạo, Phường Cầu Ông Lãnh, TP. Hồ Chí Minh',
        pkg:'Gói 1 năm · CN02', amountNum:10000000, referrer:'Vũ Minh Khang', refCode:'552017',
        date:'30/08/2026 08:05', status:'order_paid', proof:'bill-DH100234.jpg', activationCode:'ACT-100481',
        auditLog:[{label:'Khách tạo đơn', actor:'Hệ thống', time:'30/08/2026 08:05'},
                  {label:'Khách tải ảnh chuyển khoản', actor:'Đỗ Anh Tuấn', time:'30/08/2026 08:19'},
                  {label:'Admin Specialist xác nhận tiền về (chờ Head Admin)', actor:'Admin Specialist', time:'30/08/2026 09:10'},
                  {label:'Head Admin xác nhận & cấp mã kích hoạt ACT-100481', actor:'Head Admin', time:'30/08/2026 10:02'}] },
      { id:'DH100088', buyer:'Ngô Thị Em', phone:'0904444444', email:'ngothiem@gmail.com',
        address:'7 Nguyễn Trãi, Phường Bến Thành, TP. Hồ Chí Minh',
        pkg:'Gói 1 năm · CN02', amountNum:10000000, referrer:'Lê Văn Cường', refCode:'118820',
        date:'28/08/2026 11:30', status:'order_paid', proof:'bill-DH100088.jpg', activationCode:'ACT-100337',
        auditLog:[{label:'Khách tạo đơn', actor:'Hệ thống', time:'28/08/2026 11:30'},
                  {label:'Head Admin xác nhận & cấp mã kích hoạt ACT-100337', actor:'Head Admin', time:'28/08/2026 14:00'}] },
      { id:'DH100012', buyer:'Phạm Quốc Bảo', phone:'0905555555', email:'pqbao@gmail.com',
        address:'201 Cách Mạng Tháng 8, Phường Hoà Hưng, TP. Hồ Chí Minh',
        pkg:'Gói nửa năm · CN02-6M', amountNum:6000000, referrer:'Trần Thị Bích', refCode:'923983',
        date:'26/08/2026 19:12', status:'order_rejected', proof:'bill-DH100012.jpg', activationCode:null,
        auditLog:[{label:'Khách tạo đơn', actor:'Hệ thống', time:'26/08/2026 19:12'},
                  {label:'Từ chối: số tiền chuyển khoản không khớp', actor:'Admin Specialist', time:'27/08/2026 09:00'}] }
    ];
    return raw.map(o => ({ ...o, amount: o.amountNum.toLocaleString('vi-VN') + 'đ' }));
  }

  ADMIN_USERS = [
    { id:1, name:'Trần Quốc Head', email:'head@homi365.com.vn', role:'head', status:'active' },
    { id:2, name:'Hoàng Thị Mỹ Trinh', email:'trinh@homi365.com.vn', role:'head', status:'active' },
    { id:3, name:'Nguyễn Thu Hà', email:'ha.nt@homi365.com.vn', role:'specialist', status:'active' },
    { id:4, name:'Lê Minh Quân', email:'quan.lm@homi365.com.vn', role:'specialist', status:'active' },
    { id:5, name:'Phạm Bảo Ngọc', email:'ngoc.pb@homi365.com.vn', role:'specialist', status:'locked' }
  ];

  ORDER_RANGES = [['today','Hôm nay'],['week','Tuần này'],['month','Tháng này'],['all','Tất cả']];
  ORDER_RANGE_VALUES = { today:'0', week:'3', month:'10', all:'27' };
  ORDER_RANGE_VALUES_NEW = { today:'0', week:'0', month:'1', all:'1' };

  RANK_HISTORY = {
    1: [{ label:'Thăng hạng Đồng → Bạc', time:'01/09/2026' },
        { label:'Tham gia · hạng Đồng', time:'12/08/2026' }],
    5: [{ label:'Thăng hạng Bạc → Vàng', time:'01/09/2026' },
        { label:'Thăng hạng Đồng → Bạc', time:'20/08/2026' },
        { label:'Tham gia · hạng Đồng', time:'01/08/2026' }],
    3: [{ label:'Giáng hạng Bạc → Đồng · 0 đơn trong tháng', time:'01/09/2026' },
        { label:'Tham gia · hạng Đồng', time:'22/08/2026' }]
  };

  PRODUCTS = [
    { id: 'CN02', sku: 'CN02', name: 'Gói Bác sĩ 24/7 · License 12 tháng · kèm đồng hồ HW01',
      imageLabel: 'cn02-12m.png',
      desc: 'Gói dịch vụ cao cấp gồm 01 đồng hồ thông minh HW01 theo dõi nhịp tim / SOS giao tận nơi và 01 năm phần mềm Bác sĩ 24/7 (mã kích hoạt gửi qua SMS).' },
    { id: 'CN02-6M', sku: 'CN02-6M', name: 'Gói Bác sĩ 24/7 · License 6 tháng · kèm đồng hồ HW01',
      imageLabel: 'cn02-6m.png',
      desc: 'Phiên bản nửa năm của gói CN02, cùng đồng hồ HW01 và đầy đủ tính năng theo dõi sức khoẻ.' }
  ];

  componentDidMount() {"""),

    # Tính toán cho màn Đơn hàng, đặt ngay trước khối return của renderVals.
    ("    return {\n      nav, adminNav,",
     """    // Đơn hàng (B6) — bổ sung, không có trong mockup KH
    const ordersRaw = s.ordersData || [];
    const orderRows = ordersRaw
      .filter(o => (s.orderStatusFilter === 'all' || !s.orderStatusFilter) || o.status === s.orderStatusFilter)
      .filter(o => !s.orderSearch
        || o.id.toLowerCase().includes(s.orderSearch.toLowerCase())
        || o.buyer.toLowerCase().includes(s.orderSearch.toLowerCase())
        || o.phone.includes(s.orderSearch))
      .map(o => {
        const [bg, color, label] = this.badge(o.status);
        return { ...o, badgeBg: bg, badgeColor: color, statusLabel: label,
          onClick: () => this.setState({ selectedOrderId: o.id }) };
      });
    const selOrderRaw = s.selectedOrderId ? ordersRaw.find(o => o.id === s.selectedOrderId) : null;
    let selectedOrder = null;
    if (selOrderRaw) {
      const [obg, ocolor, olabel] = this.badge(selOrderRaw.status);
      const isSpecO = s.adminRole === 'specialist';
      const canConfirmO = (isSpecO && selOrderRaw.status === 'order_pending')
        || (!isSpecO && selOrderRaw.status === 'order_confirmed1');
      const canRejectO = ['order_pending', 'order_confirmed1'].includes(selOrderRaw.status);
      selectedOrder = { ...selOrderRaw, badgeBg: obg, badgeColor: ocolor, statusLabel: olabel,
        activationCodeLabel: selOrderRaw.activationCode || '— chưa cấp —',
        canConfirm: canConfirmO, canReject: canRejectO, canAct: canConfirmO || canRejectO,
        needsCodePick: canConfirmO && !isSpecO,
        isRejected: selOrderRaw.status === 'order_rejected',
        confirmLabel: isSpecO ? 'Xác nhận tiền về (Specialist)'
                              : 'Xác nhận, cấp mã & kích hoạt tài khoản (Head Admin)',
        stageNote: selOrderRaw.status === 'order_pending'
          ? 'Đang chờ Admin Specialist đối soát tiền về (bước 1/2).'
          : selOrderRaw.status === 'order_confirmed1'
            ? 'Đã qua Specialist — chờ Head Admin xác nhận để cấp mã kích hoạt (bước 2/2).'
            : (selOrderRaw.status === 'order_rejected' ? 'Đơn đã bị từ chối.' : null),
        actHint: isSpecO
          ? 'Bạn đang ở vai Admin Specialist — chỉ xác nhận được bước 1 (tiền về). Bước 2 do Head Admin làm: chọn mã kích hoạt và kích hoạt tài khoản.'
          : 'Bạn đang ở vai Head Admin — chọn mã kích hoạt còn Sẵn hàng trong kho, xác nhận là hệ thống gán mã cho đơn, gửi cho khách và kích hoạt tài khoản.' };
    }

    return {
      nav, adminNav,"""),

    # Giá trị cho màn Quản lý sản phẩm + modal Thêm hàng vào kho.
    ("      hasActionModal: !!s.actionModal,",
     """      // 7.9.1 — Tài khoản admin
      adminUsers: this.ADMIN_USERS.map(u => {
        const locked = (s.adminUserLocks[u.id] || u.status) === 'locked';
        return { ...u,
          roleLabel: u.role === 'head' ? 'Head Admin' : 'Admin Specialist',
          roleBg: u.role === 'head' ? 'rgba(0,173,238,.14)' : 'rgba(170,170,170,.18)',
          roleColor: u.role === 'head' ? '#00728f' : '#5c5c5c',
          statusLabel: locked ? 'Đã khoá' : 'Đang hoạt động',
          badgeBg: locked ? 'rgba(170,170,170,.18)' : 'rgba(132,190,82,.14)',
          badgeColor: locked ? '#5c5c5c' : '#4c7a2e',
          lockLabel: locked ? 'Mở khoá' : 'Khoá',
          lockStyle: 'height:32px;padding:0 var(--s5);background:var(--c12);border-radius:var(--r-md);font-size:12px;font-weight:600;border:1px solid '
            + (locked ? 'var(--c6);color:var(--c6)' : '#D9342B;color:#D9342B'),
          onToggleLock: () => this.setState({ adminUserLocks: { ...s.adminUserLocks, [u.id]: locked ? 'active' : 'locked' } }),
          onEdit: () => this.setState({ showAdminUserForm: true, editingAdminUserId: u.id }) };
      }),
      adminUserCount: this.ADMIN_USERS.length,
      showAdminUserForm: s.showAdminUserForm,
      adminUserFormTitle: s.editingAdminUserId ? 'Sửa tài khoản admin' : 'Thêm tài khoản admin',
      adminUserFormName: (this.ADMIN_USERS.find(u => u.id === s.editingAdminUserId) || {}).name || '',
      adminUserFormEmail: (this.ADMIN_USERS.find(u => u.id === s.editingAdminUserId) || {}).email || '',
      openAdminUserForm: () => this.setState({ showAdminUserForm: true, editingAdminUserId: null }),
      closeAdminUserForm: () => this.setState({ showAdminUserForm: false, editingAdminUserId: null }),

      // 7.3.2 — lọc số đơn theo khoảng thời gian
      orderRanges: this.ORDER_RANGES.map(([id, label]) => ({
        id, label, onClick: () => this.setState({ orderRange: id }),
        style: 'font-size:12px;font-weight:600;padding:6px 14px;border-radius:30px;border:1px solid '
          + ((s.orderRange || 'month') === id ? '#00ADEE;background:rgba(0,173,238,.08);color:#00ADEE'
                                              : 'rgba(170,170,170,.4);background:transparent;color:var(--c5)')
      })),

      // Hai link của agent: ref_code (giới thiệu) và alias (mua hàng cá nhân).
      refCode: '923983',
      refLink: 'homi365.vn/san-pham/CN02?aff_id=923983',
      personalLink: 'homi365.com.vn/NVA1111',
      copyPersonalLabel: s.copyPersonalLabel,
      copyPersonalLink: () => {
        navigator.clipboard.writeText('homi365.com.vn/NVA1111');
        this.setState({ copyPersonalLabel: 'Đã copy!' });
        setTimeout(() => this.setState({ copyPersonalLabel: 'Copy link' }), 1500);
      },

      orderTotal: (s.ordersData || []).length,
      orderPendingCount: (s.ordersData || []).filter(o => o.status === 'order_pending').length,
      orderConfirm1Count: (s.ordersData || []).filter(o => o.status === 'order_confirmed1').length,
      orderPaidCount: (s.ordersData || []).filter(o => o.status === 'order_paid').length,
      orderRevenue: (s.ordersData || []).filter(o => o.status === 'order_paid')
        .reduce((t, o) => t + o.amountNum, 0).toLocaleString('vi-VN') + 'đ',
      orderSearch: s.orderSearch,
      setOrderSearch: (e) => this.setState({ orderSearch: e.target.value }),
      orderFilters: this.ORDER_FILTERS.map(([id, label]) => ({
        id, label, onClick: () => this.setState({ orderStatusFilter: id }),
        style: 'height:34px;padding:0 14px;border-radius:30px;font-size:12px;font-weight:600;border:1px solid ' +
          ((s.orderStatusFilter || 'all') === id ? '#00ADEE;background:rgba(0,173,238,.08);color:#00ADEE'
                                                 : 'rgba(170,170,170,.4);background:transparent;color:var(--c5)')
      })),
      orders: orderRows, ordersEmpty: orderRows.length === 0,
      hasSelectedOrder: !!selectedOrder, selectedOrder,
      closeOrder: () => this.setState({ selectedOrderId: null }),
      availableStockCodes: stockData.filter(p => p.status === 'available').slice(0, 60)
        .map(p => ({ code: p.activationCode, sku: p.sku,
                     label: p.activationCode + '  ·  ' + p.sku })),
      availableStockCount: stockData.filter(p => p.status === 'available').length,
      orderActivationCode: s.orderActivationCode,
      setOrderActivationCode: (e) => this.setState({ orderActivationCode: e.target.value, orderCodeError: '' }),
      orderCodeError: s.orderCodeError,
      confirmOrder: () => {
        const o = (s.ordersData || []).find(x => x.id === s.selectedOrderId);
        if (!o) return;
        const isSpec = s.adminRole === 'specialist', now = '08/09/2026 10:00';
        // Bước 1: Specialist xác nhận tiền về. Bước 2: Head Admin chọn mã kích
        // hoạt còn Sẵn hàng trong kho, gán vào đơn và kích hoạt tài khoản.
        if (!isSpec) {
          const code = s.orderActivationCode;
          if (!code) { this.setState({ orderCodeError: 'Chọn mã kích hoạt từ kho trước khi xác nhận.' }); return; }
          const item = stockData.find(p => p.activationCode === code && p.status === 'available');
          if (!item) { this.setState({ orderCodeError: 'Mã ' + code + ' không còn ở trạng thái Sẵn hàng.' }); return; }
          this.setState({
            ordersData: s.ordersData.map(x => x.id === o.id
              ? { ...x, status: 'order_paid', activationCode: code,
                  auditLog: [...x.auditLog, { label: 'Head Admin xác nhận thanh toán, cấp mã ' + code + ' và kích hoạt tài khoản', actor: 'Head Admin', time: now }] }
              : x),
            stockData: stockData.map(p => p.activationCode === code
              ? { ...p, status: 'assigned', orderId: o.id, seller: o.referrer,
                  log: [...p.log, { label: 'Gán cho đơn ' + o.id, time: now }] }
              : p),
            orderActivationCode: '', orderCodeError: ''
          });
          return;
        }
        this.setState({ ordersData: s.ordersData.map(x => x.id === o.id
          ? { ...x, status: 'order_confirmed1',
              auditLog: [...x.auditLog, { label: 'Admin Specialist xác nhận tiền về (chờ Head Admin)', actor: 'Admin Specialist', time: now }] }
          : x) });
      },
      rejectOrder: () => {
        const now = '08/09/2026 10:05';
        const actor = s.adminRole === 'specialist' ? 'Admin Specialist' : 'Head Admin';
        this.setState({ ordersData: s.ordersData.map(x => x.id === s.selectedOrderId
          ? { ...x, status: 'order_rejected',
              auditLog: [...x.auditLog, { label: 'Từ chối đơn', actor, time: now }] }
          : x) });
      },

      products: this.PRODUCTS.map(p => ({ ...p,
        onEdit: () => this.setState({ showProductForm: true, editingProductId: p.id }) })),
      productCount: this.PRODUCTS.length,
      showProductForm: s.showProductForm,
      productFormTitle: s.editingProductId ? 'Sửa sản phẩm' : 'Thêm sản phẩm',
      productFormName: (this.PRODUCTS.find(p => p.id === s.editingProductId) || {}).name || '',
      productFormDesc: (this.PRODUCTS.find(p => p.id === s.editingProductId) || {}).desc || '',
      openProductForm: () => this.setState({ showProductForm: true, editingProductId: null }),
      closeProductForm: () => this.setState({ showProductForm: false, editingProductId: null }),

      showAddStock: s.showAddStock,
      openAddStock: () => this.setState({ showAddStock: true, addStockSku: '', addStockCode: '', addStockError: '' }),
      closeAddStock: () => this.setState({ showAddStock: false }),
      addStockSku: s.addStockSku, setAddStockSku: (e) => this.setState({ addStockSku: e.target.value, addStockError: '' }),
      addStockCode: s.addStockCode, setAddStockCode: (e) => this.setState({ addStockCode: e.target.value, addStockError: '' }),
      addStockError: s.addStockError,
      submitAddStock: () => {
        const sku = (s.addStockSku || '').trim(), code = (s.addStockCode || '').trim();
        if (!sku || !code) { this.setState({ addStockError: 'Nhập đủ mã sản phẩm và mã kích hoạt.' }); return; }
        if (stockData.some(p => p.activationCode.toLowerCase() === code.toLowerCase())) {
          this.setState({ addStockError: 'Mã kích hoạt ' + code + ' đã có trong kho.' }); return; }
        if (stockData.some(p => p.sku.toLowerCase() === sku.toLowerCase())) {
          this.setState({ addStockError: 'Mã sản phẩm ' + sku + ' đã có trong kho.' }); return; }
        this.setState({
          stockData: [{ id: 900000 + stockData.length, sku, activationCode: code,
            orderId: '—', seller: '—', stockedAt: '08/09/2026', status: 'available',
            log: [{ label: 'Nhập kho (thủ công)', time: '08/09/2026 10:00' }] }, ...stockData],
          showAddStock: false, addStockError: ''
        });
      },

      showImportStock: s.showImportStock,
      openImportStock: () => this.setState({ showImportStock: true, importText: '', importResult: null }),
      closeImportStock: () => this.setState({ showImportStock: false }),
      importText: s.importText, setImportText: (e) => this.setState({ importText: e.target.value }),
      importResult: s.importResult, hasImportResult: !!s.importResult,
      runImportStock: () => {
        // Nhập từng phần: dòng nào hợp lệ thì nhận, dòng trùng hoặc thiếu dữ
        // liệu thì bỏ qua và liệt kê lý do. Chặn trùng cả với kho hiện có lẫn
        // trùng nhau trong chính danh sách đang dán.
        const lines = (s.importText || '').split('\\n').map(l => l.trim()).filter(Boolean);
        const seenCode = new Set(stockData.map(p => p.activationCode.toLowerCase()));
        const seenSku = new Set(stockData.map(p => p.sku.toLowerCase()));
        const added = [], skipped = [];
        lines.forEach((line, i) => {
          const parts = line.split(/[,;\\t]+/).map(x => x.trim());
          const sku = parts[0], code = parts[1];
          if (!sku || !code) { skipped.push({ line, reason: 'Thiếu mã sản phẩm hoặc mã kích hoạt' }); return; }
          if (seenCode.has(code.toLowerCase())) { skipped.push({ line, reason: 'Trùng mã kích hoạt' }); return; }
          if (seenSku.has(sku.toLowerCase())) { skipped.push({ line, reason: 'Trùng mã sản phẩm' }); return; }
          seenCode.add(code.toLowerCase()); seenSku.add(sku.toLowerCase());
          added.push({ id: 950000 + i, sku, activationCode: code, orderId: '—', seller: '—',
            stockedAt: '08/09/2026', status: 'available',
            log: [{ label: 'Nhập kho (import hàng loạt)', time: '08/09/2026 10:00' }] });
        });
        this.setState({
          stockData: [...added, ...stockData],
          importResult: { total: lines.length, ok: added.length, skip: skipped.length,
            hasSkipped: skipped.length > 0, skipped: skipped.slice(0, 30) }
        });
      },

      hasActionModal: !!s.actionModal,"""),
]

# ============================================================================

# Thanh trên giờ chỉ còn logo, nên logo phải đủ lớn để không bị lọt thỏm.
# Đổi 2 số này là đổi được cả chiều cao thanh.
LOGO_H = 40           # px — chiều cao ảnh logo
BAR_PAD_Y = 16        # px trên/dưới (mockup gốc là --s5 = 12px)
BAR_H = BAR_PAD_Y * 2 + LOGO_H + 1        # +1 = đường kẻ dưới
CONTENT_MAX = 1160    # px — bằng khung nội dung màn A1, để logo thẳng hàng

LOGO_HTML = (
    '<a href="../index.html" title="Danh sách màn hình" '
    'style="display:flex;align-items:center;text-decoration:none">'
    '<img src="../assets/logo homi-01.png" alt="HOMI365" '
    'style="height:%dpx;width:auto;display:block"></a>' % LOGO_H
)

# Nút "Đăng nhập Agent" ở góc phải thanh trên — chỉ hiện trên màn công khai
# (A1 mua hàng, A2 đăng ký). Không hiện ở C1 vì đang đứng sẵn ở đó, không hiện
# ở A3 vì đã đăng nhập, không hiện ở khung quản trị.
LOGIN_BTN = (
    '<a href="c1-login.html" style="margin-left:auto;display:inline-flex;'
    'align-items:center;gap:var(--s3);height:38px;padding:0 var(--s6);'
    # Viền dùng đúng màu viền chung của mockup (ô nhập, nút phụ như "Xuất CSV")
    # để thanh trên không lệch tông với phần bên dưới.
    'border:1px solid rgba(170,170,170,.6);border-radius:var(--r-md);color:var(--c6);'
    'background:var(--c12);font-size:14px;font-weight:600;text-decoration:none"'
    ' style-hover="background:rgba(170,170,170,.08)">Đăng nhập Agent</a>'
)


def drop_district(html):
    """Bỏ ô 'Quận/Huyện' khỏi hàng địa chỉ, đưa hàng từ 3 cột về 2 cột.

    Từ 01/07/2025 Việt Nam bỏ cấp huyện, địa chỉ hành chính chỉ còn
    tỉnh/thành -> phường/xã. Mockup KH soạn trước mốc này nên vẫn còn ô huyện.
    """
    ls = html.split("\n")
    out, i, n = [], 0, 0
    while i < len(ls):
        # A1 ghi "Quận/Huyện (*)", A2 ghi "Quận/Huyện" — bắt cả hai.
        if re.search(r">Quận/Huyện( \(\*\))?</label>", ls[i]):
            # 3 dòng: <div><label>, <sc-raw-select>, </div>
            if "sc-raw-select" not in ls[i + 1] or ls[i + 2].strip() != "</div>":
                die("khối Quận/Huyện không đúng dạng 3 dòng như dự kiến")
            i += 3
            n += 1
            continue
        out.append(ls[i])
        i += 1
    if n:
        for k, l in enumerate(out):
            out[k] = l.replace("grid-template-columns:1fr 1fr 1fr",
                               "grid-template-columns:1fr 1fr")
    return "\n".join(out), n


def die(msg):
    sys.exit("LỖI: " + msg)


def main():
    if not SRC.exists():
        die("chưa có %s — chạy extract-bundle.py trước." % SRC)

    text = SRC.read_text(encoding="utf-8")
    lines = text.split("\n")

    def seg(a, b):
        """Lấy các dòng a..b (1-based, bao gồm cả hai đầu)."""
        return "\n".join(lines[a - 1:b])

    # --- cắt khối <sc-if> theo cặp thẻ, không đoán dòng kết thúc ----------
    def block(start_line):
        start_off = sum(len(l) + 1 for l in lines[:start_line - 1])
        i = text.find("<sc-if", start_off)
        if i < 0:
            die("không tìm thấy <sc-if> sau dòng %d" % start_line)
        depth, j = 0, i
        while True:
            no = text.find("<sc-if", j)
            nc = text.find("</sc-if>", j)
            if nc < 0:
                die("thiếu </sc-if> cho khối ở dòng %d" % start_line)
            if 0 <= no < nc:
                depth += 1
                j = no + 6
            else:
                depth -= 1
                j = nc + 8
                if depth == 0:
                    return text[start_off:j]

    # --- CSS -------------------------------------------------------------
    (V3 / "css").mkdir(parents=True, exist_ok=True)
    (V3 / "css" / "fonts").mkdir(exist_ok=True)
    (V3 / "js").mkdir(exist_ok=True)
    (V3 / "screens").mkdir(exist_ok=True)

    fonts_css = seg(*L_FONTS).replace('url("res/', 'url("fonts/')
    fonts_css = re.sub(r"^\s*<style>", "", fonts_css)   # dòng 12 dính thẻ mở
    (V3 / "css" / "fonts.css").write_text(
        "/* Nunito + Roboto — trích nguyên xi từ mockup KH, không đổi. */\n" + fonts_css,
        encoding="utf-8")

    (V3 / "css" / "base.css").write_text(
        "/* Reset — trích nguyên xi từ mockup KH. */\n" + seg(*L_BASE), encoding="utf-8")

    # --- tokens.css: bóc biến ra khỏi style inline của thẻ gốc ------------
    m = re.search(r'style="([^"]*)"', lines[L_ROOTDIV - 1])
    if not m:
        die("không đọc được style của thẻ gốc ở dòng %d" % L_ROOTDIV)
    decls = [d.strip() for d in m.group(1).split(";") if d.strip()]
    tokens = [d for d in decls if d.startswith("--")]
    rest = [d for d in decls if not d.startswith("--")]

    tok_lines = []
    for d in tokens:
        k, v = d.split(":", 1)
        nv = recolor(v.strip())
        note = ("   /* was %s */" % v.strip()) if nv != v.strip() else ""
        tok_lines.append("  %s: %s;%s" % (k.strip(), nv, note))

    (V3 / "css" / "tokens.css").write_text(
        "/* ============================================================\n"
        "   HOMI365 · prototype-v3 — bảng màu\n"
        "   Tên biến giữ NGUYÊN của mockup KH, chỉ đổi giá trị.\n"
        "   Sinh tự động bởi tools/build-v3.py — đừng sửa tay,\n"
        "   sửa bảng COLORS trong script rồi chạy lại.\n"
        "   ============================================================ */\n"
        ":root {\n" + "\n".join(tok_lines) + "\n"
        "\n  /* Bổ sung: nền trang ấm của HOMI365 (prototype-v2 --warm-50).\n"
        "     Thẻ/card vẫn dùng --c12 trắng -> section xen kẽ ấm / trắng. */\n"
        "  --warm-50: " + WARM + ";\n"
        "\n  /* Bổ sung: màu cột biểu đồ — teal-500 của HOMI365.\n"
        "     Dùng teal thay navy để biểu đồ tách khỏi nút/link màu chính. */\n"
        "  --c-chart: " + CHART + ";\n}\n\n"
        "/* Vòng focus — mockup KH không có, thêm để đạt WCAG 2.4.7.\n"
        "   Không ảnh hưởng layout. */\n"
        ":where(a, button, input, select, textarea):focus-visible {\n"
        "  outline: 2px solid #0F7F96;\n"
        "  outline-offset: 2px;\n"
        "}\n", encoding="utf-8")

    root_open = ('<div style="%s">' % "; ".join(rest)).replace(
        "background:var(--c12)", "background:var(--warm-50)")

    # --- runtime + font ---------------------------------------------------
    js_src = [p for p in (RAW / "res").glob("*.js")]
    runtime = RAW / "res" / "d3a2f2c4-e44e-4524-ab01-ec4bd8675302.js"
    if not runtime.exists():
        die("thiếu runtime %s" % runtime.name)
    shutil.copy(runtime, V3 / "js" / "dc-runtime.js")
    n_font = 0
    for f in (RAW / "res").glob("*.woff2"):
        shutil.copy(f, V3 / "css" / "fonts" / f.name)
        n_font += 1

    # --- thanh trên: chỉ còn logo -----------------------------------------
    # Bỏ theo yêu cầu: chữ "Homi365 ●", dòng "WhiteCoat Việt Nam · 7 màn hình
    # MVP", và dãy nút chuyển màn A1…B4 (đó là khung điều khiển của bản mockup,
    # không thuộc sản phẩm). Giữ nguyên style của thẻ bọc để chiều cao và
    # đường kẻ dưới không đổi. Bấm logo -> về trang mục lục.
    wrap0 = lines[L_TOPBAR_WRAP - 1].strip()
    if not wrap0.startswith("<div style=\"position:sticky"):
        die("dòng %d không phải thẻ bọc thanh trên" % L_TOPBAR_WRAP)
    if "padding:var(--s5) var(--s8)" not in wrap0:
        die("không tìm thấy padding của thanh trên để nới")

    def make_topbar(pad_x, inner_max=None, right=""):
        """Thanh trên. pad_x quyết định logo thẳng hàng với cái gì."""
        w = wrap0.replace("padding:var(--s5) var(--s8)",
                          "padding:%dpx %s" % (BAR_PAD_Y, pad_x))
        if inner_max is None:
            return ("  " + w + "\n    " + LOGO_HTML +
                    (("\n    " + right) if right else "") + "\n  </div>")
        return ("  " + w + "\n"
                '    <div style="width:100%;max-width:' + str(inner_max) +
                'px;margin:0 auto;display:flex;align-items:center">\n'
                "      " + LOGO_HTML +
                (("\n      " + right) if right else "") +
                "\n    </div>\n  </div>")

    # Màn người mua / thành viên: nội dung nằm trong khung 1160px canh giữa,
    # đệm ngang var(--s7)=16px -> logo dùng đúng khung đó thì mép trái trùng nhau.
    TOPBAR_WEB = make_topbar("var(--s7)", CONTENT_MAX)
    TOPBAR_PUBLIC = make_topbar("var(--s7)", CONTENT_MAX, LOGIN_BTN)
    # Màn quản trị: bố cục tràn màn hình, sidebar đệm ngang var(--s5)=12px
    # -> logo canh theo mép trái của các mục sidebar.
    TOPBAR_ADMIN = make_topbar("var(--s5)")

    # --- JS ---------------------------------------------------------------
    script = seg(*L_SCRIPT)
    for old, new in JS_PATCHES:
        if old not in script:
            die("không khớp đoạn JS cần sửa:\n---\n%s\n---" % old[:120])
        script = script.replace(old, new, 1)

    # --- đổi màu toàn bộ ---------------------------------------------------
    TOPBAR_WEB = recolor(TOPBAR_WEB)
    TOPBAR_PUBLIC = recolor(TOPBAR_PUBLIC)
    TOPBAR_ADMIN = recolor(TOPBAR_ADMIN)
    script = recolor(script)
    def bg_patch(s):
        for old, new in BG_PATCHES:
            s = s.replace(old, new)
        return s

    blocks_html = {k: recolor(bg_patch(block(v))) for k, v in BLOCKS.items()}

    # Bỏ ô Quận/Huyện theo yêu cầu ngày 08/09.
    n_district = 0
    for k, v in blocks_html.items():
        blocks_html[k], n = drop_district(v)
        n_district += n

    # Thanh trên cao hơn trước -> sửa mọi phép trừ chiều cao cho khớp,
    # nếu không màn quản trị sẽ dư ra một thanh cuộn dọc.
    n_calc = 0
    for k, v in blocks_html.items():
        if "calc(100vh - 65px)" in v:
            n_calc += v.count("calc(100vh - 65px)")
            blocks_html[k] = v.replace("calc(100vh - 65px)",
                                       "calc(100vh - %dpx)" % BAR_H)

    files_js = json.dumps(FILES, ensure_ascii=False)

    # --- sinh từng màn -----------------------------------------------------
    n_nested = []
    for sc in SCREENS:
        # Một số khối (modal QR, ngăn chi tiết…) nằm LỒNG sẵn bên trong khối màn
        # hình chứ không phải anh em cùng cấp. Nối thêm sẽ ra 2 modal chồng nhau.
        # Bỏ khối nào đã là con của khối khác trong cùng danh sách.
        chosen = []
        for b in sc["blocks"]:
            if any(blocks_html[b] in blocks_html[o]
                   for o in sc["blocks"] if o != b):
                n_nested.append("%s/%s" % (sc["code"], b))
                continue
            chosen.append(b)
        body = "\n\n".join(blocks_html[b] for b in chosen)
        base_state = dict(sc["states"][0][2])
        base_state["screen"] = sc["code"]
        hash_map = {h: st for h, label, st in sc["states"] if h}

        head_js = (
            "window.__FILES = %s;\n"
            "window.__STATE__ = %s;\n"
            "// dữ liệu mang sang từ màn trước (bấm nút điều hướng)\n"
            "try { var c = sessionStorage.getItem('__homi_carry');\n"
            "      if (c) { Object.assign(window.__STATE__, JSON.parse(c)); "
            "sessionStorage.removeItem('__homi_carry'); } } catch (e) {}\n"
            "// mở thẳng một trạng thái: %s#%s\n"
            "var H = %s, h = location.hash.slice(1);\n"
            "if (H[h]) Object.assign(window.__STATE__, H[h]);\n"
            % (files_js, json.dumps(base_state, ensure_ascii=False),
               FILES[sc["code"]], (sc["states"][1][0] if len(sc["states"]) > 1 else "..."),
               json.dumps(hash_map, ensure_ascii=False))
        )

        page = (
            "<!DOCTYPE html>\n<html lang=\"vi\">\n<head>\n"
            "<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "<title>%s · HOMI365</title>\n"
            "<link rel=\"icon\" href=\"../assets/Icon_viewweb_final.jpg\">\n"
            "<meta name=\"theme-color\" content=\"#1E3A66\">\n"
            "<link rel=\"stylesheet\" href=\"../css/fonts.css\">\n"
            "<link rel=\"stylesheet\" href=\"../css/base.css\">\n"
            "<link rel=\"stylesheet\" href=\"../css/tokens.css\">\n"
            "<script>\n%s</script>\n"
            "<script src=\"../js/dc-runtime.js\"></script>\n"
            "</head>\n<body>\n<x-dc>\n<helmet data-dc-atomics=\"\"></helmet>\n"
            "%s\n\n%s\n\n%s\n\n</div>\n</x-dc>\n%s\n</body>\n</html>\n"
            % (sc["title"], head_js, root_open,
               TOPBAR_ADMIN if sc["code"] in ADMIN_CODES
               else TOPBAR_PUBLIC if sc["code"] in ("A1", "A2")
               else TOPBAR_WEB,
               body, script)
        )
        (V3 / "screens" / FILES[sc["code"]]).write_text(page, encoding="utf-8")

    # --- index -------------------------------------------------------------
    groups = {}
    for sc in SCREENS:
        groups.setdefault(sc["group"], []).append(sc)

    cards = []
    for gname, scs in groups.items():
        rows = []
        for sc in scs:
            links = []
            for h, label, _ in sc["states"]:
                href = "screens/%s%s" % (FILES[sc["code"]], ("#" + h) if h else "")
                links.append('<li><a href="%s">%s</a></li>' % (href, label))
            rows.append(
                '<div class="scr"><h3><a href="screens/%s">%s</a></h3><ul>%s</ul></div>'
                % (FILES[sc["code"]], sc["title"], "".join(links)))
        cards.append('<section><h2>%s</h2><div class="grid">%s</div></section>'
                     % (gname, "".join(rows)))

    n_states = sum(len(sc["states"]) for sc in SCREENS)
    index = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>HOMI365 · Prototype v3</title>
<link rel="icon" href="assets/Icon_viewweb_final.jpg">
<meta name="theme-color" content="#1E3A66">
<link rel="stylesheet" href="css/fonts.css">
<link rel="stylesheet" href="css/tokens.css">
<style>
  body{margin:0;font-family:'Roboto','Nunito',sans-serif;color:var(--c1);background:var(--warm-50)}
  *{box-sizing:border-box}
  header{background:#fff;border-bottom:1px solid rgba(154,163,176,.35);padding:16px 32px}
  header .inner{max-width:1100px;margin:0 auto;display:flex;align-items:center;
                gap:20px;flex-wrap:wrap}
  header img{height:40px}
  header .sub{font-size:13px;color:var(--c5);padding-left:16px;
              border-left:1px solid rgba(154,163,176,.35)}
  main{max-width:1100px;margin:0 auto;padding:32px}
  section{margin-bottom:36px}
  h2{font-size:15px;text-transform:uppercase;letter-spacing:.08em;color:var(--c5);
     font-weight:700;margin:0 0 14px}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}
  .scr{background:#fff;border:1px solid rgba(154,163,176,.3);border-radius:8px;padding:18px}
  .scr h3{margin:0 0 10px;font-size:16px}
  .scr h3 a{color:var(--c6);text-decoration:none}
  .scr h3 a:hover{text-decoration:underline}
  ul{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:6px}
  li a{font-size:13px;color:var(--c2);text-decoration:none;display:block;padding:5px 9px;
       border-radius:5px;background:rgba(30,58,102,.05)}
  li a:hover{background:rgba(30,58,102,.12);color:var(--c6)}
  footer{max-width:1100px;margin:0 auto;padding:0 32px 48px;font-size:13px;
         color:var(--c5);line-height:1.7}
</style>
</head>
<body>
<header>
  <div class="inner">
    <img src="assets/logo homi-01.png" alt="HOMI365">
    <div class="sub">Prototype v3 &middot; __NSCREEN__ màn hình &middot; __NSTATE__ trạng thái</div>
  </div>
</header>
<main>
__CARDS__
</main>
<footer>
  Dựng từ mockup của khách hàng, giữ nguyên toàn bộ layout và các trường nhập liệu.
  Chỉ đổi bảng màu theo nhận diện HOMI365 và thay logo.
  Mở trực tiếp bằng trình duyệt, không cần cài đặt gì.
</footer>
</body>
</html>
"""
    index = (index.replace("__CARDS__", "\n".join(cards))
                  .replace("__NSCREEN__", str(len(SCREENS)))
                  .replace("__NSTATE__", str(n_states)))
    (V3 / "index.html").write_text(index, encoding="utf-8")

    # --- báo cáo đổi màu ---------------------------------------------------
    all_out = "".join((V3 / "screens" / f).read_text(encoding="utf-8")
                      for f in FILES.values())
    left = sorted({c for c, _ in COLORS if c.startswith("#") and c in all_out})

    # Soát trùng: mỗi khối chỉ được xuất hiện đúng 1 lần trong mỗi file.
    dup = []
    for f in FILES.values():
        t = (V3 / "screens" / f).read_text(encoding="utf-8")
        for name, h in blocks_html.items():
            tag = h[h.find("<sc-if"):h.find(">", h.find("<sc-if")) + 1]
            if tag and t.count(tag) > 1:
                dup.append("%s: %s xuất hiện %d lần" % (f, name, t.count(tag)))

    diff = ["# DIFF — prototype-v3 so với mockup của khách hàng", "",
            "Sinh tự động bởi `tools/build-v3.py`. Ngoài 11 mục dưới đây, "
            "**không có thay đổi nào khác**: layout, khoảng cách, bo góc, font "
            "giữ nguyên 100%.", "",
            "## 1. Đổi giá trị màu", "",
            "| Màu cũ (mockup KH) | Màu mới (HOMI365) |", "|---|---|"]
    for old, new in COLORS:
        diff.append("| `%s` | `%s` |" % (old, new))
    diff += ["", "## 2. Màu giữ nguyên — logo bên thứ ba", "",
             "| Màu | Lý do |", "|---|---|"]
    for c, why in KEEP.items():
        diff.append("| `%s` | %s |" % (c, why))
    diff += ["", "## 3. Thanh trên", "",
             "Chữ `Homi365 ●` đổi thành ảnh logo chính thức "
             "(`assets/logo homi-01.png`), bấm vào về trang mục lục. "
             "Favicon dùng `assets/Icon_viewweb_final.jpg`.", "",
             "Bỏ hai thành phần vốn là khung điều khiển của bản mockup, "
             "không thuộc sản phẩm:", "",
             "- Dòng chú thích `WhiteCoat Việt Nam · 7 màn hình MVP`.",
             "- Dãy nút chuyển màn `A1 · Thông tin nhận hàng … B4 · Kho hàng`. "
             "Việc chuyển màn giờ nằm ở `index.html`.", "",
             "Vì thanh chỉ còn một phần tử, logo nâng lên %dpx và đệm dọc nới từ "
             "12px lên %dpx — thanh cao %dpx thay vì 65px. Mọi phép "
             "`calc(100vh - 65px)` trong mockup đã được sửa theo (%d chỗ) để màn "
             "quản trị không dư thanh cuộn." % (LOGO_H, BAR_PAD_Y, BAR_H, n_calc), "",
             "Thêm nút **Đăng nhập Agent** ở góc phải thanh trên, chỉ trên 2 màn "
             "công khai A1 và A2 (trỏ sang `c1-login.html`). Không đặt ở C1 vì "
             "đang đứng sẵn ở đó, không đặt ở A3 vì đã đăng nhập, không đặt ở "
             "khung quản trị. Đây là thành phần mới so với mockup KH — cần nêu "
             "khi gửi.", "",
             "Logo canh thẳng hàng với nội dung bên dưới: màn người mua và thành "
             "viên dùng chung khung %dpx canh giữa; màn quản trị canh theo mép "
             "trái các mục sidebar. Đây là thay đổi layout duy nhất của bản này, "
             "và chỉ ở thanh trên." % CONTENT_MAX, "",
             "## 4. Bỏ trường Quận/Huyện", "",
             "Hàng địa chỉ trong form mua hàng (A1) và form đăng ký (A2) đi từ "
             "**3 ô** `Tỉnh/Thành phố · Quận/Huyện · Phường/Xã` xuống **2 ô** "
             "`Tỉnh/Thành phố · Phường/Xã`. Đã bỏ %d ô, lưới đổi từ 3 cột sang "
             "2 cột." % n_district, "",
             "Đây là **thay đổi trường nhập liệu duy nhất** so với mockup KH — "
             "cần nêu rõ khi gửi, vì các trường còn lại đều giữ nguyên như đã "
             "duyệt. Lý do: từ 01/07/2025 Việt Nam bỏ cấp huyện, địa chỉ hành "
             "chính chỉ còn tỉnh/thành → phường/xã.", "",
             "Kéo theo: dữ liệu địa chỉ lưu xuống chỉ còn 2 cấp — cần thống nhất "
             "với dev trước khi thiết kế bảng, và chốt xem đơn hàng cũ (nếu có "
             "dữ liệu chuyển đổi) xử lý cấp huyện thế nào.", "",
             "## 5. Nền trang", "",
             "Nền trang đổi sang `--warm-50` = `%s` (lấy từ "
             "`prototype-v2/css/tokens.css`), thẻ và ô nhập giữ trắng `#FFFFFF` "
             "— tạo nhịp xen kẽ ấm / trắng thay vì trắng trên trắng." % WARM, "",
             "| Màn | Trước | Sau |", "|---|---|---|",
             "| A1 · C1 | `rgba(170,170,170,.05)` | `%s` |" % WARM,
             "| A3 | `#FFFFFF` | `%s` |" % WARM,
             "| A2 · B2 · B3 · B4 | `#FFFFFF` | `%s` |" % WARM,
             "| Thanh trên · thẻ · ô nhập | `#FFFFFF` | giữ nguyên |",
             "| B1 đăng nhập quản trị | `--c3` navy | giữ nguyên |", "",
             "Kéo theo: 30 thẻ trong mockup KH **chỉ khai báo viền, không khai "
             "báo nền** — trên nền trắng cũ thì không lộ, trên nền ấm sẽ bị chìm. "
             "Đã cho về trắng (A3 5 thẻ · B2/B3/B4 mỗi màn 8 · A2 1).", "",
             "Cột biểu đồ hoa hồng đổi sang teal `%s` để tách khỏi navy của "
             "nút và link — navy là màu hành động, teal là màu dữ liệu." % CHART, "",

             "## 6. Thêm link bán hàng vào A3", "",
             "Dashboard thành viên trong mockup KH **không có link bán hàng nào**. "
             "Agent rời màn \"Kích hoạt thành công\" (A2 bước 5) là mất đường lấy "
             "link, không có chỗ xem lại. Đã thêm thẻ **Link bán hàng của bạn** "
             "ngay dưới phần chào, gồm 1 link + nút copy, dùng lại đúng link và "
             "hàm `copyLink` sẵn có của A2 bước 5.", "",
             "**Đã chốt 08/09: 2 link**, đúng theo requirement 8.1.C-4 — agent "
             "nhận cả hai ngay lúc kích hoạt (A2 bước 5) và xem lại được ở "
             "dashboard (A3), mỗi link một nút copy riêng:", "",
             "| Link | Giá trị | Dùng để |", "|---|---|---|",
             "| Giới thiệu · ref_code | `homi365.vn/san-pham/CN02?aff_id=923983` | "
             "gán tuyến trên / tuyển thành viên |",
             "| Mua hàng cá nhân · alias | `homi365.com.vn/NVA1111` | "
             "chia sẻ để khách mua trực tiếp |", "",
             "`ref_code = 923983` là mã chính thức của agent. Alias sinh đúng cú "
             "pháp **8.1.C-4**: `Homi365.com.vn/[EEEE][PPPP]` — EEEE là chữ cái "
             "đầu (viết hoa, bỏ dấu) của mỗi từ trong họ tên, PPPP là 4 số cuối "
             "SĐT. *Nguyễn Văn A* · `0901111111` → `NVA1111`.", "",
             "Còn treo — **hai link của admin ở màn B2 chưa khớp mô hình này.** "
             "B2 hiện hiện *link form* `portal.homi365.com.vn/TTB4123` và *link "
             "đăng nhập* `homi365.com.vn/dang-nhap/TTB4123`, cả hai dựng từ alias "
             "chứ không có link mua hàng lẫn ref_code. Cần chốt admin nhìn thấy "
             "những link nào của agent, và 4 dạng link này rốt cuộc là mấy thứ "
             "khác nhau. Prototype giữ nguyên phần B2 như mockup KH.", "",

             "## 7. Tách hoa hồng theo trạng thái (A3)", "",
             "Thẻ số dư trong mockup KH chỉ có **2 con số** — khả dụng và \"đang "
             "chờ duyệt (đã khóa)\"; \"đã ghi nhận\" nằm lẫn trong một dòng chữ "
             "nhỏ, \"đã rút\" nằm tận ô chỉ số phía trên. Đã tách thành **4 mục**:",
             "",
             "| Mục | Giá trị mẫu |", "|---|---|",
             "| Đã ghi nhận | 6.000.000đ |",
             "| Đang chờ duyệt · tạm giữ | 800.000đ |",
             "| Đã rút | 1.200.000đ |",
             "| **Số dư khả dụng** | **4.000.000đ** |", "",
             "Số liệu mẫu khớp: `6.000.000 = 4.000.000 + 800.000 + 1.200.000`.", "",
             "Bổ sung dòng giải thích cơ chế hold: yêu cầu rút ở trạng thái **chờ "
             "duyệt** hoặc **đã duyệt** bị tạm giữ và trừ khỏi số dư khả dụng, tới "
             "khi chi trả xong hoặc bị từ chối; từ chối thì hoàn lại khả dụng.", "",
             "\"Đã rút\" hiển thị ở **2 nơi** — ô chỉ số phía trên (trường của "
             "mockup gốc) và thẻ hoa hồng này. **Đã chốt giữ cả hai** (BA quyết "
             "08/09): ô chỉ số cho cái nhìn nhanh, thẻ hoa hồng cho quan hệ giữa "
             "4 con số. Không phải lỗi trùng lặp.", "",

             "## 8. Bổ sung màn Quản lý sản phẩm (B5)", "",
             "Mockup KH không có màn này, dù requirement **7.7.1 Logic quản lý "
             "sản phẩm** là P0. Đã thêm màn `b5-products.html` trong khung quản "
             "trị, kèm mục **Quản lý sản phẩm** ở sidebar.", "",
             "Nội dung: bảng sản phẩm với 3 cột theo đúng yêu cầu — **Tên · Hình "
             "ảnh · Mô tả** — cùng nút *Thêm sản phẩm* và nút *Sửa* trên từng "
             "dòng, cả hai mở cùng một hộp thoại 3 trường.", "",
             "**Đã chốt 08/09** — phạm vi màn này đúng bằng 3 trường trên, không "
             "hơn: không quản lý giá và bảng hoa hồng ở đây (giữ nguyên ở màn "
             "Hạng), không có công tắc bật/tắt bán, mỗi sản phẩm **chỉ 1 ảnh**.",
             "",

             "## 9. Bổ sung Thêm hàng vào kho (B4)", "",
             "Màn Quản lý kho hàng của mockup KH **chỉ xem, không nhập được hàng** "
             "— 1.200 mã trong bản demo là dữ liệu dựng sẵn. Đã thêm nút **+ Thêm "
             "hàng vào kho** cạnh nút xuất Excel, mở hộp thoại 2 trường theo yêu "
             "cầu: **Mã sản phẩm** và **Mã kích hoạt**. Hàng thêm vào mặc định ở "
             "trạng thái *Sẵn hàng*.", "",
             "**Đã chốt 08/09** — thêm nút **Import hàng loạt** bên cạnh, mở hộp "
             "thoại cho chọn file Excel/CSV hoặc dán danh sách, mỗi dòng "
             "`mã sản phẩm, mã kích hoạt`.", "",
             "**Chặn trùng ở cả hai đường nhập:**", "",
             "- Nhập tay: trùng mã kích hoạt hoặc mã sản phẩm thì báo lỗi ngay "
             "trong hộp thoại, không cho lưu.",
             "- Import: xử lý **từng phần** — dòng nào hợp lệ thì nhận, dòng nào "
             "trùng hoặc thiếu dữ liệu thì bỏ qua. Kết thúc hiện bảng tổng kết "
             "`tổng dòng / đã nhập / bỏ qua` kèm danh sách dòng bị bỏ và lý do.",
             "- Chặn trùng tính cả với kho hiện có **lẫn trùng nhau trong chính "
             "danh sách đang dán** — dán 2 dòng cùng mã thì chỉ nhận dòng đầu.", "",

             "## 10. Bổ sung màn Quản lý đơn hàng (B6)", "",
             "Mockup KH **không có màn đơn hàng nào**, dù luồng mua của chính "
             "mockup là chuyển khoản + khách tự tải ảnh bill lên. Nghĩa là tiền "
             "về tài khoản nhưng không ai xác nhận được, đơn treo vĩnh viễn và "
             "khách không bao giờ nhận mã kích hoạt. Đây là mắt xích đứt, không "
             "phải tính năng phụ.", "",
             "Màn `b6-orders.html` gồm: 4 ô thống kê (chờ đối soát · chờ Head "
             "Admin · đã thanh toán · doanh thu đã đối soát), bộ lọc theo trạng "
             "thái, ô tìm theo mã đơn / tên / SĐT, bảng đơn, và ngăn chi tiết bên "
             "phải với thông tin khách, thông tin đơn, ảnh chuyển khoản, lịch sử "
             "xử lý và nút hành động.", "",
             "**Duyệt 2 cấp** (theo quyết định 08/09), giống luồng rút tiền:", "",
             "| Bước | Ai làm | Kết quả |", "|---|---|---|",
             "| 1 | Admin Specialist | Xác nhận tiền về → `Chờ Head Admin xác nhận` |",
             "| 2 | Head Admin | Xác nhận → `Đã thanh toán`, hệ thống cấp mã kích hoạt |",
             "| — | Cả hai vai | Từ chối đơn (khi tiền chưa về hoặc sai số tiền) |", "",
             "Nút bước 2 khoá với vai Specialist và ngược lại — đổi vai bằng nút "
             "*Vai trò (demo)* ở cuối sidebar để thử cả hai.", "",
             "**Đã chốt 08/09:**", "",
             "- **Tách vai theo bước, không tách theo người.** Specialist làm "
             "bước 1; bước 2 thuộc về Head Admin, và Head Admin làm luôn việc "
             "kích hoạt tài khoản. Khác luồng rút tiền ở chỗ rút tiền cấm cùng "
             "một người làm cả hai bước, còn ở đây phân quyền theo vai là đủ.",
             "- **Mã kích hoạt do Head Admin chọn tay** từ danh sách thả xuống, "
             "chỉ liệt kê mã đang ở trạng thái *Sẵn hàng* trong kho (B4). Không "
             "chọn thì không xác nhận được. Xác nhận xong mã đó chuyển sang *Đã "
             "gán đơn hàng* và ghi vào lịch sử của cả đơn lẫn thiết bị.",
             "- **Đơn bị từ chối là chấm dứt.** Phase 1 không mở lại đơn cũ; "
             "khách muốn mua thì đặt đơn mới qua link giới thiệu. Ngăn chi tiết "
             "hiển thị rõ dòng này để admin khỏi đi tìm nút mở lại.", "",
             "- **Hoàn tiền nằm ngoài hệ thống.** Đơn bị từ chối nhưng tiền đã "
             "về tài khoản thì bộ phận kế toán xử lý thủ công bên ngoài; hệ "
             "thống không có màn hoàn tiền, không lưu trạng thái hoàn tiền, "
             "không đối soát khoản hoàn. Dev không cần làm gì cho phần này.", "",

             "## 11. Bổ sung theo rà soát requirement 09/09", "",
             "Nguồn: `docs/GAP-Requirement-vs-prototype-v3.md`. Sáu mục nhóm B "
             "đã làm xong:", "",
             "| Mã YC | Bổ sung |", "|---|---|",
             "| **7.9.1** | Màn **B7 · Tài khoản admin** — danh sách 5 tài khoản "
             "mẫu, cột vai trò (Head Admin / Admin Specialist), khoá–mở khoá, "
             "thêm–sửa tài khoản, kèm bảng giải thích quyền của từng vai. |",
             "| **7.1.3** | Đăng nhập bằng SĐT **đã mua hàng nhưng chưa là "
             "agent** → tự chuyển sang màn đăng ký và autofill từ đơn cũ "
             "(khớp luôn 7.2.8). Thêm dòng gợi ý ngay dưới nút Đăng nhập. |",
             "| **7.5.2** | Thêm khối **Lịch sử thăng/giáng hạng** vào ngăn chi "
             "tiết thành viên. |",
             "| **7.5.2** | Cây tuyến mở rộng lên **3 cấp** F0 → F1 → F2. |",
             "| **7.3.2** | Dashboard thêm bộ chọn **Hôm nay / Tuần này / Tháng "
             "này / Tất cả**, số Tổng đơn hàng đổi theo. |",
             "| **7.9.4** | Nhãn trạng thái duyệt hiện rõ số lượt: **Chờ duyệt "
             "(0/2)** · **Chờ Head Admin (1/2)** · **Đã duyệt (2/2)**. |", "",
             "Chưa làm, chờ KH quyết — xem mục A3 của file rà soát: theo **7.9.2** "
             "agent đăng ký xong phải ở trạng thái *Chờ duyệt* chứ không vào thẳng "
             "dashboard như mockup KH. Sửa chỗ này kéo theo cả màn A2, luồng duyệt "
             "và cách tính hoa hồng lúc chờ, nên chưa đụng vào.", "",

             "## Ghi chú", "",
             "- Nút **Thanh toán** ở màn A1 trong mockup KH đang để nền đỏ `#EE0000` "
             "nhưng màu hover lại là cyan `#0099d1` — gần như chắc chắn là lỗi sót. "
             "Bản này đưa về màu chính. Cần KH xác nhận.",
             "- Điều hướng giữa các màn đổi từ `setState` sang chuyển file thật, "
             "vì mỗi màn giờ là một file `.html` riêng. Dữ liệu mang sang màn sau "
             "đi qua `sessionStorage`.",
             "- Thêm vòng focus bàn phím (WCAG 2.4.7) — không ảnh hưởng layout."]
    if left:
        diff += ["", "## ⚠ Còn sót màu cũ", ""] + ["- `%s`" % c for c in left]
    (V3 / "DIFF-vs-mockup-KH.md").write_text("\n".join(diff) + "\n", encoding="utf-8")

    # --- tổng kết ----------------------------------------------------------
    print("Xong.")
    print("  màn hình      : %d file trong screens/" % len(SCREENS))
    print("  trạng thái    : %d (mở bằng #hash, liệt kê ở index.html)" % n_states)
    print("  font chép     : %d" % n_font)
    print("  runtime       : js/dc-runtime.js (%.1f KB)"
          % (runtime.stat().st_size / 1024))
    print("  bỏ ô Quận/Huyện: %d chỗ" % n_district)
    print("  khối lồng sẵn, không nối thêm: %s"
          % (", ".join(n_nested) if n_nested else "không"))
    print("  còn sót màu cũ: %s" % (", ".join(left) if left else "không"))
    print("  khối bị trùng : %s" % ("; ".join(dup) if dup else "không"))
    print("")
    print("Mở: %s" % (V3 / "index.html"))


if __name__ == "__main__":
    main()
