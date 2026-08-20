import asyncio

from generator.copy_tools import derive_visual_prompt, generate_headlines
from generator.file_tools import get_campaign_dir, save_image_from_url
from generator.image_tools import generate_images_concurrent
from generator.models import CampaignBrief


async def main() -> None:
    brief = CampaignBrief(
        product="Athen's Lemonade",
        key_message="Handcrafted lemonade for spontaneous, sun-drenched summer moments.",
        target_audience=(
            "Style-conscious young adults (18-30) drawn to nostalgic, "
            "vintage-inspired aesthetics and slow, sunny days"
        ),
        tone="playful, nostalgic, spontaneous",
        style_guide=(
            "Sunflower yellow, cherry red, cream, dark green, and amber color "
            "palette; nostalgic early-2000s fashion editorial photography with "
            "a Mediterranean feel, no identifiable landmarks; hard direct "
            "summer sunlight with a subtle frontal flash; wide-angle 24mm lens "
            "with playful perspective distortion, 35mm film grain, slightly "
            "overexposed highlights, casual imperfect crop"
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

    campaign_dir = get_campaign_dir("athens-lemonade")
    for i, result in enumerate(results):
        if not result.success:
            print(f"Image {i} failed: {result.error}")
            continue
        save_path = campaign_dir / f"variant-{i}.webp"
        save_image_from_url(result.source_url, save_path)
        result.local_path = str(save_path)
        print(f"Saved {save_path}")


if __name__ == "__main__":
    asyncio.run(main())
