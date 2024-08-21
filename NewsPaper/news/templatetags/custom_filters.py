from django import template

register = template.Library()

cenzor_symbol = '*'


@register.filter()
def censor(value):
    bad_words = ["new", "usually"]  # для примера отображения в разных новостях/статьях и в их заголовках

    if not isinstance(value, str):
        raise TypeError(f"Filter is used only for 'str' type!")

    for word in value.split():
        if word.lower() in bad_words:
            value = value.replace(word, f"{word[0]}{cenzor_symbol * (len(word) - 1)}")
    return value



