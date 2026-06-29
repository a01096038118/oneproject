import cv2

camera = None

def get_frame():

    global camera

    if camera is None:
        return None

    success, frame = camera.read()

    if not success:
        return None

    is_intrusion = False