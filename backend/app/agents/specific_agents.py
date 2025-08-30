"""
Concrete implementations of the AI agents for the Multi-Agent AI Chat System.
"""
from app.agents.base import BaseAgent
from app.agents.interfaces import (
    Message,
    Response,
    ConversationContext,
    Proposal,
    Vote,
    AgentState,
)

class ProjectManagerAgent(BaseAgent):
    async def process_message(self, message: Message) -> Response:
        # Simple echo for now
        return Response(content=f"{self.name} received: {message.content}")

    async def generate_response(self, context: ConversationContext) -> str:
        prompt = self.system_prompt + "\n\n" + "\n".join([f"{m.sender}: {m.content}" for m in context.conversation_history])
        response = await self.llm_service.generate_response(prompt)
        return response

    async def vote_on_proposal(self, proposal: Proposal) -> Vote:
        # Placeholder logic
        return Vote(proposal_id=proposal.id, agent_id=self.agent_id, approve=True)

    def validate_response(self, response: str) -> bool:
        return len(response) > 0

    def get_agent_state(self) -> AgentState:
        return AgentState(agent_id=self.agent_id, is_active=True)

class TechnicalArchitectAgent(BaseAgent):
    async def process_message(self, message: Message) -> Response:
        return Response(content=f"{self.name} received: {message.content}")

    async def generate_response(self, context: ConversationContext) -> str:
        prompt = self.system_prompt + "\n\n" + "\n".join([f"{m.sender}: {m.content}" for m in context.conversation_history])
        response = await self.llm_service.generate_response(prompt)
        return response

    async def vote_on_proposal(self, proposal: Proposal) -> Vote:
        return Vote(proposal_id=proposal.id, agent_id=self.agent_id, approve=True)

    def validate_response(self, response: str) -> bool:
        return len(response) > 0

    def get_agent_state(self) -> AgentState:
        return AgentState(agent_id=self.agent_id, is_active=True)

class CreativeStrategistAgent(BaseAgent):
    async def process_message(self, message: Message) -> Response:
        return Response(content=f"{self.name} received: {message.content}")

    async def generate_response(self, context: ConversationContext) -> str:
        prompt = self.system_prompt + "\n\n" + "\n".join([f"{m.sender}: {m.content}" for m in context.conversation_history])
        response = await self.llm_service.generate_response(prompt)
        return response

    async def vote_on_proposal(self, proposal: Proposal) -> Vote:
        return Vote(proposal_id=proposal.id, agent_id=self.agent_id, approve=True)

    def validate_response(self, response: str) -> bool:
        return len(response) > 0

    def get_agent_state(self) -> AgentState:
        return AgentState(agent_id=self.agent_id, is_active=True)

class QualityAssuranceAgent(BaseAgent):
    async def process_message(self, message: Message) -> Response:
        return Response(content=f"{self.name} received: {message.content}")

    async def generate_response(self, context: ConversationContext) -> str:
        prompt = self.system_prompt + "\n\n" + "\n".join([f"{m.sender}: {m.content}" for m in context.conversation_history])
        response = await self.llm_service.generate_response(prompt)
        return response

    async def vote_on_proposal(self, proposal: Proposal) -> Vote:
        return Vote(proposal_id=proposal.id, agent_id=self.agent_id, approve=True)

    def validate_response(self, response: str) -> bool:
        return len(response) > 0

    def get_agent_state(self) -> AgentState:
        return AgentState(agent_id=self.agent_id, is_active=True)

class ResourceCoordinatorAgent(BaseAgent):
    async def process_message(self, message: Message) -> Response:
        return Response(content=f"{self.name} received: {message.content}")

    async def generate_response(self, context: ConversationContext) -> str:
        prompt = self.system_prompt + "\n\n" + "\n".join([f"{m.sender}: {m.content}" for m in context.conversation_history])
        response = await self.llm_service.generate_response(prompt)
        return response

    async def vote_on_proposal(self, proposal: Proposal) -> Vote:
        return Vote(proposal_id=proposal.id, agent_id=self.agent_id, approve=True)

    def validate_response(self, response: str) -> bool:
        return len(response) > 0

    def get_agent_state(self) -> AgentState:
        return AgentState(agent_id=self.agent_id, is_active=True)
