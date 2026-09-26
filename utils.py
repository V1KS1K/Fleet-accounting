def input_int(prompt: str) -> int:
    """Безопасный ввод целого числа с обработкой ошибок."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: пожалуйста, введите целое число.")