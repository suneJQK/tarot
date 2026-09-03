# Quy trình Tạo lá bài Tarot (Sensual Tarot 78 Lá)

Quy trình chuẩn hóa để tạo hình và bố cục toàn bộ bộ bài Tarot dựa trên kho tàng quy chuẩn của dự án:

## 1. Cơ sở dữ liệu & Tài liệu chuẩn trong dự án
- **`cards/17-the-star.png`**: Quy chuẩn DUY NHẤT về khung viền ngoài (mạ vàng Gothic mỏng, sắc nét), phông nền giấy da cổ (*aged parchment/vellum*), ánh sáng ấm, phối cảnh thoáng đãng và chiều sâu 4 lớp.
- **`tarot prompt/00-MASTER-PROMPT.md`**: Master Prompt Specification và Master Prompt Template.
- **`tarot prompt/01-CARD-TABLE.md` & `cards.json`**: Bảng thông số chi tiết 78 lá (tên lá, biểu tượng, nhân vật, bối cảnh, độ tuổi, mái tóc, vóc dáng, số lượng đối tượng - `count lock`).
- **`tarot prompt/02-CHARACTER-SPECS.md`**: Quy chuẩn thông số nhân vật (100% nữ, 18-25 tuổi, tông da chuẩn, vóc dáng A-D, quy tắc giải phẫu khắt khe `ANATOMY LOCK`).

---

## 2. Các bước trong Quy trình Tạo lá bài Tarot

### Bước 1: Xác định thông tin lá bài
- Tra cứu lá bài cần tạo trong `cards.json` hoặc `01-CARD-TABLE.md`.
- Lấy thông tin về `{TITLE}`, `{SCENE}`, `{CHARACTER_SPECIFICATION}`, và `{COUNT_LOCK}` (số lượng đối tượng quy định nghiêm ngặt nếu có).

### Bước 2: Xây dựng Prompt theo Master Template
Áp dụng cấu trúc chuẩn từ `00-MASTER-PROMPT.md`:
```text
A single tarot card "{TITLE}" built inside the reference frame, matching the EXACT open window display, scale, and lighting style of THE STAR: keep the intricate thin golden line-art border in vintage gothic style and aged parchment background texture.

At the BOTTOM: inside the ribbon banner, the title "{TITLE}" in clean antique gold lettering.

In the large open center panel (filling the entire inner window edge to edge and bleeding slightly beneath the golden border, matching the open space of The Star without heavy inner arch barriers):
{SCENE}. {CHARACTER_SPECIFICATION} {COUNT_LOCK}

STRICT ANATOMY (HARD RULE): exactly two arms, two legs, one head and one torso per character; every joint must connect naturally to the body — NO extra limbs, NO limbs fused, NO deformed joints, NO wrong finger counts. Keep both arms clearly separated from the torso with visible armpits, elbows and wrists.

Sensual fine-art anatomy, painterly warm lighting against subtle shadows, rich atmospheric perspective and depth, symmetrical golden frame border, perfectly centered, portrait orientation 7:12 aspect ratio, vintage gothic fine-art illustration, high detail.
```

### Bước 3: Tạo hình ảnh bằng AI Model (Image Generation)
- Sử dụng công cụ sinh ảnh (`generate_image`) với `cards/17-the-star.png` làm ảnh tham chiếu (`images` parameter) để đảm bảo tính đồng bộ về khung viền Gothic, chất liệu giấy da, và phong cách hội họa fine-art.
- Lưu ảnh kết quả vào thư mục lưu trữ (`cards2/`).

### Bước 4: Kiểm tra chất lượng (Quality Assurance & Anatomy Lock)
- **Kiểm tra 4 lớp chiều sâu (4-Layer Depth)**: 
  - Lớp 1 (Nền): Giấy da cổ sepia ấm áp.
  - Lớp 2 (Nội dung): Phối cảnh tự nhiên, thoáng đãng, phóng to tràn nhẹ mép trong khung viền.
  - Lớp 3 (Khung viền): Khung viền mạ vàng Gothic mỏng, đối xứng hoàn hảo đè lên trên mép nội dung.
  - Lớp 4 (Tên): Tên lá bài trong băng rôn vàng cổ.
- **Kiểm tra giải phẫu (Anatomy Lock)**: Tối đa 2 tay, 2 chân, 1 đầu, 1 thân. Không dị dạng, không thừa chi, tay chân tách rời tự nhiên.
- **Kiểm tra Count Lock**: Đảm bảo số lượng vật phẩm khớp hoàn toàn với quy định trong `cards.json`.

### Bước 5: Lưu trữ và Cập nhật Version Control
- Lưu các hình ảnh hoàn thiện vào thư mục `cards2/`.
- Commit và push code, tài liệu quy trình, cùng hình ảnh mới lên nhánh làm việc trên GitHub (`arena/01a065f5-tarot`).
