# -*- coding: utf-8 -*-
"""
update_uat0210.py — các thay đổi giao diện sau buổi UAT 02/10/2026.

Nguồn yêu cầu: sheet "Plan Update" trong Google Sheet "[Homi] - Change Request".
Đợt 06/10 chỉ làm các mục KHÔNG bị chặn: 1, 2, 3, 4, 5, 6, 7, 10, 11, 22
(mục 16 và 19 không có gì phải sửa trên giao diện). Các mục còn lại chờ khách
hàng trả lời H2–H5 nên chưa đụng tới.

File này được `build-v3.py` nạp vào. Tách riêng để bảng vá cũ trong
`build-v3.py` giữ nguyên, và để gỡ cả đợt chỉ cần bỏ 6 lời gọi `uat.*`.

Khác hai bảng vá cũ ở hai điểm:

  * Neo là chuỗi ở ĐẦU RA CUỐI (đã đổi màu, đã đổi tên vai), không phải chuỗi
    trong mockup gốc — chạy sau cùng nên không sợ bản vá khác sửa mất neo.
  * Neo không khớp là DỪNG build, kể cả với markup. Bảng BG_PATCHES cũ im lặng
    khi trượt neo và đã từng làm thiếu cột mà build vẫn báo "Xong".
"""

# ============================================================================
# 0. TIỆN ÍCH
# ============================================================================

_INFO = ('font-size:12px;color:var(--c4);background:rgba(30,58,102,.07);'
         'border:1px solid rgba(30,58,102,.3);border-radius:var(--r-md);'
         'padding:var(--s4) var(--s5);line-height:1.6')
_INP = ('height:44px;padding:0 var(--s5);border:1px solid rgba(154,163,176,.6);'
        'border-radius:var(--r-md);font-size:14px')
_FOCUS = 'border-color:#1E3A66;box-shadow:0 0 0 3px rgba(30,58,102,.25)'
_BTN_P = ('height:44px;background:var(--c6);color:var(--c12);border:none;'
          'border-radius:var(--r-md);font-size:15px;font-weight:600')
_BTN_G = ('height:44px;background:var(--c12);color:var(--c2);'
          'border:1px solid rgba(154,163,176,.6);border-radius:var(--r-md);'
          'font-size:15px;font-weight:600')
_HOVER_P = 'background:#1B3358'
_HOVER_G = 'background:rgba(154,163,176,.08)'
_OVERLAY = ('position:fixed;inset:0;background:rgba(43,48,58,.5);display:flex;'
            'align-items:center;justify-content:center;z-index:250;'
            'padding:var(--s7)')


# ============================================================================
# 1. MARKUP
# ============================================================================

# ---- Mục 1: bước nhập SĐT trước form mua hàng (A1) ------------------------
A1_PHONE_STEP = """  <!-- (20) BƯỚC 0: nhập SĐT trước form mua hàng — bổ sung sau UAT 02/10 -->
  <sc-if value="{{isA1Phone}}" hint-placeholder-val="{{false}}">
  <div style="min-height:calc(100vh - 104px);display:flex;justify-content:center;align-items:center;background:var(--warm-50);padding:var(--s10) var(--s7)">
    <div style="width:100%;max-width:420px;background:var(--c12);border:1px solid rgba(154,163,176,.35);border-radius:var(--r-lg);padding:var(--s10);box-shadow:0 8px 30px rgba(0,0,0,.1);display:flex;flex-direction:column;gap:var(--s7)">
      <div><div style="font-size:22px;font-weight:700;color:var(--c1);line-height:1.4">Mua gói CN02</div><div style="font-size:13px;color:var(--c5);margin-top:var(--s2);line-height:1.6">Nhập số điện thoại để bắt đầu. Nếu bạn đã có tài khoản HOMI365, đăng nhập để không phải điền lại thông tin.</div></div>
      <div style="display:flex;flex-direction:column;gap:var(--s2)">
        <label style="font-size:14px;font-weight:600;color:var(--c2)">Số điện thoại (*)</label>
        <input type="text" inputmode="numeric" maxlength="10" placeholder="090xxxxxxx" value="{{buyPhoneInput}}" sc-camel-on-change="{{setBuyPhoneInput}}" style="height:44px;padding:0 var(--s5);border:1px solid {{buyPhoneBorder}};border-radius:var(--r-md);font-size:16px" style-focus=\"""" + _FOCUS + """\">
        <sc-if value="{{buyPhoneError}}" hint-placeholder-val="{{false}}">
          <div style="font-size:12px;color:var(--err)">{{buyPhoneError}}</div>
        </sc-if>
      </div>
      <sc-if value="{{buyPhoneAsk}}" hint-placeholder-val="{{true}}">
        <button sc-camel-on-click="{{submitBuyPhone}}" style=\"""" + _BTN_P + """;box-shadow:var(--sh)" style-hover=\"""" + _HOVER_P + """\">Tiếp tục</button>
      </sc-if>
      <sc-if value="{{buyPhoneFound}}" hint-placeholder-val="{{false}}">
        <div style="border:1px solid rgba(30,58,102,.3);background:rgba(30,58,102,.06);border-radius:var(--r-md);padding:var(--s6);display:flex;flex-direction:column;gap:var(--s3)">
          <div style="font-size:14px;font-weight:700;color:var(--c1)">Số điện thoại này đã có tài khoản HOMI365</div>
          <div style="font-size:13px;color:var(--c2);line-height:1.6">Đăng nhập để form tự điền theo đơn gần nhất của bạn. Bạn cũng có thể bỏ qua và tự điền như bình thường.</div>
        </div>
        <div style="display:flex;flex-direction:column;gap:var(--s3)">
          <button sc-camel-on-click="{{buyGoLogin}}" style=\"""" + _BTN_P + """;box-shadow:var(--sh)" style-hover=\"""" + _HOVER_P + """\">Đăng nhập</button>
          <button sc-camel-on-click="{{buySkipLogin}}" style=\"""" + _BTN_G + """\" style-hover=\"""" + _HOVER_G + """\">Bỏ qua và tự điền</button>
          <button sc-camel-on-click="{{buyResetPhone}}" style="background:none;border:none;font-size:13px;font-weight:600;color:var(--c6);padding:var(--s2)">Dùng số điện thoại khác</button>
        </div>
      </sc-if>
    </div>
  </div>
  </sc-if>

"""

# ---- Mục 2: dòng nhắc tự điền + "Mua cho người khác" (A1) -----------------
A1_AUTOFILL_NOTE = """
          <sc-if value="{{buyIsSelf}}" hint-placeholder-val="{{false}}">
            <div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:var(--s4);""" + _INFO + """\"><div style="flex:1;min-width:200px">Đã điền theo đơn ngày <strong>{{buyProfileDate}}</strong> ({{buyProfileOrder}}). Bạn sửa trực tiếp được nếu thông tin đã thay đổi.</div><button sc-camel-on-click="{{buyForOther}}" style="flex:none;height:32px;padding:0 var(--s5);background:var(--c12);border:1px solid #1E3A66;border-radius:var(--r-sm);font-size:12px;font-weight:700;color:#1E3A66;white-space:nowrap">Mua cho người khác</button></div>
          </sc-if>
          <sc-if value="{{buyIsOther}}" hint-placeholder-val="{{false}}">
            <div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:var(--s4);""" + _INFO + """\"><div style="flex:1;min-width:200px">Đang nhập thông tin cho <strong>người khác</strong>. Phần tự điền đã được xoá.</div><button sc-camel-on-click="{{buyForSelf}}" style="flex:none;height:32px;padding:0 var(--s5);background:var(--c12);border:1px solid #1E3A66;border-radius:var(--r-sm);font-size:12px;font-weight:700;color:#1E3A66;white-space:nowrap">Dùng lại thông tin của tôi</button></div>
          </sc-if>
"""

_A1_TITLE = ('<div style="font-size:18px;font-weight:700;color:var(--c1)">'
             'Thông tin nhận hàng</div>')

# ---- Mục 3: kiểm tra tuổi 18–100 (A1) --------------------------------------
_A1_DOB_OLD = (
    '<label style="font-size:14px;font-weight:600;color:var(--c2)">Ngày sinh</label>'
    '<input type="text" placeholder="22/01/1991" inputmode="numeric" maxlength="10" '
    'value="{{buyerDob}}" sc-camel-on-change="{{setBuyerDob}}" '
    'style="height:44px;padding:0 var(--s5);border:1px solid rgba(154,163,176,.6);'
    'border-radius:var(--r-md);font-size:14px" '
    'style-focus="border-color:#1E3A66;box-shadow:0 0 0 3px rgba(30,58,102,.25)"></div>')
_A1_DOB_NEW = (
    '<label style="font-size:14px;font-weight:600;color:var(--c2)">Ngày sinh</label>'
    '<input type="text" placeholder="22/01/1991" inputmode="numeric" maxlength="10" '
    'value="{{buyerDob}}" sc-camel-on-change="{{setBuyerDob}}" '
    'style="height:44px;padding:0 var(--s5);border:1px solid {{buyerDobBorder}};'
    'border-radius:var(--r-md);font-size:14px" '
    'style-focus="border-color:#1E3A66;box-shadow:0 0 0 3px rgba(30,58,102,.25)">'
    '<sc-if value="{{buyerDobError}}" hint-placeholder-val="{{false}}">'
    '<div style="font-size:12px;color:var(--err)">{{buyerDobError}}</div>'
    '</sc-if></div>')

