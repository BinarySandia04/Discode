from .base import Base

class Python(Base):
    async def run(self, code, discode, author, channel):
        await discode.sendMessage("It works???", channel)
