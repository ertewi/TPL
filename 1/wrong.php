<?php
// лаба по неправильному алфавиту

declare(strict_types=1);

$input = str_split('2 + 2');

F($input, 0);


function S(array $str, int $index) {
    $index = T($str, $index);
    $index = E($str, $index);

    return $index;
}

function E(array $str, int $index) {
    if (
        $str[$index] === '+'
        || $str[$index] === '-'
    ) {
        if ($str[++$index] !== ' ')
            throw new Exception('Вывод: Ошибка! Ожидалось: space');

        $index = T($str, ++$index);
        $index = E($str, $index);

        return $index;
    }

    return $index;
}

function T(array $str, int $index) {
    if (
        $str[$index] === '*'
        || $str[$index] === '/'
    ) {
        if ($str[++$index] !== ' ')
            throw new Exception('Вывод: Ошибка! Ожидалось: space');

        $index = F($str, ++$index);
        $index = T($str, $index);

        return $index;
    }

    $potentialIndex = $index;
    try {
        $potentialIndex = F($str, $potentialIndex);
        $potentialIndex = T($str, $potentialIndex);

        return $potentialIndex;
    } catch (Exception) {
    }

    return $index;
}

function F(array $str, int $index) {
    if ($str[$index] === '(') {
        $index = S($str, ++$index);

        if ($str[++$index] !== ')')
            throw new Exception('Вывод: Ошибка! Ожидалось: \')\'');
    }

    if (is_numeric($str[$index])) {
        while (is_numeric($str[++$index]));
        if ($str[$index] === ' ') ++$index;

        return $index;
    }

    if (ctype_alpha($str[$index])) {
        while (ctype_alpha($str[++$index]));
        if ($str[$index] === ' ') ++$index;

        return $index;
    }

    throw new Exception('Вывод: Ошибка! Ожидалось: number, id или \'(\'');
}