# Ameena Offline — Gemma 4 for Rural Central Asian Schools

**Tracks:** Digital Equity & Inclusivity · Future of Education · llama.cpp Special Prize
**Team:** Saidzoda Engineering LLC (Dushanbe, Tajikistan)

## The problem

Rural schools across **Tajikistan, Uzbekistan, Kyrgyzstan, and Kazakhstan** sit on the wrong side of two simultaneous gaps. The first is infrastructural: large stretches of these countries have either no internet or only 2G. The second is linguistic: ~40 million speakers of Tajik, Uzbek, Kyrgyz, and Kazakh are routinely under-served by cloud-only AI tutors built for English-speaking markets. A student in a village three hours outside Dushanbe cannot reach ChatGPT, and even if she could, the answer would come back in the wrong language at the wrong cultural register.

That is the digital divide we set out to close.

## What we built

**Ameena Offline** is a working offline AI tutor that runs **Gemma 4** locally via `llama.cpp` on a $100-class device — a Raspberry Pi, a low-end Android tablet, or a teacher's MacBook Air — and answers curriculum questions in **Tajik, Uzbek, Kyrgyz, and Kazakh**.

No internet is required at inference time. No fine-tuning is required for v1: we use prompt engineering with a teacher-persona system message and curriculum-aligned exemplars. The module is designed to slot into the existing Ameena PWA platform (`ameena.tj`), which already has an offline-first content pipeline.

Our submission is deliberately scoped to what one engineer can ship and a teacher can actually use:

1. `inference.py` — a single-file Python entry point that loads a quantized Gemma 4 GGUF and answers a Tajik prompt in roughly the time it takes to read it back.
2. Three curriculum prompts in `sample_prompts/` — math, natural science, and Tajik language — covering grades 4–6.
3. Integration design notes describing how this loop plugs into Ameena's existing offline reader.

## Technical architecture

- **Model:** `gemma-4-4b-it`, quantized to GGUF **Q4_K_M** (~2.5 GB on disk).
- **Runtime:** `llama-cpp-python` with `n_gpu_layers=0` for maximum hardware compatibility. The default 4-thread CPU config runs comfortably on $100-class ARM and x86 devices.
- **Prompt template:** Gemma 4's native ChatML form (`<bos><start_of_turn>user … <end_of_turn><start_of_turn>model`), with `temperature=0.3` and `top_p=0.9` for tutoring-grade determinism.
- **Language adaptation:** entirely prompt-based for v1 — a Tajik teacher persona plus a grade-level constraint. We have a fine-tuning path waiting in v2 (see below), but the hackathon submission ships without it because the prompting result is already useful.
- **Offline-first integration:** the Ameena PWA already routes book-content requests through an `OfflineManager` (`src/services/OfflineManager.ts`) that caches metadata to IndexedDB via `idb-keyval` and falls back to that cache whenever `navigator.onLine === false`. The book reader at `src/pages/BookReader.tsx:962-1127` calls `OfflineManager.getCachedBooks()` directly in the offline path. Wiring Gemma 4 in is a one-line change: in the same offline branch, the cloud tutor call gets replaced by a local `llama.cpp` call.
- **Mobile shell:** Capacitor wraps the PWA for Android (`app.lovable.ameena` in `capacitor.config.ts`). The GGUF weights are pre-downloaded once during onboarding and live alongside the app's IndexedDB content.

## Why Gemma 4 specifically

We considered every credible open-weight model. Gemma 4 won on four axes that matter for this market:

1. **Open weights under Apache 2.0.** Central Asian education ministries have explicit digital-sovereignty constraints: the model has to be auditable, self-hostable, and shippable inside a sealed device image. Closed cloud models are not viable for state-school deployment.
2. **Edge-runtime first.** Gemma 4 ships well-supported quantizations and is a first-class citizen in `llama.cpp`, LiteRT, and Ollama. A Q4_K_M build fits in ~2.5 GB, which is the realistic memory budget on a rural-school tablet — and on a $35 Raspberry Pi 4 that schools can deploy in a community center.
3. **Strong multilingual base.** Tajik, Uzbek, Kyrgyz, and Kazakh are mid-resource Cyrillic-script languages. Gemma 4's base coverage is good enough that prompt engineering alone reaches usable tutoring quality at grade 4–6 level — which made it possible to ship a real v1 inside the hackathon window.
4. **Native function calling.** Tool use opens the path to v2: offline quiz generation, exam scoring against a local rubric, and curriculum-tagged retrieval over Ameena's existing book corpus.

