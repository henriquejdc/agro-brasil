# Car Insurance Premium Simulator

Backend em **FastAPI** para simulação de prêmio de seguro de automóvel, organizado com princípios de **DDD**, **S.O.L.I.D.** e **Clean Architecture**.

## Regras de cálculo

- Taxa por idade: `anos_do_carro * RATE_INCREMENT_PER_YEAR`
- Taxa por valor: `floor(valor_do_carro / VALUE_STEP_AMOUNT) * RATE_INCREMENT_PER_VALUE_STEP`
- Taxa final (`applied_rate`): soma das taxas acima + ajuste GIS opcional
- Prêmio:
  - `base_premium = valor_do_carro * applied_rate`
  - `calculated_premium = base_premium - (base_premium * deductible_percentage) + broker_fee`
- Limite de apólice:
  - `base_policy_limit = valor_do_carro * COVERAGE_PERCENTAGE`
  - `deductible_value = base_policy_limit * deductible_percentage`
  - `policy_limit = base_policy_limit - deductible_value`

## Estrutura (camadas)

- `app/domain`: entidades, value objects, serviço de domínio e evento.
- `app/application`: caso de uso e DTOs internos.
- `app/interfaces`: contrato HTTP e composição FastAPI.
- `app/infrastructure`: carregamento de configuração.

## Configuração

Tudo é parametrizado por variáveis de ambiente (ou arquivo JSON indicado por `APP_CONFIG_FILE`):

- `RATE_INCREMENT_PER_YEAR` (default: `0.005`)
- `RATE_INCREMENT_PER_VALUE_STEP` (default: `0.005`)
- `VALUE_STEP_AMOUNT` (default: `10000`)
- `COVERAGE_PERCENTAGE` (default: `1.0`)
- `CURRENT_YEAR` (default: ano atual)
- `GIS_ENABLED` (default: `false`)
- `GIS_HIGH_RISK_ADJUSTMENT` (default: `0.02`)
- `GIS_LOW_RISK_ADJUSTMENT` (default: `-0.02`)
- `GIS_HIGH_RISK_STATES` (CSV, ex: `RJ,SP`)
- `GIS_LOW_RISK_STATES` (CSV, ex: `SC,PR`)

## Executar localmente

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Endpoint

`POST /quotes/simulate`

Exemplo de payload:

```json
{
  "car": {
    "make": "Toyota",
    "model": "Corolla",
    "year": 2012,
    "value": 100000.0
  },
  "deductible_percentage": 0.1,
  "broker_fee": 50.0
}
```

## Testes

```bash
pytest -q
```

## Docker

```bash
docker build -t agro-brasil .
docker run --rm -p 8000:8000 agro-brasil
```