# ---- Mục 5: khoá ô đồng ý đến khi bấm link chính sách (A1) ----------------
_A1_TC_OLD = (
    '<input type="checkbox" checked="{{buyTcChecked}}" '
    'sc-camel-on-change="{{toggleBuyTc}}" '
    'style="margin-top:3px;flex:none;width:16px;height:16px;accent-color:#1E3A66">'
    '<span>Bằng cách đăng ký mua hàng và thanh toán, bạn đã đồng ý với '
    '<a href="policy.html?s=quy-che-website" style="color:#1E3A66;font-weight:600">'
    'Điều khoản sử dụng</a> và '
    '<a href="policy.html?s=bao-mat-thong-tin" style="color:#1E3A66;font-weight:600">'
    'Chính sách bảo mật</a> của HOMI365.</span>')
_A1_TC_NEW = (
    '<input type="checkbox" class="tnc-agree" disabled checked="{{buyTcChecked}}" '
    'sc-camel-on-change="{{toggleBuyTc}}" '
    'style="margin-top:3px;flex:none;width:16px;height:16px;accent-color:#1E3A66;'
    'opacity:.4;cursor:not-allowed">'
    '<span>Bằng cách đăng ký mua hàng và thanh toán, bạn đã đồng ý với '
    '<a href="policy.html?s=quy-che-website" target="_blank" class="tnc-link" '
    'style="color:#1E3A66;font-weight:600">Điều khoản sử dụng</a> và '
    '<a href="policy.html?s=bao-mat-thong-tin" target="_blank" class="tnc-link" '
    'style="color:#1E3A66;font-weight:600">Chính sách bảo mật</a> của HOMI365.</span>')

# ---- Mục 1: C1 biết mình được gọi từ form mua hàng -------------------------
_C1_HEAD_OLD = ('<div style="font-size:22px;font-weight:700;color:var(--c1);'
                'line-height:1.4">Đăng nhập để xem điểm thưởng và ưu đãi của bạn'
                '</div></div>')
_C1_HEAD_NEW = (
    '<div style="font-size:22px;font-weight:700;color:var(--c1);line-height:1.4">'
    '{{loginHeading}}</div>'
    '<sc-if value="{{loginFromBuy}}" hint-placeholder-val="{{false}}">'
    '<div style="font-size:13px;color:var(--c5);margin-top:var(--s3);line-height:1.6">'
    'Đăng nhập xong bạn quay lại form mua hàng, thông tin được điền sẵn theo đơn '
    'gần nhất.</div>'
    '<button sc-camel-on-click="{{backToBuy}}" style="background:none;border:none;'
    'font-size:13px;font-weight:600;color:var(--c6);margin-top:var(--s2);'
    'padding:var(--s2)">Bỏ qua, quay lại form mua hàng</button>'
    '</sc-if></div>')

# ---- Mục 6: bỏ trạng thái chờ kích hoạt (A2, A3) ---------------------------
_A2_DONE_OLD = ('Ngay lập tức, bạn có thể giới thiệu khách hàng tham gia sản phẩm.'
                '<br>Điểm thưởng và ưu đãi sẽ tạm giữ cho tới khi Quản trị viên '
                'kích hoạt thành công.')
_A2_DONE_NEW = ('Bạn giới thiệu khách hàng và gửi yêu cầu đổi điểm được ngay.'
                '<br>Điểm HOMI của mỗi đơn được ghi nhận '
                'sau khi đơn đó được Quản trị viên duyệt.')

_TNC_OLD = ('Điểm chỉ được cộng sau khi tài khoản Thành viên đã được kích hoạt; '
            'các đơn phát sinh trước thời điểm kích hoạt vẫn được tính và cộng bù '
            'đầy đủ.')
_TNC_NEW = ('Điểm của mỗi đơn được cộng ngay sau khi đơn đó được HOMI365 duyệt; '
            'Thành viên dùng được link giới thiệu và gửi yêu cầu đổi điểm ngay sau '
            'khi đăng ký.')

# Banner "CHỜ KÍCH HOẠT" ở A3: cắt cả khối theo hai mốc đầu / cuối.
_A3_BANNER_START = '      <sc-if value="{{isNewAgent}}" hint-placeholder-val="{{false}}">'
_A3_BANNER_END = ('Chưa thể rút tiền — chờ kích hoạt</button>\n'
                  '      </div>\n      </sc-if>\n')

_A3_NOTE_OLD = ('Yêu cầu rút tiền đang ở trạng thái <strong>chờ duyệt</strong> hoặc '
                '<strong>đã duyệt</strong> sẽ được tạm giữ và trừ khỏi số dư khả '
                'dụng, cho tới khi chi trả xong hoặc bị từ chối. Bị từ chối thì '
                'tiền hoàn lại số dư khả dụng.')
_A3_NOTE_NEW = ('Yêu cầu đổi điểm đang <strong>chờ duyệt</strong> hoặc '
                '<strong>đã duyệt</strong> được trừ khỏi số dư khả dụng cho tới '
                'khi chi trả xong. Yêu cầu bị từ chối thì điểm được cộng lại vào '
                'số dư khả dụng.')

_A3_PENDING_ORDERS = (
    '        <sc-if value="{{hasPendingOrders}}" hint-placeholder-val="{{false}}">\n'
    '          <div style="' + _INFO + '">Bạn có <strong>{{pendingOrderCount}} đơn'
    '</strong> đang chờ Quản trị viên duyệt. Điểm HOMI của đơn được ghi nhận ngay '
    'sau khi đơn được duyệt.</div>\n'
    '        </sc-if>\n')

# ---- Mục 10: xuất danh sách chi trả (B3) ------------------------------------
_B3_EXPORT_OLD = (
    '<div style="font-size:24px;font-weight:700">Yêu cầu rút tiền</div>\n'
    '            <button style="height:38px;padding:0 var(--s6);background:var(--c12);'
    'border:1px solid rgba(154,163,176,.6);border-radius:var(--r-md);font-size:13px;'
    'font-weight:600;color:var(--c2)" style-hover="background:rgba(154,163,176,.08)">'
    'Xuất file Excel</button>')

_PO_COLS = "1.3fr 1.1fr 1fr .8fr .9fr"
B3_EXPORT_NEW = (
    '<div style="font-size:24px;font-weight:700">Yêu cầu rút tiền</div>\n'
    '            <button sc-camel-on-click="{{openPayoutExport}}" style="height:38px;'
    'padding:0 var(--s6);background:var(--c6);border:none;border-radius:var(--r-md);'
    'font-size:13px;font-weight:600;color:var(--c12)" style-hover="' + _HOVER_P + '">'
    'Xuất danh sách chi trả</button>\n'
    """
            <!-- (21) MODAL: xuất danh sách chi trả theo kỳ — bổ sung sau UAT 02/10 -->
            <sc-if value="{{showPayoutExport}}" hint-placeholder-val="{{false}}">
              <div style=\"""" + _OVERLAY + """\">
                <div style="width:100%;max-width:640px;max-height:92vh;overflow:auto;background:var(--c12);border-radius:var(--r-lg);padding:var(--s8);display:flex;flex-direction:column;gap:var(--s6);box-shadow:0 8px 30px rgba(0,0,0,.25)">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start">
                    <div><div style="font-size:18px;font-weight:700;color:var(--c1)">Xuất danh sách chi trả</div><div style="font-size:12px;color:var(--c5);margin-top:var(--s1)">Mỗi kỳ xuất một file Excel để gửi ngân hàng chi.</div></div>
                    <button sc-camel-on-click="{{closePayoutExport}}" style="background:none;border:none;font-size:18px;color:var(--c5)">✕</button>
                  </div>
                  <div style="display:flex;flex-direction:column;gap:var(--s3)">
                    <div style="font-size:12px;font-weight:600;color:var(--c5)">Kỳ chi trả</div>
                    <div style="display:flex;gap:var(--s2);flex-wrap:wrap">
                      <sc-for list="{{payoutPeriods}}" as="pp" hint-placeholder-count="3">
                        <button sc-camel-on-click="{{pp.onClick}}" style="{{pp.style}}">{{pp.label}}</button>
                      </sc-for>
                    </div>
                  </div>
                  <div style=\"""" + _INFO + """\">File gồm 5 cột: <strong>Tên chủ tài khoản · Số tài khoản · Ngân hàng · Số điểm · Số tiền</strong>. Chỉ lấy các yêu cầu <strong>đã duyệt đủ 2 bước</strong> và chưa chi của kỳ được chọn.</div>
                  <div style="border:1px solid rgba(154,163,176,.35);border-radius:var(--r-md);overflow:auto">
                    <div style="display:grid;grid-template-columns:""" + _PO_COLS + """;min-width:560px;background:rgba(154,163,176,.08);padding:var(--s4) var(--s5);font-size:11px;font-weight:700;color:var(--c5);text-transform:uppercase;letter-spacing:.03em">
                      <div>Tên chủ tài khoản</div><div>Số tài khoản</div><div>Ngân hàng</div><div style="text-align:right">Số điểm</div><div style="text-align:right">Số tiền</div>
                    </div>
                    <sc-for list="{{payoutRows}}" as="pr" hint-placeholder-count="2">
                      <div style="display:grid;grid-template-columns:""" + _PO_COLS + """;min-width:560px;align-items:center;padding:var(--s4) var(--s5);font-size:13px;color:var(--c1);border-top:1px solid rgba(154,163,176,.2)">
                        <div style="font-weight:600">{{pr.accountHolder}}</div><div style="font-family:monospace;color:var(--c4)">{{pr.accountNumber}}</div><div style="color:var(--c4)">{{pr.bankName}}</div><div style="text-align:right">{{pr.points}}</div><div style="text-align:right;font-weight:700">{{pr.amount}}</div>
                      </div>
                    </sc-for>
                    <sc-if value="{{payoutEmpty}}" hint-placeholder-val="{{false}}">
                      <div style="padding:var(--s7);text-align:center;color:var(--c5);font-size:13px">Kỳ này không có yêu cầu nào đã duyệt chờ chi.</div>
                    </sc-if>
                  </div>
                  <div style="display:flex;justify-content:space-between;gap:var(--s5);font-size:13px;color:var(--c2)"><span>Kỳ {{payoutPeriod}} · {{payoutCount}} yêu cầu</span><span>Tổng chi: <strong style="color:var(--c1)">{{payoutTotal}}</strong></span></div>
                  <sc-if value="{{payoutExported}}" hint-placeholder-val="{{false}}">
                    <div style="font-size:13px;color:#2F7A48;background:rgba(47,122,72,.12);border-radius:var(--r-md);padding:var(--s5)">Đã xuất <strong>{{payoutExported}}</strong> · {{payoutCount}} yêu cầu.</div>
                  </sc-if>
                  <div style="display:flex;gap:var(--s3)">
                    <button sc-camel-on-click="{{closePayoutExport}}" style="flex:1;""" + _BTN_G + """;font-size:14px">Đóng</button>
                    <button sc-camel-on-click="{{runPayoutExport}}" disabled="{{payoutEmpty}}" style="{{payoutBtnStyle}}">Xuất file Excel</button>
                  </div>
                </div>
              </div>
            </sc-if>""")

