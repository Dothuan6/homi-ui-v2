# DIFF — prototype-v3 so với mockup của khách hàng

Sinh tự động bởi `tools/build-v3.py`. Ngoài 12 mục dưới đây, **không có thay đổi nào khác**: layout, khoảng cách, bo góc, font giữ nguyên 100%.

## 1. Đổi giá trị màu

| Màu cũ (mockup KH) | Màu mới (HOMI365) |
|---|---|
| `#00ADEE` | `#1E3A66` |
| `#00adee` | `#1E3A66` |
| `#0099d1` | `#1B3358` |
| `#0088ba` | `#122544` |
| `#00728f` | `#0F7F96` |
| `rgba(0,173,238,.14)` | `rgba(15,127,150,.14)` |
| `rgba(0,173,238,` | `rgba(30,58,102,` |
| `#EE0000` | `#1E3A66` |
| `#84BE52` | `#2F7A48` |
| `#4c7a2e` | `#2F7A48` |
| `#73aa45` | `#2F7A48` |
| `rgba(132,190,82,` | `rgba(47,122,72,` |
| `#FFA500` | `#965C0A` |
| `#FBAE40` | `#965C0A` |
| `#FFBC40` | `#E0B15F` |
| `#a36400` | `#965C0A` |
| `rgba(255,165,0,` | `rgba(150,92,10,` |
| `#D9342B` | `#C0392B` |
| `#E20707` | `#C0392B` |
| `rgba(217,52,43,` | `rgba(192,57,43,` |
| `rgba(226,7,7,` | `rgba(192,57,43,` |
| `#1F1F1F` | `#2B303A` |
| `#424242` | `#5B6472` |
| `#414445` | `#5B6472` |
| `#939393` | `#8A93A3` |
| `#AAAAAA` | `#C9CED4` |
| `#5c5c5c` | `#5B6472` |
| `rgba(31,31,31,` | `rgba(43,48,58,` |
| `rgba(170,170,170,` | `rgba(154,163,176,` |
| `rgba(204,204,204,.9)` | `rgba(18,37,68,.16)` |
| `#344557` | `#1B3358` |
| `#2a3745` | `#122544` |
| `rgba(52,69,87,` | `rgba(27,51,88,` |

## 2. Màu giữ nguyên — logo bên thứ ba

| Màu | Lý do |
|---|---|
| `#ED1C24` | logo Techcombank |
| `#00A19A` | logo napas247 |
| `#003DA5` | logo napas247 |

## 3. Thanh trên

Chữ `Homi365 ●` đổi thành ảnh logo chính thức (`assets/logo homi-01.png`), bấm vào về trang mục lục. Favicon dùng `assets/Icon_viewweb_final.jpg`.

Bỏ hai thành phần vốn là khung điều khiển của bản mockup, không thuộc sản phẩm:

- Dòng chú thích `WhiteCoat Việt Nam · 7 màn hình MVP`.
- Dãy nút chuyển màn `A1 · Thông tin nhận hàng … B4 · Kho hàng`. Việc chuyển màn giờ nằm ở `index.html`.

Vì thanh chỉ còn một phần tử, logo nâng lên 40px và đệm dọc nới từ 12px lên 16px — thanh cao 73px thay vì 65px. Mọi phép `calc(100vh - 65px)` trong mockup đã được sửa theo (3 chỗ) để màn quản trị không dư thanh cuộn.

Thêm nút **Đăng nhập Agent** ở góc phải thanh trên, chỉ trên 2 màn công khai A1 và A2 (trỏ sang `c1-login.html`). Không đặt ở C1 vì đang đứng sẵn ở đó, không đặt ở A3 vì đã đăng nhập, không đặt ở khung quản trị. Đây là thành phần mới so với mockup KH — cần nêu khi gửi.

Logo canh thẳng hàng với nội dung bên dưới: màn người mua và thành viên dùng chung khung 1160px canh giữa; màn quản trị canh theo mép trái các mục sidebar. Đây là thay đổi layout duy nhất của bản này, và chỉ ở thanh trên.

