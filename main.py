import threading
from playwright.async_api import async_playwright
import asyncio
from player import Player, VALID_POSITIONS, TEAM_ABBR_MAPPING
from track_available_players import update_available_players, app


def parse_text_for_name_team_and_position(text):
    name_team_pos_parts = text.strip().split("\n")
    if len(name_team_pos_parts) < 3:
        return
    name = name_team_pos_parts[0]
    
    name_team_pos_parts = name_team_pos_parts[1:]
    def search_across_name_team_pos_parts(mapping):
        for k in mapping:
            for name_team_pos_part in name_team_pos_parts:
                if k.lower() == name_team_pos_part.strip().lower():
                    return mapping[k]
    
    team = search_across_name_team_pos_parts(TEAM_ABBR_MAPPING)
    pos = search_across_name_team_pos_parts(VALID_POSITIONS)
    if team is not None and pos is not None:
        return (name, team, pos)
    

async def main():
    async with async_playwright() as p:
        # Launch a persistent browser so it stays open
        browser = await p.chromium.launch(headless=False, args=["--start-maximized"])
        await browser.new_context(no_viewport=True) # Setting viewport to None is crucial
        page = await browser.new_page(no_viewport=True)

        # Open your draft page (replace with your actual URL)
        await page.goto("https://fantasy.espn.com/football/team?leagueId=563621580&teamId=1")

        # Example: wait for new page (tab) after clicking a link

        picked_players = set()
        print("Browser opened, monitoring picks every 2 seconds...")
        while True:
            prev_picked_players = picked_players.copy()
            contexts = browser.contexts
            for ctx in contexts:
                for page in ctx.pages:
                    if not page.url.startswith("https://fantasy.espn.com/football/draft"):
                        continue

                    try:
                        # Grab all picks currently on the page
                        picks = await page.query_selector_all(".pick-history-tables .player-details")

                        for pick in picks:
                            pick_text = (await pick.inner_text()).strip()
                            name_team_pos = parse_text_for_name_team_and_position(pick_text)
                            if name_team_pos:
                                picked_players.add(Player(name=name_team_pos[0], team=name_team_pos[1], position=name_team_pos[2]))

                    except Exception as e:
                        print("Error during polling:", e)
            
            if picked_players != prev_picked_players:
                update_available_players(picked_players)
            await asyncio.sleep(2)

        # If you ever want to close:
        # await browser.close()

def run_flask():
    app.run(debug=True, use_reloader=False)

flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

asyncio.run(main())