# Gemini 2.5 Flash Image — Free Image Generation

**Model:** `gemini-2.5-flash-image` (NOT `gemini-2.5-flash` which is text-only)
**Cost:** $0 (free tier: 60 requests/minute)
**Quality:** Good for cinematic/dark academia style. Slightly less detailed than Imagen 4.

## API Usage

```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_KEY")  # or from env/`.hermes/.env`

response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents="Your visual prompt here — detailed, in English or Vietnamese",
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE', 'TEXT'],
    ),
)

for part in response.candidates[0].content.parts:
    if part.inline_data and part.inline_data.mime_type.startswith('image/'):
        with open('output.png', 'wb') as f:
            f.write(part.inline_data.data)
        print(f"Image: {len(part.inline_data.data)//1024} KB")
```

## Key Differences vs FAL/Imagen 4

| Aspect | Gemini 2.5 Flash Image | FAL/Imagen 4 |
|--------|----------------------|--------------|
| Cost | **$0** | ~$0.04/image |
| Resolution | ~1344x768 | Up to 1920x1080 |
| Speed | ~3-5s/image | ~2-4s/image |
| Vietnamese prompt | Works | Better |
| Style control | Good | Excellent |

## Prompt Tips for Best Quality

- Write in **English** for better results (Gemini handles English image prompts better)
- Include the style tag explicitly: `cinematic, 1344x768, dark academia style, high quality`
- Include brand color: `#1a6b3c green accent`
- Avoid asking for text overlays in the image — Gemini often provides a text description instead
- For scene 29 (CTA/social): Gemini may refuse image gen and return "What would you like the image to convey?" — prompt without text, just the visual

## Safety Settings

Default safety settings may block some image concepts. Use minimal blocking:

```python
types.SafetySetting(category='HARM_CATEGORY_HATE_SPEECH', threshold='BLOCK_ONLY_HIGH'),
```

Skip `HARM_CATEGORY_DANGEROUS_CONTENT` and `HARM_CATEGORY_SEXUALLY_EXPLICIT` thresholds to reduce false positives.

## Troubleshooting

### "This model only supports text output"
You're using `gemini-2.5-flash` (text model). Switch to `gemini-2.5-flash-image`.

### "No image in response"
Gemini sometimes returns text only (description or refusal). Retry with a reworded prompt. For stubborn cases (social media scenes), drop all text-related words from the prompt.

### Rate limiting
Free tier: ~60 requests/minute. Space requests 1 second apart for safety.

## Requirements

```bash
pip install google-genai
```

API key from `GOOGLE_API_KEY` env var or `~/.hermes/.env`.
