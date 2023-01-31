FROM python:3.10
ADD bot.py .
RUN pip install discord.py
CMD ["python", "./bot.py"]