# Reflection

I used Cursor (model: Grok 4.6 Medium) to build a FastAPI Student Task API. The best part was the prompt process. I typed one clear prompt, and Cursor created the files, ran the tests, and reported the results by itself. For the few-shot step, giving three error examples made it use one exact JSON error shape everywhere. For the chain-of-thought step, asking it to think step by step helped it find a real bug: titles containing only spaces were being accepted. Watching it explain its reasoning, edit the code, and run pytest in one go felt faster than writing each piece myself.

The most annoying part was a Git problem. My project folder was inside my user folder, which was already a Git repository. Because of this, Cursor showed more than 800,000 changes, and my personal files appeared as untracked. I had to split my project's history into a new clean repository before pushing it. Long prompts were also cut off in the Cursor chat, which made it harder to copy them for my prompt log.

I have used GitHub Copilot before. In my experience, Copilot is great for quick suggestions while typing inside the editor, while Cursor works more like an agent that handles a whole task, including creating files, running tests, and making commits. Cursor needed more care with Git and folders, because it can change many things at once.

In a real team, I would pick Cursor for bigger tasks such as building a feature with tests, and Copilot for small inline suggestions while coding.