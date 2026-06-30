

# Session 8: Model Context Protocol (MCP)

### [Quicklinks]()


| Session Sheet                                                             | Recording | Slides | Repo          | Homework | Feedback |
| ------------------------------------------------------------------------- | --------- | ------ | ------------- | -------- | -------- |
| [MCP Servers](../00_Docs/Session_Sheets/17_MCP_Servers_and_A2A/README.md) |           |        | You are here! |          |          |


## Useful Resources

**MCP (Model Context Protocol)**

- [MCP Official Docs](https://modelcontextprotocol.io/) — Spec, tutorials, and guides
- [MCP-UI](https://mcpui.dev/) — Official standard for interactive UI in MCP
- [MCP Auth Guide (Auth0)](https://auth0.com/blog/mcp-specs-update-all-about-auth/) — Deep dive into MCP auth spec updates



## Main Assignment

In this session, you will build an MCP server with OAuth authentication — a cat
shop application that exposes tools for browsing products, managing a cart, and
checking out.

The main entry point is:

```text
server.py
```

The server implementation lives in:

```text
app/
```

Available MCP tools:

- `list_products`
- `get_product`
- `add_to_cart`
- `view_cart`
- `remove_from_cart`
- `checkout`



## Setup

From this folder:

```bash
uv sync
```

Copy the example env file and fill in your OpenAI API key:

```bash
cp .env.example .env
```



## Running the MCP Server

Run the server locally:

```bash
uv run server.py
```

The server starts on `http://localhost:8000`.

### Expose the server with ngrok

In a separate terminal, start an ngrok tunnel:

```bash
ngrok http 8000
```

Copy the ngrok forwarding URL (e.g. `https://xxxx-xx-xx-xx-xx.ngrok-free.app`) and
restart the server with it:

```bash
ISSUER_URL=https://xxxx-xx-xx-xx-xx.ngrok-free.app uv run server.py
```

> **Note:** The `ISSUER_URL` must match the public URL clients use to reach the
> server, otherwise OAuth authentication will fail.



## Outline



### Breakout Room #1

- Set up the MCP server with OAuth and the product database
- Explore the MCP tools: `list_products`, `get_product`, `add_to_cart`, `view_cart`, `remove_from_cart`, `checkout`



### Breakout Room #2

- Connect an MCP client to the server
- Build an end-to-end interaction flow using the MCP tools



## Ship

The completed MCP server and client integration!

### Deliverables

- A short Loom of either:
  - the MCP server you built and a demo of the client interacting with it; or
  - the notebook you created for the Advanced Build



## Share

Make a social media post about your final application!

### Deliverables

- Make a post on any social media platform about what you built!

Here's a template to get you started:

```
🚀 Exciting News! 🚀

I am thrilled to announce that I have just built and shipped an MCP server with OAuth authentication! 🎉🤖

🔍 Three Key Takeaways:
1️⃣
2️⃣
3️⃣

Let's continue pushing the boundaries of what's possible in the world of AI and tool integration. Here's to many more innovations! 🚀
Shout out to @AIMakerspace !

#MCP #ModelContextProtocol #OAuth #Innovation #AI #TechMilestone

Feel free to reach out if you're curious or would like to collaborate on similar projects! 🤝🔥
```



## Submitting Your Homework [OPTIONAL]

Follow these steps to prepare and submit your homework assignment:

1. Review the MCP server code in `server.py` and the `app/` directory
2. Run the MCP server locally using `uv run server.py`
3. Connect to the server using an MCP client (e.g., Claude Desktop, or a custom client)
4. Test all available tools: browsing products, adding to cart, viewing cart, removing items, and checkout
5. Record a Loom video reviewing what you have learned from this session



## Questions



### Question #1

Why is OAuth important for MCP servers, and what security considerations should you keep in mind when exposing tools to AI clients?

#### Answer

OAuth is important for **Model Context Protocol (MCP)** servers because it provides a standardized way for AI clients to authenticate users and obtain permission to access resources or execute actions on their behalf. Instead of giving an AI application long-lived API keys with broad privileges, OAuth issues scoped, revocable access tokens.

- **User identity**
  - OAuth allows the MCP server to know which user is making a request.
  - Different users can have access to different tools or data.
- **Delegated authorization**
  - Users grant permission without sharing their passwords.
  - The AI client receives an access token with specific permissions.
- **Fine-grained permissions**
  - Tokens can be limited to scopes such as:
    - Read documents
    - View calendar
    - Add items to a shopping cart
    - Never perform purchases
- **Token lifecycle**
  - Access tokens expire.
  - Refresh tokens can obtain new access tokens.
  - Tokens can be revoked if compromised.
- **Interoperability**
  - OAuth is widely supported across cloud providers and enterprise identity systems.
  - MCP clients can integrate with many services using a common authentication mechanism.

Question #2

What is Streamable HTTP transport in MCP, and why might you expose a server publicly with OAuth instead of using a local stdio connection?

#### Answer

**Streamable HTTP** is a transport mechanism in the **Model Context Protocol (MCP)** that allows an AI client and an MCP server to communicate over HTTP while supporting long-lived, streaming interactions. Unlike a local `stdio` connection, it enables remote access over a network, making it suitable for web applications, cloud deployments, and multi-user services.

Publishing an MCP server over HTTPS with OAuth enables scenarios that aren't practical with a local `stdio` connection.



#### 1. Support remote AI clients

A local `stdio` server can only be accessed by processes running on the same machine.

An HTTP server can be used by:

- ChatGPT
- enterprise AI assistants
- internal company applications
- web and mobile apps
- multiple users simultaneously



#### 2. Authenticate users

OAuth lets the server identify who is making each request.

#### 3. Delegate permissions safely

Instead of exposing API keys, OAuth issues scoped access tokens.

#### 4. Scale to many users

A cloud-hosted MCP server can:

- serve thousands of concurrent requests,
- run behind a load balancer,
- scale horizontally,
- integrate with monitoring and logging infrastructure.

A local `stdio` process is typically intended for a single local client.

Activity 1: Extend the MCP Server

Add at least one new tool to the cat shop MCP server (e.g., `search_products`, `update_cart_quantity`, or `get_order_history`). Ensure the new tool integrates properly with the existing database and OAuth authentication. Demo the new tool through an MCP client and include it in your Loom video.

## Advanced Activity: Build a Custom MCP Client

Build a custom MCP client that connects to the cat shop server over Streamable HTTP, authenticates via OAuth, and orchestrates a multi-step shopping flow (browse → add to cart → checkout). Compare the developer experience of MCP-based tool integration vs. traditional REST API calls.

Include your findings and a demo in your Loom video.