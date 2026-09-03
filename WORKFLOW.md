# 🔮 QUY TRÌNH TẠO LÁ BÀI TAROT — SENSUAL TAROT 78

> Quy trình chuẩn (SOP) để tạo bất kỳ lá nào trong bộ 78 lá, đồng nhất 100% với
> style anchor **`cards/17-the-star.png`**. Tuân thủ 3 "luật cứng":
> **Visual Anchor (The Star) · Anatomy Lock · Count Lock**.

---

## 0. SƠ ĐỒ PIPELINE

```
 cards.json ────────┐
 (scene, emblem,    │
  count-lock, age)  │   ┌────────────────┐    ┌──────────────────────┐
                    ├──▶│ build_prompt.py│──▶ │ PROMPT HOÀN CHỈNH    │
 01-CARD-TABLE.md ──┤   │  (merge + điền │    │ (5 placeholder đã    │
 (72 nhân vật: mắt, │   │   template.md) │    │  điền đủ dữ liệu)    │
  da, dáng A–D…)    │   └────────────────┘    └──────────┬───────────┘
                    │                                    │
 template.md ───────┘                                    ▼
                                          ┌──────────────────────────────┐
   2 ẢNH THAM CHIẾU ─────────────────────▶│ SINH ẢNH (image model,       │
   #1 cards/card-blank.png  (khung)       │  edit mode, tỉ lệ 7:12)      │
   #2 cards/17-the-star.png (style)       └──────────┬───────────────────┘
                                                     ▼
                                          ┌──────────────────────┐
                                          │ QA CHECKLIST (§6)    │── FAIL ──▶ vẽ lại
                                          │ khung/huy hiệu/tên/  │            (ghi chú lỗi
                                          │ count/anatomy/spec   │            vào layout như
                                          └──────────┬───────────┘            swords-07/08)
                                                PASS ▼
                                          lưu cards/{slug}.png
```

## 1. VAI TRÒ CÁC FILE NGUỒN

| File | Vai trò trong pipeline |
|---|---|
| `cards/17-the-star.png` | **Style anchor duy nhất** — chuẩn viền vàng Gothic, medallion oval, banner tên, ánh sáng, độ chi tiết. Luôn gửi ở **vị trí tham chiếu #2**. |
| `cards/card-blank.png` | **Khung bài trống** — layout nền giấy da cổ + viền. Luôn gửi ở **vị trí tham chiếu #1**. |
| `tarot prompt/template.md` | Master prompt — 5 placeholder cần điền: `{TITLE} {EMBLEM} {SCENE} {CHARACTER_SPECIFICATION} {COUNT_LOCK}`. Đã tích hợp sẵn STRICT ANATOMY. |
| `tarot prompt/cards.json` | Dữ liệu gốc 78 lá: `slug · group · emblem · title · femme · count · scene · hair · age · build · allure`. `count=null` → phát no-suit lock. |
| `tarot prompt/01-CARD-TABLE.md` | **Bảng chuẩn 72 nhân vật (bản MỚI NHẤT)**: tuổi · mắt · tóc · vóc dáng A–D · da (10 tông sáng) · nét riêng · không khí. |
| `tarot prompt/02-CHARACTER-SPECS.md` | ⚠️ Bản cũ (còn từ ngữ "chiến binh/cơ bắp" đã bị loại) — **chỉ tham khảo lịch sử, KHÔNG dùng để sinh ảnh**. |
| `build_prompt.py` | Công cụ ghép prompt tự động từ 3 nguồn trên. |

## 2. BƯỚC 1 — CHỌN LÁ & TRÍCH DỮ LIỆU

- Liệt kê 78 lá: `python3 build_prompt.py --list`
- 72 lá có nhân vật nữ (`femme: true`) + 6 lá vật thể thuần (`femme: false`):
  `wands-ace · wands-08 · cups-ace · swords-ace · swords-03 · pentacles-ace`.

## 3. BƯỚC 2 — GHÉP `CHARACTER_SPECIFICATION`

**Nguồn ưu tiên 1**: dòng tương ứng trong `01-CARD-TABLE.md`, ghép theo thứ tự:
`{tuổi} years old` + `{vóc dáng A–D}` + `{kiểu tóc}` + `{đôi mắt}` + `{màu da}` + `{nét riêng}` + `{không khí}`.

**Luật cứng khi ghép:**
1. **Tuổi & tóc giữ nguyên 100%** so với bảng chuẩn — không được sáng tác lại.
2. **Da**: chỉ 10 tông sáng (`porcelain → amber-gold`), luôn nhấn *(light tone only — never dark)*.
3. **Vóc dáng**: trần là "trung bình" (cấp D) — không plus-size; tuyệt đối không dùng từ ngữ mạnh mẽ (*warrior, muscular, broad shoulders, commanding…* — đã bị loại khỏi dự án).
4. **Nét riêng (signature)**: đúng 1 chi tiết/lá, không trùng giữa các nhân vật.
5. Nếu `cards.json` có trường `allure` → nối nguyên văn đoạn `allure` vào cuối spec.
6. Lá vật thể (`femme: false`) → thay toàn bộ spec bằng: *"There is no character on this card — a pure object scene."*

## 4. BƯỚC 3 — GHÉP `COUNT_LOCK` (KHÓA SỐ LƯỢNG)

