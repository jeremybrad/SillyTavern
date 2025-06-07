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
    response_text = "Error: Unable to process request."  # Default response
    
    try:
        data = request.get_json(force=True)
        print("Raw request JSON:", data)

        messages = data.get("messages", [])
        print("Parsed messages:", messages)

        # Build conversation context including assistant messages
        prompt_parts = []
        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")
            print(f"Message role: {role}, content: {content}")
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")

        prompt = "\n".join(prompt_parts)
        print("Constructed prompt:", repr(prompt))

        # Generate response (replace this with actual LLM call)
        if prompt:
            response_text = f"I understand your message: {prompt.split('User:')[-1].strip() if 'User:' in prompt else prompt}"
        else:
            response_text = "Hello! How can I help you today?"        # Calculate actual token counts
        prompt_tokens = len(prompt.split()) if prompt else 0
        completion_tokens = len(response_text.split())
        
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
            }],            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens
            }
        })

    except Exception as e:
        print("Exception in chat_completions:", str(e))
        print("Returning assistant message:", response_text)
        return jsonify({
            "error": str(e),
            "message": "Internal server error"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
