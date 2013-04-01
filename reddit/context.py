def nav(request):
  """
  nav should be a list of dictionaries like { 'name':str, 'url':str }
  "/" should be added after the for loop since s.startswith("/"[1:]) is always true
  """
  nav = [
    ]
  for n in nav:
    if request.path.startswith(n['url'][1:]):
      n['current'] = True
  return { 'nav': nav }
