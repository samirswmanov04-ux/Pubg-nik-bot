import os
import random

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================
# PUBG NICK GENERATOR
# =========================

STYLES = [
    {
        "a": "abcdefghijklmnopqrstuvwxyz",
        "b": "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫",
    },
    {
        "a": "abcdefghijklmnopqrstuvwxyz",
        "b": "𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟",
    },
    {
        "a": "abcdefghijklmnopqrstuvwxyz",
        "b": "𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏",
    },
    {
        "a": "abcdefghijklmnopqrstuvwxyz",
        "b": "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ",
    },
]

DECORATIONS = [
    ("꧁", "꧂"),
    ("『", "』"),
    ("乂", "乂"),
    ("亗", "亗"),
    ("♛", "♛"),
    ("★", "★"),
    ("✦", "✦"),
    ("〆", "〆"),
    ("ツ", "ツ"),
    ("彡", "彡"),
    ("⚡", "⚡"),
]

FORMATS = [
    "{left}{name}{right}",
    "{left} {name} {right}",
    "亗 {name} 亗",
    "★彡{name}彡★",
    "『{name}』ツ",
    "乂 {name} 乂",
    "♛{name}♛",
    "〆{name}〆",
    "⚡{name}⚡",
    "么{name}么",
]


def stylish_name(name):
    style = random.choice(STYLES)

    result = ""

    for char in name:
        lower = char.lower()

        if lower in style["a"]:
            index = style["a"].index(lower)
            new_char = style["b"][index]

            if char.isupper():
                new_char = new_char.upper()

            result += new_char
        else:
            result += char

    return result


def generate_nicks(name, count=10):
    result = set()

    attempts = 0

    while len(result) < count and attempts < 100:
        attempts += 1

        styled = stylish_name(name)

        left, right = random.choice(DECORATIONS)
        template = random.choice(FORMATS)

        nick = template.format(
            left=left,
            name=styled,
            right=right
        )

        result.add(nick)

    return list(result)


# =========================
# COMMANDS
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 PUBG NICK GENERATOR\n\n"
        "Menga ismingizni yuboring.\n"
        "Men sizga 10 ta chiroyli PUBG nik yaratib beraman.\n\n"
        "Masalan:\n"
        "Samir\n"
        "Shadow\n"
        "Alex\n\n"
        "Har safar boshqa shrift va boshqa bezaklar tanlanadi 🔥"
    )


async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    name = update.message.text.strip()

    if len(name) > 30:
        await update.message.reply_text(
            "❌ Ism 30 ta belgidan uzun bo‘lmasin."
        )
        return

    nicks = generate_nicks(name)

    text = "🔥 SIZ UCHUN PUBG NIKLAR:\n\n"

    for i, nick in enumerate(nicks, 1):
        text += f"{i}. {nick}\n"

    text += "\n🎮 Yana boshqa ism yuboring!"

    await update.message.reply_text(text)


# =========================
# ERROR HANDLER
# =========================

async def error_handler(update, context):
    print("Xatolik:", context.error)


# =========================
# MAIN
# =========================

def main():
    TOKEN = os.getenv("BOT_TOKEN")

    if not TOKEN:
        print("❌ BOT_TOKEN topilmadi!")
        print("Render Environment Variables bo‘limiga BOT_TOKEN qo‘shing.")
        return

    app = (
        Application.builder()
        .token(TOKEN)
        .connect_timeout(30)
        .read_timeout(30)
        .write_timeout(30)
        .pool_timeout(30)
        .build()
    )

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            generate
        )
    )

    app.add_error_handler(error_handler)

    print("✅ PUBG Nick Bot ishga tushdi!")

    app.run_polling()


if __name__ == "__main__":
    main()