# ---- Mục 11: chi không thành công + hoàn điểm (B3) --------------------------
_B3_PAID_BTN_OLD = (
    '<button sc-camel-on-click="{{openPaidModal}}" style="height:42px;'
    'background:var(--c12);color:var(--c6);border:1px solid var(--c6);'
    'border-radius:var(--r-md);font-size:14px;font-weight:600" '
    'style-hover="background:rgba(30,58,102,.06)">Đánh dấu đã chi trả</button>\n'
    '        </sc-if>\n')
B3_PAID_BTN_NEW = (
    _B3_PAID_BTN_OLD.replace(
        '</button>\n        </sc-if>\n',
        '</button>\n'
        '          <button sc-camel-on-click="{{openPayFailModal}}" style="height:42px;'
        'background:var(--c12);color:var(--err);border:1px solid var(--err);'
        'border-radius:var(--r-md);font-size:14px;font-weight:600" '
        'style-hover="background:rgba(192,57,43,.06)">Ngân hàng chi không thành công'
        '</button>\n        </sc-if>\n')
    + '        <sc-if value="{{selectedWithdrawal.canRefund}}" hint-placeholder-val="{{false}}">\n'
      '          <button sc-camel-on-click="{{openRefundModal}}" style="height:42px;'
      'background:var(--c6);color:var(--c12);border:none;border-radius:var(--r-md);'
      'font-size:14px;font-weight:600" style-hover="' + _HOVER_P + '">Hoàn điểm</button>\n'
      '        </sc-if>\n'
      '        <sc-if value="{{selectedWithdrawal.hasFailNote}}" hint-placeholder-val="{{false}}">\n'
      '          <div style="font-size:13px;color:var(--err);background:rgba(192,57,43,.08);'
      'border-radius:var(--r-md);padding:var(--s5)"><strong>Ngân hàng trả về:</strong> '
      '{{selectedWithdrawal.failNote}}</div>\n'
      '        </sc-if>\n'
      '        <sc-if value="{{selectedWithdrawal.hasRefundReason}}" hint-placeholder-val="{{false}}">\n'
      '          <div style="font-size:13px;color:var(--c4);background:rgba(30,58,102,.08);'
      'border-radius:var(--r-md);padding:var(--s5)"><strong>Lý do hoàn điểm:</strong> '
      '{{selectedWithdrawal.refundReason}}</div>\n'
      '        </sc-if>\n')

_MODAL_PAID_ANCHOR = '        <sc-if value="{{isPaidModal}}" hint-placeholder-val="{{false}}">'
B3_NEW_MODALS = """        <!-- (22) Chi không thành công + hoàn điểm — bổ sung sau UAT 02/10 -->
        <sc-if value="{{isPayFailModal}}" hint-placeholder-val="{{false}}">
          <div style="font-size:18px;font-weight:700;color:var(--c1)">Ngân hàng chi không thành công</div>
          <div style="font-size:14px;color:var(--c2);line-height:1.6">Ghi nhận khoản chi <strong>{{actionWithdrawal.amount}}</strong> cho <strong>{{actionWithdrawal.seller}}</strong> bị ngân hàng trả về? Yêu cầu chuyển sang <strong>Chi không thành công</strong>; điểm chưa được trả lại cho tới khi bạn bấm Hoàn điểm.</div>
          <div style="display:flex;flex-direction:column;gap:var(--s2)">
            <label style="font-size:12px;font-weight:600;color:var(--c5)">Nội dung ngân hàng trả về (tuỳ chọn)</label>
            <input type="text" placeholder="VD: Số tài khoản không tồn tại" value="{{paidNote}}" sc-camel-on-change="{{setPaidNote}}" style="height:40px;padding:0 var(--s5);border:1px solid rgba(154,163,176,.6);border-radius:var(--r-md);font-size:13px" style-focus=\"""" + _FOCUS + """\">
          </div>
          <div style="display:flex;gap:var(--s3)">
            <button sc-camel-on-click="{{closeActionModal}}" style="flex:1;height:44px;background:var(--c12);color:var(--c2);border:1px solid rgba(154,163,176,.6);border-radius:var(--r-md);font-size:14px;font-weight:600">Hủy</button>
            <button sc-camel-on-click="{{confirmPayFail}}" style="flex:1;height:44px;background:var(--err);color:var(--c12);border:none;border-radius:var(--r-md);font-size:14px;font-weight:600">Xác nhận</button>
          </div>
        </sc-if>

        <sc-if value="{{isRefundModal}}" hint-placeholder-val="{{false}}">
          <div style="font-size:18px;font-weight:700;color:var(--c1)">Hoàn điểm</div>
          <div style="font-size:14px;color:var(--c2);line-height:1.6">Cộng lại <strong>{{actionWithdrawal.amount}}</strong> vào số dư khả dụng của <strong>{{actionWithdrawal.seller}}</strong>. Thành viên tạo được yêu cầu đổi điểm mới sau khi sửa thông tin tài khoản.</div>
          <div style="display:flex;flex-direction:column;gap:var(--s2)">
            <label style="font-size:12px;font-weight:600;color:var(--c5)">Lý do hoàn điểm (*)</label>
            <textarea placeholder="VD: Ngân hàng trả về, sai số tài khoản" value="{{rejectReason}}" sc-camel-on-change="{{setRejectReason}}" style="min-height:90px;padding:var(--s5);border:1px solid rgba(154,163,176,.6);border-radius:var(--r-md);font-size:13px;resize:vertical"></textarea>
          </div>
          <div style=\"""" + _INFO + """\">Khi xác nhận, hệ thống gửi email báo cho thành viên rằng tài khoản nhận tiền có vấn đề, và ghi thao tác này vào Nhật ký hệ thống.</div>
          <div style="display:flex;gap:var(--s3)">
            <button sc-camel-on-click="{{closeActionModal}}" style="flex:1;height:44px;background:var(--c12);color:var(--c2);border:1px solid rgba(154,163,176,.6);border-radius:var(--r-md);font-size:14px;font-weight:600">Hủy</button>
            <button sc-camel-on-click="{{confirmRefund}}" disabled="{{rejectDisabled}}" style="{{refundConfirmStyle}}">Hoàn điểm</button>
          </div>
        </sc-if>

"""

# ---- Mục 22: nhắc gửi email khi admin sửa hồ sơ (B2) ------------------------
_B2_PF_BTNS_OLD = ('              <div style="display:flex;gap:var(--s4)">\n'
                   '                <button sc-camel-on-click="{{cancelProfileEdit}}"')
B2_PF_BTNS_NEW = ('              <div style="' + _INFO + '">{{pfMailNote}}</div>\n'
                  + _B2_PF_BTNS_OLD)

_B2_PF_EDIT_BTN_OLD = '              <button sc-camel-on-click="{{startProfileEdit}}"'
B2_PF_EDIT_BTN_NEW = (
    '              <sc-if value="{{profileSavedNote}}" hint-placeholder-val="{{false}}">\n'
    '                <div style="font-size:12px;color:#2F7A48;background:rgba(47,122,72,.12);'
    'border-radius:var(--r-sm);padding:var(--s4);line-height:1.6">{{profileSavedNote}}</div>\n'
    '              </sc-if>\n' + _B2_PF_EDIT_BTN_OLD)

