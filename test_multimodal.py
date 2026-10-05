from services.ai_service import MultimodalAI


ai = MultimodalAI()

result = ai.analyze_project(
    """
    Project Name: Hospital Management System

    The system allows patients to register.
    Doctors can manage patient records.
    Administrators can manage users.

    The project should support secure authentication.
    """
)

print(result)