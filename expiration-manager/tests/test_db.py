import pytest
import pytest_asyncio
from unittest.mock import AsyncMock
from .expiration_manager.db import DataBase

@pytest_asyncio.fixture
async def mock_db(mocker):
    mocker.patch("api.db.create_async_engine", autospec=True)
    mock_sessionmaker = mocker.patch("api.db.async_sessionmaker", autospec=True)
    mock_session = AsyncMock()
    mock_sessionmaker.return_value = AsyncMock(return_value=mock_session)
    db = DataBase()
    async with db as db_instance:
        yield db_instance, mock_session

@pytest.mark.asyncio
async def test_init(mock_db):
    db, _ = mock_db
    assert isinstance(db, DataBase)

@pytest.mark.asyncio
async def test_aenter(mock_db):
    db, _ = mock_db
    assert isinstance(db, DataBase)

@pytest.mark.asyncio
async def test_delete_after_time(mock_db):
    db, mock_session = mock_db

    mock_session.execute = AsyncMock()
    mock_session.commit = AsyncMock()

    mock_session.execute.return_value.rowcount = 5

    result = await db.delete_after_time()

    assert result == 5
    mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_delete_after_time_error(mock_db):
    db, mock_session = mock_db

    mock_session.execute = AsyncMock(side_effect=Exception("DB error"))
    mock_session.rollback = AsyncMock()

    result = await db.delete_after_time()

    assert result == 0
    mock_session.rollback.assert_awaited_once()