# (neo, thay bằng[, chỉ áp cho các khối này]). Form đăng ký A2 dùng lại đúng
# các ô Tỉnh / Phường / Ngày sinh của A1, nên bản vá riêng cho form mua hàng
# phải khoá vào khối A1 — nếu không dấu (*) ở A2 cũng mất theo.
MARKUP = [
    # --- A1 ---
    ('  <sc-if value="{{isA1}}" hint-placeholder-val="{{true}}">',
     A1_PHONE_STEP + '  <sc-if value="{{isA1}}" hint-placeholder-val="{{false}}">'),
    (_A1_TITLE, _A1_TITLE + "\n" + A1_AUTOFILL_NOTE),
    (_A1_DOB_OLD, _A1_DOB_NEW, ("A1",)),
    ('>Tỉnh/Thành phố (*)</label>\n              <div style="position:relative">\n'
     '                <input type="text" value="{{provinceQuery}}"',
     '>Tỉnh/Thành phố</label>\n              <div style="position:relative">\n'
     '                <input type="text" value="{{provinceQuery}}"', ("A1",)),
    ('>Phường/Xã (*)</label>\n              <div style="position:relative">\n'
     '                <input type="text" value="{{wardQuery}}"',
     '>Phường/Xã</label>\n              <div style="position:relative">\n'
     '                <input type="text" value="{{wardQuery}}"', ("A1",)),
    (_A1_TC_OLD, _A1_TC_NEW),
    # (06/10, bổ sung) Ba ô nhận ưu đãi ở form MUA HÀNG không còn bắt buộc:
    # người chỉ mua, không làm thành viên thì chưa cần khai tài khoản. Form
    # đăng ký thành viên (A2) vẫn bắt buộc vì đó là nơi nhận chi trả.
    ('>Ngân hàng (*)</label>', '>Ngân hàng</label>', ("A1",)),
    ('>Số tài khoản (*)</label><input type="text" placeholder="Nhập số tài khoản" '
     'value="{{buyerBankAccount}}"',
     '>Số tài khoản</label><input type="text" placeholder="Nhập số tài khoản" '
     'value="{{buyerBankAccount}}"', ("A1",)),
    ('>Tên chủ tài khoản (*)</label>', '>Tên chủ tài khoản</label>', ("A1",)),
    # --- C1 ---
    (_C1_HEAD_OLD, _C1_HEAD_NEW),
    # --- A2 ---
    (_A2_DONE_OLD, _A2_DONE_NEW),
    ('style="{{regSubmitStyle}}">Xác nhận &amp; kích hoạt</button>',
     'style="{{regSubmitStyle}}">Xác nhận &amp; hoàn tất đăng ký</button>'),
    (_TNC_OLD, _TNC_NEW),
    # --- A3 ---
    ('      <sc-if value="{{isActiveAgent}}" hint-placeholder-val="{{true}}">',
     '      <sc-if value="{{isA3}}" hint-placeholder-val="{{true}}">'),
    ('>Đang chờ duyệt · tạm giữ</div>', '>Đang chờ duyệt</div>'),
    ('<div style="font-size:12px;color:var(--c5)">Đã rút</div>',
     '<div style="font-size:12px;color:var(--c5)">Đã đổi</div>'),
    ('<div style="font-size:12px;color:var(--c5)">Đã rút (tổng)</div>',
     '<div style="font-size:12px;color:var(--c5)">Đã đổi (tổng)</div>'),
    (_A3_NOTE_OLD + '</div>\n', _A3_NOTE_NEW + '</div>\n' + _A3_PENDING_ORDERS),
    ('Bạn đã gửi yêu cầu rút tiền trong tháng này. Lượt rút tiếp theo khả dụng từ',
     'Bạn đã gửi yêu cầu đổi điểm trong tháng này. Lượt đổi tiếp theo khả dụng từ'),
    ('>Số tiền muốn rút</label>', '>Số điểm muốn đổi</label>'),
    ('placeholder="Nhập số tiền (đ)" value="{{withdrawAmount}}"',
     'placeholder="Nhập số điểm" value="{{withdrawAmount}}"'),
    ('            <div style="font-size:12px;color:var(--err)">{{withdrawAmountError}}</div>\n'
     '          </sc-if>\n',
     '            <div style="font-size:12px;color:var(--err)">{{withdrawAmountError}}</div>\n'
     '          </sc-if>\n'
     '          <div style="font-size:11px;color:var(--c5)">1 Điểm HOMI = 1 VNĐ</div>\n'),
    # --- B3 ---
    (_B3_EXPORT_OLD, B3_EXPORT_NEW),
    (_B3_PAID_BTN_OLD, B3_PAID_BTN_NEW),
    (_MODAL_PAID_ANCHOR, B3_NEW_MODALS + _MODAL_PAID_ANCHOR),
    ('<option>Khoá / mở khoá</option><option>Tải file lên</option>',
     '<option>Khoá / mở khoá</option><option>Hoàn điểm</option>'
     '<option>Tải file lên</option>'),
    ('Rut khoan thuong tich diem ct uu dai khach hang',
     'Doi diem thuong ct uu dai khach hang'),
    # --- B2 ---
    (_B2_PF_BTNS_OLD, B2_PF_BTNS_NEW),
    (_B2_PF_EDIT_BTN_OLD, B2_PF_EDIT_BTN_NEW),
]


def patch_blocks(blocks, die):
    """Áp MARKUP lên mọi khối. Mỗi bản vá phải khớp ít nhất một khối."""
    out = dict(blocks)
    for i, item in enumerate(MARKUP):
        old, new = item[0], item[1]
        only = item[2] if len(item) > 2 else None
        hit = 0
        for k in out:
            if only and k not in only:
                continue
            n = out[k].count(old)
            if n > 1:
                die("bản vá UAT #%d khớp %d lần trong khối %s — neo chưa đủ "
                    "chặt:\n%s" % (i, n, k, old[:100]))
            if n == 1:
                out[k] = out[k].replace(old, new)
                hit += 1
        if not hit:
            die("bản vá UAT #%d không khớp khối nào:\n---\n%s\n---" % (i, old[:160]))

    # Mục 6: cắt banner "CHỜ KÍCH HOẠT" ở A3.
    cut = 0
    for k in out:
        a = out[k].find(_A3_BANNER_START)
        if a < 0:
            continue
        b = out[k].find(_A3_BANNER_END, a)
        if b < 0:
            die("thấy đầu banner chờ kích hoạt ở khối %s nhưng không thấy cuối" % k)
        out[k] = out[k][:a] + out[k][b + len(_A3_BANNER_END):]
        cut += 1
    if not cut:
        die("không tìm thấy banner chờ kích hoạt ở A3 để gỡ")

    return {k: rename(v) for k, v in out.items()}


# ============================================================================
# 2. ĐỔI CHỮ "rút tiền" -> "đổi điểm" (mục 7)
# ============================================================================
# Chạy SAU CÙNG, trên cả markup lẫn script. Thứ tự: cụm dài trước, cụm chung sau.
RENAMES = [
    ("Xác nhận duyệt yêu cầu rút <strong>", "Xác nhận duyệt yêu cầu đổi <strong>"),
    ("Yêu cầu rút {{actionWithdrawal.amount}}", "Yêu cầu đổi {{actionWithdrawal.amount}}"),
    ("Yêu cầu rút tiền", "Yêu cầu đổi điểm"),
    ("yêu cầu rút tiền", "yêu cầu đổi điểm"),
    ("Rút tiền", "Đổi điểm"),
    ("rút tiền", "đổi điểm"),
]


def rename(s):
    for old, new in RENAMES:
        s = s.replace(old, new)
    return s


# ============================================================================
# 3. SCRIPT
# ============================================================================

_JS_STATE = """    selectedOrderId: null,
    // (20) Sau UAT 02/10 — bước SĐT trước form mua hàng + tự điền.
    // buyStep: 'phone' | 'form'. buyMode: '' chưa đăng nhập | 'self' đã
    // tự điền theo đơn cũ | 'other' đang mua cho người khác.
    buyStep: 'phone', buyPhoneInput: '', buyPhoneError: '', buyPhoneFound: false,
    buyMode: '', buyProfile: null, returnTo: '',
    // (21) Xuất danh sách chi trả theo kỳ.
    showPayoutExport: false, payoutPeriod: '08/2026', payoutExported: '',
    // (23) Dòng xác nhận sau khi admin lưu hồ sơ: { id, text }.
    profileSaved: null,
"""

_JS_CLASS_OLD = "  STATUS_ORDER = { pending: 0, specialist_approved: 1, approved: 2, rejected: 3, paid: 4 };"
_JS_CLASS_NEW = """  STATUS_ORDER = { pending: 0, specialist_approved: 1, approved: 2, rejected: 3, paid: 4, pay_failed: 5, refunded: 6 };
  PAYOUT_PERIODS = ['09/2026', '08/2026', '07/2026'];

  // (20) Đơn gần nhất của người đã có tài khoản — dùng để tự điền form mua
  // hàng. Bản mẫu dùng chung một hồ sơ cho mọi SĐT đã đăng ký; bản thật lấy
  // từ đơn mới nhất của chính tài khoản vừa đăng nhập.
  BUYER_LAST_ORDER = {
    orderId: 'DH100077', orderDate: '12/08/2026',
    buyerName: 'Hoàng Thị Mỹ Trinh', buyerEmail: 'trinh.htm@gmail.com',
    buyerCccd: '079191000083', buyerAddress: 'Số 36 đường 27A',
    buyerDob: '22/01/1991', buyerBankAccount: '0071001234567',
    accountHolder: 'HOANG THI MY TRINH'
  };
  buyCarry(phone) {
    const p = this.BUYER_LAST_ORDER;
    return { buyStep: 'form', buyMode: 'self', buyProfile: { ...p, buyerPhone: phone },
      buyerPhone: phone, buyerName: p.buyerName, buyerEmail: p.buyerEmail,
      buyerCccd: p.buyerCccd, buyerAddress: p.buyerAddress, buyerDob: p.buyerDob,
      buyerBankAccount: p.buyerBankAccount, accountHolder: p.accountHolder };
  }

  // (20) Mục 3 — người mua phải từ 18 đến 100 tuổi. Chỉ xét khi đã gõ đủ
  // dd/mm/yyyy; đang gõ dở thì chưa báo lỗi.
  dobError(v) {
    const m = /^(\\d{2})\\/(\\d{2})\\/(\\d{4})$/.exec(v || '');
    if (!m) return '';
    const d = +m[1], mo = +m[2], y = +m[3];
    const dt = new Date(y, mo - 1, d);
    if (dt.getFullYear() !== y || dt.getMonth() !== mo - 1 || dt.getDate() !== d)
      return 'Ngày sinh không hợp lệ.';
    const now = new Date();
    let age = now.getFullYear() - y;
    if (now.getMonth() < mo - 1 || (now.getMonth() === mo - 1 && now.getDate() < d)) age--;
    return (age < 18 || age > 100) ? 'Người mua phải từ 18 đến 100 tuổi.' : '';
  }"""

