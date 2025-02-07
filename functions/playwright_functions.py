from functions.browser import init_browser
from functions.utils import get_game_details, get_copias_disponiveis

def get_page_title(url):
  playwright, browser, page = init_browser() # Inicializa o navegador
  
  try:
    page.goto(url)
    print(page.title())
    print(page.evaluate("({width: window.innerWidth, height: window.innerHeight})"))  # Verificar viewport
  finally:
    browser.close()
    playwright.stop() # Encerra o Playwright

def get_popular_games(url):
  playwright, browser, page = init_browser()
  
  try:
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
  except Exception as e:
    print(f"Erro ao carregar a página: {e}")
    return

  # Captura todos os jogos dentro da seção "Populares da Semana"
  jogos = page.locator("div.flex.snap-start").all()

  # Verifica se há jogos disponíveis, senão encerra a execução
  if len(jogos) == 0:
    return

  for jogo in jogos:
    try:
      titulo = jogo.locator("div.text-center").inner_text()
    except Exception as e:
      print(f"Erro ao capturar nome do jogo: {e}")
      continue

    # Captura o preço corretamente
    try:
      preco_int = jogo.locator("div.flex.items-center.justify-between span span").inner_text()
    except:
      preco_int = "N/A"
    
    try:
      preco_centavos = jogo.locator("div.flex.items-center.justify-between span small").nth(1).inner_text()
    except:
      preco_centavos = ""

    preco = f"R${preco_int.strip()}{preco_centavos.strip()}"

    # Captura os detalhes
    try:
      detalhes = get_game_details(jogo)
    except:
      detalhes = ["N/A"] * 4  # Jogadores, duração, complexidade, nota média

    num_jogadores, duracao, complexidade, nota_media = detalhes

    try:
      copias_disponiveis = get_copias_disponiveis(jogo)
    except:
      copias_disponiveis = "N/A"

    print(f"Jogo: {titulo} | Jogadores: {num_jogadores} | Duração: {duracao} | Complexidade: {complexidade} | Nota média: {nota_media} | Preço: {preco} | Cópias disponíveis: {copias_disponiveis}")
    print()
  
  browser.close()
  playwright.stop()  # Encerra o Playwright
