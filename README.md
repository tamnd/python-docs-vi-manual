# Bản dịch tiếng Việt tài liệu Python

> [!WARNING]
> **This repository contains machine translations for reference only.**
> Do not copy these strings directly into
> [tamnd/python-docs-vi](https://github.com/tamnd/python-docs-vi) — all
> translations there **must be human translations** submitted through
> [Transifex](https://explore.transifex.com/python-doc/python-newest/).
> Use this repo only as a starting-point reference or to compare coverage.

Kho lưu trữ các tập tin `.po` của bản dịch tiếng Việt tài liệu chính thức
Python, tuân theo quy trình được mô tả trong
[PEP 545](https://peps.python.org/pep-0545/).

Nhánh `main` hiện đang theo dõi tài liệu Python **3.14**.

## Thỏa thuận đóng góp tài liệu

> NOTE REGARDING THE LICENSE FOR TRANSLATIONS: Python's documentation is
> maintained using a global network of volunteers. By posting this project
> on Transifex, GitHub, and other public places, and inviting you to
> participate, we are proposing an agreement that you will provide your
> improvements to Python's documentation or the translation of Python's
> documentation for the PSF's use under the CC0 license (available at
> https://creativecommons.org/publicdomain/zero/1.0/legalcode). In return,
> you may publicly claim credit for the portion of the translation you
> contributed and, if your translation is accepted by the PSF, you may
> (but are not required to) submit a patch including an appropriate
> annotation in the TRANSLATORS file. Although nothing in this
> Documentation Contribution Agreement obligates the PSF to incorporate
> your textual contribution, your participation in the Python community
> is welcomed and appreciated.
>
> You signify acceptance of this agreement by submitting your work to the
> PSF for inclusion in the documentation.

## Cách đóng góp

Xem [CONTRIBUTING.md](CONTRIBUTING.md) và [GLOSSARY.md](GLOSSARY.md) trước
khi chạm vào tập tin `.po` đầu tiên. Tóm tắt:

1. Fork kho này và clone về máy.
2. Tạo nhánh theo tên tập tin bạn định dịch, ví dụ `library-functions`.
3. Cài phần phụ thuộc: `python -m pip install -r requirements-dev.txt`.
4. Mở tập tin `.po` bằng [Poedit](https://poedit.net/) hoặc editor khác.
5. Dịch các chuỗi `msgstr` còn trống. Đừng chỉnh `msgid`. Theo quy ước
   thuật ngữ và văn phong trong [GLOSSARY.md](GLOSSARY.md).
6. `make verifs` để kiểm tra cú pháp và dòng gãy (wrap).
7. Tạo pull request và thêm tên bạn vào tập tin `TRANSLATORS`.

## Lộ trình

Xem [ROADMAP.md](ROADMAP.md) để biết trạng thái hiện tại và các giai đoạn
dịch còn lại. Người đóng góp mới có thể chọn một tập tin ngắn ở giai đoạn
1 hoặc 4 để bắt đầu.

## Dựng tài liệu đã dịch cục bộ

```sh
make
```

Lệnh trên sẽ clone CPython vào `venv/cpython/`, checkout đúng commit đã
được cố định trong `Makefile`, sao chép các tập tin `.po` vào
`locales/vi/LC_MESSAGES/`, rồi chạy Sphinx với `language=vi`. Kết quả
HTML nằm ở `venv/cpython/Doc/build/html/index.html`.

## Cấu trúc kho

Kho chỉ chứa `.po`, phản chiếu cây `Doc/` của CPython:

```
.
├── about.po
├── bugs.po
├── c-api/
├── faq/
├── howto/
├── library/
├── reference/
├── tutorial/
├── whatsnew/
├── Makefile
├── README.md
├── TRANSLATORS
└── spec/0958_python_docs_vi.md
```

## Điều phối viên

- **Duc-Tam Nguyen** – <tamnd@liteio.dev>

Điều phối viên chịu trách nhiệm quản lý nhóm dịch, đảm bảo người đóng
góp hiểu và đồng ý với Thỏa thuận đóng góp tài liệu, và duy trì chất
lượng bản dịch, như mô tả trong PEP 545.

## Giấy phép

Nội dung bản dịch được đóng góp theo giấy phép
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/legalcode),
nhất quán với yêu cầu của PEP 545.
