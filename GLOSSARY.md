# Glossary

Terminology and style rules for the Vietnamese translation. Read this
before touching a `.po` file, and update it whenever a judgment call
comes up during review.

The goal is not to be prescriptive for every word. It is to keep
consistent choices across hundreds of files and dozens of reviewers.
When in doubt, prefer what is already in here; if you disagree, open
a PR that updates the glossary and sweep the affected files.

## Style rules

### Pronoun

Drop the second-person pronoun where Vietnamese grammar allows it. Use
`bạn` only when the text directly addresses the reader in a way that
would feel incomplete without a pronoun (e.g. a call to action, a
tutorial instruction with an implied subject).

Examples:

- `msgid`: "You can create a list by..."
  `msgstr`: "Có thể tạo list bằng..." (dropped pronoun, neutral)
  `msgstr`: "Bạn có thể tạo list bằng..." (acceptable when the tone
  is explicitly addressing the reader)
- `msgid`: "If you find a bug..."
  `msgstr`: "Nếu bạn tìm thấy lỗi..." (keep `bạn`, it is a call to
  action)

Never use `anh`, `chị`, `em`, or other age/gender-specific pronouns.

### Imperative vs. noun form

Section headings and titles use noun form, not imperative. This matches
the Vietnamese convention for reference documentation.

- `msgid`: "Defining Functions"
  `msgstr`: "Định nghĩa hàm" (noun form)
  Avoid: "Hãy định nghĩa hàm" (imperative, too instructional)

Body text may use imperative when it is a direct instruction:

- `msgid`: "Run the command to see the output."
  `msgstr`: "Chạy lệnh để xem kết quả." (imperative is fine here)

### Sentence case

Headings use Vietnamese sentence case: first letter of the heading
capitalized, everything else lowercase unless it is a proper noun or a
code identifier.

- `msgid`: "Dealing with Bugs"
  `msgstr`: "Xử lý lỗi"
  Avoid: "Xử Lý Lỗi" (title case)

### Code, identifiers, file paths

Never translate. Keep them in backticks.

### reST directives

Preserve exactly. `:func:` / `:class:` / `:mod:` / `:ref:` and their
arguments stay identical. Word order in the Vietnamese sentence may
change around them.

### Quotes

Use Vietnamese guillemets `« »` only in prose that already uses them.
For the docs, follow upstream punctuation as-is: if `msgid` uses `"..."`
so does `msgstr`. Do not convert to typographic quotes (`“...”`).

### Numbers and units

Keep Arabic numerals. Do not spell out numbers that are digits in the
source. "32-bit" stays "32-bit".

## Terminology

### Keep in English (do not translate)

These are Python-specific terms where the English word is what
Vietnamese developers actually use, and translating hurts clarity.

| English | Notes |
|---|---|
| list, tuple, dict, set, frozenset | built-in container types |
| str, int, float, bool, bytes, bytearray | built-in scalar types |
| None, True, False | literals |
| iterator, iterable, generator | iteration protocol |
| decorator | `@foo` decorator syntax |
| callable | anything with `__call__` |
| context manager | `with` statement protocol |
| module, package | code organization |
| namespace | scopes, not the same as "vùng tên" in casual usage |
| attribute, method, property | object members; do not translate to "thuộc tính/phương thức" which are heavier and less precise |
| class, instance, object | OOP terms |
| exception | error-handling terms |
| traceback | stack trace |
| comprehension | list/dict/set/generator comprehensions |
| slice, slicing | list/string indexing |
| unpacking, packing | `*args`, tuple unpacking |
| closure | nested-function variable capture |
| thread, process | concurrency primitives |
| socket | networking |
| regex, regular expression | pattern matching |
| docstring | function/class documentation string |
| REPL, prompt | interactive interpreter |
| REPL | `>>>` prompt |
| API, CLI, URL, HTTP, JSON, XML | standard acronyms |
| boolean | the type is `bool` and the adjective is "boolean" |
| Unicode, ASCII, UTF-8 | encoding names |
| path, pathname | file system paths (see also "đường dẫn" below) |

### Translate

These are general computing terms where Vietnamese already has a
settled, widely-understood translation.

