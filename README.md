# 🧠 Agentic AI Reasoning Analyzer

This project demonstrates a bilingual agentic AI application using **vLLM**, **Streamlit**, and **web search** to generate informative blog-style responses in real-time from internet sources or fallback LLM knowledge.

## ⚙️ System Architecture

- **Backend**: [vLLM](https://github.com/vllm-project/vllm) running `Qwen/Qwen3-4B` with reasoning mode enabled.
- **Frontend**: Streamlit app for input and real-time streaming output.

---

## 🖥️ Step-by-Step Installation

### ✅ 1. **Backend VM** — vLLM Server with Qwen3-4B

> **Requirement**: NVIDIA GPU (A10G, A100, etc) with at least 16GB VRAM, Ubuntu 20.04 or higher.

#### 1.1 Create a virtual environment

```bash
python3 -m venv venv_backend
source venv_backend/bin/activate
```

#### 1.2 Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements_backend_vllm.txt
```

#### 1.3 Download the model (Qwen3-4B)

Make sure you've accepted the license for Qwen/Qwen3-4B on Hugging Face, then run:

```bash
huggingface-cli login
# Accept model license at https://huggingface.co/Qwen/Qwen3-4B
```

#### 1.4 Start the vLLM server

```bash
vllm serve Qwen/Qwen3-4B \
  --host 0.0.0.0 \
  --port 8000 \
  --gpu-memory-utilization 0.80 \
  --enable-reasoning \
  --reasoning-parser deepseek_r1
```

- Ensure port `8000` is open in your VM firewall.
- `--enable-reasoning` allows usage of the reasoning-specific prompt structure.

---

### ✅ 2. **Frontend VM** — Streamlit App

> **Requirement**: Python 3.10+, internet access, and can reach backend VM via internal IP or public IP.

#### 2.1 Create a virtual environment

```bash
python3 -m venv venv_frontend
source venv_frontend/bin/activate
```

#### 2.2 Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements_front.txt
```

#### 2.3 Configure Backend IP

Open `frontend.py` (or your main Streamlit file), and change this line:

```python
openai_api_base = "http://<YOUR_BACKEND_VM_IP>:8000/v1"
```

Replace `<YOUR_BACKEND_VM_IP>` with the actual IP address of the VM running vLLM.

#### 2.4 Run the Streamlit app

```bash
streamlit run frontend.py
```

- The app will launch in your browser on `http://localhost:8501`.
- You can access it from another device if you run with `--server.address 0.0.0.0`.

---

## 🧪 Test

Try queries like:

- `"apa itu machine learning"`  
- `"what is reinforcement learning wikipedia"`  
- `"perkembangan teknologi AI tahun 2024 arxiv"`

The app will:
1. Try fetching real-time information from web.
2. If no sources are found, fallback to LLM response via vLLM.

---

## 🛡️ Notes

- This project respects open-source licenses.
- You may host this on-prem or in cloud VMs (GCP, AWS, Azure).
- Recommended GPU: A100 40GB for maximum concurrency, or T4 for small use cases.