## 4. Bỏ trường Quận/Huyện

Hàng địa chỉ trong form mua hàng (A1) và form đăng ký (A2) đi từ **3 ô** `Tỉnh/Thành phố · Quận/Huyện · Phường/Xã` xuống **2 ô** `Tỉnh/Thành phố · Phường/Xã`. Đã bỏ 2 ô, lưới đổi từ 3 cột sang 2 cột.

Đây là **thay đổi trường nhập liệu duy nhất** so với mockup KH — cần nêu rõ khi gửi, vì các trường còn lại đều giữ nguyên như đã duyệt. Lý do: từ 01/07/2025 Việt Nam bỏ cấp huyện, địa chỉ hành chính chỉ còn tỉnh/thành → phường/xã.

Kéo theo: dữ liệu địa chỉ lưu xuống chỉ còn 2 cấp — cần thống nhất với dev trước khi thiết kế bảng, và chốt xem đơn hàng cũ (nếu có dữ liệu chuyển đổi) xử lý cấp huyện thế nào.

## 5. Nền trang

Nền trang đổi sang `--warm-50` = `#FAF8F3` (lấy từ `prototype-v2/css/tokens.css`), thẻ và ô nhập giữ trắng `#FFFFFF` — tạo nhịp xen kẽ ấm / trắng thay vì trắng trên trắng.

| Màn | Trước | Sau |
|---|---|---|
| A1 · C1 | `rgba(170,170,170,.05)` | `#FAF8F3` |
| A3 | `#FFFFFF` | `#FAF8F3` |
| A2 · B2 · B3 · B4 | `#FFFFFF` | `#FAF8F3` |
| Thanh trên · thẻ · ô nhập | `#FFFFFF` | giữ nguyên |
| B1 đăng nhập quản trị | `--c3` navy | giữ nguyên |

Kéo theo: 30 thẻ trong mockup KH **chỉ khai báo viền, không khai báo nền** — trên nền trắng cũ thì không lộ, trên nền ấm sẽ bị chìm. Đã cho về trắng (A3 5 thẻ · B2/B3/B4 mỗi màn 8 · A2 1).

Cột biểu đồ hoa hồng đổi sang teal `#1BA3BE` để tách khỏi navy của nút và link — navy là màu hành động, teal là màu dữ liệu.

## 6. Thêm link bán hàng vào A3

Dashboard thành viên trong mockup KH **không có link bán hàng nào**. Agent rời màn "Kích hoạt thành công" (A2 bước 5) là mất đường lấy link, không có chỗ xem lại. Đã thêm thẻ **Link bán hàng của bạn** ngay dưới phần chào, gồm 1 link + nút copy, dùng lại đúng link và hàm `copyLink` sẵn có của A2 bước 5.

**Đã chốt 08/09: 2 link**, đúng theo requirement 8.1.C-4 — agent nhận cả hai ngay lúc kích hoạt (A2 bước 5) và xem lại được ở dashboard (A3), mỗi link một nút copy riêng:

| Link | Giá trị | Dùng để |
|---|---|---|
| Giới thiệu · ref_code | `homi365.vn/san-pham/CN02?aff_id=923983` | gán tuyến trên / tuyển thành viên |
| Mua hàng cá nhân · alias | `homi365.com.vn/NVA1111` | chia sẻ để khách mua trực tiếp |

`ref_code = 923983` là mã chính thức của agent. Alias sinh đúng cú pháp **8.1.C-4**: `Homi365.com.vn/[EEEE][PPPP]` — EEEE là chữ cái đầu (viết hoa, bỏ dấu) của mỗi từ trong họ tên, PPPP là 4 số cuối SĐT. *Nguyễn Văn A* · `0901111111` → `NVA1111`.

