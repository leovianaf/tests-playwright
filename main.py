from playwright.sync_api import sync_playwright
import re

def get_page_title(url):
  with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url)

    print(page.title())
    print(page.evaluate("({width: window.innerWidth, height: window.innerHeight})"))  # Verificar viewport

    browser.close()

def get_popular_games(url):
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    try:
      page.goto(url, wait_until="domcontentloaded", timeout=60000)
    except Exception as e:
      print(f"Erro ao carregar a página: {e}")
      return

    # Captura todos os jogos dentro da seção "Populares da Semana"
    jogos = page.locator("div.flex.snap-start").all()

    for jogo in jogos:
      try:
        # Captura o nome do jogo corretamente
        titulo = jogo.locator("div.text-center").inner_text()
      except Exception as e:
        print(f"Erro ao capturar nome do jogo: {e}")
        continue

      # Captura a parte inteira do preço
      try:
        preco_int = jogo.locator("div.flex.items-center.justify-between span span").inner_text()
      except:
        preco_int = "N/A"

      # Captura os centavos usando .nth(1) para pegar o segundo <small>
      try:
        preco_centavos = jogo.locator("div.flex.items-center.justify-between span small").nth(1).inner_text()
      except:
        preco_centavos = ""

      # Mantém o formato correto do preço sem adicionar vírgula extra
      preco = f"R${preco_int.strip()}{preco_centavos.strip()}"

      try:
        # Captura todos os detalhes dentro de .group.flex
        detalhes_brutos = jogo.locator("div.group.flex").all_text_contents()
        
        # Lista de rótulos a serem removidos
        rotulos_para_remover = ["jogadores", "minutos", "complexidade", "nota média"]
        
        # Usa regex para remover rótulos e manter os valores corretamente
        padrao = re.compile(rf'\b({"|".join(rotulos_para_remover)})\s*', re.IGNORECASE)
        detalhes = [padrao.sub("", d.strip()) for d in detalhes_brutos if d.strip()]

      except Exception as e:
        print(f"Erro ao capturar detalhes do jogo {titulo}: {e}")
        detalhes = []

      # Ajusta a ordem correta das informações (Jogadores, Duração, Complexidade, Nota Média)
      num_jogadores = detalhes[0] if len(detalhes) > 0 else "N/A"

      # Verifica se há um span.hidden para duração e pega o último valor, senão mantém a extração padrão
      try:
        span_duracao = jogo.locator("div.group.flex span.hidden").last.inner_text()
        duracao = span_duracao.strip() if span_duracao else (detalhes[1] if len(detalhes) > 1 else "N/A")
      except:
        duracao = detalhes[1] if len(detalhes) > 1 else "N/A"

      complexidade = detalhes[2] if len(detalhes) > 2 else "N/A"
      nota_media = detalhes[3] if len(detalhes) > 3 else "N/A"

      # Captura a quantidade de cópias disponíveis e separa apenas o que vem depois do "•"
      try:
        copias_disponiveis_raw = jogo.locator("div.flex.items-center.justify-between div.text-xs.tracking-tight").last.inner_text()
        copias_disponiveis = copias_disponiveis_raw.split("•")[-1].strip() if "•" in copias_disponiveis_raw else copias_disponiveis_raw
      except:
        copias_disponiveis = "N/A"

      # Exibe os dados coletados
      print(f"Jogo: {titulo} | Jogadores: {num_jogadores} | Duração: {duracao} | Complexidade: {complexidade} | Nota média: {nota_media} | Preço: {preco} | Cópias disponíveis: {copias_disponiveis}")
      print()

    browser.close()

        
def main():
  URL = "https://www.comparajogos.com.br/"
  # get_page_title(URL)
  get_popular_games(URL)

main()