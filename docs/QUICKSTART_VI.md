# Bắt đầu sử dụng

## 1. Chọn đúng branch và môi trường

Branch tích hợp là main_sub. Chạy từ thư mục chứa ppe.py, không phải thư mục
bytetrack_ppe. Nếu đã có repo và có sửa đổi chưa lưu, kiểm tra git status trước
khi đổi branch.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python ppe.py test -q
```

Khuyến nghị Python 3.11/3.12 cho cài mới. Các lock/bootstrap Python 3.14 bên
trong bytetrack_ppe là môi trường lịch sử riêng, không cần làm cả hai cách.
Không cần train lại để inference nếu đã có checkpoint tương thích.

## 2. Chạy giao diện

Terminal thứ nhất:

```powershell
python ppe.py review-api
```

Terminal thứ hai, kích hoạt cùng môi trường:

```powershell
python ppe.py dashboard
```

Mở http://localhost:8501; API URL là http://127.0.0.1:5000.
Fresh clone chưa có dữ liệu publish nên /api/health trả 503 là dự kiến.
Giao diện vẫn mở được. Trước khi tạo job, đặt checkpoint bốn lớp tại
bytetrack_ppe/weights/candidates/CHVG4-best.pt. Job UI chưa có lựa chọn
model/device và dùng mặc định của runner, gồm CPU.
--model trong một lần chạy CLI không đổi model của job UI.
Không mở server này ra Internet.

## 3. Chạy thử video

Chuẩn bị video và weight riêng; thay hai đường dẫn ví dụ bằng file của bạn:

```powershell
python ppe.py infer --video "C:\videos\test.mp4" --model "C:\models\ppe.pt" --max-frames 30 --device cpu --run-name test-01
```

Model phải đúng thứ tự person, head, helmet, vest. File best.pt không tự cho
biết model gì; cần xem class mapping và thông tin bàn giao.
Kết quả nằm trong bytetrack_ppe/outputs/runs/test-01/.
Lần chạy trên không thay dữ liệu đang hiển thị ở dashboard và không gửi W&B.
Lần chạy CLI không tự xuất hiện trong danh sách job của dashboard: xem file ở
thư mục output được in ra. Preview/publish tương tác trên UI dành cho job tạo
bằng ứng dụng. Dùng run-name mới cho lần thử tiếp.

## 4. Chọn phần khác

| Nhu cầu | Lệnh |
| --- | --- |
| Xem tất cả điểm vào | python ppe.py --help |
| W&B inference | python ppe.py wandb --help |
| Association riêng | python ppe.py association --help |
| Research Event Engine | python ppe.py event-video --help |
| Chuyển dataset 4 lớp | python ppe.py convert --help |
| Kiểm tra dataset | python ppe.py validate --help |
| CHVG4 baseline training | python ppe.py train --help |

Root config.yaml chỉ thuộc research runtime, không điều khiển review pipeline.
Workflow train cuối YOLO26L khác với lệnh train baseline; đọc
[hướng dẫn chọn workflow](TRAINING_PATHS.md).

Xem [CLI](CLI.md), [kiểm thử](TESTING.md) và [xử lý lỗi](TROUBLESHOOTING.md).