Còn treo — **hai link của admin ở màn B2 chưa khớp mô hình này.** B2 hiện hiện *link form* `portal.homi365.com.vn/TTB4123` và *link đăng nhập* `homi365.com.vn/dang-nhap/TTB4123`, cả hai dựng từ alias chứ không có link mua hàng lẫn ref_code. Cần chốt admin nhìn thấy những link nào của agent, và 4 dạng link này rốt cuộc là mấy thứ khác nhau. Prototype giữ nguyên phần B2 như mockup KH.

## 7. Tách hoa hồng theo trạng thái (A3)

Thẻ số dư trong mockup KH chỉ có **2 con số** — khả dụng và "đang chờ duyệt (đã khóa)"; "đã ghi nhận" nằm lẫn trong một dòng chữ nhỏ, "đã rút" nằm tận ô chỉ số phía trên. Đã tách thành **4 mục**:

| Mục | Giá trị mẫu |
|---|---|
| Đã ghi nhận | 6.000.000đ |
| Đang chờ duyệt · tạm giữ | 800.000đ |
| Đã rút | 1.200.000đ |
| **Số dư khả dụng** | **4.000.000đ** |

Số liệu mẫu khớp: `6.000.000 = 4.000.000 + 800.000 + 1.200.000`.

Bổ sung dòng giải thích cơ chế hold: yêu cầu rút ở trạng thái **chờ duyệt** hoặc **đã duyệt** bị tạm giữ và trừ khỏi số dư khả dụng, tới khi chi trả xong hoặc bị từ chối; từ chối thì hoàn lại khả dụng.

"Đã rút" hiển thị ở **2 nơi** — ô chỉ số phía trên (trường của mockup gốc) và thẻ hoa hồng này. **Đã chốt giữ cả hai** (BA quyết 08/09): ô chỉ số cho cái nhìn nhanh, thẻ hoa hồng cho quan hệ giữa 4 con số. Không phải lỗi trùng lặp.

## 8. Bổ sung màn Quản lý sản phẩm (B5)

Mockup KH không có màn này, dù requirement **7.7.1 Logic quản lý sản phẩm** là P0. Đã thêm màn `b5-products.html` trong khung quản trị, kèm mục **Quản lý sản phẩm** ở sidebar.

Nội dung: bảng sản phẩm với 3 cột theo đúng yêu cầu — **Tên · Hình ảnh · Mô tả** — cùng nút *Thêm sản phẩm* và nút *Sửa* trên từng dòng, cả hai mở cùng một hộp thoại 3 trường.

**Đã chốt 08–09/09** — phạm vi màn này đúng bằng 3 trường trên, không hơn: không quản lý giá, không quản lý gói, không có công tắc bật/tắt bán, mỗi sản phẩm **chỉ 1 ảnh**.

Danh sách chỉ có **1 sản phẩm CN02**, đúng theo **6.1.C-3** (*"cho 1 sản phẩm pilot (CN02)"*). Hai lựa chọn *Gói 1 năm 10.000.000đ* và *Gói nửa năm 6.000.000đ* ở màn mua hàng là **gói license của cùng sản phẩm đó**, không phải 2 sản phẩm — khớp với kho B4, nơi cả 1.200 thiết bị đều mang một dòng SKU `CN02-xxxx`.

## 9. Bổ sung Thêm hàng vào kho (B4)

Màn Quản lý kho hàng của mockup KH **chỉ xem, không nhập được hàng** — 1.200 mã trong bản demo là dữ liệu dựng sẵn. Đã thêm nút **+ Thêm hàng vào kho** cạnh nút xuất Excel, mở hộp thoại 2 trường theo yêu cầu: **Mã sản phẩm** và **Mã kích hoạt**. Hàng thêm vào mặc định ở trạng thái *Sẵn hàng*.

**Đã chốt 08/09** — thêm nút **Import hàng loạt** bên cạnh, mở hộp thoại cho chọn file Excel/CSV hoặc dán danh sách, mỗi dòng `mã sản phẩm, mã kích hoạt`.

**Chặn trùng ở cả hai đường nhập:**

