import asyncio
from playwright.async_api import async_playwright


async def save_first_search_result_content(search_url, output_file):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto(search_url)

        await page.wait_for_selector('div#search')

        first_link = await page.eval_on_selector('div#search a', 'element => element.href')

        new_page = await browser.new_page()
        await new_page.goto(first_link)

        content = await new_page.content()

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        await new_page.close()

        await browser.close()


search_url = "https://www.google.com/search?q=site%3Atr.linkedin.com%2Fcompany&sca_esv=8dca5a6e4fb2a16a&sca_upv=1&rlz=1C1GCEU_trTR1008TR1008&sxsrf=ADLYWILbO5iqFvjkPxPybT9kKqxmc1H1rw%3A1721903430559&ei=RimiZtDeIfqL7NYPwZ_V8Qg&ved=0ahUKEwjQmcOS_sGHAxX6BdsEHcFPNY4Q4dUDCA8&uact=5&oq=site%3Atr.linkedin.com%2Fcompany&gs_lp=Egxnd3Mtd2l6LXNlcnAiHHNpdGU6dHIubGlua2VkaW4uY29tL2NvbXBhbnlIAFAAWABwAHgAkAEAmAEAoAEAqgEAuAEDyAEAmAIAoAIAmAMAkgcAoAcA&sclient=gws-wiz-serp"
output_file = "search_result.html"

asyncio.run(save_first_search_result_content(search_url, output_file))
