# uTON Observatory

## О проекте / токене

UTONIC TON, the Liquid Re-staking Token of UTONIC.

Самоописание из метаданных токена; заявления проекта не проверены независимо.

Источники (проверены 2026-11-23):

- <https://tonapi.io/v2/jettons/EQAfF5j3JMIpZlLmACv7Ub7RH7WmiVMuV4ivcgNYHvNnqHTz>

Generated from https://github.com/Freebielife/TON-Observatory-Template.

Run python3 -m scripts.refresh_observatory; python3 build.py; python3 verify.py.
Publish index.html in TON Sites only after independent on-chain verification.
Данные операций, сжиганий и пулов собраны из API блокчейна; полнота и ошибки источников хранятся в снимке.
Only native TON swap pairs supported. Locks, staking and custom project NFT badges are configured through project.json and verified against TonAPI.
В GitHub Actions задан резервный график `13,43 * * * *` (каждые 30 минут). Исполнение зависит от GitHub; подключение к общему Cloudflare runner не подтверждено.

Foundation version: 1.3.0. Holders show 10, expandable to top 20.
`project.json` is the per-project specification. Contract/pool/precision changes require regenerating from the factory; do not reuse another token's snapshot.
Run `python3 build.py` for an atomic bundle and `build/report.json` size report.
No external fonts, scripts or images are needed to render the saved page. Fresh data checks and manual wallet lookups require network access.
Cloudflare dispatch registration and GitHub repository access remain separate deployment steps. No credentials go into HTML.

## Особенность данных uTON

Проверка 2026-11-23: `get_jetton_data` возвращает выпуск 30 472,672432754 uTON
(30 472 672 432 754 / 10^9), а `get_wallet_data` крупнейшего кошелька —
478 870 573,420187369 uTON (478 870 573 420 187 369 / 10^9).
Адрес кошелька подтверждён `get_wallet_address`; Toncenter показывает тот же баланс.
Причина расхождения не установлена. См. точные URL и результаты в
[data/supply-verification.json](data/supply-verification.json).

Пока баланс превышает выпуск, рейтинг и оценка капитализации не публикуются.
На странице отображается причина. Проверка повторяется при каждом обновлении;
при согласованных данных разделы восстановятся автоматически.
Поэтому раскрытие холдеров 10→20 пока нельзя проверить на реальных данных uTON.
Поддерживаются только две подтверждённые прямые пары TON (STON.fi и DeDust).
Операции TONCO и пары с иными токенами не входят в ленту.

Изображение пользователя встроено в баннер и флаги карточек. Официальные ссылки:
[сайт](https://utonic.org), [канал](https://t.me/utonic_uton),
[X](https://twitter.com/UTONIC_uTON), [документация](https://docs.utonic.org).
Публикация в TON Storage/Resistance Tools выполняется отдельно.
