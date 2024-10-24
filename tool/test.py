from prompt_toolkit import prompt

text = prompt('Give me some input: ', default='aa', multiline=True)
print('You said: %s' % text)
