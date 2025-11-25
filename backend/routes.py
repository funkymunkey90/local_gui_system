"""Stores all routing calls"""
from fastapi import APIRouter
from modules.sqlite_manager import SQLite_Man

router = APIRouter()


@router.get("/db/tables")
async def list_tables() -> dict:
    """Return list of tables in the connected SQLite DB."""
    _query = "SELECT name FROM sqlite_master WHERE type='table';"
    # Use existing SQLite_Man; it's expected main.py has connected it already
    try:
        SQLite_Man.execute_async(query=_query)
        _table_list = [row[0] for row in SQLite_Man.fetchall()]
    except ValueError:
        _table_list = None
    return {"counting": len(_table_list) if _table_list is not None else 0, "tables": _table_list}


@router.get("/db/ping")
async def ping() -> dict:
    """pings connection"""
    return {"status": "ok", "note": "This route is provided by backend/routes.py"}
