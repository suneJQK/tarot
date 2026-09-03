# 🔮 Sensual Tarot 78

Bộ 78 lá bài Tarot phong cách gothic fine-art, đồng nhất theo style anchor
**`cards/17-the-star.png`** — khung viền vàng Gothic trên giấy da cổ, tỉ lệ dọc 7:12.

## Quy trình tạo lá bài

Xem chi tiết tại **[WORKFLOW.md](WORKFLOW.md)**. Tóm tắt:

```bash
python3 build_prompt.py --list              # liệt kê 78 lá
python3 build_prompt.py 03-empress          # ghép prompt cho 1 lá
python3 build_prompt.py --all -d prompts/   # ghép đủ 78 prompt
```

Sinh ảnh với 2 ảnh tham chiếu theo đúng thứ tự:
**#1 `cards/card-blank.png`** (khung) → **#2 `cards/17-the-star.png`** (style),
rồi chạy QA checklist (khung · huy hiệu · tên · count-lock · anatomy-lock) trước khi
lưu vào `cards/{slug}.png`.

## Cấu trúc

| Đường dẫn | Vai trò |
|---|---|
| `cards/` | Ảnh lá bài + 2 file chuẩn (`card-blank.png`, `17-the-star.png`) |
| `tarot prompt/template.md` | Master prompt template (5 placeholder) |
| `tarot prompt/cards.json` | Dữ liệu 78 lá (scene, emblem, count-lock…) |
| `tarot prompt/00-MASTER-PROMPT.md` | 3 quy chuẩn cứng: Visual Anchor · Anatomy Lock · 4-Layer Depth |
| `tarot prompt/01-CARD-TABLE.md` | Bảng chuẩn 72 nhân vật (bản mới nhất — dùng bản này) |
| `tarot prompt/02-CHARACTER-SPECS.md` | Bản cũ, chỉ tham khảo — không dùng để sinh ảnh |
| `build_prompt.py` | Công cụ ghép prompt tự động |
| `WORKFLOW.md` | Quy trình tạo lá bài đầy đủ (SOP 9 bước) |
