import gradio as gr
import hashlib
import os
from typing import List, Dict
from document_processor.file_handler import DocumentProcessor
from retriever.builder import RetrieverBuilder
from agents.workflow import AgentWorkflow
from config import constants, settings
from utils.logging import logger

EXAMPLES = {
    "Wikipedia Machine Learning Summary": {
        "question": "Provide one-sentence definition of machine learning.",
        "file_paths": ["examples/Wikipedia Machine Learning Summary.md"]
    },
    "Wikipedia Machine Learning Article": {
        "question": "Summarize the main applications of machine learning mentioned in the article.",
        "file_paths": ["examples/Wikipedia Machine Learning Article.pdf"]
    },
    "DeepSeek-R1 Technical Report": {
        "question": "Summarize DeepSeek-R1 model's performance evaluation on all coding tasks against OpenAI o1-mini model",
        "file_paths": ["examples/DeepSeek Technical Report.pdf"]
    },
    "Google 2024 Environmental Report": {
        "question": "Retrieve the data center PUE efficiency values in Singapore 2nd facility in 2019 and 2022. Also retrieve regional average CFE in Asia pacific in 2023",
        "file_paths": ["examples/google-2024-environmental-report.pdf"]  
    }    
}

def main():
    processor = DocumentProcessor()
    retriever_builder = RetrieverBuilder()
    workflow = AgentWorkflow()

    with gr.Blocks(title="DocChat🐥") as demo:
        gr.Markdown("## DocChat: powered by Docling and LangGraph", elem_classes="title")
        gr.Markdown("""
                    1. Upload your document(s) or select one of the examples from the drop-down menu and hit **Load Example** button.
                    2. Enter your question.
                    3. Hit **Submit** button and wait for results.
                    
                    ⚠️ **NOTE:** DocChat only accepts documents in these formats: **.pdf**, **.docx**, **.md**
                    """, elem_classes="text")

        # Maintain the session state for retrieving doc changes
        session_state = gr.State({
            "file_hashes": frozenset(),
            "retriever": None
        })

        # Layout
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Input document(s) and question(s)")
                example_dropdown = gr.Dropdown(
                    label="Select example",
                    choices=list(EXAMPLES.keys()),
                    value=None, # initially unselected
                )
                load_example_btn = gr.Button("Load example📝")

                files = gr.Files(label="Upload Documents", file_types=constants.ALLOWED_TYPES)
                question = gr.Textbox(label="❓ Question", lines=3)

                submit_btn = gr.Button("Submit 🚀")
                
            with gr.Column():
                gr.Markdown("### Results")
                answer_output = gr.TextArea(label="✨ Answer", interactive=False)
                verification_output = gr.TextArea(label="✅ Verification Report")

        def load_example(example_key: str):
            """
            Given a key like 'Example 1', 
            read the relevant docs from disk and return
            them as file-like objects, plus the example question.
            """
            if not example_key or example_key not in EXAMPLES:
                return [], ""

            ex_data = EXAMPLES[example_key]
            question = ex_data["question"]
            file_paths = ex_data["file_paths"]

            # Prepare the file list to return
            loaded_files = []
            for path in file_paths:
                if os.path.exists(path):
                    loaded_files.append(path)
                else:
                    logger.warning(f"File not found: {path}")

            # The function returns lists matching the outputs we define below
            return loaded_files, question

        load_example_btn.click(
            fn=load_example,
            inputs=[example_dropdown],
            outputs=[files, question]
        )

        # Standard flow for question submission
        def process_question(question_text: str, uploaded_files: List, state: Dict):
            """Handle questions with document caching."""
            try:
                if not question_text.strip():
                    raise ValueError("❌ Question cannot be empty")
                if not uploaded_files:
                    raise ValueError("❌ No documents uploaded")

                current_hashes = _get_file_hashes(uploaded_files)
                
                if state["retriever"] is None or current_hashes != state["file_hashes"]:
                    logger.info("Processing new/changed documents...")
                    chunks = processor.process(uploaded_files)
                    retriever = retriever_builder.build_hybrid_retriever(chunks)
                    
                    state.update({
                        "file_hashes": current_hashes,
                        "retriever": retriever
                    })
                
                result = workflow.full_pipeline(
                    question=question_text,
                    retriever=state["retriever"]
                )
                
                return result["draft_answer"], result["verification_report"], state
                    
            except Exception as e:
                logger.error(f"Processing error: {str(e)}")
                return f"❌ Error: {str(e)}", "", state

        submit_btn.click(
            fn=process_question,
            inputs=[question, files, session_state],
            outputs=[answer_output, verification_output, session_state]
        )

    demo.launch(server_name="0.0.0.0", server_port=7860, theme=gr.themes.Ocean())

def _get_file_hashes(uploaded_files: List) -> frozenset:
    """Generate SHA-256 hashes for uploaded files."""
    hashes = set()
    for file in uploaded_files:
        with open(file.name, "rb") as f:
            hashes.add(hashlib.sha256(f.read()).hexdigest())
    return frozenset(hashes)

if __name__ == "__main__":
    os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
    main()
