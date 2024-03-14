import asyncio
import logging

from shazamio import Shazam, Serialize

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - [%(filename)s:%(lineno)d - %(funcName)s()] - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


async def main():


    shazam = Shazam()



    # pass path
    new_version_path = await shazam.recognize("test/Are You Ready.mp3")
    serialized_new_path = Serialize.full_track(new_version_path)
    print(serialized_new_path)

    # pass bytes
    with open("test/Are You Ready.mp3", "rb") as file:
        new_version_path = await shazam.recognize(file.read())
        serialized_new_path = Serialize.full_track(new_version_path)
        print(serialized_new_path)


loop = asyncio.get_event_loop_policy().get_event_loop()
loop.run_until_complete(main())
