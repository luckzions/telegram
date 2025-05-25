from telethon import TelegramClient, events
import re
import os

# Substitua com suas informações
api_id = 26329643
api_hash = '287e9c29fb6c1063bf59e8c17d66e96c'
session_name = 'minha_conta'

client = TelegramClient(session_name, api_id, api_hash)

contador_async = 1  # Contador para salvar arquivos .txt únicos

@client.on(events.NewMessage)
async def handler(event):
    global contador_async

    texto = event.raw_text

    # 🎁 GIFT CARD
    if '🎁 GIFT CARD GERADO 🎁' in texto:
        match = re.search(r'Codigo: (\w+)', texto)
        if match:
            codigo = match.group(1)
            resposta = f"/resgatar {codigo}"
            await client.send_message(event.chat_id, resposta)
            print(f"[✓] Código detectado e enviado: {resposta}")

    # 📁 Baixar arquivos específicos
    if event.file:
        nome = event.file.name or "arquivo"
        extensoes_permitidas = ('.rar', '.zip', '.js', '.py')
        if nome.lower().endswith(extensoes_permitidas):
            caminho = os.path.join(os.getcwd(), nome)
            await event.download_media(file=caminho)
            print(f"[↓] Arquivo salvo: {nome}")

    # 📝 Salvar mensagens que contenham "async function"
    if "async function" in texto:
        while True:
            nome_arquivo = f"async_function_{contador_async}.txt"
            caminho_arquivo = os.path.join(os.getcwd(), nome_arquivo)
            if not os.path.exists(caminho_arquivo):
                with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                    f.write(texto)
                print(f"[📝] Texto com 'async function' salvo como: {nome_arquivo}")
                contador_async += 1
                break
            else:
                contador_async += 1

# /ping simples
@client.on(events.NewMessage(pattern='/ping'))
async def ping(event):
    await event.reply('pong')

print("Conectando...")
client.start()
print("Bot conectado krl, scrappando tudo KAKAKA")
client.run_until_disconnected()
