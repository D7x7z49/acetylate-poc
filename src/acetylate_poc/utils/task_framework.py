import asyncio
from functools import wraps


class AsyncTaskFramework:

    def __init__(self, file_path, queue_size=300, task_num=7) -> None:
        self.file_path = file_path
        self.queue_size = queue_size
        self.task_num = task_num

    
    def main(self, task_fun):
        def decorator(file_iterator):
            queue = asyncio.Queue(self.queue_size)

            tasks = []
            zfill_length = len(str(self.task_num))
            for i in range(self.task_num):
                task = asyncio.create_task(task_fun(f'task-{i:0{zfill_length}d}', queue))
                tasks.append(task)

            @wraps(file_iterator)
            async def wrapper(*args, **kwargs):
                if asyncio.iscoroutinefunction(file_iterator):
                    async for target in file_iterator(*args, **kwargs):
                        await queue.put(target)
                else:
                    for target in file_iterator(*args, **kwargs):
                        await queue.put(target)

                await queue.join()
                for task in tasks:
                    task.cancel()

                await asyncio.gather(*tasks, return_exceptions=True)

            return wrapper
        return decorator



if __name__ == "__main__":

    async def example_task(name, queue):
        while True:
            item = await queue.get()
            if item:
                asyncio.sleep(1)
                print(f"Task {name} processed item: {item}")
            queue.task_done()



    async def main():

        tf = AsyncTaskFramework(file_path='', queue_size=2, task_num=2)

        tf.main(example_task)
        async def file_iterator(num):
            for i in range(num):
                yield i
        async for i in file_iterator(5):
            print(i)

    asyncio.run(main())
    