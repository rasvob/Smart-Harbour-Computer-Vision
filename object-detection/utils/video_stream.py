import cv2

class VideoStream():
    def __init__(self, video_name:str):
        self.video_name = video_name
        self.cap = cv2.VideoCapture(self.video_name)
        self.frame_id = -1

    def __iter__(self):
        return self

    def __next__(self):
        ret, frame = self.cap.read()
        if ret:
            self.frame_id += 1
            return frame
        else:
            raise StopIteration

    def __len__(self):
        return int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def __getitem__(self, idx):
        for _ in range(idx - self.frame_id):
            ret, frame = self.cap.read()
        if ret:
            self.frame_id = idx
            return frame
        else:
            raise IndexError

    def __del__(self):
        self.cap.release()