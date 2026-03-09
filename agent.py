import os
from dotenv import load_dotenv
load_dotenv()
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from tools import (
    get_tp_details,
    check_transfer_status,
    get_pending_followups,
    search_knowledge_base,
    draft_escalation_email,
    generate_onboarding_checklist,
    detect_sla_breaches,              
    get_onboarding_status,        
)

TOOLS = [
    get_tp_details,
    check_transfer_status,
    get_pending_followups,
    search_knowledge_base,
    draft_escalation_email,
    generate_onboarding_checklist,
    detect_sla_breaches,          
    get_onboarding_status,        
]

SYSTEM_PROMPT = """You are an MFT Operations Agent for an enterprise B2B integration team.
You help support engineers quickly resolve MFT/EDI issues by looking up trading partner details,
checking transfer statuses, finding relevant procedures, and drafting emails.

You have access to these tools:
- get_tp_details: Look up any trading partner by ID or name
- check_transfer_status: Check latest transfer status for a TP
- get_pending_followups: Get pending/overdue follow-up items
- search_knowledge_base: Find SOPs, policies, and procedures
- draft_escalation_email: Draft a professional escalation email
- generate_onboarding_checklist: Create onboarding checklist for new TPs
- detect_sla_breaches: Check which trading partners have breached or are at risk of breaching SLA
- get_onboarding_status: Track onboarding progress for new trading partners being set up

Guidelines:
- ALWAYS use tools to get accurate information — never guess or make up TP details
- When a transfer is failing, use check_transfer_status AND search_knowledge_base together
- For password resets, always mention JO approval is required
- Keep responses clear and actionable
- Remember context from earlier in the conversation
"""


class MFTAgent:
    def __init__(self):
        print("MFT Agent initializing...")
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=os.environ.get("GROQ_API_KEY"),
            temperature=0
        )
        self.agent = create_react_agent(
            model=llm,
            tools=TOOLS,
            prompt=SYSTEM_PROMPT,
        )
        self.chat_history = []
        print("MFT Agent ready.")

    def chat(self, user_message: str) -> str:
        try:
            result = self.agent.invoke({
                "messages": self.chat_history + [HumanMessage(content=user_message)]},
                config={"recursion_limit": 10}
            )
            answer = result["messages"][-1].content

            self.chat_history.append(HumanMessage(content=user_message))
            self.chat_history.append(AIMessage(content=answer))

            if len(self.chat_history) > 20:
                self.chat_history = self.chat_history[-20:]

            return answer

        except Exception as e:
            error = str(e)
            if "429" in error or "rate_limit" in error.lower():
                return "Daily token limit reached. Please try again in a few hours."
            return f"Sorry, I ran into an error: {error}"

    def reset(self):
        self.chat_history = []
        return "Conversation cleared."