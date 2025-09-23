<?php

declare(strict_types=1);

while (true) {
    echo "\n";
    $input = trim(fgets(STDIN));
    try {
        validate($input);

        echo 'Вывод: Выражение корректно.';
        echo "\n";
    } catch (Exception $e) {
        echo $e->getMessage();
    }
}
function validate(string $str): void {
    $str = trim($str);
    if (empty($str)) {
        return;
    }

    $symbol = $str[0];

    if ($symbol === '(') {
        preg_match('/^\((.*)\)(.*?)$/', $str, $matches);
        if (empty($matches)) {
            throw new Exception('Вывод: Ошибка! Ожидалось: \')\'');
        }

        if (empty(trim($matches[1]))) {
            throw new Exception('Вывод: Ошибка! Ожидалось: number, id или \'(\'');
        }
        validate(trim($matches[1]));

        if (!empty(trim($matches[2]))) {
            validateOperation(trim($matches[2]));
        }

        return;
    }

    if (is_numeric($symbol) || ctype_alpha($symbol)) {
        preg_match('/^[a-zA-Z0-9]+(.*)/', $str, $matches);
        if (empty(trim($matches[1]))) {
            return;
        }

        validateOperation(trim($matches[1]));
        return;
    }

    throw new Exception('Вывод: Ошибка! Ожидалось: number, id или \'(\'');
}

function validateOperation(string $str): void {
    $operand = $str[0];

    if (!in_array($operand, ['+', '-', '*', '/']) ) {
        throw new Exception('Вывод: Ошибка! Ожидалось: +, -, *, /');
    }

    preg_match('/^ *(.*)$/', substr($str, 1), $matches);
    if (empty(trim($matches[0]))) {
        throw new Exception('Вывод: Ошибка! Ожидалось: id, number');
    }

    validate($matches[1]);
}