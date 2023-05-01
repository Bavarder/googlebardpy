# Google Bard

## Installation

### Pypi

```sh
pip install googlebardpy
```

### Codeberg

```sh
pip install --index-url https://codeberg.org/api/packages/Bavarder/pypi/simple/ googlebardpy
```

## Usage

### Get the token

1. Go to [bard.google.com](https://bard.google.com)
2. Open developer tools
3. Go to Application
4. Go to Cookies
5. Copy the content of `__Secure-1PSID`

### Use the chatbot

```python
secure_1psid = "..."
chat = BardChat(secure_1psid)
chat.ask("Hello, who are you ?")
```
