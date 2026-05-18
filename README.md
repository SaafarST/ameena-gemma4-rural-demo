# Ameena Offline — Gemma 4 for Rural Central Asian Schools

> Submission for the **Kaggle Gemma 4 Good Hackathon**
> Tracks: **Digital Equity & Inclusivity** + **Future of Education** + **llama.cpp Special Prize**

## The problem

Rural schools across **Tajikistan, Uzbekistan, Kyrgyzstan, and Kazakhstan** routinely have either no internet or only 2G. The ~40M speakers of these languages are also under-served by cloud-only AI tutors built for English. The result is a double exclusion: by infrastructure and by language.

## What we built

An **offline AI tutor** that runs **Gemma 4** locally via `llama.cpp` on a $100-class device — Raspberry Pi, an Android tablet, or a MacBook Air — and answers curriculum questions in **Tajik, Uzbek, Kyrgyz, and Kazakh**. No internet. No fine-tuning required for v1: we use prompt engineering plus curriculum-aligned examples. The module is designed to slot into the existing Ameena PWA (`ameena.tj`) via its offline sync layer.

## Architecture

| Layer | Component | Source |
|---|---|---|
| Model | `gemma-4-4b-it` quantized to GGUF Q4_K_M (~2.5 GB) | Hugging Face |
| Inference | `llama-cpp-python` — CPU only, `n_gpu_layers=0` | this repo |
| Prompting | Gemma 4 ChatML template + Tajik teacher persona | `inference.py` |
| Host integration | Ameena PWA — `OfflineManager` caches model + content to IndexedDB | `src/services/OfflineManager.ts` |
| Mobile shell | Capacitor (`app.lovable.ameena`) wraps the PWA for Android | `capacitor.config.ts` |
| PWA / service worker | `vite-plugin-pwa` + Workbox precache | `vite.config.ts` |

The Ameena codebase already has an offline-first reader at `src/pages/BookReader.tsx:962-1127` that falls back to `OfflineManager.getCachedBooks()` whenever `navigator.onLine` is false. The Gemma 4 module plugs into the same boundary: when the device is offline, tutor requests are routed to the local Llama runtime instead of the cloud API.

## Quick start

```bash
# 1. Download a GGUF build of Gemma 4 (user-provided).
#    Recommended: gemma-4-4b-it-Q4_K_M.gguf (~2.5 GB)
#    Place it next to inference.py, or:
export GEMMA4_MODEL_PATH=/path/to/gemma-4-4b-it-Q4_K_M.gguf

# 2. Install runtime
pip install -r requirements.txt

# 3. Run the default Tajik math demo
python inference.py

# 4. Run a curriculum prompt from the bundled set
python inference.py sample_prompts/tajik_science.txt

# 5. Or ask a custom question
python inference.py "Феълҳои номукаммалро шарҳ диҳед."
```

## Sample prompts (`sample_prompts/`)

| File | Subject | Grade | Example |
|---|---|---|---|
| `tajik_math.txt` | Mathematics | 5 | Adding fractions |
| `tajik_science.txt` | Natural science | 6 | What is water made of |
| `tajik_language.txt` | Tajik language | 4 | Imperfect verbs with examples |

All three are written in Tajik (Cyrillic), using the teacher-persona prompting pattern Ameena uses in production.

## Why Gemma 4 specifically

1. **Open weights (Apache 2.0)** — Central Asian digital-sovereignty requirements rule out closed cloud models for state-school deployment. Gemma 4 can be self-hosted, audited, and shipped inside a sealed device image.
2. **Edge-runtime first** — Gemma 4 ships well-supported quantizations and runs in llama.cpp, LiteRT, and Ollama. A Q4_K_M build fits in 2.5 GB RAM, which is the realistic budget on a rural-school tablet.
3. **Strong multilingual base** — Tajik, Uzbek, Kyrgyz, and Kazakh are mid-resource Cyrillic languages. Gemma 4's base coverage is good enough that prompt engineering reaches usable tutoring quality without fine-tuning, which is essential for a v1 that has to ship inside 4 hours.
4. **Function calling** — Native tool use opens the path to offline quiz generation, exam scoring, and curriculum-tagged retrieval in v2.

## Impact

- **Live pilots.** One private school and one institute in Dushanbe are paying customers today.
- **Pipeline.** 33+ rural schools targeted for Q1 2026 rollout.
- **Languages.** Tajik, Uzbek, Kyrgyz, Kazakh — ~40M speakers, mid-resource Cyrillic.
- **Offline-first.** The Ameena PWA already runs 30-day offline windows; Gemma 4 extends that to AI tutoring on the same hardware.
- **SDG alignment.** UN SDG 4 (Quality Education) and SDG 10 (Reduced Inequalities).

## Team

- **Tohir Saidzoda** — CTO, Saidzoda Engineering LLC (Dushanbe). Background in Tajik-language LLM continual pretraining (Qwen3 8B and 14B on ~1B-token Tajik corpora).
- **Madina Abdusalomzoda** — CEO, Saidzoda Engineering LLC. Education strategy and partnerships.
- **Saidzoda Engineering** — NVIDIA for Startups member; Google Cloud credits recipient.

## Links

- **Live platform:** https://ameena.tj
- **Company:** https://saidzoda.com
- **Video demo:** *(see Kaggle submission for unlisted YouTube URL)*

## License

- **Code in this repo:** CC-BY-4.0
- **Gemma 4 weights:** Apache 2.0 (user downloads separately; not redistributed here)
- **Tajik educational corpus** used for prompt design: proprietary to Saidzoda Engineering; not included.
