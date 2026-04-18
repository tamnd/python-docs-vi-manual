# Hướng dẫn đóng góp

Cảm ơn bạn đã quan tâm đến việc dịch tài liệu Python sang tiếng Việt.
Tài liệu này mô tả quy trình đóng góp vào kho `python-docs-vi`.

## Trước khi bắt đầu

- Đọc [README](README.md), đặc biệt là **Thỏa thuận đóng góp tài liệu**.
  Khi bạn gửi pull request, bạn đã mặc định đồng ý với thỏa thuận đó.
- Đăng nhập GitHub và có sẵn [Git](https://git-scm.com/).
- Cài Python 3.10+ và `pip`.
- Khuyến nghị dùng [Poedit](https://poedit.net/) để chỉnh tập tin `.po`.

## Quy trình

1. **Đặt chỗ** – Mở một issue mô tả tập tin bạn muốn dịch, ví dụ
   `library/functions.po`, để tránh trùng việc với người khác.
2. **Fork & clone** – Fork kho này và clone bản fork của bạn về máy.
3. **Tạo nhánh** – Tên nhánh nên phản ánh tập tin đang dịch, ví dụ
   `library-functions`.
4. **Cài phụ thuộc** – `python -m pip install -r requirements-dev.txt`.
5. **Dịch** – Mở tập tin `.po` và điền các `msgstr` còn trống.
   - Không sửa `msgid` (chuỗi nguồn tiếng Anh).
   - Giữ nguyên các chỉ thị reST (`:func:`, `:mod:`, v.v.).
   - Không thêm `msgid` mới; chúng được CPython sinh tự động.
6. **Kiểm tra** – Chạy `make verifs` để kiểm tra cú pháp và wrap.
7. **Commit & push** – `git add`, `git commit`, `git push`.
8. **Pull request** – Mở PR vào nhánh `main`, tham chiếu issue bạn đã mở.
   Thêm tên bạn vào [TRANSLATORS](TRANSLATORS) nếu muốn được ghi công.

## Quy ước dịch

- Giữ tên hàm, lớp, tham số và các thuật ngữ mã nguồn nguyên tiếng Anh.
- Dịch các cụm kỹ thuật theo `GLOSSARY.md` (sẽ bổ sung sau).
- Giữ khoảng trắng và ký tự đặc biệt giống hệt `msgid`.
- Các chú thích `# fuzzy` do `msgmerge` sinh ra phải được xử lý và xóa
  trước khi commit.

## Báo lỗi

- Lỗi trong **bản dịch**: mở issue tại kho này.
- Lỗi trong **tài liệu gốc tiếng Anh**: báo cho dự án
  [CPython](https://github.com/python/cpython/issues).
