# Step 1: Use a base image with Python installed
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requiremts.txt file to the container
COPY requiremts.txt .

# Step 4: Install the dependencies
RUN pip install --no-cache-dir -r requiremts.txt

# Step 5: Copy the rest of the application code into the container
COPY . .

# Step 6: Expose the port that Flask will run on
EXPOSE 5000

# Step 7: Define the command to run your application
CMD ["python", "app.py"]
