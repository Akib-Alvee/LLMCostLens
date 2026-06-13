import asyncio
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionFactory, engine
from app.models.model_pricing import ModelPricing

MODEL_PRICING = (
    ("local-mock", Decimal("0"), Decimal("0")),
    ("gpt-4o-mini", Decimal("0.00015"), Decimal("0.00060")),
    ("gpt-4o", Decimal("0.005"), Decimal("0.015")),
)


async def seed_model_pricing(session: AsyncSession) -> int:
    model_names = [model_name for model_name, _, _ in MODEL_PRICING]
    result = await session.execute(
        select(ModelPricing.model_name).where(ModelPricing.model_name.in_(model_names))
    )
    existing_model_names = set(result.scalars())

    pricing_rows = [
        ModelPricing(
            model_name=model_name,
            input_cost_per_1k_tokens=input_cost,
            output_cost_per_1k_tokens=output_cost,
        )
        for model_name, input_cost, output_cost in MODEL_PRICING
        if model_name not in existing_model_names
    ]
    session.add_all(pricing_rows)
    return len(pricing_rows)


async def main() -> None:
    async with AsyncSessionFactory.begin() as session:
        created_count = await seed_model_pricing(session)

    await engine.dispose()
    print(f"Created {created_count} model pricing row(s).")


if __name__ == "__main__":
    asyncio.run(main())
