import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters


# Har xil shriftlar
FONT_STYLES = [
    {
        "a": "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫",
        "A": "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ"
    },
    {
        "a": "𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏",
        "A": "𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵"
    },
    {
        "a": "𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟",
        "A": "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅"
    },
    {
        "a": "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ",
        "A": "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"
    }
]


# Bezaklar
DECORATIONS = [
    ("꧁", "꧂"),
    ("『", "』"),
    ("乂", "乂"),
    ("么", "么"),
    ("彡", "彡"),
    ("★", "★"),
    ("✦", "✦"),
    ("亗", "亗"),
    ("♛", "♛"),
    ("ツ", "ツ"),
    ("〆", "〆"),
    ("⚡", "⚡"),
]


def stylize(text, style):
    result = ""

    for char in text:
        if char.isalpha():
            lower = char.lower()

            if lower in style["a"]:
                index = style["a"].index(lower)

                if char.isupper():
                    result += style["A"][index]
                else:
                    result += style["a"][index]
            else:
                result += char
        else:
            result += char

    return result


def generate_nicks(name):
    nicks = []

    # Aralash va tasodifiy variantlar
    for _ in range(12):
        style = random.choice(FONT_STYLES)
        left, right = random.choice(DECORATIONS)

        styled_name = stylize(name, style)

        # Har xil formatlar
        formats = [
            f"{left}{styled_name}{right}",
            f"{left} {styled_name} {right}",
            f"{left}〆{styled_name}{right}",
            f"亗 {styled_name} 亗",
            f"★彡{styled_name}彡★",
            f"『{styled_name}』ツ",
            f"乂 {styled_name} 乂",
            f"♛{styled_name}♛",
            f"〆{styled_name}〆",
            f"⚡{styled_name}⚡",
        ]

        nick = random.choice(formats)

        if nick not in nicks:
            nicks.append(nick)

    return nicks[:10]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Mening ismim Samir Samanov"
        "🎮 PUBG Nick Generator\n\n"
        "Ismingizni yuboring va men sizga chiroyli PUBG niklar yaratib beraman!\n\n"
        "Masalan:\n"
        "Samir\n"
        "Ali\n"
        "Shadow"
    )


async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()

    if not name:
        return

    if len(name) > 30:
        await update.message.reply_text(
            "❌ Ism juda uzun. 30 ta belgidan oshmasin."
        )
        return

    nicks = generate_nicks(name)

    message = "🔥 Siz uchun PUBG niklar:\n\n"

    for i, nick in enumerate(nicks, 1):
        message += f"{i}. `{nick}`\n"

    message += "\n🎮 Yangi ism yuboring — yana boshqa niklar yarataman!"

    await update.message.reply_text(
        message,
        parse_mode="Markdown"
    )


def main():
    # BOT TOKENINGIZNI SHU YERGA YOZING
    TOKEN = "8883360079:AAE5Hhm3rm0c4JZYSb2_SbKrvqnt_TIgW2Q"

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
        MessageHandler(filters.TEXT & ~filters.COMMAND, generate)
    )

    print("Bot ishga tushdi!")
    app.run_polling()


if __name__ == "__main__":
    main()