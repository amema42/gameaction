# 🎯 GameAction

**GameAction** is a lightweight number guessing game powered entirely by GitHub Actions and Discussions — no backend, no frontend, just GitHub.

## 💡 How it works

- When a **new discussion** is created, a **random number between 1 and 100** is automatically generated and saved to `game_data.json`.
- Participants **comment guesses** in the discussion.
- A GitHub Action:
  - Checks the guessed number
  - Responds with ✅ correct / ❌ incorrect
  - Tracks the number of attempts
  - Announces the win once the correct number is guessed

## ⚙️ Tech stack

- **GitHub Actions** – automation engine
- **GitHub Discussions** – game UI
- **Python** – game logic
- **JSON** – lightweight storage (in-repo)

## 📁 Repo structure

```
.github/
├── workflows/
│   └── on-discussion-create.yml      # Triggers secret number generation
scripts/
└── save_secret_number.py             # Stores number + metadata
game_data.json                        # Stores state per discussion
```

## 🧪 Play the game

1. Open the [Discussions tab](https://github.com/amema42/gameaction/discussions).
2. Start a new discussion to begin a game.
3. Comment your guess (e.g., `37`).
4. The bot will reply and track your attempts.

---

**Built entirely with GitHub.** No server, no UI — just automation for fun. 🧠🎮
