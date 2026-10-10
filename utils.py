def input_int(prompt: str) -> int:
    """Безопасный ввод целого числа."""
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите корректное целое число.")