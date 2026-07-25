from collections import Counter


# ==========================================================
# Calculate Final Interview Report
# ==========================================================

def generate_final_report(
    answer_evaluations: list,
    camera_data: dict = None
):
    """
    Generate a complete interview report.
    """

    if camera_data is None:
        camera_data = {
            "total_frames": 0,
            "detected_frames": 0,
            "face_lost": 0
        }

    if not answer_evaluations:

        return {
            "overall_score": 0,
            "average_technical_score": 0,
            "average_communication_score": 0,
            "recommendation": "No Interview Data",
            "overall_feedback": "No interview data available.",
            "strengths": [],
            "improvements": [],
            "camera_report": {},
            "answers": []
        }

    technical_scores = []
    communication_scores = []

    strengths = []
    improvements = []

    # ======================================================
    # Collect evaluation data
    # ======================================================

    for item in answer_evaluations:

        evaluation = item.get("evaluation", {})

        technical_scores.append(
            evaluation.get("technical_score", 0)
        )

        communication_scores.append(
            evaluation.get("communication_score", 0)
        )

        strengths.extend(
            evaluation.get("strengths", [])
        )

        improvements.extend(
            evaluation.get("improvements", [])
        )

    # ======================================================
    # Average Scores
    # ======================================================

    average_technical_score = round(
        sum(technical_scores) / len(technical_scores),
        2
    )

    average_communication_score = round(
        sum(communication_scores) / len(communication_scores),
        2
    )

    # ======================================================
    # Overall Score
    # ======================================================

    overall_score = round(
        (
            average_technical_score * 0.7 +
            average_communication_score * 0.3
        ) * 10,
        2
    )

    # ======================================================
    # Recommendation
    # ======================================================

    if overall_score >= 85:
        recommendation = "Strongly Recommended"

    elif overall_score >= 75:
        recommendation = "Recommended"

    elif overall_score >= 60:
        recommendation = "Needs Improvement"

    else:
        recommendation = "Not Ready"

    # ======================================================
    # Remove duplicate strengths
    # ======================================================

    unique_strengths = []

    seen = set()

    for item in strengths:

        key = item.strip().lower()

        if key not in seen:
            seen.add(key)
            unique_strengths.append(item)

    # ======================================================
    # Remove duplicate improvements
    # ======================================================

    unique_improvements = []

    seen = set()

    for item in improvements:

        key = item.strip().lower()

        if key not in seen:
            seen.add(key)
            unique_improvements.append(item)

    top_strengths = [
        text
        for text, _
        in Counter(unique_strengths).most_common(5)
    ]

    top_improvements = [
        text
        for text, _
        in Counter(unique_improvements).most_common(5)
    ]

    # ======================================================
    # Camera Analytics
    # ======================================================

    total_frames = camera_data.get("total_frames", 0)
    detected_frames = camera_data.get("detected_frames", 0)
    face_lost = camera_data.get("face_lost", 0)

    visibility = 0

    if total_frames > 0:
        visibility = round(
            (detected_frames / total_frames) * 100,
            2
        )

    if visibility >= 90:
        presence = "Excellent"
        camera_feedback = (
            "Excellent camera presence. "
            "Your face remained visible throughout the interview."
        )

    elif visibility >= 75:
        presence = "Good"
        camera_feedback = (
            "Good camera presence with only minor face losses."
        )

    elif visibility >= 60:
        presence = "Fair"
        camera_feedback = (
            "Your face was occasionally lost. "
            "Try staying centered in front of the camera."
        )

    else:
        presence = "Poor"
        camera_feedback = (
            "Your face was frequently not visible. "
            "Improve your camera positioning."
        )

    eye_contact_score = visibility

    # ======================================================
    # Overall Feedback
    # ======================================================

    overall_feedback = (
        f"Overall interview score: {overall_score}%. "
        f"Technical average: {average_technical_score}/10. "
        f"Communication average: {average_communication_score}/10. "
        f"Recommendation: {recommendation}."
    )

    # ======================================================
    # Return Report
    # ======================================================

    return {

        "overall_score": overall_score,

        "average_technical_score": average_technical_score,

        "average_communication_score": average_communication_score,

        "recommendation": recommendation,

        "overall_feedback": overall_feedback,

        "strengths": top_strengths,

        "improvements": top_improvements,

        "camera_report": {

            "visibility": visibility,

            "presence": presence,

            "eye_contact_score": eye_contact_score,

            "face_lost": face_lost,

            "feedback": camera_feedback

        },

        "answers": answer_evaluations

    }