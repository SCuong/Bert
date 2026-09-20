---
description: Autonomous overnight execution protocol for iterative review-loop development
globs: ["*"]
---

# Autonomous Overnight Execution Protocol

Quy định bắt buộc đối với Agent trong chế độ autonomous overnight tại workspace `A:\Bert`.

## 1. Bounded Phase & Scope

* Mỗi `docs/NEXT_TASK.md` được gửi đến là một **bounded phase** riêng biệt.
* Agent **CHỈ** thực hiện đúng phạm vi và các yêu cầu được mô tả trong task hiện tại.
* Tuyệt đối không tự ý làm trước các phase sau, không tự ý huấn luyện mô hình khi task chưa cho phép.
* Tuyệt đối không bịa đặt số liệu, metrics, đồ thị hoặc artifacts giả định. Mọi kết quả phải xuất phát từ thực thi thực tế.
* Tuyệt đối không sao chép/tái sử dụng implementation từ tài liệu tham khảo của giảng viên (`Bài giảng/`, `Báo cáo bài tập lớn/`, `AI.Code/`, `NLP_Demo/`).

## 2. Git & An Toàn Mã Nguồn

* **KHÔNG** sử dụng `git push --force` hoặc bất kỳ cờ ép buộc nào.
* **KHÔNG** sử dụng `git reset --hard`.
* **KHÔNG** tự ý xóa hoặc hoàn tác các thay đổi chưa commit trừ khi được chỉ định rõ.
* Trước khi commit, luôn kiểm tra `git status` và `git diff` để đảm bảo chỉ commit các file thuộc phạm vi task.
* Không commit file trong `.agents/runtime/`, dữ liệu tạm, checkpoints hoặc cache.

## 3. Quy Trình Kết Thúc Mỗi Phase

Khi hoàn thành tất cả các mục trong `docs/NEXT_TASK.md`:

1. **Chạy Verification:** Thực hiện đầy đủ các lệnh kiểm tra, test, lint hoặc smoke-check được yêu cầu trong task.
2. **Kiểm tra Git Diff:** Chạy `git diff` và `git status` để rà soát thay đổi.
3. **Commit Implementation:** Commit toàn bộ thay đổi mã nguồn/tài liệu với message theo chuẩn quy định của task.
4. **Push:** Đẩy commit lên branch `main` (`git push origin main`).
5. **Lấy Commit SHA:** Chạy `git rev-parse HEAD` để lấy commit SHA vừa push.
6. **Tạo / Cập Nhật `docs/REVIEW_REQUEST.md`:** Ghi nhận báo cáo review theo format chuẩn bên dưới.
7. **Commit & Push REVIEW_REQUEST:** Commit `docs/REVIEW_REQUEST.md` và push lên `origin/main` (hoặc push cùng đợt nếu cập nhật trước khi push).
8. **Dừng (Stop):** Ngừng gọi công cụ và kết thúc turn để Stop hook kích hoạt, chờ sidecar phát hiện `NEXT_TASK.md` tiếp theo.

## 4. Định Dạng Chuẩn Của `docs/REVIEW_REQUEST.md`

```text
request_commit_sha: <SHA của implementation cần review>
status: READY_FOR_REVIEW

# Summary
<Tóm tắt các công việc và thay đổi đã thực hiện>

# Verification
<Chi tiết các lệnh kiểm tra đã chạy và kết quả đầu ra thực tế>

# Files Changed
<Danh sách các file đã tạo, sửa đổi hoặc xóa>

# Known Issues
<Các vấn đề tồn đọng hoặc cần lưu ý (nếu có)>

# Proposed Next Phase
<Đề xuất bước tiếp theo cho reviewer>
```

## 5. Xử Lý Khi Gặp Blocker (Safety Fallback)

Nếu gặp các tình huống sau:
* Merge conflict;
* File chưa commit không rõ nguồn gốc;
* Lỗi xác thực Git (authentication error);
* Lặp lại cùng một lỗi >= 3 lần không khắc phục được an toàn;
* Yêu cầu xóa dữ liệu nguy hiểm;
* Thay đổi file ngoài phạm vi project không liên quan;
* Blocker cần quyết định chủ quan của người dùng;

**Quy tắc:**
* **KHÔNG** tự ý đoán hoặc thực hiện hành động mạo hiểm.
* Tạo / cập nhật `docs/REVIEW_REQUEST.md` với:
  `status: BLOCKED`
* Ghi rõ nguyên nhân bị block trong mục `# Known Issues`.
* Commit và push `docs/REVIEW_REQUEST.md` nếu an toàn, sau đó **DỪNG (Stop)** conversation ngay lập tức để người dùng can thiệp.
