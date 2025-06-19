
├── app/
│   ├── api/                      # FastAPI роутери та схеми
│   ├── core/                     # Налаштування, конфігурації
│   ├── models/                   # Pydantic моделі
│   ├── services/                 # Логіка взаємодії з Solana та Telegram
│   ├── utils/                    # Утиліти та допоміжні функції
│   └── main.py                   # Точка входу FastAPI
├── bot/
│   ├── handlers/                 # Обробники команд Telegram
│   ├── state/                    # Стан FSM для користувачів
│   ├── services/                 # Логіка Telegram бота
│   └── bot.py                    # Ініціалізація та запуск бота
├── db/
│   ├── models.py                 # Опис моделей бази даних
│   ├── crud.py                   # Операції з базою даних
│   └── session.py                # Налаштування сесій бази даних
├── config.py                     # Конфігурації проєкту
├── requirements.txt              # Залежності
└── README.md                     # Документація
