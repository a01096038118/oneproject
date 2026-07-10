from ultralytics import YOLO

def start_training():
   
    model = YOLO('yolov8n.pt') 
    # model = YOLO(r'C:\Alot1team\project\troubleshooting\yolo_trainning\results\my_experiment_v1-5\weights\last.pt')
  
    model.train(
        data=r'C:\Alot1team\project\troubleshooting\yolo_trainning\data.yaml', 
        epochs=120,
        imgsz=640,
        patience=90,
        augment=True,        # 증강 활성화
        mosaic=0,
        degrees=5,        # 회전 적용
        perspective=0.001,   # 원근 변환 적용
        shear=0,           # 기울기 적용
        fliplr=0,           # 좌우 대칭
        batch=16,
        project=r'C:\Alot1team\project\troubleshooting\yolo_trainning\results',  
        name='my_experiment_v1'                 
    )

if __name__ == '__main__':

    # model = YOLO(r'C:\Alot1team\project\troubleshooting\yolo_trainning\results\my_experiment_v1-5\weights\last.pt')
    # model.train(resume=True)

    start_training()


    

    
