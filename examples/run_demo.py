import asyncio

from generator.copy_tools import derive_visual_prompt, generate_headlines
from generator.file_tools import get_campaign_dir, save_image_from_url
from generator.image_tools import generate_images_concurrent
from generator.models import CampaignBrief


async def main() -> None:
    brief = CampaignBrief(
        product="Aurora Trail Running Shoes",
        key_message="Engineered for unpredictable terrain, built for confident strides.",
        target_audience="Weekend trail runners aged 25-45 who value durability and grip",
        tone="energetic, adventurous",
        style_guide=(
            "Bold sans-serif type, earthy color palette (moss green, clay "
            "orange), high-contrast outdoor photography"
        ),
    )

    print("Generating headline variants...")
    headline_set = generate_headlines(brief, n=4)
    for variant in headline_set.variants:
        print(f"\n[{variant.tone}] {variant.headline}")
        print(f"  -> {variant.reasoning}")

    print("\nDeriving visual prompts...")
    prompts = [derive_visual_prompt(v, brief) for v in headline_set.variants]
    for prompt in prompts:
        print(f"  - {prompt}")

    print("\nGenerating images (Recraft)...")
    results = await generate_images_concurrent(prompts, provider="recraft")

    campaign_dir = get_campaign_dir("demo-run")
    for i, result in enumerate(results):
        if not result.success:
            print(f"Image {i} failed: {result.error}")
            continue
        save_path = campaign_dir / f"variant-{i}.png"
        save_image_from_url(result.file_path, save_path)
        print(f"Saved {save_path}")


if __name__ == "__main__":
    asyncio.run(main())