## Implementation notes from `inference.py`

The submission code is intentionally small and well-commented. Highlights:

- The model path defaults to `./gemma-4-4b-it-Q4_K_M.gguf` but can be overridden with the `GEMMA4_MODEL_PATH` env var so the same script runs in a CI box, a teacher's laptop, and a Raspberry Pi without edits.
- A user can pass a literal prompt OR a path to one of the bundled prompt files: `python inference.py sample_prompts/tajik_science.txt`. The CLI helps demonstrate the cross-subject coverage on stage.
- The chat template is hard-coded to Gemma 4's tokens (`<start_of_turn>`, `<end_of_turn>`) so the model produces clean turn boundaries that the host app can parse for streaming UI.
- Temperature `0.3` is deliberate: tutoring needs reproducibility and "the same kid gets the same explanation," not creative variance.

## Impact and validation

This is not a hypothetical project. Ameena is an operating platform with paying contracts:

- **Live pilots.** One private school and one educational institute in Dushanbe, Tajikistan, are paying customers today.
- **Pipeline.** 33+ rural schools targeted for Q1 2026 rollout.
- **Languages addressed.** Tajik, Uzbek, Kyrgyz, Kazakh — ~40M speakers across four post-Soviet republics.
- **Device floor.** $100 Android tablets, Raspberry Pi 4 with 4 GB RAM, MacBook Air. The Q4_K_M GGUF fits all three.
- **Connectivity floor.** 2G or no internet. The Ameena PWA already runs 30-day offline content windows; Gemma 4 extends that to AI tutoring on the same hardware.
- **Alignment.** UN SDG 4 (Quality Education) and SDG 10 (Reduced Inequalities).

## What is and is not in this submission

**In:** a runnable `inference.py`, three Tajik curriculum prompts, a README that any judge can follow, and a 3-minute video that shows the same script answering a Tajik math question offline. The integration design is documented in this writeup and in the repo README; the wiring points in the live Ameena codebase (`OfflineManager.ts`, `BookReader.tsx`) are real and cited by file and line.

**Out of scope for this 4-hour submission, planned for v2:**

1. LoRA fine-tuning on Saidzoda Engineering's existing ~370M-token Tajik corpus (CPT pipeline already exists for Qwen3 8B; porting to Gemma 4 is the natural next step).
2. Capacitor APK build that ships GGUF weights bundled with the Ameena app — currently the weights are downloaded once during onboarding.
3. Integration with Ameena's exam engine for fully offline certification.

## Team

- **Tohir Saidzoda** — CTO, Saidzoda Engineering LLC. Background in continual pretraining of Tajik-language LLMs (Qwen3 8B/14B over ~370M-token Tajik corpora) and the Ameena platform engineering.
- **Madina Abdusalomzoda** — CEO and co-founder. Education strategy, school partnerships, government relations.
- **Saidzoda Engineering** — Dushanbe-based, NVIDIA for Startups member, Google Cloud credits recipient. Eight engineers building Central Asia's first sovereign AI infrastructure for education.

## Links

- **Code repository:** https://github.com/[USERNAME]/ameena-gemma4-rural-demo
- **Video demo (3 min, unlisted YouTube):** [URL added at submission]
- **Live platform:** https://ameena.tj
- **Company:** https://saidzoda.com

## License

- **Code in this repo:** Creative Commons Attribution 4.0 (CC-BY-4.0).
- **Gemma 4 weights:** Apache 2.0 (downloaded by the user, not redistributed here).
- **Tajik educational corpus** used for prompt design: proprietary to Saidzoda Engineering; not included in this submission.