- Nhập tay: trùng mã kích hoạt hoặc mã sản phẩm thì báo lỗi ngay trong hộp thoại, không cho lưu.
- Import: xử lý **từng phần** — dòng nào hợp lệ thì nhận, dòng nào trùng hoặc thiếu dữ liệu thì bỏ qua. Kết thúc hiện bảng tổng kết `tổng dòng / đã nhập / bỏ qua` kèm danh sách dòng bị bỏ và lý do.
- Chặn trùng tính cả với kho hiện có **lẫn trùng nhau trong chính danh sách đang dán** — dán 2 dòng cùng mã thì chỉ nhận dòng đầu.

## 10. Bổ sung màn Quản lý đơn hàng (B6)

Mockup KH **không có màn đơn hàng nào**, dù luồng mua của chính mockup là chuyển khoản + khách tự tải ảnh bill lên. Nghĩa là tiền về tài khoản nhưng không ai xác nhận được, đơn treo vĩnh viễn và khách không bao giờ nhận mã kích hoạt. Đây là mắt xích đứt, không phải tính năng phụ.

Màn `b6-orders.html` gồm: 4 ô thống kê (chờ đối soát · chờ Head Admin · đã thanh toán · doanh thu đã đối soát), bộ lọc theo trạng thái, ô tìm theo mã đơn / tên / SĐT, bảng đơn, và ngăn chi tiết bên phải với thông tin khách, thông tin đơn, ảnh chuyển khoản, lịch sử xử lý và nút hành động.

**Duyệt 2 cấp** (theo quyết định 08/09), giống luồng rút tiền:

| Bước | Ai làm | Kết quả |
|---|---|---|
| 1 | Admin Specialist | Xác nhận tiền về → `Chờ Head Admin xác nhận` |
| 2 | Head Admin | Xác nhận → `Đã thanh toán`, hệ thống cấp mã kích hoạt |
| — | Cả hai vai | Từ chối đơn (khi tiền chưa về hoặc sai số tiền) |

Nút bước 2 khoá với vai Specialist và ngược lại — đổi vai bằng nút *Vai trò (demo)* ở cuối sidebar để thử cả hai.

**Đã chốt 08/09:**

- **Tách vai theo bước, không tách theo người.** Specialist làm bước 1; bước 2 thuộc về Head Admin, và Head Admin làm luôn việc kích hoạt tài khoản. Khác luồng rút tiền ở chỗ rút tiền cấm cùng một người làm cả hai bước, còn ở đây phân quyền theo vai là đủ.
- **Mã kích hoạt do Head Admin chọn tay** từ danh sách thả xuống, chỉ liệt kê mã đang ở trạng thái *Sẵn hàng* trong kho (B4). Không chọn thì không xác nhận được. Xác nhận xong mã đó chuyển sang *Đã gán đơn hàng* và ghi vào lịch sử của cả đơn lẫn thiết bị.
- **Đơn bị từ chối là chấm dứt.** Phase 1 không mở lại đơn cũ; khách muốn mua thì đặt đơn mới qua link giới thiệu. Ngăn chi tiết hiển thị rõ dòng này để admin khỏi đi tìm nút mở lại.

- **Hoàn tiền nằm ngoài hệ thống.** Đơn bị từ chối nhưng tiền đã về tài khoản thì bộ phận kế toán xử lý thủ công bên ngoài; hệ thống không có màn hoàn tiền, không lưu trạng thái hoàn tiền, không đối soát khoản hoàn. Dev không cần làm gì cho phần này.

## 11. Bổ sung theo rà soát requirement 09/09

Nguồn: `docs/GAP-Requirement-vs-prototype-v3.md`. Sáu mục nhóm B đã làm xong:

