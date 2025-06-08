import os
from dotenv import load_dotenv
import logging

from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("Trello MCP Server")

@mcp.tool()
def get_health_status() -> str:
    """サーバーのヘルスステータスを返します。"""
    return "OK"

if __name__ == "__main__":
    load_dotenv()  # .env ファイルをロード
    trello_api_key = os.getenv("TRELLO_API_KEY")
    if trello_api_key:
        logger.info(f"TRELLO_API_KEY loaded: {trello_api_key[:4]}...{trello_api_key[-4:]}")
    else:
        logger.warning("TRELLO_API_KEY not found or empty.")

    trello_token = os.getenv("TRELLO_TOKEN")
    if trello_token:
        logger.info(f"TRELLO_TOKEN loaded: {trello_token[:4]}...{trello_token[-4:]}")
    else:
        logger.warning("TRELLO_TOKEN not found or empty.")

    trello_board_id = os.getenv("TRELLO_BOARD_ID")
    if trello_board_id:
        logger.info(f"TRELLO_BOARD_ID loaded: {trello_board_id}")
    else:
        logger.warning("TRELLO_BOARD_ID not found or empty.")

    trello_workspace_id = os.getenv("TRELLO_WORKSPACE_ID")
    if trello_workspace_id:
        logger.info(f"TRELLO_WORKSPACE_ID loaded: {trello_workspace_id}")
    else:
        logger.warning("TRELLO_WORKSPACE_ID not found or empty.")

    mcp.run()
