# =====================================================
#  🐍 NY CREATION - Dockerfile
# =====================================================
#  🚀 Author   : Nand Yaduwanshi (@Tmzeroo)
#  📢 Channel  : @CreativeYdv
#  🏗 Purpose  : Containerized Deployment of nand.py
# =====================================================

# 🏗 STEP 1: Use an official Python 3.9 slim image
FROM python:3.9-slim

# 🏠 STEP 2: Set the working directory inside the container
WORKDIR /app

# 📥 STEP 3: Copy all project files into the container
COPY . .

# 🛠 STEP 4: Update & Install required dependencies
RUN apt-get update && apt-get install -y \
    && pip install --no-cache-dir telebot flask aiogram pyTelegramBotAPI pymongo aiohttp

# 🔓 STEP 5: Grant execution permissions to all files
RUN chmod +x *

# 🌐 STEP 6: Expose port 8080 (If Flask is used)
EXPOSE 8080

# 🎬 STEP 7: Command to start the application
CMD ["python3", "nand.py"]

# =====================================================
#  🔥 DEPLOY & RUN USING:
#  docker build -t nycreation .
#  docker run -d --name NY_Creation nycreation
# =====================================================