_JS_BADGE_OLD = "      paid: ['rgba(47,122,72,.14)', '#2F7A48', 'Đã chi trả'],"
_JS_BADGE_NEW = (_JS_BADGE_OLD + "\n"
    "      pay_failed: ['rgba(192,57,43,.12)', '#C0392B', 'Chi không thành công'],\n"
    "      refunded: ['rgba(154,163,176,.18)', '#5B6472', 'Đã hoàn điểm'],")

_JS_FILTER_OLD = "['rejected','Từ chối'],['paid','Đã chi trả']];"
_JS_FILTER_NEW = ("['rejected','Từ chối'],['paid','Đã chi trả'],"
                  "['pay_failed','Chi không thành công'],['refunded','Đã hoàn điểm']];")

_JS_WD_SEED_OLD = "    return raw.map(w => ({ ...w, amount: w.amountNum.toLocaleString('vi-VN') + 'đ' }));\n  }\n\n  makeStock() {"
_JS_WD_SEED_NEW = """    // (22) Hai dòng mẫu cho luồng ngân hàng chi không thành công.
    raw.push(
      { id:6, seller:'Đỗ Anh Tuấn', amountNum:1500000, date:'22/08/2026', accountNumber:'0451000987654', bankName:'Vietcombank', branch:'CN Bình Dương', accountHolder:'DO ANH TUAN', status:'pay_failed', failNote:'Số tài khoản không tồn tại.',
        auditLog:[{label:'Tạo yêu cầu', actor:'Đỗ Anh Tuấn', time:'22/08/2026 09:14'},{label:'Admin duyệt (chờ Head)', actor:'Admin', time:'23/08/2026 10:02'},{label:'Head xác nhận duyệt', actor:'Head', time:'24/08/2026 08:40'},{label:'Ngân hàng chi không thành công', actor:'Admin', time:'03/09/2026 09:30'}] },
      { id:7, seller:'Trần Thị Bích', amountNum:1000000, date:'18/07/2026', accountNumber:'0071001234567', bankName:'Vietcombank', branch:'CN TP.HCM', accountHolder:'TRAN THI BICH', status:'refunded', failNote:'Tên chủ tài khoản không khớp.', refundReason:'Ngân hàng trả về do sai tên chủ tài khoản; thành viên đã được báo cập nhật lại.',
        auditLog:[{label:'Tạo yêu cầu', actor:'Trần Thị Bích', time:'18/07/2026 14:20'},{label:'Head xác nhận duyệt', actor:'Head', time:'20/07/2026 09:00'},{label:'Ngân hàng chi không thành công', actor:'Admin', time:'04/08/2026 10:10'},{label:'Hoàn điểm: sai tên chủ tài khoản', actor:'Admin', time:'04/08/2026 10:25'},{label:'Gửi email báo tài khoản nhận tiền có vấn đề', actor:'Hệ thống', time:'04/08/2026 10:25'}] }
    );
""" + _JS_WD_SEED_OLD

_JS_AUDIT_OLD = "  AUDIT = [\n"
_JS_AUDIT_NEW = """  AUDIT = [
    // (22)(23) Dòng mẫu cho hoàn điểm và admin sửa hồ sơ — sau UAT 02/10.
    { time:'17/09/2026 10:05', actor:'Nguyễn Thị Hạnh', role:'Admin',
      module:'Rút tiền', target:'YC-2026-0091 · Đỗ Anh Tuấn',
      action:'Hoàn điểm', before:'Chi không thành công', after:'Đã hoàn điểm · +1.500.000',
      evidence:'Lý do: sai số tài khoản', ip:'113.161.46.118' },
    { time:'17/09/2026 09:40', actor:'Nguyễn Thị Hạnh', role:'Admin',
      module:'Thành viên', target:'Ngô Thị Em · NTE3112',
      action:'Cập nhật', before:'Email: em3112@gmail.com', after:'Email: ngothiem.hcm@gmail.com',
      evidence:'Đã gửi email báo (địa chỉ cũ + mới)', ip:'113.161.46.118' },
"""

_JS_AUDIT_BADGE_OLD = "    'Tải file lên': ['rgba(30,58,102,.12)', '#1E3A66']"
_JS_AUDIT_BADGE_NEW = ("    'Hoàn điểm': ['rgba(150,92,10,.15)', '#965C0A'],\n"
                       + _JS_AUDIT_BADGE_OLD)

# Hằng tính trước `return {` của renderVals.
_JS_CONSTS_OLD = "    // A2\n    const regStepBg"
_JS_CONSTS_NEW = """    // (20) A1 sau UAT 02/10 — tuổi người mua + điều kiện bật nút Thanh toán.
    const buyerDobError = this.dobError(s.buyerDob);
    const payOk = s.buyTcChecked && s.payStage !== 'sending' && !buyerDobError;

    // A2
    const regStepBg"""

_JS_BAL_OLD = "    const availableBalance = 4000000;"
_JS_BAL_NEW = ("    // (20) Mục 6 — thành viên mới dùng được ngay; số dư là số thật,\n"
               "    // chưa có đơn nào được duyệt thì bằng 0.\n"
               "    const availableBalance = s.agentStage === 'active' ? 4000000 : 0;")

_JS_BAL_LBL_OLD = ("      availableBalanceLabel: '4.000.000đ', pendingBalanceLabel: '800.000đ', "
                   "earnedBalanceLabel: '6.000.000đ',")
_JS_BAL_LBL_NEW = (
    "      availableBalanceLabel: s.agentStage === 'active' ? '4.000.000đ' : '0đ',\n"
    "      pendingBalanceLabel: s.agentStage === 'active' ? '800.000đ' : '0đ',\n"
    "      earnedBalanceLabel: s.agentStage === 'active' ? '6.000.000đ' : '0đ',\n"
    "      // H1 đã chốt: điểm ghi nhận SAU KHI admin duyệt đơn. Thành viên mới\n"
    "      // có 1 đơn đang chờ duyệt nên điểm chưa vào số dư.\n"
    "      hasPendingOrders: s.agentStage !== 'active', pendingOrderCount: 1,")

_JS_WD_ERR_OLD = ("'Vui lòng nhập số tiền hợp lệ.' : (withdrawAmountNum > availableBalance "
                  "? 'Số tiền vượt quá số dư khả dụng.' : '')")
_JS_WD_ERR_NEW = ("'Vui lòng nhập số điểm hợp lệ.' : (withdrawAmountNum > availableBalance "
                  "? 'Số điểm vượt quá số dư khả dụng.' : '')")

_JS_ISA1_OLD = "      isA1: s.screen === 'A1', isA2: s.screen === 'A2',"
_JS_ISA1_NEW = """      isA1: s.screen === 'A1' && s.buyStep === 'form',
      // (20) Bước 0 — nhập SĐT trước form mua hàng.
      isA1Phone: s.screen === 'A1' && s.buyStep !== 'form',
      buyPhoneInput: s.buyPhoneInput,
      setBuyPhoneInput: (e) => this.setState({
        buyPhoneInput: (e.target.value || '').replace(/\\D/g, '').slice(0, 10),
        buyPhoneError: '', buyPhoneFound: false }),
      buyPhoneError: s.buyPhoneError,
      buyPhoneBorder: s.buyPhoneError ? '#C0392B' : 'rgba(154,163,176,.6)',
      buyPhoneFound: s.buyPhoneFound, buyPhoneAsk: !s.buyPhoneFound,
      // Chỉ trả lời CÓ / CHƯA có tài khoản — không lộ tên hay đơn hàng của
      // người khác cho ai gõ đúng số.
      submitBuyPhone: () => {
        const ph = (s.buyPhoneInput || '').trim();
        if (!ph) { this.setState({ buyPhoneError: 'Vui lòng nhập số điện thoại.' }); return; }
        if (!/^0\\d{9}$/.test(ph)) { this.setState({ buyPhoneError: 'Số điện thoại gồm 10 chữ số, bắt đầu bằng 0.' }); return; }
        if (this.REGISTERED_PHONES.includes(ph)) { this.setState({ buyPhoneFound: true, buyPhoneError: '' }); return; }
        this.setState({ buyStep: 'form', buyerPhone: ph, buyMode: '' });
      },
      buyGoLogin: () => GO('C1', { agentLoginStep: 'login', agentPhone: s.buyPhoneInput,
        loginPhoneChecked: true, returnTo: 'A1' }),
      buySkipLogin: () => this.setState({ buyStep: 'form', buyerPhone: s.buyPhoneInput, buyMode: '' }),
      buyResetPhone: () => this.setState({ buyPhoneInput: '', buyPhoneFound: false, buyPhoneError: '' }),
      // (20) Mục 2 — tự điền theo đơn gần nhất, cho đổi sang mua cho người khác.
      buyIsSelf: s.buyMode === 'self', buyIsOther: s.buyMode === 'other',
      buyProfileDate: (s.buyProfile || {}).orderDate || '',
      buyProfileOrder: (s.buyProfile || {}).orderId || '',
      buyForOther: () => this.setState({ buyMode: 'other', buyerName: '', buyerPhone: '',
        buyerEmail: '', buyerCccd: '', buyerAddress: '', buyerDob: '',
        buyerBankAccount: '', accountHolder: '' }),
      buyForSelf: () => { const p = s.buyProfile || {}; this.setState({ buyMode: 'self',
        buyerName: p.buyerName || '', buyerPhone: p.buyerPhone || '',
        buyerEmail: p.buyerEmail || '', buyerCccd: p.buyerCccd || '',
        buyerAddress: p.buyerAddress || '', buyerDob: p.buyerDob || '',
        buyerBankAccount: p.buyerBankAccount || '', accountHolder: p.accountHolder || '' }); },
      buyerDobError,
      buyerDobBorder: buyerDobError ? '#C0392B' : 'rgba(154,163,176,.6)',
      // (20) C1 được gọi từ form mua hàng.
      loginFromBuy: s.returnTo === 'A1',
      loginHeading: s.returnTo === 'A1' ? 'Đăng nhập để tiếp tục mua hàng'
        : 'Đăng nhập để xem điểm thưởng và ưu đãi của bạn',
      backToBuy: () => GO('A1', { buyStep: 'form', buyerPhone: s.agentPhone.trim(), buyMode: '' }),
      isA2: s.screen === 'A2',"""

