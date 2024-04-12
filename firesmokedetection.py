import cv2
import os
from datetime import datetime
from ultralytics import YOLO

# 加载YOLOv8模型
model = YOLO('./best.pt')

# 打开视频文件
# video_path = "path/to/your/video/file.mp4"
cap = cv2.VideoCapture(0)  # 0表示默认摄像头，如果有多个摄像头，可以尝试使用1, 2, cdc等

# 创建保存视频帧的文件夹
save_folder = './detect_results/'
os.makedirs(save_folder, exist_ok=True)

folder_count = 1
while os.path.exists(os.path.join(save_folder, str(folder_count))):
    folder_count += 1

save_folder = os.path.join(save_folder, str(folder_count))
os.makedirs(save_folder)

# 视频帧计数器
frame_count = 0

# 视频帧宽高
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 视频帧写入对象
out = cv2.VideoWriter(os.path.join(save_folder, 'output.mp4'), cv2.VideoWriter_fourcc(*'XVID'), 30,
                      (frame_width, frame_height))

# 遍历视频帧
while cap.isOpened():
    # 从视频中读取一帧
    success, frame = cap.read()

    if success:
        # 在该帧上运行YOLOv8推理
        results = model(frame)

        # 在帧上可视化结果
        annotated_frame = results[0].plot()

        # 保存视频帧
        cv2.imwrite(os.path.join(save_folder, f'{frame_count}.jpg'), annotated_frame)

        # 写入视频
        out.write(annotated_frame)

        # 显示带注释的帧
        cv2.imshow("YOLOv8推理", annotated_frame)

        # 如果按下'q'则中断循环
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        # 计数器自增
        frame_count += 1
    else:
        # 如果视频结束则中断循环
        break

# 释放视频捕获对象、关闭视频写入对象、关闭显示窗口
cap.release()
out.release()
cv2.destroyAllWindows()
