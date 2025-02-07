import re

def get_duracao(jogo, detalhes):
  """Verifica se há um `span.hidden` para duração e retorna o último valor disponível."""
  try:
    # Verifica se há pelo menos um span.hidden antes de tentar acessar
    if jogo.locator("div.group.flex span.hidden").count() > 0:
      span_duracao = jogo.locator("div.group.flex span.hidden").last.inner_text()
      return span_duracao.strip() if span_duracao else "N/A"
    
    # Se não houver span.hidden, retorna o segundo detalhe (duração)
    elif len(detalhes) > 1:
      return detalhes[1].strip()
    
    else:
      return "N/A"

  except Exception as e:
    print(f"Erro ao capturar duração: {e}")
    return "N/A"


def get_game_details(jogo):
  """Extrai jogadores, duração, complexidade e nota média."""
  try:
    detalhes_brutos = jogo.locator("div.group.flex").all_text_contents()
    rotulos_para_remover = ["jogadores", "minutos", "complexidade", "nota média"]

    # Remove os rótulos mesmo quando colados aos valores
    padrao = re.compile(rf'\b({"|".join(rotulos_para_remover)})\s*', re.IGNORECASE)
    detalhes = [padrao.sub("", d.strip()) for d in detalhes_brutos if d.strip()]
  except:
    detalhes = []

  num_jogadores = detalhes[0] if len(detalhes) > 0 else "N/A"

  # Usa uma função para verificar duração corretamente
  duracao = get_duracao(jogo, detalhes)

  complexidade = detalhes[2] if len(detalhes) > 2 else "N/A"
  nota_media = detalhes[3] if len(detalhes) > 3 else "N/A"

  return num_jogadores, duracao, complexidade, nota_media

def get_copias_disponiveis(jogo):
  """Captura a quantidade de cópias disponíveis, separando apenas o que vem depois do '•'."""
  try:
    copias_disponiveis_raw = jogo.locator("div.flex.items-center.justify-between div.text-xs.tracking-tight").last.inner_text()
    return copias_disponiveis_raw.split("•")[-1].strip() if "•" in copias_disponiveis_raw else copias_disponiveis_raw
  except:
    return "N/A"
