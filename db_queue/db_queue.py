from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from sqlalchemy import text
from datetime import datetime


async def fecth_task(db: AsyncSession, worker_id):
    query = text(
        """
        SELECT id, task_name
        FROM tasks
        WHERE status = 'pending'
        LIMIT 1
        FOR UPDATE SKIP LOCKED
        """
    )
    try:
        result = await db.execute(query)
        task = result.mappings().fetchone()

        if not task:
            return None
    except Exception as e:
        raise Exception(f"Ошибка при получении задачи: {e}")

    update_query = text(
        """
        UPDATE tasks
        SET status = 'processing'
        worker_id = :worker_id
        updated_at = :updated_at
        WHERE id = :id
        """
    )
    try:
        await db.execute(
            update_query, 
            {
                "worker_id": worker_id,
                "updated_at": datetime.now(),
                "id": task["id"]
            }
        )
        await db.commit()

    except Exception as e:
        await db.rollback()
        raise Exception(f"Ошибка при обновлении задачи: {e}")

    return task


async def worker_process(worker_id):
    async with get_db() as db:
        while True:
            task = await fecth_task(db, worker_id)
            if not task:
                return "Нет доступных задач"
            try:
                # решение задачи

                update_query = text(
                    """
                    UPDATE tasks
                    SET status = 'completed'
                    worker_id = :worker_id
                    updated_at = :updated_at
                    WHERE id = :id
                    """
                )

                await db.execute(
                    update_query,
                    {
                        "worker_id": worker_id,
                        "updated_at": datetime.now(),
                        "id": task["id"],
                    },
                )
                await db.commit()

            except Exception as e:
                await db.rollback()
                raise Exception(f"Ошибка при обновлении статуса задачи: {e}")
