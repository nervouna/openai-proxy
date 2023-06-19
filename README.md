# openai-proxy
Proxy for OpenAI api using python flask, supports SSE streaming.

## Install dependencies

With [rye][1]:

```bash
rye sync
```

With pip:

```bash
pip install -r requirements.txt
```

## Testing

- Update the variables in example.env, rename it to `.env`.
- Use `python3 main.py` to start a local server.
- Test the proxy with any http client.

```bash
curl -N http://127.0.0.1:9000/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{"stream": true, "model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "What is the OpenAI mission?"}]}'
```

[1]: https://rye-up.com/