_JS_PAY_OLD = """      payDisabled: !s.buyTcChecked || s.payStage === 'sending',
      payStyle: 'height:48px;color:var(--c12);border:none;border-radius:var(--r-md);'
        + 'font-size:16px;font-weight:700;box-shadow:var(--sh);background:'
        + ((s.buyTcChecked && s.payStage !== 'sending')
             ? 'var(--c6)' : 'rgba(154,163,176,.5)')
        + ';cursor:' + ((s.buyTcChecked && s.payStage !== 'sending')
             ? 'pointer' : 'not-allowed'),"""
_JS_PAY_NEW = """      payDisabled: !payOk,
      payStyle: 'height:48px;color:var(--c12);border:none;border-radius:var(--r-md);'
        + 'font-size:16px;font-weight:700;box-shadow:var(--sh);background:'
        + (payOk ? 'var(--c6)' : 'rgba(154,163,176,.5)')
        + ';cursor:' + (payOk ? 'pointer' : 'not-allowed'),"""

_JS_LOGIN_OLD = """        if (ph && s.agentPassword === '123456') {
          GO('A3',"""
_JS_LOGIN_NEW = """        if (ph && s.agentPassword === '123456') {
          // (20) Gọi từ form mua hàng thì quay lại form, điền sẵn.
          if (s.returnTo === 'A1') { GO('A1', this.buyCarry(ph)); return; }
          GO('A3',"""

_JS_OTP_OLD = "      agentOtpConfirm: () => GO('A3', { agentStage: 'active' }),"
_JS_OTP_NEW = ("      agentOtpConfirm: () => (s.returnTo === 'A1'\n"
               "        ? GO('A1', this.buyCarry(s.agentPhone.trim()))\n"
               "        : GO('A3', { agentStage: 'active' })),")

_JS_CMT1_OLD = """        // Agent đã được Head duyệt -> dashboard hoạt động (rút tiền được).
        // Agent chưa duyệt -> dashboard chờ kích hoạt (ưu đãi tạm giữ)."""
_JS_CMT1_NEW = """        // Sau UAT 02/10 không còn trạng thái chờ kích hoạt: thành viên nào
        // cũng vào dashboard dùng được ngay. 'new' chỉ còn nghĩa là chưa có
        // đơn nào được duyệt nên số dư bằng 0."""

_JS_CMT2_OLD = "      // Chưa kích hoạt thì hoa hồng bị giữ, chưa được tính điểm.\n      heldCommissionLabel: '1.200.000đ',\n"
_JS_CMT2_NEW = ""

# B3 — trạng thái mới + xuất danh sách chi trả.
_JS_ACTION_OLD = "    // Action modal\n    const actionWithdrawalRaw"
_JS_ACTION_NEW = """    // (22) Ngân hàng chi không thành công -> hoàn điểm thủ công.
    if (selectedWithdrawal) {
      const st = selectedWithdrawal.status;
      Object.assign(selectedWithdrawal, {
        canRefund: st === 'pay_failed',
        hasFailNote: !!selectedWithdrawal.failNote,
        hasRefundReason: !!selectedWithdrawal.refundReason
      });
      if (st === 'pay_failed') selectedWithdrawal.approvalStageNote =
        'Ngân hàng chi không thành công. Điểm của yêu cầu này chưa được trả lại — bấm Hoàn điểm để cộng lại vào số dư của thành viên.';
      if (st === 'refunded') selectedWithdrawal.approvalStageNote =
        'Đã hoàn điểm cho thành viên. Yêu cầu này đóng lại, thành viên tạo yêu cầu mới sau khi sửa thông tin tài khoản.';
    }

    // (21) Danh sách chi trả theo kỳ: yêu cầu đã duyệt đủ 2 bước, chưa chi.
    const payoutRows = withdrawalsData
      .filter(w => w.status === 'approved' && (w.date || '').slice(3) === s.payoutPeriod)
      .map(w => ({ ...w, points: w.amountNum.toLocaleString('vi-VN') }));
    const payoutEmpty = payoutRows.length === 0;

    // Action modal
    const actionWithdrawalRaw"""

_JS_WD_RET_OLD = "      openPaidModal: () => this.setState({ actionModal: { type: 'paid', kind: 'withdrawal', id: s.selectedWithdrawalId }, paidNote: '' }),"
_JS_WD_RET_NEW = _JS_WD_RET_OLD + """
      // (22) Chi không thành công + hoàn điểm.
      openPayFailModal: () => this.setState({ actionModal: { type: 'payfail', kind: 'withdrawal', id: s.selectedWithdrawalId }, paidNote: '' }),
      openRefundModal: () => this.setState({ actionModal: { type: 'refund', kind: 'withdrawal', id: s.selectedWithdrawalId }, rejectReason: '' }),
      isPayFailModal: !!(s.actionModal && s.actionModal.type === 'payfail'),
      isRefundModal: !!(s.actionModal && s.actionModal.type === 'refund'),
      refundConfirmStyle: 'flex:1;height:44px;border:none;border-radius:5px;font-size:14px;font-weight:600;color:#FFFFFF;background:'
        + (rejectDisabled ? 'rgba(154,163,176,.5)' : 'var(--c6)') + ';cursor:' + (rejectDisabled ? 'not-allowed' : 'pointer'),
      confirmPayFail: () => {
        const id = s.actionModal.id, now = '03/09/2026 10:15';
        const actor = s.adminRole === 'specialist' ? 'Admin' : 'Head';
        this.setState({ withdrawalsData: withdrawalsData.map(w => w.id === id
          ? { ...w, status: 'pay_failed', failNote: (s.paidNote || '').trim(),
              auditLog: [...w.auditLog, { label: 'Ngân hàng chi không thành công', actor, time: now }] }
          : w), actionModal: null, paidNote: '' });
      },
      confirmRefund: () => {
        if (!s.rejectReason.trim()) return;
        const id = s.actionModal.id, now = '03/09/2026 10:20';
        const actor = s.adminRole === 'specialist' ? 'Admin' : 'Head';
        this.setState({ withdrawalsData: withdrawalsData.map(w => w.id === id
          ? { ...w, status: 'refunded', refundReason: s.rejectReason.trim(),
              auditLog: [...w.auditLog,
                { label: 'Hoàn điểm: ' + s.rejectReason.trim(), actor, time: now },
                { label: 'Gửi email báo tài khoản nhận tiền có vấn đề', actor: 'Hệ thống', time: now }] }
          : w), actionModal: null, rejectReason: '' });
      },
      // (21) Xuất danh sách chi trả.
      showPayoutExport: s.showPayoutExport,
      openPayoutExport: () => this.setState({ showPayoutExport: true, payoutExported: '' }),
      closePayoutExport: () => this.setState({ showPayoutExport: false, payoutExported: '' }),
      payoutPeriod: s.payoutPeriod,
      payoutPeriods: this.PAYOUT_PERIODS.map(p => ({
        label: 'Tháng ' + p, onClick: () => this.setState({ payoutPeriod: p, payoutExported: '' }),
        style: 'height:34px;padding:0 14px;border-radius:30px;font-size:12px;font-weight:600;border:1px solid '
          + (s.payoutPeriod === p ? '#1E3A66;background:rgba(30,58,102,.08);color:#1E3A66'
                                  : 'rgba(154,163,176,.4);background:transparent;color:var(--c5)')
      })),
      payoutRows, payoutEmpty, payoutCount: payoutRows.length,
      payoutTotal: payoutRows.reduce((t, w) => t + w.amountNum, 0).toLocaleString('vi-VN') + 'đ',
      payoutExported: s.payoutExported,
      payoutBtnStyle: 'flex:1;height:44px;border:none;border-radius:var(--r-md);font-size:14px;font-weight:600;color:#FFFFFF;background:'
        + (payoutEmpty ? 'rgba(154,163,176,.5)' : 'var(--c6)') + ';cursor:' + (payoutEmpty ? 'not-allowed' : 'pointer'),
      runPayoutExport: () => { if (payoutEmpty) return; this.setState({
        payoutExported: 'chi-tra-HOMI365-' + s.payoutPeriod.slice(3) + '-' + s.payoutPeriod.slice(0, 2) + '.xlsx' }); },"""

# B2 — sửa hồ sơ: nhắc gửi email (mục 22).
_JS_PF_OLD = """      saveProfileEdit: () => this.setState({
        memberEdits: { ...s.memberEdits, [s.selectedMemberId]: { ...s.profileDraft } },
        profileEdit: false, profileDraft: {} }),"""
