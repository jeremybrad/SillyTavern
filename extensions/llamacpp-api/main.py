from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route('/v1/models', methods=['GET'])
def list_models():
    return jsonify({
        "object": "list",
        "data": [{"id": "local-llama", "object": "model"}]
    })

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    try:
        data = request.get_json(force=True)
        print("Raw request JSON:", data)

        messages = data.get("messages", [])
        print("Parsed messages:", messages)

        prompt_parts = []
        for msg in messages:
            role = msg.get("role")
            content = msg.get("content")
            print(f"Message role: {role}, content: {content}")
            if role in ("system", "user"):
                prompt_parts.append(content)

        prompt = "\n".join(prompt_parts)
        print("Constructed prompt:", repr(prompt))

        response_text = f"Echo: {prompt}" if prompt else "Error: Empty prompt."

        return jsonify({
            "id": "chatcmpl-local",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": "local-llama",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response_text
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": len(prompt),
                "completion_tokens": 9,
                "total_tokens": len(prompt) + 9
            }
        })

    except Exception as e:
        print("Exception in chat_completions:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=8080, debug=True)
