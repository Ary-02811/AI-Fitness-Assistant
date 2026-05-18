import cv2
import mediapipe as mp
import numpy as np
import time

# =========================
# MediaPipe Setup
# =========================

mp_pose = mp.solutions.pose

pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

mp_draw = mp.solutions.drawing_utils

# =========================
# Angle Calculation
# =========================

def calculate_angle(a, b, c):

    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(
        c[1] - b[1],
        c[0] - b[0]
    ) - np.arctan2(
        a[1] - b[1],
        a[0] - b[0]
    )

    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle

# =========================
# Counters
# =========================

left_reps = 0
right_reps = 0

left_stage = "down"
right_stage = "down"

# =========================
# FPS
# =========================

prev_time = 0

# =========================
# Webcam
# =========================

cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()

    if not success:
        break

    # Mirror effect
    frame = cv2.flip(frame, 1)

    h, w, _ = frame.shape

    # =========================
    # FPS Calculation
    # =========================

    current_time = time.time()

    fps = 0

    if current_time != prev_time:
        fps = int(1 / (current_time - prev_time))

    prev_time = current_time

    # =========================
    # RGB Conversion
    # =========================

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # =========================
    # Pose Detection
    # =========================

    results = pose.process(rgb)

    try:

        landmarks = results.pose_landmarks.landmark

        # ======================================================
        # LEFT ARM
        # ======================================================

        left_shoulder = [
            landmarks[
                mp_pose.PoseLandmark.LEFT_SHOULDER.value
            ].x,

            landmarks[
                mp_pose.PoseLandmark.LEFT_SHOULDER.value
            ].y
        ]

        left_elbow = [
            landmarks[
                mp_pose.PoseLandmark.LEFT_ELBOW.value
            ].x,

            landmarks[
                mp_pose.PoseLandmark.LEFT_ELBOW.value
            ].y
        ]

        left_wrist = [
            landmarks[
                mp_pose.PoseLandmark.LEFT_WRIST.value
            ].x,

            landmarks[
                mp_pose.PoseLandmark.LEFT_WRIST.value
            ].y
        ]

        left_angle = calculate_angle(
            left_shoulder,
            left_elbow,
            left_wrist
        )

        # ======================================================
        # RIGHT ARM
        # ======================================================

        right_shoulder = [
            landmarks[
                mp_pose.PoseLandmark.RIGHT_SHOULDER.value
            ].x,

            landmarks[
                mp_pose.PoseLandmark.RIGHT_SHOULDER.value
            ].y
        ]

        right_elbow = [
            landmarks[
                mp_pose.PoseLandmark.RIGHT_ELBOW.value
            ].x,

            landmarks[
                mp_pose.PoseLandmark.RIGHT_ELBOW.value
            ].y
        ]

        right_wrist = [
            landmarks[
                mp_pose.PoseLandmark.RIGHT_WRIST.value
            ].x,

            landmarks[
                mp_pose.PoseLandmark.RIGHT_WRIST.value
            ].y
        ]

        right_angle = calculate_angle(
            right_shoulder,
            right_elbow,
            right_wrist
        )

        # ======================================================
        # LEFT REP LOGIC
        # ======================================================

        if left_angle > 150:
            left_stage = "down"

        if left_angle < 50 and left_stage == "down":
            left_stage = "up"
            left_reps += 1

        # ======================================================
        # RIGHT REP LOGIC
        # ======================================================

        if right_angle > 150:
            right_stage = "down"

        if right_angle < 50 and right_stage == "down":
            right_stage = "up"
            right_reps += 1

        # ======================================================
        # FORM CHECKING
        # ======================================================

        left_feedback = "GOOD"

        if left_angle > 120 and left_stage == "up":
            left_feedback = "GO HIGHER"

        if left_angle < 30:
            left_feedback = "TOO FAST"

        right_feedback = "GOOD"

        if right_angle > 120 and right_stage == "up":
            right_feedback = "GO HIGHER"

        if right_angle < 30:
            right_feedback = "TOO FAST"

        # ======================================================
        # ANGLE DISPLAY
        # ======================================================

        cv2.putText(
            frame,
            str(int(left_angle)),
            tuple(np.multiply(left_elbow, [w, h]).astype(int)),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            2
        )

        cv2.putText(
            frame,
            str(int(right_angle)),
            tuple(np.multiply(right_elbow, [w, h]).astype(int)),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # ======================================================
        # LEFT PANEL
        # ======================================================

        cv2.rectangle(frame, (10, 10), (300, 170), (40, 40, 40), -1)

        cv2.putText(
            frame,
            f"REPS: {left_reps}",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"STAGE: {left_stage}",
            (20, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"FORM: {left_feedback}",
            (20, 130),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        # ======================================================
        # RIGHT PANEL
        # ======================================================

        cv2.rectangle(frame, (330, 10), (620, 170), (40, 40, 40), -1)

        cv2.putText(
            frame,
            f"REPS: {right_reps}",
            (340, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"STAGE: {right_stage}",
            (340, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"FORM: {right_feedback}",
            (340, 130),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

    except:
        pass

    # =========================
    # Draw Skeleton
    # =========================

    if results.pose_landmarks:

        mp_draw.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

    # =========================
    # FPS Display
    # =========================

    cv2.putText(
        frame,
        f"FPS: {fps}",
        (20, 460),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    # =========================
    # Title
    # =========================

    cv2.putText(
        frame,
        "AI FITNESS ASSISTANT",
        (140, 440),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    # =========================
    # Show Window
    # =========================

    cv2.imshow("AI Fitness Assistant", frame)

    # =========================
    # Quit
    # =========================

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()