_JS_PF_NEW = """      // (23) Mục 22 — admin sửa hồ sơ thì hệ thống gửi email cho người đó,
      // nêu giá trị mới. Đổi email thì gửi cả địa chỉ cũ lẫn địa chỉ mới.
      saveProfileEdit: () => {
        const cur = selectedMember || {}, d = s.profileDraft || {};
        const keys = ['name', 'phone', 'email', 'cccd', 'dobGender', 'address', 'bankAccount', 'bankHolder'];
        const changed = keys.filter(k => d[k] !== undefined && d[k] !== cur[k]);
        const mailChanged = changed.includes('email');
        const text = !changed.length ? ''
          : mailChanged
            ? 'Đã lưu hồ sơ · đã gửi email báo thay đổi tới ' + cur.email + ' (địa chỉ cũ) và ' + d.email + ' (địa chỉ mới).'
            : 'Đã lưu hồ sơ · đã gửi email báo thay đổi tới ' + cur.email + '.';
        this.setState({
          memberEdits: { ...s.memberEdits, [s.selectedMemberId]: { ...(s.memberEdits[s.selectedMemberId] || {}), ...d } },
          profileEdit: false, profileDraft: {},
          profileSaved: text ? { id: s.selectedMemberId, text } : null });
      },
      profileSavedNote: (s.profileSaved && s.profileSaved.id === s.selectedMemberId
        && s.profileOpen && !s.profileEdit) ? s.profileSaved.text : '',
      pfMailNote: (() => {
        const cur = (selectedMember || {}).email || '', nw = pfv('email');
        return (nw && nw !== cur)
          ? 'Email đã đổi. Khi lưu, hệ thống gửi email báo thay đổi tới cả địa chỉ cũ (' + cur + ') và địa chỉ mới (' + nw + '), nêu rõ các giá trị mới.'
          : 'Khi lưu, hệ thống sẽ gửi email báo thay đổi tới ' + cur + ', nêu rõ các giá trị mới.';
      })(),"""


JS = [
    ("    selectedOrderId: null,\n", _JS_STATE),
    (_JS_CLASS_OLD, _JS_CLASS_NEW),
    (_JS_BADGE_OLD, _JS_BADGE_NEW),
    (_JS_FILTER_OLD, _JS_FILTER_NEW),
    (_JS_WD_SEED_OLD, _JS_WD_SEED_NEW),
    (_JS_AUDIT_OLD, _JS_AUDIT_NEW),
    (_JS_AUDIT_BADGE_OLD, _JS_AUDIT_BADGE_NEW),
    (_JS_CONSTS_OLD, _JS_CONSTS_NEW),
    (_JS_BAL_OLD, _JS_BAL_NEW),
    (_JS_BAL_LBL_OLD, _JS_BAL_LBL_NEW),
    (_JS_WD_ERR_OLD, _JS_WD_ERR_NEW),
    (_JS_ISA1_OLD, _JS_ISA1_NEW),
    (_JS_PAY_OLD, _JS_PAY_NEW),
    (_JS_LOGIN_OLD, _JS_LOGIN_NEW),
    (_JS_OTP_OLD, _JS_OTP_NEW),
    (_JS_CMT1_OLD, _JS_CMT1_NEW),
    (_JS_CMT2_OLD, _JS_CMT2_NEW),
    (_JS_ACTION_OLD, _JS_ACTION_NEW + ""),
    (_JS_WD_RET_OLD, _JS_WD_RET_NEW),
    (_JS_PF_OLD, _JS_PF_NEW),
    # pfv(): ô sửa hồ sơ lấy giá trị nháp, chưa có thì lấy giá trị đang lưu —
    # để mở thẳng trạng thái "#sua-ho-so" bằng hash vẫn thấy form điền sẵn.
    ("    // (21) Danh sách chi trả theo kỳ:",
     "    const pfv = (k) => { const d = s.profileDraft || {};\n"
     "      return d[k] !== undefined ? d[k] : ((selectedMember || {})[k] || ''); };\n\n"
     "    // (21) Danh sách chi trả theo kỳ:"),
] + [
    ("      pf%s: (s.profileDraft || {}).%s || ''," % (a, b),
     "      pf%s: pfv('%s')," % (a, b))
    for a, b in [("Name", "name"), ("Phone", "phone"), ("Email", "email"),
                 ("Cccd", "cccd"), ("Dob", "dobGender"), ("Address", "address"),
                 ("BankAccount", "bankAccount"), ("BankHolder", "bankHolder")]
]


def patch_script(script, die):
    for i, (old, new) in enumerate(JS):
        n = script.count(old)
        if n != 1:
            die("bản vá JS UAT #%d khớp %d lần (cần đúng 1):\n---\n%s\n---"
                % (i, n, old[:160]))
        script = script.replace(old, new)
    return rename(script)


# ============================================================================
# 4. TRẠNG THÁI XEM THỬ (index.html + #hash)
# ============================================================================

def patch_screens(screens):
    by = {sc["code"]: sc for sc in screens}

    # A1 — mặc định giờ là bước nhập SĐT; các trạng thái cũ đều ở bước form.
    a1 = by["A1"]
    old = [(h, lb, dict(st, buyStep="form")) for h, lb, st in a1["states"][1:]]
    prof = {"orderId": "DH100077", "orderDate": "12/08/2026",
            "buyerName": "Hoàng Thị Mỹ Trinh", "buyerPhone": "0901234567",
            "buyerEmail": "trinh.htm@gmail.com", "buyerCccd": "079191000083",
            "buyerAddress": "Số 36 đường 27A", "buyerDob": "22/01/1991",
            "buyerBankAccount": "0071001234567",
            "accountHolder": "HOANG THI MY TRINH"}
    filled = {k: v for k, v in prof.items() if k not in ("orderId", "orderDate")}
    a1["states"] = [
        ("", "Bước 0 — nhập số điện thoại", {"buyStep": "phone"}),
        ("sdt-da-co", "SĐT đã có tài khoản — gợi ý đăng nhập",
         {"buyStep": "phone", "buyPhoneInput": "0901234567", "buyPhoneFound": True}),
        ("form", "Form mua hàng — khách mới hoặc bỏ qua đăng nhập",
         {"buyStep": "form", "buyerPhone": "0900000000"}),
        ("form-tu-dien", "Form tự điền theo đơn gần nhất (sau đăng nhập)",
         dict(filled, buyStep="form", buyMode="self", buyProfile=prof)),
        ("mua-cho-nguoi-khac", "Form — mua cho người khác",
         {"buyStep": "form", "buyMode": "other", "buyProfile": prof}),
        ("loi-tuoi", "Form — ngày sinh ngoài 18–100 tuổi",
         {"buyStep": "form", "buyerPhone": "0900000000", "buyerDob": "15/03/2015",
          "buyTcChecked": True}),
    ] + old

    # C1 — đăng nhập được gọi từ form mua hàng.
    by["C1"]["states"].insert(2, (
        "tu-mua-hang", "Đăng nhập từ form mua hàng — xong quay lại A1",
        {"agentLoginStep": "login", "agentPhone": "0901234567",
         "loginPhoneChecked": True, "returnTo": "A1"}))

    # A3 — đổi nhãn + hash theo mục 6 và 7.
    a3 = by["A3"]
    a3["states"] = [
        ("", "Thành viên mới — dùng được ngay, chưa có đơn được duyệt",
         {"agentStage": "new"}),
        ("da-tinh-hh", "Thành viên đã có điểm", {"agentStage": "active"}),
        ("doi-diem", "Form yêu cầu đổi điểm",
         {"agentStage": "active", "showWithdrawForm": True}),
        ("doi-diem-ok", "Đổi điểm — gửi thành công",
         {"agentStage": "active", "showWithdrawSuccess": True}),
    ]

    # B2 — sửa hồ sơ có dòng nhắc gửi email.
    by["B2"]["states"] += [
        ("sua-ho-so", "Sửa hồ sơ — nhắc gửi email báo thay đổi",
         {"selectedMemberId": 2, "profileOpen": True, "profileEdit": True}),
        ("sua-ho-so-doi-email", "Sửa hồ sơ — đổi email, gửi cả địa chỉ cũ và mới",
         {"selectedMemberId": 2, "profileOpen": True, "profileEdit": True,
          "profileDraft": {"email": "cuong.levan@gmail.com"}}),
    ]

    # B3 — xuất danh sách chi trả, chi không thành công, hoàn điểm.
    by["B3"]["states"] += [
        ("xuat-chi-tra", "Modal xuất danh sách chi trả theo kỳ",
         {"showPayoutExport": True}),
        ("bao-chi-loi", "Modal ghi nhận ngân hàng chi không thành công",
         {"selectedWithdrawalId": 3,
          "actionModal": {"type": "payfail", "kind": "withdrawal", "id": 3}}),
        ("chi-khong-thanh-cong", "Chi tiết yêu cầu chi không thành công",
         {"selectedWithdrawalId": 6}),
        ("hoan-diem", "Modal hoàn điểm — lý do bắt buộc",
         {"selectedWithdrawalId": 6,
          "actionModal": {"type": "refund", "kind": "withdrawal", "id": 6}}),
        ("da-hoan-diem", "Chi tiết yêu cầu đã hoàn điểm",
         {"selectedWithdrawalId": 7}),
    ]

    # Mục 7 — đổi chữ ở tên màn và nhãn trạng thái.
    for sc in screens:
        sc["title"] = rename(sc["title"])
        sc["states"] = [(h, rename(lb), st) for h, lb, st in sc["states"]]
    return screens


# ============================================================================
# 5. otp.js + policies.js
# ============================================================================

def patch_otp(js, die):
    old = "    var hint = document.querySelector('.tnc-hint');\n"
    if js.count(old) != 1:
        die("không tìm thấy neo trong OTP_JS để mở khoá ô đã tích sẵn")
    # Trạng thái mở bằng #hash có thể đã tích sẵn ô đồng ý (ví dụ
    # a1-buy.html#loi-duong-truyen). Ô đã tích mà vẫn khoá thì vô lý.
    # KHÔNG đọc box.checked: trước khi runtime dựng xong, thẻ input thô còn
    # mang thuộc tính checked="{{…}}" nên trình duyệt coi là đã tích.
    return js.replace(old, "    var st0 = window.__STATE__ || {};\n"
                           "    if (st0.buyTcChecked || st0.tncChecked) read = true;\n"
                      + old).replace(
        "// cuộn hết văn bản, hoặc mở một link chính sách.",
        "// cuộn hết văn bản, hoặc mở một link chính sách. Từ 06/10 form mua hàng\n"
        "// (A1) dùng chung cơ chế này: ô đồng ý khoá tới khi bấm link chính sách.")


