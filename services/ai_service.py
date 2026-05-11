import streamlit as st

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


class AIChatAssistant:
    def __init__(self):
        self.api_key = None
        self.client = None

        if "OPENAI_API_KEY" in st.secrets:
            self.api_key = st.secrets["OPENAI_API_KEY"]

        if self.api_key and OpenAI is not None:
            self.client = OpenAI(api_key=self.api_key)

    def is_available(self):
        return self.client is not None

    def _fallback_response(self, role_name: str):
        return (
            f"The OpenAI assistant is not connected yet for the {role_name} role. "
            "Add OPENAI_API_KEY to Streamlit secrets to enable real AI responses."
        )

    def get_host_response(self, prompt, sessions, needs, claims):
        if not self.is_available():
            return self._fallback_response("Host")

        context = f'''
You are helping a Host in a campus collaboration app.
Sessions: {sessions}
Needs: {needs}
Claims: {claims}
User question: {prompt}
Give a concise helpful answer focused on missing items, event descriptions, summaries, and next actions.
'''
        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a helpful event planning assistant inside a college collaboration app."},
                {"role": "user", "content": context},
            ],
            temperature=0.4,
        )
        return response.choices[0].message.content

    def get_contributor_response(self, prompt, sessions, needs, claims):
        if not self.is_available():
            return self._fallback_response("Contributor")

        context = f'''
You are helping a Contributor in a campus collaboration app.
Open Sessions: {sessions}
Needs: {needs}
My Claims: {claims}
User question: {prompt}
Give a concise helpful answer focused on what still needs items, what the user claimed, and which event to join.
'''
        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a helpful campus collaboration assistant inside a college app."},
                {"role": "user", "content": context},
            ],
            temperature=0.4,
        )
        return response.choices[0].message.content