| Mã YC | Bổ sung |
|---|---|
| **7.9.1** | Màn **B7 · Tài khoản admin** — danh sách 5 tài khoản mẫu, cột vai trò (Head Admin / Admin Specialist), khoá–mở khoá, thêm–sửa tài khoản, kèm bảng giải thích quyền của từng vai. |
| **7.1.3** | Đăng nhập bằng SĐT **đã mua hàng nhưng chưa là agent** → tự chuyển sang màn đăng ký và autofill từ đơn cũ (khớp luôn 7.2.8). Thêm dòng gợi ý ngay dưới nút Đăng nhập. |
| **7.5.2** | Thêm khối **Lịch sử thăng/giáng hạng** vào ngăn chi tiết thành viên. |
| **7.5.2** | Cây tuyến mở rộng lên **3 cấp** F0 → F1 → F2. |
| **7.3.2** | Dashboard thêm bộ chọn **Hôm nay / Tuần này / Tháng này / Tất cả**, số Tổng đơn hàng đổi theo. |
| **7.9.4** | Nhãn trạng thái duyệt hiện rõ số lượt: **Chờ duyệt (0/2)** · **Chờ Head Admin (1/2)** · **Đã duyệt (2/2)**. |

Chưa làm, chờ KH quyết — xem mục A3 của file rà soát: theo **7.9.2** agent đăng ký xong phải ở trạng thái *Chờ duyệt* chứ không vào thẳng dashboard như mockup KH. Sửa chỗ này kéo theo cả màn A2, luồng duyệt và cách tính hoa hồng lúc chờ, nên chưa đụng vào.

## 12. Sửa theo rà soát bản deploy 09/09

Nguồn: `docs/AUDIT-deploy-vs-requirement.md`.

| Mã YC | Đã sửa |
|---|---|
| **7.2.2** | **Autofill khi đăng ký ngay sau khi mua.** Nút *Đăng ký thành viên* ở modal thanh toán thành công giờ mang toàn bộ thông tin người mua sang màn A2 (họ tên, SĐT, email, CCCD, địa chỉ, ngày sinh, số tài khoản, mã đơn, hạng tuyến trên). Trước đó form mở ra trống trơn — lỗi phát sinh do tách mỗi màn một file. |
| **7.9.1** | **Chặn Admin Specialist khỏi màn Tài khoản admin.** Mục *Tài khoản admin* biến mất khỏi sidebar khi đang ở vai Specialist; vào thẳng URL thì ra màn **403**. |
| **7.3.3** | Thêm dòng **còn thiếu bao nhiêu đơn để lên hạng kế tiếp** ngay dưới ô *Hạng hiện tại*. |
| **7.3.2** | Thêm mốc **Khoảng ngày…** mở ra 2 ô chọn ngày và nút Áp dụng, cạnh 4 mốc có sẵn. |
| **7.5.2** | Cây tuyến **3 cấp** F0 → F1 → F2 giờ mới thật sự chạy — bản vá dữ liệu trước đó đặt nhầm vào nhóm xử lý markup nên chưa từng có hiệu lực. Tiêu đề đổi thành *Sơ đồ tuyến dưới (3 cấp)*. |
| — | Thay hết **Medigo** còn sót thành **HOMI365** (điều khoản T&C, câu chúc mừng ở A2, lời chào ở A3, tiêu đề đăng nhập quản trị). |
| — | Sửa nhãn **Bước 1/3 → Bước 1/5** ở màn đăng ký cho khớp số bước thật. |

### Ba điểm đã chốt 09/09 — requirement phải sửa theo

Cả ba quyết định đều **giữ nguyên hành vi prototype**, nhưng **trái với Acceptance Criteria trong sheet**. Không sửa sheet thì dev đọc spec sẽ code ra thứ khác với bản KH đã duyệt.

**1. Duyệt 2 lớp tách theo VAI TRÒ** (Specialist bước 1 · Head Admin bước 2). Cần sửa 3 dòng:

- `7.9.2 AC` đang ghi *"lượt 1: bất kỳ Admin Specialist hoặc Head Admin nào"* và *"lượt 2 phải do người KHÁC"* → viết lại thành tách theo vai trò.
- `7.9.3 AC` đang ghi *"2 người khác nhau, hoặc Head Admin tự chốt"* → bỏ vế Head Admin tự chốt.
- `7.9.4 AC` đang ghi *"nút Xác nhận của chính người đó bị vô hiệu hoá"* → đổi thành khoá theo vai trò.

