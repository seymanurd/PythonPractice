import asyncio
from playwright.async_api import async_playwright
import csv

async def get_links(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(url)
        
        all_links = []

        while True:
            await page.wait_for_selector('div#search')

            links = await page.eval_on_selector_all('div#search a', 'elements => elements.map(element => element.href)')
            all_links.extend(links)

            next_button = await page.query_selector('a#pnnext')
            if next_button:
                await next_button.click()
                await page.wait_for_timeout(2000)  
            else:
                break
        
        await browser.close()
        
        return all_links

url = "https://www.google.com/search?q=site%3Atr.linkedin.com%2Fcompany&sca_esv=8dca5a6e4fb2a16a&sca_upv=1&rlz=1C1GCEU_trTR1008TR1008&sxsrf=ADLYWILbO5iqFvjkPxPybT9kKqxmc1H1rw%3A1721903430559&ei=RimiZtDeIfqL7NYPwZ_V8Qg&ved=0ahUKEwjQmcOS_sGHAxX6BdsEHcFPNY4Q4dUDCA8&uact=5&oq=site%3Atr.linkedin.com%2Fcompany&gs_lp=Egxnd3Mtd2l6LXNlcnAiHHNpdGU6dHIubGlua2VkaW4uY29tL2NvbXBhbnlIAFAAWABwAHgAkAEAmAEAoAEAqgEAuAEDyAEAmAIAoAIAmAMAkgcAoAcA&sclient=gws-wiz-serp"

links = asyncio.run(get_links(url))

filtered_links = [link for link in links if link.startswith("https://tr.linkedin.com/company")]

csv_filename = 'link.csv'

with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    
    csvwriter.writerow(['Company Links'])
    
    for link in filtered_links:
        csvwriter.writerow([link])

print(f'Links written in "{csv_filename}" file.')
