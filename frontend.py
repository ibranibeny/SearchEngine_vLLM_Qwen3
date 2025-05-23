import streamlit as st
import asyncio
from openai import OpenAI
import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from duckduckgo_search import DDGS
import warnings
import random

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

openai_api_key = "EMPTY"
openai_api_base = "http://<YOUR_BACKEND_VM_IP>:8000/v1"

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15A372 Safari/604.1"
]

# Web Search Agent
async def web_search_agent(query):
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=8):
                body = r.get('body', '')
                link = r.get('href', '')
                if body and link:
                    results.append(f"{body}\nSumber: {link}")
        return '\n\n'.join(results)
    except Exception as e:
        print(f"DuckDuckGo search failed: {e}")
        return ""

# Reasoning Agent
async def reasoning_agent(sources, model_id, output_box):
    client = OpenAI(api_key=openai_api_key, base_url=openai_api_base)
    context = "\n\n".join(f"[{k}]\n{v}" for k, v in sources.items()) if sources else "(Tidak ditemukan sumber relevan, silakan gunakan pengetahuan sendiri untuk menjawab.)"
    messages = [
        {"role": "system", "content": "You are a journalist assistant whong analyze then generates new journalist article from multiple web sources, bilingual in Indonesian and English, and clearly shows the source URL. If no sources are provided, answer based on your own knowledge."},
        {"role": "user", "content": f"Anda adalah seorang jurnalist yang akan melakukan analisa lalu membuatkan artikel dalam bentuk news article yang mudah dimengerti, dalam dua bahasa (Bahasa Indonesia dan Bahasa Inggris), berdasarkan informasi berikut dan sebutkan URL sumber jika ada:\n{context}"}
    ]

    stream = client.chat.completions.create(model=model_id, messages=messages, stream=True)
    result_text = ""
    for chunk in stream:
        content = getattr(chunk.choices[0].delta, "content", None)
        if content:
            result_text += content
            output_box.markdown(result_text)

# Orchestrator
async def agentic_ai_pipeline_stream(query, output_box):
    try:
        web_content = await web_search_agent(query)
    except:
        web_content = ""
    sources = {"Web Sources": web_content} if web_content.strip() else {}
    client = OpenAI(api_key=openai_api_key, base_url=openai_api_base)
    model = client.models.list().data[0].id
    await reasoning_agent(sources, model, output_box)

# Streamlit UI
st.set_page_config(page_title="Agentic AI", layout="wide")
st.title("Agentic AI Search Engine")
query = st.text_input("Put your Question:", key="input")

if query:
    st.subheader("Output:")
    output_box = st.empty()
    asyncio.run(agentic_ai_pipeline_stream(query, output_box))

