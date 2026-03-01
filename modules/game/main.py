import asyncio
try:
    from webgame import Game
except ImportError:
    from modules.game.webgame import Game
async def main():
    game = Game()
    await game.run()

if __name__ == "__main__":
    asyncio.run(main())