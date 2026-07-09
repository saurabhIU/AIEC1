## Session 10: LLM Servers


| 📰 Session Sheet                                        | ⏺️ Recording                                                                                                                                           | 🖼️ Slides                                                                                                                                                                         | 👨‍💻 Repo    | 📝 Homework                                                                                                                                 | 📁 Feedback                                         |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| [LLM Servers](../00_Docs/Session_Sheets/16_LLM_Servers) | [Recording!](https://us02web.zoom.us/rec/share/HDunij9p7eCXeP_OgsRDRjTdWUqiEhDBGWrFJEn1bwWR1wz1jKX6EHXSOM45d0sC.rHiyo_znZ-R8Jh6S) passcode: `D80X^YjL` | [Session 10 Slides](https://www.canva.com/design/DAG-EBu7B5A/POcowC5rDLENSPcSVpbf8g/edit?utm_content=DAG-EBu7B5A&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton) | You are here! | [Session 10 Assignment: LLM Servers](https://forms.gle/Riqvwf6KrZcCRKV86) [Demo Day Submission (3/12)](https://forms.gle/7xyuBUn69GX4v6K98) | [Feedback 3/5](https://forms.gle/W28QFWJXpSS4ZAR6A) |


**⚠️!!! PLEASE BE SURE TO SHUTDOWN YOUR DEDICATED ENDPOINT ON FIREWORKS AI WHEN YOU'RE FINISHED YOUR ASSIGNMENT !!!⚠️**

# Build 🏗️

In today's assignment, we'll be creating Fireworks AI endpoints, and then building a RAG application.

- 🤝 Breakout Room #1
  - Set-up Open Source Endpoint (Instructions [here](./ENDPOINT_SETUP.md)) ((This process may take 15-20min.))
  - Test Endpoint and Embeddings with the `endpoint_slammer.ipynb` notebook.
- 🤝 Breakout Room #2
  - Use the Open Source Endpoints to build a RAG LangGraph application



# Ship 🚢

The completed notebook and your RAG app/notebook!

### Deliverables

- A short Loom of either:
  - the notebook and the RAG application you built for the Main Homework Assignment; or
  - the notebook you created for the Advanced Build



# Share 🚀

Make a social media post about your final application!

### Deliverables

- Make a post on any social media platform about what you built!

Here's a template to get you started:

```
🚀 Exciting News! 🚀

I am thrilled to announce that I have just built and shipped a RAG application powered by open-source endpoints! 🎉🤖

🔍 Three Key Takeaways:
1️⃣
2️⃣
3️⃣

Let's continue pushing the boundaries of what's possible in the world of AI and question-answering. Here's to many more innovations! 🚀
Shout out to @AIMakerspace !

#LangChain #QuestionAnswering #RetrievalAugmented #Innovation #AI #TechMilestone

Feel free to reach out if you're curious or would like to collaborate on similar projects! 🤝🔥
```



# Submitting You Homework



## Main Homework Assignment

Follow these steps to prepare and submit your homework assignment:

1. Follow the instructions in `ENDPOINT_SETUP.md`
2. Replace both `model` values in `endpoint_slammer.ipynb` with the `gpt-oss` endpoint you created in Step 1
3. Run the code cells in `endpoint_slammer.ipynb`
4. Respond to the questions in the section below
5. Build a sample RAG
6. Record a Loom video reviewing what you have learned from this session

**⚠️!!! PLEASE BE SURE TO SHUTDOWN YOUR DEDICATED ENDPOINT ON FIREWORKS AI WHEN YOU HAVE FINISHED YOUR ASSIGNMENT !!!⚠️**

## Questions



### ❓ Question #1:

What is the difference between serverless and dedicated endpoints?

#### ✅ Answer:

*With serverless endpoints we don't own GPU's. Whenever a request is sent to serverless endpoint, the requests joins a pool of requests from many other customers. You pay only for input tokens and output tokens.*

*Advantage of serverless:*

1. No infrastructure to manage
2. Very inexpensive for small apps
3. Automatically scales
4. Great for development



### Disadvantages

1. Latency can vary.
2. Throughput isn't guaranteed.
3. Performance depends on shared capacity.

In dedicated endpoints, LLM servers (Fireworks) reserves a dedicated GPU for your application. You pay for GPU time. The GPU reserved can't be used by any other customer traffic.This is similar to EC2 instance on AWS. 

### ❓ Question #2:

Why is it important to consider token throughput and latency when choosing an LLM for user-facing applications?

#### ✅ Answer:

For user-facing applications, **users don't judge the model by benchmark scores—they judge it by how fast it responds and whether it feels responsive**. That's why **latency** and **token throughput** are just as important as model quality.

### 1. Latency determines how quickly users see a response. It is the delay before the model starts responding.

For an LLM, it's often broken into:

- **Time to First Token (TTFT):** How long before the first word appears.
- **Total response time:** How long until the complete answer is generated.

Suppose a user asks:

> "Generate my workout for today."



### Model A

- TTFT: **0.3 seconds**
- Throughput: **100 tokens/sec**



### Model B

- TTFT: **3 seconds**
- Throughput: **100 tokens/sec**

The screen stays blank for 3 seconds.

Even though both models generate at the same speed after they start, **Model A feels much faster**.

### 2.Token throughput determines how quickly the answer finishes

Throughput is the rate at which the model generates tokens.

Suppose your workout plan is about **600 tokens**.

### Model A:

100 tokens/sec

600 tokens -> 6 sec

Model B:

20 tokens/sec

600 tokens -> 30 sec

Thirty seconds is long enough that many users may leave or think the app has stalled.

## Activity 1: RAGAS Evaluation with Cost Analysis

Use RAGAS to evaluate your open-source Fireworks AI powered RAG app against an OpenAI `gpt-4.1-mini` powered equivalent. Compare retrieval quality, answer faithfulness, and end-to-end accuracy across both providers.

Additionally, instrument both pipelines with **LangSmith** to capture token usage and cost per query. Use LangSmith's tracing and cost dashboards to compare the total cost of running each provider at scale. Include your evaluation results, cost breakdown, and analysis in your Loom video.

## Advanced Activity: Local Models

Swap out the Fireworks AI endpoints for **locally-running open-source models** using [Ollama](https://ollama.com/) or another local inference server of your choice. Run both your embedding model and your chat model locally, and rebuild the RAG pipeline on top of them.

- Compare quality and latency between the local setup and your Fireworks AI hosted endpoint.
- Reflect: what are the trade-offs of local models vs. managed endpoints in a production setting?

Include your findings and a demo in your Loom video.