import zmq
import numpy as np
import cv2
import time

# Connect to the Unity ZMQ publisher
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:12345")  # Replace with the appropriate IP and port

# Subscribe to the topics
topics = [b"/car/scan", b"/car/steering", b"/car/vel", b"/car/image_front", b"/car/depth"]
for topic in topics:
    socket.setsockopt(zmq.SUBSCRIBE, topic)

frame_count = 0
start_time = time.perf_counter()

while True:
    # Receive the topic and data
    [topic, data] = socket.recv_multipart()
    
    # Process the received data based on the topic
    if topic == b"/car/image_front":
        frame_count += 1
        image_array = np.frombuffer(data, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        cv2.imshow("Front Image", image)

        # Calculate FPS
        end_time = time.perf_counter()
        time_diff = end_time - start_time
        if time_diff >= 1.0:  # Every second, update the FPS value
            fps = frame_count / time_diff
            print("FPS: ", fps)
            frame_count = 0
            start_time = time.perf_counter()
    # if topic in [b"/car/scan", b"/car/steering", b"/car/vel", b"/car/segment", b"/car/depth"]:
        # Assuming other topics contain string data
        # print(f"Received data for topic {topic.decode()}: {data.decode()}")
    # cv2.waitKey(10)  # Adjust as needed

    # Add more processing if required for other topics

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Clean up
cv2.destroyAllWindows()
socket.close()
context.term()