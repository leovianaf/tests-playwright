from functions import get_page_title, get_popular_games
   
def main():
  URL = "https://www.comparajogos.com.br/"
  # get_page_title(URL)
  # get_popular_games(URL)

  URL_LOAD = "https://www.comparajogos.com.br/price-drops"
  get_popular_games(URL_LOAD)

main()