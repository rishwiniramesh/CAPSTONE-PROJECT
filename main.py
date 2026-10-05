import streamlit as st

from services.pdf_processor import extract_text_from_pdf
from services.ai_service import MultimodalAI


st.set_page_config(
    page_title="AI Software Project Management System",
    page_icon="🤖",
    layout="wide",
)


st.title("🤖 AI-Based Software Project Management System")

st.write(
    "Upload your existing software project. "
    "The system will analyze its documents, source code, "
    "images, and diagrams to identify possible problems "
    "and suggest improvements."
)

st.divider()

st.header("📂 Upload Your Existing Project")

uploaded_files = st.file_uploader(
    "Upload your project files",
    type=[
        "html",
        "css",
        "js",
        "pdf",
        "txt",
        "md",
        "png",
        "jpg",
        "jpeg",
    ],
    accept_multiple_files=True,
)


if not uploaded_files:

    st.info(
        "Upload files such as coal.html, CSS, JavaScript, "
        "SRS, documentation, or project images."
    )

    st.stop()


text_documents = []
images = []


for uploaded_file in uploaded_files:

    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):

        try:
            text = extract_text_from_pdf(uploaded_file)

            if text.strip():
                text_documents.append(
                    {
                        "filename": uploaded_file.name,
                        "text": text,
                    }
                )
            else:
                st.warning(
                    f"No readable text found in "
                    f"{uploaded_file.name}"
                )

        except Exception as error:

            st.error(
                f"Could not read {uploaded_file.name}: "
                f"{error}"
            )


    elif filename.endswith(
        (".html", ".css", ".js", ".txt", ".md")
    ):

        try:

            text = uploaded_file.read().decode(
                "utf-8",
                errors="ignore",
            )

            if text.strip():

                text_documents.append(
                    {
                        "filename": uploaded_file.name,
                        "text": text,
                    }
                )

        except Exception as error:

            st.error(
                f"Could not read {uploaded_file.name}: "
                f"{error}"
            )


    elif filename.endswith(
        (".png", ".jpg", ".jpeg")
    ):

        image_bytes = uploaded_file.read()

        images.append(
            (
                uploaded_file.name,
                image_bytes,
            )
        )


st.header("📊 Uploaded Project")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Files",
        len(uploaded_files),
    )

with col2:
    st.metric(
        "Documents / Code",
        len(text_documents),
    )

with col3:
    st.metric(
        "Images / Diagrams",
        len(images),
    )


if text_documents:

    st.subheader("📄 Project Files")

    for document in text_documents:

        with st.expander(
            document["filename"]
        ):

            st.code(
                document["text"][:10000],
                language="text",
            )


combined_text = ""

for document in text_documents:

    combined_text += (
        f"\n\n===== FILE: "
        f"{document['filename']} =====\n\n"
    )

    combined_text += document["text"]


if images:

    st.subheader("🖼️ Project Images / Diagrams")

    for filename, image_bytes in images:

        with st.expander(filename):

            st.image(
                image_bytes,
                width="stretch",
            )


st.divider()

st.header("🤖 AI Project Review")

st.write(
    "The AI will review the uploaded project and identify "
    "potential failures, weaknesses, missing functionality, "
    "risks, and improvement tasks."
)


if st.button(
    "🚀 Analyze My Project",
    type="primary",
):

    try:

        with st.spinner(
            "AI is analyzing your project..."
        ):

            ai = MultimodalAI()

            result = ai.analyze_project(
                project_text=combined_text,
                images=images,
            )

            st.session_state["analysis"] = result

    except Exception as error:

        st.error(
            f"AI analysis failed: {error}"
        )


if "analysis" in st.session_state:

    st.divider()

    st.header("📋 AI Analysis")

    st.markdown(
        st.session_state["analysis"]
    )