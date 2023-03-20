# Use an official Node.js runtime as a parent image
FROM node:14

# Set the working directory to /app
WORKDIR /app

# Copy the HTML file and package.json to the container
COPY index.html .
COPY package.json .

# Install any needed packages specified in package.json
RUN npm install

# Make port 8081 available to the world outside this container
EXPOSE 8081

# Run the command to start the web server and serve the HTML file
CMD ["npm", "start"]

