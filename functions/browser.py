from playwright.sync_api import sync_playwright

def init_browser():
  """Inicializa o navegador Playwright e retorna um contexto ativo."""
  playwright = sync_playwright().start()
  browser = playwright.chromium.launch(headless=False)
  page = browser.new_page()
  return playwright, browser, page