_POL = [
    ("'Điểm chỉ được cộng vào tài khoản sau khi Thành viên đã được kích hoạt.',\n"
     "        'Các đơn hàng phát sinh trước thời điểm kích hoạt vẫn được ghi nhận và "
     "cộng bù đầy đủ, tính từ đơn đầu tiên.',",
     "'Điểm của mỗi đơn được cộng ngay sau khi đơn đó được HOMI365 duyệt.',\n"
     "        'Thành viên dùng được link giới thiệu và gửi yêu cầu đổi điểm ngay sau "
     "khi đăng ký.',"),
    ("trước khi tài khoản được kích hoạt.'", "khi hoàn tất đăng ký.'"),
]


def patch_policy(js, die):
    for old, new in _POL:
        if js.count(old) != 1:
            die("không khớp neo trong TNC_POLICY_JS:\n%s" % old[:100])
        js = js.replace(old, new)
    return js


# ============================================================================
# 6. DIFF-vs-mockup-KH.md — mục 19
# ============================================================================

DIFF = [
    "## 19. Cập nhật sau UAT 02/10 — đợt 06/10", "",
    "Nguồn: sheet `Plan Update` trong Google Sheet `[Homi] - Change Request`. "
    "Đợt này chỉ làm các mục **không bị chặn** bởi câu hỏi H2–H5. Toàn bộ bản vá "
    "nằm ở `tools/update_uat0210.py`, neo không khớp là dừng build.", "",
    "| Mục | Màn | Thay đổi | Xem thử |", "|---|---|---|---|",
    "| 1 | A1, C1 | Thêm **bước nhập số điện thoại** trước form mua hàng. Số đã có "
    "tài khoản thì hiện khối gợi ý với hai nút Đăng nhập / Bỏ qua và tự điền; số "
    "mới vào thẳng form, điền sẵn số vừa nhập. Hệ thống chỉ trả lời có hay chưa có "
    "tài khoản. Đăng nhập đi qua C1 rồi **quay lại form mua hàng** (đã chốt). | "
    "`a1-buy.html`, `#sdt-da-co`, `#form`, `c1-login.html#tu-mua-hang` |",
    "| 2 | A1 | Sau đăng nhập form **tự điền theo đơn gần nhất**, có dòng \"Đã "
    "điền theo đơn ngày …\", sửa trực tiếp được. Nút **Mua cho người khác** xoá "
    "phần tự điền; có nút dùng lại thông tin cũ. | `#form-tu-dien`, "
    "`#mua-cho-nguoi-khac` |",
    "| 3 | A1 | Ô Ngày sinh kiểm tra tuổi **18–100**, báo lỗi ngay dưới ô và khoá "
    "nút Thanh toán. Chỉ xét khi đã gõ đủ `dd/mm/yyyy`. | `#loi-tuoi` |",
    "| 4 | A1 | Bỏ dấu (*) ở Tỉnh/Thành phố và Phường/Xã. Nút Thanh toán vốn "
    "không phụ thuộc hai ô này nên không có điều kiện nào phải gỡ. Bổ sung cùng "
    "ngày: ba ô **Ngân hàng, Số tài khoản, Tên chủ tài khoản** ở form mua hàng "
    "cũng bỏ dấu (*) — vẫn giữ ô, chỉ không bắt buộc nhập. Form đăng ký thành "
    "viên A2 giữ nguyên bắt buộc. | `#form` |",
    "| 5 | A1 | Ô đồng ý chính sách **mờ và khoá**, bấm một trong hai link chính "
    "sách thì mở. Hai link đổi sang mở tab mới — trước đây mở cùng tab, bấm là "
    "mất dữ liệu đang nhập. Dùng lại cơ chế của A2 bước 4 trong `js/otp.js`. | "
    "`#form` |",
    "| 6 | A2, A3 | **Bỏ trạng thái chờ kích hoạt.** A2 bước 5 và nút bước 4 "
    "không còn chữ \"kích hoạt\", \"tạm giữ\". A3 gỡ banner CHỜ KÍCH HOẠT; khối "
    "số dư và nút đổi điểm hiện cho cả thành viên mới, số dư là số thật. Đơn chưa "
    "duyệt hiện dòng \"điểm được ghi nhận sau khi đơn được duyệt\" (H1 đã chốt). "
    "Sửa câu tương ứng ở Điều khoản mục 2. | `a2-register.html#buoc-5`, "
    "`a3-dashboard.html` |",
    "| 7 | mọi màn | Đổi toàn bộ **\"rút tiền\" → \"đổi điểm\"**: tiêu đề, nút, "
    "cột bảng, bộ lọc, sidebar, phân hệ trong nhật ký, tên trạng thái ở "
    "`index.html`. Hash `#rut-tien` đổi thành `#doi-diem`. | — |",
    "| 10 | B3 | Nút **Xuất danh sách chi trả** mở hộp thoại chọn kỳ, liệt kê 5 "
    "cột của file, xem trước các dòng và tổng chi của kỳ. | "
    "`b3-withdrawals.html#xuat-chi-tra` |",
    "| 11 | B3, B8 | Hai trạng thái mới **Chi không thành công** và **Đã hoàn "
    "điểm**, có bộ lọc riêng. Yêu cầu đã duyệt có thêm nút ghi nhận ngân hàng "
    "trả về; sau đó nút **Hoàn điểm** với lý do bắt buộc và dòng nhắc hệ thống "
    "gửi email. B8 thêm hành động Hoàn điểm. | `#bao-chi-loi`, "
    "`#chi-khong-thanh-cong`, `#hoan-diem`, `#da-hoan-diem` |",
    "| 22 | B2, B8 | Form sửa hồ sơ có dòng nhắc **hệ thống sẽ gửi email báo "
    "thay đổi**; đổi email thì nêu cả địa chỉ cũ và mới. Lưu xong hiện dòng xác "
    "nhận. B8 thêm dòng mẫu. | `b2-members.html#sua-ho-so`, "
    "`#sua-ho-so-doi-email` |", "",
    "**Hai mục không có gì phải sửa trên giao diện:**", "",
    "- **Mục 19** (bỏ từ \"tách nhánh\"): prototype không dùng từ này ở màn nào.",
    "- **Mục 16** (email khi thăng/hạ cấp): không có giao diện, xem danh sách "
    "email dưới đây.", "",
    "**Email hệ thống phát sinh từ đợt này** — nội dung do team HOMI365 biên "
    "soạn:", "",
    "| Email | Gửi cho | Khi nào | Mục |", "|---|---|---|---|",
    "| Báo thăng / hạ cấp | Thành viên | Mỗi khi cấp thay đổi | 16 |",
    "| Báo tài khoản nhận tiền có vấn đề | Thành viên | Admin bấm Hoàn điểm | 11 |",
    "| Báo hồ sơ được sửa, nêu giá trị mới | Thành viên (đổi email thì cả địa "
    "chỉ cũ lẫn mới) | Admin lưu hồ sơ | 22 |", "",
    "**Giả định của bản mẫu — cần xác nhận khi làm thật:**", "",
    "1. **Thế nào là \"đã có tài khoản\" (mục 1).** Bản mẫu coi là số đã đăng ký "
    "thành viên, vì chỉ thành viên mới đăng nhập được. Khách từng mua nhưng chưa "
    "đăng ký thành viên được coi như khách mới.",
    "2. **Mua cho người khác (mục 2)** xoá hết phần tự điền, kể cả số điện thoại "
    "và tài khoản ngân hàng. Ai là người giới thiệu của đơn mua lần 2 trở đi "
    "đang chờ trả lời câu hỏi H5 ở sheet Change Request.",
    "3. **Chi không thành công (mục 11)** được ghi nhận từ trạng thái Đã duyệt, "
    "trước khi đánh dấu đã chi trả. Nếu ngân hàng trả về sau khi đã đánh dấu thì "
    "cần thêm nhánh từ Đã chi trả.",
    "4. **Cột của file chi trả (mục 10)** là 5 cột theo sheet; danh sách cuối "
    "cùng còn chờ phía HOMI365 xác nhận.",
    "5. **Nội dung chuyển khoản** ở chi tiết yêu cầu đổi từ `Rut khoan thuong…` "
    "sang `Doi diem thuong…` cho khớp mục 7.",
    "6. **Điều khoản mục 2** (bước 4 đăng ký và trang chính sách) đã sửa một câu "
    "cho khớp mục 6 — cần Pháp lý đọc lại.", "",
    "**Chưa làm, chờ khách hàng:** mục 8, 9 (H2, H3) · 12, 13, 14 (màn đề xuất "
    "thăng/hạ cấp) · 15, 20, 21 (H4) · 17, 18 (H5) · 23 (xác nhận đảo quyết định "
    "về B5).", "",
    "**Còn lệch, nằm ngoài phạm vi đợt này:** ngăn chi tiết thành viên ở B2 và "
    "hộp thoại Head duyệt hồ sơ vẫn ghi \"ưu đãi đang tạm giữ\", \"kích hoạt\". "
    "Sau mục 6 các câu này không còn đúng, nhưng ý nghĩa mới của bước Head duyệt "
    "hồ sơ chưa được chốt nên chưa sửa.", "",
]


def patch_diff(diff):
    """Chèn mục 19 vào trước phần 'Ghi chú'."""
    i = diff.index("## Ghi chú")
    return diff[:i] + DIFF + diff[i:]
