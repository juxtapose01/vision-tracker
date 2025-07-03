import cv2
import mediapipe as mp
import asyncio
import websockets

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
zones = 10  # Divide screen into 10 zones
letters_per_zone = len(letters) // zones

async def track_gaze(websocket):
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        height, width = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark

            left_iris_x = landmarks[474].x * width
            right_iris_x = landmarks[469].x * width
            avg_iris_x = (left_iris_x + right_iris_x) / 2

            zone_width = width / zones
            zone_index = min(int(avg_iris_x // zone_width), zones - 1)

            # Get letter from zone
            start = zone_index * letters_per_zone
            end = min(start + letters_per_zone, len(letters))
            group = letters[start:end]
            selected_letter = group[len(group) // 2]  # pick center letter

            await websocket.send(selected_letter)
            print("👁️ Gaze letter:", selected_letter)

        cv2.imshow("Eye Tracker", frame)
        if cv2.waitKey(5) & 0xFF == 27:  # ESC to quit
            break
        await asyncio.sleep(0.2)
    cap.release()
    cv2.destroyAllWindows()

async def main():
    async with websockets.serve(track_gaze, "localhost", 5678):
        print(" WebSocket server running at ws://localhost:5678")
        await asyncio.Future()

asyncio.run(main())
