from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Dict, List
from langchain_core.documents import Document
import logging

logger = logging.getLogger(__name__)

class VerificationAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0
        )
        self.prompt = ChatPromptTemplate.from_template(
            """Verify the following answer against the provided context. Check for:
            1. Direct factual support (YES/NO)
            2. Unsupported claims (list)
            3. Contradictions (list)
            4. Relevance to the question (YES/NO)
            
            Respond in this format:
            Supported: YES/NO
            Unsupported Claims: [items]
            Contradictions: [items]
            Relevant: YES/NO
            
            Answer: {answer}
            Context: {context}
            """
        )
        
    def check(self, answer: str, documents: List[Document]) -> Dict:
        """Verify the answer against the provided documents."""
        context = "\n\n".join([doc.page_content for doc in documents])
        
        chain = self.prompt | self.llm | StrOutputParser()
        try:
            verification = chain.invoke({
                "answer": answer,
                "context": context
            })
            logger.info(f"Verification report: {verification}")
            logger.info(f"Context used: {context}")
        except Exception as e:
            logger.error(f"Error verifying answer: {e}")
            raise
        
        return {
            "verification_report": verification,
            "context_used": context
        }