| Trường hợp trong `cards.json` | Count Lock phát ra |
|---|---|
| `count: null` | *"COUNT LOCK (HARD): this card shows NO suit objects anywhere…"* |
| `count: {n, obj, layout}` | `COUNT LOCK (HARD): {layout}` — **giữ nguyên văn**, kể cả các cảnh báo lỗi cũ (vd: `swords-07` từng vẽ nhầm 9 kiếm; `swords-08` từng thừa 1 kiếm). |

> Count Lock là **ràng buộc cứng** — QA bước 6 sẽ đếm lại từng vật trên ảnh.

## 5. BƯỚC 4–5 — ĐIỀN TEMPLATE & SINH ẢNH

**Ghép prompt tự động:**

```bash
python3 build_prompt.py 03-empress            # in ra stdout
python3 build_prompt.py 03-empress -o empress.txt
python3 build_prompt.py --all -d prompts/     # sinh đủ 78 file
```

**Sinh ảnh** — dùng image model ở chế độ edit/tham chiếu với **đúng thứ tự 2 ảnh**:

1. Ảnh #1 = `cards/card-blank.png` *(khung & bố cục)*
2. Ảnh #2 = `cards/17-the-star.png` *(style anchor)*

Gửi prompt đã điền + câu khai báo vai trò ảnh, vd:

> *"Image 1 is the blank card template (frame layout). Image 2 is THE STAR — the style anchor for border, oval medallion, ribbon banner, lighting and detail quality. Keep the portrait 7:12 aspect ratio."* + `[prompt từ build_prompt.py]`

## 6. BƯỚC 6 — QA CHECKLIST (bắt buộc trước khi chốt)

| # | Tiêu chí | PASS khi |
|---|---|---|
| 1 | **Khung viền** | Viền vàng Gothic mỏng, đối xứng, hoa văn góc giống The Star; nền giấy da cổ. |
| 2 | **Huy hiệu** | Oval medallion đỉnh chứa đúng `emblem` mạ vàng phát sáng. |
| 3 | **Tên lá** | Banner đáy ghi đúng `title`, chữ vàng antique, không sai chính tả. |
| 4 | **Count Lock** | Đếm tay số vật suit trên ảnh = đúng `count.n` (hoặc 0 nếu `count=null`). |
| 5 | **Anatomy Lock** | Mỗi nhân vật: đúng 2 tay · 2 chân · 1 đầu · 1 thân; khớp nối tự nhiên; không thừa/thiếu chi, không chi dính sườn/hông/ngực; ngón tay đúng số. Thấy 3 tay / tay dính thân / sai khớp → **VẼ LẠI**, không chấp nhận bản lỗi. |
| 6 | **Spec khớp bảng** | Tuổi cảm nhận 18–25 · đúng mắt/tóc/da/nét riêng trong `01-CARD-TABLE.md`. |
| 7 | **Da** | Thuộc 10 tông sáng — không da sẫm/đen kể cả vùng bóng. |
| 8 | **Chiều sâu 4 lớp** | Cảnh tràn mép trong, viền vàng + medallion + banner đè lên trên mép cảnh. |
| 9 | **Tỉ lệ & tông** | Dọc 7:12, ánh sáng ấm fine-art, chi tiết sắc nét ngang The Star. |

**FAIL bất kỳ mục nào** → vẽ lại; nếu lỗi lặp lần 2 → vá `count.layout`/scene trong `cards.json` bằng cảnh báo chống lỗi cụ thể (theo mẫu `THIS CARD HAS ALREADY FAILED…` như `swords-07`, `swords-08`) rồi sinh lại prompt.

## 7. BƯỚC 7 — LƯU TRỮ

- Tên file: **`cards/{slug}.png`** (vd: `cards/wands-ace.png`) — slug = khóa duy nhất xuyên suốt json/bảng/script.
- Không sửa lại `17-the-star.png` và `card-blank.png` (2 file chuẩn của pipeline).

## 8. CHẠY BATCH 78 LÁ

```bash
python3 build_prompt.py --all -d prompts/     # 1) sinh 78 prompt
#  2) với từng prompts/{slug}.txt → sinh ảnh (Bước 5) → QA (Bước 6) → lưu cards/{slug}.png
#  3) ghi trạng thái từng lá: PASS / FAIL-lần-n / ghi chú lỗi
```

Nên chạy theo nhóm: `major (22) → wands (14) → cups (14) → swords (14) → pentacles (14)`,
ưu tiên trước các lá có `emblem`/count-lock phức tạp (`swords-07`, `swords-08`, `wands-10`, `pentacles-10`) để vá layout sớm.

## 9. VÍ DỤ END-TO-END — ACE OF WANDS

```bash
$ python3 build_prompt.py wands-ace
```

- `{TITLE}` = `ACE OF WANDS` · `{EMBLEM}` = `one leafy wand`
- `{CHARACTER_SPECIFICATION}` = *"There is no character on this card — a pure object scene."* (vì `femme: false`)
- `{COUNT_LOCK}` = *"exactly one wand, sprouting and alive, held by the divine hand; no second staff anywhere, not even in the landscape"*
- Kết quả mẫu đã sinh theo quy trình này: **`cards/wands-ace.png`** ✅