Rủi ro vận hành cần KH biết trước: **Specialist nghỉ là mọi thứ nghẽn ở bước 1**, kể cả khi Head Admin đang trực. Requirement bản cũ thiết kế để tránh đúng chuyện này. Nếu KH muốn chặn rủi ro mà vẫn giữ tách vai trò, cách gọn nhất là thêm một câu: *Head Admin được phép làm thay bước 1 khi cần*.

**2. Tuyến trên hạng Đồng → báo lỗi** (không giấu lời mời). `7.2.1 AC` đang ghi ngược lại (*"không hiển thị thông báo cho đăng ký thành viên, mà chỉ báo đơn hàng thành công"*) → phải viết lại cho khớp dòng *Logic điều kiện đăng ký thành viên mới*.

Đã chỉnh prototype: báo lỗi **ngay khi bấm** nút Đăng ký thành viên, thay vì để khách điền hết 5 bước rồi mới chặn ở bước cuối.

**3. Agent sau đăng ký vào thẳng dashboard**, không qua *Chờ duyệt (0/2)*. `7.9.2` đang bắt hồ sơ đăng ký phải đủ 2 lượt xác nhận mới kích hoạt → phải bỏ phần đăng ký ra khỏi phạm vi duyệt 2 lớp, chỉ giữ cho rút tiền và đơn hàng.

**Cơ chế tạm giữ hoa hồng — chốt 09/09.** Đăng ký xong là **active ngay**, nhưng kích hoạt của admin mới mở khoá phần tiền:

| | Sau khi đăng ký | Sau khi admin kích hoạt |
|---|---|---|
| Link giới thiệu & link mua hàng | có, dùng được ngay | có |
| Bán hàng, ghi nhận đơn & tuyến dưới | bình thường | bình thường |
| Hoa hồng phát sinh | **tạm giữ** | được giải phóng |
| Điểm tích luỹ | **không cộng** (= 0) | cộng đủ, kể cả phần trước đó |
| Rút tiền | **không được** | được |

Đã dựng vào prototype:

- A2 bước 5: đổi *"Kích hoạt thành công · đã chính thức là seller"* → **"Đăng ký thành công"** kèm câu giải thích hoa hồng bị giữ.
- A3 agent mới: thay banner chào mừng bằng khối **CHỜ KÍCH HOẠT** — nêu rõ bán được ngay nhưng hoa hồng tạm giữ, chưa tính điểm, chưa rút được; hiện số **hoa hồng đang tạm giữ** và **số dư khả dụng 0đ**; nút rút tiền để trạng thái khoá.
- Điểm tích luỹ của agent chưa kích hoạt đổi từ 80 về **0**.

Nhờ vậy màn duyệt hồ sơ ở B2 vẫn có lý do tồn tại: nó là chỗ mở khoá tiền, không phải chỗ cho phép bán hàng.

Còn phải chốt với dev: khi admin kích hoạt, phần hoa hồng đã giữ được cộng dồn **toàn bộ về quá khứ** hay chỉ tính từ thời điểm kích hoạt trở đi — bản này đang mô tả theo hướng cộng dồn toàn bộ.

## Ghi chú

- Nút **Thanh toán** ở màn A1 trong mockup KH đang để nền đỏ `#EE0000` nhưng màu hover lại là cyan `#0099d1` — gần như chắc chắn là lỗi sót. Bản này đưa về màu chính. Cần KH xác nhận.
- Điều hướng giữa các màn đổi từ `setState` sang chuyển file thật, vì mỗi màn giờ là một file `.html` riêng. Dữ liệu mang sang màn sau đi qua `sessionStorage`.
- Thêm vòng focus bàn phím (WCAG 2.4.7) — không ảnh hưởng layout.