| English | Vietnamese |
|---|---|
| documentation | tài liệu |
| example | ví dụ |
| error | lỗi |
| warning | cảnh báo |
| variable | biến |
| value | giá trị |
| expression | biểu thức |
| statement | câu lệnh |
| loop | vòng lặp |
| condition | điều kiện |
| function | hàm |
| parameter | tham số |
| argument | đối số |
| return value | giá trị trả về |
| default value | giá trị mặc định |
| syntax | cú pháp |
| keyword | từ khóa |
| operator | toán tử |
| number | số |
| integer | số nguyên |
| floating-point | dấu phẩy động |
| string | chuỗi (but keep `str` for the type name) |
| character | ký tự |
| byte | byte (kept English) |
| file | tập tin |
| directory, folder | thư mục |
| path | đường dẫn |
| input, output | đầu vào, đầu ra |
| command line | dòng lệnh |
| library | thư viện |
| framework | framework (kept English) |
| implementation | triển khai |
| version | phiên bản |
| release | bản phát hành |
| install, installation | cài đặt |
| import | import (kept, verb form stays English) |
| source code | mã nguồn |
| algorithm | thuật toán |
| data structure | cấu trúc dữ liệu |
| memory | bộ nhớ |
| platform | nền tảng |
| operating system | hệ điều hành |
| developer | lập trình viên |
| user | người dùng |
| environment | môi trường |
| variable (environment) | biến môi trường |
| tutorial | hướng dẫn |
| reference | tham khảo |
| deprecated | không dùng nữa (adjective); có thể dùng "đã bỏ" in past tense |

### Judgment calls

Where the choice depends on context.

- **"You"**: see Pronoun section above.
- **"Simply", "just"**: usually drop in Vietnamese. It reads
  condescending.
- **"Note that..."**: translate to "Lưu ý:", not "Chú ý rằng..." which
  is more awkward.
- **"See X"**: "Xem X".
- **"Returns X"**: use noun form "Trả về X", not "Hàm trả về X".
- **"Raises X"**: "Gây ra X" or "Ném X" — prefer "Gây ra X".
- **"The X function"**: drop the article, just "Hàm X" or keep X in
  code style without "hàm" at all. `:func:\`X\`` handles the hyperlink
  either way.

### Tricky cases

- `async` / `await`: keep English. `asyncio` too.
- `type hint`, `type annotation`: "chú thích kiểu" reads better than
  "gợi ý kiểu".
- `yield`: keep English. Do not translate to "trả ra" or similar.
- `iterable` vs `iterator`: keep both English. They are different
  protocols and Vietnamese has no concise single-word distinction.
- `raise` (exception): keep as a verb; "Gây ra một exception" reads
  better than "Ném một ngoại lệ".
- `with` statement: "câu lệnh `with`" — keep `with` in code style.
- `__init__`, `__call__`, dunders: never translate; wrap in backticks.

## Common MT artifacts to fix during review

These are patterns the Google MT output in PR #1 kept producing. Watch
for them and fix during unfuzzy review.

1. **Over-literal `bạn`.** Google uses it in every sentence. Most can be
   dropped. Keep only where the text is actually addressing the reader.
2. **"Các" noise.** Google inserts `các` before every plural noun. In
   Vietnamese, `các` is often unnecessary and can be dropped ("các
   hàm" → "hàm" when context is clear).
3. **"Việc X"**: Google frequently wraps verbs in `việc X`. Often
   cleaner to use the verb directly: "Việc sử dụng X" → "Sử dụng X".
4. **Literal "rằng".** Google translates "that" as "rằng" even when
   Vietnamese would omit the complementizer. "cho rằng" → "cho là" or
   drop entirely.
5. **Inverted adjective-noun order.** "Python function" → Google gives
   "hàm Python" (correct). But "built-in function" sometimes becomes
   "built-in hàm" which is wrong. Should be "hàm dựng sẵn" or "hàm
   built-in".
6. **Code tokens in awkward positions.** Because placeholders kept
   `:func:\`x\`` intact, Vietnamese word order sometimes leaves the
   token dangling. Rewrite for fluency.

## How to update this file

Open a PR that changes `GLOSSARY.md` in the same commit as whatever
`.po` changes motivated the update. State the motivating file and a
one-line reason. Sweep any other files that the old rule applied to
in the same PR if it is small, or open a follow-up if it is large.

No vote is required for uncontroversial additions (new Python 3.x
keywords, clearly-settled translations). Changes to settled rules in
this file need at least one reviewer from the team.
